from re import U
import streamlit as st
import pandas as pd
import altair as alt


@st.cache
def load_data():
    """
    Write 1-2 lines of code here to load the data from CSV to a pandas dataframe
    and return it.
    """
    return pd.read_csv("pulse39.csv")


@st.cache
def get_slice_membership(df, genders, races, educations, age_range):
    """
    Implement a function that computes which rows of the given dataframe should
    be part of the slice, and returns a boolean pandas Series that indicates 0
    if the row is not part of the slice, and 1 if it is part of the slice.

    In the example provided, we assume genders is a list of selected strings
    (e.g. ['Male', 'Transgender']). We then filter the labels based on which
    rows have a value for gender that is contained in this list. You can extend
    this approach to the other variables based on how they are returned from
    their respective Streamlit components.
    """
    labels = pd.Series([1] * len(df), index=df.index)
    if genders:
        labels &= df['gender'].isin(genders)
    if age_range:
        labels &= (df['age'] >= age_range[0]) & (df['age'] <= age_range[1])

    if races:
        labels &= df['race'] == races
    # ... complete this function for the other demographic variables
    return labels


def make_long_reason_dataframe(df, reason_prefix):
    """
    ======== You don't need to edit this =========

    Utility function that converts a dataframe containing multiple columns to
    a long-style dataframe that can be plotted using Altair. For example, say
    the input is something like:

         | why_no_vaccine_Reason 1 | why_no_vaccine_Reason 2 | ...
    -----+-------------------------+-------------------------+------
    1    | 0                       | 1                       | 
    2    | 1                       | 1                       |

    This function, if called with the reason_prefix 'why_no_vaccine_', will
    return a long dataframe:

         | id | reason      | agree
    -----+----+-------------+---------
    1    | 1  | Reason 2    | 1
    2    | 2  | Reason 1    | 1
    3    | 2  | Reason 2    | 1

    For every person (in the returned id column), there may be one or more
    rows for each reason listed. The agree column will always contain 1s, so you
    can easily sum that column for visualization.
    """
    reasons = df[[c for c in df.columns if c.startswith(reason_prefix)]].copy()
    reasons['id'] = reasons.index
    reasons = pd.wide_to_long(reasons, reason_prefix,
                              i='id', j='reason', suffix='.+')
    reasons = reasons[~pd.isna(reasons[reason_prefix])].reset_index().rename({
        reason_prefix: 'agree'}, axis=1)
    return reasons


# MAIN CODE


st.title("Household Pulse Explorable")
with st.spinner(text="Loading data..."):
    df = load_data()
st.text("Visualize the overall dataset and some distributions here...")

bar_chart = alt.Chart(df).mark_bar().encode(
    alt.Y("race", scale=alt.Scale(zero=False)),
    alt.X("count()"),
    tooltip=["education", "sexual_orientation"]
).properties(
    width=400,
    height=300
).interactive()

bar_chart2 = alt.Chart(df).mark_bar().encode(
    alt.X("count()"),
    alt.Y("education")
).properties(
    width=400,
    height=300
).interactive()
st.write(df)
st.altair_chart(bar_chart)
st.altair_chart(bar_chart2)

st.header("Custom slicing")
st.text("Implement your interactive slicing tool here...")

gender_options = st.multiselect("Select attributes", df['gender'].unique())

age_options = st.select_slider("Select age", df['age'].sort_values(
).unique(), value=(df['age'].min(), df['age'].max()))

race_option = st.radio("Select race", df['race'].unique())

slice_labels = get_slice_membership(
    df, gender_options, race_option, None, age_options)
vaccine_reasons_inslice = make_long_reason_dataframe(
    df[slice_labels], 'why_no_vaccine_')
vaccine_reasons_outslice = make_long_reason_dataframe(
    df[~slice_labels], 'why_no_vaccine_')
receive_vaccine = df[slice_labels]["received_vaccine"] == True
receive_vaccine_out = df[~slice_labels]["received_vaccine"] == True

button_clicked = st.button("Choose a random person")
st.write(button_clicked)

col1, col2 = st.columns(2)
with col1:
    sliced_df = df[slice_labels]
    st.metric("Percentage received vaccine (in slice)", round(
        receive_vaccine.sum() / sliced_df.shape[0] * 100, 2))
    
    mean_intention = sliced_df["vaccine_intention"].mean()

    st.metric("Mean intension (in slice)", round(mean_intention, 2))
    chart = alt.Chart(vaccine_reasons_inslice, title='In Slice').mark_bar().encode(
        y='sum(agree)',
        x='reason',
    ).properties(
        width=300,
        height=600
    ).interactive()
    st.write(chart)

with col2:
    sliced_df = df[~slice_labels]
    st.metric("Percentage received vaccine (out slice)", round(
        receive_vaccine_out.sum() / sliced_df.shape[0] * 100, 2))
    
    mean_intention = sliced_df["vaccine_intention"].mean()

    st.metric("Mean intension (out slice)", round(mean_intention, 2))
    chart2 = alt.Chart(vaccine_reasons_outslice, title='Out Slice').mark_bar().encode(
        y='sum(agree)',
        x='reason',
    ).properties(
        width=300,
        height=600
    ).interactive()
    st.write(chart2)

st.header("Person sampling")
st.text("Implement a button to sample and describe a random person here...")
