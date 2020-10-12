from os import walk
import csv
import sys

print(">> RUNNING DATA TRANSFORMER...")

files = [] # Original file names

# Unpack
for (dirpath, dirnames, filenames) in walk('../data'):
  files = filenames

countryName = "Brazil"
if len(sys.argv) > 1:
  countryName = " ".join(sys.argv[1:])


class Columns:
  CountryRegion = None
  LastUpdate = None
  Date = None

  Confirmed = None
  Deaths = None
  Recovered = None
  Active = None
  ConfirmedVariation = None
  DeathsVariation = None
  RecoveredVariation = None
  ActiveVariation = None




def getStructure(cols):
  colStructure = Columns()
  for index, col in enumerate(cols):
    parsedCol = col.replace("/", "").replace("-", "").replace("_", "") # Remove unnecessary characters
    setattr(colStructure, parsedCol, index) # Setting the structure indexes
  
  return colStructure



def mergeData(originalData, addon, cols, date, lastRow):
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
  if lastRow != None:
    newData.DeathsVariation = newData.Deaths - lastRow.Deaths
    newData.ActiveVariation = newData.Active - lastRow.Active
    newData.ConfirmedVariation = newData.Confirmed - lastRow.Confirmed
    newData.RecoveredVariation = newData.Recovered - lastRow.Recovered
  else:
    newData.DeathsVariation = 0
    newData.ActiveVariation = 0
    newData.ConfirmedVariation = 0
    newData.RecoveredVariation = 0
  return newData


def findCountry(name, content, date, lastRow):
  # Assemble the columns structure
  firstRow = None
  structure = Columns()
  resultRow = Columns()
  rowsLen = 0
  for idx, row in enumerate(content):
    if firstRow == None:
      firstRow = row
      structure = getStructure(row)
    else:
      if row[structure.CountryRegion] == name:
        rowsLen = rowsLen + 1
        resultRow = mergeData(resultRow, row, firstRow, date, lastRow)
  
  if (rowsLen == 0):
    return None
  return resultRow


#for filename in files:
print("\n >> [EXTRACTION] Getting data collection...")
countryRows = []
for idx, filename in enumerate(files):
  with open('../data/' + filename) as file:
    spamreader = csv.reader(file, dialect='excel')
    print("   >> [FIND] Getting the target country " + str(idx+1) + "/" + str(len(files)), end="\r")
    last = None
    if len(countryRows) > 0:
      last = countryRows[-1]
    
    country = findCountry(name=countryName, content=list(spamreader), date=filename.replace(".csv", ""), lastRow=last)
    if country != None:
      countryRows.append(country)

print("   >> [FIND] Getting the target country " + str(len(files)) + "/" + str(len(files)))
print("   >> [FIND] DONE!")
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



print("\n >> [LOAD] Loading data into "+ countryName +".csv")
with open('../treatedData/'+countryName+'.csv', mode="w", newline='') as dataFile:
  writer = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerows(dataArray)
print(" >> [LOAD] Done")


print("\n>> ALL DONE!")



