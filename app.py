import streamlit as st
import pandas as pd
import folium, json
from streamlit_folium import st_folium
from folium import plugins
import random

random.seed(100)

APP_TITLE = "서울시 레히오나"


def display_map(df_orig, geo_json, gu_name):
    if gu_name != "---전체---":
        df = df_orig[(df_orig["시군구"] == gu_name)].copy()
    else:
        df = df_orig.copy()

    map = folium.Map(
        location=[37.552213, 127.011354], tiles="cartodbpositron", zoom_start=11
    )

    if len(df) == 0:
        st_map = st_folium(map, width=1500, height=700)
        return st_map, df

    code_list = list(df["행정동코드"].unique())
    choropleth = folium.Choropleth(
        geo_data=geo_json,
    ).add_to(map)

    geo_json["features"] = [
        feature
        for feature in geo_json["features"]
        if feature["properties"]["adm_cd"] in code_list
    ]
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=["adm_nm"],
            labels=False,
        )
    )

    colors = [
        "#{:02x}{:02x}{:02x}".format(*[random.randint(0, 255) for i in range(3)])
        for j in range(len(df))
    ]
    color_dict = {code: color for code, color in zip(code_list, colors)}

    def style_function(x):
        return {
            "fillColor": color_dict[x["properties"]["adm_cd"]],
            "lineOpacity": 0.5,
            "fillOpacity": 0.6,
            "weight": 1.5,
            "color": "white",
            "dashArray": "2",
        }

    def highlight_function(x):
        return {"lineOpacity": 0.8, "fillOpacity": 0.8}

    choropleth.geojson.add_child(
        folium.GeoJson(
            geo_json,
            style_function=style_function,
            highlight_function=highlight_function,
        )
    )

    for key in choropleth._children:
        if key.startswith("color_map"):
            del choropleth._children[key]

    choropleth.add_to(map)

    st_map = st_folium(map, width=1400, height=500)

    return st_map, df


def get_description(st_map, df):
    hjd_name = ""
    if st_map["last_active_drawing"]:
        hjd_code = st_map["last_active_drawing"]["properties"]["adm_cd"]
        hjd_name = df[df["행정동코드"] == hjd_code]["행정동"].values[0]
    return hjd_name


def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.subheader(APP_TITLE)
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 3rem;
                padding-bottom: 2rem;
            }
            [data-testid="stSidebar"]{
                min-width: 10rem;
                max-width: 15rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with open("seoul_geojson.json", "r") as read:
        geo_json = json.load(read)
    df = pd.read_csv("레히오나.csv", dtype={"행정동코드": object})
    df["행정동코드"] = df["행정동코드"].apply(lambda x: x[:-1])
    gu_list = sorted(list(df["시군구"].unique()))

    gu_name = st.sidebar.selectbox("군/구", ["---전체---"] + gu_list, index=1)

    st_map, df = display_map(df, geo_json, gu_name)

    hjd_name = get_description(st_map, df)

    if hjd_name != "":
        st.subheader(hjd_name)
        st.write(df[df["행정동"] == hjd_name]["요약 스토리"].values[0])
        st.write(df[df["행정동"] == hjd_name]["외식업 스토리"].values[0])
        st.write(df[df["행정동"] == hjd_name]["소매업 스토리"].values[0])
        st.write(df[df["행정동"] == hjd_name]["인구 스토리"].values[0])


if __name__ == "__main__":
    main()
