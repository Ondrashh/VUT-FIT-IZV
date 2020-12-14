#!/usr/bin/env python3.8
# coding=utf-8

"""
Projekt do předmětu IZV
2. část
Zpracoval: Ondřej Pavlacký (xpavla15)"""

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
def get_dataframe(filename: str, verbose: bool = True) -> pd.DataFrame:
    # Kontrola na existenci souboru
    if not os.path.isfile(filename):
        print("Soubor neexistuje")
    with gzip.open(filename, 'rb') as f:
        # Pomocí pickle se vytáhnou data
        unpickle = pickle.load(f)
        kokos = ["dasd", "dasdasd"]
        datas = pd.DataFrame(unpickle)
        # print("origin_size={:.1f} MB".format(datas.memory_usage(index=False, deep=True).sum() / 1048576))
        datas["p36"] = datas["p36"].astype("int")
        datas["p36"] = datas["p36"].astype("int8")
        datas["p2b"] = datas["p2b"].astype("int8")
        datas["p6"] = datas["p6"].astype("int8")
        datas["p13a"] = datas["p13a"].astype("int8")
        datas["p13b"] = datas["p13b"].astype("int8")
        # datas["p37"] = datas["p37"].astype("int")
        datas.drop(columns=['p2b'])
        datas["p2a"] = pd.to_datetime(datas["p2a"], format='%Y-%m-%d')
        datas["date"] = datas["p2a"]
        # print("new size={:.1f} MB".format(datas.memory_usage(index=False, deep=True).sum() / 1048576))
        datas_new = 0
        return  datas


# Ukol 2: následky nehod v jednotlivých regionech
def plot_conseq(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    # Výběr pouze sloupců, které mě zajímají
    grouped = df[["p13a", "p13b", "p13c", "region"]].groupby(["region"], as_index=False)
    p13a_sorted = grouped.sum().sort_values(by=["p13a"], ascending=False)
    p13b_sorted = grouped.sum().sort_values(by=["p13b"], ascending=False)
    p13c_sorted = grouped.sum().sort_values(by=["p13c"], ascending=False)
    #bruda = np.sum(grouped[["p13a", "p13b", "p13c"]])
    grouped1 = df["region"].value_counts().rename_axis('unique_values').reset_index(name='counts')
    print(grouped1)
    print(grouped1._internal_names)
    fig, axes = plt.subplots(4, 1, figsize=(8, 8))
    ax = axes.flatten()
    fig.suptitle('Úkol 2. - počty zranění/nehod', fontsize=20)
    sns.barplot(data=p13a_sorted, x='region', y='p13a', ax=ax[0])
    ax[0].set(ylabel='Zemřeli při nehodě',)
    sns.barplot(data=p13b_sorted, x='region', y='p13b', ax=ax[1])
    ax[1].set(ylabel='Těžce zranění')
    sns.barplot(data=p13c_sorted, x='region', y='p13c', ax=ax[2])
    ax[2].set(ylabel='Lehce zranění')
    sns.barplot(data=grouped1,x='unique_values', y='counts', ax=ax[3])
    fig.tight_layout()
    fig.show()
    print("Hello")

# Ukol3: příčina nehody a škoda
def plot_damage(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    pass


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
    df = get_dataframe("accidents.pkl.gz")
    plot_conseq(df, fig_location="01_nasledky.png", show_figure=True)
    plot_damage(df, "02_priciny.png", True)
    plot_surface(df, "03_stav.png", True)
