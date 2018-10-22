#!/usr/bin/env python
# coding: utf-8

# In[10]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_csv("skigebiete_linkliste.csv")
linkliste = df['0'].tolist()

skigebiete_final = []
for gebiet_link in linkliste:
    print(gebiet_link)
    website = requests.get("https://www.bergfex.ch"+gebiet_link).text
    soup = BeautifulSoup(website, "html.parser")

    # Titel des Skigebiets
    titel = soup.find('h1', {"class": "has-sup"})
    titel = (titel.text.replace("Skigebiet ", ""))
    # Offene Skilifte auslesen
    for skigebiet in soup.find_all('table', class_="schneewerte"):
        try:
            offenelifte = (skigebiet.find_all('td')[-1].text).split(" von ") # Auslesen im Format "12 von 24" (offene Lifte sind immer das letzte TD, deshalb -1)
            total = offenelifte[1].strip()
            offen = offenelifte[0].strip()
            skigebiete_final.append({"titel": titel, "totallifte": total, "offen": offen}) # In die finale Liste laden
        except:
            print("Fehler mit Skigebiet: "+"https://www.bergfex.ch"+gebiet_link)

df_skigebiete = pd.DataFrame(skigebiete_final)
import datetime

now = datetime.datetime.now()
#print (now.strftime("%Y-%m-%d %H:%M"))
df_skigebiete.to_csv('skigebiete_oeffnungszeiten/'+now.strftime("%Y-%m-%d_%H-%M_skigebiete_oeffnungszeiten.csv"))


# In[ ]:




