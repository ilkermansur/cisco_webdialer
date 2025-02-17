"""
__author__   = ilker MANSUR imansur@btegitim.com
__purpose__  = Check agents and route call to alternate anoncement
__version__  = 1.0

"""

# Import Library
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree
import time

# Credential for CUCM AXL Application user
axlusername = 'axluser'
axlpassword = 'Aa123456'
fqdn = '192.168.85.80'

session = Session()
session.verify = False
session.auth = HTTPBasicAuth(axlusername, axlpassword)
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
wsdl = f'https://{fqdn}:8443/realtimeservice2/services/RISService70?wsdl'
  
disable_warnings(InsecureRequestWarning)

client = Client(wsdl=wsdl, transport=transport,plugins=[history])
service = client.create_service('{http://schemas.cisco.com/ast/soap}RisBinding',
                                f'https://{fqdn}:8443/realtimeservice2/services/RISService70')

def show_history():
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))  


def get_device_ip(device_name):
    """
    The function `get_device_ip` retrieves the IP address of a specified device using a selection
    criteria dictionary and a service call.
    
    :param device_name: The `get_device_ip` function seems to be a part of a script that interacts with
    a service to retrieve IP information for a specific device based on the device name provided. The
    function uses a set of criteria to query the service and extract the IP address of the device
    :return: The function `get_device_ip(device_name)` is returning the IP address of the device with
    the given `device_name`. It queries a service using the provided `cm_selection_criteria` to get
    information about the device, extracts the IP address from the response, and returns it.
    """

    cm_selection_criteria = {
                            'DeviceClass': 'Any',
                            'Status': 'Any',
                            'NodeName': '',
                            'SelectBy': 'Name',
                            'SelectItems': {
                                'item': device_name
                                },
                            'Protocol': 'Any',
                            }

    try:
        phone_query_response = service.selectCmDevice(StateInfo='', CmSelectionCriteria=cm_selection_criteria)
        ip_info = phone_query_response['SelectCmDeviceResult']['CmNodes']['item'][0]['CmDevices']['item'][0]['IPAddress']['item'][0]['IP']
    
        return ip_info


    except Fault as f:
        print(f)
        show_history()

print (get_device_ip(device_name='SEPAC7E8AB69C2C'))