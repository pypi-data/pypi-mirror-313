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

import argparse
import sys

from typing import List

import qumulo.lib.opts

from qumulo.lib.request import pretty_json, RequestError
from qumulo.lib.util import tabulate
from qumulo.rest.portal import DEFAULT_PORTAL_PORT_NUMBER as PORTAL_PORT
from qumulo.rest.portal import EvictionSettings, HubPortal, SpokePortal
from qumulo.rest_client import RestClient

JSON_HELP = 'Pretty-print JSON'
ADDR_HELP = 'The IP address of a node in the remote cluster'
PORT_HELP = 'The TCP port for portal activity on the remote cluster (3713 by default)'
HUB_ROOT_HELP = (
    'Full path to the prospective directory that will serve as the hub portal root directory'
)
SPOKE_ROOT_HELP = (
    'The full path to the directory that serves as the spoke portal root directory. Qumulo Core'
    ' creates this directory for you automatically. If this directory exists already, the system'
    ' outputs an error.'
)


def pretty_enum(state: str) -> str:
    return ' '.join([word.title() for word in state.split('_')])


def format_hub_portals(hubs: List[HubPortal], as_json: bool) -> str:
    if as_json:
        output = []
        for hub in hubs:
            out = hub.to_dict()
            output.append(out)

        return pretty_json(output)

    columns = ['ID', 'State', 'Hub Root', 'Spoke Host', 'Spoke Name']

    rows = []
    for hub in hubs:
        addr = f'{hub.spoke_address}:{hub.spoke_port}' if hub.spoke_address else '-'
        root = hub.root_path or 'Deleted'
        row = [hub.id, pretty_enum(hub.state), root, addr, hub.spoke_cluster_name]
        rows.append(row)

    return tabulate(rows, columns)


def format_spoke_portals(spokes: List[SpokePortal], as_json: bool) -> str:
    if as_json:
        output = []
        for spoke in spokes:
            out = spoke.to_dict()
            output.append(out)

        return pretty_json(output)

    columns = ['ID', 'State', 'Spoke Root', 'Hub Host', 'Hub Root ID', 'Hub Portal ID']
    rows = []

    for spoke in spokes:
        addr = f'{spoke.hub_address}:{spoke.hub_port}' if spoke.hub_address else '-'
        row = [
            spoke.id,
            pretty_enum(spoke.state),
            spoke.spoke_root_path,
            addr,
            spoke.hub_root or '-',
            spoke.hub_id or '-',
        ]
        rows.append(row)

    return tabulate(rows, columns)


class CreatePortal(qumulo.lib.opts.Subcommand):
    NAME = 'portal_create'
    SYNOPSIS = 'Create a spoke portal and propose a hub portal relationship on another cluster'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--spoke-root', required=True, help=SPOKE_ROOT_HELP)
        parser.add_argument('-a', '--hub-address', required=True, help=ADDR_HELP)
        parser.add_argument('-p', '--hub-port', default=PORTAL_PORT, help=PORT_HELP, type=int)
        parser.add_argument('--hub-root', required=True, help=HUB_ROOT_HELP)
        parser.add_argument('-j', '--json', help=JSON_HELP, action='store_true')
        parser.add_argument('-w', '--writable-spoke', help=argparse.SUPPRESS, action='store_true')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        spoke_id = rest_client.portal.create_portal(args.spoke_root, args.writable_spoke)

        try:
            spoke = rest_client.portal.propose_hub_portal(
                spoke_id, args.hub_address, args.hub_port, args.hub_root
            )
        except RequestError as e:
            context = ''

            if e.status_code // 100 == 5:
                # Server errors are presumed to be transient and can be retried
                # 4XX errors are misconfiguration or user errors and should not be retried
                context = (
                    ' Retry this operation with the following command:'
                    '\n'
                    f'portal_propose_hub --spoke-id {spoke_id} --hub-address {args.hub_address} '
                    f'--hub-port {args.hub_port} --hub-root "{args.hub_root}"'
                )

            print(
                f'Created spoke portal with ID {spoke_id}. Could not establish a relationship with '
                f'the proposed hub cluster.{context}',
                file=sys.stderr,
            )
            raise
        else:
            print(format_spoke_portals([spoke], args.json))


class GetSpokePortal(qumulo.lib.opts.Subcommand):
    NAME = 'portal_get_spoke'
    SYNOPSIS = 'Get the configuration and state for the specified spoke portal'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('-i', '--id', type=int, required=True, help='Spoke portal ID')
        parser.add_argument('-j', '--json', help=JSON_HELP, action='store_true')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        spoke = rest_client.portal.get_spoke_portal(args.id)
        print(format_spoke_portals([spoke], args.json))


