from os import walk
import csv


files = [] # Original file names

# Unpack
for (dirpath, dirnames, filenames) in walk('../data'):
  files = filenames


class Columns:
  CountryRegion = None
  LastUpdate = None
  Confirmed = None
  Deaths = None
  Recovered = None
  Active = None
  Date = None



def getStructure(cols):
  colStructure = Columns()
  for index, col in enumerate(cols):
    parsedCol = col.replace("/", "").replace("-", "").replace("_", "") # Remove unnecessary characters
    setattr(colStructure, parsedCol, index) # Setting the structure indexes
  
  return colStructure



def mergeData(originalData, addon, cols, date):
  newData = originalData
  parsedAddons = Columns()
  
  for idx, col in enumerate(cols):
    setattr(parsedAddons, col.replace("/", "").replace("-", "").replace("_", "").replace(" ", ""), addon[idx])
  
  numericCols = ["Confirmed", "Deaths", "Recovered", "Active"]
  for col in numericCols:
    if getattr(newData, col) == None or getattr(newData, col) == "":
      setattr(newData, col, 0)
    if getattr(parsedAddons, col) == None or getattr(parsedAddons, col) == "":
      setattr(parsedAddons, col, 0)

  newData.CountryRegion = parsedAddons.CountryRegion
  newData.LastUpdate = parsedAddons.LastUpdate
  newData.Confirmed = float(newData.Confirmed) + float(parsedAddons.Confirmed)
  newData.Deaths = float(newData.Deaths) + float(parsedAddons.Deaths)
  newData.Recovered = float(newData.Recovered) + float(parsedAddons.Recovered)
  newData.Active = float(newData.Active) + float(parsedAddons.Active)
  newData.Date = date
  return newData


def findCountry(name, content, date):
  # Assemble the columns structure
  firstRow = None
  structure = Columns()
  resultRow = Columns()
  for row in content:
    if firstRow == None:
      firstRow = row
      structure = getStructure(row)
    else:
      if row[structure.CountryRegion] == name:
        resultRow = mergeData(resultRow, row, firstRow, date)
  
  return resultRow


#for filename in files:
print("\n >> [EXTRACTION] Getting data collection...")
countryRows = []
for filename in files[35:]:
  with open('../data/' + filename) as file:
    spamreader = csv.reader(file, dialect='excel')
    print(" >> [FIND] Getting the target country")
    country = findCountry(name="Brazil", content=spamreader, date=filename.replace(".csv", ""))
    print(" >> [FIND] DONE!")
    countryRows.append(country)

print(" >> [EXTRACTION] DONE! LENGTH = " + str(len(countryRows)))


# TRANSFORM PHASE
def getColumns(obj):
  return list(obj.__dict__.keys())

def toColumnsOrder(obj, cols):
  result = []
  for col in cols:
    result.append(getattr(obj, col))
  return result

dataArray = []
print("\n >> [TRANSFORM] Transformming data")
dataArray.append(getColumns(countryRows[0]))
for row in countryRows[1:]:
  dataArray.append(toColumnsOrder(row, dataArray[0]))

print(" >> [TRANSFORM] DONE!")



print("\n >> [LOAD] Loading data into Data.csv")
print(dataArray)
with open('../treatedData/Data.csv', mode="w", newline='') as dataFile:
  writer = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerows(dataArray)
print(" >> [LOAD] Done")




for d in dataArray:
  print(d)




