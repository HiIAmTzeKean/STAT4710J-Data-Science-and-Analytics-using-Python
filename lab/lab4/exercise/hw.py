

import os
import pandas as pd
import numpy as np
import requests
import bs4
import lxml
import re

# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def question1():
    """
    NOTE: You do NOT need to do anything with this function.
    The function for this question makes sure you
    have a correctly named HTML file in the right
    place. Note: This does NOT check if the supplementary files
    needed for your page are there!
    >>> question1()
    >>> os.path.exists('lab06_1.html')
    True
    """
    # Don't change this function body!
    # No python required; create the HTML file.

    return


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------




def extract_book_links(text):
    """
    :Example:
    >>> fp = os.path.join('data', 'products.html')
    >>> out = extract_book_links(open(fp, encoding='utf-8').read())
    >>> url = 'scarlet-the-lunar-chronicles-2_218/index.html'
    >>> out[1] == url
    True
    """
    book_list = []
    soup = bs4.BeautifulSoup(text, 'html.parser')
    star_list = soup.find_all('p','star-rating Four')
    star_list.extend(soup.find_all('p','star-rating Five'))
    for item in star_list:
        url = item.find_next('a').get('href')
        value = re.search(r'[0-9]+.{2}[0-9]', item.find_next(class_="price_color").text).group(0)
        if float(value) >= 50:
            continue
        book_list.append(re.sub(r'^catalogue/','',url))
    return book_list


def get_product_info(text, categories):
    """
    :Example:
    >>> fp = os.path.join('data', 'Frankenstein.html')
    >>> out = get_product_info(open(fp, encoding='utf-8').read(), ['Default'])
    >>> isinstance(out, dict)
    True
    >>> 'Category' in out.keys()
    True
    >>> out['Rating']
    'Two'
    """
    target = {
        'UPC': None,
        'Product Type': None,
        'Price (excl. tax)': None,
        'Price (incl. tax)': None,
        'Tax': None,
        'Availability': None,
        'Number of reviews': None,
        'Category': None,
        'Rating': None,
        'Description': None,
        'Title': None,
    }
    soup = bs4.BeautifulSoup(text, 'html.parser')
    category = soup.find(class_='breadcrumb').find('a',attrs={'href': re.compile("../category/books/.*")}).get('href')
    for topic in categories:
        if re.search(topic,category,re.IGNORECASE):
            target['Category'] = topic
            break
    # book not in category
    if not target['Category']:
        return None

    for item in soup.find_all('th'):
        if item.text in target:
            target[item.text] = item.find_next('td').text
            
    target['Description'] = soup.find('div', id='product_description').find_next('p').text
    target['Title'] = soup.find('div', class_=re.compile('.* product_main$')).h1.text
    
    return target


def scrape_books(k, categories):
    """
    :param k: number of book-listing pages to scrape.
    :returns: a dataframe of information on (certain) books
    on the k pages (as described in the question).
    :Example:
    >>> out = scrape_books(1, ['Mystery'])
    >>> out.shape
    (1, 11)
    >>> out['Rating'][0] == 'Four'
    True
    >>> out['Title'][0] == 'Sharp Objects'
    True
    """
    base_url = 'http://books.toscrape.com/'
    target_url = []
    postfix_url = ''
    target_book = []
    for i in range(5):
        response = requests.get(base_url + postfix_url)
        target_url.extend(extract_book_links(response.text))
        postfix_url = 'catalogue/page-' + str(i+2) + '.html'

    for url in target_url:
        try:
            response = requests.get(base_url + 'catalogue/' + url)
            book = get_product_info(response.text, ['default'])
            if book:
                target_book.append(book)
        except Exception as e:
            print(e)
    return pd.DataFrame(target_book)
    

# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def stock_history(ticker, year, month):
    """
    Given a stock code and month, return the stock price details for that month
    as a DataFrame.

    >>> history = stock_history('BYND', 2019, 6)
    >>> history.shape == (20, 13)
    True
    >>> history.label.iloc[-1]
    'June 03, 19'
    """
    # ticker='BYND'
    # year= 2019
    # month = 6
    dates = pd.date_range(f"{year}-{month}-01", f"{year}-{month+1}-01" ,inclusive="left")
    start_date = str(dates[0].date())
    end_date = str(dates[-1].date())
    api_key = "f6nioD6ObBHqziNSiJXauvxdDsrDoUpL"
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={start_date}&to={end_date}&apikey={api_key}"
    response = requests.get(url)
    df = pd.DataFrame(response.json().get('historical'))
    df['symbol'] = ticker
    return df


def stock_stats(history):
    """
    Given a stock's trade history, return the percent change and transactions
    in billions of dollars.

    >>> history = stock_history('BYND', 2019, 6)
    >>> stats = stock_stats(history)
    >>> len(stats[0]), len(stats[1])
    (7, 6)
    >>> float(stats[0][1:-1]) > 30
    True
    >>> float(stats[1][:-1]) > 1
    True
    >>> stats[1][-1] == 'B'
    True
    """
    history.sort_values('date', inplace=True)
    price_open = history[history.date == history.date.min()].open.iloc[0]
    price_close = history[history.date == history.date.max()].close.iloc[0]
    percentage_change = (price_open - price_close)/price_open * 100
    percentage_change = round(percentage_change, 2)
    history["average price"] = (history.open + history.close)/2
    history["transaction vol"] = history.volume * history["average price"] / 1e9
    total_transaction_vol = history["transaction vol"].sum()
    total_transaction_vol = round(total_transaction_vol, 2)
    
    if percentage_change < 0:
        percentage_change = f"{percentage_change:.2f}%"
    else:
        percentage_change = f"+{percentage_change:.2f}%"
    total_transaction_vol = f"{total_transaction_vol:.2f}B"
    
    return (percentage_change, total_transaction_vol)
