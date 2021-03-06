import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

cur = pd.read_csv("tr-vaccination.csv")
df = pd.DataFrame()
cities = cur.columns.tolist()[3:]

URL = "https://covid19asi.saglik.gov.tr/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
element = soup.find("div", attrs={'class': 'svg-turkiye-haritasi'})
elem = element.find_all("script")

temp = []
temp.append("".join(filter(str.isdigit,elem[0].string)))
df["toplam"] = temp

temp = []
temp.append("".join(filter(str.isdigit,elem[2].string))[1:])
df["1.doz"] = temp

temp = []
temp.append("".join(filter(str.isdigit,elem[3].string))[1:])
df["2.doz"] = temp

temp = []
temp.append(str(int(df.toplam) - int(df['1.doz']) - int(df['2.doz'])))
df["3.doz"] = temp

temp = []
temp.append(elem[4].string.split("'")[1])
df["date"] = temp

g_nodes = element.find_all("g")[1:]
for node in g_nodes:
    city = node["data-adi"]
    temp = []
    temp.append({"toplam": node["data-toplam"], "1.doz": node["data-birinci-doz"], 
                 "2.doz": node["data-ikinci-doz"], 
                 "3.doz": re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(int(node["data-toplam"].replace(".","")) - int(node["data-birinci-doz"].replace(".","")) - int(node["data-ikinci-doz"].replace(".",""))))})
    df[city] = temp

cur = cur.append(df, ignore_index = True)    
cur.to_csv("tr-vaccination.csv", sep = ",", encoding= "utf-8-sig", index = False)

## used these to initialize the dataframe at day 0.
"""df["toplam"] = []
df["1.doz"] = []
df["2.doz"] = []
df["Adana"] = []
df["Adıyaman"] = []
df["Afyon"] = []
df["Ağrı"] = []
df["Amasya"] = []
df["Ankara"] = []
df["Antalya"] = []
df["Artvin"] = []
df["Aydın"] = []
df["Balıkesir"] = []
df["Bilecik"] = []
df["Bingöl"] = []
df["Bitlis"] = []
df["Bolu"] = []
df["Burdur"] = []
df["Bursa"] = []
df["Çanakkale"] = []
df["Çankırı"] = []
df["Çorum"] = []
df["Denizli"] = []
df["Diyarbakır"] = []
df["Edirne"] = []
df["Elazığ"] = []
df["Erzincan"] = []
df["Erzurum"] = []
df["Eskişehir"] = []
df["Gaziantep"] = []
df["Giresun"] = []
df["Gümüşhane"] = []
df["Hakkari"] = []
df["Hatay"] = []
df["Isparta"] = []
df["Mersin"] = []
df["İstanbul"] = []
df["İzmir"] = []
df["Kars"] = []
df["Kastamonu"] = []
df["Kayseri"] = []
df["Kırklareli"] = []
df["Kırşehir"] = []
df["Kocaeli"] = []
df["Konya"] = []
df["Kütahya"] = []
df["Malatya"] = []
df["Manisa"] = []
df["Manisa"] = []
df["Kahramanmaraş"] = []
df["Mardin"] = []
df["Muğla"] = []
df["Muş"] = []
df["Nevşehir"] = []
df["Niğde"] = []
df["Ordu"] = []
df["Rize"] = []
df["Sakarya"] = []
df["Samsun"] = []
df["Siirt"] = []
df["Sinop"] = []
df["Sivas"] = []
df["Tekirdağ"] = []
df["Tokat"] = []
df["Trabzon"] = []
df["Tunceli"] = []
df["Şanlıurfa"] = []
df["Uşak"] = []
df["Van"] = []
df["Yozgat"] = []
df["Zonguldak"] = []
df["Aksaray"] = []
df["Bayburt"] = []
df["Karaman"] = []
df["Kırıkkale"] = []
df["Batman"] = []
df["Şırnak"] = []
df["Bartın"] = []
df["Ardahan"] = []
df["Iğdır"] = []
df["Yalova"] = []
df["Karabük"] = []
df["Kilis"] = []
df["Osmaniye"] = []
df["Düzce"] = []"""