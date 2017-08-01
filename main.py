import threading
import requests
import os
from bs4 import BeautifulSoup
from xml.dom import minidom

end = False

def scrapData(second):

    global end
    if end:
        return

    url = "http://gkmean.cafe24.com/sitemap.xml"
    page = requests.get(url)

    root = minidom.Document()
    rss = root.createElement('rss')
    rss.setAttribute('version', '2.0')
    rss.setAttribute('xmlns:g', 'http://base.google.com/ns/1.0')
    root.appendChild(rss)

    channel = root.createElement('channel')
    rss.appendChild(channel)

    title = root.createElement('title')
    title.appendChild(root.createTextNode('봉다리 - bondaly'))
    channel.appendChild(title)

    siteLink = root.createElement('link')
    siteLink.appendChild(root.createTextNode('http://gkmean.cafe24.com'))
    channel.appendChild(siteLink)

    desc = root.createElement('description')
    desc.appendChild(root.createTextNode('봉다리'))
    channel.appendChild(desc)

    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find_all('loc')

    print(len(items))

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        for link in soup.find_all('loc'):
            correctURL = link.text
            correctPAGE = requests.get(correctURL)
            corSoup = BeautifulSoup(correctPAGE.content, 'html.parser')
            p_no = corSoup.find('input', id='pars_no')['dds']
            p_name = corSoup.find('input', id='pars_name')['dds']
            p_img = corSoup.find('input', id='pars_img')['dds']
            p_price = corSoup.find('input', id='pars_price')['dds']

            item = root.createElement('item')
            channel.appendChild(item)

            g_id = root.createElement('g:id')
            g_id.appendChild(root.createTextNode(p_no))
            item.appendChild(g_id)

            g_title = root.createElement('g:title')
            g_title.appendChild(root.createCDATASection(p_name))
            item.appendChild(g_title)

            g_description = root.createElement('g:description')
            g_description.appendChild(root.createCDATASection(p_name))
            item.appendChild(g_description)

            g_google_product_category = root.createElement('g:google_product_category')
            g_google_product_category.appendChild(root.createCDATASection('Apparel & Accessories > Clothing'))
            item.appendChild(g_google_product_category)

            g_product_type = root.createElement('g:product_type')
            g_product_type.appendChild(root.createTextNode('product'))
            item.appendChild(g_product_type)

            g_link = root.createElement('g:link')
            g_link.appendChild(root.createTextNode(correctURL))
            item.appendChild(g_link)

            g_image_link = root.createElement('g:image_link')
            g_image_link.appendChild(root.createTextNode('http:' + p_img))
            item.appendChild(g_image_link)

            g_condition = root.createElement('g:condition')
            g_condition.appendChild(root.createTextNode('new'))
            item.appendChild(g_condition)

            g_availability = root.createElement('g:availability')
            g_availability.appendChild(root.createTextNode('in stock'))
            item.appendChild(g_availability)

            g_price = root.createElement('g:price')
            g_price.appendChild(root.createTextNode(p_price))
            item.appendChild(g_price)

            g_brand = root.createElement('g:brand')
            g_brand.appendChild(root.createTextNode('봉다리'))
            item.appendChild(g_brand)

    else:
        print("fail...")

    fileexi = os.path.exists('./bondaly_catalog.xml')

    xml_str = root.toprettyxml(indent="\t")
    save_path_file = "bondaly_catalog.xml"

    if fileexi:
        os.remove('bondaly_catalog.xml')

        with open(save_path_file, "w") as f:
            f.write(xml_str)
    else:
        with open(save_path_file, "w") as f:
            f.write(xml_str)

    print('Im Working...')

    threading.Timer(second, scrapData, [second]).start()


scrapData(3600)