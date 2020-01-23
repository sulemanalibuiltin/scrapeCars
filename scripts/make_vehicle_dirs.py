from scrape_links import readVehicles
import os
import errno

def main():
	vehicle_type = 'mpv'
	if os.path.exists(os.path.dirname(vehicle_type+'s/')):
		print 'main folder already exists, exiting..'
		return
	num_lines, vehicles = readVehicles('final-'+vehicle_type+'s-list')

	for make in vehicles:
		vehicles_make = vehicles[make]
		for model in vehicles_make:
			vehicles_make_model = vehicles_make[model]
			for year_set in vehicles_make_model:
				start_year = year_set[0]
				end_year = year_set[-1]
				if start_year != end_year:
					dname = '{0}/{1}/{2}-{3}/'.format(make, model, start_year, end_year)
				else:
					dname = '{0}/{1}/{2}/'.format(make, model, start_year)
				dir_name = vehicle_type + 's/' + dname.replace(' ', '_')
				os.makedirs(os.path.dirname(dir_name))
				# if not os.path.exists(os.path.dirname(filename)):
				# 	try:
				# 		os.makedirs(os.path.dirname(filename))
				# 	except OSError as exc: # Guard against race condition
				# 		if exc.errno != errno.EEXIST:
				# 			raise

if __name__ == '__main__':
	main()