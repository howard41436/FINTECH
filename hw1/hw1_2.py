'''
Required Modules:
requests, calendar, tabulate, bs4, pandas
Usage:
python3 hw1_2.py
'''
import requests, calendar, tabulate
from bs4 import BeautifulSoup
import pandas as pd
def transform_date(row):
	org = row[0]
	month, year = row[0].split('-')
	if month == 'Sept':
		month = 'Sep'
	year = int('20' + year)
	month = list(calendar.month_abbr).index(month)
	date = calendar.monthrange(year, month)[1]
	return '{}-{}{}-{}'.format(year, ('', '0')[int(month < 10)], month, date)
url = "http://www.finra.org/investors/margin-statistics"

r = requests.get("http://www.finra.org/investors/margin-statistics")
soup = BeautifulSoup(r.text, "html.parser")
table = soup.find_all('table')
df = pd.DataFrame()
for i,tab in enumerate(table):
	tmp = pd.read_html(str(tab))
	drp = list(tmp[0].index.values)[-1]
	if tab == table[0]:
		tmp[0] = tmp[0].drop([drp])
		df = pd.DataFrame(tmp[0])
	else:
		tmp[0] = tmp[0].drop([drp])
		df = pd.concat([df, pd.DataFrame(tmp[0])], axis = 0)
	if i > 8:
		break
df['Date'] = df.apply(transform_date, axis = 1)
df['Value'] = df.apply(lambda row: int(row[2] + row[3] - row[1]), axis = 1)
df = df.drop(columns = list(df.columns.values)[:4])
df.index = [''] * len(df)
print(tabulate.tabulate(df.head(20), headers = 'keys', tablefmt = 'psql', showindex = False))
