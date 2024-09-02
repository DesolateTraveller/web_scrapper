import streamlit as st
from bs4 import BeautifulSoup
import requests

@st.cache_data
def scrape_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Example: Extracting some serializable data
        title = soup.title.string if soup.title else "No title"
        headings = [h.get_text(strip=True) for h in soup.find_all('h1')]
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]

        # Return serializable data only
        return {
            "title": title,
            "headings": headings,
            "paragraphs": paragraphs
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    st.title("Web Scraper")

    url = st.text_input("Enter a URL to scrape")
    
    if st.button("Scrape"):
        if url:
            data = scrape_webpage(url)
            if "error" in data:
                st.error(data["error"])
            else:
                st.write("**Title:**", data["title"])
                st.write("**Headings:**", data["headings"])
                st.write("**Paragraphs:**", data["paragraphs"])
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
