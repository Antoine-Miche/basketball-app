#Importation des librairies

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from PIL import Image
import base64
import plotly.graph_objects as go


# Config of the page of our dashboard
st.set_page_config(
    page_title="Euroleague dashboard",
    page_icon="🏀",
    layout = "wide",

)

#Import data
#Import the global data
data = pd.read_csv("sportsref_download.xls.csv", sep = ";")
data = data.fillna(0)

#Import the data of the match
data_of_the_match = pd.read_csv("last_match.csv", sep = ";")

player_photo = pd.read_csv("player_photo.csv", sep = ";")


st.markdown(
    """
    <div style='display: flex; justify-content: center; align-items: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/fr/thumb/f/ff/Logo_AS_Monaco_Basket.svg/800px-Logo_AS_Monaco_Basket.svg.png' style='margin-right: 1rem; width: 100px;'>
        <h1 style='text-align: center;'>Stats analysis of Monaco team players against Partizan belgrade</h1>
        <img src='https://www.basketeurope.com/wp-content/uploads/2017/12/1200px-KK_Partizan_logo.svg-426x500.png' style='margin-left: 1rem; width: 100px;'>
    </div>
    """,
    unsafe_allow_html=True,
)



st.divider()

col1, col2, col3 = st.columns(3)



with col2:

    l1_col1, l1_col2, l1_col3 = st.columns([1, 3, 1])

    # Add elements to the columns
    with l1_col2:
        
        player_select = st.selectbox("Player name :", (data_of_the_match.Player.values))
        st.markdown(f'<div style="text-align:center"><img src="{player_photo["url photos"].loc[player_photo["Nom des joueurs"] == player_select].values[0]}" style="max-width:200px"></div>', unsafe_allow_html=True)

    with l1_col1:
        st.write("")

    with l1_col3:
        st.write("")

    st.divider()

    l2_col21, l2_col22, l2_col23 = st.columns([2, 3, 2])
    with l2_col21:
        st.write("<p style='text-align: center; color: white; font-weight : bold'>For this match</p>", unsafe_allow_html=True)
        minute_played = data_of_the_match.MP.loc[data_of_the_match["Player"] == player_select].values[0]
        st.write(f"<p style='text-align: center;'>{minute_played}</p>", unsafe_allow_html=True)
        pt = data_of_the_match.PTS.loc[data_of_the_match["Player"] == player_select].values[0]
        st.write(f"<p style='text-align: center;'>{pt}</p>", unsafe_allow_html=True)
        pf = data_of_the_match.PF.loc[data_of_the_match["Player"] == player_select].values[0]
        st.write(f"<p style='text-align: center;'>{pf}</p>", unsafe_allow_html=True)
    with l2_col22:
        st.write("<p style='text-align: center; font-weight : bold'>VS</p>", unsafe_allow_html=True)
        st.write("<p style='text-align: center; font-weight : bold'>Minute played</p>", unsafe_allow_html=True)
        st.write("<p style='text-align: center; font-weight : bold'>Points</p>", unsafe_allow_html=True)
        st.write("<p style='text-align: center; font-weight : bold'>Personnal foul</p>", unsafe_allow_html=True)
    with l2_col23:
        st.write("<p style='text-align: center; color: white; font-weight : bold'>Euroleague season</p>", unsafe_allow_html=True)
        av_minute_played = data.MP.loc[data["Player"] == player_select].values[0]
        st.write(f"<p style='text-align: center;'>{av_minute_played}</p>", unsafe_allow_html=True)
        av_pt = data.PTS.loc[data["Player"] == player_select].values[0]
        st.write(f"<p style='text-align: center;'>{av_pt}</p>", unsafe_allow_html=True)
        av_pf = data.PF.loc[data["Player"] == player_select].values[0]
        st.write(f"<p style='text-align: center;'>{av_pf}</p>", unsafe_allow_html=True)

