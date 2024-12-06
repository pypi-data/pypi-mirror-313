import uuid
from collections import defaultdict
from typing import Any, List, Optional, Union

import dominate.tags as dt
import dominate.util as du
import markdown
from dominate.tags import dom_tag
from matplotlib.pyplot import Figure as MatplotlibFigure
from pandas import DataFrame
from pandas.io.formats.style import Styler
from plotly.graph_objects import Figure as PlotlyFigure

from htmlreport.share import (
    _add_header,
    _add_matplotlib_figure,
    _add_pandas_dataframe,
    _add_pandas_styler,
    _add_plotly_figure,
)


class Tabby:
    def __init__(
        self, keys: Optional[List[Any]] = None, uid: Optional[str] = None
    ) -> None:
        """
        Object used to display data analyses in separate tabs.

        :param keys: Used to define keys of object before adding content. Useful if specific order of keys is desired. \
        Keys will be in order content is added to them if not parsed. Each key will be calculated as str(key), hence, \
        it is recommended to parse a list containing strings.
        :param uid: Enables pre-defined value of the object's HTML id attribute after rendering. Random id used if not \
        parsed.
        """
        self.id = uuid.uuid4() if uid is None else uid
        self.plotly = False
        if keys is None:
            self.data = defaultdict(list)
        else:
            self.data = defaultdict(list, {str(k): [] for k in keys})

    @staticmethod
    def _remove_keyword_from_key(to_handle: str) -> str:
        return to_handle.replace(".", "-")

    def add(
        self,
        key: Any,
        obj: Union[dom_tag, DataFrame, Styler, PlotlyFigure, MatplotlibFigure],
    ) -> None:
        """
        Add instance of pandas DataFrame, pandas Styler or plotly Figure to tab. Can add instance of dominate dom_tag \
        if user wishes to interact with dominate package.

        :param key: Key of tab to add content to. Key will be calculated as str(key), hence, it is recommended to \
        parse a string to method.
        :param obj: Object to add.
        :return: None
        """
        key = str(key)

        if isinstance(obj, DataFrame):
            self.data[key].append(du.raw(_add_pandas_dataframe(obj=obj)))
        elif isinstance(obj, Styler):
            self.data[key].append(du.raw(_add_pandas_styler(obj=obj)))
        elif isinstance(obj, PlotlyFigure):
            self.plotly = True
            self.data[key].append(du.raw(_add_plotly_figure(plot=obj)))
        elif isinstance(obj, MatplotlibFigure):
            self.data[key].append(du.raw(_add_matplotlib_figure(plot=obj)))
        elif isinstance(obj, dt.dom_tag):
            self.data[key].append(obj)
        else:
            raise TypeError(
                "obj must be an instance of pandas.DataFrame, "
                "pandas.io.formats.style.Styler, plotly.Figure, "
                "matplotlib.pyplot.Figure, or dominate.tags.dom_tag"
            )

    def add_para(self, key: Any, content: str) -> None:
        """
        Add a paragraph to tab using HTML <p> tag.

        :param key: Key of tab to add content to. Key will be calculated as str(key), hence, it is recommended to \
        parse a string to method.
        :param content: Text to be displayed.
        :return: None
        """
        key = str(key)
        self.data[key].append(dt.p(content))

    def add_header(self, key: Any, content: str, size: int = 1) -> None:
        """
        Add a header to tab using HTML heading tag.

        :param key: Key of tab to add content to. Key will be calculated as str(key), hence, it is recommended to \
        parse a string to method.
        :param content: Text to be displayed.
        :param size: Size of the header - between 1 (largest) and 6 (smallest). Determines the HTML tag used. Defaults \
        to 1.
        :return: None
        """
        key = str(key)
        self.data[key].append(_add_header(size=size, content=content))

    def add_markdown(self, key: Any, content: str) -> None:
        """
        Add content to tab using markdown style input. Uses markdown package to render HTML from input.

        :param key: Key of tab to add content to. Key will be calculated as str(key), hence, it is recommended to \
        parse a string to method.
        :param content: Markdown content to render to HTML.
        :return: None
        """
        key = str(key)
        self.data[key].append(du.raw(markdown.markdown(content, output_format="html5")))

    def keys(self) -> List[str]:
        """
        Get keys of object.

        :return: List[str]
        """
        return list(self.data)

    def _nav_bar_to_dom_tag(self) -> dt.div:
        nav_parent = dt.nav().add(
            dt.div(
                cls="nav nav-tabs nav-fill", id=f"tabby-{self.id}-nav", role="tablist"
            )
        )
        for key in self.data:
            key_wout_keyword = Tabby._remove_keyword_from_key(to_handle=key)
            key_concat = key_wout_keyword.lower().replace(" ", "-")
            nav_parent.add(
                dt.a(
                    key,
                    id=self._create_html_id(key=key_concat, is_nav=True),
                    cls="nav-item nav-link",
                    role="tab",
                    aria_controls=self._create_html_id(key=key_concat, is_nav=False),
                    href=f"#{self._create_html_id(key=key_concat, is_nav=False)}",
                    data_toggle="tab",
                    aria_selected="false",
                )
            )
        nav_parent[0]["class"] = nav_parent[0]["class"] + " active"
        nav_parent[0]["aria-selected"] = "true"

        return nav_parent

    def _content_to_dom_tag(self) -> dt.div:
        content_parent = dt.div(cls="tab-content", id=f"tabby-{self.id}-con")
        for key, outputs in self.data.items():
            key_wout_keyword = Tabby._remove_keyword_from_key(to_handle=key)
            key_concat = key_wout_keyword.lower().replace(" ", "-")
            content_child = content_parent.add(
                dt.div(
                    id=self._create_html_id(key=key_concat, is_nav=False),
                    cls="tab-pane fade show",
                    role="tabpanel",
                    aria_labelledby=self._create_html_id(key=key_concat, is_nav=True),
                )
            )

            for output in outputs:
                content_child.add(dt.div(output))
        content_parent[0]["class"] = content_parent[0]["class"] + " active"

        return content_parent

    def to_dom_tag(self) -> dt.div:
        """
        Get full content of object (nav bar and tabbed content).

        :return: dominate.tags.div
        """
        parent_div = dt.div(id=f"tabby-{self.id}-sec", cls="project-tab")
        child_div = (
            parent_div.add(dt.div(cls="container-fluid"))
            .add(dt.div(cls="row"))
            .add(dt.div(cls="col-md-12"))
        )
        child_div.add(self._nav_bar_to_dom_tag())
        child_div.add(self._content_to_dom_tag())

        return parent_div

    def to_html(self) -> str:
        """
        Get HTML representation of object.

        :return: str
        """
        return self.to_dom_tag().render()

    def _create_html_id(self, key: str, is_nav: bool) -> str:
        """
        Provides consistent method of producing raw HTML ids for the <div> and <a> tags that respectively produce
        the nav bar and tabbed content.
        """
        return f"tabby-{self.id}-{'nav' if is_nav else 'content'}-{key}"
