from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator( rotation_range=20, width_shift_range=0.1, height_shift_range=0.1, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')