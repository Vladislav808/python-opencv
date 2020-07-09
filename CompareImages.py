import tkinter as tk
from simpletk import *
import cv2
from PIL import Image, ImageChops


def main():
	"""Create a main window with all widgets"""
	global app, label1, label2, label3, buttn, buttn2, buttn3, memo, lineEdit1, lineEdit2, chbox, chbox2
	app = TApplication('')
	app.title = 'Image Comparison v1.0.0'
	app.background = '#B0C4DE'
	app.size = (1200, 600)
	app.position = (100, 100)
	
	#Create Labels
	x_pos = 40
	y_pos = 40
	label1 = TLabel(app)
	label1.position = (x_pos, y_pos)
	label1.size = (150, 20)
	label1.text = 'Catalog for first image'
	label1.color = '#4B0082'
	label1.background = '#B0C4DE'

	label2 = TLabel(app)
	label2.position = (x_pos, y_pos + 40)
	label2.size = (150, 20)
	label2.text = 'Catalog for seconf image'
	label2.color = '#4B0082'
	label2.background = '#B0C4DE'	

	#Create button
	buttn = TButton(app, height = 20, width = 60)
	buttn.background = 'white'
	buttn.position = (40, 120)
	buttn.text = 'Load'

	buttn2 = TButton(app, height = 20, width = 60)
	buttn2.background = 'white'
	buttn2.position = (200, 110)
	buttn2.text = 'Clear'

	buttn3 = TButton(app, height = 20, width = 60)
	buttn3.background = 'white'
	buttn3.position = (40, 160)
	buttn3.text = 'Compare'
	#Create Memos
	memo = TMemo(app, height = 70, width = 360, bg = "white", fg = '#556B2F', wrap = "word")
	memo.position = (40, 200)
	memo.font = ('Times New Roman', 12)

	#Create Edits
	lineEdit1 = TEdit(app, height = 20, width = 200)
	lineEdit1.position = (200, 40)
	lineEdit1.background = 'white'

	lineEdit2 = TEdit(app, height = 20, width = 200)
	lineEdit2.position = (200, 80)
	lineEdit2.background = 'white'

	#Create CheckBox
	chbox = TCheckBox(app)
	chbox.text = 'Open files in a separate window'
	chbox.position = (180, 160)
	chbox.background = '#B0C4DE'

	chbox2 = TCheckBox(app)
	chbox2.text = 'Show difference in one image'
	chbox2.position = (180, 140)
	chbox2.background = '#B0C4DE'


