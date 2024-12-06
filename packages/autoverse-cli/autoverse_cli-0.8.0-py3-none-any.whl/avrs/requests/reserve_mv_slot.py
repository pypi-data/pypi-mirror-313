from avrs.requests.request import AvrsApiRequest
from argparse import RawTextHelpFormatter

RESERVE_MV_SLOT_HELP = '''
slot (if an open slot exists, there are 4 total) using the given name to add a new vehicle and the appropriate topics.
It will despawn the default vehicle and remove the default ROS topics when it is first run. Each vehicle added will be 
given its own topics prefixed by the given name, and the slot index will correspond to the vcan it will use.
Note that this will require having active vcans for each vehicle you wish to use. 
(eg, if you want to use 4 vehicles, you will need vcan0, vcan1, vcan2, and vcan3)
'''

# use these to spawn MVs
MV_LANDMARKS = [
    'MvStart0',
    'MvStart1',
    'MvStart2',
    'MvStart3'
]

class ReserveMvSlot(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'SpawnObject', 0)
        psr = parser.add_parser('reserve-mv-slot', help=RESERVE_MV_SLOT_HELP, formatter_class=RawTextHelpFormatter)

        psr.add_argument(
            'slot_name',
            help='the name of the vehicle to put in the specified slot')

        psr.add_argument(
            'slot_index',
            type=int,
            choices=[0, 1, 2, 3],
            help='the slot index (0-4) to reserve')

        psr.add_argument(
            '--bsu-can-name', 
            default='vcan0',
            help='the name of the CAN interface to use for the BSU CAN bus on the new vehicle')

        psr.add_argument(
            '--kistler-can-name',
            default='vcan1',
            help='the name of the CAN interface to use for the Kistler CAN bus on the new vehicle')

        psr.add_argument(
            '--badenia-can-name', 
            default='vcan2',
            help='the name of the CAN interface to use for the bandanania CAN bus on the new vehicle')

        psr.add_argument(
            '--with-view-cameras',
            action='store_true',
            help='if the new vehicle should have cameras attached to it')

        psr.add_argument(
            '--enable-lidar',
            action='store_true',
            help='if set, the lidar will be enabled on the new vehicle')

        psr.add_argument(
            '--enable-camera-sensor',
            action='store_true',
            help='if set, the camera will be enabled on the new vehicle')

        psr.add_argument(
            '--disable-hud',
            action='store_true',
            help='if set, the new vehicle will not create a HUD (mutiple HUDs will clutter the screen)')


        psr.set_defaults(func=self.send_request)
    
    def get_request_body(self, args):

        eav_init_pld = {
            'TypeName': 'Eav24Initializer',
            'Body': {
                'bsuCanName': args.bsu_can_name,
                'kistlerCanNam': args.kistler_can_name,
                'badeniaCanName': args.badenia_can_name,
                'bHudEnabled': not args.disable_hud,
                'bEnableLidar': args.enable_lidar,
                'bEnableCameraSensor': args.enable_camera_sensor
            }
        }

        plds = [
            eav_init_pld
        ]

        if args.with_view_cameras:
            plds.append(
                {
                    'TypeName': 'InitializerTemplates',
                    'Body': {
                        'Templates': [
                            {
                                'PayloadType': 'SimViewTargetIpd',
                                'PayloadSpec': 'DefaultCarCams'
                            }
                        ]
                    }
                })

        return {
            'Name': args.slot_name,
            'Type': 'Eav24',
            'Location': {},
            'Rotation': {},
            'Landmark': MV_LANDMARKS[args.slot_index],
            'Payloads': plds
        }