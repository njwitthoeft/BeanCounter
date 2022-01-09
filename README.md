# BeanCounter
Image analysis for rapid phenotyping of soybeans. Developed under the [UROP @ University of Minnesota](https://hdl.handle.net/11299/219531)

### BeanCounter is published (but not peer-reviewed)!
[Nicholas' poster from Early 2021](https://hdl.handle.net/11299/219531)

![image](https://user-images.githubusercontent.com/49255471/148705955-8bb7cdad-7335-4054-8ead-2292c8965cfc.png)

## #BeanCounter is published again!
[Sam Kuralle's Poster from Late 2021](https://www.linkedin.com/feed/update/urn:li:activity:6872335054912196608/)

![1638492357851](https://user-images.githubusercontent.com/49255471/148706144-ee81c777-7fc1-416c-a8d0-f6822625e70c.jpg)


## Overview
This software is used to rapidly measure dimensions of seeds from images taken in an overhead camera rig.

## Inputs
Use python main_interactive_mask.py -inpath "YOUR_FOLDER" to set the input folder. In my use case, images were overhead shots of a seed-counting tray. This allows the beans to be placed approximately equidistant from each other.

## Outputs
A csv with filename, seed number, a calibration distance (farthest two seeds), surface area, perimeter, circularity, length, width, and aspect ratio.

## Usage
Set up an environment using anaconda. Run conda env create -f analysis.yml to make an environment named analysis.
Activate the analysis environment, then run main_interactive_mask.py -inpath "YOUR_FOLDER"

The images will load, then the first will be used to mask areas outside of the seed tray. 

![Masked](extras/traced.png)
![Traced](extras/masked.png)

After masking, use any key to move forward and review each image, or hold down to skip through the images. If imaged are not consitently framed, the mask may interfere with the seed shape description.


The program will output a 'results.csv' file with each seed of each image as a row. 

Files should be named in a way that identifies the accession in the image.
