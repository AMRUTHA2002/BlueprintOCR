import easyocr as ocr
import streamlit as st
from PIL import Image
import numpy as np
import streamlit_authenticator as stauth
import pickle
from pathlib import Path

st.set_page_config(page_title="Blueprint OCR", page_icon=":🔎:", layout="wide")

# --- USER AUTHENTICATION ---
names = ["Amrutha", "Ansika"]
usernames = ["amruthuse", "ansika123"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "userCookie", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")



if authentication_status:

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")

    st.title("Blueprint OCR")

    st.markdown("## Built using `easyocr`")

    st.markdown("")

    image = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])


    @st.cache_resource
    def load_model(): 
        reader = ocr.Reader(['en'],model_storage_directory='.',gpu=True)
        return reader 

    reader = load_model()

    if image is not None:

        input_image = Image.open(image) 
        st.image(input_image) 

        with st.spinner("🤖 Extracting... "):
            

            result = reader.readtext(np.array(input_image))

            result_text = [] 


            for text in result:
                result_text.append(text[1])

            st.write(result_text)
        st.balloons()
    else:
        st.write("Upload an Image")

    st.caption("Here is the text extracted from your image...")

