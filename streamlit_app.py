import streamlit as st
# import matplotlib.pyplot as plt
import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
TODAY = datetime.date.today()
today_day = TODAY.strftime('%Y-%m-%d')

st.set_page_config(layout="wide", page_title="Natural Gas Analysis")
# 'D:\Lab\container\trader_lab\Dashbord\dash_soy.h5', key='soybean_cots')

##########  CREATING DATASETS ###############
soft_reports = pd.read_hdf('./data/dash_soy.h5', key='soybean_cots',)
soft_yf = pd.read_hdf('./data/soft_main_prices.h5', key='soft_prices', )
soft_reports.index = soft_reports.index.set_levels(pd.to_datetime(
    soft_reports.index.levels[1], format="%Y-%m-%d"), level=1)

com_starting_date = soft_yf.index.min()
com_ending_date = soft_yf.index.max()

com_date_range = pd.date_range(com_starting_date[1], com_ending_date[1])


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background: linear-gradient(to bottom, #bdffa9 0%,	#8bd05a 100%);
background-position: top left;
}}

        
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

.stTabs [data-testid="stMarkdownContainer"] p {{
 background-color:"green"}}

.stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
    font-size:1.5rem;
    font:"serif";
    }}

[data-testid="stSidebar"] >  div:first-child {{
background: linear-gradient(to bottom, #aaff77  0%,#095608 100%); 
background-position: top left;
background-attachment: fixed;
}}

[data-testid="st.tabs"] >  div:first-child {{
<h3></h3>
}}

</style>
"""

st.markdown("""
  <style>
  .css-16idsys.e16nr0p34 {
    background-color: #A0BFE0; 
            
    
  }
  </style>
""", unsafe_allow_html=True)

# side bar
st.sidebar.image("data/logo1.png")
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("""
            <style>
                .css-18e3th9 {
                        padding-top: 0rem;
                        padding-bottom: 0rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
                .css-1d391kg {
                        padding-top: 0rem;
                        padding-right: 1rem;
                        padding-bottom: 0rem;s
                        padding-left: 1rem;
                    }
            </style>
        """, unsafe_allow_html=True)


css = """
<style>
    .stTabs [data-baseweb="tab-highlight"] {
        background-color:transparent;
    }
</style>
"""

st.markdown(css, unsafe_allow_html=True)


column = st.sidebar.columns((1, 1))


with column[0]:
    start_soft = st.date_input(label="**FROM**", value=pd.to_datetime(
        "2019-01-31", format="%Y-%m-%d"), label_visibility="collapsed")
with column[1]:
    end_soft = st.date_input(
        label="**TO**", value=pd.to_datetime(today_day, ), label_visibility="collapsed")

top_chart_commodity = st.sidebar.selectbox(
    "**COMMODITY PRICE**", (soft_yf.index.get_level_values("ticker").unique()),
    label_visibility="collapsed")
soft_close = soft_yf.loc[top_chart_commodity, "close"]


cot_commodity_report = st.sidebar.selectbox(
    "**COM TICKER**", (soft_reports.index.get_level_values("ticker").unique()), label_visibility="collapsed")


column_of_report = st.sidebar.selectbox(
    "**COT Ind full**", soft_reports.columns[1:], label_visibility="collapsed")

############# TOP PRICE CHART #################

top_fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.05, row_heights=[0.50, 0.50])
start_time_nat = pd.to_datetime(start_soft, format="%Y-%m-%d")
end_time_nat = pd.to_datetime(end_soft, format="%Y-%m-%d")
times_mask = (soft_close.index < str(end_time_nat)) & (
    soft_close.index >= str(start_time_nat))
timetrimmed_soft = soft_close.loc[times_mask]
top_fig.add_trace(go.Scatter(x=timetrimmed_soft.index,
                             y=timetrimmed_soft,
                             fill='tozeroy',
                             line=dict(color='black', width=1),
                             name="SOFT"),
                  row=1, col=1)


max_close_soft = soft_close.loc[times_mask].max()
min_close_soft = soft_close.loc[times_mask].min()
top_fig.update_layout(
    yaxis_range=[min_close_soft, max_close_soft, ], uniformtext_minsize=12)
top_fig.add_annotation(text=top_chart_commodity,
                       xref="paper", yref="paper", font=dict(size=30, color="#050303"), opacity=0.5,
                       x=0.0, y=1.1, showarrow=False)

########## PLOT COT REPORT #############

cot_commodity = soft_reports.loc[cot_commodity_report]
subset_cot_commodity = cot_commodity
final_com = subset_cot_commodity[column_of_report]

max_diff = final_com.max()
min_diff = final_com.min()

top_fig.add_trace(go.Scatter(x=final_com.index,
                             y=final_com,
                             fill='tonexty',
                             name=" ", mode='lines',  # line_color='blue',
                             line=dict(color='#403824', width=1)),
                  row=2, col=1)

top_fig.update_yaxes(range=[min_diff, max_diff], row=2, col=1)
top_fig.update_xaxes(range=[start_time_nat, end_time_nat])
top_fig.update_layout(showlegend=False)
top_fig.add_annotation(text=cot_commodity_report,
                       xref="paper", yref="paper", font=dict(size=30, color="#050303"), opacity=0.5,
                       x=0.0, y=0.45, showarrow=False)
top_fig.update_traces(hovertemplate="%{x|%Y-%m-%d}", hoverinfo="skip")
top_fig.update_layout(
    hoverlabel=dict(
        bgcolor='rgba(0,0,0,0)',
        font_size=10,
        font_color='rgba(0,0,0,10)',
        font_family="Ariel"))
top_fig.update_traces(xaxis='x1')
top_fig.update_layout(paper_bgcolor='rgb(184, 247, 212)',
                      plot_bgcolor='rgb(184, 247, 212)')
top_fig.update_layout(paper_bgcolor='rgb(0,0,0,0)',
                      plot_bgcolor='rgb(0,0,0,0)')
top_fig.update_layout(hovermode="x unified",
                      height=1000)
top_fig.update_traces(xaxis='x1')

top_fig.for_each_xaxis(lambda x: x.update(showgrid=False))
top_fig.for_each_yaxis(lambda x: x.update(showgrid=False))
st.plotly_chart(top_fig, use_container_width=True)

#############
