from bs4 import BeautifulSoup
import requests


def get_seo_details(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        seo_data = {
            "title": soup.title.string if soup.title else "No Title",
            "meta_description": soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={
                "name": "description"}) else "No Meta Description",
            "h1": soup.find("h1").text if soup.find("h1") else "No H1 Tag"
        }
        return seo_data
    except Exception as e:
        return {"error": str(e)}
