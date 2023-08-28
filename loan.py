import streamlit as st
import pandas as pd
import plotly.express as px
template = 'plotly'
# Function to calculate loan data
def loan_amount(principal, rate, term):
    # Calculate monthly interest rate
    monthly_rate = rate / 12
    # Calculate monthly payment using the formula assuming linear payments
    monthly_payment = int((principal * monthly_rate) / (1 - (1 + monthly_rate) ** (-term)))
    #monthly_payment = monthly_payment.style.format("{:.2}")
    
    # Initialize remaining principal and total amount
    remaining_principal = principal
    total_amount = 0
    # Initialize data frame
    data = pd.DataFrame()
    # Iterate over loan term and calculate some values for each month
    for month in range(1, term + 1):
        # Calculate interest amount
        interest_amount = int(remaining_principal * monthly_rate)
        # Calculate principal amount
        principal_amount = monthly_payment - interest_amount
        # Update remaining principal and total amount
        remaining_principal = remaining_principal - principal_amount
        total_amount = total_amount + monthly_payment
        # Print the result
        data_one_iter = pd.DataFrame({
            'month': [month],
            'interest_amount': [interest_amount],
            'remaining_principal': [remaining_principal],
            'total_amount': [total_amount]})
        data = pd.concat([data, data_one_iter], ignore_index=True)
    data['interest_monthly_ratio'] = data['interest_amount'] / monthly_payment
    data.index = data.month
    data=data.drop("month",axis = 1)
    
    
    
    return data, total_amount,monthly_payment
st.title('Loan Calculation')
col1, col2, col3 = st.columns(3)
with col1:
    principal = st.slider('Principal amount',min_value=0, value=5000000)
with col2:  
    interest_rate = st.slider('Interest rate', min_value=0.000, value=10.000)
with col3:
    term = st.slider('Term (in months)', min_value=0, value=120)
data, total_amount, monthly_payment = loan_amount(principal, interest_rate, term)


#fig_remining_principal = px.line(data, x='month', y='remaining_principal', template=template)
#fig_interest_payed = px.line(data, x='month', y=['interest_amount', 'monthly_payment'], template=template)
#fig_interest_payment_ratio = px.line(data, x='month', y='interest_monthly_ratio', template=template)
st.write('Monthly installment: ', monthly_payment)
st.write('Total amount payed at the end of the loan period: ', (total_amount))
show_brake_down = st.checkbox('Show loan breakdown per month')
if show_brake_down:
    st.markdown('## Loan breakdown per month')
    st.dataframe(data)
    # create download button with streamlit, donload the data frame as csv file
    st.download_button(label='Download data', data=data.to_csv(index=False), file_name='loan_breakdown.csv', mime='text/csv')
    
    #st.write(monthly_payment)
    
    st.write(data.style.format("{:.2}"))
    
    fig = px.pie(
    hole = 0.2,labels = data.values(),names = data.keys())
#st.header("Donut chart")
#st.plotly_chart(fig)
    



