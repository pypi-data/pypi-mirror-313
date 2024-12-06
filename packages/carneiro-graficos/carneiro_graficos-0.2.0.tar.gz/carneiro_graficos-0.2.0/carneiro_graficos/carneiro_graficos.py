import matplotlib.pyplot as plt
import numpy as np


class CarneiroGraficos:
    def bar(self, data, bar_labels, bar_colors, loc="upper right", title="", ylabel="", xlabel=""):
        """
        Cria um gráfico de barras a partir de um dicionário de dados.
        :param data: Dicionário com os dados a serem plotados.
        :param bar_labels: Rótulos das barras.
        :param bar_colors: Cores das barras.
        :param loc: Localização da legenda.
        :param title: Título do gráfico.
        :param ylabel: Rótulo do eixo y.
        :param xlabel: Rótulo do eixo x.
        """

        fig, ax = plt.subplots()
        bar_container = ax.bar(
            data.keys(),
            data.values(),
            edgecolor="black",
            linewidth=0.5,
            width=0.9,
            label=bar_labels,
            color=bar_colors
        )
        ax.bar_label(bar_container, fmt='{:,.0f}')
        ax.legend(title="", loc=loc)
        ax.set(title="Commits na Anton.IA", xlabel=xlabel, ylabel=xlabel)
        plt.show()

    def pie(self, data, color="Blues", title="", title_size=12):
        """
        Cria um gráfico de pizza a partir de um dicionário de dados.
        :param data: Dicionário com os dados a serem plotados.
        :param color: Cor do gráfico. Ex: "Blues", "Greens", "Reds", "Oranges".
        :param title: Título do gráfico.
        :param title_size: Tamanho do título.
        """
        colors = plt.get_cmap(color)(np.linspace(0.2, 0.7, len(data)))

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(
            data.values(),
            labels=data.keys(),
            colors=colors,
            autopct='%1.1f%%',
            shadow={'ox': -0.07, 'edgecolor': 'none', 'shade': 0.9},
            startangle=90,
            explode=(0.06, 0.06, 0.06, 0.3),
            radius=3,
            center=(4, 4),
            textprops={'size': 'smaller'},
            wedgeprops={
                "linewidth": 0.3,
                "edgecolor": "black"
            },
            frame=True
        )
        ax.set_title(title, fontsize=title_size)
        ax.set(xlim=(0, 8), xticks=np.arange(1, 8), ylim=(0, 8), yticks=np.arange(1, 8))
        plt.show()
