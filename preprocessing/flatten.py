import os
import shutil

from tqdm import tqdm

data_dir = 'dataset'

DS_Store_name = '.DS_Store'

makes = os.listdir(data_dir)
for make in tqdm(makes):
	make_dir = os.path.join(data_dir, make)

	ds_file = os.path.join(make_dir, DS_Store_name)
	if os.path.exists(ds_file):
		os.remove(ds_file)
		
	models = os.listdir(make_dir)
	for model in models:
		model_dir = os.path.join(make_dir, model)

		ds_file = os.path.join(model_dir, DS_Store_name)
		if os.path.exists(ds_file):
			os.remove(ds_file)
		
		year_dirs = [os.path.join(model_dir, y) for y in os.listdir(model_dir)]
		year_dirs = [y for y in year_dirs if os.path.isdir(y)]		
		for year_dir in year_dirs:
			ds_file = os.path.join(year_dir, DS_Store_name)
			if os.path.exists(ds_file):
				os.remove(ds_file)

			filenames = [os.path.join(year_dir, f) for f in os.listdir(year_dir)]
			for filename in filenames:
				shutil.move(filename, model_dir)
			
			os.rmdir(year_dir)
