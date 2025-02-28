#---------------------------------------------------------------------------------------------------------------------------------
### Authenticator
#---------------------------------------------------------------------------------------------------------------------------------
import streamlit as st
#---------------------------------------------------------------------------------------------------------------------------------
### Import Libraries
#---------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#----------------------------------------
import requests
from bs4 import BeautifulSoup
from transformers import T5ForConditionalGeneration, T5Tokenizer
#from gensim.summarization import summarize
#---------------------------------------------------------------------------------------------------------------------------------
### Title and description for your Streamlit app
#---------------------------------------------------------------------------------------------------------------------------------
#import custom_style()
st.set_page_config(page_title="Web Scrapper | v0.1",
                   layout="wide",
                   page_icon="💻",             
                   initial_sidebar_state="collapsed")
#----------------------------------------
st.markdown(
    """
    <style>
    .title-large {
        text-align: center;
        font-size: 35px;
        font-weight: bold;
        background: linear-gradient(to left, red, orange, blue, indigo, violet);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .title-small {
        text-align: center;
        font-size: 20px;
        background: linear-gradient(to left, red, orange, blue, indigo, violet);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    <div class="title-large">Web Scapper </div>
    <div class="title-small">Version : 0.1</div>
    """,
    unsafe_allow_html=True
)
#----------------------------------------

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #F0F2F6;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #333;
        z-index: 100;
    }
    .footer p {
        margin: 0;
    }
    .footer .highlight {
        font-weight: bold;
        color: blue;
    }
    </style>

    <div class="footer">
        <p>© 2025 | Created by : <span class="highlight">Avijit Chakraborty</span> | <a href="mailto:avijit.mba18@gmail.com"> 📩 </a></p> <span class="highlight">Thank you for visiting the app | Unauthorized uses or copying is strictly prohibited | For best view of the app, please zoom out the browser to 75%.</span>
    </div>
    """,
    unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------
### Functions & Definitions
#---------------------------------------------------------------------------------------------------------------------------------

@st.cache_data(ttl="2h")
def fetch_webpage(url):
    if not url:
        return None
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None


def parse_html(html_content):
    if not html_content:
        return None
    return BeautifulSoup(html_content, 'html.parser')

def extract_text(soup):
    if soup is None:
        return "No content extracted."
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text if text else "No text found."

@st.cache_data(ttl="2h")
def summarize_text(text):
    if not text:
        return "No content available to summarize."
    model_name = "t5-large"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    preprocessed_text = "summarize: " + text.strip().replace("\n", " ")
    inputs = tokenizer.encode(preprocessed_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=512, min_length=100, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#---------------------------------------------------------------------------------------------------------------------------------
### Main app
#---------------------------------------------------------------------------------------------------------------------------------
st.markdown(
            """
            <style>
                .centered-info {
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
                font-size: 15px;
                color: #007BFF; 
                padding: 5px;
                background-color: #E8F4FF; 
                border-radius: 5px;
                border: 1px solid #007BFF;
                margin-top: 5px;
                margin-bottom: 10px;
                }
            </style>
            """,unsafe_allow_html=True,)
st.markdown('<div class="centered-info"><span style="margin-left: 10px;">A lightweight streamlit app that helps user to extract the information from a webpage by uploading the links.</span></div>',unsafe_allow_html=True,)

st.divider()

col1, col2, col3, col4 = st.columns((0.2,0.25,0.3,0.25))
with col1:
    with st.container(border=True):
        
        url = st.text_input("**:blue[Enter the URL]**")
        if st.button("**:blue[Scrape]**"):
            st.divider()
            if not url:
                st.warning("Please enter a valid URL.")
            else:
                st.success("Webpage fetched successfully!")
    
            with col2:
               with st.container(border=True): 
        
                    with st.spinner("Fetching webpage & generating the summary..."):
                        html_content = fetch_webpage(url)
                        if html_content:
                            soup = parse_html(html_content)
                            text = extract_text(soup)
                            summary = summarize_text(text)
                            
                            st.subheader("Page Title",divider='blue')
                            title = soup.title.string if soup.title else "No title found"
                            st.write(title)
        
                            with col3:
                                with st.container(border=True): 

                                    st.subheader("Web View",divider='blue')
                                    st.write(text[:20000])

                            with col4:  
                                with st.container(border=True): 

                                    st.subheader("Page Summary",divider='blue')
                                    st.write(summary)
                                    
                                text_file_name = f"{title}_summary.txt"
                                st.download_button(label="📥 **Download summary (.txt)**",data=summary,file_name=text_file_name,mime="text/plain",)    

