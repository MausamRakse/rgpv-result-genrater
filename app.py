import streamlit as st
import requests
import json
import random
import webbrowser
import time
import  cv2
from streamlit_lottie import st_lottie
from PIL import Image


## url of server
url='https://tough-novel-cattle.ngrok-free.app'
st.set_page_config(
    page_title="RESULT AUTOMATE APP",
    page_icon = "👨🏻‍💻", 
 ) 
st.title("FIND RGPV RESULT  👨🏻‍💻")

if "my_input" not in st.session_state:
    st.session_state["my_input"]=""
#sidebar
with st.sidebar:
    # for animation
    def load_lottiefile(filepath:str):
        with open(filepath,"r")as f:
            return json.load(f)

    def load_lottieurl(url:str):
        r = requests.get(url)
        if r.status_code !=200:
           return none
        return r.json()
    lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")  
    st_lottie(
    lottie_hello,
    speed=2,
    reverse=False,
    loop=True,
    quality="low", 
    )
    # for token 
with st.sidebar:
    st.header("FOR DOWNLOADE FILE")
    st.subheader(" FILL TOKEN ✍🏻")
    token =st.text_input("ENTER TOKEN",st.session_state["my_input"])
    file = st.button("Get File")
    if file:
       
        webbrowser.open(url+'/get_file?token='+token)


   
# Taking Inputs
code = st.text_input("Enter College Code",st.session_state["my_input"])
branch = st.text_input("Enter Branch Code",st.session_state["my_input"])
year = st.text_input("Enter Year Of Admission",st.session_state["my_input"])
sem = st.text_input("Enter Semester",st.session_state["my_input"])
start = st.text_input("Enter Starting Roll Number",st.session_state["my_input"])
end = st.text_input("Enter Ending Roll Number",st.session_state["my_input"])
nol = st.text_input("Number Of Lateral Students",st.session_state["my_input"])
submit = st.button("Submit")



if submit:

    ## for random num
    beg,last=100000,999999
    var =random.randint(beg, last)
    st.subheader("YOUR TOKEN ⬇️")
    st.subheader(var)
    # for data sending to server
    data={'code':code,
          "branch":branch,
          'year':year,
          'sem':sem,
          'start':start,
          'end':end,
          'nol':nol,
          'token': var}
    response=requests.post(url+'/webhook',json.dumps(data),headers={'Content-Type':'application/json'})
    time.sleep(2)

    # for clock:
    try:
        print(response.text)
        response=response.text.split(',')
        text=response[0].split(':')[1][1:-1]
        de_time=response[1].split(':')[1].split('}')[0]
        # time = response.text.split(':')[-1].split('}')[0]
        time_clock= int (de_time)
        st.subheader("YOUR PROCESS  IS STARTED WAIT SOME TIME ⏱")
        ph = st.empty()
        N = time_clock*60
        for secs in range(N,0,-1):
            mm, ss = secs//60, secs%60
            ph.metric(" time ⏱", f"{mm:02d}:{ss:02d}")
            time.sleep(1)

    except Exception as e:
        print(e)
        st.subheader("Server Error❗⚠️")
       
   
