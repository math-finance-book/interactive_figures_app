import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import math
#from math import pow, exp, sqrt
from scipy import stats
norm = stats.norm

import plotly.graph_objects as go
#import dash_bootstrap_components as dbc
#from dash import dcc, html, Output, Input, callback
#from dash.dash_table import FormatTemplate
#from pages.formatting import Slider, text_style, largefig, blue, red, green
from pages.formatting import smallfig, largefig, blue, red, green


def disc_function(FV,r,T):
    PV = FV * np.exp(-r*T)
    return PV

def bs_d1_d2(St,r,t,K,sig):
    d1 = np.log(St/K)
    d1 += (sig*sig/2 + r ) * t
    #with np.errstate(divide='ignore'):
    #    d1 /= sig * t**0.5
    d1=np.divide(d1,sig * t**0.5)
    d2 = d1 - sig * t**0.5
    return d1,d2

def cdf_approx(dn,call):
    if call:
      Ndn = (0.50 * (1.0 + math.erf(dn / math.sqrt(2.0))))
    else:
      Ndn = (0.50 * (1.0 + math.erf(-dn / math.sqrt(2.0))))
    return Ndn

def bs_delta(d1,d2,call):
    #Nd1 = cdf_approx(dn=d1,call=call)
    #Nd2 = cdf_approx(dn=d2,call=call)
    if call:
        Nd1 = norm.cdf(d1,0,1)
        Nd2 = norm.cdf(d2,0,1)
    else:
        Nd1 = norm.cdf(-d1,0,1)
        Nd2 = norm.cdf(-d2,0,1)
    return Nd1,Nd2


def bs_gamma(d1,St,sig,t):
    gamma = norm.pdf(d1)
    with np.errstate(divide='ignore'):
        gamma /= (St*sig*np.sqrt(t)) 
    return gamma

def bs_price(St,r,t,K,call,Nd1,Nd2,T):
    pvk = disc_function(K,r, T-t)
    if call:
      price = St * Nd1 - pvk * Nd2
    else:
      price = pvk * Nd2 - St * Nd1 
    return price

def bs_vega(St,d1,t):
   return St*norm.pdf(d1)*np.sqrt(t)

def bs_theta(d1,Nd1,Nd2,St,sig,r,K,t,call):
   q=0
   theta=-(St*sig*np.exp(-q*t))/(2*np.sqrt(t))*norm.pdf(d1)
   if call:
      theta-=r*K*np.exp(-r*t)*Nd2
      theta+=q*St*np.exp(-q*t)*Nd1
   else:
      theta+=r*K*np.exp(-r*t)*Nd2
      theta-=q*St*np.exp(-q*t)*Nd1
   return theta

def create_plot(sig,t,r):
    S_to_K=np.linspace(1/4,4,200)
    K=100 #normalize K then multiply by ratio
    #r=0.05
    St=S_to_K*K
    d1,d2=bs_d1_d2(St,r,t,K,sig)
    Nd1_call,Nd2_call=bs_delta(d1,d2,call=True) #call
    Nd1_put,Nd2_put=bs_delta(d1,d2,call=False) #call
    gamma=bs_gamma(d1,St,sig,t)
    vega=bs_vega(St,d1,t)
    theta_call=bs_theta(d1,Nd1_call,Nd2_call,St,sig,r,K,t,call=True)
    theta_put=bs_theta(d1,Nd1_put,Nd2_put,St,sig,r,K,t,call=False)

    fig=go.Figure()
    trace1=go.Scatter(x=S_to_K,y=Nd1_call,mode="lines",line={"color": blue},name="Call")
    trace2=go.Scatter(x=S_to_K,y=Nd1_put,mode="lines",line={"color": green},name="Put")
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.layout.xaxis["title"] = r"S/K"
    fig.layout.yaxis["title"] = r"Delta"
    #fig.update_layout(showlegend=True)

    fig2=go.Figure()
    trace1=go.Scatter(x=S_to_K,y=gamma,mode="lines")
    #trace2=go.Scatter(x=S_to_K,y=Nd1_put,mode="lines",line={"color": green},name="Put")
    fig2.add_trace(trace1)
    #fig2.add_trace(trace2)
    fig2.layout.xaxis["title"] = r"S/K"
    fig2.layout.yaxis["title"] = r"Gamma"

    fig3=go.Figure()
    trace1=go.Scatter(x=S_to_K,y=vega,mode="lines")
    #trace2=go.Scatter(x=S_to_K,y=Nd1_put,mode="lines",line={"color": green},name="Put")
    fig3.add_trace(trace1)
    #fig2.add_trace(trace2)
    fig3.layout.xaxis["title"] = r"S/K"
    fig3.layout.yaxis["title"] = r"Vega"

    fig4=go.Figure()
    trace1=go.Scatter(x=S_to_K,y=theta_call,mode="lines",line={"color": blue},name="Call")
    trace2=go.Scatter(x=S_to_K,y=theta_put,mode="lines",line={"color": green},name="Put")
    fig4.add_trace(trace1)
    fig4.add_trace(trace2)
    fig4.layout.xaxis["title"] = r"S/K"
    fig4.layout.yaxis["title"] = r"Theta"


    return (
        largefig(fig,showlegend=True),
        largefig(fig2,showlegend=False),
        largefig(fig3,showlegend=False),
        largefig(fig4,showlegend=True)
    )


vol_slider = st.slider(
    "Volatlity (sigma) ", 
    min_value=0+0.00001, 
    max_value=0.3*5, 
    step=0.1, 
    value=0.3,
)

t_slider = st.slider(
    "Time(Years) (T) ", 
    min_value=0.0, 
    max_value=1.0, 
    step=0.1, 
    value=0.5, 
)

r_slider = st.slider(
    "Interest Rate (r) ", 
    min_value=0.0, 
    max_value=0.1, 
    step=0.01, 
    value=0.05, 
)

fig1,fig2,fig3,fig4 = create_plot(vol_slider,t_slider,r_slider)

st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st.plotly_chart(fig4)