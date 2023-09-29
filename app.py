import streamlit as st


max_width = 800
st.markdown(f"""
<style>
    .appview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: 0rem;
        padding-right: 0rem;
        padding-left: 0rem;
        padding-bottom: 0rem;
    }}
</style>"""+"""
<style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
</style>""",unsafe_allow_html=True)

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

qs = [ 
    "Full Name*", "Phone Number*", "Email Address*","Country*", "What is your Occupation?*",
    "What’s happening in your life right now that has you potentially considering becoming a life coach? And ultimately what’s your goal?*",
    "What best describes your financial situation?*","Please confirm you have read our Program Brochure before booking the Enrollment Interview*"
]

money_qs = ["I have the cash and/or credit to invest in myself","I don’t have much money right now or access to credit",""]
b_qs = ["Yes", "No", ""]

thresh = 49
url1 = "https://pages.jayshettycoaching.com/test-jscs-qualified-booking/"
url2 = "https://pages.jayshettycoaching.com/test-jscs-unqualified-lead/"

import datetime
from featurizer import *
import streamlit.components.v1 as components
from streamlit.runtime.scriptrunner import get_script_run_ctx

def get_remote_ip() -> str:
    try:
        ctx = get_script_run_ctx()
        if ctx is None: return None
        session_info = st.runtime.get_instance().get_client(ctx.session_id)
        if session_info is None: return None
    except: return None
    return session_info.request.remote_ip

country_list = [f"{i[0]}: {i[1]}" for i in CODES.items()]

with st.form("Answers"):
    cols = st.columns([4,2,4])
    with cols[0]:
        name = st.text_input(f"{qs[0]}")
    with cols[1]:
        country = st.selectbox("Country Code*", country_list, index=226)
        country_code = country.split("+")[-1]
    with cols[2]:
        phone_number = st.text_input("Phone Number*")
    cols2 = st.columns([4,6])
    with cols2[0]:
        email = st.text_input(f"{qs[2]}")
    with cols2[1]:
        occupation = st.text_input(f"{qs[4]}")
    long_question_response = st.text_area(f"{qs[5]}", height=170)
    has_money = st.selectbox(f"{qs[6]}", money_qs, index=2)
    read_brochure = st.selectbox(f"{qs[7]}", b_qs, index=2)
    check = st.checkbox("I understand my Enrollment Advisor will call me on the number I provided and at the appointment time I will schedule. I will be ready for the call.*")
    
    if st.form_submit_button("Submit"):
        vals = {
            qs[0]: len(name), qs[1]: len(phone_number), qs[2]: len(email),
            qs[4]: len(occupation), qs[5]: len(long_question_response),
            qs[6]: len(has_money), qs[7]: len(read_brochure)
        }  
        if all(i != 0 for i in vals.values()) and check:    
            features = [
                name, country_code+phone_number, None, email, occupation,
                long_question_response, int("cash" in has_money), 
                int("Yes" in read_brochure), datetime.datetime.now()
            ]
            f = Featurizer(
                *features
            )
            feats = f.generate_feature_dict()
            score, int_score = model.predict([feats])
            st.success(f"Thank you for submitting the survey!\n\nYou are more likely to convert than {int_score}% of other leads!\n\nFind your calendar invite below:\n\n[Click Here]({url1 if int_score > thresh else url2})", icon="✅")
        else:
            error =  "**Please be sure to complete the following fields:**"
            for name, count in vals.items():
                if count == 0:
                    error = error + f"\n\n{name}"
            if not check:
                error = error + "\n\nI understand my Enrollment Advisor will call me*"
            st.error(error, icon="🚨")
st.success(st.experimental_get_query_params())
st.success(get_remote_ip())
