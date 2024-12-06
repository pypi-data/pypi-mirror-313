# html-report

Jump to [quickstart](#quickstart) or [example report](#usage-example).

## Description

### What is it?

A simple package that empowers data enthusiasts to quickly produce interactive HTML reports, containing tables produced with [*pandas*](https://github.com/pandas-dev/pandas) and plots produced with [*plotly*](https://github.com/plotly/plotly.py). The package takes care of the grunt work, thereby allowing you to focus your time on what matters: exploring your data.

### Main features

The main features of the package are as follows:

* Summarise your data analysis by outputting interactive HTML reports containing tables and plots. 
* Complete abstraction of HTML and CSS syntax is achieved by wrapping [*dominate*](https://github.com/Knio/dominate).
* Isolate related results from the remainder of the report using section functionality of the package's `HTMLReport` class. See use of section functionality in [example report](#usage-example).
* Separate related results onto different tabs using the package's `Tabby` class. See use of Tabby in [example report](#usage-example).

### Project vision and status

Future development will have two aims:

1. Improve ability to draw and share value from data, and
2. Improve automatic visual appearance of reports.

Development will prioritise (1), since the aim of the project is to speed up the journey from analysis to reporting (rather than facilitate aesthetically pleasing output). Manual addition of CSS can improve report appearance if desired.

The package has a lot of scope for improvement. It's been shared in a very basic form, with the assumption that the most desired improvements will become clear as usage increases. Early ideas for improvements are as follows:
* Add auto-formatting of DataFrames.
* Allow addition of plots produced with other plotting libraries (e.g. [matplotlib](https://matplotlib.org/)) to report.
* Document class naming structure to allow manual CSS choices.
* Implement Collapsy: collapsable button with similar purpose to Tabby.

### Motivation for package use?

See below examples of common approaches adopted when sharing results of data analysis (and their shortcomings).

#### Approach 1: Sharing static data

Do you share static data - for example, screenshots of DataFrames and Figures from a Jupyter notebook's output - via another medium (e.g. Slack)? If so, consider the following:

* Each time your input data or method of analysis changes, you must reproduce the output, screenshot and share the results again.
* Each time you share the output, you must also provide an explanation of the results.
* A chat / email history containing analysis of many versions of the same data can lead to confusion in the future.

#### Approach 2: Sharing code

Sharing code (that performs analysis) likely means GitHub or GitLab is in use. Whilst this comes with the ability to rollback a data pull function, static data or the method of analysis to a specific point in time, it also has shortcomings:

* Each new colleague who wishes to view the output must clone the repository and execute the analysis, which is sub-optimal. This could be especially time consuming if the data pull (if required) and anaylsis-producing code is computationally expensive.
* Non-technical colleagues may fail to understand the output due to their inability to digest the code, and may be incapable of producing the output altogether.

#### Suggestion: use *html-report*!

A suggested workflow when using the package is:

1. Create a GitHub or GitLab repo.
2. Write Python code to perform analysis.
3. Embed use of the package in the project's code so that a new report is produced upon code execution.

This workflow has the following advantages over other approaches:

* Use of plotly reaps all the benefits of plotly's javascript (which facilitates interactive plots). 
* Use of pandas reaps all the benefits of pandas' Styler object for formatting (see [here](https://pandas.pydata.org/docs/user_guide/style.html)).
* Use of markdown reaps all the benefits of markdown style formatting.
* Use of HTML and CSS allows users willing to get their hands dirty with CSS to produce visually appealing reports.
* A set of *.html* files in a local directory can be easily organsied and distributed, unlike a set of screenshots in a chat history.
* Non-technical colleagues are highly likely to be familiar with *.html* files.
* Use of version control brings the same advantages as approach 2 (above).

## Usage
### Installation

The package will be available for installation from PyPI soon.

### Understanding the package

The functionality of the package is intentionally simple: you can only add content to your report. This may lead to the following queries:

1. *How do I view the content of my report?* Solution: Render using `save()` and view in browser!
2. *How do I delete content from my report?* Solution: Comment out / delete a few lines of code and re-run your report building code to create a new instance of `HTMLReport`!
3. *How do I change the order of content in my report?* Solution: Swap a few lines of code and re-run your report building code to create a new instance of `HTMLReport`!

Given the approaches suggested by (2) and (3), it's advisable to separate your report building code and computationally intensive code (e.g. iterating over a large DataFrame), thereby enabling you to create an updated copy of your report fast.

## Quickstart

The package defines two classes:

* `HTMLReport`, and
* `Tabby`.

### Quickstart: `HTMLReport`

The workhorse class that facilitates the production of interactive reports.

#### Recommendation

It is recommended to separate reports into sections, since it allows readers to digest results faster. A section is added one at a time using `add_section`. Order of section creation maps to order of display in the report.

```
add_section(
    self,
    id: str,
    width: Optional[str] = None
) -> None
```

Parameters:

* `id`: Identifier of section.
* `width`: Width of section. Advised to parse width as a percentage (e.g. '80%') of the containing block. See documentation on CSS width property for range of values that can be parsed.

#### Descriptive content

Descriptive content is added through the functions `add_header`, `add_para` and `add_markdown`. 
```
add_header(
    self,
    content: str,
    size: Optional[int] = None,
    sec: Optional[str] = None
) -> None

add_para(
    self,
    content: str,
    sec: Optional[str] = None
) -> None:

add_markdown(
    self,
    content: str,
    sec: Optional[str] = None
) -> None
```

Common parameters:

* `content`: Paragraph or heading text to be displayed / markdown content to render to HTML.
* `sec`: Identifier of the section to add the header / paragraph / markdown content to. If not parsed, content added to main report body.

Additional parameters:
* `size` (`add_header`): Size of the header - between 1 (largest) and 6 (smallest). Determines the HTML tag used.

The function `add_markdown` depends on the [markdown](https://pypi.org/project/Markdown/) package. `add_markdown(content)` calls `markdown.markdown(content, output_format="html5")` to render HTML style tags from markdown style input. See function's behaviour [here](https://python-markdown.github.io/reference/).

#### Analytical content

`HTMLReport`'s workhorse function, which allows analysis to be added to the report, is `add`. 

```
add(
    self,
    obj: Union[Tabby, dom_tag, DataFrame, Styler, Figure],
    sec: Optional[str] = None,
) -> None
```

Parameters:

* `obj`: Object to add. Add instance of pandas DataFrame, pandas Styler, plotly Figure or Tabby to report. Can add instance of dominate dom_tag if you wish to interact with dominate package.
* `sec`: Identifier of the section to add object to. If not parsed, content added to main report body.

#### Output

The report can be rendered using `save()` or `to_html()`.

```
to_html(
    self
) -> str

save(
    self,
    filepath: Union[str, Path] = "unnamed_report.html",
    open_browser: bool = True,
) -> None
```

Parameters:
* `filepath`: Location to save report in.
* `open_browser`: If True, automatically open in browser on save.
        

### Quickstart: `Tabby`

Supplementary class to `HTMLReport`. Allows descriptive and analytical content to be displayed on different tabs, thereby making the content within the report more digestable.

When adding content, a key must be parsed to specify which tab the content should be added to. This is done through the parameter `key`, which is considered similar to the parameter `sec` found in `HTMLReport`'s methods. Unlike `sec`, `key` is not optional.

When adding content to a tab:
* if a previously seen value of `key` is parsed, content is appended to tab, or
* if a previously unseen value of `key` is parsed, a new tab is automatically created and content is appended to new tab.

Order of tab creation maps to order of display when rendered. If specific order of keys is desired, then `keys: Optional[List[Any]] = None` can be parsed to `Tabby` constructor. Whether created in constructor method or a content addition method, each key will be calculated as `str(key)`. Hence, it is recommended to always parse a key as a string.

#### Descriptive content

Added in similar manner as `HTMLReport` with functions `add_header`, `add_para` and `add_markdown`. 

```
add_header(
    self,
    key: Any,
    content: str,
    size: int = 1
) -> None

add_para(
    self,
    key: Any,
    content: str
) -> None

add_markdown(
    self,
    key: Any,
    content: str
) -> None
```

Common parameters:

* `key`: Key of tab to add content to. Key will be calculated as `str(key)`, hence, it is recommended to parse a string to method.
* `content`: Paragraph or heading text to be displayed / markdown content to render to HTML.

Additional parameters:
* `size` (`add_header`): Size of the header - between 1 (largest) and 6 (smallest). Determines the HTML tag used.

#### Analytical content

Similarly to `HTMLReport`, `Tabby`'s workhorse function is `add`. 

```
add(
    self,
    key: Any,
    obj: Union[dom_tag, DataFrame, Styler, Figure],
) -> None
```

Parameters:

* `key`: Key of tab to add content to. Key will be calculated as `str(key)`, hence, it is recommended to parse a string to method.
* `obj`: Object to add. Add instance of pandas DataFrame, pandas Styler or plotly Figure to tab. Can add instance of dominate dom_tag if you wish to interact with dominate package.

## Usage example 

Download the example [here](https://github.com/ben-j-barlow/html-report/blob/master/example/report.html) and open in browser to see the rendered version of the report.

```
from pathlib import Path

import plotly.express as px
import seaborn as sns

from htmlreport import HTMLReport, Tabby

iris = sns.load_dataset("iris")

# section 1: prepare data

data_summary = iris.head(5).style.format(precision=2)
data_summary.set_table_styles(
    [
        {"selector": "th.col_heading", "props": "text-align: center;"},
        {"selector": "th.col_heading.level0", "props": "font-size: 1.5em;"},
        {"selector": "td", "props": "text-align: center; font-weight: bold;"},
    ],
    overwrite=False,
)
data_summary.set_caption("The iris dataset").set_table_styles(
    [
        {
            "selector": "caption",
            "props": "caption-side: bottom; text-align: center; font-size:1.25em;",
        }
    ],
    overwrite=False,
)

keys = [str(ele) for ele in iris["species"].unique()]
tab_spec = Tabby(keys=keys)
var_to_display = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
for spec in keys:
    mask = iris["species"] == spec
    to_plot = iris.loc[mask, var_to_display]
    tab_spec.add(key=spec, obj=px.box(to_plot))
    tab_spec.add_para(
        key=spec,
        content="""Plots produced with Plotly reap all the benefits of Plotly's javascript. For example, check the 
        responsiveness of plots by resizing your window!""",
    )

# section 2: produce report

rep = HTMLReport(
    title="html-report: Example Report",
    default_header_size=3,
    default_section_width="70%",
)

rep.add_section(id="summ")
rep.add_header(content="Data Overview", sec="summ")
rep.add_markdown(
    content="""Use of `add_section()` creates border around content later added to section.  
    The heading above, paragraph below and data below are added using `add_header()`, `add_para()` and `add()`, 
    respectively.""",
    sec="summ",
)
rep.add_para(
    content="The first 5 rows of the data to analyse:",
    sec="summ",
)
rep.add(data_summary, sec="summ")


rep.add_section(id="spec")
rep.add_header(content="Analysis of Species", sec="spec")
rep.add_markdown(
    content="Line breaks and emphasis in the descriptive content below is achieved with markdown style input.",
    sec="spec",
)
rep.add_markdown(
    content=f"""There are 3 species to analyse:  
<em>{keys[0]}</em>  
<em>{keys[1]}</em>  
<em>{keys[2]}</em>""",
    sec="spec",
)
rep.add_para(
    content="See use of Tabby below:",
    sec="spec",
)
rep.add(obj=tab_spec, sec="spec")


output = rep.to_html()  # output as str
rep.save(
    filepath=Path(__file__).parent / "report.html", open_browser=True
)  # output as file
```