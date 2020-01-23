import requests,json;
from tqdm import tqdm

#makes_url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
vehicle_type = 'mpv'
start_year = 2000
end_year = 2018

makes_url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/' + vehicle_type + '?format=json'
makes_request = requests.get(makes_url);
makes = makes_request.json()[u'Results']

file = open('initial-'+vehicle_type+'s-list', 'w+')
fail = open(vehicle_type+'s-fail', 'a+')
fail.write('\n')

for make in tqdm(makes):
# for i in tqdm(range(3)):
	# make = makes[i]
	make_id = make[u'MakeId']
	make_name = make[u'MakeName'].strip()

	for model_year in range(start_year, end_year+1):
		# model_url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/' + make_id + '?format=json'
		model_url = 'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeIdYear/makeId/' \
					+ str(make_id) + '/modelyear/' \
					+ str(model_year) + '/vehicleType/' \
					+ vehicle_type + '?format=json'

		models_request = requests.get(model_url);
		# print model_url
		# print models_request
		try:
			models = models_request.json()[u'Results']
		except:
			fail_string = 'request failed: '+ str(make_id) + ' ' + make_name + ' ' + str(model_year) + '\n'
			fail.write(fail_string)
			# print fail_string
			continue
		for model in models:
			model_name = model[u'Model_Name'].strip()
			make_model_year = '"' + make_name + '","' + model_name + '",' + str(model_year) + '\n'
			# print make_model_year
			file.write(make_model_year)
	file.flush()
	fail.flush()

fail.close()
file.close()