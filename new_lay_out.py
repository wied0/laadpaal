import os
import pandas as pd
import geopandas
import folium
import plotly.graph_objects as go
from streamlit_folium import folium_static
import streamlit as st
import plotly.figure_factory as ff

path_raw = '/Users/rubenwiedijk/PycharmProjects/VA_opdracht/dashboard/data_raw'
path_clean = '/Users/rubenwiedijk/PycharmProjects/VA_opdracht/dashboard/data_clean'

st.set_page_config(
    page_title = 'Streamlit Sample Dashboard Template',
    page_icon = '✅',
    layout = 'wide'
)

# def _max_width_(prcnt_width:int = 50):
#     max_width_str = f"max-width: {prcnt_width}%;"
#     st.markdown(f"""
#                 <style>
#                 .reportview-container .main .block-container{{{max_width_str}}}
#                 </style>
#                 """,
#                 unsafe_allow_html=True,
#     )

st.markdown("## Dashboard")
my_expander = st.expander("Procentuele toename electrische auto's", expanded=True)

with my_expander:
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown("**2018**")
        number1 = 111
        st.markdown(f"<h1 style='text-align: center; color: white;'>{13.55}%</h1>", unsafe_allow_html=True)

    with kpi2:
        st.markdown("**2019**")
        number2 = 222
        st.markdown(f"<h1 style='text-align: center; color: white;'>{5.51}%</h1>", unsafe_allow_html=True)

    with kpi3:
        st.markdown("**2020**")
        number3 = 333
        st.markdown(f"<h1 style='text-align: center; color: white;'>{7.94}%</h1>", unsafe_allow_html=True)

    st.markdown("<hr/>",unsafe_allow_html=True)



# kpi 1

my_expander1 = st.expander("Laadpalen in Nederland", expanded=True)
with my_expander1:
    kpi01, kpi02, kpi03 = st.columns(3)
    with kpi01:
        st.markdown("**Aantal laadpaal locaties in Nederland**")
        unumber1 = 7787
        st.markdown(f"<h1 style='text-align: center; color: white;'>{unumber1}</h1>", unsafe_allow_html=True)

    with kpi02:
        st.markdown("**Aantal laadpalen in Nederland**")
        number1 = 11065
        st.markdown(f"<h1 style='text-align: center; color: white;'>{number1}</h1>", unsafe_allow_html=True)

    with kpi03:
        st.markdown("**Aantal laadpalen per locatie**")
        number1 = round(11065/7787, 2)
        st.markdown(f"<h1 style='text-align: center; color: white;'>{number1}</h1>", unsafe_allow_html=True)


st.markdown("<hr/>", unsafe_allow_html=True)


uchart1, uchart2 = st.columns(2)

