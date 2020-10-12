import os
import sys
path = "\\".join(os.path.realpath(__file__).split('\\')[0:-1])

countryName = "Brazil"
if len(sys.argv) > 1:
  countryName = " ".join(sys.argv[1:])


# SYNC DATA
print("\n>> SYNCING DATA...")
if os.path.exists(path+'\\data\\COVID-19') == True:
  os.system("cd " + path + "\\data\\COVID-19 && git pull")
else:
  os.system("cd " + path + "\\data && git clone https://github.com/CSSEGISandData/COVID-19.git")
print(">> DONE!")

#if os.path.exists(path+'\\treatedData\\'+ countryName +'.csv') == False:
  
os.system("cd " + path + "\\src && python DataTransformer.py " + countryName)
os.system("cd " + path + "\\src && python DataPrinter.py " + countryName)