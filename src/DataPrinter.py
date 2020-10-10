import csv
import matplotlib.pyplot as plt
from os import walk
import math

# Loading
def getAllByIndex(data, index):
  arr = []
  for item in data:
    arr.append([float(item[index])])
  return arr


def reformatDate(date):
  numbers = date.split('-')
  return numbers[1] + "/" + numbers[0] + "/" + numbers[2] 

def getFileNames(files):
  result = []
  for file in files:
    result.append(reformatDate(file.replace('.csv', '')))
  return result

files = [] # Original file names

# Unpack
for (dirpath, dirnames, filenames) in walk('../data'):
  files = filenames

with open('../treatedData/Data.csv') as file:
    spamreader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data = []
    for row in spamreader:
      data.append(row)



confirmed = getAllByIndex(data[1:], 0)
deaths = getAllByIndex(data[1:], 1)
recovered = getAllByIndex(data[1:], 2)
active = getAllByIndex(data[1:], 3)

#plt.plot(getFileNames(files)[35:-1], deaths, 'r', getFileNames(files)[35:-1], confirmed, 'b', getFileNames(files)[35:-1], recovered, 'g', getFileNames(files)[35:-1], active, 'orange')
plt.plot(getFileNames(files)[35:-1], active, 'orange')
plt.xticks(rotation=25, ticks=[getFileNames(files)[35], getFileNames(files)[65],  getFileNames(files)[95], getFileNames(files)[125], getFileNames(files)[155], getFileNames(files)[185], getFileNames(files)[215], getFileNames(files)[240], getFileNames(files)[-1]])
plt.xlabel('Gráfico completo do COVID-19 no Brasil (' + getFileNames(files)[35] + "-" + getFileNames(files)[-1] + ")")

plt.show()

class Statistic:
  data = None
  media = None
  varianca = None
  desvioPadrao = None

  def __init__(self, data):
    self.data = data
    self.getMedia()
    self.getVarianca()
    self.getDesvioPadrao()

  def getMedia(self):
    soma = 0
    for item in self.data:
      soma = soma + item[0]
    self.media = soma / len(self.data)
    return
  
  def getVarianca(self):
    soma = 0
    for item in self.data:
      soma = soma + ((item[0] - self.media) ** 2)
    self.varianca = soma / (len(self.data) - 1)
    return

  def getDesvioPadrao(self):
    self.desvioPadrao = math.sqrt(self.varianca)
    return


statistics = {
  "deaths": Statistic(deaths),
  "confirmed": Statistic(confirmed),
  "recovered": Statistic(recovered),
  "active": Statistic(active)
}

print(statistics['deaths'].media)