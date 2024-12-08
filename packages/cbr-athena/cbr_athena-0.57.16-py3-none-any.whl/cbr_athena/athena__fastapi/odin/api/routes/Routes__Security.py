import requests
from starlette.requests                                     import Request
from cbr_athena.athena__fastapi.odin.FastApi_Header_Auth    import route_with_auth
from cbr_athena.athena__fastapi.routes.Fast_API_Route       import Fast_API__Routes
from cbr_athena.utils.IP_Data                               import IP_Data
from osbot_utils.utils.Status                               import status_ok, status_error

FAST_API_ROUTES__ODIN__API__SECURITY =  ['/security/security/ip_address'                ,
                                         '/security/config/current_ip_address'          ,
                                         '/security/security/which_ips_are_attacking_odin',
                                         '/security/security/block_ip_address'            ]


class Routes__Security(Fast_API__Routes):
    path_prefix: str = "security"

    def __init__(self):
        super().__init__()

    def add_routes(self):

        @route_with_auth(self.router, 'get', '/security/ip_address', summary="Get information and details about a specific IP address")
        def info__ip_adresss(ip_address):
            try:
                return IP_Data().request_get(ip_address)
            except Exception as e:
                return status_error(message=f"Failed to get into about IP {ip_address}", error=str(e))

        @route_with_auth(self.router, 'get', '/config/current_ip_address',
                         summary="Get Odin IP Address")

        def my_current_ip_address(request: Request):
            response = requests.get("https://api.ipify.org?format=json")
            if response.status_code == 200:
                ip_info = response.json()
                return {"ip": ip_info["ip"]}
            else:
                return {"error": "Could not retrieve IP address"}

        @route_with_auth(self.router, 'get', '/security/which_ips_are_attacking_odin',
                         summary="Which IPs are currently attacking Odin")
        def ips_attacking_odin():
            # todo: refactor to work live
            ip_traffic_details = 'http://localhost:5001/web/dev/logs/ip-address?ip_address={ip_address}&env=PROD&hours=24'
            ip_data = IP_Data()
            try:
                ip_addresses = [] # todo add dymamic list
                data = []
                for ip_address in ip_addresses:
                    ip_details = ip_data.request_get(ip_address)
                    item = {'ip_address': ip_address,
                            'ip_details' : ip_details,
                            'link_for_more_info': ip_traffic_details.format(ip_address=ip_address)}
                    data.append(item)
            except Exception as e:
                return {'error': str(e)}
            return data

        @route_with_auth(self.router, 'get', '/security/block_ip_address',
                         summary="Block IP Address at firewall level")
        def block_ip_address(ip_address):
            return {'message': f'ip address is being blocked at the firewall {ip_address}'}

