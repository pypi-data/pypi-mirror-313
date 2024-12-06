import json
import uuid
from typing import Dict, List

import bpkio_api.mappings as mappings
import bpkio_api.models as models
from bpkio_api.api import BroadpeakIoApi
from bpkio_api.endpoints.enums import UpsertOperationType
from bpkio_api.models.common import summary
from bpkio_cli.click_mods.plugin_functions import get_shared_function
from bpkio_cli.core.logging import logger
from pydantic import BaseModel


class ResourcePackager:
    def __init__(self, api) -> None:
        self.api: BroadpeakIoApi = api
        self.resources: List[models.BaseResource] = []
        self.id_mappings: Dict = {}
        self.in_resources: List = []

    def extract(self):
        pass

    def package(self, root_resources: List[BaseModel]):
        for resource in root_resources:
            self._discover(resource)

        # Remove duplicates
        self._dedupe()

        return self._prepare()

    def _discover(self, model):
        """Function to traverse a resource and retrieve all its dependents,
        in a recursive way.

        Args:
            model (BaseResource): The root resource (or model) to start from
        """
        if isinstance(model, models.BaseResource):

            # Get full version of the model if it's a sparse one
            if type(model) is models.ServiceSparse:
                model = self.api.services.retrieve(model.id)
            if type(model) is models.SourceSparse:
                model = self.api.sources.retrieve(model.id)

            # Add it to the list of things to save
            self.resources.append(model)

        # then go through pydantic object and find dependents recursively
        if isinstance(model, BaseModel):
            for field_name, field_value in model:
                if field_value:
                    if isinstance(field_value, models.BaseResource):
                        endpoint = mappings.model_to_endpoint(
                            self.api, model=type(field_value)
                        )
                        if endpoint and hasattr(endpoint, "retrieve"):
                            dependent = endpoint.retrieve(field_value.id)
                            logger.info(
                                f"Found dependent: {summary(dependent, with_class=True)}"
                            )
                            self._discover(dependent)
                        else:
                            logger.error(
                                f"No retrieve endpoint for resource of type {field_value.__class__.__name__}"
                            )

                    elif isinstance(field_value, BaseModel):
                        self._discover(field_value)

                    elif isinstance(field_value, list):
                        for v in field_value:
                            self._discover(v)

    def _dedupe(self):
        seen = set()
        result = []
        for item in reversed(self.resources):
            if item.id not in seen:
                seen.add(item.id)
                result.append(item)
        result.reverse()
        self.resources = result

    def _prepare(self):
        """Goes through the list of resources extracted by self._discover,
        find and generalises all relations, and prepares a JSON package
        that can be deployed.
        """

        def replace_guid_with_id(model):
            if isinstance(model, BaseModel):
                for field_name, field_value in model:
                    if field_name == "id" and field_value in self.id_mappings:
                        setattr(model, field_name, self.id_mappings[field_value])
                    else:
                        replace_guid_with_id(field_value)
            elif isinstance(model, list):
                for item in model:
                    replace_guid_with_id(item)

        for resource in reversed(self.resources):
            # Extract original ID
            orig_id = resource.id

            # Create a GUID to replace it with
            guid = str(uuid.uuid4())

            self.id_mappings[orig_id] = guid

            # Transform the resource into an IN model
            in_obj = mappings.to_input_model(resource)

            # Replace dependent IDs in it
            replace_guid_with_id(in_obj)

            # Make a JSON payload from it
            json_payload = json.loads(in_obj.json())

            # Record it
            self.in_resources.append(
                dict(guid=guid, model=in_obj.__class__.__name__, payload=json_payload)
            )

        return self.in_resources


class PackageInstaller:
    def __init__(self, api, name_prefix: str | None = None) -> None:
        self.guid_mappings: Dict = {}
        self.resources: Dict = {}
        self.api = api
        self._prefix = name_prefix

    def deploy(self, package: list):
        def replace_guid_with_id(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == "id" and value in self.guid_mappings:
                        obj[key] = self.guid_mappings[value]
                    else:
                        replace_guid_with_id(value)
            elif isinstance(obj, list):
                for i, value in enumerate(obj):
                    replace_guid_with_id(value)

        for instruction in package:
            payload = instruction["payload"]

            # Replace the GUIDs with IDs (if any)
            replace_guid_with_id(payload)

            # Parse it into the pydantic model
            model: BaseModel = getattr(models, instruction["model"])
            in_obj = model.parse_obj(payload)

            # Ensure name unicity (for models that can be duplicated)
            # if self._prefix and isinstance(in_obj, (models.ServiceIn)):
            if self._prefix:
                in_obj.name = self._prefix + " " + in_obj.name

            # Create it
            try:
                message = ""
                endpoint = mappings.model_to_endpoint(self.api, model=model)

                # Special handling for objects that require admin access.
                if instruction["model"] == "TranscodingProfileIn":
                    # TODO - first check whether it already exists (by name)
                    create_profile_function = get_shared_function("create_profile")
                    (resource, status) = create_profile_function(
                        profile=in_obj,
                        tenant=self.api.get_tenant_id(),
                        upsert=True,
                    )
                else:
                    if hasattr(endpoint, "upsert"):
                        (resource, status) = endpoint.upsert(
                            in_obj, if_exists="retrieve"
                        )
                    elif hasattr(endpoint, "create"):
                        resource = endpoint.create(in_obj)
                        status = UpsertOperationType.CREATED
                    else:
                        raise Exception(f"No create endpoint for model {model}")
            except Exception as e:
                resource = in_obj
                status = UpsertOperationType.ERROR
                message = e.args[0]

            logger.info(
                "{}: {} {} {} ({})".format(
                    status.name,
                    resource.__class__.__name__,
                    resource.name,
                    getattr(resource, "id", ""),
                    message,
                )
            )

            # Record the new ID, and map it to the guid
            if hasattr(resource, "id"):
                self.guid_mappings[instruction["guid"]] = resource.id
                self.resources[resource.id] = (resource, status, message)
            else:
                self.resources[resource.name] = (resource, status, message)

        return self.resources
