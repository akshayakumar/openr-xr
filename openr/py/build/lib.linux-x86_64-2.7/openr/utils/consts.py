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

from thrift.protocol.TCompactProtocol import TCompactProtocolFactory


class Consts(object):
    TIMEOUT_MS = 5000
    CONST_TTL_INF = -2**31
    ADJ_DB_MARKER = 'adj:'
    INTERFACE_DB_MARKER = 'intf:'
    PREFIX_DB_MARKER = 'prefix:'

    KVSTORE_REP_PORT = 60002
    KVSTORE_PUB_PORT = 60001
    DECISION_REP_PORT = 60004
    FIB_REP_PORT = 60009
    HEALTH_CHECKER_CMD_PORT = 60012
    LINK_MONITOR_CMD_PORT = 60006
    PREFIX_MGR_CMD_PORT = 60011
    MONITOR_REP_PORT = 60008
    FIB_AGENT_PORT = 60100
    CONFIG_STORE_URL_PREFIX = "ipc:///tmp/config_store_cmd"

    TOPOLOGY_OUTPUT_FILE = '/tmp/openr-topology.png'

    PREFIX_ALLOC_KEY = 'prefix-allocator-config'
    LINK_MONITOR_KEY = 'link-monitor-config'
    PREFIX_MGR_KEY = 'prefix-manager-config'

    # Default serializer/deserializer for communication with OpenR
    PROTO_FACTORY = TCompactProtocolFactory
