from selenium import webdriver as WD
from bs4 import BeautifulSoup as BS
import time
import csv
import requests

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = WD.Chrome("/Users/iosdev/Downloads/chromedriver")
browser.get(START_URL)
time.sleep(10)

headers = ["NAME", "LIGHT YEARS FROM EARTH", "PLANET MASS", "STELLAR MAGNITUDE", "DISCOVERY DATE", "HYPERLINK", "PLANET TYPE", "DISCOVERY DATE", "PLANET MASS", "PLANET RADIUS", "ORBITAL RADIUS", "ORBITAL PERIOD", "ECCENTRICITY"]
planet_data = []
newPlanetData = []

def scrape():
    for i in range(0,430) : 
        soup = BS(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}) : 
            li_tags = ul_tag.find_all("li")
            tempList = []
            # enumerate fnc. will fetch value of index and element
            for index, li_tag in enumerate(li_tags) : 
                if index == 0 : 
                    tempList.append(li_tag.find_all("a")[0].contents[0])

                else:
                    try:
                        tempList.append(li_tag.contents[0])
                    except:
                        tempList.append("")
                        hlinkLI = li_tags[0]
                        tempList.append("https://exoplanets.nasa.gov/"+hlinkLI.find_all("a",href=True)[0]["href"])
                
            planet_data.append(tempList)
        
        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()



# Hl stands for HYPERLINK
def scrapeMoreData(Hl) : 
    try:
        page = requests.get(Hl)
        Soup = BS(page.contents, "html.parcer")
        tempList = []

        for tr_tag in Soup.find_all("tr", attrs={"class":"fact_row"}) : 
            td_tags = tr_tag.find_all("td")

            for td_tag in td_tags : 
                try:
                    tempList.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                
                except:
                    tempList.append("")
        
        newPlanetData.append(tempList)
    
    except:
        time.sleep(1)
        scrapeMoreData(Hl)

scrape()
for data in planet_data :
    scrapeMoreData(data[5])
finalPlanetData = []

for index, data in enumerate(planet_data) : 
    # newPDE stands for New Planet Data Element
    # newPDE = newPlanetData[index]
    finalPlanetData.append(data + finalPlanetData[index])

    with open("FinalData.csv", "w") as f :
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(finalPlanetData)

