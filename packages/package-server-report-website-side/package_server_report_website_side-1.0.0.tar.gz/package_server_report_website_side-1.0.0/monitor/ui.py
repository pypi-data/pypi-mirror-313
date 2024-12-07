from bs4 import BeautifulSoup
import requests


def get_ui_details(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        images = soup.find_all("img")
        missing_alt_text = [img["src"] for img in images if not img.get("alt")]

        ui_data = {
            "missing_alt_text": missing_alt_text,
            "total_images": len(images)
        }
        return ui_data
    except Exception as e:
        return {"error": str(e)}
