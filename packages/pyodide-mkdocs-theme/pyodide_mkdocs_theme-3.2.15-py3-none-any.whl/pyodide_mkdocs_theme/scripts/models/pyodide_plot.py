
import matplotlib
import matplotlib.pyplot as plt
from typing import Callable, Sequence


from unittest.mock import Mock
js = Mock()


class PyodidePlot:
    """
    Helper class, to draw figures from pyodide runtime, into a specified html element.
    If no argument is provided, the default `div_id` is used (arguments configuration of
    the plugin).

    ```python
    import matplotlib.pyplot as plt
    PyodidePlot().target()

    plt.plot(xs, ys, ...)
    plt.title("...")
    plt.show()
    ```

    ---

    In case you want to target more than one figure in the same page, pass the html id of the
    div tag to target to the `PyodidePlot` constructor:

    ```python
    fig1 = PyodidePlot("figure_id1")
    fig2 = PyodidePlot("figure_id2")

    fig1.target()       # Draw in "figure_id1"
    plt.plot(...)

    fig2.target()       # Draw in "figure_id2"
    plt.plot(...)
    ```

    ---
    """

    def __init__(self, div_id:str=''):
        self.div_id = div_id or js.config().argsFigureDivId

    def __getattr__(self, prop:str):
        return getattr(plt, prop)


    def target(self, keep_fig=False):
        """
        Close any previously created figure, then setup the current run to draw in
        the div tag targeted by the current instance.
        If keep_fig is set to True, the automatic `Figure N` will be kept, above the
        drawn figure.
        """
        for _ in plt.get_fignums():
            plt.close()
        div = js.document.getElementById(self.div_id)
        js.document.pyodideMplTarget = div
        div.textContent = ""
        if not keep_fig:
            plt.gcf().canvas.manager.set_window_title('')
        return plt

    refresh = target        # backward compatibility



    def plot_func(
        self,
        func:Callable,
        rng:Sequence,
        fmt:str=None,
        title:str=None,
        *,
        show:bool=True,
        keep_figure_num: bool = False,
        **kw
    ):
        """
        Draw an automatic graph for the given function on the given range, then "show"
        automatically the resulting graph in the correct figure element in the page.

        Arguments:
            func:  Callable, func(x) -> y
            rng:   Sequence of xs
            fmt:   Curve formatting (just like `pyplot.plot`)
            title: If given, will be added as title of the graph.
            show:  Call `pyplot.show()` only if `True`. This allows to customize the graph
                   before applying show manually.
            keep_figure_num: if False (by default), the `Figure N` above the drawing is
                   automatically removed.

        """
        self.target(keep_figure_num)

        xs = list(rng)
        ys = [*map(func, rng)]
        args = (xs,ys) if fmt is None else (xs,ys,fmt)
        out = plt.plot(*args, **kw)

        if title:
            plt.title(title)
        if show:
            plt.show()
        return out



    def plot(self, *args, keep_figure_num:bool=False, **kw):
        """
        Generic interface, strictly equivalent to `pyplot.plot`, except the `PyodidePlot`
        instance will automatically apply the drawing to the desired html element it is
        related to.

        _Use specifically this method to "plot"_ ! You then can rely on `pyplot` to finalize
        the figure as you prefer.
        """
        self.target(keep_figure_num)
        out = plt.plot(*args, **kw)
        return out


