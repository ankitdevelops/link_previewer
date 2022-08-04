from django.shortcuts import redirect, render
from bs4 import BeautifulSoup
import requests
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def home(request):
    context = None
    url = request.POST.get("url")
    if url:
        try:
            response = requests.get(url)
            html_document = BeautifulSoup(response.content, "html.parser")
            context = {
                "title": get_title(html_document),
                "description": get_description(html_document),
                "image": get_image(html_document),
                "domain": get_domain(html_document,url),
            }
        except Exception as ex:
            return redirect('home')
    
    return render(request, "index.html", context)


def get_title(html_document):
    title = None
    if html_document.find("meta", property="og:title") :
        title = html_document.find("meta", property="og:title").get("content")
    elif html_document.find("meta", property="twitter:title"):
        title = html_document.find("meta", property="twitter:title").get("content")
    elif html_document.title:
        title = html_document.title.string
    elif html_document.find("h1"):
        title = html_document.find("h1").string
    else:
        title = "No Title Found"
    return title


def get_description(html_document):
    description = None
    if  html_document.find("meta", property="og:description"):
        description = html_document.find("meta", property="og:description").get(
            "content"
        )
    elif html_document.find("meta", property="twitter:description"):
        description = html_document.find("meta", property="twitter:description").get(
            "content"
        )
    elif  html_document.find("p"):
        description = html_document.find("p").string
    else:
        description = "No Description Found"
    return description


def get_image(html_document):
    image = None
    if  html_document.find("meta", property="og:image"):
        image = html_document.find("meta", property="og:image").get("content")
    elif html_document.find_all("img"):
        url = html_document.find_all("img")
        for i in url:
            if i.get("src").startswith("https"):
                image = i.get("src")
                break
        image = "https://icon-library.com/images/no-picture-available-icon/no-picture-available-icon-1.jpg"
    return image


def get_domain(html_document,url):
    domain = None
    if html_document.find("meta", property="og:url"):
        domain = html_document.find("meta", property="og:url").get("content")
    elif html_document.find("link", rel="canonical"):
         domain = html_document.find("link", rel="canonical").get("href")
    else:
       domain = url
    return domain
