# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class DataDownloader:
    # inicializátor - obsahuje volitelné parametry:
    def __init__(self, url='https://ehw.fit.vutbr.cz/izv/', folder ='data', cache_filename ='data_{}.pkl.gz'):
        kokot = 5

    # funkce stáhne do datové složky folder všechny soubory s daty z adresy url.
    def download_data(self):
        sdasd = 1

    UserAgent()

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    r = requests.get("https://ehw.fit.vutbr.cz/izv/", allow_redirects=True)

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
        sdasd = 1

    """ get_list(self, regions = None)
    Vrací zpracovaná data pro vybrané kraje (regiony). Argument regions specifikuje
    seznam (list) požadovaných krajů jejich třípísmennými kódy. Pokud seznam není
    uveden (je použito None), zpracují se všechny kraje včetně Prahy. Výstupem funkce
    je dvojice ve stejném formátu, jako návratová hodnota funkce """
    def get_list(self, regions = None):
        sdasd = 1




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
    print(kokos.parse_region_data("kokos1"))

