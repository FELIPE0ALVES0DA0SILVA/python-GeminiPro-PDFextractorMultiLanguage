from dotenv import load_dotenv

load_dotenv() ## load all the enviroments variables from .env

import streamlit as st
import os

from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

## Function to load Gemini Pro Vision

model= genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input, image, prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

## initialize our streamlit app

st.set_page_config(
    page_icon='🚢',
    page_title='MultiLanguage Invoice Extractor'
)

st.header('MultiLanguage Invoice Extractor 🚢')

input=st.text_input('Input Prompt: ',key='input')
upload_file=st.file_uploader('Choose an image... ',type=['jpg','jpeg', 'png'])

image =''

if upload_file is not None:
    image=Image.open(upload_file)
    st.image(image, caption='Uploaded Image.',use_column_width=True)

submit = st.button('Tell me about the invoice')

input_prompt='''
    You are an expert in understanding invoices. We will upload  a image  as invoice and you will have to answer any questions based on the uoloaded invoice image
'''

## if submit button is clicked

## Function to process the image uploaded to pass to gemini vision pro api
def input_image_setup(uploaded_file):
    if upload_file is not None:
        #Read the file into bytes
        bytes_data = upload_file.getvalue()

        image_parts = [
            {
                'mime_type': upload_file.type,
                'data': bytes_data
            }
        ]

        return image_parts

if submit:
    image=input_image_setup(upload_file)
    response=get_gemini_response(input=input_prompt,image=image,prompt=input)
    st.subheader('The Response is')
    st.write(response)



