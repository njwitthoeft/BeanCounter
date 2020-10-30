# BeanCounter
Image analysis for rapid phenotyping of soybeans. Developing under the UROP @ University of Minnesota

## Overview
This software is used to rapidly measure dimensions of seeds from images taken in a fixed overhead camera rig.

## Inputs
BeanCounter takes in an unstructured folder of images.
These images must be taken:
1. Be taken from a fixed position
2. Be taken in even and consistent lighting
3. Can contain barcodes identifying seedlots
4. Can be of any size, and contain any number of seeds
 
## Outputs
1. A i-line CSV containing measurements of individual seeds, where i is the number of seeds in the image
2. A one-line CSV containing population parameters of a seedlot
3. A i*j-line CSV containing information about each seed, where j is the number of images in the collection
4. A j-line CSV containing population parameters of a collection of seedlots

## Usage
1. Create a folder which contains all images of interest
2. Use the Create Project tool to add the folder of images to BeanCounter
3. Use the Actions -> Run tool to run the analysis: This should take less than 60 seconds
4. Use BeanCounter to view information about your seedlot and project
5. Use the Actions -> Make Report tool to export a CSV or CSV and PDF report
