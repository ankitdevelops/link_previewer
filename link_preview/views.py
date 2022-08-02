from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def home(request):
    url = request.GET.get("url")
    if url:
        response = requests.get(url)
        html_document = BeautifulSoup(response.content, "html.parser")

        context = {
            "title": get_title(html_document),
            "description": get_description(html_document),
            "image": get_image(html_document),
            "domain": get_domain(html_document),
        }
    else:
        context = None
    return render(request, "index.html", context)


def get_title(html_document):
    title = None
    if not title:
        title = html_document.find("meta", property="og:title").get("content")
    elif not title:
        title = html_document.find("meta", property="twitter:title").get("content")
    elif not title:
        title = html_document.title.string
    else:
        title = html_document.find("h1").string
    return title


def get_description(html_document):
    description = None
    if not description:
        description = html_document.find("meta", property="og:description").get(
            "content"
        )
    elif not description:
        description = html_document.find("meta", property="twitter:description").get(
            "content"
        )
    else:
        description = html_document.find("p").string
    return description


def get_image(html_document):
    image = None
    if not image:
        image = html_document.find("meta", property="og:image").get("content")
    else:
        url = html_document.find_all("img")
        for i in url:
            if i.get("src").startswith("https"):
                image = i.get("src")
                break

    return image


def get_domain(html_document):
    domain = None
    if not domain:
        domain = html_document.find("meta", property="og:url").get("content")
    else:
        domain = html_document.find("link", rel="canonical").get("href")
    return domain
