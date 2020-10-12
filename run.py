import os
import sys
path = "\\".join(os.path.realpath(__file__).split('\\')[0:-1])

countryName = "Brazil"
if len(sys.argv) > 1:
  countryName = " ".join(sys.argv[1:])

if os.path.exists(path+'\\treatedData\\'+ countryName +'.csv') == False:
  os.system("cd " + path + "\\src && python DataTransformer.py " + countryName)

os.system("cd " + path + "\\src && python DataPrinter.py " + countryName)