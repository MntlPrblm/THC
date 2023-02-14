#imports
import os
import time
import sys
import socket
import netifaces
import platform
import phonenumbers
import webbrowser
import requests
#from imports
from scapy.all import ARP, Ether, srp
from datetime import date
from colorama import Fore
from phonenumbers import geocoder, carrier, timezone
from ip2geotools.databases.noncommercial import DbIpCity

#ART AND TITLE SCREENS===================================================================
help = """
phonecheck: does basic OSINT for pn
help: shows this screen
clear: clears the screen
exit: exits
getlocalip: shows you your ip address on local network
networkscan: runs a network scan, dosent work on secure networks
ping: checks to see if IP is up
default: shows you default gateway IP
library: takes to the notes created by the script
drillbit: finds address from name and city
"""
titlescreen = """
================================

                        )
                       (
           _ ___________ )
    THC   [_[___________#

================================
"""

print(Fore.LIGHTRED_EX+titlescreen)
print("Loading...")
time.sleep(1)


#FUNCTIONS================================================================================
#ip geolocator
def get_location():
    ip_address = input("Victim IP address: ")
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    print(location_data)
    start()


#name to location
def drillbit():
    first_name = input("First name: ")
    last_name = input("last name: ")
    state = input("State abbreviated: ")
    city = input("City: ")
    city = city.replace(' ','-')
    webbrowser.open("https://www.beenverified.com/people/"+first_name+"-"+last_name+"/"+state+"/"+city)
    start()

#phone osint
def phonecheck(pn):
    print("checking phone number")
    z = phonenumbers.parse(pn, None)
    print(z)
    real_number = phonenumbers.is_possible_number(z)
    if real_number == True:
        print("Number has NPA 200, aka Real number")
    else:
        print("NPA not found, not real number")
    location = geocoder.description_for_number(z, "en")
    print("Location: "+location)
    ro_number = phonenumbers.parse(pn, "RO")
    OGcarrier = carrier.name_for_number(ro_number, "en")
    print("Original carrier: "+OGcarrier)
    gb_number = phonenumbers.parse(pn, "GB")
    time_zone = timezone.time_zones_for_number(gb_number)
    print("Timezone: "+str(time_zone))
    print("==============================================")
    print("open OSINT websites for phone numbers?")
    osintpn = input("Y or N: ")
    if osintpn == "y":
        webbrowser.open("https://www.usphonebook.com/")
        webbrowser.open("https://www.truepeoplesearch.com/")
    start()

#default gateway finder
def default_gateway():
    gateways = netifaces.gateways()
    default_gateway = gateways['default'][netifaces.AF_INET][0]
    print(default_gateway)
    start()

#runs before script
def prereq():
    os.system('cls')
    print("Loading...")
    if os.path.exists("./library") == False:
        os.mkdir("library")
    user_os = platform.system()
    if user_os != "Windows":
        print("You need windows to run this script")
        time.sleep(3)
        sys.exit()
    os.system('cls')
    start()

#function to get local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

#function to scan network for mac addresses
def network_scan():
    local_ip = input("Localhost IP address (normally 192.168.1.1/24): ")
    #create ARP packet
    arp = ARP(pdst=local_ip)
    #create Ether destination
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    #creates packet
    packet = ether/arp
    result = srp(packet, timeout=3)[0]
    #client list
    clients = []
    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    # print clients
    print("Available devices in the network:")
    print("IP" + " "*18+"MAC")
    for client in clients:
        print("{:16}    {}".format(client['ip'], client['mac']))
    start()

#function to check if IP address is up
def ping():
    IP = input("Please type IP address: ")
    ret = os.system("ping -n 3 "+IP)
    if ret == 0:
        print("IP is up")
    else:
        print("IP is down")
    start()

#library function
def library():
    os.system("cls")
    try:
        os.chdir("./library")
    except FileNotFoundError:
        print("In directory")
    print("Creating a file requires a restart of script")
    print(Fore.CYAN+"================")
    print(Fore.LIGHTRED_EX+"[1] show entries")
    print("[2] make entry")
    print("[3] read entry")
    print("[0] exit")
    print(Fore.CYAN+"================")
    print("")
    library_in = input(Fore.WHITE+"Library input: ")
    if library_in == "0":
        os.chdir("../")
        start()
    if library_in == "1":
        path = os.getcwd()
        dir_list = os.listdir(path)
        # prints all files
        print("------------------")
        print(dir_list)
        print("------------------")
        input("Press enter to continue")
        library()
    if library_in == "2":
        today = date.today()
        filename = input("Filename with .txt: ")
        content = input("Content in file: ")
        f = open(filename, "w")
        f.write(content)
        f.close
        library()
    if library_in == "3":
        file_to_read = input("File to read: ")
        if os.path.exists(file_to_read) == True:
            with open(file_to_read, 'r') as f:
                print(f.read())
        print("=======================")
        input("press enter to continue")
        library()



#start==========================================================================================
def start():
    print(Fore.LIGHTCYAN_EX+"==============================================")
    print(Fore.LIGHTRED_EX+"THC ver 420, Lets fucking goooooooooooo")
    print(Fore.LIGHTCYAN_EX+"==============================================")
    user_in = input(Fore.LIGHTWHITE_EX+"Input: ")
    #to library
    if user_in == "library":
        library()
    #to ping server
    if user_in == "ping":
        ping()
    #to exit
    elif user_in == "exit":
        sys.exit()
    #to run network scan
    elif user_in == "networkscan":
        network_scan()
    #to clear screen
    elif user_in == "clear":
        os.system("cls")
        start()
    #to get local ip
    elif user_in == "getlocalip":
        local_ip = get_local_ip()
        print(local_ip)
        start()
    #to show help
    elif user_in == "help":
        print(help)
        start()
    #to find gateway
    elif user_in == "default":
        default_gateway()
    elif user_in == "phonecheck":
        pn = input("Phone number to search with country code: ")
        phonecheck(pn)
    elif user_in == "drillbit":
        drillbit()
    elif user_in == "iptracker":
        get_location()
    else:
        print("Invalid command")
        time.sleep(1)
        start()

if __name__=="__main__":
    prereq()
    print("THC starting...")
    start()
