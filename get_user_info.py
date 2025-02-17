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
username = 'axluser'
password = 'Aa123456'
fqdn = '192.168.85.80'
userid = 'user01'
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


def get_user_info (userid=userid):
    """
    The function `get_user_info` retrieves user information such as user ID, telephone number, and
    associated devices using the `axl.getUser` method.
    
    :param userid: The code snippet you provided seems to be a function that retrieves user information
    using a library or API called `axl`. It takes a `userid` as input and returns the user's ID,
    telephone number, and associated devices
    :return: The `get_user_info` function is returning the `userid`, `telephone_number`, and
    `controlled_devices` associated with the user specified by the input `userid`. The function makes a
    call to `axl.getUser` to retrieve this information and then extracts and returns these specific
    details.
    """

    try:
        get_user_info = axl.getUser(userid=userid, returnedTags={
                                                            'userid':'',
                                                            'telephoneNumber':'',
                                                            'associatedDevices':''
                                                            })

        userid = get_user_info['return']['user']['userid']
        telephone_number = get_user_info['return']['user']['telephoneNumber']
        controlled_devices = get_user_info['return']['user']['associatedDevices']['device']

        return userid, telephone_number, controlled_devices

    except Fault as f:
        print (f)
        print (show_history())

userid, telephone_number,controlled_devices =get_user_info()

print (f'userid : {userid} \n\
telephony number : {telephone_number} \n\
controlled devices : {controlled_devices}')
