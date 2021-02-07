#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np
import os
# muzeze pridat vlastni knihovny

""" Třetí část projektu do předmětu IZV 
    1/3 - geo.py - Vizualizace geografických dat
    Vypracoval: Ondřej Pavlacký - xpavla15 
    3BIT 2020/21  """


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""
    # Smazani dat, ktere mají NaN/inf
    try:
        df.dropna(subset=["d"], inplace=True)
        df.dropna(subset=["e"], inplace=True)
        # Reindexovani
        df.reindex()
        # Vraceni geopandas.GeoDataFrame viz. zadani
        return geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df["d"], df["e"]), crs="epsg:5514")
    except:
        print("Chyba ve vstupnim souboru!\n")
        exit(0)


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s dvemi podgrafy podle lokality nehody """
    gdf_new = gdf.set_geometry(gdf.centroid).to_crs("EPSG:3857")
    # Chci vykreslit 2 grafy
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 6))
    gdf1 = gdf_new
    gdf2 = gdf_new
    # Podminky pro nehody v obci a mino ve Zlinskem kraji
    ax1 = gdf1[(gdf_new["p5a"] == 1) & (gdf_new["region"] == "ZLK")].centroid.plot(ax=ax1, markersize=4,
                                                                                   color="red", alpha=0.8)
    ax2 = gdf2[(gdf_new["p5a"] == 2) & (gdf_new["region"] == "ZLK")].centroid.plot(ax=ax2, markersize=4,
                                                                                   color="green", alpha=0.8)
    # Pridani podkladovych map pro vykreslovani
    ctx.add_basemap(
        ax1,
        crs=gdf1.crs.to_string(),
        source=ctx.providers.Stamen.TonerLite,
    )
    ctx.add_basemap(
        ax2,
        crs=gdf2.crs.to_string(),
        source=ctx.providers.Stamen.TonerLite,
    )
    # Pridani titulku k podgrafum
    ax1.title.set_text('Nehody v ZLK kraji: v obci')
    ax2.title.set_text('Nehody v ZLK kraji: mimo obec')
    # Vypnuti bocnich os
    ax1.axis("off")
    ax2.axis("off")
    # Uložení obrázku podle podmínky, kotrola adresáře a při neexistujícím, vytvoření nového
    # Musím prvně ukládat, protože jinak se to neuloží
    if fig_location is not None:
        d = os.path.dirname(fig_location)
        # Viz časté chyby v první části
        if d and not os.path.isdir(d):
            os.makedirs(d)
        # Samotné uložení obrázku
        plt.savefig(fig_location)
    # Podmínka pro vykreslení grafu
    if show_figure:
        plt.show()


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """
    # Vytrideni zaznamu jenom ze Zlinskeho kraje
    gdf = gdf[(gdf["region"] == "ZLK")].set_geometry(gdf.centroid).to_crs("EPSG:5514")
    gdf = gdf.set_geometry(gdf.centroid).to_crs(epsg=3857)

    # Vytvoreni matice o rozmerech (X, 2)
    coords = np.dstack([gdf.geometry.x, gdf.geometry.y]).reshape(-1, 2)

    # Pouzijeme K-means, metodu uceni bez ucitele, pocet clusteru jsem zvolil 10 podle experimentu
    # Vysledne prirazeni je v atributu *labels_*
    model = sklearn.cluster.MiniBatchKMeans(n_clusters=10).fit(coords)

    # Vytvoreni kopie zaznamu
    gdf4 = gdf.copy()
    gdf4["cluster"] = model.labels_

    # Spojeni dohromady (funkce dissolve - geograficky ekvivalent groupby)
    # Udela se suma regionu, podle toho zjistim pocet nehod
    gdf4 = gdf4.dissolve(by="cluster", aggfunc={"region": "count"}).rename(columns={"region": "count"})

    # Urceni reprezentativnich bodu
    gdf_coords = geopandas.GeoDataFrame(
    geometry=geopandas.points_from_xy(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1]))
    gdf5 = gdf4.merge(gdf_coords, left_on="cluster", right_index=True).set_geometry("geometry_y")

    # Zobrazíme graf
    plt.figure(figsize=(15, 8))
    ax = plt.gca()

    # Vypnuti bocnich os
    ax.axis("off")

    # Vykresleni jednotlivych nehod
    gdf.plot(ax=ax, color="tab:grey", alpha=0.5, markersize=1)
    gdf5.plot(ax=ax, markersize=gdf4["count"] , column="count", legend=True,  alpha=0.4)
    ctx.add_basemap(ax, crs="epsg:3857", source=ctx.providers.Stamen.TonerLite, zoom=10, alpha=0.6)  ###

    # Uložení obrázku podle podmínky, kotrola adresáře a při neexistujícím, vytvoření nového
    # Musím prvně ukládat, protože jinak se to neuloží
    if fig_location is not None:
        d = os.path.dirname(fig_location)
        # Viz časté chyby v první části
        if d and not os.path.isdir(d):
            os.makedirs(d)
        # Samotné uložení obrázku
        plt.savefig(fig_location)
    # Podmínka pro vykreslení grafu
    if show_figure:
        plt.show()

if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)

