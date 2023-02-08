#imports
import os
import time
import sys
import socket
import netifaces
import platform
#from imports
from scapy.all import ARP, Ether, srp
from datetime import date
from colorama import Fore

#ART AND TITLE SCREENS===================================================================
help = """
help: shows this screen
clear: clears the screen
exit: exits
get local ip: shows you your ip address on local network
network scan: runs a network scan, dosent work on secure networks
ping: checks to see if IP is up
default gateway: shows you default gateway IP
library: takes to the notes created by the script
"""




#FUNCTIONS================================================================================
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
    print(Fore.CYAN+"==============================================")
    print(Fore.LIGHTRED_EX+"THC, Titus' Hacking Counterpart. Also Weed lol.")
    print(Fore.CYAN+"==============================================")
    user_in = input(Fore.WHITE+"Input: ")
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
    elif user_in == "network scan":
        network_scan()
    #to clear screen
    elif user_in == "clear":
        os.system("cls")
        start()
    #to get local ip
    elif user_in == "get local ip":
        local_ip = get_local_ip()
        print(local_ip)
        start()
    #to show help
    elif user_in == "help":
        print(help)
        start()
    #to find gateway
    elif user_in == "default gateway":
        default_gateway()
    else:
        print("Invalid command")
        time.sleep(1)
        start()

if __name__=="__main__":
    prereq()
    print("THC starting...")
    start()