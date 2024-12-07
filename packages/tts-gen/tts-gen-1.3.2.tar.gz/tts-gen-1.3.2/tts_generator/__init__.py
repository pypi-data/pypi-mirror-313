import sys

__version__ = '1.3.2'
__server_url__ = 'http://192.168.110.250:8081'
__server_bridge_url__ = 'http://192.168.110.250:4999'
__server_gx_v2_url__ = 'http://192.168.110.250:5001'

if not sys.version_info[0] == 3:
    statement = "The Python requirement is Python 3"
    raise Exception(statement)

