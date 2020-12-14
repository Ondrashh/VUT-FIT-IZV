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

    # Funkce stáhne do datové složky folder všechny soubory s daty z adresy url.
    # Funkce po stáhnutí zip souborů z přiřazené URL adresy přečte 
    def download_data(self):

        # GET request na získání obsahu stránky, přidána hlavička aby nás server neodmítnul
        r = requests.get("https://ehw.fit.vutbr.cz/izv/", headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"},allow_redirects=True)

        # Rozparsování html souboru, abych mohli přistupovat k elementům
        result = BeautifulSoup(r.text, "html.parser")
        # Chceme získat tak buttonu, protože pod ním se skrývá odkaz na zip soubory
        zip_html_tag = result.findAll(class_='btn btn-sm btn-primary')

        # Pokud složka do které chceme importovat neexistuje, tak ji vytvoříme
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        # Pro každý odkaz stáhneme soubory abychom je mohli zpacovat
        for item in zip_html_tag:
            # Tady probíhá získávání odkazu a následné stahování zip souborů do složky folder
            url = item.get('href')
            link_to_download = 'https://ehw.fit.vutbr.cz/izv/' + url
            just_zip_name = url.split("/")
            download_request = requests.get(link_to_download, stream=True)
            with open(self.folder + '/' + just_zip_name[1], 'wb') as fd:
                fd.write(download_request.content)

    # Tato funkce rozparsuje tada z jednotlivých zip souborů pro kraje, tak abychom je mohli dále použít
    # ----------------------------------------------------------------------------------------------------------
    # DŮLEŽITÉ: data nejsou "čistěna" od anomálií, např. věci jako jsou XX v sloupcí s číselnou hodnotou
    # schválně poněchány, ale v implementaci se snažím číselné hodnoty ukládat jako int a věci, které se takto
    # nedají uložit nechávám jako string => tudíž později poznám nevalidní data jiným typem
    # Doufám tedy, že jsem tímto splnit podmínky "očistění" dat, protože pokud se tato metoda ukáže v další
    # fázi jako neefektví tuto část bych přepracoval
    # ----------------------------------------------------------------------------------------------------------
    # Metoda je primárně volána pomocí get_list()
    # Argumenty: region - jeden kraj, který zpracuje
    # returns: tuple(list[str_nazvy_sloupcu], list[np.ndarrays_data sloupců])
    def parse_region_data(self, region):
        # Pokud složka neexistuje, musím si ji vytvořit a stáhnout všechny soubory
        # Viz. zadání
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            # Je volána metoda download_data()
            self.download_data()

        # Definice první části tuple, definovány názvy datových sloupců
        data_head = ["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12",
                         "p13a", "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23",
                         "p24", "p27", "p28", "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b",
                         "p51", "p52", "p53", "p55a", "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k",
                         "l", "n", "o", "p", "q", "r", "s", "t", "p5a", "region"]

        # Definuji si měsíc, protože dynamicky hledám poslední měsíc v roce 2020
        month = 0
        try:
            # Pro každou položku ve složce folder hledám příslušný soubor pro konec roku
            for file in os.listdir(self.folder):
                # Získání celé adresy
                current_file = self.folder + '/' + file
                # Rozparsování názvu zip souborů abych mohl najít poslední soubor v roce 2020
                rok_zip = current_file.rsplit('-', 2)
                if(file != "datagis2016.zip"):
                    if(len(rok_zip) > 2):
                        if(rok_zip[2] == "2020.zip"):
                            if(int(month) < int(rok_zip[1])):
                                #Získám si poslední měsíc v roce 2020
                                month = rok_zip[1]
            # Sestavení názvu souboru s daty posledního měsíce v roce 2020
            year2020 = "datagis-" + month + "-2020.zip"
            # Seznam souborů definující konce jednotlivých roků a podle nich vyhledávám data
            files_to_extract = ["datagis2016.zip", "datagis-rok-2017.zip", "datagis-rok-2018.zip",
                               "datagis-rok-2019.zip", year2020]


            # Definice výsledného array, kam poté appenduji jednotlivé řádky
            result_array = []
            # Cyklus na průchod souborů konců roků a následná extrakce řádků, které budu poté potřebovat
            for file in files_to_extract:
                if not os.path.isfile(self.folder + '/' + file):
                    print("Stahuji znovu")
                    self.download_data()
                with ZipFile(self.folder + '/' + file, 'r') as zip:
                    with zip.open(self.Regions[region].value) as file:
                        reader = csv.reader(TextIOWrapper(file, "windows-1250",),delimiter=';')
                        # Potřebuji projít každý řádek v souboru
                        for row in reader:
                            iter = 0
                            # Vytvoření pomocného listu, abych mohl přetypovávat hodnoty jednotlivých řádků
                            test = [None] * 65
                            # Tento cyklus slouží k průchodu všech prvků řádku abych je přetypovat
                            for i in row:
                                try:
                                    # Vím že na této pozici se nachází datum, které přetypuji na datetime formát
                                    if(iter == 3):
                                        test[iter] = datetime.strptime(i, "%Y-%m-%d")
                                    # Následně zkusím přetypovat content na číslo, protože většina obsahu jsou čísla
                                    else:
                                        test[iter] = int(i)
                                    iter += 1
                                # Pokud je obsah nic, nebo string tak se přiřadí typem string
                                except ValueError:
                                    test[iter] = i
                                    iter += 1
                            # Přiřazení regionu na konec viz. zadání
                            test[64] = region
                            # Append s výskedným arrayem, které symbolizuje výsledek
                            result_array.append(test)

            # Velmi důležitá část, měním závislost řádku a sloupců, protože když to otočím
            # můžu jednododuše získat jednotlivé sloupce s daty
            result_array= np.transpose(result_array)

            # Vytvoření výsledné dvojice (tuple)
            var = (data_head, result_array)

            # Funkce vrací tuple(list[str], list[np.ndarray])
            # Viz. zadání
            return var

        # Probíhá kontrola, jestli je vůbec zadán validní kraj
        except KeyError:
            print("Not a valid region!")
            exit(101)


    # Funkce vrací zpracovaná dat pro kraje, které jsou mu zadané
    # Pro zpracování volá metodu parse_region_data !
    # Argumenty: regions - seznam regionů, které zpracovává (None = všechny)
    # returns: tuple(list[str_nazvy_sloupcu], list[np.ndarrays_data sloupců])
    # V podstatě vrací to stejné co parse_region_data, ale rozšířené
    def get_list(self, regions=None):
        # Vytvoření arraye abychom mohli získat výsledky ze souboru
        cols = []
        for j in range(0, 65):
            if (j == 3):
                a = np.array([], dtype=str)
            else:
                a = np.array([], dtype=int)
            cols.append(a)

        # Pokud není zadán žádný kraj bereme všechny viz. zadání
        if (regions == None):
            regions = []
            for region in self.Regions:
                regions.append(region.name)
        # Cyklus se provede pro všechny zadané regiony
        # Dělí se na:
        # 1) Pokud je soubor s daty kraje už uložen - otevře ho a data vezme z něj a vrátí je
        # 2) Pokud není uložen tak zavolá metodu parse_region_data a následně vytvoří soubor a vrátí hodnotu
        for region in regions:
            try:
                # Získá si název cache souboru jak by se měl jmenovat
                cache_file_name = self.folder + '/' + self.cache_filename.replace("{}", region)
                # Pokusí se ho otevřit
                with gzip.open(cache_file_name, 'rb') as f:
                    # Pomocí pickle se vytáhne data
                    datas = pickle.load(f)
                    # Přiřazení do listu polí
                    for i in range(0, 65):
                        cols[i] = np.append(cols[i], datas[1][i])
            # Pokud cache file neexistuje, tak si ho vytvoříme
            except FileNotFoundError:
                # Vytvoření názvu cache souboru
                cache_file_name = self.folder + '/' + self.cache_filename.replace("{}", region)
                # Získání dat o regionu pomocí metody parse_region_data
                datas = self.parse_region_data(region)
                # Přiřazení do pomocného listu polí
                for i in range(0, 65):
                    cols[i] =  np.append(cols[i], datas[1][i])
                # Vytvoření cache souboru s daty pr odalší použití
                with gzip.open(cache_file_name, 'wb') as f:
                     pickle.dump(datas, f)
                     f.close()

        # Vytvoření dvojice (tuple), abychom ji mohli vrátit
        list_of_all = (datas[0], cols)

        # Vrací tuple(list[str_nazvy_sloupcu], list[np.ndarrays_data sloupců])
        return list_of_all

# Main, pokud bude skript spuštěn samostatně vyberu si 3 kraje a rozparsuji data
if __name__ == '__main__':
    # Vypsání základních informací a zpracování předdefinovaných dat
    print("Spuštění skriptu jako hlavní: načítání dat...")
    data = DataDownloader().get_list(["VYS", "JHM", "OLK"])
    print("Sloupce:", data[0])
    print("Počet sloupců a množství záznamů:", np.shape(data[1]))
    print("Kraje které jsem vybral: VYS, JHM, OLK")

