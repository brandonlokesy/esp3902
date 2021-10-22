import numpy as np

pixel2cm_x = 2.524705882

def y_mm(p):
	# return 0.3953*p + 88.144 ##old
	return 0.3977*p + 91.446

def x_mm(p):
	# temp = 1258-p + 10
	temp = 1258-p #old
	# temp = 1219-p
	# return temp/pixel2cm_x
	# return (temp / pixel2cm_x) + 10
	return (temp / pixel2cm_x) + 7

#for x y = -2.7077*p + 1217.4