import requests
import os
import csv
import pickle
import gzip
from bs4 import BeautifulSoup
from enum import Enum
from zipfile import ZipFile
from io import TextIOWrapper
import numpy as np

from IZV.IZV.download import DataDownloader


def plot_stat(data_source, fig_location = None, show_figure = False):
    print(data_source[1])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data_source = DataDownloader().get_list(["VYS","JHM"])
    plot_stat(data_source)
