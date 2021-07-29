import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
import ast
import os

data = pd.read_csv("tr-vaccination.csv")
cities = data.columns.to_list()[5:]
date = (date.today() - timedelta(days = 1)).strftime("%d.%m.%Y")
data2 = pd.DataFrame(columns = data.columns.to_list()[1:5])
data3 = pd.read_excel("nufus1.xlsx")

cur_index = len(data)-1

if not os.path.exists("images"):
    os.mkdir("images")
    
if not os.path.exists("images/" + date):
    os.mkdir("images/" + date)

if not os.path.exists("images/" + date + "/sorted"):
    os.mkdir("images/" + date + "/sorted")
    
if not os.path.exists("images/" + date + "/unsorted"):
    os.mkdir("images/" + date + "/unsorted")
    
for city in cities:
    yesterday = ast.literal_eval(data[city][cur_index - 1])
    today = ast.literal_eval(data[city][cur_index])
    firstDose = int(today["1.doz"].replace(".","")) - int(yesterday["1.doz"].replace(".",""))
    secondDose = int(today["2.doz"].replace(".","")) - int(yesterday["2.doz"].replace(".",""))
    try:
        thirdDose = int(today["3.doz"].replace(".","")) - int(yesterday["3.doz"].replace(".",""))
    except:
        thirdDose = int(today["3.doz"].replace(".",""))
    totalDose = int(today["toplam"].replace(".","")) - int(yesterday["toplam"].replace(".",""))
    new_row = {'toplam': totalDose, '1.doz': firstDose, '2.doz': secondDose, '3.doz': thirdDose}
    data2 = data2.append(new_row, ignore_index = True)
    
data2.index = cities
data2["18üstü"] = data3["18üstü"].to_list()[1:]
data2["genel"] = data3["toplam"].to_list()[1:]
data2["1dozoran"] = ["%.2f" % (elem*100) + "%" for elem in (data2["1.doz"] / data2["18üstü"]).to_list()]
data2["2dozoran"] = ["%.2f" % (elem*100) + "%" for elem in (data2["2.doz"] / data2["18üstü"]).to_list()]
data2["toplamoran"] = [elem for elem in (data2["toplam"] / data2["18üstü"]).to_list()]
data2["g1dozoran"] = ["%.2f" % (elem*100) + "%" for elem in (data2["1.doz"] / data2["genel"]).to_list()]
data2["g2dozoran"] = ["%.2f" % (elem*100) + "%" for elem in (data2["2.doz"] / data2["genel"]).to_list()]
data2["gtoplamoran"] = [elem for elem in (data2["toplam"] / data2["genel"]).to_list()]
for i in range(3):
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Şehir', 'Toplam', '1.Doz', '2.Doz', '3.Doz', '18 Üstü 1.Doz', '18 Üstü 2.Doz'],
                    fill_color = 'rgb(251,180,174)',
                    align='left'),
        cells=dict(values=[data2.index[27*i:27*(i+1)], 
                           data2['toplam'][27*i:27*(i+1)], 
                           data2['1.doz'][27*i:27*(i+1)], 
                           data2['2.doz'][27*i:27*(i+1)], 
                           data2['3.doz'][27*i:27*(i+1)], 
                           data2["1dozoran"][27*i:27*(i+1)], 
                           data2["2dozoran"][27*i:27*(i+1)],
                           data2["g1dozoran"][27*i:27*(i+1)], 
                           data2["g2dozoran"][27*i:27*(i+1)]],
                   fill_color = 'rgb(203,213,232)',
                   align = 'left'))])
    fig.add_annotation(x=0.007, y=1.03,
            text=date,
            showarrow=False)
    fig.update_layout(title_text = "Günlük Aşılama Değerleri - " + str(i+1), 
                      title_x = 0.5,
                      font=dict(size=12),
                      title_font=dict(size=20),
                      width=1000, 
                      height=800)        
    fig.write_image("images/" + date + "/unsorted/günlük-" + str(i+1) + ".png")
    
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Şehir', 'Toplam', '1.Doz', '2.Doz', '3.Doz', '18 Üstü 1.Doz', '18 Üstü 2.Doz', 'Genel 1.Doz', 'Genel 2.Doz'],
                    fill_color = 'rgb(251,180,174)',
                    align='left'),
        cells=dict(values=[data2.sort_values(by=['toplamoran'], ascending = False).index[27*i:27*(i+1)], 
                           data2.sort_values(by=['toplamoran'], ascending = False)['toplam'][27*i:27*(i+1)], 
                           data2.sort_values(by=['toplamoran'], ascending = False)['1.doz'][27*i:27*(i+1)], 
                           data2.sort_values(by=['toplamoran'], ascending = False)['2.doz'][27*i:27*(i+1)], 
                           data2.sort_values(by=['toplamoran'], ascending = False)['3.doz'][27*i:27*(i+1)], 
                           data2.sort_values(by=['toplamoran'], ascending = False)["1dozoran"][27*i:27*(i+1)], 
                           data2.sort_values(by=['toplamoran'], ascending = False)["2dozoran"][27*i:27*(i+1)],
                           data2.sort_values(by=['toplamoran'], ascending = False)["g1dozoran"][27*i:27*(i+1)], 
                           data2.sort_values(by=['toplamoran'], ascending = False)["g2dozoran"][27*i:27*(i+1)]],
                   fill_color = 'rgb(203,213,232)',
                   align = 'left'))])
    fig.add_annotation(x=0.007, y=1.03,
            text=date,
            showarrow=False)
    fig.update_layout(title_text ="Toplam Doza Göre Sıralı Günlük Aşılama Değerleri - " + str(i+1), 
                      title_x = 0.5,
                      font=dict(size=12),
                      title_font=dict(size=20),
                      width=1000, 
                      height=800)
                          
    fig.write_image("images/" + date + "/sorted/günlük-" + str(i+1) + ".png")
data2.to_csv("images/" + date + "/daily-vaccination.csv", sep = ",", encoding= "utf-8-sig")
    