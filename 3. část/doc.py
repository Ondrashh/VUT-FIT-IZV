#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np
import seaborn as sns
import os

"""IZV - třetí část - doc.py
    Skript k třetí části projektu
    Vytvořil: Ondřej Pavlacký (xpavla15)
    3BIT 2020/21"""


# Vypocet a vykresleni procent nehod
def graf_alkohol_drogy_nehody(df: pd.DataFrame):
    df_alkohol_drogy = df[(df["p11"] != 0) & (df["p11"] != 2)]
    grouped_alkohol_drogy = df_alkohol_drogy[["p11", "region"]].groupby(["region"], as_index=False)
    grouped_vsichni = df[["p11", "region"]].groupby(["region"], as_index=False)
    vsechny_nehody = grouped_vsichni.count().sort_values(by=["p11"], ascending=False)
    alkohol_drogy_nehody = grouped_alkohol_drogy.count().sort_values(by=["p11"], ascending=False)

    # Vytvoření osy pro vykreslování
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    # Použití barplotu podle specifikace v zadání = sloupcové grafy
    sns.barplot(data=alkohol_drogy_nehody, x='region', y='p11', ax=ax)
    ax.set_facecolor('#E6E6E6')
    ax.grid(linestyle='dashed')
    ax.set_axisbelow(True)
    ax.set(ylabel='Zemřeli při nehodě', xlabel='')
    plt.savefig("fig.png")

    # Vypocet procentualni ucast STC
    pocet_celkem_STC = vsechny_nehody[vsechny_nehody["region"] == "STC"]["p11"]
    pocet_alkohol_drogy = alkohol_drogy_nehody[alkohol_drogy_nehody["region"] == "STC"]["p11"]
    podil_procent = (pocet_alkohol_drogy[10]/pocet_celkem_STC[10])*100
    print(f"Podil nehod v STC: {podil_procent}")

    # Vypocet procentualni ucast KVK
    pocet_celkem_KVK = vsechny_nehody[vsechny_nehody["region"] == "KVK"]["p11"]
    pocet_alkohol_drogy = alkohol_drogy_nehody[alkohol_drogy_nehody["region"] == "KVK"]["p11"]
    podil_procent = (pocet_alkohol_drogy[3] / pocet_celkem_KVK[3]) * 100
    print(f"Podil nehod v KVK: {podil_procent}\n")


