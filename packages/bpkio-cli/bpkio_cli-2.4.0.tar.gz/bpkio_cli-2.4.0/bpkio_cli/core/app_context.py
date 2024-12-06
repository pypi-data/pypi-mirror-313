from typing import Optional

from bpkio_api.api import BroadpeakIoApi
from bpkio_api.credential_provider import TenantProfileProvider
from bpkio_api.models import Tenant
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.resource_chain import ResourceChain
from bpkio_cli.core.resource_recorder import ResourceRecorder
from bpkio_cli.core.response_handler import ResponseHandler
from bpkio_cli.utils.httpserver import LocalHTTPServer


class AppContext:
    def __init__(self, api: BroadpeakIoApi, tenant_provider=None):
        self.api = api
        self.tenant_provider: TenantProfileProvider = tenant_provider
        self._tenant: Optional[Tenant] = None

        self.flags = dict()
        self.resource_chain = ResourceChain()
        self.cache: ResourceRecorder = ResourceRecorder("no.fqdn", "no.tenant")
        self.response_handler = ResponseHandler(self.cache)
        self.config = CONFIG
        self.local_server: Optional[LocalHTTPServer] = None

    @property
    def current_resource(self):
        return self.resource_chain.last()[1]

    @property
    def tenant(self):
        return self._tenant

    @tenant.setter
    def tenant(self, new_value: Tenant):
        self._tenant = new_value

        self.cache = ResourceRecorder(self.api.fqdn, new_value.id)
        self.response_handler = ResponseHandler(self.cache)

