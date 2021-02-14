import streamlit as st
import pandas as pd
import plotly.express as px              
import plotly.graph_objects as go  

from datetime import datetime
from io import StringIO
from datetime import datetime             

@st.cache(persist=True, allow_output_mutation=True)
def load_data(data):        
	file_contents = []
	data = data.split('\r\n')
        
	for each in data:
		splitted = each.split(', ')

		file_contents.append([datetime.strptime(splitted[0], '%d/%m/%Y'), splitted[1], splitted[2].split()[0]])

	return file_contents 

def net_worth(df):
	net_worth = df.groupby('Date')['Price'].sum().reset_index(name='sum')
	net_worth['cumulative sum'] = net_worth['sum'].cumsum()

	net_worth = go.Figure(data=go.Scatter(x=net_worth["Date"], y=net_worth["cumulative sum"]))

	net_worth.update_layout(
    	xaxis_title="Date",
    	yaxis_title="Net Worth (Tenge)",
    	hovermode='x unified'
    )

	net_worth.update_xaxes(tickangle=45)

	net_worth.show()

def month_exp():
	df = df[df.Amount < 0] 
	df.Amount = df.amount*(-1) 

	Total_Monthly_Expenses_Table = df.groupby('Date')['amount'].sum().reset_index(name='sum')

	Total_Monthly_Expenses_Chart = px.bar(Total_Monthly_Expenses_Table, x = "year_month", y = "sum")
	Total_Monthly_Expenses_Chart.update_yaxes(title = 'Expenses (Tenge)', visible = True, showticklabels = True)
	Total_Monthly_Expenses_Chart.update_xaxes(title = 'Date', visible = True, showticklabels = True)
	Total_Monthly_Expenses_Chart.show()

def main():
	st.title('MMM Statistics')
	st.markdown('Сайт создан для анализа MMM приложения')

	st.sidebar.subheader('Как экспортировать файл с данными?')	
	st.sidebar.text('1) Зайдите в МММ приложение')
	st.sidebar.text('2) File -> Export')
	st.sidebar.text('3) Загрузите сюда')

	uploaded_file = st.sidebar.file_uploader("", type=['txt'])

	st.sidebar.markdown('For STEP 😊')

	if uploaded_file is not None:
		bytes_data = uploaded_file.read()
		
		stringio = StringIO(bytes_data.decode('utf-8'))
		
		raw_data = stringio.read()

		data = load_data(raw_data)

		df = pd.DataFrame(data, columns=['Date', 'Category', 'Amount'])

		with st.beta_expander('Net Worth'):
			st.header('Overall Time')
			st.plotly_chart(net_worth(df))
			
		with st.beta_expander('Month Expenses'):
			st.plotly_chart(month_exp(df))
			
if __name__ == '__main__':
	main()