def tabulka_alkohol_drogy_nehody(df: pd.DataFrame):
    df = df[["p11", "region"]]
    bez_alk = df[(df["p11"] == 2)]
    grouped = bez_alk.groupby(["region"], as_index=False)
    bez_alk_final = grouped.count().sort_values(by=["region"], ascending=False)
    alk_024 = df[(df["p11"] == 1)]
    grouped = alk_024.groupby(["region"], as_index=False)
    alk_024_final = grouped.count().sort_values(by=["region"], ascending=False)
    alk_05 = df[(df["p11"] == 3)]
    grouped = alk_05.groupby(["region"], as_index=False)
    alk_05_final = grouped.count().sort_values(by=["region"], ascending=False)
    alk_08 = df[(df["p11"] == 6)]
    grouped = alk_08.groupby(["region"], as_index=False)
    alk_08_final = grouped.count().sort_values(by=["region"], ascending=False)
    alk_10 = df[(df["p11"] == 7)]
    grouped = alk_10.groupby(["region"], as_index=False)
    alk_10_final = grouped.count().sort_values(by=["region"], ascending=False)
    alk_15 = df[(df["p11"] == 8)]
    grouped = alk_15.groupby(["region"], as_index=False)
    alk_15_final = grouped.count().sort_values(by=["region"], ascending=False)
    alk_inf = df[(df["p11"] == 9)]
    grouped = alk_inf.groupby(["region"], as_index=False)
    alk_inf_final = grouped.count().sort_values(by=["region"], ascending=False)
    drog = df[(df["p11"] == 4)]
    grouped = drog.groupby(["region"], as_index=False)
    drog_final = grouped.count().sort_values(by=["region"], ascending=False)
    drog_alk = df[(df["p11"] == 5)]
    grouped = drog_alk.groupby(["region"], as_index=False)
    drog_alk_final = grouped.count().sort_values(by=["region"], ascending=False)
    nezjistovano = df[(df["p11"] == 0)]
    grouped = nezjistovano.groupby(["region"], as_index=False)
    nezjistovano_final = grouped.count().sort_values(by=["region"], ascending=False)

    # Vypocet procenta ze vsech testovanych
    procento_pozitivnich = (22514/292465)
    #Vypocet osob, ktere by mohly byt pozitivni
    pocet_moznych_pozitivnich = 292465 * procento_pozitivnich
    print(f"Pocet moznych nalezu u netestovanych osob: {pocet_moznych_pozitivnich}")
    print("----------------TABULKA S HODNOTAMI----------------------\n"

          f"ZLK | {bez_alk_final[bez_alk_final['region'] == 'ZLK']['p11'][13]}  {alk_024_final[alk_024_final['region'] == 'ZLK']['p11'][13]}    {alk_05_final[alk_05_final['region'] == 'ZLK']['p11'][13]}  {alk_08_final[alk_08_final['region'] == 'ZLK']['p11'][13]}  {alk_10_final[alk_10_final['region'] == 'ZLK']['p11'][13]}  {alk_15_final[alk_15_final['region'] == 'ZLK']['p11'][13]}  {alk_inf_final[alk_15_final['region'] == 'ZLK']['p11'][13]}  {drog_final[drog_final['region'] == 'ZLK']['p11'][13]}  {drog_alk_final[drog_alk_final['region'] == 'ZLK']['p11'][13]}\n"
          f"VYS | {bez_alk_final[bez_alk_final['region'] == 'VYS']['p11'][12]}  {alk_024_final[alk_024_final['region'] == 'VYS']['p11'][12]}   {alk_05_final[alk_05_final['region'] == 'VYS']['p11'][12]}   {alk_08_final[alk_08_final['region'] == 'VYS']['p11'][12]}  {alk_10_final[alk_10_final['region'] == 'VYS']['p11'][12]}  {alk_15_final[alk_15_final['region'] == 'VYS']['p11'][12]}  {alk_inf_final[alk_15_final['region'] == 'VYS']['p11'][12]}  {drog_final[drog_final['region'] == 'VYS']['p11'][12]}  {drog_alk_final[drog_alk_final['region'] == 'VYS']['p11'][12]}\n"
          f"ULK | {bez_alk_final[bez_alk_final['region'] == 'ULK']['p11'][11]}  {alk_024_final[alk_024_final['region'] == 'ULK']['p11'][11]}   {alk_05_final[alk_05_final['region'] == 'ULK']['p11'][11]}   {alk_08_final[alk_08_final['region'] == 'ULK']['p11'][11]}  {alk_10_final[alk_10_final['region'] == 'ULK']['p11'][11]}  {alk_15_final[alk_15_final['region'] == 'ULK']['p11'][11]}  {alk_inf_final[alk_15_final['region'] == 'ULK']['p11'][11]}  {drog_final[drog_final['region'] == 'ULK']['p11'][11]}  {drog_alk_final[drog_alk_final['region'] == 'ULK']['p11'][11]}\n"
          f"STC | {bez_alk_final[bez_alk_final['region'] == 'STC']['p11'][10]}  {alk_024_final[alk_024_final['region'] == 'STC']['p11'][10]}   {alk_05_final[alk_05_final['region'] == 'STC']['p11'][10]}   {alk_08_final[alk_08_final['region'] == 'STC']['p11'][10]}  {alk_10_final[alk_10_final['region'] == 'STC']['p11'][10]}  {alk_15_final[alk_15_final['region'] == 'STC']['p11'][10]}  {alk_inf_final[alk_15_final['region'] == 'STC']['p11'][10]}  {drog_final[drog_final['region'] == 'STC']['p11'][10]}  {drog_alk_final[drog_alk_final['region'] == 'STC']['p11'][10]}\n"
          f"PLK | {bez_alk_final[bez_alk_final['region'] == 'PLK']['p11'][9]}   {alk_024_final[alk_024_final['region'] == 'PLK']['p11'][9]}  {alk_05_final[alk_05_final['region'] == 'PLK']['p11'][9]}   {alk_08_final[alk_08_final['region'] == 'PLK']['p11'][9]}  {alk_10_final[alk_10_final['region'] == 'PLK']['p11'][9]}   {alk_15_final[alk_15_final['region'] == 'PLK']['p11'][9]}   {alk_inf_final[alk_15_final['region'] == 'PLK']['p11'][9]}   {drog_final[drog_final['region'] == 'PLK']['p11'][9]}   {drog_alk_final[drog_alk_final['region'] == 'PLK']['p11'][9]}\n"
          f"PHA | {bez_alk_final[bez_alk_final['region'] == 'PHA']['p11'][8]}   {alk_024_final[alk_024_final['region'] == 'PHA']['p11'][8]}  {alk_05_final[alk_05_final['region'] == 'PHA']['p11'][8]}   {alk_08_final[alk_08_final['region'] == 'PHA']['p11'][8]}  {alk_10_final[alk_10_final['region'] == 'PHA']['p11'][8]}   {alk_15_final[alk_15_final['region'] == 'PHA']['p11'][8]}   {alk_inf_final[alk_15_final['region'] == 'PHA']['p11'][8]}   {drog_final[drog_final['region'] == 'PHA']['p11'][8]}   {drog_alk_final[drog_alk_final['region'] == 'PHA']['p11'][8]}\n"
          f"PAK | {bez_alk_final[bez_alk_final['region'] == 'PAK']['p11'][7]}   {alk_024_final[alk_024_final['region'] == 'PAK']['p11'][7]}  {alk_05_final[alk_05_final['region'] == 'PAK']['p11'][7]}   {alk_08_final[alk_08_final['region'] == 'PAK']['p11'][7]}  {alk_10_final[alk_10_final['region'] == 'PAK']['p11'][7]}   {alk_15_final[alk_15_final['region'] == 'PAK']['p11'][7]}   {alk_inf_final[alk_15_final['region'] == 'PAK']['p11'][7]}   {drog_final[drog_final['region'] == 'PAK']['p11'][7]}   {drog_alk_final[drog_alk_final['region'] == 'PAK']['p11'][7]}\n"
          f"OLK | {bez_alk_final[bez_alk_final['region'] == 'OLK']['p11'][6]}   {alk_024_final[alk_024_final['region'] == 'OLK']['p11'][6]}  {alk_05_final[alk_05_final['region'] == 'OLK']['p11'][6]}   {alk_08_final[alk_08_final['region'] == 'OLK']['p11'][6]}  {alk_10_final[alk_10_final['region'] == 'OLK']['p11'][6]}   {alk_15_final[alk_15_final['region'] == 'OLK']['p11'][6]}   {alk_inf_final[alk_15_final['region'] == 'OLK']['p11'][6]}   {drog_final[drog_final['region'] == 'OLK']['p11'][6]}   {drog_alk_final[drog_alk_final['region'] == 'OLK']['p11'][6]}\n"
          f"MSK | {bez_alk_final[bez_alk_final['region'] == 'MSK']['p11'][5]}   {alk_024_final[alk_024_final['region'] == 'MSK']['p11'][5]}  {alk_05_final[alk_05_final['region'] == 'MSK']['p11'][5]}   {alk_08_final[alk_08_final['region'] == 'MSK']['p11'][5]}  {alk_10_final[alk_10_final['region'] == 'MSK']['p11'][5]}   {alk_15_final[alk_15_final['region'] == 'MSK']['p11'][5]}   {alk_inf_final[alk_15_final['region'] == 'MSK']['p11'][5]}   {drog_final[drog_final['region'] == 'MSK']['p11'][5]}   {drog_alk_final[drog_alk_final['region'] == 'MSK']['p11'][5]}\n"
          f"LBK | {bez_alk_final[bez_alk_final['region'] == 'LBK']['p11'][4]}   {alk_024_final[alk_024_final['region'] == 'LBK']['p11'][4]}  {alk_05_final[alk_05_final['region'] == 'LBK']['p11'][4]}   {alk_08_final[alk_08_final['region'] == 'LBK']['p11'][4]}  {alk_10_final[alk_10_final['region'] == 'LBK']['p11'][4]}   {alk_15_final[alk_15_final['region'] == 'LBK']['p11'][4]}   {alk_inf_final[alk_15_final['region'] == 'LBK']['p11'][4]}   {drog_final[drog_final['region'] == 'LBK']['p11'][4]}   {drog_alk_final[drog_alk_final['region'] == 'LBK']['p11'][4]}\n"
          f"KVK | {bez_alk_final[bez_alk_final['region'] == 'KVK']['p11'][3]}   {alk_024_final[alk_024_final['region'] == 'KVK']['p11'][3]}  {alk_05_final[alk_05_final['region'] == 'KVK']['p11'][3]}   {alk_08_final[alk_08_final['region'] == 'KVK']['p11'][3]}  {alk_10_final[alk_10_final['region'] == 'KVK']['p11'][3]}   {alk_15_final[alk_15_final['region'] == 'KVK']['p11'][3]}   {alk_inf_final[alk_15_final['region'] == 'KVK']['p11'][3]}   {drog_final[drog_final['region'] == 'KVK']['p11'][3]}   {drog_alk_final[drog_alk_final['region'] == 'KVK']['p11'][3]}\n"
          f"JHM | {bez_alk_final[bez_alk_final['region'] == 'JHM']['p11'][2]}   {alk_024_final[alk_024_final['region'] == 'JHM']['p11'][2]}  {alk_05_final[alk_05_final['region'] == 'JHM']['p11'][2]}   {alk_08_final[alk_08_final['region'] == 'JHM']['p11'][2]}  {alk_10_final[alk_10_final['region'] == 'JHM']['p11'][2]}   {alk_15_final[alk_15_final['region'] == 'JHM']['p11'][2]}   {alk_inf_final[alk_15_final['region'] == 'JHM']['p11'][2]}   {drog_final[drog_final['region'] == 'JHM']['p11'][2]}   {drog_alk_final[drog_alk_final['region'] == 'JHM']['p11'][2]}\n"
          f"JHC | {bez_alk_final[bez_alk_final['region'] == 'JHC']['p11'][1]}   {alk_024_final[alk_024_final['region'] == 'JHC']['p11'][1]}  {alk_05_final[alk_05_final['region'] == 'JHC']['p11'][1]}   {alk_08_final[alk_08_final['region'] == 'JHC']['p11'][1]}  {alk_10_final[alk_10_final['region'] == 'JHC']['p11'][1]}   {alk_15_final[alk_15_final['region'] == 'JHC']['p11'][1]}   {alk_inf_final[alk_15_final['region'] == 'JHC']['p11'][1]}   {drog_final[drog_final['region'] == 'JHC']['p11'][1]}   {drog_alk_final[drog_alk_final['region'] == 'JHC']['p11'][1]}\n"
          f"HKK | {bez_alk_final[bez_alk_final['region'] == 'HKK']['p11'][0]}   {alk_024_final[alk_024_final['region'] == 'HKK']['p11'][0]}  {alk_05_final[alk_05_final['region'] == 'HKK']['p11'][0]}   {alk_08_final[alk_08_final['region'] == 'HKK']['p11'][0]}  {alk_10_final[alk_10_final['region'] == 'HKK']['p11'][0]}   {alk_15_final[alk_15_final['region'] == 'HKK']['p11'][0]}   {alk_inf_final[alk_15_final['region'] == 'HKK']['p11'][0]}   {drog_final[drog_final['region'] == 'HKK']['p11'][0]}   {drog_alk_final[drog_alk_final['region'] == 'HKK']['p11'][0]}\n")


if __name__ == '__main__':
    # Nacteni souboru
    df = pd.read_pickle("accidents.pkl.gz")
    graf_alkohol_drogy_nehody(df)
    tabulka_alkohol_drogy_nehody(df)
