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

		file_contents.append([splitted[0], splitted[1], float(splitted[2].split()[0])])

	return file_contents 

def net_worth(df):
	Net_Worth_Table = df.groupby('Date')['Amount'].sum().reset_index(name ='sum')
	Net_Worth_Table['cumulative sum'] = Net_Worth_Table['sum'].cumsum()
	Net_Worth_Chart = go.Figure(
			data = go.Scatter(x = Net_Worth_Table["Date"], y = Net_Worth_Table["cumulative sum"]),
			)
	
	Net_Worth_Chart.update_layout(
		xaxis_title = "Date",
		yaxis_title = "Net Worth (Tenge)",
		)
	
	Net_Worth_Chart.update_xaxes(
		tickangle = 45
		)
	
	return Net_Worth_Chart

def w_exp(df):
	df = df[df.Amount < 0] 
	df.Amount = df.Amount*(-1) 
	
	Total_Expenses_Table = df.groupby('Date')['Amount'].sum().reset_index(name = 'sum')
	Total_Expenses_Chart = px.bar(Total_Expenses_Table, x = "Date", y = "sum")
	Total_Expenses_Chart.update_yaxes(title = 'Expenses (Tenge)', visible = True, showticklabels = True)
	Total_Expenses_Chart.update_xaxes(title = 'Date', visible = True, showticklabels = True)
	
	return Total_Expenses_Chart

def w_inc(df):
	df = df[df.Amount > 0] 
	
	Total_Incomes_Table = df.groupby('Date')['Amount'].sum().reset_index(name = 'sum')
	Total_Incomes_Chart = px.bar(Total_Incomes_Table, x = "Date", y = "sum")
	Total_Incomes_Chart.update_yaxes(title = 'Incomes (Tenge)', visible = True, showticklabels = True)
	Total_Incomes_Chart.update_xaxes(title = 'Date', visible = True, showticklabels = True)
	
	return Total_Incomes_Chart

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
			
		with st.beta_expander('Expenses'):
			st.header('Overall Time')
			st.plotly_chart(w_exp(df))
		
		with st.beta_expander('Incomes'):
			st.header('Overall Time')
			st.plotly_chart(w_inc(df))
			
if __name__ == '__main__':
	main()
