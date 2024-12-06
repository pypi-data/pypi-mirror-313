#!/usr/bin/env python3
import argparse
from argparse import RawDescriptionHelpFormatter
from argparse import RawTextHelpFormatter

from avrs.app_version import *
from avrs.cfg import *
from avrs.launcher import *
from avrs.can_tool import *
from avrs.argparse_help import *

from avrs.requests.move_to_landmark import MoveToLandmarkRequest
from avrs.requests.restart import Restart
from avrs.requests.reset_to_track import ResetToTrack
from avrs.requests.teleport import Teleport
from avrs.requests.npc import Npc
from avrs.requests.reserve_mv_slot import ReserveMvSlot
from avrs.requests.vd import Vd
from avrs.requests.vehicle_input import AvrsConfigureVehicleInputRequest
from avrs.requests.log_path import LogPath
from avrs.requests.demo import AvrsDemoRequest
from avrs.requests.environment import *
from avrs.requests.code_booz import *
from avrs.requests.vehicle_replay import *
from avrs.requests.scenario_control import *
from avrs.requests.list_sim_objects import *
from avrs.requests.fault_injection import *
from avrs.requests.change_camera import *
from avrs.requests.toggle_hud import * 
from avrs.simconfig import *
from avrs.requests.get_object_config import *
from avrs.requests.misc import *


def get_version():
    return get_app_version()

def main():
    parser = argparse.ArgumentParser(
            prog='avrs', 
            description='Autoverse CLI',
            epilog='',
            formatter_class=RawTextHelpFormatter)

    version_psr = parser.add_argument(
            '--version', 
            help='show the cli version', 
            action='version', 
            version=get_version())

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='request verbose output')

    sps = parser.add_subparsers(required=True, help='sub-command help')

    cfg = load_cfg('avrs')
    check_app_is_latest()

    AvrsLauncher(sps, cfg)


    MoveToLandmarkRequest(sps, cfg)
    Restart(sps, cfg)
    ResetToTrack(sps, cfg)
    Teleport(sps, cfg)
    #Npc(sps, cfg)
    ReserveMvSlot(sps, cfg)
    Vd(sps, cfg)
    AvrsConfigureVehicleInputRequest(sps, cfg)
    LogPath(sps, cfg)
    AvrsEnvironmentRequests(sps, cfg)
    AvrsCodeBoozRequest(sps, cfg)
    AvrsVehicleReplayRequests(sps, cfg)
    AvrsCanTool(sps, cfg)
    AvrsSimConfig(sps, cfg)
    AvrsScenarioRequests(sps, cfg)
    AvrsListSimObjectsRequest(sps, cfg)
    AvrsFaultInjectionRequests(sps, cfg)
    AvrsChangeCameraRequest(sps, cfg)
    AvrsToggleHudRequest(sps, cfg)
    AvrsGetObjectConfigRequest(sps, cfg)
    AvrsGetSimVersionRequest(sps, cfg)
    AvrsPingRequest(sps, cfg)
    AvrsConfigureSimLodRequest(sps, cfg)

    if os.environ.get('AVRS_WITH_DEMO', '0') == '1':
        AvrsDemoRequest(sps, cfg)

    if os.environ.get('AVRS_GEN_DOCS', '0') == '1':
        generate_argparse_docs(parser)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()