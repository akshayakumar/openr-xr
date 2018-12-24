#
# Copyright (c) 2014-present, Facebook, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import click
import zmq

from openr.cli.commands import fib
from openr.Platform import ttypes as platform_types
from openr.utils.consts import Consts


class FibContext(object):
    def __init__(self, verbose, zmq_ctx, host, timeout, fib_rep_port,
                 fib_agent_port, lm_cmd_port, decision_rep_port, client_id,
                 enable_color):
        '''
            :param zmq_ctx: the ZMQ context to create zmq sockets
            :param host string: the openr router host
            :param fib_rep_port int: the fib module port
            :param enable_color bool: whether to turn on coloring display
        '''

        self.verbose = verbose
        self.host = host
        self.timeout = timeout
        self.zmq_ctx = zmq_ctx
        self.enable_color = enable_color
        self.fib_rep_port = fib_rep_port
        self.fib_agent_port = fib_agent_port
        self.lm_cmd_port = lm_cmd_port
        self.decision_rep_port = decision_rep_port
        self.client_id = client_id
        self.proto_factory = Consts.PROTO_FACTORY


class FibCli(object):
    def __init__(self):
        self.fib.add_command(FibRoutesCli().routes)
        self.fib.add_command(FibCountersCli().counters)
        self.fib.add_command(FibListRoutesCli().list_routes, name='list')
        self.fib.add_command(FibAddRoutesCli().add_routes, name='add')
        self.fib.add_command(FibDelRoutesCli().del_routes, name='del')
        self.fib.add_command(FibSyncRoutesCli().sync_routes, name='sync')
        self.fib.add_command(FibValidateRoutesCli().validate)
        self.fib.add_command(FibListRoutesLinuxCli().list_routes_linux,
                             name='list-linux')
        self.fib.add_command(FibValidateRoutesLinuxCli().validate_linux,
                                name='validate-linux')

    @click.group()
    @click.option('--fib_rep_port', default=Consts.FIB_REP_PORT, help='Fib rep port')
    @click.option('--fib_agent_port', default=Consts.FIB_AGENT_PORT,
                  help='Fib thrift server port')
    @click.option('--client-id', default=platform_types.FibClient.OPENR,
                  help='FIB Client ID')
    @click.option('--verbose/--no-verbose', default=False,
                  help='Print verbose information')
    @click.pass_context
    def fib(ctx, fib_rep_port, fib_agent_port,  # noqa: B902
            client_id, verbose):
        ''' CLI tool to peek into Fib module. '''

        ctx.obj = FibContext(
            verbose, zmq.Context(),
            ctx.obj.hostname,
            ctx.obj.timeout,
            ctx.obj.ports_config.get('fib_rep_port', None) or fib_rep_port,
            ctx.obj.ports_config.get('fib_agent_port', None) or fib_agent_port,
            ctx.obj.ports_config.get('lm_cmd_port', None) or
            Consts.LINK_MONITOR_CMD_PORT,
            ctx.obj.ports_config.get('decision_rep_port', None) or
            Consts.DECISION_REP_PORT,
            client_id,
            ctx.obj.enable_color)


class FibRoutesCli(object):

    @click.command()
    @click.option('--json/--no-json', default=False,
                  help='Dump in JSON format')
    @click.pass_obj
    def routes(cli_opts, json):  # noqa: B902
        ''' Request routing table of the current host '''

        fib.FibRoutesCmd(cli_opts).run(json)


class FibCountersCli(object):

    @click.command()
    @click.pass_obj
    def counters(cli_opts):  # noqa: B902
        ''' Get various counters on fib agent '''

        fib.FibCountersCmd(cli_opts).run()


class FibListRoutesCli(object):

    @click.command()
    @click.pass_obj
    def list_routes(cli_opts):  # noqa: B902
        ''' Get and print all the routes on fib agent '''

        fib.FibListRoutesCmd(cli_opts).run()


class FibAddRoutesCli(object):

    @click.command()
    @click.argument('prefixes')   # Comma separated list of prefixes
    @click.argument('nexthops')   # Comma separated list of nexthops
    @click.pass_obj
    def add_routes(cli_opts, prefixes, nexthops):  # noqa: B902
        ''' Add new routes in FIB '''

        fib.FibAddRoutesCmd(cli_opts).run(prefixes, nexthops)


class FibDelRoutesCli(object):

    @click.command()
    @click.argument('prefixes')   # Comma separated list of prefixes
    @click.pass_obj
    def del_routes(cli_opts, prefixes):  # noqa: B902
        ''' Delete routes from FIB '''

        fib.FibDelRoutesCmd(cli_opts).run(prefixes)


class FibSyncRoutesCli(object):

    @click.command()
    @click.argument('prefixes')   # Comma separated list of prefixes
    @click.argument('nexthops')   # Comma separated list of nexthops
    @click.pass_obj
    def sync_routes(cli_opts, prefixes, nexthops):  # noqa: B902
        ''' Re-program FIB with specified routes. Delete all old ones '''

        fib.FibSyncRoutesCmd(cli_opts).run(prefixes, nexthops)


class FibValidateRoutesCli(object):

    @click.command()
    @click.pass_obj
    def validate(cli_opts):  # noqa: B902
        ''' Validator to check that all routes as computed by Decision '''

        fib.FibValidateRoutesCmd(cli_opts).run(cli_opts)


class FibListRoutesLinuxCli(object):

    @click.command()
    @click.pass_obj
    def list_routes_linux(cli_opts):  # noqa: B902
        ''' List routes from linux kernel routing table '''

        fib.FibListRoutesLinuxCmd(cli_opts).run()


class FibValidateRoutesLinuxCli(object):

    @click.command()
    @click.pass_obj
    def validate_linux(cli_opts):  # noqa: B902
        ''' Validate that FIB routes and Kernel routes match '''

        fib.FibValidateRoutesLinuxCmd().run(cli_opts)
