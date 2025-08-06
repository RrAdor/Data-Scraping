 Data-Scraping
 # Data-Scraping
cd C:/programfiles/Mongodb/Server/8.0/bin/mongod.exe           #run the MongoDB server
MongoDB Compass/connect to localhost 27017/
venv\scripts\activate                                          #activate the virtual environment
cd news_scraper                                                #go to the root project
scrapy crawl news -a portal_url="https://www.prothomalo.com"
