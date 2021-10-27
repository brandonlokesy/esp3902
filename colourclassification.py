import numpy as np
import pandas as pd
# import cv2
# import imutils
from PIL import ImageColor
# from scipy.spatial.distance import euclidean
# from scipy.spatial.distance import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
# from collections import OrderedDict 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

'''
Lego Colours are taken from here:
https://brickipedia.fandom.com/wiki/Medium_Blue'''

legoColoursHEX = {
    "brightRed" : "#DE000D", 
    "brightBlue" : "#0057A8", 
    # "darkGreen" : "#007B28",
    # "mediumBlue" : "#478CC6",
    "brightYellow" : "#FEC400"
    #"lightPurple" : "#E4ADC8",
    # "brightYellowishGreen" : "#95B90B",
    # "brightLightOrange" : "#F8BB3D",
    # "darkPurple" : "#2C1577",
    # "black" : "#010101",
    # "mediumAzure" : "#36AEBF"
                    }

# val is (coords, rail pos)
colourLocations = {"brightRed" : ((-350, 200, 50), 0),
                    "brightBlue" : ((-330, 100, 50), 0),
                    "brightYellow" : ((-200, 0, 50), 0)}

# legoColoursRGB = dict((k, ImageColor.getcolor(v, "RGB"))for k,v in legoColoursHEX.items())
legoColoursBGR = dict((k, ImageColor.getcolor(v, "RGB")[::-1])for k,v in legoColoursHEX.items())
df = pd.DataFrame([[k,v] for k,v in legoColoursBGR.items()], columns = ['colour','BGR'])
bgrArray = np.array([np.array(v) for v in legoColoursBGR.values()])

# inputHEX = '#50bafe'
# inputBGR = ImageColor.getcolor(inputHEX, "RGB")[::-1]

# dist = euclidean_distances(bgrArray, np.array([inputBGR]))
# idx = dist.argmin()
# print(f"the colour is {df.iloc[idx]['colour']}")

# df2 = pd.read_csv('./Color Data/colordata.csv')
df2 = pd.read_csv('./Colour Data/colourdata.csv')
df2[['r','g','b']]
KNN = KNeighborsClassifier(n_neighbors=2)
# scaler = StandardScaler()
X = df2[['r','g','b']]
y = df2[['Label']].values.ravel()
KNN.fit(X,y)

def get_colour(inputBGR):
    dist = euclidean_distances(bgrArray, np.array([inputBGR]))
    # print(df.iloc[dist.argmin()].colour)
    return df.iloc[dist.argmin()].colour

def get_colour_knn(inputBGR):
    rgb = np.array([inputBGR[::-1]])
    return KNN.predict(rgb)[0]

def colourBucket(colour):
    return colourLocations[colour]