with uchart1:
    os.chdir(path_clean)
    geo_df = pd.read_csv('geo_df.csv')

    def color_producer(type):
        if type == 'North Brabant':
            return 'goldenrod'
        elif type == 'Samenwerkingsverband Regio Eindhoven':
            return 'goldenrod'
        elif type == 'Noord-Brabant':
            return 'goldenrod'
        elif type == 'Nordbraban':
            return 'goldenrod'
        elif type == 'Noord Brabant ':
            return 'goldenrod'
        elif type == 'South Holland':
            return 'Orange'
        elif type == 'Zuid-Holland':
            return 'Orange'
        elif type == 'Zuid Holland':
            return 'Orange'
        elif type == 'ZH':
            return 'Orange'
        elif type == 'North Holland':
            return 'Yellow'
        elif type == 'Stadsregio Amsterdam':
            return 'Yellow'
        elif type == 'Noord-Holland':
            return 'Yellow'
        elif type == 'Nordholland':
            return 'Yellow'
        elif type == 'Noord Holand':
            return 'Yellow'
        elif type == 'Noord Holland':
            return 'yellow'
        elif type == 'Noord-Hooland':
            return 'yellow'
        elif type == 'Zeeland':
            return 'aqua'
        elif type == 'Seeland':
            return 'aqua'
        elif type == 'Utrecht':
            return 'lightblue'
        elif type == 'UT':
            return 'lightblue'
        elif type == 'UTRECHT':
            return 'lightblue'
        elif type == 'Limburg':
            return 'pink'

            # In[8]:

    gdf = geopandas.GeoDataFrame(
        geo_df, geometry=geopandas.points_from_xy(geo_df.Longitude, geo_df.Latitude))

    # In[9]:

    laadpaaldata = pd.read_csv('laadpaaldata_dt.csv')

    # In[10]:

    # st.text("Op deze kaart worden de laadpalen weergegeven uit de dataframe. De laadpalen zijn groepeerd per provincie,
    # dankzij de kleuren legenda kan je in één oogopslag zien welke kleur bij welke provincie hoort. Hier is terug te zien dat de meeste laadpalen zich bevinden in de randstad. Dit is ook niet zo gek want het voornaamste gedeelte van de bevolking woont in de randstad.")

    m = folium.Map(location=[52.0907374, 5.1214209], zoom_start=7.5, tiles='cartodbdark_matter')

    for Town in gdf.iterrows():
        row_values = Town[1]
        location = tuple([row_values['Latitude'], row_values['Longitude']])
        marker = folium.Circle(location=location, popup=row_values['AddressLine1'],
                               color=color_producer(row_values['StateOrProvince']),
                               fill_color=color_producer(row_values['StateOrProvince'])
                               )
        marker.add_to(m)


    # In[11]:

    #  ik heb een functie gevonden op het internet voor het toevoegen van een categorische legenda:
    # (bron: https://stackoverflow.com/questions/65042654/how-to-add-categorical-legend-to-python-folium-map)


    def add_categorical_legend(folium_map, title, colors, labels):
        if len(colors) != len(labels):
            raise ValueError("colors and labels must have the same length.")

        color_by_label = dict(zip(labels, colors))

        legend_categories = ""
        for label, color in color_by_label.items():
            legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"

        legend_html = f"""
        <div id='maplegend' class='maplegend'>
          <div class='legend-title'>{title}</div>
          <div class='legend-scale'>
            <ul class='legend-labels'>
            {legend_categories}
            </ul>
          </div>
        </div>
        """
        script = f"""
            <script type="text/javascript">
            var oneTimeExecution = (function() {{
                        var executed = false;
                        return function() {{
                            if (!executed) {{
                                 var checkExist = setInterval(function() {{
                                           if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                              clearInterval(checkExist);
                                              executed = true;
                                           }}
                                        }}, 100);
                            }}
                        }};
                    }})();
            oneTimeExecution()
            </script>
          """

        css = """

        <style type='text/css'>
          .maplegend {
            z-index:9999;
            float:right;
            background-color: rgba(255, 255, 255, 1);
            border-radius: 5px;
            border: 2px solid #bbb;
            padding: 10px;
            font-size:12px;
            positon: relative;
          }
          .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
          .maplegend .legend-scale ul {
            margin: 0;
            margin-bottom: 5px;
            padding: 0;
            float: left;
            list-style: none;
            }
          .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
          .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 0px solid #ccc;
            }
          .maplegend .legend-source {
            font-size: 80%;
            color: #777;
            clear: both;
            }
          .maplegend a {
            color: #777;
            }
        </style>
        """

        folium_map.get_root().header.add_child(folium.Element(script + css))

        return folium_map


    m = add_categorical_legend(m, 'StateOrProvince',
                               colors=['goldenrod', 'Orange', 'yellow', 'aqua', 'navy', 'red'],
                               labels=['Noord-Brabant', 'Zuid-Holland', 'Noord-Holland', 'Zeeland', 'Utrecht',
                                       'Limburg'])

    folium_static(m)

with uchart2:
    os.chdir(path_clean)
    laadpaaldata = pd.read_csv('laadpaaldata_dt.csv')
    # gemiddelde en mediaan berekenen
    contimemean = laadpaaldata['ConnectedTime'].mean()
    chatimemean = laadpaaldata['ChargeTime'].mean()

    contimemedian = laadpaaldata['ConnectedTime'].median()
    chatimemedian = laadpaaldata['ChargeTime'].median()

    # displot creëren
    fig = ff.create_distplot([laadpaaldata['ConnectedTime'], laadpaaldata['ChargeTime']],
                             group_labels=['Tijd aan de lader', 'Tijd om op te laden'], show_rug=False,
                             curve_type='normal')

    # verticale lijnen van gemiddelde en mediaan toevoegen
    fig.add_shape(type='line', x0=contimemean, y0=0, x1=contimemean, y1=1, line=dict(color='Blue', ), xref='x',
                  yref='paper',
                  name='Gemiddelde Connected time')
    fig.add_shape(type='line', x0=chatimemean, y0=0, x1=chatimemean, y1=1, line=dict(color='Red', ), xref='x',
                  yref='paper',
                  name='Gemiddelde Charge time')
    fig.add_shape(type='line', x0=contimemedian, y0=0, x1=contimemedian, y1=1, line=dict(color='Blue', ), xref='x',
                  yref='paper',
                  name='Mediaan Connected time')
    fig.add_shape(type='line', x0=chatimemedian, y0=0, x1=chatimemedian, y1=1, line=dict(color='Red', ), xref='x',
                  yref='paper',
                  name='Mediaan Charge time')

    # annotations bij de lijnen toevoegen
    fig.add_annotation(x=contimemean, y=0.8, yref='paper',
                       text="Gemiddelde tijd aan de lader",
                       showarrow=True, ax=120)
    fig.add_annotation(x=chatimemean, y=0.9, yref='paper',
                       text="Gemiddelde tijd om op te laden",
                       showarrow=True, ax=150, ay=-60)
    fig.add_annotation(x=contimemedian, y=0.6, yref='paper',
                       text="Mediaan tijd aan de lader",
                       showarrow=True, ax=120)
    fig.add_annotation(x=chatimemedian, y=0.8, yref='paper',
                       text="Mediaan tijd om op te laden",
                       showarrow=True, ay=-80)

    fig.update_layout(barmode='overlay',
                      autosize=False, width=800, height=550)
    fig.update_traces(opacity=0.75)

    # titels en astitels
    fig.update_layout(title='Oplaadtijd en connectietijd (zonder uitschieters) met kansdichtheidbenadering')
    fig.update_xaxes(title='Tijd in uren')
    fig.update_yaxes(title='Dichtheid')

    st.plotly_chart(fig)

