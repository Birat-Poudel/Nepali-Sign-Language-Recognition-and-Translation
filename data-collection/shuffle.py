import os
import random

base_folder = "data"

# Names of the train and test folders
train_folder = "train"
test_folder = "test"

subfolders = ["0","1","2","A", "B", "C", "D", "E","G","H","I"]

for folder_name in [train_folder, test_folder]:
    folder = os.path.join(base_folder, folder_name)
    
    for subfolder in subfolders:
        subfolder_path = os.path.join(folder, subfolder)
        images = [f for f in os.listdir(subfolder_path) if f.endswith(".jpg")]

        random.shuffle(images)

        for i, image in enumerate(images):
            os.rename(os.path.join(subfolder_path, image), os.path.join(subfolder_path, f"{i + 1}_{image}"))