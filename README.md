# ESP3902 Lego Colour Sorter

## Relevant Files
*<code>main.py</code> is the computer vision file that performs the image masking and contour detection.
* <code>arduino.py</code> interfaces serial with the Arduino Maker Uno
* <code>esp3902_motor.ino</code> sets up the the connections between the Arduino Maker Uno and the Motor Shield
* <code>pydexarm.py</code> Is a file provided by Rotrics. We have modified the input data structure for the input coordinates to a tuple
* <code>coordinatestransform.py</code> maps pixels from the camera to real-world coordinates in the robot's base frame. This mapping is created experimentally through the use of an optical breadboard to obtain fixed distances between measurement points. 
* <code>colourclassification.py</code> classifies the the input colour based on a dictionary of known Lego colours. The <code>get_colour()</code> function calculates the Euclidean distance between the input colour and the known colours and returns the colour that minimises this distance.
* </code>legobrick.py</code> forms the data structure to store the Lego brick's last known position.

## Other Files
Most of the other files here were used for testing purposes. They are not required to operate the system
* <code>contour-threshold.py</code> was used to determine the threshold values to use to detect contours on the input image.
*<code>colour-testing.py</code> was used to experiment the HSV masking of an input image.
*<code>calibration.py</code> was used to map pixels on the camera to real-world coordinates.