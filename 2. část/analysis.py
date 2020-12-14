#!/usr/bin/env python3.8
# coding=utf-8

"""
Projekt do předmětu IZV
2. část
Zpracoval: Ondřej Pavlacký (xpavla15)
"""

from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os
import pickle
import gzip

# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz

# Ukol 1: nacteni dat
def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:

    # Kontrola na existenci souboru
    if not os.path.isfile(filename):
        print("Soubor neexistuje")
        return 1
    # Otevření rar souboru
    with gzip.open(filename, 'rb') as f:
        # Pomocí pickle se vytáhnou data
        unpickle = pickle.load(f)

        # Získání dat z formátu pickle
        datas = pd.DataFrame(unpickle)
        if(verbose == True):
            # Výpis původního využití paměti (1MB = 1048576B) viz. zadání
            print("origin_size={:.1f} MB".format(datas.memory_usage(index=False, deep=True).sum() / 1048576))
        # Změny typů z obj. na int

        datas = datas[["p2b", "p2a", "p13a", "p13b", "p13c", "region", "p12"]]
        datas["p2b"] = datas["p2b"].astype("int8")
        datas["p13a"] = datas["p13a"].astype("int8")
        datas["p13b"] = datas["p13b"].astype("int8")
        datas["p13c"] = datas["p13c"].astype("int8")
        # datas.drop(columns=['p32'])
        # Přetypování na datum
        datas["p2a"] = pd.to_datetime(datas["p2a"], format='%Y-%m-%d')
        # Vytvoření nového sloupce dat viz. zadání
        datas["date"] = datas["p2a"]

        # Pokud je zadán výpis dat
        if (verbose == True):
            # Výpis nového (upraveného) využití paměti (1MB = 1048576B) viz. zadání
            print("new size={:.1f} MB".format(datas.memory_usage(index=False, deep=True).sum() / 1048576))
        return  datas

# Ukol 2: následky nehod v jednotlivých regionech
def plot_conseq(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    # Výběr pouze sloupců, které mě zajímají
    grouped = df[["p13a", "p13b", "p13c", "region"]].groupby(["region"], as_index=False)

    # Vytvoření vytříděných položek podle sloupců  (od největšího po nejmenší)
    p13a_sorted = grouped.sum().sort_values(by=["p13a"], ascending=False)
    p13b_sorted = grouped.sum().sort_values(by=["p13b"], ascending=False)
    p13c_sorted = grouped.sum().sort_values(by=["p13c"], ascending=False)
    total_count = df["region"].value_counts().rename_axis('unique_values').reset_index(name='counts')

    # Vytvoření osy pro vykreslování
    fig, axes = plt.subplots(4, 1, figsize=(8, 8))
    ax = axes.flatten()

    # Vytvoření titulku
    fig.suptitle('Úkol 2. - počty zranění/nehod', fontsize=20)
    # Použití barplotu podle specifikace v zadání = sloupcové grafy
    sns.barplot(data=p13a_sorted, x='region', y='p13a', ax=ax[0])
    ax[0].set_facecolor('#E6E6E6')
    ax[0].grid(linestyle='dashed')
    ax[0].set_axisbelow(True)
    ax[0].set(ylabel='Zemřeli při nehodě', xlabel='')
    sns.barplot(data=p13b_sorted, x='region', y='p13b', ax=ax[1])
    ax[1].set(ylabel='Těžce zranění', xlabel='')
    ax[1].set_facecolor('#E6E6E6')
    ax[1].grid(linestyle='dashed')
    ax[1].set_axisbelow(True)
    sns.barplot(data=p13c_sorted, x='region', y='p13c', ax=ax[2])
    ax[2].set(ylabel='Lehce zranění', xlabel='' )
    ax[2].set_facecolor('#E6E6E6')
    ax[2].grid(linestyle='dashed')
    ax[2].set_axisbelow(True)
    sns.barplot(data=total_count,x='unique_values', y='counts', ax=ax[3])
    ax[3].set(ylabel='Počet všech nehod', xlabel='')
    ax[3].set_facecolor('#E6E6E6')
    ax[3].grid(linestyle='dashed')
    ax[3].set_axisbelow(True)
    fig.tight_layout()


    # Uložení obrázku podle podmínky, kotrola adresáře a při neexistujícím, vytvoření nového
    # Musím prvně ukládat, protože jinak se to neuloží
    if(fig_location != None):
        d = os.path.dirname(fig_location)
        # Viz časté chyby v první části
        if d and not os.path.isdir(d):
            os.makedirs(d)
        # Samotné uložení obrázku
        plt.savefig(fig_location)
    # Podmínka pro vykreslení grafu
    if(show_figure == True):
        fig.show()



# Ukol3: příčina nehody a škoda
def plot_damage(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    grouped = df[["region", "p12"]].groupby(["region", "p12"], as_index=False)
    # yay = grouped.unstact(type="p12")
    print(grouped)

# Ukol 4: povrch vozovky
def plot_surface(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    pass


if __name__ == "__main__":
    # pass
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce.
    print("Jala Zohan\n")
    df = get_dataframe("accidents.pkl.gz", True)
    plot_conseq(df, fig_location="Fotky/04_nasledky.png", show_figure=True)
    plot_damage(df, "02_priciny.png", True)
    plot_surface(df, "03_stav.png", True)
