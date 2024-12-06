import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


class SimplesMatLib:
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

    def stackplot(
        self,
        categorias,
        data,
        loc="upper right",
        titulo='Stackplot',
        eixo_x='Eixo X',
        eixo_y='Eixo Y',
        alpha=0.8,
        tick_interval=5,
        legend_fontsize=9.5,
        titulo_fontsize=12,
        eixo_x_fontsize=10,
        eixo_y_fontsize=10
    ):
        """
        Cria um gráfico de stackplot a partir de um dicionário de dados.
        :param categorias: Categorias do gráfico.
        :param data: Dicionário com os dados a serem plotados.
        :param loc: Localização da legenda.
        :param titulo: Título do gráfico.
        :param eixo_x: Rótulo do eixo x.
        :param eixo_y: Rótulo do eixo y.
        :param alpha: Transparência das barras.
        :param tick_interval: Intervalo dos ticks.
        :param legend_fontsize: Tamanho da fonte da legenda.
        :param titulo_fontsize: Tamanho da fonte do título.
        :param eixo_x_fontsize: Tamanho da fonte do eixo x.
        :param eixo_y_fontsize: Tamanho da fonte do eixo y.
        """
        fig, ax = plt.subplots()
        ax.stackplot(
            categorias,
            data.values(),
            labels=data.keys(),
            alpha=alpha
        )
        ax.legend(loc=loc, reverse=False, fontsize=legend_fontsize)
        ax.set_title(titulo, fontsize=titulo_fontsize)
        ax.set_xlabel(eixo_x, fontsize=eixo_x_fontsize)
        ax.set_ylabel(eixo_y, fontsize=eixo_y_fontsize)
        ax.yaxis.set_minor_locator(mticker.MultipleLocator(tick_interval))

        plt.show()
