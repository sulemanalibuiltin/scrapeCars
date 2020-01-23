import json
from hashlib import md5
from urllib2 import Request
from urllib2 import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm

# read the make and model from a file
# file is in format of:
# make,model,start_year,end_year(optional)
def readVehicles(vehicleFile):
	vehicles = dict()
	cl = open(vehicleFile, 'r')
	allcl = cl.readlines()
	cl.close()

	for item in allcl:
		me, mlyr = item.split('","', 1)
		make = me[1:].strip()
		model, years = mlyr.strip().split('",', 1)
		year_s = [int(x) for x in years.split(',', 1)]
		if make not in vehicles:
			vehicles[make] = dict()
		if model not in vehicles[make]:
			vehicles[make][model] = []
		vehicles[make][model].append(year_s)
	return len(allcl), vehicles

# download a file with a given user-agent string
def get_soup(url, header):
	# return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,
	# headers=header)), 'html.parser')
	return BeautifulSoup(urlopen(Request(url, headers=header)), 'html.parser')

# format item metadata
def makeLine(make, model, start_year, end_year, img, Type):
	d = dict()
	d['make'] = make
	d['model'] = model
	d['start_year'] = start_year
	if start_year != end_year:
		d['end_year'] = end_year
		text = '' + start_year + end_year + make + model + img
	else:
		text = '' + start_year + make + model + img
	m = md5()
	m.update(text.encode('utf-8'))
	d['hash'] = m.hexdigest()
	if start_year != end_year:
		fname = '{0}/{1}/{2}-{3}/{4}.{5}'.format(make, model, start_year, end_year, d['hash'], Type)
	else:
		fname = '{0}/{1}/{2}/{3}.{4}'.format(make, model, start_year, d['hash'], Type)
	d['filename'] = fname.replace(' ', '_')
	d['url'] = img
	return d

# for a specific make model and years of vehicle attempt to get num images
def getVehicle(makeIn, modelIn, start_yearIn, end_yearIn, num, outFile, outError):
	make = makeIn.replace(' ', '+')
	model = modelIn.replace(' ', '+')
	query = '{0}+{1}+{2}'.format(start_yearIn, make, model)
	if start_yearIn != end_yearIn:
		query = '{0}+{1}+{2}+{3}'.format(start_yearIn, end_yearIn, make, model)

	# query with no usage rights
	url = 'https://www.google.com/search?q=' + query + '&source=lnms&tbm=isch'

	# return images with appropriate usage rights
	# url = 'https://www.google.com/search?q=' + query + '&tbs=sur:fc&tbm=isch'

	header = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
	try:
		soup = get_soup(url, header)
		ActualImages = []
		for a in soup.find_all('div', {'class': 'rg_meta'}):
			link, Type = json.loads(a.text)['ou'], json.loads(a.text)['ity']
			ActualImages.append((link, Type))

		for i, (img, Type) in enumerate(ActualImages[:num]):
			if Type is not None:
				# write out where to get the image from
				data = makeLine(makeIn, modelIn, start_yearIn, end_yearIn, img, Type)
				outFile.write(json.dumps(data) + '\n')

	except:
		# spout some error messages when things go poorly
		data = makeLine(makeIn, modelIn, start_yearIn, end_yearIn, img, 'FAIL')
		outError.write(json.puts(data) + '\n')

def main(imagesPerMakeModel=100):
	vehicle_type = 'truck'
	num_lines, vehicles = readVehicles('final-'+vehicle_type+'s-list')
	# num_lines, vehicles = readVehicles('short-'+vehicle_type+'-list')

	# outFile = open('dataset', 'w')
	# outError = open('errorset', 'w')
	outFile = open(vehicle_type+'s-dataset', 'w')
	outError = open(vehicle_type+'s-errorset', 'w')

	print 'Total lines', num_lines
	pbar = tqdm(total=num_lines)
	for make in vehicles:
		vehicles_make = vehicles[make]
		for model in vehicles_make:
			vehicles_make_model = vehicles_make[model]
			for year_set in vehicles_make_model:
				getVehicle(
					make,
					model,
					str(year_set[0]),
					str(year_set[-1]),
					imagesPerMakeModel,
					outFile,
					outError)
				outFile.flush()
				outError.flush()
				pbar.update(1)
	pbar.close()
	outFile.close()
	outError.close()

if __name__ == '__main__':
	main()
