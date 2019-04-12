import codecs
import requests
import time
import io
import re
import sys
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup as soup

def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def getTag(parent_tag, tag_type, tag_attribute, tag_value):

    return parent_tag.find(tag_type, {tag_attribute:tag_value})

agent = requests.utils.default_headers()
agent.update({
    "User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
})

mainPage = requests.get('https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=1', headers=agent)

csv = open("good_reads_data.csv", "w")

csv.write("title, author, rating, format, pages, publish_date\n")


count = 0
while mainPage.status_code == 200:
    parsed = soup(mainPage.content, 'html.parser')
    mainPage.close()
    books = parsed.findAll("a", {"class":"bookTitle", "itemprop":"url"})
#     print(books)
    print(len(books))
    for i in range(len(books)):
        book_href = "https://www.goodreads.com" + books[i]['href']
        #print(book_href)

        if ((count % 100) == 0):

            time.sleep(3)
        bookPage = requests.get(book_href, headers=agent)
        if bookPage.status_code == 200:
            parsedBookPage = soup(bookPage.content, 'html.parser')
            bookPage.close()
            #f1.write(str(bookPage.content))
            title = books[i].span.text
            title = re.sub('[,]' , '', title)
            # print("Title: " + title)
            authorName = getTag(parsedBookPage, "a", "class", "authorName")
            if authorName == None:
                authorName = u''
            else:
                authorName = authorName.span.text
            # print("Author Name: " + authorName)
            rating = getTag(parsedBookPage, "span", "itemprop", "ratingValue")  #parsedBookPage.find("span", {"itemprop":"ratingValue"})
            if rating == None:
                  rating = u''
            else:
                  rating = rating.text.strip()
            print("Rating:" + rating+":")
            bookFormat = getTag(parsedBookPage, "span", "itemprop", "bookFormat")  #parsedBookPage.find("span", {"itemprop":"bookFormat"})
            if bookFormat == None:
                bookFormat = u''
            else:
                bookformat = bookFormat.text
            print("format: " + bookformat)
            pages = getTag(parsedBookPage, "span", "itemprop", "numberOfPages")  #parsedBookPage.find("span", {"itemprop":"numberOfPages"})

            details = getTag(parsedBookPage, "div", "id", "details")  #parsedBookPage.find("div", {"id": "details"})
            details_div = details.find_all("div", {"class": "row"})
            publish_date = ""
            for divs in details_div:

                if divs.text and "Published" in str(divs.text):
                    div_split = divs.text.split()
                    index = div_split.index("Published")
                    end_index = index + 1
                    while True :
                        if end_index > len(div_split) or representsInt(div_split[end_index - 1]):
                            break
                        end_index = end_index + 1

                    publish_date = ' '.join(div_split[index+1:end_index])
            # print(publish_date)


            if pages == None:
                pages = u''
            else:
                pages = pages.text.split(' ')[0]

            # print("pages: " + pages)
            out_string = title + ',' + authorName + ',' + rating + ',' + bookformat + ',' + pages + ',' + publish_date +'\n'
            # out_string = '~'.join((title, authorName, rating, bookformat, pages)).strip()
            print(out_string)
            csv.write(out_string)
            print(count)
            count = count + 1
            # print("Book " + repr(count))

    if (count >= 3000):
        break
    p = parsed.find("div", {"class":"pagination"})
    p = p.find("a", {"class":"next_page"})['href']
    nextLink = "https://www.goodreads.com" + p
    mainPage = requests.get(nextLink, headers=agent)
    #print(nextLink)

csv.close()