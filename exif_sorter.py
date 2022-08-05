# PLEASE USE THIS PROGRAM WITH CAUTION AS IT IS VERY UNTESTED


# The path of the location of pictures to process e.g. /home/user/Pictures/unsorted_pictures or C:\Users\SomeUser\Pictures\UnsortedPictures
pictures_path = ""

from PIL import Image, ExifTags
import os
import json

# Get a particular exif metadata attribute of an image
def get_exif_attribute(img, attribute):
    img_exif = img.getexif()
    if img_exif is None:
        return 'Unknown'
    else:
        for key,val in img_exif.items():
            if key in ExifTags.TAGS:
                if ExifTags.TAGS[key] == attribute:
                    return val
    return 'Unknown'

# Generates the model filepath dictionary: a dictionary of an array of image filepaths as values and camera model as keys 
def create_model_filepath_dictionary(pictures_path):
    model_filepath_dict = {}
    for image in os.listdir(pictures_path):
        image_path = os.path.join(pictures_path,image)
        if os.path.isfile(image_path):
            try:
                img = Image.open(image_path)
                model = get_exif_attribute(img, 'Model').strip()
                if model not in model_filepath_dict.keys():
                    model_filepath_dict[model] = []
                model_filepath_dict[model].append(image_path)
                
            except:
                continue

    return model_filepath_dict

# Create a folder for every key of the model filepath dictionary
def create_model_folders(model_filepath_dict, pictures_path):
    # Created in case a camera model name causes failure in creating folder
    error_count = 0
    for key in model_filepath_dict.copy().keys():
        key_path = os.path.join(pictures_path,key)
        if not os.path.isdir(key_path):
            try:
                os.mkdir(key_path)
            except:
                error_count += 1
                new_key_name = "ErrorCam" + str(error_count)
                model_filepath_dict[new_key_name] = model_filepath_dict.pop(key)
                key_path = os.path.join(pictures_path,new_key_name)
                os.mkdir(key_path)

# Move images into specific folder in accordance with the model filepath dictionary
def move_into_folders(model_filepath_dict, pictures_path):
    for key in model_filepath_dict.keys():
        key_path = os.path.join(pictures_path, key)
        for image_path in model_filepath_dict[key]:
            try:
                os.rename(image_path, os.path.join(key_path, os.path.basename(image_path)))
            except:
                if not os.path.isdir(os.path.join(pictures_path,'Errored_Files')):
                    os.mkdir(os.path.join(pictures_path,'Errored_Files'))
                os.rename(image_path, os.path.join(os.path.join(pictures_path, 'Errored_Files'), os.path.basename(image_path)))
                continue

model_filepath_dict = create_model_filepath_dictionary(pictures_path)
create_model_folders(model_filepath_dict,pictures_path)
move_into_folders(model_filepath_dict, pictures_path)
