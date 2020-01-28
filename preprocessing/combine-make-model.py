import os
import shutil

from tqdm import tqdm

data_dir = 'all'
output_dir = 'combined_all'

append_string = '='

if not os.path.exists(output_dir):
	os.mkdir(output_dir)

makes = os.listdir(data_dir)
for make in tqdm(makes):
	make_dir = os.path.join(data_dir, make)
		
	models = os.listdir(make_dir)
	for model in models:
		model_dir = os.path.join(make_dir, model)
		dst_make_model_dir = os.path.join(output_dir, make + append_string + model)

		if not os.path.exists(dst_make_model_dir):
			os.mkdir(dst_make_model_dir)

		category_filenames = [os.path.join(model_dir, f) for f in os.listdir(model_dir)]
		for category_filename in category_filenames:
			shutil.copy(category_filename, dst_make_model_dir)
			
