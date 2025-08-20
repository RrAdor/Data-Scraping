# article and video summarizer
cd C:/programfiles/Mongodb/Server/8.0/bin/mongod.exe           #run the MongoDB server
MongoDB Compass/connect to localhost 27017/

IF WE WANT TO see the data scraping part in the terminal:
venv\scripts\activate                                          #activate the virtual environment
cd news_scraper                                                #go to the root project
scrapy crawl news -a portal_url="https://www.prothomalo.com"

IF WE ONLY WANT TO CHECK THE full functional project:
cd newsarticle
python manage.py runserver