def insert(event):
	"""Download and compare images. Compare using the PIL and OpenCV libraries by hash calculation"""
	global way1, way2, image1, image2, loadim1, loadim2, dif, im1, im2
	global threshold1, threshold2, threshold_median1, threshold_median2, threshold_gauss1, threshold_gauss2
	way1 = lineEdit1.text
	way2 = lineEdit2.text
	# PIL
	im1 = Image.open(way1)
	im2 = Image.open(way2)
	# Returns the absolute value of the pixel difference between two images.
	# Determine the similarity of images using the internal method 
	dif = ImageChops.difference(im1, im2) 

	# We read images, resized and turn into a gray tint
	image1 = cv2.imread(way1)
	image2 = cv2.imread(way2)
	resized1 = cv2.resize(image1, (8, 8), interpolation = cv2.INTER_AREA)
	resized2 = cv2.resize(image2, (8, 8), interpolation = cv2.INTER_AREA)
	gray1 = cv2.cvtColor(resized1, cv2.COLOR_BGR2GRAY)
	gray2 = cv2.cvtColor(resized2, cv2.COLOR_BGR2GRAY)
	# Threshold binarization
	avg1 = gray1.mean() # threshold value - average value for each pixel
	ret, threshold1 = cv2.threshold(gray1, avg1, 255, cv2.THRESH_BINARY)
	avg2 = gray2.mean()
	ret, threshold2 = cv2.threshold(gray2, avg2, 255, cv2.THRESH_BINARY)
	#------------------------------
	# Adaptive Median Threshold
	threshold_median1 = cv2.adaptiveThreshold(gray1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
	threshold_median2 = cv2.adaptiveThreshold(gray2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
	#------------------------------
	# Adaptive Gaussian Threshold
	threshold_gauss1 = cv2.adaptiveThreshold(gray1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	threshold_gauss2 = cv2.adaptiveThreshold(gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	#------------------------------
	
	# Face recognition
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	
	gray_face1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) # 1 image
	gray_face2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY) # 2 image
	faces1 = face_cascade.detectMultiScale(gray_face1, 1.3, 5)
	faces2 = face_cascade.detectMultiScale(gray_face2, 1.3, 5)
	# Draw squares around faces
	for (x, y, w, h) in faces1:
		image1 = cv2.rectangle(image1, (x, y), (x + w, y + h), (255, 255, 0), 2)
	for (x, y, w, h) in faces2:
		image2 = cv2.rectangle(image2, (x, y), (x + w, y + h), (255, 255, 0), 2)
	
	cv2.imshow('Image1', image1)
	cv2.imshow('Image2', image2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	# Creating windows for loading images
	loadim1 = TImage(app, height = 580, width = 380)
	loadim1.position = (410, 10)
	loadim1.picture = way1
	loadim1.center = True
	loadim2 = TImage(app, height = 580, width = 380)
	loadim2.position = (800, 10)
	loadim2.picture = way2
	loadim2.center = True
	lineEdit1.background = 'green'
	lineEdit2.background = 'green'

	if chbox.checked == True:
		cv2.imshow(str(way1), image1)
		cv2.imshow(str(way2), image2)
		cv2.waitKey(0)
	else:
		pass

	if chbox2.checked == True:
		dif.show()
	else:
		pass


def calc_hash(event):
	"""Сount each hash and compare values"""
	global hash_avg1, hash_avg2, hash_median1, hash_median2
	global hash_gauss1, hash_gauss2
	global dist_avg, dist_m, dist_g
	
	hash_avg1, hash_avg2 = [], []
	hash_median1, hash_median2 = [], []
	hash_gauss1, hash_gauss2 = [], []
	
	# We calculate the hash for the mean value
	for x in range(8):
		for y in range(8):
			val_avg1 = threshold1[x, y]
			if val_avg1 == 255:
				hash_avg1.append(1)
			else:
				hash_avg1.append(0)
	for x in range(8):
		for y in range(8):
			val_avg2 = threshold2[x, y]
			if val_avg2 == 255:
				hash_avg2.append(1)
			else:
				hash_avg2.append(0)
	# We calculate the hash for adapt.median. threshold value
	for x in range(8):
		for y in range(8):
			val_med1 = threshold_median1[x, y]
			if val_med1 == 255:
				hash_median1.append(1)
			else:
				hash_median1.append(0)
	for x in range(8):
		for y in range(8):
			val_med2 = threshold_median2[x, y]
			if val_med2 == 255:
				hash_median2.append(1)
			else:
				hash_median2.append(0)
	# Calculate the hash for adapt.Gauss. threshold value
	for x in range(8):
		for y in range(8):
			val_g1 = threshold_gauss1[x, y]
			if val_g1 == 255:
				hash_gauss1.append(1)
			else:
				hash_gauss1.append(0)
	for x in range(8):
		for y in range(8):
			val_g2 = threshold_gauss2[x, y]
			if val_g2 == 255:
				hash_gauss2.append(1)
			else:
				hash_gauss2.append(0)
	# CALCULATE HAMMING DISTANCE
	# Average threshold value
	i = 0 
	dist_avg = 0
	while i < len(hash_avg1):
		dist_avg = dist_avg + abs(hash_avg1[i] - hash_avg2[i])
		i += 1

	# Adapt.median. threshold. value
	j = 0
	dist_m = 0
	while j < len(hash_median1):
		dist_m = dist_m + abs(hash_median1[j] - hash_median2[j])
		j += 1

	# Adapt. gauss. threshold. value
	z = 0
	dist_g = 0
	while z < len(hash_gauss1):
		dist_g = dist_g + abs(hash_gauss1[z] - hash_gauss2[z])
		z += 1

	minimum = min(dist_avg, dist_m, dist_g)
	if 0 <= dist_avg <= 8 or 0 <= dist_m <= 8 or 0 <= dist_g <= 8:
		memo.insert(INSERT, 100 - minimum * 2.4)
		memo.insert(INSERT, '%')
	elif 9 <= dist_avg <= 13 or 9 <= dist_m <= 13 or 9 <= dist_g <= 13:
		memo.insert(INSERT, 100 - minimum * 3.25)
		memo.insert(INSERT, '%')
	elif 14 <= dist_avg <= 18 or 14 <= dist_m <= 18 or 14 <= dist_g <= 18:
		memo.insert(INSERT, 100 - minimum * 3.5)
		memo.insert(INSERT, '%')
	elif 19 <= dist_avg <= 20 or 19 <= dist_m <= 20 or 19 <= dist_g <= 20:
		memo.insert(INSERT, 100 - minimum * 3.8)
		memo.insert(INSERT, '%')
	elif  dist_avg > 21 or  dist_m > 21 or  dist_g > 21:
		memo.insert(INSERT, 0)
		memo.insert(INSERT, '%')
	memo.insertLine(1, str(im1)[64:73])
	memo.insertLine(2, str(im2)[64:73])


def delet_text(event):
	"""Clears input fields"""
	lineEdit1.text, lineEdit2.text = ('', '')
	lineEdit1.background = 'white'
	lineEdit2.background = 'white'
	way1, way2 = ('', '')
	

main()
buttn.onClick = insert 
buttn2.onClick = delet_text
buttn3.onClick = calc_hash
app.run()