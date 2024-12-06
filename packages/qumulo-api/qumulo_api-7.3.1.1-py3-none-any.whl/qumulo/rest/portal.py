# Copyright (c) 2024 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from dataclasses import dataclass
from typing import Dict, List, Optional

from dataclasses_json import DataClassJsonMixin

import qumulo.lib.request as request

from qumulo.lib.uri import MonitorURI

DEFAULT_PORTAL_PORT_NUMBER = 3713


@dataclass
class HubPortal(DataClassJsonMixin):
    id: int
    state: str
    root: str
    root_path: Optional[str]
    spoke_cluster_uuid: str
    spoke_cluster_name: str
    spoke_address: Optional[str]
    spoke_port: Optional[int]
    spoke_type: str


@dataclass
class SpokePortal(DataClassJsonMixin):
    id: int
    state: str
    spoke_root: str
    spoke_root_path: str
    spoke_type: str
    hub_root: Optional[str]
    hub_address: Optional[str]
    hub_port: Optional[int]
    hub_id: Optional[int]


@dataclass
class EvictionResult(DataClassJsonMixin):
    evicted_blocks: int


@dataclass
class EvictionSettings(DataClassJsonMixin):
    # Fraction of free total cluster capacity that the system will try to maintain by evicting
    # cached spoke portal data, in the range [0.0, 1.0].
    # 0 means no eviction, 1 means always try to evict.
    free_threshold: float


class Portal:
    def __init__(self, client: request.SendRequestObject):
        self.client = client

    def create_portal(self, spoke_root: str, is_writable_spoke: bool = False) -> int:
        method = 'POST'
        uri = '/v1/portal/spokes/'

        body: Dict[str, object] = {'spoke_root': spoke_root, 'is_writable_spoke': is_writable_spoke}
        return int(self.client.send_request(method, uri, body=body).data)

    def propose_hub_portal(
        self, spoke_id: int, hub_address: str, hub_port: int, hub_root: str
    ) -> SpokePortal:
        method = 'POST'
        uri = f'/v1/portal/spokes/{spoke_id}/propose'

        body: Dict[str, object] = {
            'hub_root': hub_root,
            'hub_address': hub_address,
            'hub_port': hub_port,
        }

        response = self.client.send_request(method, uri, body=body)
        return self._decode_spoke_portal(response.data)

    def authorize_hub_portal(
        self, portal_id: int, spoke_address: str, spoke_port: int
    ) -> HubPortal:
        method = 'POST'
        uri = f'/v1/portal/hubs/{portal_id}/authorize'
        body: Dict[str, object] = {'spoke_address': spoke_address, 'spoke_port': spoke_port}

        response = self.client.send_request(method, uri, body=body)
        return self._decode_hub_portal(response.data)

    def get_hub_portal(self, portal_id: int) -> HubPortal:
        method = 'GET'
        uri = f'/v1/portal/hubs/{portal_id}'

        response = self.client.send_request(method, uri)
        return self._decode_hub_portal(response.data)

    def get_spoke_portal(self, portal_id: int) -> SpokePortal:
        method = 'GET'
        uri = f'/v1/portal/spokes/{portal_id}'
        response = self.client.send_request(method, uri)
        return self._decode_spoke_portal(response.data)

    def modify_hub_portal(self, portal_id: int, spoke_address: str, spoke_port: int) -> HubPortal:
        method = 'PATCH'
        uri = f'/v1/portal/hubs/{portal_id}'
        body: Dict[str, object] = {'spoke_address': spoke_address, 'spoke_port': spoke_port}

        response = self.client.send_request(method, uri, body=body)
        return self._decode_hub_portal(response.data)

    def modify_spoke_portal(self, portal_id: int, hub_address: str, hub_port: int) -> SpokePortal:
        method = 'PATCH'
        uri = f'/v1/portal/spokes/{portal_id}'
        body: Dict[str, object] = {'hub_address': hub_address, 'hub_port': hub_port}
        response = self.client.send_request(method, uri, body=body)
        return self._decode_spoke_portal(response.data)

    def delete_hub_portal(self, portal_id: int) -> None:
        method = 'DELETE'
        uri = f'/v1/portal/hubs/{portal_id}'
        self.client.send_request(method, uri)

    def delete_spoke_portal(self, portal_id: int) -> None:
        method = 'DELETE'
        uri = f'/v1/portal/spokes/{portal_id}'
        self.client.send_request(method, uri)

    def list_hub_portals(self) -> List[HubPortal]:
        method = 'GET'
        uri = '/v1/portal/hubs/'

        responses = self.client.send_request(method, uri).data['entries']
        results: List[HubPortal] = []

        for response in responses:
            results.append(self._decode_hub_portal(response))

        return results

    def list_spoke_portals(self) -> List[SpokePortal]:
        method = 'GET'
        uri = '/v1/portal/spokes/'

        responses = self.client.send_request(method, uri).data['entries']
        results: List[SpokePortal] = []

        for response in responses:
            skeleton = {'hub_root': None, 'hub_address': None, 'hub_port': None, 'hub_id': None}
            skeleton.update(response)
            results.append(SpokePortal.from_dict(skeleton))

        return results

    def evict_link(self, portal_id: int, dir_id: str, name: str) -> EvictionResult:
        method = 'POST'
        uri = f'/v1/portal/spokes/{portal_id}/evict-link'

        body = {'dir_id': dir_id, 'name': name}
        response = self.client.send_request(method, uri, body=body)
        return EvictionResult.schema().load(response.data)

    def evict_data(self, portal_id: int, file_id: str) -> EvictionResult:
        method = 'POST'
        uri = f'/v1/portal/spokes/{portal_id}/evict-data'

        body = {'file_id': file_id}
        response = self.client.send_request(method, uri, body=body)
        return EvictionResult.schema().load(response.data)

    def evict_tree(self, portal_id: int, dir_id: str) -> MonitorURI:
        method = 'POST'
        uri = f'/v1/portal/spokes/{portal_id}/evict-tree'

        body = {'dir_id': dir_id}
        response = self.client.send_request(method, uri, body=body)
        return MonitorURI.schema().load(response.data)

    def get_eviction_settings(self) -> request.ResponseWithEtag[EvictionSettings]:
        response = self.client.send_request('GET', '/v1/portal/spokes/eviction-settings')
        assert response.etag is not None
        return request.ResponseWithEtag(
            EvictionSettings.schema().load(response.data), response.etag
        )

    def set_eviction_settings(
        self, config: EvictionSettings, etag: Optional[str] = None
    ) -> request.ResponseWithEtag[EvictionSettings]:
        response = self.client.send_request(
            'PUT', '/v1/portal/spokes/eviction-settings', body=config.to_dict(), if_match=etag
        )
        assert response.etag is not None
        return request.ResponseWithEtag(
            EvictionSettings.schema().load(response.data), response.etag
        )

    @staticmethod
    def _decode_spoke_portal(portal: Dict[str, object]) -> SpokePortal:
        return SpokePortal.from_dict(portal, infer_missing=True)

    @staticmethod
    def _decode_hub_portal(portal: Dict[str, object]) -> HubPortal:
        return HubPortal.from_dict(portal, infer_missing=True)
