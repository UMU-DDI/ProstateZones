import pandas as pd
import random
import numpy as np
import os
import re
import shutil

os.environ['PYTHONHASHSEED'] = str(2023)


def copy_image(src, dst):

    if not os.path.exists(dst):
        shutil.copytree(src, dst)

def copy_segmentation(src, dst):

    if not os.path.exists(dst):
        shutil.copyfile(src, dst)

'''
This file will take the downloaded PROSTATEx dataset + segmentations and structure them in folders.
'''


# Path to the fodler containing the downloaded PROSTATEx dataset.
path_to_ProstateX_data = r'...\PROSTATEx'

# Path to the folder containing the downloaded segmentations.
path_to_segmentations = r'...\ProstateSegmentations'

# Path to the folder where we want to save the structured data.
output_path = r'__Desired_Output_Directory__'



# Create list with samples and duplicates.
samples = []
duplicates = []

with open('_samples_.txt', "r") as lst_samples:
    for s in lst_samples:
        samples.append('ProstateX-' + s.replace("\n", ""))

with open('_duplicates_.txt', "r") as lst_duplicates:
    for d in lst_duplicates:
        duplicates.append('ProstateX-' + d.replace("\n", ""))



# Defining the DataFrame with the names of relevant images we will use.
df = pd.DataFrame(columns = ['PatientID', 'T2_Ax', 'T2_Sag', 'T2_Cor', 'DWI', 'ADC', 'HBV'])

with open('list_of_PROSTATEx_files.txt', 'r') as _file_:
    for line in _file_:
        data = line.strip().split(':')

        df.loc[len(df)] = data

############################################
# COPY TO OUTPUT FOLDER
############################################

# Extracting our selected samples from the dataset.
df_ProstateX = df[df['PatientID'].isin(samples)]


# Copy our selected files to our output folder.

for patient_folder in list(df_ProstateX['PatientID']):
    
    row = df_ProstateX.loc[df_ProstateX['PatientID'] == patient_folder].reset_index()

    numbers = ''.join([n for n in patient_folder if n.isdigit()])


    for path_Folder, folders, files in os.walk(os.path.join(path_to_ProstateX_data, patient_folder)):
            
            
        if re.search(row['T2_Ax'][0], path_Folder) and row['T2_Ax'][0] != '':

            copy_image(path_Folder,
                       os.path.join(output_path, 'Images', patient_folder, 'tra-' + numbers))
            
            continue

        if re.search(row['T2_Sag'][0], path_Folder) and row['T2_Sag'][0] != '':

            copy_image(path_Folder,
                       os.path.join(output_path, 'Images', patient_folder, 'sag-' + numbers))

            continue
        
        if re.search(row['T2_Cor'][0], path_Folder) and row['T2_Cor'][0] != '':

            copy_image(path_Folder,
                       os.path.join(output_path, 'Images', patient_folder, 'cor-' + numbers))

            continue

        if re.search(row['DWI'][0], path_Folder) and row['DWI'][0] != '':

            copy_image(path_Folder,
                       os.path.join(output_path, 'Images', patient_folder, 'dwi-' + numbers))

            continue

        if re.search(row['ADC'][0], path_Folder) and row['ADC'][0] != '':

            copy_image(path_Folder,
                       os.path.join(output_path, 'Images', patient_folder, 'adc-' + numbers))

            continue

        if re.search(row['HBV'][0], path_Folder) and row['HBV'][0] != '':

            copy_image(path_Folder,
                       os.path.join(output_path, 'Images', patient_folder, 'hbv-' + numbers))

            continue


############################################
# ORGANIZE INTO TRAIN / VALIDATE / TEST
############################################

random.seed(2023)

train = random.sample([sample for sample in samples if sample not in duplicates], 120)
train.sort()

validate = list(set(samples) - set(train) - set(duplicates))
validate.sort()


for sample in samples:

    if sample in train:
        fld = 'Train'
    elif sample in validate:
        fld = 'Validate'
    elif sample in duplicates:
        fld = 'Test'
    else:
        continue

    dst = os.path.join(output_path, fld, sample)

    numbers = ''.join([n for n in sample if n.isdigit()])

    # Copy the images
    for img in ['tra-', 'adc-', 'hbv-']:
        copy_image(os.path.join(output_path, 'Images', sample, img + numbers),
                   os.path.join(dst, img + numbers))

    # Copy segmentations
    if ('Train' in dst) or ('Validate' in dst):
        # Singles from training & validating.
        copy_segmentation(os.path.join(path_to_segmentations, 'Singles', 'Seg-' + numbers + '.nrrd'),
                   os.path.join(dst, 'Seg-' + numbers + '.nrrd'))

    elif 'Test' in dst:
        # Duplicates for testing.
        for r in ['R1', 'R2']:
            copy_segmentation(os.path.join(path_to_segmentations, 'Duplicates', r, 'Seg-' + numbers + '_' + r + '.nrrd'),
                       os.path.join(dst, 'Seg-' + numbers + '_' + r + '.nrrd'))