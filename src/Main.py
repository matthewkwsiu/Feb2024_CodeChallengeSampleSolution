import time
import re

IP_LEASE_TIME = 60 # 60 seconds
EXPIRED_LEASE_TIME = 0
ipAddressLeaseTimes = {} # dictionary to store IP Addresses and their 
                         # associated lease times

def isIpLeased(ipKey):
    """
    Checks if an IP Address is leased.
 
    Args:
        ipKey (int): IP address being validated.
 
    Returns:
        boolean: Whether the IP address is leased.
    """
    # Initialize IP if it hasn't been initalized in the dictionary
    if ipKey not in ipAddressLeaseTimes:
        ipAddressLeaseTimes[ipKey] = EXPIRED_LEASE_TIME
        return False

    # IP is still leased if lease time is greater than current time
    # Otherwise, it isn't leased
    return time.time() < ipAddressLeaseTimes[ipKey] 

def getNewIpAddress():
    """
    Returns the next available IP Address.
 
    Args:
        None
 
    Returns:
        String: Next Valid IP Address.
    """
    for a in range(1, 256):
        for b in range(1, 256):
            for c in range(1, 256):
                for d in range(1, 256):
                    ipString = str(a) + "." + str(b) + "." + str(c) + "." + str(d)
                    if(not isIpLeased(ipString)):
                        return ipString
    return None

def ask():
    """
    Leases an IP Address if available.
 
    Args:
        None
 
    Returns:
        None
    """
    newIp = getNewIpAddress()
    if(newIp == None):
        print("No IP Addresses Available")
        return
    ipAddressLeaseTimes[newIp] = time.time() + IP_LEASE_TIME
    print("Offer", newIp)

def renew(ip):
    """
    Renews a leased IP Address. Prints error message 
    otherwise. 
 
    Args:
        None
 
    Returns:
        None
    """
    if(isIpLeased(ip)):
        ipAddressLeaseTimes[ip] = time.time() + IP_LEASE_TIME
        print("RENEWED for", ip)
    else:
        print(ip, "is invalid")

def release(ip):
    """
    Releases a leased IP Address. Prints error message 
    otherwise. 
 
    Args:
        None
 
    Returns:
        None
    """
    if(isIpLeased(ip)):
        ipAddressLeaseTimes[ip] = EXPIRED_LEASE_TIME
        print("RELEASED for", ip)
    else:
        print(ip, "is invalid")

def status(ip):
    """
    Indicates the status of an IP Address. AVAILABLE if the 
    IP address is unleased, and ASSIGNED if the address is 
    leased.

    Args:
        None
 
    Returns:
        None
    """
    if(isIpLeased(ip)):
        print(ip, "ASSIGNED")
    else:
        print(ip, "AVAILABLE")
    return

def main():
    while(True):
        userInput = input().strip()

        # Check for empty command
        if not len(userInput) > 0:
            print("no command entered")
            continue

        # Check for "ASK" command
        print("You entered", userInput)
        if(userInput == "ASK"):
            ask()
            continue

        userInput = userInput.split(" ", 1)
        # Check for no IP address entered
        if(not len(userInput) == 2):
            print("Invalid command")
            continue
        
        command, ipInputted = userInput
        # Check for valid IP address format
        if(not re.search(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", ipInputted)):
            print("Invalid IP address")
            continue

        match command: 
            case "RENEW":
                renew(ipInputted)
            case "RELEASE":
                release(ipInputted)
            case "STATUS":
                status(ipInputted)
            case _: 
                print("Invalid command")

if __name__ == "__main__":
    main()
