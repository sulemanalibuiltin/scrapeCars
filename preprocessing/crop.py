import os
import argparse

import cv2
from imageai.Detection import ObjectDetection

execution_path = os.getcwd()
from tqdm import tqdm

parser = argparse.ArgumentParser(description="YOLO car cropped.")
parser.add_argument("--data_dir", type=str,
                      help="The location of the dataset")
parser.add_argument("--output_dir", type=str,
                      help="The location of the dataset")
args = parser.parse_args()

if __name__=='__main__':
	failed_filenames = []	
	
	detector = ObjectDetection()
	detector.setModelTypeAsRetinaNet()
	detector.setModelPath( os.path.join(execution_path , "object-detection-models/resnet50_coco_best_v2.0.1.h5"))
	detector.loadModel(detection_speed="fastest")

	custom_objects = detector.CustomObjects(car=True, truck=True)	
	
	categories = os.listdir(args.data_dir)
	categories.sort()
	
	if not os.path.exists(args.output_dir):
		os.mkdir(args.output_dir)

	for category in tqdm(categories):
		category_dir = os.path.join(args.data_dir, category)
		dst_dir = os.path.join(args.output_dir, category)

		if not os.path.exists(dst_dir):
		    os.mkdir(dst_dir)

		category_filenames = [os.path.join(category_dir, f) for f in os.listdir(category_dir)]
		dst_filenames = [os.path.join(dst_dir, f) for f in os.listdir(category_dir)]
		
		for category_filename, dst_filename in zip(category_filenames, dst_filenames):
			if os.path.exists(dst_filename):
				continue
			try:
				_, detections = detector.detectCustomObjectsFromImage(
					custom_objects=custom_objects,
					input_image=category_filename,
					output_type="array",
				)

				max_area = 448*448
				max_box_points = None 
				for detection in detections:
					box_points = detection['box_points']
					x1, y1, x2, y2 = box_points
					box_area = ((x2 - x1) * (y2 - y1))
					if box_area > max_area:
						max_area = box_area
						max_box_points = box_points

				if max_box_points is not None:
					x1, y1, x2, y2 = max_box_points
					
					pre, ext = os.path.splitext(category_filename)
					input_image = cv2.imread(category_filename)
					if input_image is None:
						continue
					height, width = input_image.shape[:2]

					x1, y1, x2, y2 = (
						x1 if x1 > 0 else 0,
						y1 if y1 > 0 else 0,
						x2 if x2 < width else width,
						y2 if y2 < height else height
					)
				
					if ext.lower() not in ['.jpg','.jpeg', '.png']:
						dpre, dext = os.path.splitext(dst_filename)
						dst_filename = dpre + '.jpg' 				

					crop_img = input_image[y1:y2, x1:x2]
					cv2.imwrite(dst_filename, crop_img)
				else:
					failed_filenames.append(category_filename)
			except:
				failed_filenames.append(category_filename)