class GetHubPortal(qumulo.lib.opts.Subcommand):
    NAME = 'portal_get_hub'
    SYNOPSIS = 'Get the configuration and state for the specified hub portal'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('-i', '--id', type=int, required=True, help='Hub portal ID')
        parser.add_argument('-j', '--json', help=JSON_HELP, action='store_true')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        hub = rest_client.portal.get_hub_portal(args.id)

        print(format_hub_portals([hub], args.json))


class ModifySpokePortal(qumulo.lib.opts.Subcommand):
    NAME = 'portal_modify_spoke'
    SYNOPSIS = 'Change the configuration for a spoke portal'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('-i', '--id', type=int, required=True, help='Spoke portal ID')
        parser.add_argument('-a', '--hub-address', required=True, help=ADDR_HELP)
        parser.add_argument('-p', '--hub-port', default=PORTAL_PORT, help=PORT_HELP, type=int)
        parser.add_argument('-j', '--json', help=JSON_HELP, action='store_true')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        spoke = rest_client.portal.modify_spoke_portal(args.id, args.hub_address, args.hub_port)
        print(format_spoke_portals([spoke], args.json))


class DeleteSpokePortal(qumulo.lib.opts.Subcommand):
    NAME = 'portal_delete_spoke'
    SYNOPSIS = 'Delete a spoke portal'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('-i', '--id', type=int, required=True, help='Spoke portal ID')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        rest_client.portal.delete_spoke_portal(args.id)


class ModifyHubPortal(qumulo.lib.opts.Subcommand):
    NAME = 'portal_modify_hub'
    SYNOPSIS = 'Change the configuration for a hub portal'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('-i', '--id', type=int, required=True, help='Hub portal ID')
        parser.add_argument('-a', '--spoke-address', required=True, help=ADDR_HELP)
        parser.add_argument('-p', '--spoke-port', default=PORTAL_PORT, help=PORT_HELP, type=int)
        parser.add_argument('-j', '--json', help=JSON_HELP, action='store_true')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        hub = rest_client.portal.modify_hub_portal(args.id, args.spoke_address, args.spoke_port)
        print(format_hub_portals([hub], args.json))


class DeleteHubPortal(qumulo.lib.opts.Subcommand):
    NAME = 'portal_delete_hub'
    SYNOPSIS = 'Delete a hub portal'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('-i', '--id', type=int, required=True, help='Hub portal ID')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        rest_client.portal.delete_hub_portal(args.id)


class ProposeHubPortal(qumulo.lib.opts.Subcommand):
    NAME = 'portal_propose_hub'
    SYNOPSIS = 'Propose a relationship from a spoke portal to a hub portal'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--spoke-id',
            type=int,
            required=True,
            help='The identifier of the spoke portal from which to propose a relationship',
        )
        parser.add_argument('-a', '--hub-address', required=True, help=ADDR_HELP)
        parser.add_argument('-p', '--hub-port', default=PORTAL_PORT, help=PORT_HELP, type=int)

        parser.add_argument('--hub-root', required=True, help=HUB_ROOT_HELP)

        parser.add_argument('-j', '--json', help=JSON_HELP, action='store_true')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        spoke = rest_client.portal.propose_hub_portal(
            args.spoke_id, args.hub_address, args.hub_port, args.hub_root
        )
        print(format_spoke_portals([spoke], args.json))


class AuthorizeHubPortal(qumulo.lib.opts.Subcommand):
    NAME = 'portal_authorize_hub'
    SYNOPSIS = 'Authorize the specified hub portal to activate the relationship'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-i',
            '--id',
            type=int,
            required=True,
            help='The identifier of the hub portal to authorize',
        )
        parser.add_argument(
            '-a',
            '--spoke-address',
            required=True,
            help='The IP address of a node in the spoke portal host cluster that proposed the '
            'relationship',
        )
        parser.add_argument('-p', '--spoke-port', default=PORTAL_PORT, help=PORT_HELP, type=int)

        parser.add_argument('-j', '--json', help=JSON_HELP, action='store_true')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        hub = rest_client.portal.authorize_hub_portal(args.id, args.spoke_address, args.spoke_port)
        print(format_hub_portals([hub], args.json))


