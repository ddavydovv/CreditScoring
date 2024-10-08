import pandas as pd
import asyncio
import joblib
import streamlit as st
import json
from keras.api.models import load_model


st.set_page_config(
    page_title="Credit Scoring",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)



st.header('Автоматизированная система кредитного скоринга')

PATH_DATA = 'lending_club_loan_two.csv.zip'
PATH_UNIQUE_DATA = 'unique_values.json'
PATH_MODEL = 'model.sav'


async def loan_data(path):
    data = pd.read_csv(path, compression='zip', low_memory=True)
    return data


async def start():
    df = await loan_data(PATH_DATA)
    st.write(df[:50])


with open(PATH_UNIQUE_DATA) as file:
    dict_unique = json.load(file)


term = st.sidebar.selectbox('Term', dict_unique['term'])
loan_amnt = st.sidebar.slider('Loan amnt', min_value=min(dict_unique['loan_amnt']), max_value=max(dict_unique['loan_amnt']))
int_rate = st.sidebar.slider('Int rate', min_value=min(dict_unique['int_rate']), max_value=max(dict_unique['int_rate']))
installment = st.sidebar.slider('Installment', min_value=min(dict_unique['installment']), max_value=max(dict_unique['installment']))
annual_inc = st.sidebar.slider('Annual inc', min_value=min(dict_unique['annual_inc']), max_value=max(dict_unique['annual_inc']))
dti = st.sidebar.slider('DTI', min_value=min(dict_unique['dti']), max_value=max(dict_unique['dti']))
open_acc = st.sidebar.slider('Open acc', min_value=min(dict_unique['open_acc']), max_value=max(dict_unique['open_acc']))
pub_rec = st.sidebar.selectbox('Pub rec', dict_unique['pub_rec'])
revol_bal = st.sidebar.slider('Revol bal', min_value=min(dict_unique['revol_bal']), max_value=max(dict_unique['revol_bal']))
revol_util = st.sidebar.slider('Revol util', min_value=min(dict_unique['revol_util']), max_value=max(dict_unique['revol_util']))
total_acc = st.sidebar.slider('Total acc', min_value=min(dict_unique['total_acc']), max_value=max(dict_unique['total_acc']))
mort_acc = st.sidebar.selectbox('Mort acc', dict_unique['mort_acc'])
pub_rec_bankruptcies = st.sidebar.selectbox('Pub rec bankruptcies', dict_unique['pub_rec_bankruptcies'])

dict_data = {
    "term": term,
    "loan_amnt": loan_amnt,
    "int_rate": int_rate,
    "installment": installment,
    "annual_inc": annual_inc,
    "dti": dti,
    "open_acc": open_acc,
    "pub_rec": pub_rec,
    "revol_bal": revol_bal,
    "revol_util": revol_util,
    "total_acc": total_acc,
    "mort_acc": mort_acc,
    "pub_rec_bankruptcies": pub_rec_bankruptcies
}

parameters = ["A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4", "C5", "D1", "D2", "D3", "D4", "D5", "E1", "E2", "E3", "E4", "E5", "F1", "F2", "F3", "F4", "F5", "G1", "G2", "G3", "G4", "G5"]
sub_grade_dict_params = ["sub_grade_A2", "sub_grade_A3", "sub_grade_A4", "sub_grade_A5", "sub_grade_B1", "sub_grade_B2", "sub_grade_B3", "sub_grade_B4", "sub_grade_B5", "sub_grade_C1", "sub_grade_C2", "sub_grade_C3", "sub_grade_C4", "sub_grade_C5", "sub_grade_D1", "sub_grade_D2", "sub_grade_D3", "sub_grade_D4", "sub_grade_D5", "sub_grade_E1", "sub_grade_E2", "sub_grade_E3", "sub_grade_E4", "sub_grade_E5", "sub_grade_F1", "sub_grade_F2", "sub_grade_F3", "sub_grade_F4", "sub_grade_F5", "sub_grade_G1", "sub_grade_G2", "sub_grade_G3", "sub_grade_G4", "sub_grade_G5"]
sub_grade = st.sidebar.selectbox('Sub grade', parameters)
for param in sub_grade_dict_params:
    param_split = param.split('_')[2]
    if param_split == sub_grade:
        dict_data[param] = True
    else:
        dict_data[param] = False


parameters_verification_status = ["Source Verified", "Verified"]
verification_status_dict_params = ["verification_status_Source Verified", "verification_status_Verified"]
verification_status = st.sidebar.selectbox('Verification status', parameters_verification_status)
for param in verification_status_dict_params:
    param_split = param.split('_')[2]
    if param_split == verification_status:
        dict_data[param] = True
    else:
        dict_data[param] = False


parameters_purpose = ["purpose_credit_card", "purpose_debt_consolidation", "purpose_educational", "purpose_home_improvement", "purpose_house", "purpose_major_purchase", "purpose_medical", "purpose_moving", "purpose_other", "purpose_renewable_energy", "purpose_small_business", "purpose_vacation", "purpose_wedding"]
purpose_dict_params = ["purpose_credit_card", "purpose_debt_consolidation", "purpose_educational", "purpose_home_improvement", "purpose_house", "purpose_major_purchase", "purpose_medical", "purpose_moving", "purpose_other", "purpose_renewable_energy", "purpose_small_business", "purpose_vacation", "purpose_wedding"]
purpose = st.sidebar.selectbox('Purpose', parameters_purpose)
for param in purpose_dict_params:
    if param == purpose:
        dict_data[param] = True
    else:
        dict_data[param] = False


initial_list_status_w = st.sidebar.selectbox('Initial list status w', dict_unique['initial_list_status_w'])
dict_data["initial_list_status_w"] = initial_list_status_w


parameters_application_type = ["INDIVIDUAL", "JOINT"]
application_type_dict_params = ["application_type_INDIVIDUAL", "application_type_JOINT"]
application_type = st.sidebar.selectbox('Application type', parameters_application_type)
for param in application_type_dict_params:
    param_split = param.split('_')[2]
    if param_split == application_type:
        dict_data[param] = True
    else:
        dict_data[param] = False


parameters_home_ownership = ["OTHER", "OWN", "RENT"]
home_ownership_dict_params = ["home_ownership_OTHER", "home_ownership_OWN", "home_ownership_RENT"]
home_ownership = st.sidebar.selectbox('Home ownership', parameters_home_ownership)
for param in home_ownership_dict_params:
    param_split = param.split('_')[2]
    if param_split == home_ownership:
        dict_data[param] = True
    else:
        dict_data[param] = False


parameters_zip_code = ["05113", "11650", "22690", "29597", "30723", "48052", "70466", "86630", "93700"]
zip_code_dict_params = ["zip_code_05113", "zip_code_11650", "zip_code_22690", "zip_code_29597", "zip_code_30723", "zip_code_48052", "zip_code_70466", "zip_code_86630", "zip_code_93700"]
zip_code = st.sidebar.selectbox('Zip code', parameters_zip_code)
for param in zip_code_dict_params:
    param_split = param.split('_')[2]
    if param_split == zip_code:
        dict_data[param] = True
    else:
        dict_data[param] = False


data_predict = pd.DataFrame([dict_data])
model = load_model('model.h5')

button = st.sidebar.button("Оценить")
if button:
    output = model.predict(data_predict)[0]

    if round(output[0]) == 1:
        text = 'Одобрить выдачу кредита'
    else:
        text = 'Отказать в выдаче кредита'

    st.sidebar.success(f"Результат анализа: {text}")

asyncio.run(start())