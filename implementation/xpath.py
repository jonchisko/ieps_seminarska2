from lxml import html
import json
import sys

def parseOverstock(filename):

    # Get html document
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    file = open(filename, 'rb')
    page = html.fromstring(file.read())
    file.close()
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # Find elements
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    base = '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor]/td[2]'

    titles = page.xpath(base + '/a/b/text()')

    listingPrices = page.xpath(base + '/table/tbody/tr/td[1]/table/tbody/tr[1]/td[@align="left"]/s/text()')

    prices = page.xpath(base + '/table/tbody/tr/td[1]/table/tbody/tr[2]/td[@align="left"]/span/b/text()')

    savings = page.xpath(base + '/table/tbody/tr/td[1]/table/tbody/tr[3]/td[@align="left"]/span/text()')
    absoluteSavings = [i.split(' ')[0] for i in savings]
    relativeSavings = [i.split(' ')[1].replace('(', '').replace(')', '') for i in savings]

    contents = [i.replace('\n', ' ') for i in page.xpath(base + '/table/tbody/tr/td[2]/span/text()')]
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # Pack it up in a JSON format
    #  = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    result = {'Items':[]}
    for i in range(len(contents)):
        result['Items'].append({'Title': titles[i],
                                'ListPrice': listingPrices[i],
                                'Price': prices[i],
                                'Saving': absoluteSavings[i],
                                'SavingPercent': relativeSavings[i],
                                'Content': contents[i]})
    result = json.dumps(result, indent=4)
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    print(result)

def parseRTV(filename):
    file = open(filename, 'rb')
    page = html.fromstring(file.read())
    file.close()

    result = {'Article':{}}

    author = page.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div/text()')[0]
    result['Article']['Author'] = author

    date = page.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]')[0].\
                replace('\n', '').\
                replace('\t', '')
    result['Article']['PublishedTime'] = date

    title = page.xpath('//*[@id="main-container"]/div[3]/div/header/h1/text()')[0]
    result['Article']['Title'] = title

    subtitle = page.xpath('//*[@id="main-container"]/div[3]/div/header/div[2]/text()')[0]
    result['Article']['SubTitle'] = subtitle

    lead = page.xpath('//*[@id="main-container"]/div[3]/div/header/p/text()')[0]
    result['Article']['Lead'] = lead.strip()

    paragraphs = page.xpath('//*[@id="main-container"]/div[3]/div/div[2]/article/p/descendant-or-self::*/text()')
    result['Article']['Content'] = '\n'.join(paragraphs)

    result = json.dumps(result, indent=4, ensure_ascii=False)
    print(result)

def parseBolha(filename):
    # Get html document
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    file = open(filename, 'rb')
    page = html.fromstring(file.read())
    file.close()

    # Get elements
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    featured = [i.get('class') == "ad featured" for i in page.xpath('//*[@id="list"]/div[@class="ad featured" or @class="ad"]')]

    titles = page.xpath('//*[@id="list"]/div[@class="ad featured" or @class="ad"]/div[@class = "coloumn content"]/h3/a/@title')

    content = page.xpath('//*[@id="list"]/div[@class="ad featured" or @class="ad"]/div[@class = "coloumn content"]/child::b/text() |'
                         '//*[@id="list"]/div[@class="ad featured" or @class="ad"]/div[@class = "coloumn content"]/text()')

    # Clean text (also join it, not sure how this could be done using pure XPATH)
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    tmp = []
    wholeLine = ''
    for line in content:
        text = line.strip()

        if text == '' and wholeLine != '':
            tmp.append(wholeLine.replace('\n', ' ').strip())
            wholeLine = ''
        else:
            wholeLine += ' ' + text
    tmp.append(wholeLine.replace('\n', ' ').strip())

    price = page.xpath('//*[@id="list"]/div[@class="ad featured" or @class="ad"]/div[@class = "coloumn prices"]/div[@class = "price"]/span/text()')

    # Pack it up in JSON
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    result = {'Items': []}
    for i in range(len(price)):
        result['Items'].append({'Title':titles[i], 'Price': price[i], 'Description': tmp[i], 'Featured': featured[i]})

    result = json.dumps(result, indent=4, ensure_ascii=False)

    print(result)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid number of arguments.')

    elif sys.argv[1] == 'over1':
        parseOverstock('../input/jewelry01.html')
    elif sys.argv[1] == 'over2':
        parseOverstock('../input/jewelry02.html')
    elif sys.argv[1] == 'rtv1':
        parseRTV('../input/audi.html')
    elif sys.argv[1] == 'rtv2':
        parseRTV('../input/volvo.html')
    elif sys.argv[1] == 'other1':
        parseBolha('../input/xbox_bolha.html')
    elif sys.argv[1] == 'other2':
        parseBolha('../input/ps4_bolha.html')
    else:
        print('Invalid argument. Look at the code.')

