from zeep import Client
from zeep.transports import Transport
from requests import Session
import urllib3

# SSL uyarılarını devre dışı bırak
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def make_call(cucm_ip, userid, password, destination, deviceName):
    """
    CUCM WebDialer kullanarak arama yapma fonksiyonu
    
    Args:
        cucm_ip (str): CUCM sunucu IP adresi
        userid (str): UserID
        password (str): User password
        destination (str): Aranacak numara
        source_user (str): Arayan kullanıcının user ID'si
    """
    # SSL doğrulamasını devre dışı bırak
    session = Session()
    session.verify = False
    transport = Transport(session=session)
    
    # WSDL URL'sini oluştur
    wsdl_url = f'https://{cucm_ip}:8443/webdialer/services/WebdialerSoapService?wsdl'
    
    try:
        # SOAP client'ı oluştur
        client = Client(
            wsdl_url,
            transport=transport
        )
        
        # Credential nesnesini oluştur - userID kullanıcı adının tam halini içermeli
        cred = client.get_type('ns0:Credential')(
            token=None,
            userID=userid,
            password=password
        )
        
        # User Profile nesnesini oluştur
        prof = client.get_type('ns0:UserProfile')(
            user=userid,
            deviceName=deviceName,
            lineNumber='',
            supportEM=True,
            locale='en_US',  # Varsayılan locale
            dontAutoClose=False,
            dontShowCallConf=False
        )
        
        # Debug bilgisi
        print(f"\nKullanılan kimlik bilgileri:")
        print(f"userID: {cred.userID}")
        print(f"password: {'*' * len(password)}")
        
        # Aramayı başlat
        result = client.service.makeCallSoap(cred=cred, dest=destination, prof=prof)
        
        print(f"\nArama başlatıldı: {destination} numarası {userid} kullanıcısı tarafından aranıyor")
        print("Sonuç:", result)
        return result
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        if hasattr(e, 'detail'):
            print("Detaylı hata:", e.detail)
        raise

if __name__ == "__main__":
    # Test parametreleri
    cucm_ip = "192.168.85.80"
    userid = "imansur"  # Kullanıcı adı
    password = "Aa123456"  # Şifre
    destination = "5555"  # Aranacak numara
    deviceName = "CSFimansur"
    
    make_call(cucm_ip, userid, password, destination, deviceName)
