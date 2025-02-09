import streamlit as st
import pandas as pd
import numpy as np

from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query("SELECT * FROM `modern-water-402010.neobank_Gold_Tier.unique_customers_mart` LIMIT 100")
st.dataframe(rows)

moving_average = run_query("SELECT * FROM `modern-water-402010.neobank_Gold_Tier.moving_avg_trx_mart` LIMIT 1000")
chart_data = pd.DataFrame(moving_average, columns=["year", "month", "moving_avg"])

selected_year = st.sidebar.selectbox("Select Year", chart_data['year'].unique())

filtered_data = chart_data[chart_data['year'] == selected_year]
#chart_data['date'] = chart_data['year'] + chart_data['month']
filtered_data = filtered_data[['month', 'moving_avg']]
monthly_sum = filtered_data.groupby('month')['moving_avg'].sum()
st.line_chart(monthly_sum)



def plot_line_chart(moving_average):
    device_counts = moving_average['month'].value_counts()
    st.line_chart(device_counts)


# Print results.
st.write("Some wise words from Shakespeare:")
#for row in rows:
#    st.write("✍️ " + row['word'])

import streamlit as st
import pandas as pd
import numpy as np

from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)



# Function to plot bar chart using Streamlit
def plot_bar_chart(df):
    device_counts = df['Device_Type'].value_counts()
    st.bar_chart(device_counts)

# Function to plot bar chart for total users per country
def plot_country_bar_chart(df):
    country_counts = df['Country'].value_counts().sort_values(ascending=False)
    st.bar_chart(country_counts)

def finance_dashboard():
    st.markdown("## Unique users per device type")
    plot_bar_chart(df_device)

def marketing_dashboard():
    st.markdown("## Total users per country")
    plot_country_bar_chart(df_country)

# Generate demo data for device type
np.random.seed(0)
data_device = {
    'User_ID': np.arange(1000),
    'Device_Type': np.random.choice(['Desktop', 'Mobile', 'Tablet'], size=1000)
}
df_device = pd.DataFrame(data_device)

# Generate demo data for country
np.random.seed(0)
data_country = {
    'User_ID': np.arange(1000),
    'Country': np.random.choice(['USA', 'UK', 'Canada', 'Australia', 'Germany'], size=1000)
}
df_country = pd.DataFrame(data_country)

# Main Streamlit app
def main():
    st.sidebar.title('Departments')
    department = st.sidebar.radio('Select Department', ['Finance', 'Marketing'])

    if department == 'Finance':
        plot_line_chart()
    elif department == 'Marketing':
        marketing_dashboard()
        finance_dashboard()

if __name__ == "__main__":
    main()
