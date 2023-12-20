import os
import cv2
import random
import numpy as np

def augment_images(folder_path, num_augmentations=5):
   # Get the list of image files in the folder
   image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

   for image_file in image_files:
       # Read the image
       image_path = os.path.join(folder_path, image_file)
       image = cv2.imread(image_path)

       # Apply augmentations
       for i in range(num_augmentations):
           # Apply slight zoom
           zoomed_image = cv2.resize(image, None, fx=1.1, fy=1.1)

           # Apply slight blur
           blurred_image = cv2.GaussianBlur(zoomed_image, (5, 5), 0)

           # Adjust contrast
           contrast_adjusted_image = cv2.convertScaleAbs(blurred_image, alpha=1.2, beta=0)

           # Rotate image randomly between -10 to 10 degrees
           angle = random.randint(-3, 3)
           rows, cols = contrast_adjusted_image.shape[:2]
           M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
           rotated_image = cv2.warpAffine(contrast_adjusted_image, M, (cols, rows))

           # Random crop
           crop_width = random.randint(620, 640)
           crop_height = random.randint(460, 480)
           h, w = rotated_image.shape[:2]
           if h > crop_height and w > crop_width:
             x = random.randint(0, h - crop_height)
             y = random.randint(0, w - crop_width)
             cropped_image = rotated_image[x:x+crop_height, y:y+crop_width]
           else:
             cropped_image = rotated_image

           # Flip horizontally
           flipped_image = cv2.flip(cropped_image, 1)

           # Add random noise
           noise = np.random.normal(0, 0.2, flipped_image.shape).astype(np.uint8)
           noisy_image = cv2.add(flipped_image, noise)

           # Save the augmented image with a suffix added to the filename
           augmented_image_file = os.path.splitext(image_file)[0] + f'_augmented_{i+1}' + os.path.splitext(image_file)[1]
           augmented_image_path = os.path.join(folder_path, augmented_image_file)
           cv2.imwrite(augmented_image_path, noisy_image)

           print(f"Augmented image saved: {augmented_image_path}")

   print("Augmentation complete.")

# Provide the folder path where the images are located
folder_path = './01_base_images'

# Call the function to augment the images (5 augmentations per image)
augment_images(folder_path, num_augmentations=5)