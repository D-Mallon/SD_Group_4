The overall goal of this application is to provide information for users on the Dublin bikes srevices, including station locations, bike capacities, weather, routes, etc.... To this end, the application makes use of a database hosted on AWS, and automated web scrapers to periodically pull data from relevant APIs and write it to the database. This information forms the basis of a web application, with the aforementioend functionalities.

Files:

1. YML Environment: Contains the configurations for the python applications

2. Open Weather API Scraper: Web scraper to periodically collect weather information for Dublin, Ireland

3. Dublin Bikes API Scraper: Web scraper to periodcically collect information on the Dublin Bikes stations

4. Crontab file to run API requests on repeat at 5 minute intervals

- crontab general info for discussion at meeting
  https://www.taniarascia.com/setting-up-a-basic-cron-job-in-linux/
  https://www.cyberithub.com/solved-errors-in-crontab-file-cant-install/
