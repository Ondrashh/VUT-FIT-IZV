# Projekt do předmětu IZV, První část
# Zpracoval: Ondřej Pavlacký (xpavla15) 3BIT
# Implementace modulu get_stat.py
# Vytvořeno: 11.11.2020
# VUT FIT

import matplotlib.pyplot as plt

from IZV.IZV.download import DataDownloader


def plot_stat(data_source, fig_location = None, show_figure = False):
    # data_source = DataDownloader().get_list(["VYS", "JHM"])
    # print(type(data_source[1][0][0]))
    for zaznam in data_source[1]:
        
    fig = plt.figure(figsize=(8, 4))
    ax1 = fig.add_axes((0.1, 0.1, 0.8, 0.8))
    ax2 = fig.add_axes((0.6, 0.6, 0.25, 0.25))
    ax1.plot([0, 1], [1, 0], color='C3')
    ax2.plot([0, 1], [0, 1], color='#35495e')
    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data_source = DataDownloader().get_list(["VYS", "JHM", "OLK"])
    plot_stat(data_source)
