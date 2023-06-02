import math
import copy

"""
known issues:
- subnet mask in dotted notation cannot verify consistent subnet mask
- network address cannot handle situations which include adding a one to the next octet before
"""

class IP_Calculator():
  def __init__(self):
    pass
    
  def GatherVerifiyInput(self):
    self.ipAddress =  input("Enter IP address (x.x.x.x):\n")
    self.subnetMask = input("\nEnter dotted notation (ie. 255.255.255.0) \nor slash notation subnet mask(ie. /24):\n")
    print("\nValidating input..\n")
    try:
      #ip address testing
      self.splitIpaddress = self.ipAddress.split(".")
      if len(self.splitIpaddress) != 4:
        print("The amount of octets is too low or input is invalid. Please try again.\n")
        return False
      for octet in self.splitIpaddress:
        num = int(octet)
        if num > 255 or num < 0:
          print(f"The octet {octet} is invalid. Try again.\n")
          return False
      #subnet mask testing
      if self.subnetMask[0] == "/":
        slashNum = int(self.subnetMask[1:])
        if slashNum < 0 or slashNum > 32:
          print(f"Slash notation number {self.subnetMask} is invalid. Please try again.\n")
          return False
        return True
      
      split_mask = self.subnetMask.split(".")
      if len(split_mask) == 4:
        slash = 0
        bitRange = ("0", "128","192","224","240","248","252","254","255")
        for i, octet in enumerate(split_mask):
          num = int(octet)
          if num < 0 or num > 255:
            print(f"The octet {octet} is invalid. Try again.\n")
            return False
          slash += bitRange.index(octet)
        self.subnetMask = f"/{str(slash)}"
        return True
      print("Subnet mask error; cannot identify subnet mask format, Please try agian.")
      return False

    except ValueError as e:
      print(f"Input given failed validation because of incorrect values. Please try again.\n\nError: {e}\n")
      return False
    except Exception as e:
      print(f"Input validation failed; please try again.\n\nError: {e}\n") #later
      return False
    finally:
      print("Input validation completed.\n")
    
  def CalculateIPaddress(self):
    if self.subnetMask[0] == "/":
      classRange = (8,16,24,32)
      slashNotation = int(self.subnetMask[1:])
      currentIPClass = None
      for ipClass in classRange:
        if slashNotation <= ipClass:
          currentIPClass = ipClass
          break
        continue
      hostSubnet = int(math.pow(2,(currentIPClass - slashNotation)))

      classLocation = classRange.index(currentIPClass)
      networkAddress = self.splitIpaddress
      
      networkAddress[classLocation] = str(int(math.floor(int(self.splitIpaddress [classLocation]) / hostSubnet) * hostSubnet))
      broadcastAddress = copy.deepcopy(networkAddress)

      for classPos, octet in enumerate(networkAddress):
        print(octet)
        if classPos > classLocation:
          networkAddress[classPos] = "0"
          broadcastAddress[classPos] = "255"
          
      lastHost = copy.deepcopy(broadcastAddress)
      lastHost[classLocation] = str(int(lastHost[classLocation]) + int(hostSubnet) - 1)
      broadcastAddress = copy.deepcopy(lastHost)
      firstHost = copy.deepcopy(networkAddress)
      firstHost[3] = str(int(firstHost[3]) + 1)
      #here
      nextSubnet = copy.deepcopy(networkAddress)
      nextSubnet[classLocation] = str(int(nextSubnet[classLocation]) + hostSubnet)
      lastHost[3] = "254"
      if currentIPClass == 32:
        lastHost[3] = str(int(networkAddress[3]) + hostSubnet - 2)
      
      print("First host address: " + ".".join(firstHost) + self.subnetMask)
      print("Last host address: " + ".".join(lastHost) + self.subnetMask)
      print("Broadcast address: " + ".".join(broadcastAddress) + self.subnetMask)
      print("Network address: " + ".".join(networkAddress) + self.subnetMask)
      print("Next subnet address: " + ".".join(nextSubnet) + self.subnetMask)
