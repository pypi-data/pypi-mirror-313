import os
import webbrowser
from pathlib import Path
from typing import Optional, Union

import dominate
import dominate.tags as dt
import dominate.util as du
import markdown
from dominate.tags import dom_tag
from pandas import DataFrame
from pandas.io.formats.style import Styler
from plotly.graph_objects import Figure

from htmlreport.javascript import _get_plotly_resize_script
from htmlreport.share import (
    _add_header,
    _add_pandas_dataframe,
    _add_pandas_styler,
    _add_plotly_figure,
)
from htmlreport.tabby import Tabby


class HTMLReport:
    def __init__(
        self,
        title: str = "HTMLReport",
        doc_type: str = "<!DOCTYPE html>",
        default_section_width: str = "80%",
        default_header_size: int = 3,
    ):
        """
        Object used to report data analyses.

        :param title: Value of report's HTML title tag (the name of the tab when open in browser). Parsed to \
        dominate.document constructor.
        :param doc_type: See behaviour when parsed to dominate.document constructor if user wishes to change from \
        default.
        :param default_section_width: Default width of new sections. Advised to parse width as a percentage \
        (e.g. '80%') of the containing block. See documentation on CSS width property for range of values that can be \
        parsed.
        :param default_header_size: Default size of headers added to report - between 1 (largest) and 6 (smallest). \
        Determines the HTML tag used.
        """
        self.document = dominate.document(title=title, doctype=doc_type)
        self.plotly_activated = False
        self.tabby_activated = False
        self.section = {}
        self.default_section_width = default_section_width
        self.default_header_size = default_header_size
        with open(Path(__file__).parent / "css/report.css") as css:
            self.document.head.add(dt.style(css.read()))

    def _handle_section(self, sec: Optional[str]) -> Union[dt.div, dominate.document]:
        if sec:
            try:
                return self.section[sec]["div"]
            except KeyError:
                raise RuntimeError(f"section with id '{sec}' not created")
        return self.document

    def _activate_plotly(self) -> None:
        self.plotly_activated = True
        self.document.head.add(
            dt.script(src="https://cdn.plot.ly/plotly-latest.min.js")
        )

    def _activate_tabby(self) -> None:
        self.tabby_activated = True
        self.document.head.add(
            dt.link(
                rel="stylesheet",
                href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
                integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
                crossorigin="anonymous",
            )
        )
        self.document.head.add(
            dt.script(
                src="https://code.jquery.com/jquery-3.3.1.slim.min.js",
                integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
                crossorigin="anonymous",
            )
        )
        self.document.head.add(
            dt.script(
                src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js",
                integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM",
                crossorigin="anonymous",
            )
        )
        with open(Path(__file__).parent / "css/tabby.css") as css:
            self.document.head.add(dt.style(css.read()))

    def add_section(self, id: str, width: Optional[str] = None) -> None:
        """
        Add a section to the report to allow grouping of analyses.

        :param id: Identifier of section.
        :param width: Width of section. Advised to parse width as a percentage (e.g. '80%') of the containing block. \
        See documentation on CSS width property for range of values that can be parsed.
        :return: None
        """
        if width is None:
            width = self.default_section_width
        new_sec = self.document.add(dt.div(cls="hr-section", style=f"width: {width}"))
        self.section[id] = {
            "div": new_sec,
        }

    def add(
        self,
        obj: Union[Tabby, dom_tag, DataFrame, Styler, Figure],
        sec: Optional[str] = None,
    ) -> None:
        """
        Add instance of pandas DataFrame, pandas Styler, plotly Figure or Tabby to report. Can add instance of \
        dominate dom_tag if user wishes to interact with dominate package.

        :param obj: Object to add.
        :param sec: Identifier of the section to add the object to. If not parsed, content added to main report body.

        :return: None
        """
        to_add = self._handle_section(sec=sec)
        if isinstance(obj, Tabby):
            if not self.tabby_activated:
                self._activate_tabby()
            if obj.plotly and not self.plotly_activated:
                self._activate_plotly()
            to_add.add(obj.to_dom_tag())
        elif isinstance(obj, dom_tag):
            to_add.add(obj)
        elif isinstance(obj, DataFrame):
            to_add.add(du.raw(_add_pandas_dataframe(obj=obj)))
        elif isinstance(obj, Styler):
            to_add.add(du.raw(_add_pandas_styler(obj=obj)))
        elif isinstance(obj, Figure):
            if not self.plotly_activated:
                self._activate_plotly()
            to_add.add(du.raw(_add_plotly_figure(plot=obj)))
        else:
            raise TypeError(
                "obj must be an instance of pandas.DataFrame, pandas.io.formats.style.Styler, plotly.Figure, "
                "dominate.tags.dom_tag or htmlreport.Tabby"
            )

    def add_header(
        self, content: str, size: Optional[int] = None, sec: Optional[str] = None
    ) -> None:
        """
        Add a header to report using HTML heading tag.

        :param content: Text to be displayed.
        :param size: Size of the header - between 1 (largest) and 6 (smallest). Determines the HTML tag used. Defaults \
        to value of property default_header_size.
        :param sec: Identifier of the section to add the header to. If not parsed, content added to main report body.

        :return: None
        """
        if size is None:
            size = self.default_header_size
        to_add = self._handle_section(sec=sec)
        to_add.add(_add_header(size=size, content=content))

    def add_para(self, content: str, sec: Optional[str] = None) -> None:
        """
        Add a paragraph to report using HTML <p> tag.

        :param content: Text to be displayed.
        :param sec: Identifier of the section to add the paragraph to. If not parsed, content added to main report body.

        :return: None
        """
        to_add = self._handle_section(sec=sec)
        to_add.add(dt.p(content))

    def add_markdown(self, content: str, sec: Optional[str] = None) -> None:
        """
        Add content to report using markdown style input. Uses markdown package to render HTML from input.

        :param content: Markdown content to render to HTML.
        :param sec: Identifier of the section to add the content to. If not parsed, content added to main report body.

        :return: None
        """
        to_add = self._handle_section(sec=sec)
        to_add.add(du.raw(markdown.markdown(content, output_format="html5")))

    def to_html(self) -> str:
        """
        Get HTML representation of report.

        :return: str
        """
        if self.plotly_activated:
            self.document.add(du.raw(_get_plotly_resize_script()))
        return self.document.render()

    def save(
        self,
        filepath: Union[str, Path] = "unnamed_report.html",
        open_browser: bool = True,
    ) -> None:
        """
        Save report as a HTML file and optionally open in browser on save.

        :param filepath: Location to save report in.
        :param open_browser: If True, automatically open in browser on save.
        :return: None
        """
        if isinstance(filepath, str):
            filepath = Path(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_html())
        if open_browser:
            webbrowser.open("file://" + os.path.realpath(filepath))
