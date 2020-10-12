import os

path = "\\".join(os.path.realpath(__file__).split('\\')[0:-1])
if os.path.exists(path+'\\treatedData\\Data.csv') == False:
  os.system("cd " + path + "\\src && python DataTransformer.py")

os.system("cd " + path + "\\src && python DataPrinter.py")