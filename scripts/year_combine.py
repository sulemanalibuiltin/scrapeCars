vehicle_type = 'mpv'

cl = open('real-first-'+vehicle_type+'s-list', 'r')
allcl = cl.readlines()
cl.close()

vehicles = dict()

for item in allcl:
	me, mlyr = item.split('","', 1)
	make = me[1:].strip()
	model, year = mlyr.strip().split('",', 1)
	if make not in vehicles:
		vehicles[make] = dict()
	if model not in vehicles[make]:
		vehicles[make][model] = []
	vehicles[make][model].append(int(year))

cy = open('combined-years-'+vehicle_type+'s-list', 'w')

for make in vehicles:
	for model in vehicles[make]:
		model_years = vehicles[make][model]
		num_years = len(model_years)
		if num_years == 1:
			write_str = '"' + make + '","' + model + '",' + str(model_years[0]) + '\n'
			cy.write(write_str)
		else:
			start_year = model_years[0]
			curr_years = [start_year]
			for i in range(1,num_years):
				end_year = model_years[i]
				if (end_year - start_year) < 4:
					curr_years.append(end_year)
				else:
					if len(curr_years) == 1:
						write_str = '"' + make + '","' + model + '",' + str(curr_years[0]) + '\n'
					else:
						write_str = '"' + make + '","' + model + '",' + str(curr_years[0]) + ',' + str(curr_years[-1]) + '\n'
					start_year = end_year
					curr_years = [start_year]
					cy.write(write_str)
			if len(curr_years) == 1:
				write_str = '"' + make + '","' + model + '",' + str(curr_years[0]) + '\n'
			else:
				write_str = '"' + make + '","' + model + '",' + str(curr_years[0]) + ',' + str(curr_years[-1]) + '\n'
			cy.write(write_str)
cy.close()