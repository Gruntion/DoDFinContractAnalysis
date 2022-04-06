from bs4 import BeautifulSoup
import requests

#this code grabs all the Contract Award data from https://www.defense.gov/News/Contracts and writes it to 2 files
#Starting with 07/01/2014 File Names are Contract_Data_1of2 and... 2of2.

#[NOTE]:FUNCTION "NavigatePages()" is currently tailored to run on a particular site, when expanding
#to collect data from a wider range of sources the majority of the changes will be made here.

#This is the main Function of this code, all other functions are called as a result of this function
#running.
def NavigatePages():

    for i in range(194, 74, -1):
        #Debugging Purposes -ignore-
        print(str(i))

        #if and elif (else-if) statements Bounds Checking.. displays an error if the variable that represents the changing page,
        #number changes to something outside our needs.
        if(i == 0):
            print("Scraping Complete")
        elif(i == 195):
            print("Out_Of_Bounds")
            break

        else:
            url = ("https://www.defense.gov/News/Contracts/?Page=" + str(i))
            html_document = GetHTMLdocument(url)
            soup = BeautifulSoup(html_document, 'html.parser')
            contract_list = soup.find_all('listing-titles-only')
            ReverseArticles(contract_list, "Contract_Data_1of2.txt")

    for i in range(74, 0, -1):
        # Debugging Purposes -ignore-
        print(str(i))
        if (i == 0):
            print("Scraping Complete")
        elif (i == 195):
            print("Out_Of_Bounds")
            break
        else:
            url = ("https://www.defense.gov/News/Contracts/?Page=" + str(i))
            html_document = GetHTMLdocument(url)
            soup = BeautifulSoup(html_document, 'html.parser')
            contract_list = soup.find_all('listing-titles-only')
            ReverseArticles(contract_list, "Contract_Data_2of2.txt")

#Articles on each page come in from most recent to least, this function reverses them
#so that they can be written to file in order from past to present for simplicity.
def ReverseArticles(contract_list, file_name):
    for contract in reversed(contract_list):
        link = contract['article-url']
        html_document = GetHTMLdocument(link)
        soup = BeautifulSoup(html_document, 'html.parser')

        cdate = soup.find("h1", class_="maintitle")
        body_text = soup.find("div", class_="body")

        WriteArticle(cdate, body_text, file_name)

#This Writes Each Article into a file with the name that is passed in the NavigatePages() Function
def WriteArticle(contract_date, contract, file_name):
    f = open(file_name, "a")
    f.write(contract_date.text)
    f.close()
    f = open(file_name, "a", encoding="utf-8")
    f.write(contract)
    f.close()

#Function is invoked by passing a url as an argument
#The Websites page data is then collected and then organized into Unicode
#(a conversion that allows the page data be easily handled and written to file.)
def GetHTMLdocument(url):
    response = requests.get(url)
    return response.text

#"Calls" NavigatePages Function
#This is the line that tells everything to compute.
NavigatePages()