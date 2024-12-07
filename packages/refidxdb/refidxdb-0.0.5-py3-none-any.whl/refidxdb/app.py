import re
from pathlib import Path

import plotly.graph_objects as go
import polars as pl
import streamlit as st

from refidxdb import databases

st.set_page_config(layout="wide")
st.title("RefIdxDB")

db = st.selectbox(
    "Database",
    list(databases.keys()),
)
cache_dir = databases[db]().cache_dir
files = [str(item) for item in Path(cache_dir).rglob("*") if item.is_file()]
if db == "refidx":
    files = [item for item in files if re.search(r"/data-nk", item)]
file = st.selectbox(
    "File",
    files,
    format_func=lambda x: "/".join(x.replace(cache_dir, "").split("/")[2:]),
)

logx = st.checkbox("Log x-axis", False)
logy = st.checkbox("Log y-axis", False)

with st.expander("Full file path"):
    st.write(file)

data = databases[db](file)
nk = data.nk.with_columns(pl.col("w").truediv(data.scale))

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=nk["w"],
        y=nk["n"],
        name="n",
    )
)
fig.add_trace(
    go.Scatter(
        x=nk["w"],
        y=nk["k"],
        name="k",
    )
)
fig.update_layout(
    xaxis=dict(
        title=f"Wavelength in {data.scale}",
        type="log" if logx else "linear",
    ),
    yaxis=dict(
        title="Values",
        type="log" if logy else "linear",
    ),
)
fig.update_traces(connectgaps=True)
st.plotly_chart(fig, use_container_width=True)
st.table(nk.select(pl.all().cast(pl.Utf8)))
