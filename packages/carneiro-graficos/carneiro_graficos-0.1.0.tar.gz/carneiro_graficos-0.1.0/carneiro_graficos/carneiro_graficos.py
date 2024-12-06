import matplotlib.pyplot as plt


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
