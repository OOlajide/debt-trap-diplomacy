import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from millify import millify

st.set_page_config(
    page_title="Debt Trap Diplomacy",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": None,
        "Report a bug": "https://twitter.com/sageOlamide",
        "About": None
    }
)

#style metric containers
st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: #c8d7db;
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: #b0020d;
}
</style>
"""
            , unsafe_allow_html=True)
  
st.markdown(f'<h1 style="color:#d1cc2c;font-size:60px;text-decoration:underline;text-align:center;">{"Debt Trap Diplomacy: A Tale Of China & Africa"}</h1>', unsafe_allow_html=True)

st.header("Intro")
st.markdown("""---""")

text_1 = '<p style="font-family:sans-serif; color:#48b0ae; font-size: 20px;">Debt-trap diplomacy is an international financial relationship where a creditor country or institution extends debt to a borrowing nation partially, or solely, to increase the lender\'s political leverage. The creditor country is said to extend excessive credit to a debtor country with the intention of extracting economic or political concessions when the debtor country becomes unable to meet its repayment obligations. The conditions of the loans are often not publicized. The borrowed money commonly pays for contractors and materials sourced from the creditor country.<a href="https://en.wikipedia.org/wiki/Debt-trap_diplomacy">[SOURCE]</a></p>'

text_2 = '<p style="font-family:sans-serif; color:#48b0ae; font-size: 20px;">The aim of this dashboard is to analyze Chinese debt to African countries.</p>'

text_3 = '<p style="font-family:sans-serif; color:#48b0ae; font-size: 20px;">The data used for this dashboard is <a href="https://www.kaggle.com/datasets/ramjasmaurya/chinese-debt-trap">Ram Jas\' Chinese debt trap dataset</a>, the dataset consists of loans from Chinese entities to African countries between <b>2000 - 2020</b>. The dashboard is hosted on <a href="https://replit.com/">Replit</a>, the repo is available <a href="https://replit.com/@OOlajide/debt-trap-diplomacy">here</a>.</p>'

st.markdown(text_1, unsafe_allow_html=True)
st.markdown(text_2, unsafe_allow_html=True)
st.markdown(text_3, unsafe_allow_html=True)

st.markdown("""---""")
st.header("Visualizations")
st.markdown("""---""")

df = pd.read_csv("data/africa.csv")

# Function to convert allocation to amount
def allocation_to_amount(allocation):
    # Remove '$' and the suffix
    amount_str = allocation[1:-1]
    # Remove commas and convert to float
    amount = float(amount_str.replace(',', ''))
    if allocation.endswith('B'):
        amount *= 1e9  # 1 billion
    elif allocation.endswith('M'):
        amount *= 1e6  # 1 million
    return int(amount)

# Apply the function to create the 'Amount' column
df['Amount'] = df['$ Allocation'].apply(allocation_to_amount)
df.drop(['S.no', '$ Allocation'], axis=1, inplace=True)
df.rename(columns={'Project': 'project', 'Year': 'year', 'Lender': 'lender', 'Country': 'country',
                   'Invested On': 'sector', 'Amount': 'amount_usd'}, inplace=True)

col_1, col_2, col_3 = st.columns(3)
with col_1:
    st.metric("Total Amount (USD) Lent", millify(df['amount_usd'].sum()))
with col_2:
    st.metric("Total African Countries Lent", millify(df['country'].nunique()))
with col_3:
    st.metric("Total Chinese Lenders", millify(df['lender'].nunique()))

col_4, col_5 = st.columns(2)
with col_4:
    st.metric("Maximum Amount (USD) Lent", millify(df['amount_usd'].max()))
with col_5:
    st.metric("Minimum Amount (USD) Lent", millify(df['amount_usd'].min()))

df_1 = df.groupby(['country'], as_index=False)['amount_usd'].agg('sum')
df_1 = df_1.sort_values(by=['amount_usd'], ascending=False)
iso = ['AGO', 'ETH', 'ZMB', 'KEN', 'EGY', 'NGA', 'CMR', 'ZAF', 'COG', 'GHA',\
       'SDN', 'CIV', 'UGA', 'ZWE', 'GNQ', 'GIN', '', 'MOZ', 'COD', 'TZA',\
       'SEN', 'GAB', 'DJI', 'MAR', 'BWA', 'TCD', 'SLE', 'MLI', 'NER', 'TGO',\
       'MRT', 'ERI', 'RWA', 'MUS', 'BEN', 'NAM', 'MDG', 'SSD', 'MWI', 'LSO',\
       'CAF', 'BFA', 'TUN', 'BDI', 'COM', 'LBR', 'CPV', 'SYC', 'GMB', 'DZA']
df_1['iso'] = iso

map_fig_1 = px.choropleth(df_1, locations="iso",
                    scope='africa',
                    color="amount_usd",
                    hover_name="country",
                    color_continuous_scale=px.colors.sequential.Plasma_r,
                    title='African Countries By Total Volume (USD) Of Debt Owed Chinese Entities Between (2000 - 2020)')
map_fig_1.update_layout(margin=dict(l=30, r=30, b=30, t=30))
st.plotly_chart(map_fig_1, theme="streamlit", use_container_width=True)

iso_dict = dict(zip(df_1['country'], df_1['iso']))
df_2 = df
df_2['country_iso'] = df_2['country']
df_2 = df_2.replace({"country_iso": iso_dict})
df_2 = df_2.sort_values('year')

map_fig_2 = px.choropleth(
  df_2,
  locations="country_iso",
  color="amount_usd",
  scope='africa',
  hover_name="country",
  animation_frame="year",
  title = "Yearly Volume (USD) Of Debt Owed Chinese Entities By African Countries",
  color_continuous_scale=px.colors.sequential.Plasma_r)
updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])]
st.plotly_chart(map_fig_2, theme="streamlit", use_container_width=True)

fig_1 = px.histogram(df, x="year", y="amount_usd", title="Yearly Debt Volume (USD) From China To Africa", barmode='group')
fig_1.update_layout(bargap=0.2, hovermode="x unified")
st.plotly_chart(fig_1, theme="streamlit", use_container_width=True)

df_pie_1 = df
df_pie_1 = df_pie_1.groupby(['country'], as_index=False)['amount_usd'].agg('sum')
fig_2 = px.pie(df_pie_1, values='amount_usd', names='country', title='Share Of Debt By Country',
              hover_data={
                "amount_usd": ':,d'
              })
fig_2.update_layout(margin=dict(t=30, b=30, l=30, r=30))
st.plotly_chart(fig_2, theme="streamlit", use_container_width=True)


df_pie_2 = df
df_pie_2 = df_pie_2.groupby(['lender'], as_index=False)['amount_usd'].agg('sum')
df_pie_2['lender'] = df_pie_2['lender'].str.slice(0,25)
fig_3 = px.pie(df_pie_2, values='amount_usd', names='lender', title='Share Of Debt By Lending Chinese Entity',
              hover_data={
                "amount_usd": ':,d'
              })
fig_3.update_layout(margin=dict(t=30, b=30, l=30, r=30))
st.plotly_chart(fig_3, theme="streamlit", use_container_width=True)

df_pie_3 = df
df_pie_3 = df_pie_3.groupby(['sector'], as_index=False)['amount_usd'].agg('sum')
fig_3 = px.pie(df_pie_3, values='amount_usd', names='sector', title='Share Of Debt By Investment Sector',
              hover_data={
                "amount_usd": ':,d'
              })
fig_3.update_layout(margin=dict(t=30, b=30, l=30, r=30))
st.plotly_chart(fig_3, theme="streamlit", use_container_width=True)

st.markdown("""---""")
st.header("Observations")
st.markdown("""---""")

st.markdown(
"""
- <p style="font-family:sans-serif; color:#b7bdc7; font-size: 16px;">Between 2000 and 2020, 50 African countries borrowed a total of $153B from 43 distinct Chinese entities, thats's an average of $3.06B borrowed per country.</p>
- <p style="font-family:sans-serif; color:#b7bdc7; font-size: 16px;">Angola alone borrowed $44.7B in that timeframe, accounting for 28% of the total $153B borrowed by African countries.</p>
- <p style="font-family:sans-serif; color:#b7bdc7; font-size: 16px;">The minimum amount borrowed at an instance was $1M while the maximum was $10B.</p>
- <p style="font-family:sans-serif; color:#b7bdc7; font-size: 16px;">Of all countries in Africa, only Libya and Somalia didn't borrow a single dollar from Chinese entities between 2000 and 2020.</p>
- <p style="font-family:sans-serif; color:#b7bdc7; font-size: 16px;">African countries borrowed more $ from Chinese entities in 2016 than any other year. They collectively borrowed $27.6B in 2016 alone, this represents 17% of the $153B borrowed between 2000 and 2020.</p>
- <p style="font-family:sans-serif; color:#b7bdc7; font-size: 16px;">Export–Import Bank of the Republic of China (CHEXIM) lent $84.9B in total between 2000 and 2020, this amounts to 55.6% of debt owed to Chinese entities by African countries.</p>
- <p style="font-family:sans-serif; color:#b7bdc7; font-size: 16px;">$44B (29%) of $ loans taken from Chinese entities between 2000 and 2020 was spent on transportation projects, rail transportaion majorly. This doesn't come as a surprise as Africa is lacking in that aspect and China is known to be a major exporter of rail technology. Power comes second with $38B (25%). Mining completes the top 3 with $17B (11.4%). This is anticipated considering China is known to have interest in African mineral resources, and has provided some <b>loan for mineral</b> concessions to some African countries in the past like <a href="https://www.reuters.com/article/zimbabwe-china-idUSL6N0NS5MG20140506">Zimbabwe</a> and <a href="https://www.reuters.com/article/guinea-mining-china-idUKL8N1LN4B8">Guinea</a>.</p>
""", unsafe_allow_html=True
)
st.markdown("""---""")

# - <p style="font-family:sans-serif; color:#b7bdc7; font-size: 16px;"></p>