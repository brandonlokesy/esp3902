import numpy as np

pixel2cm_x = 2.524705882

def y_mm(p):
	return 0.3953*p + 88.144

def x_mm(p):
	# temp = 1258-p + 10
	temp = 1258-p
	# return temp/pixel2cm_x
	return (temp / pixel2cm_x) + 10