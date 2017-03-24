import socket
import os
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
import subprocess

def getBSSID():
    data=str(subprocess.check_output("netsh wlan show interfaces"))
    data=data.replace(" ","")
    bssid=""
    index=data.index("SSID")+5
    while(data[index]!= "r" ):
        bssid=bssid+data[index]
        index+=1
    bssid=bssid[0:len(bssid)-1]
    return bssid

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def sendSms():
    account_sid = "AC32dc469056fcc10397cc8890568574e9" # Your Account SID from www.twilio.com/console
    auth_token  = "92c21219bdf7769b3494096b6c2dcc80"  # Your Auth Token from www.twilio.com/console

    client = TwilioRestClient(account_sid, auth_token)

    msg="\nBSSID: "+getBSSID()+"\n   "+"Ip: "+get_lan_ip()

    try:
        message = client.messages.create(body=msg,to="+972543014987",from_="+17028007210")
    except TwilioRestException as e:
        print(e)






sendSms()
