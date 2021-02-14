import streamlit as st
import pandas as pd
import csv

from datetime import datetime             
import plotly.express as px              
import plotly.graph_objects as go   

@st.cache(persist=True, allow_output_mutation=True)
def load_data(uploaded_file):        
	reader = csv.reader(uploaded_file, delimiter='|')
	file_contents = []
        
	for each in reader:
		if len(each) > 0:
			file_contents.append(each[0])		

	return file_contents

def net_worth(df):
	net_worth = df.groupby('Date')['Price'].sum().reset_index(name='sum')
	net_worth['cumulative sum'] = net_worth['sum'].cumsum()

	net_worth = go.Figure(data=go.Scatter(x=net_worth["Date"], y = net_worth["cumulative sum"]),
    							layout=go.Layout(title=go.layout.Title(text="Net Worth Over Time")
    							)
    						)

	net_worth.update_layout(
    	xaxis_title="Date",
    	yaxis_title="Net Worth (Tenge)",
    	hovermode='x unified'
    )

	net_worth.update_xaxes(tickangle=45)

	net_worth.show()

def main():
	st.title('MMM Statistics')
	st.markdown('Сайт создан для анализа MMM приложения')

	st.sidebar.subheader('Как экспортировать файл с данными?')	
	st.sidebar.text('1) Зайдите в МММ приложение')
	st.sidebar.text('2) File -> Export')
	st.sidebar.text('3) Загрузите сюда')

	uploaded_file = st.sidebar.file_uploader("", type=['csv'])

	st.sidebar.markdown('For STEP 😊')

	if uploaded_file is not None:
		df = pd.read_csv(uploaded_file, sep='|')

		with st.beta_expander('Net Worth'):
			st.header('Overall Time')
			st.plotly_chart(net_worth(df))
			
		with st.beta_expander('Облако слов'):			
			word_cloud = create_wc(texts, form)

			fig, ax = plt.subplots()

			ax.imshow(word_cloud, interpolation='bilinear')
			ax.axis("off")

			st.pyplot(fig)


if __name__ == '__main__':
	main()
