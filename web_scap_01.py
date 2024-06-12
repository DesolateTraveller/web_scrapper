import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Web Scraping App")

# Input field for the URL
url = st.text_input("Enter the URL of the webpage you want to scrape:")

def scrape_webpage(url):
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title and a snippet of text (as an example)
        title = soup.title.string if soup.title else "No title found"
        snippet = ' '.join(soup.get_text().split()[:])  # Get the first 100 words of text

        return title, snippet
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None, None

if url:
    if st.button("Scrape Webpage"):
        with st.spinner("Scraping the webpage..."):
            title, snippet = scrape_webpage(url)
            if title and snippet:
                st.success("Webpage scraped successfully!")
                st.subheader("Page Title")
                st.write(title)
                st.subheader("Page Content Snippet")
                st.write(snippet)
            else:
                st.error("Failed to scrape the webpage.")
