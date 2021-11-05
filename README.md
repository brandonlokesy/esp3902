# ESP3902 Lego Colour Sorter

## Relevant Files

* `main.py` is the computer vision file that performs the image masking and contour detection.
* `arduino.py` interfaces serial with the Arduino Maker Uno
* `motor.ino` sets up the the connections between the Arduino Maker Uno and the Motor Shield
* `pydexarm.py` Is a file provided by Rotrics. We have modified the input data structure for the input coordinates to a tuple
* `coordinatestransform.py` maps pixels from the camera to real-world coordinates in the robot's base frame. This mapping is created experimentally through the use of an optical breadboard to obtain fixed distances between measurement points.
* `colourclassification.py` classifies the the input colour based on a dictionary of known Lego colours. The `get_colour_svm()` function uses a support vector machine algorithm to classify the input RGB values into one of the colours in the database.
* `legobrick.py` forms the data structure to store the Lego brick's last known position.

## Other Files

Most of the other files here were used for testing purposes. They are not required to operate the system

* `contour-threshold.py` was used to determine the threshold values to use to detect contours on the input image.
* `colour-testing.py` was used to experiment the HSV masking of an input image.
* `calibration.py` was used to map pixels on the camera to real-world coordinates.

## Hardware Specifications
