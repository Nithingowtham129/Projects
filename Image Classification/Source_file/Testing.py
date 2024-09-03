
from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image

json_file = open('C:/Users/NITHIN GOWTHAM/Documents/java opp/Python/image classification - dataset/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("C:/Users/NITHIN GOWTHAM/Documents/java opp/Python/image classification - dataset/model.h5")
print("Loaded model from disc")

def classify(img_file, label):
    img_name = img_file
    labels = label
    test_image = image.load_img(img_name, target_size= (64,64))

    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)

    if result[0][0] == 1:
        prediction = 'Steve Jobs'
    else:
        prediction = 'Elon Musk'
    print("Predicted : ", prediction ," <===> ", labels)

import os
path = "C:/Users/NITHIN GOWTHAM/Documents/java opp/Python/image classification - dataset/Test_data"
files = []
label = []

# r = root , d = directory, f = files
for r, d, f in os.walk(path):
    for file in f:
        files.append(os.path.join(r, file))
        label.append(file)
i=0
for f in files:
    classify(f,label[i])
    i+=1;
    print("------------------------------------------------------------------------")