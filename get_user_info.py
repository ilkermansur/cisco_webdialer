from requests import Session
from zeep import Client
from zeep.transports import Transport
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
from lxml import etree
from requests.auth import HTTPBasicAuth

disable_warnings(InsecureRequestWarning)

##################################################################################################################
# Credential for CUCM AXL Application user
username = 'axluser'
password = 'Aa123456'
fqdn = '192.168.85.80'
##################################################################################################################
address = 'https://{}:8443/axl/'.format(fqdn)
wsdl = 'AXLAPI.wsdl'
binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
client = Client(wsdl=wsdl, transport=transport, plugins=[history])
axl = client.create_service(binding, address)

def show_history():
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))  


def get_user_info (userid):
    """
    The function `get_user_info` retrieves user information such as user ID, telephone number, and
    associated devices using the AXL API in Python.
    
    :param userid: The `get_user_info` function you provided seems to be using the `axl` module to
    retrieve user information based on the `userid` parameter passed to the function. It then extracts
    specific details such as `userid`, `telephoneNumber`, and `associatedDevices` from the response and
    prints them
    """

    try:
        get_user_info = axl.getUser(userid='user01', returnedTags={
                                                            'userid':'',
                                                            'telephoneNumber':'',
                                                            'associatedDevices':''
                                                            })

        userid = get_user_info['return']['user']['userid']
        telephone_number = get_user_info['return']['user']['telephoneNumber']
        controlled_devices = get_user_info['return']['user']['associatedDevices']['device']


        print (
            f'userid :{userid}\n',
            f'telephone_number :{telephone_number}\n',
            f'controlled_devices :{controlled_devices}'
            )

    except Fault as f:
        print (f)
        print (show_history())

get_user_info(userid='user01')




    

