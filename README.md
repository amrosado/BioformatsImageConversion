# Bioformats Image Conversion
A python script to dump a series of images from an OME metadata library such as a Volocity library.  Deals with bfconvert not processing patterns in series output correctly.

## Running
1. Install bioformats cmd line tools from and append to system path (https://docs.openmicroscopy.org/bio-formats/6.5.0/users/comlinetools/index.html)
2. Pip install all requirements using the requirements.txt file
```pip install -r requirements.txt```
2. Run BioformatsFileConversion.py after changing your paths for the input and output
```python BioformatsFileConversion.py```
3. Wait for all files to be converted.

## What does the code do?
The code just processes xml output from shoinf in bftools and uses the xml output to dump all image series from a OME Image library using bfconvert.  I wasn't able to do this with a volocity library using bioformats cmd line tools.

## contact
If you have any questions or feature requests contact Aaron Rosado (arosad2@protonmail.ch) or use Github Issues.