chart1 = st.container()
chart2 = st.container()

with chart1:
    path_clean = '/Users/rubenwiedijk/PycharmProjects/VA_opdracht/dashboard/data_clean'

    os.chdir(path_clean)

    diesel_per_month = pd.read_csv('diesel_per_month.csv', index_col='datum_tenaamstelling')
    benzine_per_month = pd.read_csv('bezine_per_month.csv', index_col='datum_tenaamstelling')

    option = st.selectbox('How would you like to be contacted?',
                          ('brandstofverbruik_gecombineerd',
       'brandstofverbruik_stad', 'brandstofverbruik_buiten', 'co2_uitstoot_gecombineerd',
       'emissie_co2_gecombineerd_wltp', 'brandstof_verbruik_gecombineerd_wltp'))

    description = {'brandstofverbruik_gecombineerd': 'Het brandstofverbruik in l/100 km, tijdens een combinatie van gestandaardiseerde stadsrit- en rit buiten de stad, getest op een rollenbank.',
                    'brandstofverbruik_stad':'Het brandstofverbruik in l/100 km, tijdens een gestandaardiseerde stadsritcyclus, getest op een rollenbank.',
                   'brandstofverbruik_buiten':'Het brandstofverbruik in l/100 km, tijdens een gestandaardiseerde rit buiten de stad, getest op een rollenbank.',
                   'co2_uitstoot_gecombineerd': 'De gewogen uitstoot van CO2 in g/km van een plug-in hybride voertuig, tijdens een combinatie van een stadsrit en een rit buiten de stad, getest op een rollenbank. De waarde is berekend aan de hand van de uitstoot die ontstaat door eenmaal met lege accu’s en eenmaal met volle accu’s te rijden.',
                   'emissie_co2_gecombineerd_wltp': 'CO2 uitstoot gemeten bij een op een rollenbank rijdend voertuig tijdens een rit volgens de WLTP test onder gecombineerde belasting.',
                   'brandstof_verbruik_gecombineerd_wltp':'Gewogen brandstofverbruik gemeten bij een op een rollenbank rijdend voertuig tijdens een rit volgens de WLTP test onder gecombineerde belasting.'}
    st.write(description[option])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=benzine_per_month.index, y=benzine_per_month[option], name='Benzine'))
    fig.add_trace(
        go.Scatter(x=diesel_per_month.index, y=diesel_per_month[option], name='Diesel'))

    fig.update_xaxes(range=[diesel_per_month.index.min(), diesel_per_month.index.max()])

    fig.update_xaxes(title='Datum')
    fig.update_yaxes(title= option)
    fig.update_layout(title='Verbuik van benzine en diesel over tijd',
                      autosize=False, width=1300, height=500)

    st.plotly_chart(fig)

with chart2:
    fig = go.Figure()

    path_clean = '/Users/rubenwiedijk/PycharmProjects/VA_opdracht/dashboard/data_clean'

    os.chdir(path_clean)

    cumsum_sales = pd.read_csv('cumsum_sales.csv', index_col='datum_tenaamstelling')

    for column in cumsum_sales.columns:
        fig.add_trace(go.Scatter(x=cumsum_sales.index, y=cumsum_sales[column], name=column))

    fig.update_xaxes(range=['2017-01-01', diesel_per_month.index[-1]])
    fig.update_xaxes(title='Jaar')
    fig.update_yaxes(title='Aantal')
    fig.update_layout(title='Verkoop autos per merk',
                      autosize=False, width=1300, height=500)

    st.plotly_chart(fig)
