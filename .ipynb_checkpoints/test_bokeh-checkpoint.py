from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Panel, Tabs, Div

# Simple tab content
tab1 = Panel(child=Div(text="<b>Tab 1 Content</b>"), title="Tab 1")
tab2 = Panel(child=Div(text="<b>Tab 2 Content</b>"), title="Tab 2")

# Create tabs
tabs = Tabs(tabs=[tab1, tab2])

# Layout
curdoc().add_root(column(tabs))
curdoc().title = "Minimal Tabs Test"


