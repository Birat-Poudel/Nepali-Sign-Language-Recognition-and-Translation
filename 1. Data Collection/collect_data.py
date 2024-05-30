import os
import cv2

train_directory = "data/train"
test_directory = "data/test"

# Creating data/train and data/test directories
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(train_directory):
    os.makedirs(train_directory)
if not os.path.exists(test_directory):
    os.makedirs(test_directory)
   
# Creating sub-folders in data/train and data/test for "nepali characters" list 
# as "characters" list for simplicity
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
   
for char in characters:
    if not os.path.exists(f"{train_directory}/{char}"):
        os.makedirs(f"{train_directory}/{char}")
    if not os.path.exists(f"{test_directory}/{char}"):
        os.makedirs(f"{test_directory}/{char}")
    
min_value = 70
cap = cv2.VideoCapture(0)
interrupt = -1
flag = True

# Initialize count dictionaries
train_chars_count = {char: len(os.listdir(f"{train_directory}/{char}")) for char in characters}
test_chars_count = {char: len(os.listdir(f"{test_directory}/{char}")) for char in characters}

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    cv2.rectangle(frame, (269, 9), (621, 355), (265, 0, 0), 1)
    cv2.imshow("Frame", frame)

    roi = frame[50:350, 270:570]
    cv2.imshow("ROI", roi)

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)
    blur = cv2.bilateralFilter(blur, 3, 75, 75)
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    _, roi = cv2.threshold(th3, min_value, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    cv2.imshow("ROI", roi)
    
    interrupt = cv2.waitKey(10)
    
    if interrupt & 0xFF == 27:  # ESC key
        break

    #Check for keypresses corresponding to the characters
    for char in characters:
        if interrupt & 0xFF == ord(char.lower()):
            directory_to_save = test_directory if train_chars_count[char] % 3 == 0 and flag else train_directory
            file_path = f"{directory_to_save}/{char}/{test_chars_count[char] if directory_to_save == test_directory else train_chars_count[char]}.jpg"
            cv2.imwrite(file_path, roi)
            
            if directory_to_save == test_directory:
                test_chars_count[char] += 1
            else:
                train_chars_count[char] += 1
                
            flag = not flag
            
cap.release()
cv2.destroyAllWindows()