#script for automating dad's machinery pricing job

import os, sys, requests, json, csv, datetime, time
from bs4 import BeautifulSoup, NavigableString
import yagmail

if datetime.datetime.today().weekday() == 6:
	loggingfile = 'tracking.txt'
	file = f'mascusfortnightly{datetime.datetime.today().date()}.csv'

	with open(loggingfile, 'a', encoding='UTF8') as f:
		f.write(f"script starting at {datetime.datetime.now()} \n")
		f.close()

	with open(file, 'w', encoding='UTF8') as f:
		writer = csv.writer(f)

		header = ['category', 'title', 'price', 'location', 'year', 'usage']

		writer.writerow(header)

		for page_number in range(10):
			results = []
			url = f'https://www.mascus.co.uk/+/has%3dprice/+/{page_number},100,createdate_desc,search.html'
			page = requests.get(url)
			soup = BeautifulSoup(page.content, 'html.parser')
			page_results = soup.find_all('li', class_='col-row single-result')
			
			for i in page_results:
				title_div = i.findChild("a" , class_='title-font', recursive=True)
				title = title_div.get_text()
				price_div = i.findChild("span" , class_='title-font no-ws-wrap', recursive=True)
				result_details_div = i.findChild("p", class_='result-details', recursive=True)
				details = list(result_details_div.children)
				filtered_details = [x for x in details if isinstance(x, NavigableString) == True]
				category = filtered_details[0]
				location = filtered_details[-1]
				usage = 'N/A'
				year = 'N/A'
				for d in filtered_details:
					if ' h' in d and d[-1] == 'h':
						usage = d
					try: 
						y = int(d[1:])
					except:
						y = -1

					if y != -1:
						year = d
				if price_div:
					price = price_div.get_text()

					results.append([category, title, price, location, year, usage])
			

			for i in results:
				writer.writerow(i)
			time.sleep(0.1)
			print(f'fileupdated with {len(results)} more rows' )

	with open(loggingfile, 'a', encoding='UTF8') as f:
		f.write(f"data scraping finished at {datetime.datetime.now()} \n")
		f.close()
					
		
	yag = yagmail.SMTP('mascusdaily@gmail.com', os.getenv('MASCUS_EMAIL_PW'))
	print(file)

	contents = 'Here are the most recent 10 pages from mascus'

	yag.send(to='afgray48@gmail.com', subject='Weeklu Mascus Email', contents=contents, attachments=file)

	with open(loggingfile, 'a', encoding='UTF8') as f:
		f.write(f"email sent at {datetime.datetime.now()} \n")
		f.close()


	print('script completed succesfully')

else:
	print('Not Monday no scraping needed')		

		
