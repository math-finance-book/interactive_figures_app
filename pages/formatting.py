
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_iconify import DashIconify
import plotly.io as pio
import pandas as pd
import numpy as np

##############################################
#
# COLORS
#
#############################################

plotly_template = pio.templates["simple_white"]
colors = plotly_template.layout.colorway
blue = colors[0]
red = colors[1]
green = colors[2]
purple = colors[3]
orange = colors[4]
teal = colors[5]
pink = colors[6]
lime = colors[7]
magenta = colors[8]
yellow = colors[9]
white = "#fff"
black = "#000"
primary = "#2780e3"
gray700 = "#495057"
gray200 = "#e9ecef"
medblue = "#93CCFD"
danger = "#ff0039"
light = "#f8f9fa"
dark = "#373a3c"
secondary = "#373a3c"
riceblue = "#00205B"
ricegrey = "#C1C6C8"
gray400 = "#ced4da"
gray600 = "#868e96"
gray100 = "#f8f9fa"
gray300 = "#dee2e6"
gray500 = "#adb5bd"
lightblue = "#E6F4FF"


tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'color': white,
    'backgroundColor': primary
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': white,
    'color': primary,
    'fontWeight': 'bold',
    'padding': '6px'
}

text_style = {"color": primary, "font-weight": "bold", "background-color": white} # {"color": riceblue, 'font-weight': 'bold', 'background-color': ricegrey}

def myinput(id, value=None, placeholder=""):
    if value:
        return dbc.Input(
            id=id, 
            type="numeric", 
            placeholder=placeholder, 
            value=value, 
            style={"backgroundColor": lightblue}
        )
    else:
        return dbc.Input(
            id=id, 
            type="text", 
            placeholder=placeholder, 
            style={"backgroundColor": lightblue}
        )

###################################################
#
# DATA TABLE STYLING
#
###################################################

style_header = {
    "backgroundColor": gray700,
    "fontWeight": "bold",
    "color": white,
}

style_header_dark = {
    "backgroundColor": gray700,
    "fontWeight": "bold",
    "color": white,
}

def mybadge(txt) :
    return html.H4(dbc.Badge(txt, className="ms-1", color=primary, text_color=white))

style_data = {"backgroundColor": gray200}
style_editable = {"backgroundColor": lightblue}
style_light = style_data
style_dark = {"backgroundColor": gray200}

css_no_header = [{"selector": "tr:first-child", "rule": "display: none"}]


style_data_conditional = [
    {"if": {"row_index": "odd"}, "backgroundColor": gray200,},
    {"if": {"row_index": "even"}, "backgroundColor": gray400},
]

#############################################################
#
# FIGURE STYLING
#
#############################################################

def largefig(fig, showlegend=False):
    fig.layout.template = "simple_white"
    fig.update_layout(margin=dict(l=25, r=25, t=40, b=25))
    fig.update_xaxes(title_font_size=16, showgrid=True)
    fig.update_yaxes(title_font_size=16, showgrid=True)
    fig.update_layout(font_size=14)
    fig.update_layout(showlegend=showlegend)
    return fig


def smallfig(fig, showlegend=False):
    fig.layout.template = "simple_white"
    fig.update_layout(margin=dict(l=25, r=25, t=25, b=25))
    fig.update_xaxes(title_font_size=14, showgrid=True)
    fig.update_yaxes(title_font_size=14, showgrid=True)
    fig.update_layout(font_size=12)
    fig.update_layout(showlegend=showlegend)
    return fig

#####################################################
#
# SLIDER STYLING
#
#####################################################

def marks(a, b, c):
    marks = [i if i != int(i) else int(i) for i in np.arange(a, b + c, c)]
    labels = [str(x) if x != int(x) else str(int(x)) for x in marks]
    return dict(zip(marks, labels))


def pctmarks(a, b, c):
    marks = range(a, b + c, c)
    labels = [str(x) + "%" for x in marks]
    return dict(zip(marks, labels))


def dolmarks(a, b, c):
    marks = range(a, b + c, c)
    labels = ["$" + "{:,}".format(x) for x in marks]
    return dict(zip(marks, labels))


def kdolmarks(a, b, c):
    marks = range(a, b + c, c)
    labels = ["$" + "{:,}".format(int(x / 1000)) + "k" for x in marks]
    return dict(zip(marks, labels))


dct = dict(pct=pctmarks, dol=dolmarks, kdol=kdolmarks)


def Slider(text, mn, mx, step, value, tick, name, kind=None):
    if kind == "tip":
        slider = dcc.Slider(
            mn,
            mx,
            step,
            id=name,
            value=value,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
        )
    else:
        markfn = marks if not kind else dct[kind]
        slider = dcc.Slider(
            mn,
            mx,
            step,
            id=name,
            value=value,
            marks=markfn(mn, mx, tick),
            tooltip={"placement": "bottom", "always_visible": False},
        )
    return html.Div([dbc.Label(text, html_for=name), slider])


