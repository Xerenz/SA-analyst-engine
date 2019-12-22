'''need to find out all the information 
about a malware given its name 
possibly some other parameters'''

''' Use case: We need to determine what kind of threat was detected 
(what was the user behavior which caused the threat to be downloaded on the machine)'''

'''
test1 = {'Infection Channel': 'Via removable drives, Downloaded from the Internet, Dropped by other malware', 
		'ALIASES': 'VBS/Agent.NDH(ESET-NOD32); HEUR:Worm.Script.Generic(Kaspersky); Worm.VBS.Agent(Ikarus)', 
		'PLATFORM': 'Windows 2000, Windows Server 2003, Windows XP (32-bit, 64-bit), Windows Vista (32-bit, 64-bit), Windows 7 (32-bit, 64-bit)', 
		'OVERALL RISK RATING': 'LOW', 
		'DAMAGE POTENTIAL': 'MEDIUM', 
		'DISTRIBUTION POTENTIAL': 'MEDIUM', 
		'REPORTED INFECTION': 'LOW', 
		'INFORMATION EXPOSURE': 'MEDIUM', 
		'Threat Type': ' Worm', 
		'Destructiveness': ' No', 
		'Encrypted': ' Yes', 
		'In the wild': ' Yes'}

test2 = {'Infection Channel': 'Dropped by other malware, Via removable drives', 
		'ALIASES': 'Worm:VBS/Jenxcus!lnk(Microsoft), VBS/Autorun.worm.aadd!lnk(McAfee), Troj/JenxLnk-B(Sophos), LNK/Agent.AK trojan(Eset), VBS/Autorun.BC.worm(Panda)', 
		'PLATFORM': 'Windows 2000, Windows Server 2003, Windows XP (32-bit, 64-bit), Windows Vista (32-bit, 64-bit), Windows 7 (32-bit, 64-bit)', 
		'OVERALL RISK RATING': 'LOW', 
		'DAMAGE POTENTIAL': 'LOW', 
		'DISTRIBUTION POTENTIAL': 'MEDIUM', 
		'REPORTED INFECTION': 'LOW', 
		'INFORMATION EXPOSURE': 'LOW', 
		'Threat Type': ' Trojan', 
		'Destructiveness': ' No', 
		'Encrypted': ' No', 
		'In the wild': ' Yes'}

test3 = {'Infection Channel': 'Downloaded from the Internet', 
		'PLATFORM': 'Linux', 
		'OVERALL RISK RATING': 'LOW', 
		'DAMAGE POTENTIAL': 'MEDIUM', 
		'DISTRIBUTION POTENTIAL': 'LOW', 
		'REPORTED INFECTION': 'LOW', 
		'INFORMATION EXPOSURE': 'LOW', 
		'Threat Type': ' Trojan', 
		'Destructiveness': ' No', 
		'Encrypted': ' No', 
		'In the wild': ' Yes'} 
'''


from bs4 import BeautifulSoup

import requests
import json
import sys

## global variables 

url = 'https://www.trendmicro.com/vinfo/us/threat-encyclopedia/malware/'
keys, values = [], []


'''
extract_class function to scrape:
	Threat Type
	Destructiveness 
	Encrypted 
	In the wild'''

def extract_class(classify):
	clist = [c for c in classify.descendants if c.name is None]
	for c in clist:
		k, v = c.strip().split(':')
		keys.append(k)
		values.append(v)

	return dict(zip(keys, values))


''' 
extract_details function to scrape labels:
	OVERALL RISK RATING 
	DAMAGE POTENTIAL
	DISTRIBUTION POTENTIAL
	DISTRIBUTION POTENTIAL
	REPORTED INFECTION
	INFORMATION EXPOSURE'''

def extract_details(details):
	for tag in details.descendants:
		if tag.name == 'strong':
			keys.append(tag.text[:-1].replace(' \xa0', ''))
		elif tag.name == 'p':
			values.append(tag.text)
		elif (tag.name == 'img' and
			tag.get('title') is not None):
			values.append(tag['title'])

	return dict(zip(keys, values))


'''extract_channel to scrape Infection Channel'''

def extract_channel(channel):
	data = {}
	k, v = channel.text.split(':')
	data[k] = v.strip()

	return data

'''Combine 3 dicts'''

def main_data(soup):
	channel = soup.find('div', class_='labelHeader')
	details = soup.find('div', class_='malwareHeader')
	classify = soup.find('div', class_='iconDetails')

	main = {}

	for d in [extract_channel(channel), extract_details(details), extract_class(classify)]:
		for k, v in d.items():
			main[k] = v

	return main

'''Search for a query in the Trend Threat Encyclopedia
Handle exceptions and check if the query was valid'''

def simple_search(name):
	name = name.strip().lower()
	try:
		response = requests.get(url + name)
	except requests.exceptions.RequestException as e:
		print(e)
		sys.exit(0) # exit out of execution on exception
	else:
		soup = BeautifulSoup(response.content, 'lxml')
		title_tag = soup.find('title') 
		title_text = title_tag.text
		if 'Search' in title_text:
			return ["Invalid query : {}".format(name)], False
		return soup, True


## test
if __name__ == '__main__': 
	# test set

	# invalid case
	invalid = 'DFRZ.TGCHGbv'

	malwares = ['Trojan.SH.KERBERDS.A', 
				'Trojan.JS.KOVCOREG.A',
				'Rootkit.Linux.SKIDMAP.A',
				'Coinminer.Win64.MALXMR.TIAOODBZ',
				'Backdoor.Linux.BASHLITE.SMJC2',
				'ELF_SETAG.SM',
				invalid,]

	for mal in malwares:
		result, valid = simple_search(mal)
		print('\n', mal)
		if valid:
			print(json.dumps(main_data(result), indent=4))
		else:
			print(result)
