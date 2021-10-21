import streamlit as st
import plotly.express as px
import pandas as pd
from functools import reduce

df=pd.read_csv("ALL_AMAN.csv")
df['Date']=pd.to_datetime(df['Date'])
df['Period']=df['Date'].dt.strftime("%b-%Y")
# df['Month']=df['Date'].dt.month
# df['year']=df['Date'].dt.year
# df['Period']=df.Month.astype(str)+"-"+df.year.astype(str)
# df['Period']=pd.to_datetime(df['Period'])
print(df.head())

df1=df[['Period','order_completed','order_amount']]
df11=df1[df1['order_completed']=='No'].groupby('Period').agg(total_amount_lost=('order_amount',sum))
df11=df11.reset_index()
df11=df11.sort_values(by='Period',ascending=False)
print(df11)
df12=df1[df1['order_completed']=='Yes'].groupby('Period').agg(total_amount_charged=('order_amount',sum))
df12=df12.reset_index()
df12=df12.sort_values(by='Period',ascending=False)
print(df12)

# join the tables
merge1=[df11,df12]
merging1=reduce(lambda left,right:pd.merge(left,right,on=['Period'],how='outer'),merge1)
print(merging1)
# extract a value from a column
sep_value=merging1['total_amount_lost'].values[0]
sep_value=int(sep_value)
oct_value=merging1['total_amount_lost'].values[1]
oct_value=int(oct_value)
nov_value=merging1['total_amount_lost'].values[2]
nov_value=int(nov_value)
dec_value=merging1['total_amount_lost'].values[3]
dec_value=int(dec_value)

sep_value1=merging1['total_amount_charged'].values[0]
sep_value1=int(sep_value1)

oct_value1=merging1['total_amount_charged'].values[1]
oct_value1=int(oct_value1)

nov_value1=merging1['total_amount_charged'].values[2]
nov_value1=int(nov_value1)

dec_value1=merging1['total_amount_charged'].values[3]
dec_value1=int(dec_value1)
# create the first chart
st.sidebar.subheader("Total Charges Vs Total Lost amount")
selectbox1= st.sidebar.selectbox("Select Period",merging1['Period'].unique())
col1,col2,col3=st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    st.subheader("Total Amount Billed Vs Total Amount Lost")
with col3:
    st.write("")

col1,col2=st.columns(2)
with col1:
    if selectbox1 =='Sep-2021':
        st.subheader("Total amount Lost in Sept-2021")
        st.metric("Amount Lost: $",  sep_value)
    elif selectbox1 =='Oct-2021':
        st.subheader("Total amount Lost in Oct-2021")
        st.metric("Amount Lost: $",oct_value)
    elif selectbox1=='Nov-2021':
        st.subheader("Total amount Lost in Nov-2021")
        st.metric("Amount Lost: $",nov_value)
    else:
        st.subheader("Total amount Lost in Dec-2021")
        st.metric("Amount Lost: $",dec_value)



with col2:
    if selectbox1=='Sep-2021':
        st.subheader("Total amount charged in Sep-2021")
        st.metric("Amount Billed $:",sep_value1)
    elif selectbox1=='Oct-2021':
        st.subheader("Total amount charged in Oct-2021")
        st.metric("Amount Billed $:", oct_value1)
    elif selectbox1=='Nov-2021':
        st.subheader("Total amount charged in Nov-2021")
        st.metric("Amount Billed $:", nov_value1)
    else:
        st.subheader("Total amount charged in dec-2021")
        st.metric("Amount Billed $:",dec_value1)


# chart Number 2 filter by department and filter by period

df2=df[['Period','Department','order_completed','order_amount']]
df3=df2[df2['order_completed']=='Yes']
df4=df2[df2['order_completed']=='No']

st.sidebar.subheader("Lost Encounters by Department and Period")
selectbox2=st.sidebar.selectbox("Select Department",df2.Department.unique())
# yes table
data1=df3[df3['Department']==selectbox2]

col1,col2=st.columns(2)

with col1:
        st.subheader("Radiology Revenues billed")
        fig1 = px.histogram(data1, x='Period', y='order_amount', width=400, color='Period')
        st.plotly_chart(fig1)

data2=df4[df4['Department']==selectbox2]
with col2:
        st.subheader("Radiology Lost Revenues")
        fig2=px.histogram(data2,x='Period',y='order_amount',width=400,color="Period")
        st.plotly_chart(fig2)


# chart 3
df5=df[['order_completed','procedure_time','ordered_test']]
df5_1=df5[df5['order_completed']=='Yes']
df5_1=df5_1.drop('order_completed',axis=1)
df5_1['procedure_time']=pd.to_datetime(df5_1['procedure_time'])
df5_1['hour']=df5_1['procedure_time'].dt.hour
df5_1=df5_1.drop('procedure_time',axis=1)
df6=df5_1[(df5_1['ordered_test']=='CT') | (df5_1['ordered_test']=='X-Ray ')]
df7=df6[df6['ordered_test']=='CT'].groupby('hour').agg(CT=('hour','count'))
df7=df7.reset_index()
df8=df6[df6['ordered_test']=='X-Ray '].groupby('hour').agg(X_Ray=('hour','count'))
df8=df8.reset_index()
print(df8)

