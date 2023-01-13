from requests_html import HTMLSession  
import pandas as pd

HEADERS = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
fListOfSets = 'list_of_urls.txt'
output =[]
zero_items = '0 Items'
xpath_name = '//*[@id="item-name-title"]/text()'
xpath_items = '/html/body/div[3]/center/table/tbody/tr/td/section/div/div/div[1]/div[3]/span[1]/span/text()'
xpath_desc = '//*[@id="_idStoreResultListSection"]/table/tbody/tr[3]/td[2]/text()'
xpath_price = '//*[@id="_idStoreResultListSection"]/table/tbody/tr[3]/td[5]/text()'

def render_JS_store(URL):
    session = HTMLSession()
    response_store = session.get(URL)
    response_store.html.render(timeout=20)
    response_store.close()
    session.close()
    return response_store

def get_data_from_rendered_page2(TARGET_URL):
    rendered_page_response = render_JS_store(TARGET_URL)
    try:
        numberOfItems = rendered_page_response.html.xpath(xpath_items)
        name = rendered_page_response.html.xpath(xpath_name)
        if zero_items!=numberOfItems[0]:
            description = rendered_page_response.html.xpath(xpath_desc)
            price = rendered_page_response.html.xpath(xpath_price)[0].split()
            items = rendered_page_response.html.xpath(xpath_items)
        else:
            numberOfItems = zero_items
            description = rendered_page_response.html.xpath(xpath_name)
            price = "[EUR, 0.0]"
            items = "[0 Items]"
    finally: None
    return name,description,price,items

file = open(fListOfSets,'r')
sets = file.readlines()
for set_url in sets:
    x = get_data_from_rendered_page2(set_url)
    out = {
        'NAME' : x[0],
        'DESC' : x[1],
        'PRICE' : x[2],
        'ITEMS' : x[3]
    }
    output.append(out)

df = pd.DataFrame(output)
print(120 * '*')
print(df)                    # #printing the output to the command line   
print(120 * '*')
file.close()