import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

data = []
dfs = []
webpage_urls = ["https://data.gov.au/dataset?q=&groups=business&sort=extras_harvest_portal+asc%2C+score+desc%2C+metadata_modified+desc&_organization_limit=0&organization=reservebankofaustralia&_groups_limit=0",
                "https://data.gov.au/dataset?q=&groups=business&sort=extras_harvest_portal+asc%2C+score+desc%2C+metadata_modified+desc&_organization_limit=0&organization=department-of-finance&_groups_limit=0",
                "https://data.gov.au/dataset?q=&groups=business&sort=extras_harvest_portal+asc%2C+score+desc%2C+metadata_modified+desc&_organization_limit=0&organization=departmentofagriculturefisheriesandforestry&_groups_limit=0",
                "https://data.gov.au/dataset?organization=department-of-communications&q=&groups=business&sort=extras_harvest_portal+asc%2C+score+desc%2C+metadata_modified+desc&_organization_limit=0&_groups_limit=0",
                "https://data.gov.au/dataset?organization=ip-australia&q=&groups=business&sort=extras_harvest_portal+asc%2C+score+desc%2C+metadata_modified+desc&_organization_limit=0&_groups_limit=0",
                "https://data.gov.au/dataset?q=&organization=australiancommunicationsandmediaauthority&groups=business&sort=extras_harvest_portal+asc%2C+score+desc%2C+metadata_modified+desc&_organization_limit=0&_groups_limit=0",
                "https://data.gov.au/dataset?q=&organization=www-mitchellshirecouncil-vic-gov-au&groups=business&sort=extras_harvest_portal+asc%2C+score+desc%2C+metadata_modified+desc&_organization_limit=0&_groups_limit=0",
                "https://data.gov.au/dataset?q=&groups=business&sort=extras_harvest_portal+asc%2C+score+desc%2C+metadata_modified+desc&_organization_limit=0&organization=digital-transformation-agency&_groups_limit=0"]

# fetching data from all urls

for i in webpage_urls:
    wiki2 = i
    page= urllib.request.urlopen(wiki2)
    soup = BeautifulSoup(page, "lxml")

    lobbying = {}
    #always only 2 active li, so select first by [0]  and second by [1]
    org = soup.find_all('li', class_="nav-item active")[0].span.get_text()
    groups = soup.find_all('li', class_="nav-item active")[1].span.get_text()

    data2 = soup.find_all('h3', class_="dataset-heading")
    for element in data2:
        lobbying[element.a.get_text()] = {}
    data2[0].a["href"]
    prefix = "https://data.gov.au"
    for element in data2:
        lobbying[element.a.get_text()]["link"] = prefix + element.a["href"]
        lobbying[element.a.get_text()]["Organisation"] = org
        lobbying[element.a.get_text()]["Group"] = groups
        #print(lobbying)
        df = pd.DataFrame.from_dict(lobbying, orient='index') \
               .rename_axis('Titles').reset_index()
        dfs.append(df)
df = pd.concat(dfs, ignore_index=True)
df1 = df.drop_duplicates(subset = 'Titles').reset_index(drop=True)



df1['Organisation'] = df1['Organisation'].str.replace('\(\d+\)', '')
df1['Group'] = df1['Group'].str.replace('\(\d+\)', '')

with pd.option_context('display.max_rows', 999):
    print (df1)
df1.to_csv('D:/output_new.csv')