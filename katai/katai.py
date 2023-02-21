import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from geopy.distance import geodesic
from datetime import timedelta as td

#1.title
st.header("Airport Distance")
st.subheader("2つの空港は経緯度によって、距離を計算できる")

#2.gif
file_ = open("2.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="2 gif">',
    unsafe_allow_html=True,
    )



#3.password
st.markdown("    ")
st.markdown("    ")

st.markdown("##### 6桁のパスワードを入力してください ")
password = st.text_input("")
action_button = st.button('確認')

# if action_button == True and password =="123456":
#     st.write('go on')
# else:
#     st.stop()
    
    #st.write('ボタンをクリックしてください') 
if password != "123456":
    #st.text("パスワードが間違っています。再入力してください")
    st.stop()
    
    
    
    
    
#4.distanceを計算
#from math import radians, sin, cos, atan2, sqrt
def haversine_distance(long1, lat1, long2, lat2, degrees=False):
    TokyoStation = (lat1, long1)
    NagoyaStation = (lat2, long2)

    dis = geodesic(TokyoStation, NagoyaStation).km

    return dis

        # # 角度 vs ラジアン
        # if degrees:
        #     long1 = radians(long1)
        #     lat1 = radians(lat1)
        #     long2 = radians(long2)
        #     lat2 = radians(lat2)
        # # 半正弦計算距離式
        # a = sin((lat2 - lat1) / 2)**2 + cos(lat1) * cos(lat2) * sin((long2 - long1)/2)**2
        # b = 2 * atan2(sqrt(a), sqrt(1-a))
        # distance = 6378.137 * b # 単位：km
        # return distance

       
#データを読み込み
df = pd.read_csv("./airport.csv",encoding='shift-jis')
st.map(df)
airport_code1 = st.selectbox("空港番号を選択してください: ",
                            df['Airport Code'].unique())
airport_code2 = st.selectbox(" ",
                            df['Airport Code'].unique())



def get_distances(df, airport_code1="CDG",airport_code2="CHC"):
        
    temp_df = df[df['Airport Code']==airport_code1]
    temp_lat1 = temp_df['lat'].values[0] 
    temp_long1 = temp_df['lon'].values[0] 
    st.write("空港番号: {}, 経度: {}, 緯度:  {}".format(airport_code1, temp_long1, temp_lat1))
   
   
    others_df = df[df['Airport Code']!=airport_code1]
    temp_df = df[df['Airport Code']==airport_code2]
    temp_lat2 = temp_df['lat'].values[0] 
    temp_long2 = temp_df['lon'].values[0] 
    st.write("空港番号:{}, 経度: {}, 緯度: {}".format(airport_code2, temp_long2, temp_lat2))
    test_distance = haversine_distance(long1=temp_long1, long2=temp_long2, lat1=temp_lat1, lat2=temp_lat2)
    st.write("2 点間の距離は：", round(test_distance,2),"km")
    st.write("飛行機の平均時速は500km/hのスピードを飛ぶとしたら",td(hours=round(test_distance/700,2)),"かかります。")
    
    others_df['distance'] = others_df.apply(lambda x: haversine_distance(long1=temp_long1,
                                                                         lat1=temp_lat1,
                                                                         long2=temp_long2,
                                                                         lat2=temp_lat2,
                                                                         degrees=True),
                                                                         axis=1)
    

    
    return others_df.sort_values('distance')

result_df = get_distances(df,airport_code1=airport_code1,airport_code2=airport_code2)



