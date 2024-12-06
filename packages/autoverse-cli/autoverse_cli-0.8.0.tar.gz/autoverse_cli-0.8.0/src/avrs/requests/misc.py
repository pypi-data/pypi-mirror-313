from avrs.requests.request import AvrsApiRequest

class AvrsGetSimVersionRequest(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'GetVersion', 0)
        psr = parser.add_parser('get-sim-version', help='get the version of the currently running simulator')
        psr.set_defaults(func=self.send_request)
    
    def get_request_body(self, args):
        return {
        }

class AvrsPingRequest(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'GetVersion', 0)
        psr = parser.add_parser('ping', help='ping the simulator to see if it is running and responsive')
        psr.set_defaults(func=self.send_ping)

    def send_ping(self, args):
        try:
            self.send_http_request(args)
        except:
            print('no')

class AvrsConfigureSimLodRequest(AvrsApiRequest):
    def __init__(self, parser, cfg):
        AvrsApiRequest.__init__(self, parser, cfg, 'ConfigureSimLod', 'lodctrl')
        psr = parser.add_parser('set-lod', help='set the LOD of the sim, possibly reducing GPU overhead')

        psr.add_argument(
            'lod', 
            type=int, 
            help='the new lod level to set. 0 is max lod, 1 is min lod')

        psr.set_defaults(func=self.send_request)
    
    def get_request_body(self, args):
        return {
            'newLod': args.lod
        }