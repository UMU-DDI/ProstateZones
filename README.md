# ProstateZones

This repository contains files to organize the data and ease the use of the ProstateZones dataset.
The ProstateZones dataset is a collection of segmentations of the prostatic zones and urethra delineated on publicly available images from the PROSTATEx dataset. The dataset is intended for research purposes in the field of medical imaging, particularly focusing on automatic segmentations of the prostate, prostatic zones, and urethra.


## Usage
The files in this repository are structured to facilitate organization and utilization of the ProstateZones dataset.

### Download
To start, download the images and segmentations.

#### Images
The images can be downloaded from the Cancer Imaging Archive (TCIA) at the following link: https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=23691656
#### Segmentations
The segmentations are available on Zenodo, accessible through the DOI: 10.5281/zenodo.10718469

### Structure Data
To pair the images and segmentations, and divide into Train/Validate/Test folders, run the followig lines of code:

```ruby
pip install > requirements.txt
```

```ruby
python data_to_folders.py --image_folder 'path/to/PROSTATEx_image_folder' --segmentation_folder 'path/to/PorstateZones_segmentation_folder' --output_folder 'path/to/output_folder' --images T2_Sag T2_Cor DWI ADC HBV
```
The above lines of code will extract the Axial T2 weigthed image that was used for the manual delineations from the PROSTATEx data and copy it to a new folder. If any additional sequences are of interest, they can be added through the `--image`-flag.
Images will be renamed into a more straightforward structure, while still keeping the 4-digit patient specifier as in the original PROSTATEx naming convention:

- tra : Axial T2w
- sag : Sagittal T2w
- cor : Coronal T2w
- dwi : Diffusion Weighted image
- adc : Apparent Diffusion Coefficient
- hbv : High B-value image

#### Folder Structure:

After running the above lines of code the data will have the following structure in the output folder.

- **Images**
  - ProstateX-0000
    - _adc-0000_
    - _cor-0000_
    - _dwi-0000_
    - _hbv-0000_
    - _sag-0000_
    - tra-0000
  - ProstateX-0007
  - ...

- **Train**
  - ProstateX-0000
    - _adc-0000_
    - _hbv-0000_
    - tra-0000
    - Seg-0000.nrrd
  - ProstateX-0008
  - ...

- **Validate**
  - ProstateX-0007
    - _adc-0007_
    - _hbv-0007_
    - tra-0007
    - Seg-0007.nrrd
  - ProstateX-0010
  - ...

- **Test**
  - ProstateX-0015
    - _adc-0015_
    - _hbv-0015_
    - tra-0015
    - Seg-0015_R1.nrrd
    - Seg-0015_R2.nrrd
  - ProstateX-0019
  - ...
 
**Note:** _italic_ images are optional in each folder depending on the inputs to the `--image`-flag, although Sagittal and Coronal images will not be included in the Train/Validate/Test folders, which (without modification) only include images with the same orientation as the segmentations.


### Evaluation Workflow
The evaluation workflow used to analyze the inter-reader variability data is included in this repository.
To run the evaluation workflow, you'll need Hero, a software tool for medical image analysis. You can sign up for a free trial at their webpage: https://www.heroimaging.com/

#### Setup for Hero
To set up the data for running the workflow in Hero, watch the provided videos on loading data and batching. These videos will guide you through the process of configuring Hero to work with the ProstateZones dataset.


## Further Information

For more information about the dataset, see the Data publication:

....

## Citation
If you use this dataset in your work, please cite it as:

#### ProstateZones segmentations

- ...

#### PROSTATEx dataset

- Geert Litjens, Oscar Debats, Jelle Barentsz, Nico Karssemeijer, and Henkjan Huisman. "ProstateX Challenge data", The Cancer Imaging Archive (2017). DOI: 10.7937/K9TCIA.2017.MURS5CL
- Litjens G, Debats O, Barentsz J, Karssemeijer N, Huisman H. "Computer-aided detection of prostate cancer in MRI", IEEE Transactions on Medical Imaging 2014;33:1083-1092. DOI: 10.1109/TMI.2014.2303821
- Clark K, Vendt B, Smith K, Freymann J, Kirby J, Koppel P, Moore S, Phillips S, Maffitt D, Pringle M, Tarbox L, Prior F. The Cancer Imaging Archive (TCIA): Maintaining and Operating a Public Information Repository, Journal of Digital Imaging, Volume 26, Number 6, December, 2013, pp 1045-1057. DOI: 10.1007/s10278-013-9622-7
