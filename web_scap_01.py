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
st.set_page_config(page_title="Web Scrapper",
                   layout="wide",
                   #page_icon=               
                   initial_sidebar_state="collapsed")
#----------------------------------------
st.title(f""":rainbow[Web Scrapper | v0.3]""")
st.markdown('Created by | <a href="mailto:avijit.mba18@gmail.com">Avijit Chakraborty</a>', 
            unsafe_allow_html=True)
st.info('**Disclaimer : :blue[Thank you for visiting the app] | Unauthorized uses or copying of the app is strictly prohibited | Click the :blue[sidebar] to follow the instructions to start the applications.**', icon="ℹ️")
#----------------------------------------
# Set the background image
st.divider()
#---------------------------------------------------------------------------------------------------------------------------------
### Functions & Definitions
#---------------------------------------------------------------------------------------------------------------------------------

def scrape_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        snippet = ' '.join(soup.get_text().split()[:])  
        return title, snippet
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None, None

def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def extract_text(soup):
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

#def summarize_text(text):
    #summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    ## Summarize the text
    #summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    #return summary[0]['summary_text']


def summarize_text(text):
    model_name = "t5-large"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    preprocessed_text = "summarize: " + text.strip().replace("\n", " ")
    inputs = tokenizer.encode(preprocessed_text, 
                              return_tensors="pt", 
                              max_length=512, 
                              truncation=True)
    summary_ids = model.generate(
        inputs, 
        max_length=512, 
        min_length=100, 
        length_penalty=2.0, 
        num_beams=4, 
        early_stopping=True
    )

    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
#---------------------------------------------------------------------------------------------------------------------------------
### Main app
#---------------------------------------------------------------------------------------------------------------------------------

# Input field for the URL
url = st.text_input("**:blue[Enter the URL of the webpage you want to scrape:]**")
if st.button("**:blue[Scrape Webpage]**"):
    
    st.divider()
    html_content = fetch_webpage(url)
    title, snippet = scrape_webpage(url)
            
    if title and snippet:
        st.success("Webpage fetched successfully!")
              
        col1, col2, col3 = st.columns((0.3,0.4,0.3))

        with col1:

            with st.container(height=750,border=True):
            
                st.subheader("Web View",divider='blue')
                st.write(html_content, unsafe_allow_html=True)  # Display raw HTML

                with col2:

                    with st.container(height=750,border=True):

                        st.subheader("Page Title",divider='blue')
                        soup = parse_html(html_content)
                        title = soup.title.string if soup.title else "No title found"
                        st.write(title)

                        st.divider()

                        st.subheader("Page Content",divider='blue')
                        text = extract_text(soup)
                        st.write(text[:5000])

                        with col3:  

                                with st.container(height=750,border=True):

                                    st.subheader("Page Summary",divider='blue')
                                    with st.spinner("Scraping the webpage & generating the summary.."):
                                        summary = summarize_text(text)
                                        st.write(summary)

    else:
        st.error("Failed to scrape the webpage.")
