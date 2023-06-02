import IP_calculator_class as ipCalculator
print("IP subnetting calculator\n")


session = ipCalculator.IP_Calculator()

if __name__ == "__main__":
  def main():
    testResult = session.GatherVerifiyInput()
    if testResult == False:
      return
    session.CalculateIPaddress()

  main()

