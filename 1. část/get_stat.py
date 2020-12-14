# Projekt do předmětu IZV, První část
# Zpracoval: Ondřej Pavlacký (xpavla15) 3BIT
# Implementace modulu get_stat.py
# Vytvořeno: 11.11.2020
# VUT FIT

import numpy as np
import sys
import os
import copy
import matplotlib.pyplot as plt
import argparse
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from download import DataDownloader

# Funkce určená k vykreslovní grafů pro data a statistiky z krajů
def plot_stat(data_source, fig_location = None, show_figure = False):

    # Znovu si transppnuji array abych mohl filtrovat podle řádků a ne podle sloupců
    array_to_filter = np.transpose(data_source[1])

    # Seznamy pro jednotlivé roky které si vyparsuju z celkových dat
    rok2016 = []
    rok2017 = []
    rok2018 = []
    rok2019 = []
    rok2020 = []

    # Parsování dat pro jednotlivé roky
    for zaznam in array_to_filter:
        if(zaznam[3].year == 2016):
            rok2016.append(zaznam)
        if (zaznam[3].year == 2017):
            rok2017.append(zaznam)
        if (zaznam[3].year == 2018):
            rok2018.append(zaznam)
        if (zaznam[3].year == 2019):
            rok2019.append(zaznam)
        if (zaznam[3].year == 2020):
            rok2020.append(zaznam)

    # Vytvoření seznamů pro uschování dat pro jednotlivé kraje a roky
    regions2016 = []
    keywords = []
    # Získání regionů 
    for item in rok2018:
            if item[64] not in regions2016:
                regions2016.append(item[64])
    keywords = regions2016
    counts2016 = np.zeros(len(regions2016))
    dic2016 = dict(zip(regions2016, counts2016))
    dic2017 = copy.deepcopy(dic2016)
    dic2018 = copy.deepcopy(dic2016)
    dic2019 = copy.deepcopy(dic2016)
    dic2020 = copy.deepcopy(dic2016)

    # Nahrávání do dictionary četnosti jednotlivých krajů
    for item in rok2016:
        for keyword in keywords:
            if(keyword == item[64]):
                dic2016[keyword] += 1
    for item in rok2017:
        for keyword in keywords:
            if(keyword == item[64]):
                dic2017[keyword] += 1
    for item in rok2018:
        for keyword in keywords:
            if(keyword == item[64]):
                dic2018[keyword] += 1
    for item in rok2019:
        for keyword in keywords:
            if(keyword == item[64]):
                dic2019[keyword] += 1
    for item in rok2020:
        for keyword in keywords:
            if(keyword == item[64]):
                dic2020[keyword] += 1

    # Setřídím hodnoty podle velikosti, aby bylo podle největšího po největší
    sorted2016 = {k: v for k, v in sorted(dic2016.items(), key=lambda item: item[1],reverse=True)}
    sorted2017 = {k: v for k, v in sorted(dic2017.items(), key=lambda item: item[1],reverse=True)}
    sorted2018 = {k: v for k, v in sorted(dic2018.items(), key=lambda item: item[1],reverse=True)}
    sorted2019 = {k: v for k, v in sorted(dic2019.items(), key=lambda item: item[1],reverse=True)}
    sorted2020 = {k: v for k, v in sorted(dic2020.items(), key=lambda item: item[1],reverse=True)}

    # Vytvoření 5ti podgrafů
    fig, axs = plt.subplots(5)
    # Nadpis grafu
    fig.suptitle('Statistika nehodovosti')
    # Nastavení velikosti okna
    fig.set_figheight(8.2)
    fig.set_figwidth(6)

    # Definice pro jednotlivé podgrafu pro kraje
    axs[0].set_title("2016")
    axs[0].spines["top"].set_visible(False)
    axs[0].spines["right"].set_visible(False)
    # Vytvoření sloupce pro graf
    bar_plot =axs[0].bar(*zip(*sorted2016.items()))

    axs[1].set_title("2017")
    bar_plot1 = axs[1].bar(*zip(*sorted2017.items()))
    axs[1].spines["top"].set_visible(False)
    axs[1].spines["right"].set_visible(False)

    bar_plot2 = axs[2].bar(*zip(*sorted2018.items()))
    axs[2].spines["top"].set_visible(False)
    axs[2].spines["right"].set_visible(False)
    axs[2].set_title("2018")

    axs[3].set_title("2019")
    axs[3].spines["top"].set_visible(False)
    axs[3].spines["right"].set_visible(False)
    bar_plot3 = axs[3].bar(*zip(*sorted2019.items()))

    axs[4].set_title("2020")
    axs[4].spines["top"].set_visible(False)
    axs[4].spines["right"].set_visible(False)
    bar_plot4 = axs[4].bar(*zip(*sorted2020.items()))

    # Vykreslení hodnot na jednotlivými sloupci grafu
    for rect in bar_plot:
        height = rect.get_height()
        axs[0].text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')
    for rect in bar_plot1:
        height = rect.get_height()
        axs[1].text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')
    for rect in bar_plot2:
        height = rect.get_height()
        axs[2].text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')
    for rect in bar_plot3:
        height = rect.get_height()
        axs[3].text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')
    for rect in bar_plot4:
        height = rect.get_height()
        axs[4].text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')

    # Pomůže s odsazením jednotlivých grafů
    fig.tight_layout()

    # Pokud ho mám uložit ta kontroluji jestli složka existuje, jinak vytvořím a uložím
    if fig_location:
        if not os.path.exists(fig_location):
            os.makedirs(fig_location)
        plt.savefig(fig_location+'/IZV_nehodovost.png')


    # Pokud je zadán přepínač, vykreslí grafy na obrazovku
    if show_figure:
        plt.show()

# Pokud je skript spuštěn samostatně:
if __name__ == '__main__':

    # Parsování argumentů pomocí argparse viz. zadání
    parser = argparse.ArgumentParser()
    # Přidání argumentů
    parser.add_argument('--fig_location', help='Picture folder', required=False)
    parser.add_argument('--show_figure', required=False, action='store_true')
    args = parser.parse_args()
    picture_location = None
    show = False
    if args.fig_location:
        picture_location = args.fig_location
    if args.show_figure:
        show = True

    # Manuální volání get_list když je skript zavolán samostatně
    data_source = DataDownloader().get_list(["VYS", "JHM", "OLK", "HKK", "PLK"])
    plot_stat(data_source, picture_location, show)
