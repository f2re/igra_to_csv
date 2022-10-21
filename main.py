# -*- coding: utf-8 -*-
from   datetime import datetime as dt
# подключаем библиотеку подключения к монго
import re
import sys

# 
# парсим данные в csv из файла
# 
def parse_aero_from_csv( file ):
  
  fout = open(file+"-air.csv", "wt")

  count = 0
  print("\nUsing readline()") 

  curdate = False

  # create DF
  # df = pd.DataFrame(columns = [ 'dt','L','H','T','D','dd','ff' ])
  # df.columns = [ 'dt','L','H','T','D','dd','ff' ]
  fp = open(file,'r')
  lines = fp.readlines()

  fout.write( ";".join(['date','L','H','T','D','dd','ff'])+"\n" )

  for line in lines:
    line = line.strip()

    # если начинается с решетки, то меняем дату
    if line[0]=="#":
      splitted = re.sub('\s+',' ',line).split(' ')
      hour = int(splitted[4])
      hour = 0 if hour>23 else hour
      curdate = dt( int(splitted[1]), int(splitted[2]), int(splitted[3]), hour, 0 )
    else:
      # 21 -9999  99500A  149    95A  710 -9999 -9999 -9999 
      # 21 -9999 100200A  149    32A  840 -9999 -9999 -9999 
      # 10 -9999  50000  5560B -208B  380 -9999   350   240 
      data = []
      if curdate is not False:
        data.append(curdate.strftime('%Y-%m-%d %H:%M:%S')) #['dt'] 
        # print(data) 
        # уровень
        data.append(str(float(re.sub('[a-zA-Z]*','',line[8:16]).strip())/100) ) #['L']   
        # высота
        data.append(str(float(re.sub('[a-zA-Z]*','',line[17:22]).strip())) ) #['H']   
        # высота
        data.append(str(float(re.sub('[a-zA-Z]*','',line[23:28]).strip())/10) ) #['T']   
        data.append(str(float(re.sub('[a-zA-Z]*','',line[34:39]).strip())/10) ) #['D']   
        data.append(str(float(re.sub('[a-zA-Z]*','',line[40:45]).strip())) ) #['dd']  
        data.append(str(float(re.sub('[a-zA-Z]*','',line[46:51]).strip())/10) ) #['ff']  

      count += 1
      fout.write(";".join(data)+"\n")

  fout.close()
  print("Aero file "+file+"-air.csv"+" saved!")

  return data

if len(sys.argv) >1:
  parse_aero_from_csv(sys.argv[1])