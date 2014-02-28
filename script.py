# Experiment s geoprofilingem dle Rossmova vzorce: http://en.wikipedia.org/wiki/Rossmo's_formula
# Jan Cibulka 2014 - jan.cibulka@economia.cz
# data ve wgs84 UTM33

#Import knihoven
import csv
import pandas as pd
import math

# Načtení míst s graffiti
points = {}

pointFile = csv.reader(open('TEOF_points.txt'), delimiter=',', quotechar='"')
for row in pointFile:
    if(row[0] == 'OBJECTID'):
        continue
    points[row[1]] = [float(row[2].replace(',','')), float(row[3].replace(',',''))]

# Načtení adresních bodů, zdroj RÚIAN
addr = {}

addrFile = csv.reader(open('TEOF_addr.txt'), delimiter=',', quotechar='"')
for row in addrFile:
    if(row[0] == 'OBJECTID'):
        continue
    addr['a' + row[0]] = [float(row[17].replace(',','')), float(row[18].replace(',',''))]

# Vzorec
# Rossmo's formula: http://en.wikipedia.org/wiki/Rossmo's_formula

def rossmo(x, y, cx, cy, b):
    if((math.fabs(x - cx) + math.fabs(y - cy)) > b):
        buff = 1
    else:
        buff = 0
        
    return (buff / (math.fabs(x - cx) + math.fabs(y - cy))) - (((1 - buff) * buff) / (2 * buff - math.fabs(x - cx) - math.fabs(y - cy)))

#Samotný výpočet, uložení do csv
output = []
b = 0
k = 1.2

for address in addr:
    distance = 0
    x = addr[address][0]
    y = addr[address][1]
    
    for point in points:
        cx = points[point][0]
        cy = points[point][1]
        
        distance = distance + k * rossmo(x, y, cx, cy, b)
    output.append([address, x, y, distance])

data = pd.DataFrame(output, columns=['address', 'X', 'Y', 'probab'])
data.sort('probab', ascending=False).to_csv('output.csv')