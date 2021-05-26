import os
import numpy as np
import time
import itertools
from PIL import Image
from tqdm import tqdm
import argparse
import pdb
import skimage.measure
import cv2

parser = argparse.ArgumentParser(description='find-duplicate-images')
parser.add_argument('--inspection_folder', type=str, default="D:\\Pictures\\Inspection", help='Directory of videos.')
args = parser.parse_args()

inspection_folder = args.inspection_folder
print("Inspection folder: " + str(inspection_folder))

folders = [x[0] for x in os.walk(inspection_folder)]

COMPARE_SIZE = 300

to_delete = []

sleep_time = 0.1

def check_folder(folder):
	print("Checking Folder -> " + folder)
	files = os.listdir(folder)
	files.sort()
	files_lower = [f.lower() for f in files]
	m = len(files)
	# pdb.set_trace()

	images = []
	images_name = []
	frames_count = []
	time.sleep(sleep_time)
	for i in tqdm(range(m)):
		if 'mov' in files_lower[i] or 'mp4' in files_lower[i]:
			try:
				vidcap = cv2.VideoCapture(os.path.join(folder, files[i]))
				success, img = vidcap.read()

				if img is not None:
					length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
					img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					img = Image.fromarray(img).convert('L')

					img = img.resize((COMPARE_SIZE, COMPARE_SIZE))
					img = np.array(img)

					img = skimage.measure.block_reduce(img, (2, 2), func=np.mean)
					img = skimage.measure.block_reduce(img, (2, 2), func=np.mean)
					img = skimage.measure.block_reduce(img, (2, 2), func=np.mean)

					images.append(img)
					images_name.append(files[i])
					frames_count.append(length)
			except Exception as e: 
				print(files[i], e)
				pass
	time.sleep(sleep_time)

	images = np.array(images)
	frames_count = np.array(frames_count)
	m = images.shape[0]
	print("Videos Read. Total videos found = " + str(m))

	if m < 2:
		print()
		return

	print("Finding duplicates now...")
	im_duplicates = []
	for i in tqdm(range(m)):
		img_match = np.all(images == images[i], axis=(1, 2))
		frames_count_match = frames_count == frames_count[i]
		duplicates = np.logical_and(frames_count_match, img_match)
		duplicates[i] = False
		idx = np.where(duplicates)[0]
		if idx.size > 0:
			im_duplicate = list()
			im_duplicate.append(i)
			for j in range(idx.shape[0]):
				im_duplicate.append(idx[j])
			im_duplicate.sort()
			im_duplicates.append(im_duplicate)
	time.sleep(sleep_time)

	im_duplicates.sort()
	im_duplicates = list(im_duplicates for im_duplicates, _ in itertools.groupby(im_duplicates))

	if len(im_duplicates) > 0:
		print()
		print("Duplicates:")
		for i in range(len(im_duplicates)):
			for j in range(len(im_duplicates[i])):
				print(images_name[im_duplicates[i][j]], end="\t")
				if j > 0:
					to_delete.append(os.path.join(folder, images_name[im_duplicates[i][j]]))
			print()
	else:
		print("No duplicates found.")
	print()


for folder in folders:
	check_folder(folder)

print('-----------------------------Overall Report----------------------------------')

if len(to_delete) == 0:
	print("No duplicates found.")
	exit()

print("\nFiles marked for delete:")
for file in to_delete:
	print(file)
print("Print Y to delete")
inp = input()
if inp == 'Y':
	for file in to_delete:
		os.remove(file)
	print("Done.")
else:
	print("Files not deleted.")
