import requests
import re
import time
import sys
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup as soup

agent = requests.utils.default_headers()
agent.update({
    "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
})
#arr = ["https://www.amazon.com/s?k=fiction&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=mystery&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=mystery&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=sex&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=dating&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=religion&i=stripbooks&ref=nb_sb_noss"]
arr = ["https://www.amazon.com/s?k=religion&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=sex&i=stripbooks&ref=nb_sb_noss","https://www.amazon.com/s?k=religion&i=stripbooks&ref=nb_sb_noss"]
htmlpage = requests.get(arr[0], headers=agent)
arr_count = 1
csv = open("amazonn.csv", "w", encoding='utf=8')
csv.write("name, author, rating, format, year\n")
check = 0
while htmlpage.status_code == 200:
    # print(arr[0])
    mysoup = soup(htmlpage.content, 'html.parser')
    # print(soup)
    htmlpage.close()
    # print(mysoup.findAll("div",{"class":"sg-row"}))
    books=mysoup.findAll("div", {"class":"sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"})
    #books = mysoup.findAll("div", {"class":"sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"})
# sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28
# sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28
    # sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28
    print(len(books))
    for i in range(0,len(books)):
        title = books[i].find("h5", {"class":"a-color-base s-line-clamp-2"}).find("span", "a-size-medium a-color-base a-text-normal")
        year = books[i].find("span", {"class":"a-size-base a-color-secondary a-text-normal"})
        if year == None:
            year = ''
        else:
            year = year.text.split(' ')
            if (len(year) == 3):
                year = year[2]
            else:
                year = ''
        authorName = books[i].find("div", {"class":"a-row a-size-base a-color-secondary"})
        if (authorName == None):
            authorName = ''
        else:
            authorName = authorName.find("a","a-size-base a-link-normal")
            if (authorName == None):
                authorName = ''
            else :
                authorName = authorName.text.strip()
        bookFormat = books[i].find("div",{"class":"a-row a-size-base a-color-base"}).find("a",{"class":"a-size-base a-link-normal a-text-bold"})
        if bookFormat == None:
            bookFormat = ''
        else:
            bookFormat = bookFormat.text.strip()
        rating = books[i].find("span", {"class":"a-icon-alt"})
        if(rating==None):
            rating = ''
        else:
            rating = rating.text
            rating = rating.split()[0]
        p1 = books[i].find("div", {"class":"a-section a-spacing-none a-spacing-top-small"})
        price = p1.find("span", {"class":"a-price-whole"})
        fraction = books[i].find("span", {"class":"a-price-fraction"})
        if price == None:
            price = ''
        else:
            price = price.text
            price = re.sub('[,]', '', price)
        if fraction==None:
            fraction = ''
        else:
            fraction = fraction.text
        price = price + fraction
        row = str(title.text).replace(",", "~") + "," + str(authorName).replace(",", "~") + "," + str(rating).replace(",", "~") + "," + str(bookFormat).replace(",", "~") + "," + str(year).replace(",", "~") +"\n"
        csv.write(row)
        # with csv:
        #     spamwriter = csv.writer(csv, delimiter='~')
        #     spamwriter.writerow(ans)
        check = check + 1
    if (check > 1000 ):
        break
    p = mysoup.findAll("div", {"class":"a-section s-border-bottom"})[0].find("li",{"class":"a-last"})
    if ((check % 25) == 0):
            time.sleep(4)
    print(p)
    
    # if mysoup.findAll("div", {"class":"a-section s-border-bottom"})[0].find("li",{"class":"a-disabled a-last"})!=None:
    #     htmlpage = requests.get(arr[arr_count], headers=agent)
    #     arr_count=arr_count+1
    #     mysoup = soup(htmlpage.content, 'html.parser')
    # # print(mysoup)
    #     htmlpage.close()
    #     books = mysoup.findAll("div", {"class":"sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"})
    
    # else:
    p = mysoup.findAll("div", {"class":"a-section s-border-bottom"})[0].find("li",{"class":"a-last"}).find("a")["href"]
    print (p)
    nextLink = "https://www.amazon.com" + p
    print(nextLink)
    if ((check % 50) == 0):
        time.sleep(4)
    htmlpage = requests.get(nextLink, headers=agent)
csv.close()
