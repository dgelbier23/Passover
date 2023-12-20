from ultralytics import YOLO
from PIL import Image

# Establish model
model_yolo = YOLO("Machine Learning\\runs\\detect\\train7\\weights\\best.pt")

# Get testing data
im1 = Image.open("Machine Learning\\data\\images\\test\\image15.jpeg")
# vid2 = 'Machine Learning\\Model\\data\\images\\test\\Video_1.mov'
# vid1 = 'Machine Learning\\Model\\data\\images\\test\\Video_2.mov'

# Run tests
results = model_yolo.predict(source=im1, save=True,save_txt=True, project="Machine Learning\\runs\\detect")  # save plotted images