merge2=[df7,df8]
merging2=reduce(lambda left,right:pd.merge(left,right,on=['hour'],how='outer'),merge2)
merging2=merging2.fillna(0)
print(merging2)
st.subheader("Radiology Orders by day time")
# when in y , we use list, then we have to add barmode.
fig3=px.histogram(merging2,x='hour',y=['CT','X_Ray'],barmode='group')
st.plotly_chart(fig3)

# chart 4 - map

df9=df[['patient_number ','procedure_time','latitude','longitude']]
df9['procedure_time']=pd.to_datetime(df9['procedure_time'])
df9['hour']=df9['procedure_time'].dt.hour
df9=df9.drop('procedure_time',axis=1)
print(df9)
st.sidebar.subheader("Map Plot")
slider=st.sidebar.slider("Select the hour",1,23,9)
df10=df9[df9['hour']==slider]
st.markdown("%i patients presented to AMAN betwee %i:00 and %i00" %(len(df10),slider,(slider+3)%24))
st.map(df10)


#chart 5

df13=df[['Period','chief_complaint','Department']]
selectbox3= st.sidebar.selectbox("Select Department",df13['Period'].unique(),key='13')
data3=df13[df13['Period']==selectbox3]
fig4=px.histogram(data3,x='Department',y='chief_complaint',facet_col='chief_complaint',histfunc='count',color='chief_complaint')
st.plotly_chart(fig4)
print(df13)

# chart 6
import datetime
t=st.time_input("please pick the time",datetime.time(8,45))
st.write(f"alarm is set on {t}")

s=st.date_input("pick a date",datetime.date(1979,6,21))
st.write(s)

# chart 7

# df14=df[['ordering_physician','Period','order_description']]
# df14['count']=df14.groupby('Period')['order_description'].transform('count')
# print(df14)
# selectbox4= st.sidebar.selectbox("select order test",df14['order_description'].unique(),key='15')
# multi = st.sidebar.multiselect('select physician name',df14.ordering_physician.unique())
# data = df14[df14['order_description']==selectbox4]
# data1=data[data['ordering_physician']==multi]

# chart 8

df15=df[['nationality','Period']]
print(df15)
multi = st.sidebar.multiselect("Select Nationality",df15['nationality'].unique())
if len(multi)>0:
    data4=df15[df15['nationality'].isin(multi)]
    fig5=px.histogram(data4,x='Period',y='nationality',histfunc='count',facet_col='nationality',color='nationality')
    st.plotly_chart(fig5)

# line chart
df16=df[['Period','ordering_physician','order_completed','order_amount','ordered_test']]
dfism=df16[(df16['order_completed']=='No')&( df16['ordering_physician']=='Dr_H_Ismaeel ')].groupby(['ordered_test','Period'],as_index=False).agg(Dr_Hussain_not_done=('order_amount',sum))
print(dfism)

dfism1=dfism[dfism['ordered_test']=='CBC'].groupby('Period',as_index=False).agg(Dr_Huss_CBC_not_done=('Dr_Hussain_not_done',sum))
print(dfism1)

dfism2=dfism[dfism['ordered_test']=='CT'].groupby('Period',as_index=False).agg(Dr_Huss_CT_not_done=('Dr_Hussain_not_done',sum))
print(dfism2)

dfism3=dfism[dfism['ordered_test']=='TSH'].groupby('Period',as_index=False).agg(Dr_Huss_TSH_not_done=('Dr_Hussain_not_done',sum))
print(dfism3)

dfism4=dfism[dfism['ordered_test']=='X-Ray '].groupby('Period',as_index=False).agg(Dr_Huss_X_Ray_not_done=('Dr_Hussain_not_done',sum))
print(dfism4)

merge3=[dfism1,dfism2,dfism3,dfism4]
merging3= reduce(lambda left,right:pd.merge(left,right , on =['Period'],how='outer'),merge3)
merging3=merging3.fillna(0)
print(merging3)

selectbox4= st.sidebar.selectbox("Select Test",['CBC','CT','TSH','X_Ray'])

if selectbox4=='CBC':
    fig6=px.line(merging3,x='Period',y='Dr_Huss_CBC_not_done')
    st.plotly_chart(fig6)
elif selectbox4=='CT':
    fig7=px.line(merging3,x='Period',y='Dr_Huss_CT_not_done')
    st.plotly_chart(fig7)
elif selectbox4=='TSH':
    fig8=px.line(merging3,x='Period',y='Dr_Huss_not_done')
    st.plotly_chart(fig8)
else:
    fig9=px.line(merging3,x='Period',y='Dr_Huss_X_Ray_not_done')
    st.plotly_chart(fig9)


# expander
from PIL import Image
image = Image.open("C:/Users/j.elachkar/Desktop/diab.PNG")
with st.expander("see explanation"):
    st.write("that is a nice feature")
    st.image(image,caption='nice pic')
