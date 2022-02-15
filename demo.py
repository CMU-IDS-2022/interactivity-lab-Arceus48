import streamlit as st
import pandas as pd
import altair as alt

st.header("My first streamlit app")
st.write("Hello world")

@st.cache
def load(url):
    return pd.read_json(url)

df = load("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/penguins.json")

if st.checkbox("Show data"):
    st.write(df)

scatter = alt.Chart(df).mark_point().encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species")
)

# st.write(scatter)

# picked = alt.selection_single(empty="none", on="mouseover")
# picked = alt.selection_multi(empty="none", on="mouseover")
# picked = alt.selection_interval(encodings=["y"])
# Split all penguins based on all fields given

# input_dropdown = alt.binding_select(options=["Adelie", "Chinstrap", "Gentoo"], name="Species of penguins ")
# picked = alt.selection_single(encodings=["color"], bind=input_dropdown)

brush = alt.selection_interval(encodings=["x"])

scatter = alt.Chart(df).mark_circle(size=100).encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species")
    # color = alt.condition(picked, "Species", alt.value("lightgray"))
).add_selection(brush)


hist = alt.Chart(df).mark_bar().encode(
    alt.X("Body Mass (g)", bin=True),
    alt.Y("count()"),
    alt.Color("Species")
).transform_filter(brush)

st.write(scatter & hist)

# scales = alt.selection_interval(bind="scales")

# st.write(scatter.add_selection(scales))

# min_weight = st.slider("Minimum Body Mass", 2500, 6500)
# st.write(min_weight)

# scatter_filter = scatter.transform_filter(f"datum['Body Mass (g)'] >= {min_weight}")
# st.write(scatter_filter)