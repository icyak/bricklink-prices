from requests_html import HTMLSession
import pandas as pd

HEADERS = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64;'
     'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
FLISTOFSETS= 'list_of_urls.txt'
output =[]
ZERO_ITEMS = '0 Items'
XPATH_NAME = '//*[@id="item-name-title"]/text()'
XPATH_ITEMS = '/html/body/div[3]/center/table/tbody/tr/td/section/div/div/div[1]/div[3]/span[1]/span/text()'
XPATH_DESC = '//*[@id="_idStoreResultListSection"]/table/tbody/tr[3]/td[2]/text()'
XPATH_PRICE = '//*[@id="_idStoreResultListSection"]/table/tbody/tr[3]/td[5]/text()'

def render_JS_store(url):
    session = HTMLSession()
    response_store = session.get(url)
    response_store.html.render(timeout=20)
    response_store.close()
    session.close()
    return response_store

def extract_data(target_url):
    rendered_page_response = render_JS_store(target_url)
    try:
        items_from_page = rendered_page_response.html.xpath(XPATH_ITEMS)
        name = rendered_page_response.html.xpath(XPATH_NAME)
        if ZERO_ITEMS!=items_from_page[0]:
            description = rendered_page_response.html.xpath(XPATH_DESC)
            price = rendered_page_response.html.xpath(XPATH_PRICE)[0].split()
            items = rendered_page_response.html.xpath(XPATH_ITEMS)
        else:
            items_from_page = ZERO_ITEMS
            description = rendered_page_response.html.xpath(XPATH_NAME)
            price = "[EUR, 0.0]"
            items = "[0 Items]"
    finally: None
    return name,description,price,items

with open(FLISTOFSETS,'r',encoding='utf-8') as file:
    sets = file.readlines()

#file = open(FLISTOFSETS,'r',encoding='utf-8')
#sets = file.readlines()
for set_url in sets:
    x = extract_data(set_url)
    out = {
        'NAME' : x[0],
        'DESC' : x[1],
        'PRICE' : x[2],
        'ITEMS' : x[3]
    }
    output.append(out)

df = pd.DataFrame(output)
print(120 * '*')
print(df)
print(120 * '*')
file.close()