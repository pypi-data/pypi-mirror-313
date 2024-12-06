import bpkio_cli.utils.prompt as prompt
import click
from bpkio_api.models import ServiceIn, SourceIn
from bpkio_api.models.common import summary
from bpkio_cli.core.exceptions import UsageError
from bpkio_cli.core.resource_chain import ResourceChain
from bpkio_cli.utils.url_builders import (get_service_handler,
                                          get_source_handler)
from bpkio_cli.writers.breadcrumbs import display_tip


def retrieve_api_resource_from_chain(
    id: int | str | None = None,
    endpoint_path: list = [],
    **kwargs,
):
    """A helper function to retrieve a broadpeak.io resource from the APIs"""
    ctx = click.get_current_context()

    # retrieve the identifiers
    resource_chain: ResourceChain = ctx.obj.resource_chain
    if not id:
        id, _ = resource_chain.last()
    parent_id, _ = resource_chain.parent()

    api = ctx.obj.api
    endpoint = api.get_endpoint_from_path(endpoint_path)

    # 2nd level resources (eg. slots)
    if parent_id:
        resource = endpoint.retrieve(parent_id, id, **kwargs)

    # root-level resources (eg. sources)
    else:
        if isinstance(id, int) or str(id).isdigit():
            id = int(id)
            resource = endpoint.retrieve(id, **kwargs)
        else:
            input_id = id
            # Fuzzy search on possible matching resources
            resources = endpoint.search(id, **kwargs)
            if len(resources) == 0:
                raise UsageError(f"No resource found for argument '{id}'")

            if len(resources) > 1:
                # first check if it's not already been resolved a step before (for breadcrumbs)
                if ctx.obj.current_resource in resources:
                    resource = ctx.obj.current_resource
                else:
                    resource = prompt.fuzzy(
                        message="More than one matching resource. Which one do you mean?",
                        choices=[
                            prompt.Choice(
                                res,
                                name=summary(res, with_class=True),
                            )
                            for res in resources
                        ],
                    )

            else:
                resource = resources[0]

            display_tip(f"Resource '{input_id}' resolved to '{resource.id}'")

    # "resolve" the resource in the chain
    resource_chain.overwrite_last(id, resource)

    # Record the resource
    if ctx.obj.cache and hasattr(resource, "id"):
        ctx.obj.cache.record(resource)

    return resource


def get_api_endpoint(path: list):
    api = click.get_current_context().obj.api
    return api.get_endpoint_from_path(path)


def get_content_handler(
    resource,
    replacement_fqdn=None,
    extra_url=None,
    additional_query_params=(),
    additional_headers=(),
    subplaylist_index=None,
    user_agent=None,
    session=None,
    service_as_param=False,
):
    api = click.get_current_context().obj.api

    if isinstance(resource, SourceIn):
        # check if the resource config has headers configured
        if (
            hasattr(resource, "origin")
            and resource.origin
            and len(resource.origin.customHeaders)
        ):
            for custom_header in resource.origin.customHeaders:  # type: ignore
                additional_headers = additional_headers + (
                    f"{custom_header.name}={custom_header.value}",
                )

        return get_source_handler(
            resource,
            extra_url=extra_url,
            additional_query_params=additional_query_params,
            additional_headers=additional_headers,
            subplaylist_index=subplaylist_index,
            user_agent=user_agent,
        )

    if isinstance(resource, ServiceIn):
        if (
            hasattr(resource, "advancedOptions")
            and resource.advancedOptions.authorizationHeader
        ):
            additional_headers = additional_headers + (
                f"{resource.advancedOptions.authorizationHeader.name}={resource.advancedOptions.authorizationHeader.value}",
            )

        if session:
            additional_query_params = additional_query_params + (
                f"bpkio_sessionid={session}",
            )

        return get_service_handler(
            resource,
            replacement_fqdn=replacement_fqdn,
            extra_url=extra_url,
            additional_query_params=additional_query_params,
            additional_headers=additional_headers,
            subplaylist_index=subplaylist_index,
            api=api,
            user_agent=user_agent,
            service_as_param=service_as_param,
        )
