import csv
import matplotlib.pyplot as plt
from os import walk
import numpy as np
import math

print("\n>> RUNNING DATA PRINTER")

# Loading
def getAllByIndex(data, index):
  arr = []
  for item in data:
    arr.append([float(item[index])])
  return arr
def getAllByIndexBarVersion(data, index):
  arr = []
  for item in data:
    arr.append(float(item[index]))
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


print("\n >> [READING] Getting data for each column...")
confirmed = getAllByIndex(data[1:], 0)
deaths = getAllByIndex(data[1:], 1)
recovered = getAllByIndex(data[1:], 2)
active = getAllByIndex(data[1:], 3)
deathsVariation = getAllByIndexBarVersion(data[1:], 7)
activeVariation = getAllByIndexBarVersion(data[1:], 8)
confirmedVariation = getAllByIndexBarVersion(data[1:], 9)
recoveredVariation = getAllByIndexBarVersion(data[1:], 10)
print(" >> [READING] DONE!")


class Statistic:
  data = None
  media = None
  maximo = None
  minimo = None
  soma = None
  
  desvioPadrao = None
  varianca = None
  amplitude = None
  intervaloInterQuartil = None
  coeficienteDeVariacao = None  

  q1 = None
  q2 = None
  q3 = None
  q4 = None

  d1M = None
  d2M = None
  d3M = None
  d4M = None
  d5M = None
  d6M = None
  d7M = None
  d8M = None
  d9M = None
  d10M = None

  def __init__(self, data):
    self.data = data
    self.treatData()
    self.getSoma()
    self.getMedia()
    self.getVarianca()
    self.getDesvioPadrao()
    self.getMinMax()
    self.getAmplitude()
    self.getQuartis()
    self.getIntervaloInterQuartil()
    self.getCoeficienteDeVariacao()
    self.getMediaDecis()

  def treatData(self):
    newData = []
    for item in self.data:
      if isinstance(item, list):
        newData.append(item[0])
      else: newData.append(item)
    self.data = newData  

  def getSoma(self):
    soma = 0
    for item in self.data:
      soma = soma + item
    self.soma = soma
  
  def getMedia(self):
    self.media = self.soma / len(self.data)
    return
  
  def getVarianca(self):
    soma = 0
    for item in self.data:
      soma = soma + ((item - self.media) ** 2)
    self.varianca = soma / (len(self.data) - 1)
    return

  def getDesvioPadrao(self):
    self.desvioPadrao = math.sqrt(self.varianca)
    return

  def getMinMax(self):
    minimo = self.data[0]
    maximo = self.data[0]
    for item in self.data:
      if item < minimo: minimo = item
      if item > maximo: maximo = item
    self.minimo = minimo
    self.maximo = maximo

  def getAmplitude(self):
    self.amplitude = self.maximo - self.minimo
  
  def getQuartis(self):
    # Sorting data
    sorted = self.data
    sorted.sort()
    self.q1 = sorted[round(len(sorted)/4) - 1]
    self.q2 = sorted[round(len(sorted)/4*2) - 1]
    self.q3 = sorted[round(len(sorted)/4*3) - 1]
    self.q4 = sorted[round(len(sorted)/4*4) - 1]


  def getIntervaloInterQuartil(self):
    self.intervaloInterQuartil = self.q3 - self.q1

  def getCoeficienteDeVariacao(self):
    self.coeficienteDeVariacao = (self.desvioPadrao / self.media) * 100

  def getMediaDecis(self):
    sorted = self.data
    sorted.sort()
    for i in range(10):
      decil = sorted[round(len(sorted)/10 * i) : round(len(sorted)/10 * (i + 1))]
      somaDecil = 0
      for item in decil:
        somaDecil = somaDecil + item
      setattr(self, 'd' + str(i+1) + 'M', somaDecil / len(decil))


print("\n >> [STATISTICS] Running statistics calculations...")
statistics = {
  "deaths": Statistic(deaths),
  "confirmed": Statistic(confirmed),
  "recovered": Statistic(recovered),
  "active": Statistic(active),
  "deathsVariation": Statistic(deathsVariation),
  "confirmedVariation": Statistic(confirmedVariation),
  "recoveredVariation": Statistic(recoveredVariation),
  "activeVariation": Statistic(activeVariation),
}



#PRINT STATISTICS
for key in statistics:
  print("   "+str(key), ": {")
  for keyB in statistics[key].__dict__:
    if keyB == "data": continue
    print("     ", keyB, ":", getattr(statistics[key], keyB))
  print("   }")

print(" >> [STATISTICS] DONE!")





# DRAW
print("\n >> [CHART] Drawing canvas...")
#plt.plot(getFileNames(files)[35:-1], deaths, 'r', getFileNames(files)[35:-1], confirmed, 'b', getFileNames(files)[35:-1], recovered, 'g', getFileNames(files)[35:-1], active, 'orange')
#plt.plot(getFileNames(files)[35:-1], confirmed, 'b')
#plt.plot(getFileNames(files)[35:-1], recovered, 'g')
#plt.plot(getFileNames(files)[35:-1], active, 'orange')
#plt.plot(getFileNames(files)[35:-1], deaths, 'r')

#plt.bar(getFileNames(files)[35:-1], confirmedVariation, color="b")
#plt.bar(getFileNames(files)[35:-1], recoveredVariation, color="g")
plt.bar(getFileNames(files)[35:-1], activeVariation, color="orange")
#plt.bar(getFileNames(files)[35:-1], deathsVariation, color="r")

desvioPadrao = []
for i in range(len(getFileNames(files)[35:-1])):
  desvioPadrao.append(statistics['activeVariation'].desvioPadrao)
plt.plot(getFileNames(files)[35:-1],  desvioPadrao, 'purple')

plt.xticks(rotation=25, ticks=[getFileNames(files)[35], getFileNames(files)[65],  getFileNames(files)[95], getFileNames(files)[125], getFileNames(files)[155], getFileNames(files)[185], getFileNames(files)[215], getFileNames(files)[240], getFileNames(files)[-1]])
#plt.xlabel('Gráfico completo do COVID-19 no Brasil (' + getFileNames(files)[35] + "-" + getFileNames(files)[-1] + ")")




# DECIL
#d = statistics['activeVariation']
#plt.bar(["0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8", "8-9", "9-10"], [d.d1M,d.d2M,d.d3M,d.d4M,d.d5M,d.d6M,d.d7M,d.d8M,d.d9M,d.d10M,], color="r")
#d = statistics['recovered']
#plt.bar(["0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8", "8-9", "9-10"], [d.d1M,d.d2M,d.d3M,d.d4M,d.d5M,d.d6M,d.d7M,d.d8M,d.d9M,d.d10M,], color="g")

print(" >> [CHART] DONE!")
print("\n>> ALL DONE!")
plt.show()