class ListPortals(qumulo.lib.opts.Subcommand):
    NAME = 'portal_list'
    SYNOPSIS = 'List all accepted and pending portals on the current cluster'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('-j', '--json', help=JSON_HELP, action='store_true')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        hubs = rest_client.portal.list_hub_portals()
        spokes = rest_client.portal.list_spoke_portals()

        if args.json:
            result = {
                'hubs': [hub.to_dict() for hub in hubs],
                'spokes': [spoke.to_dict() for spoke in spokes],
            }
            print(pretty_json(result))
            return

        columns = ['ID', 'State', 'Role', 'Local Root']
        rows = [[hub.id, pretty_enum(hub.state), 'Hub', hub.root_path] for hub in hubs]

        rows.extend(
            [
                [spoke.id, pretty_enum(spoke.state), 'Spoke', spoke.spoke_root_path]
                for spoke in spokes
            ]
        )

        print(tabulate(rows, columns))


class ListHubPortals(qumulo.lib.opts.Subcommand):
    NAME = 'portal_list_hubs'
    SYNOPSIS = 'List accepted and pending hub portals on the current cluster'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('-j', '--json', help=JSON_HELP, action='store_true')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        hubs = rest_client.portal.list_hub_portals()

        print(format_hub_portals(hubs, args.json))


class ListSpokePortals(qumulo.lib.opts.Subcommand):
    NAME = 'portal_list_spokes'
    SYNOPSIS = 'List accepted and pending spoke portals on the current cluster'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('-j', '--json', help=JSON_HELP, action='store_true')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        spokes = rest_client.portal.list_spoke_portals()
        print(format_spoke_portals(spokes, args.json))


class EvictLink(qumulo.lib.opts.Subcommand):
    NAME = 'portal_evict_link'
    SYNOPSIS = 'Remove a cached link from a directory to a child file or directory'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-i',
            '--spoke-id',
            type=int,
            required=True,
            help='The identifier of the spoke portal from which to remove the cached link',
        )
        parser.add_argument(
            '--dir-id',
            type=str,
            required=True,
            help='The identifier of the parent directory from which to remove the cached link',
        )
        parser.add_argument(
            '--name',
            type=str,
            required=True,
            help='The name of the cached child file or directory to unlink',
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        res = rest_client.portal.evict_link(args.spoke_id, args.dir_id, args.name)
        print(pretty_json(res.to_dict()))


class EvictData(qumulo.lib.opts.Subcommand):
    NAME = 'portal_evict_data'
    SYNOPSIS = 'Free the capacity consumed by a cached file in the specified spoke portal'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-i',
            '--spoke-id',
            type=int,
            required=True,
            help='The identifier of the spoke portal from which to remove the cached file',
        )
        parser.add_argument(
            '--file-id',
            type=str,
            required=True,
            help='The identifier of the file to be removed from the spoke portal cache',
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        print(pretty_json(rest_client.portal.evict_data(args.spoke_id, args.file_id).to_dict()))


class EvictTree(qumulo.lib.opts.Subcommand):
    NAME = 'portal_evict_tree'
    SYNOPSIS = 'Remove a cached directory from a spoke portal'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-i',
            '--spoke-id',
            type=int,
            required=True,
            help='The identifier of the spoke portal from which to remove the cached directory',
        )
        parser.add_argument(
            '--dir-id',
            type=str,
            required=True,
            help='The identifier of the cached directory to remove',
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        print(pretty_json(rest_client.portal.evict_tree(args.spoke_id, args.dir_id).to_dict()))


class GetEvictionSettings(qumulo.lib.opts.Subcommand):
    NAME = 'portal_get_eviction_settings'
    SYNOPSIS = 'Retrieve the configuration for automated removal of cached data'

    @staticmethod
    def main(rest_client: RestClient, _: argparse.Namespace) -> None:
        settings = rest_client.portal.get_eviction_settings()
        print(pretty_json(settings.data.to_dict()))


class SetEvictionSettings(qumulo.lib.opts.Subcommand):
    NAME = 'portal_set_eviction_settings'
    SYNOPSIS = 'Configure the automated removal of cached data'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-f',
            '--free-threshold',
            type=float,
            required=True,
            help=(
                'The threshold of remaining free capacity on a cluster, as a decimal number '
                'between 0 and 1, that triggers the automated removal of cached data. For example, '
                'if you set this value to 0.05, the system begins to remove cached data from spoke '
                'portals when the cluster is 95%% full.'
            ),
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        config = EvictionSettings(free_threshold=args.free_threshold)
        settings = rest_client.portal.set_eviction_settings(config)
        print(pretty_json(settings.data.to_dict()))
