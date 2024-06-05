import os
import cv2
import random

# Define directories
train_directory = "data/train"
test_directory = "data/test"

# Create base directories if they do not exist
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(train_directory):
    os.makedirs(train_directory)
if not os.path.exists(test_directory):
    os.makedirs(test_directory)

# Define character lists
nepali_characters = [
    'क', 'ख', 'ग', 'घ', 'ङ',
    'च', 'छ', 'ज', 'झ', 'ञ',
    'ट', 'ठ', 'ड', 'ढ', 'ण',
    'त', 'थ', 'द', 'ध', 'न',
    'प', 'फ', 'ब', 'भ', 'म',
    'य', 'र', 'ल', 'व', 'श',
    'ष', 'स', 'ह', 'क्ष', 'त्र', 'ज्ञ']

characters = [
    '0', '1', '2', '3', '4', 
    '5', '6', '7', '8', '9', 
    'A', 'B', 'C', 'D', 'E', 
    'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 
    'P', 'Q', 'R', 'S', 'T', 
    'U', 'V', 'W', 'X', 'Y', 'Z']

# Create sub-folders for each character in train and test directories
for char in characters:
    os.makedirs(f"{train_directory}/{char}", exist_ok=True)
    os.makedirs(f"{test_directory}/{char}", exist_ok=True)

# Initialize camera
cap = cv2.VideoCapture(0)

min_value = 70
num_images_to_capture = 10
image_count = 0
capture_images = False
capture_char = ''

# Initialize count dictionaries
train_chars_count = {char: len(os.listdir(f"{train_directory}/{char}")) for char in characters}
test_chars_count = {char: len(os.listdir(f"{test_directory}/{char}")) for char in characters}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    cv2.rectangle(frame, (269, 9), (621, 355), (265, 0, 0), 1)
    cv2.imshow("Frame", frame)

    roi = frame[50:350, 270:570]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)
    blur = cv2.bilateralFilter(blur, 3, 75, 75)
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    _, roi = cv2.threshold(th3, min_value, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    cv2.imshow("ROI", roi)

    interrupt = cv2.waitKey(10)

    if interrupt & 0xFF == 27:  # ESC key
        break

    if not capture_images:
        for char in characters:
            if interrupt & 0xFF == ord(char.lower()):
                capture_images = True
                capture_char = char
                image_count = 0
                break
    else:
        # Determine if the image should go to train or test directory (30% test, 70% train)
        if random.random() < 0.3:  # 30% chance
            directory_to_save = test_directory
        else:
            directory_to_save = train_directory

        if directory_to_save == test_directory:
            file_path = f"{directory_to_save}/{capture_char}/{test_chars_count[capture_char]}.jpg"
            test_chars_count[capture_char] += 1
        else:
            file_path = f"{directory_to_save}/{capture_char}/{train_chars_count[capture_char]}.jpg"
            train_chars_count[capture_char] += 1

        cv2.imwrite(file_path, roi)

        image_count += 1
        if image_count >= num_images_to_capture:
            capture_images = False
            break  # Exit the loop after capturing the desired number of images

cap.release()
cv2.destroyAllWindows()