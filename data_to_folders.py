import pandas as pd
import random
import numpy as np
import os
import re
import shutil
import argparse

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

# ['T2_Ax','T2_Sag','T2_Cor','DWI','ADC','HBV']

parser = argparse.ArgumentParser()
parser.add_argument('--images', type=str, default=[], nargs='+', help='Additional image sequences you want to include. Options are: T2_Sag, T2_Cor, DWI, ADC, and HBV.')
parser.add_argument('--image_folder', type=str, default='C:\William\Doktorand\Data\ProstateX - Images\PROSTATEx', help='Path to the folder containing the images.')
parser.add_argument('--segmentation_folder', type=str, default='C:\William\Doktorand\Data\ProstateX - Segmentations', help='Path to the folder containing the segmentations.')
parser.add_argument('--output_folder', type=str, default='output', help='Path to the desired output folder.')
args = parser.parse_args()

# List of image sequences that should be included
image_sequences = args.images
image_sequences.insert(0, 'T2_Ax')

# Path to the fodler containing the downloaded PROSTATEx dataset.
path_to_ProstateX_data = args.image_folder

# Path to the folder containing the downloaded segmentations.
path_to_segmentations = args.segmentation_folder

# Path to the folder where we want to save the structured data.
output_path = args.output_folder

# Access support txt-files
base = os.getcwd()
support_files = os.path.join(base, 'Support Files')


# Create list with samples and duplicates.
samples = []
duplicates = []

with open(os.path.join(support_files, '_samples_.txt'), "r") as lst_samples:
    for s in lst_samples:
        samples.append('ProstateX-' + s.replace("\n", ""))

with open(os.path.join(support_files, '_duplicates_.txt'), "r") as lst_duplicates:
    for d in lst_duplicates:
        duplicates.append('ProstateX-' + d.replace("\n", ""))



# Defining the DataFrame with the names of relevant images we will use.
df = pd.DataFrame(columns = ['PatientID', 'T2_Ax', 'T2_Sag', 'T2_Cor', 'DWI', 'ADC', 'HBV'])

with open(os.path.join(support_files,'list_of_PROSTATEx_files.txt'), 'r') as _file_:
    for line in _file_:
        data = line.strip().split(':')

        df.loc[len(df)] = data

image_sequences.insert(0, 'PatientID')

# Extracting our selected samples from the dataset.
df_sequences = df.filter(items=image_sequences)
df_ProstateX = df_sequences[df_sequences['PatientID'].isin(samples)]

############################################
# COPY TO OUTPUT FOLDER
############################################

mapping = {'T2_Ax': 'tra-', 'T2_Sag': 'sag-', 'T2_Cor': 'cor-', 'DWI': 'dwi-', 'ADC': 'adc-', 'HBV': 'hbv-'}

for patient_folder in list(df_ProstateX['PatientID']):
    
    row = df_ProstateX.loc[df_ProstateX['PatientID'] == patient_folder].reset_index()

    numbers = ''.join([n for n in patient_folder if n.isdigit()])


    for path_Folder, folders, files in os.walk(os.path.join(path_to_ProstateX_data, patient_folder)):

        for sequence in image_sequences[1:]:

            if re.search(row[sequence][0], path_Folder) and row[sequence][0] != '':

                copy_image(path_Folder, os.path.join(output_path, 'Images', patient_folder, mapping[sequence] + numbers))


############################################
# ORGANIZE INTO TRAIN / VALIDATE / TEST
############################################

random.seed(2023)

train = random.sample([sample for sample in samples if sample not in duplicates], 120)
train.sort()

validate = list(set(samples) - set(train) - set(duplicates))
validate.sort()

# Remove T2_Sag and T2_Cor if they are part of the image sequences, as we only want image in the same orientation as the segmentations in the Train/Validate/Test setup.
updated_image_sequences = [seq for seq in image_sequences if seq not in ['PatientID','T2_Sag', 'T2_Cor']]

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
    for sequence in updated_image_sequences:
        copy_image(os.path.join(output_path, 'Images', sample, mapping[sequence] + numbers), os.path.join(dst, mapping[sequence] + numbers))

    # Copy segmentations
    if ('Train' in dst) or ('Validate' in dst):
        # Singles from training & validating.
        copy_segmentation(os.path.join(path_to_segmentations, 'Singles', 'Seg-' + numbers + '.nrrd'), os.path.join(dst, 'Seg-' + numbers + '.nrrd'))

    elif 'Test' in dst:
        # Duplicates for testing.
        for r in ['R1', 'R2']:
            copy_segmentation(os.path.join(path_to_segmentations, 'Duplicates', r, 'Seg-' + numbers + '_' + r + '.nrrd'), os.path.join(dst, 'Seg-' + numbers + '_' + r + '.nrrd'))