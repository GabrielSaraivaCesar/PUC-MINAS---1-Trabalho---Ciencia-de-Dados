import csv
import matplotlib.pyplot as plt
from os import walk
import numpy as np
import math
import sys

print("\n>> RUNNING DATA PRINTER")

countryName = "Brazil"
if len(sys.argv) > 1:
  countryName = " ".join(sys.argv[1:])
  

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

with open('../treatedData/'+ countryName +'.csv') as file:
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


def loadStatistics():
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
  # for key in statistics:
  #   print("   "+str(key), ": {")
  #   for keyB in statistics[key].__dict__:
  #     if keyB == "data": continue
  #     print("     ", keyB, ":", getattr(statistics[key], keyB))
  #   print("   }")

  return statistics

  print(" >> [STATISTICS] DONE!")





# DRAW
def loadChart(statistics):
  def plotRange():
    return getFileNames(files)[(len(files) - len(data)):-1]
  
  def getLabels():
    def pers(value, total):
      return round(total/100*value)
    names = getFileNames(files)
    labels = [names[-1]]
    for i in range(9):
      labels.append(names[pers((i+1)*10, len(names))])
      print(pers(i*10, (len(names))))
    print(labels)
    return labels

  print("\n >> [CHART] Drawing canvas...")
  
  fig, axs = plt.subplots(2,2)
  fig.subplots_adjust(hspace=0.4)
  
  #ax1.plot(plotRange(), deaths, 'r', plotRange(), confirmed, 'b', plotRange(), recovered, 'g', plotRange(), active, 'orange')
  axs[0,0].plot(plotRange(), confirmed, 'b')
  axs[0,1].plot(plotRange(), recovered, 'g')
  axs[1,0].plot(plotRange(), active, 'orange')
  axs[1,1].plot(plotRange(), deaths, 'r')
  
  #ax1.set_xticks(ticks=getLabels())
  axs[0,0].set_xticks(ticks=getLabels())
  axs[0,1].set_xticks(ticks=getLabels())
  axs[1,0].set_xticks(ticks=getLabels())
  axs[1,1].set_xticks(ticks=getLabels())

  axs[0,0].set_xticklabels(fontsize=7, rotation=15, labels=getLabels())
  axs[0,0].set_title("Casos Confirmados")

  axs[0,1].set_xticklabels(fontsize=7, rotation=15, labels=getLabels())
  axs[0,1].set_title("Recuperações")

  axs[1,0].set_xticklabels(fontsize=7, rotation=15, labels=getLabels())
  axs[1,0].set_title("Casos Ativos")
  
  axs[1,1].set_xticklabels(fontsize=7, rotation=15, labels=getLabels())
  axs[1,1].set_title("Mortes")

  #plt.bar(plotRange(), confirmedVariation, color="b")
  #plt.bar(plotRange(), recoveredVariation, color="g")
  #plt.bar(plotRange(), activeVariation, color="orange")
  #plt.bar(plotRange(), deathsVariation, color="r")

  desvioPadrao = []
  for i in range(len(plotRange())):
    desvioPadrao.append(statistics['active'].desvioPadrao)
  #plt.plot(plotRange(),  desvioPadrao, 'purple')

  #plt.xlabel('Gráfico completo do COVID-19 no Brasil (' + getFileNames(files)[35] + "-" + getFileNames(files)[-1] + ")")




  # DECIL
  #d = statistics['activeVariation']
  #plt.bar(["0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8", "8-9", "9-10"], [d.d1M,d.d2M,d.d3M,d.d4M,d.d5M,d.d6M,d.d7M,d.d8M,d.d9M,d.d10M,], color="r")
  #d = statistics['recovered']
  #plt.bar(["0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-7", "7-8", "8-9", "9-10"], [d.d1M,d.d2M,d.d3M,d.d4M,d.d5M,d.d6M,d.d7M,d.d8M,d.d9M,d.d10M,], color="g")
  plt.show()
  print(" >> [CHART] DONE!")

statistics = loadStatistics()
loadChart(statistics)

print("\n>> ALL DONE!")

