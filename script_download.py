# -*- coding: utf-8 -*-

# Lo scipt originale è stato perso il 31/07/2022 a causa di un danneggiamento dell'HDD del PC fisso con sopra Windows 7
# Questa è una ricostruzione ottenuta partendo da uno screen e dalla cronologia di Chrome dei giorni 9-10 luglio 2022

# Siti internet consultati:
# 1) ottenere tutti i link delle download pages contenuti nella pagina principale
#       https://pythonprogramminglanguage.com/get-links-from-webpage/
# 2) creare una cartella per il salvataggio + scaricare e salvare i file pdf + rinominare i file automaticamente (risposta di SIM + medyas)
#       https://stackoverflow.com/questions/54616638/download-all-pdf-files-from-a-website-using-python

# Altri siti consultati, ma scartati in seguito come soluzioni (troppo complicati o poco chiari per me):
# https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests/16696317#16696317
# https://stackoverflow.com/questions/1080411/retrieve-links-from-web-page-using-python-and-beautifulsoup
# https://python.plainenglish.io/notesdownloader-use-web-scraping-to-download-all-pdfs-with-python-511ea9f55e48
# https://stackoverflow.com/questions/43359121/is-there-a-better-simpler-way-to-download-multiple-files
# https://stackoverflow.com/questions/57270165/how-to-download-multiple-files-using-python-3-7
# https://stackoverflow.com/questions/46264056/python-download-multiple-files-from-links-on-pages



import os
import requests
from urllib.parse import urljoin
from urllib import request
from bs4 import BeautifulSoup

#%% Ottenere l'elenco dei link che portano alle pagine di download

url_sito = 'https://ocw.mit.edu/courses/16-225-computational-mechanics-of-materials-fall-2003/pages/assignments/'

# scarica il webpage data, però è codificato ("surrounded by HTML tags")
html_pagina = request.urlopen(url_sito)
# BeautifoulSoup è un parser per l'HTML e restituisce un HTML leggibile anche da un umano dopo il parsing
soup = BeautifulSoup(html_pagina, "lxml")

elenco_link = []
# il codice HTML dopo il parsing viene fatto passare e, quando si trova la 'a' (che, a quanto pare, indica un link nel linguaggio HTML),
# il corrispondente link viene scaricato
# Così si ottengono tutti i link esistenti, ma solo quelli che portano al download dei file servono: la parola_flag è contenuta solo nei
# link utili e solamente questi vengono salvati nell'elenco_link
parola_flag = 'resources'
for link in soup.find_all('a'):
    if str(link).find(parola_flag) != -1:
        elenco_link.append(link.get('href'))

# i link ottenuti finora sono "mozzi": manca la parte iniziale che indica il protocollo + dominio (i.e. https://ocw.mit.edu)
# Dato che ogni link ha sempre la forma https://dominio/..., si vede che l'url iniziale è tutto ciò che c'è prima del terzo '/'
# (l'ultimo '/' non serve perché i link in elenco_link contengono già la '/' all'inizio)

# taglia l'url usando '/' come separatore e lo rimette insieme inserendo '/' tra ogni pezzi, usando pezzi_url[0:3] si stanno
# considerando solo i primi 3 pezzi (i.e. tutto ciò che c'è prima del terzo '/')
pezzi_url = url_sito.split('/')     
url_base = '/'.join(pezzi_url[0:3])

# gli url vengono poi "ricuciti"
link_completi = []
for link_i in elenco_link:
    link_completi.append(url_base + link_i)


#%% Scaricare i pdf

# ora che l'elenco dei link è stato ottenuto, bisogna andare in ognuno di essi e scaricare il file

# se non esiste una cartella con questo nome, la crea
# (la r di RAW serve per far funzionare l'indirizzo, altre possibilità sono "C:/nome" o "C:\\nome"
# dato che il normale '\' viene letto come se fosse un carattere Unicode, tipo \n = "a capo")
path_cartella_download = r'C:\Users\andre\Downloads\MIT_OCW'
if not os.path.exists(path_cartella_download):
    os.mkdir(path_cartella_download)


for url in link_completi:
    # "GET request", credo che sia per avere accesso al codice HTML
    my_file = requests.get(url)
    soup = BeautifulSoup(my_file.text, "html.parser")
    
    # SOLUZIONE 1
    # prende il link completo, lo divide in stringhe usando '/' come separatore e considera il penultimo pezzo
    # (contiene il nome originale del file, mentre l'ultimo è solo uno spazio bianco IN QUESTO CASO)
    # NB: l'estensione NON è compresa in QUESTO link e dev'essere aggiunta a mano
    nome_file_pdf = url.split('/')[-2] + '.pdf'
    nome_file = os.path.join(path_cartella_download, nome_file_pdf)
    
    # fruga nel codice HTML alla ricerca delle stringhe che contengono il nome del file con la sua estensione
    for link in soup.select("a[href$='.pdf']"):
        # SOLUZIONE 2
        # più automatica (considera automaticamente l'estensione e considera anche la possibilità che ci siano più file nella stessa pagina),
        # ma crea dei nomi tendenzialmente osceni per i file (codice alfanumerico + nome del pdf)
        # nome_file_pdf = link['href'].split('/')[-1]
        # nome_file = os.path.join(path_cartella_download, nome_file_pdf)
        
        # 'wb' = Writing Binary (crea il file, ma non modifica il suo contenuto?)
        with open(nome_file, 'wb') as f:
            url_del_pdf = urljoin(url, link['href'])
            f.write(requests.get(url_del_pdf).content)



#%% Main del file

#link_sito = 'https://ocw.mit.edu/courses/16-225-computational-mechanics-of-materials-fall-2003/pages/lecture-notes/'
