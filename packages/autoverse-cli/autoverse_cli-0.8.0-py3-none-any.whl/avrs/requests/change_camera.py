from avrs.requests.request import AvrsApiRequest

class AvrsChangeCameraRequest(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'ChangeCamera', '')
        psr = parser.add_parser('change-camera', help='changes the active camera on an object')
        psr.set_defaults(func=self.send_request)

    def get_request_body(self, args):
        return {
        }
