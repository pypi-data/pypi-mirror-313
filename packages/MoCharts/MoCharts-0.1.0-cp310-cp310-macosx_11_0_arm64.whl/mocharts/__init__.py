from .plot.plots.scatterplot import scatterplot
from .plot.plots.lineplot import lineplot
from .plot.plots.barplot import barplot
from .plot.plots.boxplot import boxplot
from .plot.plots.heatmapplot import heatmap
from .plot.plots.histogramplot import histplot
from .plot.plots.kdeplot import kdeplot
from .plot.plots.kde2Dplot import kde2Dplot
from .plot.plots.radarplot import radarplot
from .plot.plots.graphplot import graphplot
from .plot.plots.treeplot import treeplot
from .plot.plots.barstemplot import barstemplot
from .plot.plots.parallelplot import parallel
from .plot.plots.scatter3Dplot import scatter3Dplot
from .plot.plots.surface3Dplot import surface3Dplot
from .plot.plots.wordcloud import wordcloud
from .plot.plots.text import text
from .plot.other_widget import colored_text

from .plot.combination_plots.ridgeplot import ridgeplot
# from .plot.combination_plots.kde2Dplot import kde2Dplot

from .plot.result import Figure, SubPlots
from .plot import template
from .render.local_server.utils import add_share_data
from .render.jupyter.renderer import connect_server
from .render.utils import mochart_plot, mochart_save

def render_init():
    """Init empty mocharts figure
    """
    fig =Figure(figsize=(0,0))
    fig.show()

__all__ = ["SubPlots", "scatterplot", "lineplot", "barplot", "boxplot", "Figure",
           "heatmap", "histplot", "kdeplot", "graphplot", "treeplot", "barstemplot", "parallel",
           "scatter3Dplot", "radarplot", "add_share_data", "wordcloud", "text", "connect_server",
           "colored_text", "template", "mochart_plot", "surface3Dplot", "render_init",
           "ridgeplot", "kde2Dplot", "mochart_save"]