with col1:
    
    st.write("<h3 style='text-align: center;font: bold;'>Offensive stats</h3>", unsafe_allow_html=True)

    categories = ["Field goal (%)", "3 points (%)", "Free throw (%)","Field goal (%)"]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[data["FG%"].loc[data["Player"]==player_select].values[0],
        data["3P%"].loc[data["Player"]==player_select].values[0],
        data["FT%"].loc[data["Player"]==player_select].values[0],
        data["FG%"].loc[data["Player"]==player_select].values[0]],
        theta=categories,
        fill='toself',
        name='Euroleague season',
        fillcolor='white',
        line=dict(color='white', width=3),
        opacity=0.5
    ))
    fig.add_trace(go.Scatterpolar(
        r=[data_of_the_match["FG%"].loc[data_of_the_match["Player"]==player_select].values[0],
        data_of_the_match["3P%"].loc[data_of_the_match["Player"]==player_select].values[0],
        data_of_the_match["FT%"].loc[data_of_the_match["Player"]==player_select].values[0],
        data_of_the_match["FG%"].loc[data_of_the_match["Player"]==player_select].values[0]],
        theta=categories,
        fill='toself',
        name='Match',
        fillcolor='red',
        line=dict(color='red', width=3),
        opacity=0.5
    ))

    fig.update_layout(
    polar=dict(
        bgcolor = "rgba(0,0,0,0)",
        radialaxis=dict(
        visible=True,
        range=[0, 1]
        ),
        angularaxis=dict(
            tickfont=dict(size=13, family='Arial', color='white'),
            linewidth=3,
            type='category',
            direction='clockwise'
        )),
    showlegend=True,
    paper_bgcolor="rgba(0,0,0,0)", 
    plot_bgcolor="rgba(0,0,0,0)"
    )



    st.plotly_chart(fig,use_container_width=True)

with col3:


    # Définir les données
    categories = ["Offensive rebound", "Defensive rebound", "Total rebound", "Assist", "Steal", "Block", "Turnover"]
    season_avg = [data["ORB"].loc[data["Player"]==player_select].values[0],
                   data["DRB"].loc[data["Player"]==player_select].values[0],
                   data["TRB"].loc[data["Player"]==player_select].values[0],
                   data["AST"].loc[data["Player"]==player_select].values[0],
                   data["STL"].loc[data["Player"]==player_select].values[0],
                   data["BLK"].loc[data["Player"]==player_select].values[0],
                   data["TOV"].loc[data["Player"]==player_select].values[0]]
    
    match_stats = [data_of_the_match["ORB"].loc[data_of_the_match["Player"]==player_select].values[0],
                   data_of_the_match["DRB"].loc[data_of_the_match["Player"]==player_select].values[0],
                   data_of_the_match["TRB"].loc[data_of_the_match["Player"]==player_select].values[0],
                   data_of_the_match["AST"].loc[data_of_the_match["Player"]==player_select].values[0],
                   data_of_the_match["STL"].loc[data_of_the_match["Player"]==player_select].values[0],
                   data_of_the_match["BLK"].loc[data_of_the_match["Player"]==player_select].values[0],
                   data_of_the_match["TOV"].loc[data_of_the_match["Player"]==player_select].values[0]]

    diffs = [((m-s)/s*100) if s!=0 else 0 for s,m in zip(season_avg, match_stats)]

    # Créer les graphiques
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=season_avg, y=categories, name='Euroleague season', orientation='h', marker=dict(color='white')))
    fig_bar.add_trace(go.Bar(x=match_stats, y=categories, name='Match', orientation='h', marker=dict(color='red'), textposition='auto'))

    # Ajouter les annotations avec les différences en pourcentage
    for i, diff in enumerate(diffs):
        if diff > 0:
            x = match_stats[i] + 0.40
            text = f"+{diff:.1f}%"
        else:
            x = season_avg[i] + 0.40
            text = f"{diff:.1f}%"
        fig_bar.add_annotation(x=x, y=categories[i], text=text, 
                                font=dict(color='white', size=14), 
                                showarrow=False, align='center')

    fig_bar.update_layout(
        barmode='group',
        margin=dict(l=50, r=50, t=50, b=50), height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(tickfont=dict(size=14, color='white')),
        xaxis=dict(tickfont=dict(size=14, color='white'))
    )

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=season_avg, theta=categories, fill='toself', name='Euroleague season', fillcolor = "white", line=dict(color='white', width=3), opacity=0.5 ))
    fig_radar.add_trace(go.Scatterpolar(r=match_stats, theta=categories, fill='toself', name='Match', fillcolor = "red", line=dict(color='red', width=3), opacity=0.5 ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor = "rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, max(season_avg+match_stats)]
            ),
            angularaxis=dict(
                tickfont=dict(size=14, family='Arial', color='white'),
                linewidth=3,
                type='category',
                direction='clockwise'
            )
        ),
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Afficher les radio buttons et les graphiques correspondants

    st.write("<h3 style='text-align: center;font: bold;'>Compare euroleague season vs match stats</h3>", unsafe_allow_html=True)
    graph_type = st.radio('Graph Type', ('Bar Chart', 'Radar Chart'))
    if graph_type == 'Bar Chart':
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.plotly_chart(fig_radar, use_container_width=True)
