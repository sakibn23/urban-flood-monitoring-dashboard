from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
import streamlit as st
import plotly.express as px
from pymongo import MongoClient
import certifi

st.set_page_config(page_title="Urban Flood Monitoring",page_icon="🌧️",layout="wide")
st.title("🌧️ Urban Flood Risk & Rainfall Monitoring")
st.caption("Environmental IoT analytics prototype | Cloud data via Azure Cosmos DB (MongoDB API)")

@st.cache_resource
def get_collection():
    uri=os.getenv("MONGODB_URI")
    if not uri:
        raise ValueError("MONGODB_URI environment variable is not set.")
    client = MongoClient(
    uri,
    serverSelectionTimeoutMS=10000,
    tlsCAFile=certifi.where()
)
    client.admin.command("ping")
    db = client[os.getenv("MONGODB_DATABASE", "urban_flood_db")]
    return db[os.getenv("MONGODB_COLLECTION", "flood_observations")]

try:
    collection=get_collection()
    raw=list(collection.find({},{"_id":0}))
except Exception as exc:
    st.error("Unable to connect to Azure database.")
    st.error(f"Error type: {type(exc).__name__}")
    st.error(f"Error code: {getattr(exc, 'code', None)}")
    st.stop()


if not raw:
    st.warning("The collection is empty. Import flood_observations.json first.")
    st.stop()

df=pd.json_normalize(raw)
df["timestamp"]=pd.to_datetime(df["timestamp"],errors="coerce")
df["rainfall_mm"]=pd.to_numeric(df["measurements.rainfall_mm"],errors="coerce")
df["water_level_m"]=pd.to_numeric(df["measurements.water_level_m"],errors="coerce")
df["soil_moisture_pct"]=pd.to_numeric(df["measurements.soil_moisture_pct"],errors="coerce")
df["temperature_c"]=pd.to_numeric(df["measurements.temperature_c"],errors="coerce")
df["humidity_pct"]=pd.to_numeric(df["measurements.humidity_pct"],errors="coerce")
df["zone"]=df["location.zone"]
df["latitude"]=df["location.latitude"]
df["longitude"]=df["location.longitude"]

with st.sidebar:
    st.header("Filters")
    zones=sorted(df["zone"].dropna().unique())
    selected_zones=st.multiselect("Monitoring zones",zones,default=zones)
    risk_options=["Low","Moderate","High"]
    selected_risk=st.multiselect("Risk level",risk_options,default=risk_options)
    start_date=df["timestamp"].min().date()
    end_date=df["timestamp"].max().date()
    dates=st.date_input("Date range",value=(start_date,end_date),min_value=start_date,max_value=end_date)

filtered=df[df["zone"].isin(selected_zones)&df["risk_level"].isin(selected_risk)].copy()
if isinstance(dates,tuple) and len(dates)==2:
    filtered=filtered[(filtered["timestamp"].dt.date>=dates[0])&(filtered["timestamp"].dt.date<=dates[1])]
if filtered.empty:
    st.info("No observations match the selected filters.")
    st.stop()

latest=filtered.sort_values("timestamp").groupby("sensor_id",as_index=False).tail(1)
high=filtered[filtered["risk_level"]=="High"]
active_sensors=filtered[filtered["sensor_status"]=="Active"]["sensor_id"].nunique()
c1,c2,c3,c4=st.columns(4)
c1.metric("Observations",f"{len(filtered):,}")
c2.metric("Avg rainfall",f"{filtered['rainfall_mm'].mean():.2f} mm")
c3.metric("Peak water level",f"{filtered['water_level_m'].max():.2f} m")
c4.metric("High-risk observations",f"{len(high):,}")

st.subheader("Rainfall and water-level trends")
trend=filtered.set_index("timestamp").resample("D")[["rainfall_mm","water_level_m"]].mean().reset_index()
left,right=st.columns(2)
with left:
    st.plotly_chart(px.line(trend,x="timestamp",y="rainfall_mm",title="Daily average rainfall",labels={"timestamp":"Date","rainfall_mm":"Rainfall (mm)"}),use_container_width=True)
with right:
    st.plotly_chart(px.line(trend,x="timestamp",y="water_level_m",title="Daily average water level",labels={"timestamp":"Date","water_level_m":"Water level (m)"}),use_container_width=True)

st.subheader("Zone-level monitoring")
left,right=st.columns(2)
zone_metrics=filtered.groupby("zone",as_index=False).agg(avg_rainfall=("rainfall_mm","mean"),max_water=("water_level_m","max"),high_risk=("risk_level",lambda s:(s=="High").sum()))
with left:
    st.plotly_chart(px.bar(zone_metrics.sort_values("avg_rainfall",ascending=False),x="zone",y="avg_rainfall",title="Average rainfall by zone",labels={"zone":"Zone","avg_rainfall":"Rainfall (mm)"}),use_container_width=True)
with right:
    st.plotly_chart(px.bar(zone_metrics.sort_values("high_risk",ascending=False),x="zone",y="high_risk",title="High-risk observations by zone",labels={"zone":"Zone","high_risk":"High-risk observations"}),use_container_width=True)

st.subheader("Monitoring sensor map")
map_df=latest[latest["sensor_status"]=="Active"].copy()
if not map_df.empty:
    map_df["marker_size"]=map_df["water_level_m"].clip(lower=0.2)
    st.plotly_chart(px.scatter_geo(map_df,lat="latitude",lon="longitude",color="risk_level",size="water_level_m",hover_name="zone",hover_data={"sensor_id":True,"rainfall_mm":True,"water_level_m":True,"latitude":False,"longitude":False},projection="mercator",title="Latest selected sensor observation by location"),use_container_width=True)
else:
    st.info("No active sensor observations are available for the selected filter.")

st.subheader("Environmental indicator relationships")
st.plotly_chart(px.scatter(filtered,x="rainfall_mm",y="water_level_m",color="risk_level",hover_data=["zone","timestamp"],title="Rainfall and water-level relationship",labels={"rainfall_mm":"Rainfall (mm)","water_level_m":"Water level (m)"}),use_container_width=True)

st.subheader("High-risk observations")
alerts=filtered[filtered["risk_level"]=="High"].sort_values("timestamp",ascending=False)
st.dataframe(alerts[["timestamp","sensor_id","zone","rainfall_mm","water_level_m","soil_moisture_pct","sensor_status","risk_level"]],use_container_width=True)
st.download_button("Download filtered observations (CSV)",filtered.drop(columns=["location","measurements"],errors="ignore").to_csv(index=False),file_name="flood_monitoring_filtered.csv",mime="text/csv")

st.caption("Synthetic educational dataset. Risk categories are illustrative rules, not operational flood warnings or validated hydrological predictions.")
