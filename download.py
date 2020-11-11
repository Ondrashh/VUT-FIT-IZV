# Projekt do předmětu IZV, První část
# Zpracoval: Ondřej Pavlacký (xpavla15) 3BIT
# Implementace modulu download.py
# Vytvořeno: 11.11.2020
# VUT FIT

import requests
import os
import csv
import pickle
import gzip
from bs4 import BeautifulSoup
from enum import Enum
from zipfile import ZipFile
from io import TextIOWrapper
from datetime import datetime
import numpy as np

# Hlavní třída DataDownloader, která stahuje zip -> csv soubory které zpracuje a následně uchovává
class DataDownloader:
    # Vytvoření Enum Regions pro snadnou práci se zkratkami a jejich přiřazenými soubory
    class Regions(Enum):
        PHA = "00.csv"
        STC = "01.csv"
        JHC = "02.csv"
        PLK = "03.csv"
        KVK = "05.csv"
        ULK = "04.csv"
        LBK = "18.csv"
        HKK = "19.csv"
        PAK = "17.csv"
        OLK = "14.csv"
        MSK = "07.csv"
        JHM = "06.csv"
        ZLK = "15.csv"
        VYS = "16.csv"

    # inicializátor - obsahuje volitelné parametry:
    # V inicializátoru probíhá přířazení argumentů, abychom věděli s jakým URL a složkami mám pracovat
    def __init__(self, url='https://ehw.fit.vutbr.cz/izv/', folder ='data', cache_filename ='data_{}.pkl.gz'):
        self.url = url
        self.folder = folder
        self.cache_filename = cache_filename

    # funkce stáhne do datové složky folder všechny soubory s daty z adresy url.
    # Funkce po stáhnutí zip souborů z přiřazené URL adresy přečte 
    def download_data(self):

        r = requests.get("https://ehw.fit.vutbr.cz/izv/", headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"},allow_redirects=True)

        result = BeautifulSoup(r.text, "html.parser")
        zip_html_tag = result.findAll(class_='btn btn-sm btn-primary')

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        for item in zip_html_tag:
            url = item.get('href')
            link_to_download = 'https://ehw.fit.vutbr.cz/izv/' + url
            just_zip_name = url.split("/")
            download_request = requests.get(link_to_download, stream=True)
            with open(self.folder + '/' + just_zip_name[1], 'wb') as fd:
                fd.write(download_request.content)


    """nejsou data pro daný kraj stažená, stáhne je do datové složky folder. Poté
    je pro daný region specifikovaný tříznakovým kódem (viz tabulka níže) vždy
    vyparsuje do následujícího formátu dvojice (tuple), kde první položka je seznam
    (list) řetězců a druhá položka bude seznam (list) NumPy polí, schematicky:
    tuple(list[str], list[np.ndarray])
    Seznam řetězců odpovídá názvům jednotlivých datových sloupců, NumPy pole
    budou obsahovat data. Platí, že délka obou seznamů je stejná, shape všech
    NumPy polí je stejný. Při parsování přidejte nový sloupec “region”, který bude
    obsahovat tříznaký kód patřičného kraje, tj. odpovídá hodnotě region. Pro každý
    sloupec zvolte vhodný datový typ (t.j. snažte se vyhnout textovým řetězcům,
    vyřešte desetinnou čárku atp.). """
    def parse_region_data(self, region):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            self.download_data()
        data_head = ["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12",
                         "p13a", "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23",
                         "p24", "p27", "p28", "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b",
                         "p51", "p52", "p53", "p55a", "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k",
                         "l", "n", "o", "p", "q", "r", "s", "t", "p5a", "region"]

        # result_tuple = tuple(data_head, list[np.ndarray])
        lines_count = 0
        month = 0
        try:
            for file in os.listdir(self.folder):
                # print(self.folder + '/' + self.Regions[region].value)
                #print(file)

                current_file = self.folder + '/' + file
                rok_zip = current_file.rsplit('-', 2)
                if(file != "datagis2016.zip"):
                    if(len(rok_zip) > 2):
                        if(rok_zip[2] == "2020.zip"):
                            if(int(month) < int(rok_zip[1])):
                                month = rok_zip[1]

            year2020 = "datagis-" + month + "-2020.zip"
            files_to_extract = ["datagis2016.zip", "datagis-rok-2017.zip", "datagis-rok-2018.zip",
                               "datagis-rok-2019.zip", year2020]

            """item_array = np.ndarray(1)
            item_array = np.append(kokos, item_array)
            print(files_to_extract)
            for file in files_to_extract:
                current_zip = ZipFile(self.folder + '/' + file)
                with current_zip.open(self.Regions[region].value, 'r') as csvfile:
                    current_csv = list(csv.reader(TextIOWrapper(csvfile, encoding='windows-1250')))
                    # print(current_csv[1][0])
                    var = sum(1 for _ in current_csv)
                    lines_count += var
                    print(lines_count)
                    # item_array = np.append()
                    # for line in current_csv:
                    #  print(line)
            # print(item_array)"""

            cols = []
            for j in range(0, 6):
                if(j == 3 ):
                    a = np.array([], dtype=str)
                else:
                    a = np.array([], dtype=int)
                cols.append(a)
            test = [None]*65
            result_array =  []
            for file in files_to_extract:
                with ZipFile(self.folder + '/' + file, 'r') as zip:
                    with zip.open(self.Regions[region].value) as file:
                        reader = csv.reader(TextIOWrapper(file, "windows-1250",),delimiter=';')
                        for row in reader:
                            #print(row[0])
                            iter = 0
                            for i in row:
                                try:
                                    if(iter == 3):
                                        test[iter] = datetime.strptime(i, "%Y-%m-%d")
                                        #print(test[iter].year)
                                    else:
                                        test[iter] = int(i)
                                    iter += 1
                                except ValueError:
                                    test[iter] = i
                                    iter += 1
                            test[64] = region
                            #print(test[0])
                            # print(row[0])
                            # print(np.shape(row)
                            #print(np.shape(row))
                            #row = np.transpose(row)
                            #test = np.append(test, [region])
                            conv = int(row[0])
                            #print(type(conv))
                            #row[0] = conv
                            #print(type(row[0]))
                            #print(type(int(row[0])))

                            result_array.append(test)



                            # print(data)
                            # data = data.decode("windows-1250")
                            # data = data.replace('"', "")
                            # array = []
                            # var = np.transpose(data)
                            # print(var)
                            # print(data.count())
                            # data = data.replace(',', '.')
                            """for d in data.splitlines():
                                #print(d)
                                d = d.split(';')
                                d = np.transpose(d)
                                d = np.append(d, [region])"""
                            # print(d[0])
                        #print(d[63])
                        #array.append(d)
                        #print(np.shape(d))
                        #print(d[0][1])

                        #print(d)
                        #print(np.shape(d))
                        # print(d)
                        # print(np.shape(d))
                        #d = np.transpose(d)
                        #print(np.shape(d))
                        #print(np.shape(d))

                        # print(np.shape(d))
                        # print(np.shape(result_array))
                        #result_array.append(d)
                        #dalsi = result_array
                        #dalsi = np.transpose(dalsi)
                        # print(dalsi)
                        #print(np.shape(result_array))
            # print(np.shape(result_array[500]))
            # print(cols)
            #print(np.shape(result_array))
            # print(result_array[-1])
            # print(np.shape(result_array))
            #colums_rule = np.transpose(result_array)
            #print(np.shape(colums_rule))
            #print(cols[0])
                # print(colums_rule[j])

            #print(result_array[0])
            print("Parser did it, mom get the camera")
            """for item in result_array:
                for j in range(0, 64):
                    a = np.array([])
                    cols.append(a)"""

            result_array= np.transpose(result_array)
            #kokos = result_array[0]
            #print(type(kokos))
            #kokos1 = (map(int, kokos))
            #print(type(kokos1))
            #result_array[0] = list(map(int, result_array[0]))
            #print(type(result_array[0][0]))
            #print(result_array)
            #print(np.shape(result_array))
            # pr
            var = (data_head, result_array)
            #print(var)
            return var

        except KeyError:
            print("Not a valid region!")
            exit(101)


    """ get_list(self, regions = None)
    Vrací zpracovaná data pro vybrané kraje (regiony). Argument regions specifikuje
    seznam (list) požadovaných krajů jejich třípísmennými kódy. Pokud seznam není
    uveden (je použito None), zpracují se všechny kraje včetně Prahy. Výstupem funkce
    je dvojice ve stejném formátu, jako návratová hodnota funkce """
    def get_list(self, regions=None):
        cols = []
        for j in range(0, 65):
            if (j == 3):
                a = np.array([], dtype=str)
            else:
                a = np.array([], dtype=int)
            cols.append(a)
        if (regions == None):
            regions = []
            for region in self.Regions:
                regions.append(region.name)
            print(regions)
        get_list_result = []
        for region in regions:
            try:
                cache_file_name = self.cache_filename.replace("{}", region)
                with gzip.open(cache_file_name, 'rb') as f:
                    print(region, " : Beru ze souboru")
                    datas = pickle.load(f)
                    for i in range(0, 65):
                        cols[i] = np.append(cols[i], datas[1][i])


            except FileNotFoundError:
                print(region, " : Parsuju sam")
                cache_file_name = self.cache_filename.replace("{}", region)
                datas = self.parse_region_data(region)
                for i in range(0, 65):
                    cols[i] =  np.append(cols[i], datas[1][i])
                """with gzip.open(cache_file_name, 'wb') as f:
                     pickle.dump(datas, f)
                     f.close()"""
                #print(cols)
                #print(cols[64])
                print("Delam to pro tenhle:", region)
                #print(datas[0])
                #print(get_list_result)
        list_of_all = (datas[0], cols)
        # print(type(datas[1]))
        #rint(cols)
        #print(np.shape(cols))
        return list_of_all
"""Pro každý kraj získá data s využitím funkce parse_region_data tak, že se
budou výsledky uchovávat v paměti (v nějakém atributu instance třídy) a ukládat do
pomocného cache souboru pomocí následujícího schématu:
○ pokud už je výsledek načtený v paměti (tj. dostupný ve vámi zvoleném
atributu), vrátí tuto dočasnou kopii
○ pokud není uložený v paměti, ale je již zpracovaný v cache souboru, tak
načte výsledek z cache, uloží jej do atributu a vrátí.
○ jinak se zavolá funkce parse_region_data, výsledek volání se
uloží do cache, poté do paměti a výsledek vrátí
Pokud bude skript spuštěný jako hlavní (t.j. nebude importovaný jako modul)
1
pro 3 vámi vybrané kraje, stáhněte data
 (s využitím funkce get_list) a vypište do konzole základní
informace o stažených datech (jaké jsou sloupce, počet záznamů a jaké kraje jsou v
datasetu).
"""


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')
    kokos = DataDownloader()
    # kokos.download_data()
    # damn  = kokos.parse_region_data("JHM")
    kokos.get_list(["VYS"])
    # print(damn)

