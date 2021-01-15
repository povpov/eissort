import requests
from io import StringIO
from lxml import etree
from config import url, login, password

title, anchors, links = "", "", ""


def verify_anchors():
    global title, anchors, links
    resY, resN = 0, 0
    for anchor in anchors:
        if "#" + anchor in links:
            print(anchor, " - OK")
            resY += 1
        else:
            print(anchor, " - Error")
            resN += 1
    print("=" * 15)
    print(f"anchors: {resY} - OK, {resN} - Error", resN == 0)
    print(" ")


def verify_links():
    resY, resN = 0, 0
    global title, anchors, links
    for link in links:
        if link.startswith(f"#id-{''.join(title.split())}"):
            if link[1:] in anchors:
                print(link[1:], " - OK")
                resY += 1
            else:
                print(link[1:], " - Error")
                resN += 1

    print("=" * 15)
    print(f"links: {resY} - OK, {resN} - Error", resN == 0)


with requests.Session() as session:
    session.auth = (login, password)
    response = session.get(url)

    if response.status_code == 200:
        response.encoding = 'utf-8'
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(response.text), parser)
        title = tree.find('//h1[@id="title-text"]/a').text
        anchors = tree.xpath("//span[@data-macro-name='anchor']/@id")
        links = tree.xpath("//a/@href")

        verify_anchors()
        verify_links()
