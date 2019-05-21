Official Team Orion Repository
=====================================================

Package Installation
--------------------------

**First Step**<br>
Download Miniconda 3 ISIS3 Environment

You must have Miniconda ISIS3 installed in the path 
`$USER_HOME/mininconda3/envs/isis3`
And this can be done by following the install instructions found 
<a href= https://github.com/USGS-Astrogeology/ISIS3/blob/dev/README.md>
here for both the conda base environment & isis3</a><br>

**DO NOT INSTALL THE COMPLETE ISIS3 DATA DISTRIBUTION**: 

It is far too big to be useful for this application
 
The default install location for both programs should be sufficient. 

**Important: When the conda environment install asks you if you would like to add the conda 
path to your .bashrc file, you must put yes to give the main command line access to your conda 
commands. 

All the above can be achieved by follow the github install 


**Step Two**<br>
Clone the Repository into prefered IDE w/ .iml file support (Pycharm prefered for this)
or download and run it on command line in the Project Directory

Running Package
=======================

**First Step**<br>
Run the ISSS.py to create the server


`python3 ISSS.py`
or
`python ISSS.py`


**Step Two**<br>
Test ISIS3 basic command
```
$ lowpass -h 


-> 
FROM        = Null
TO          = Null
SAMPLES     = Null
LINES       = Null
LOW         = Null
HIGH        = Null
MINOPT      = (*COUNT, PERCENTAGE)
MINIMUM     = 1
REPLACEMENT = (*CENTER, NULL)
FILTER      = (*ALL, INSIDE, OUTSIDE)
NULL        = TRUE
HRS         = TRUE
HIS         = TRUE
LRS         = TRUE
LIS         = TRUE
```


**Step Three**
Run the startup script and feed it a .cub file
Currently the webpage runs the isis3 command:

`isis2std from= <your cube>`
`campt from= <your cube>`
`catlab from= <your cube>`
`catoriglab from= <your cube>`


**Step Four**
Shutdown The Server with 
`ctrl + c`


Alpha Caption Writer
=====================================================
~~1. Receive and save a cube file (.cub) from the user as well as optionally taking in
a template cube.~~

~~2. Bring the user to a page with an editable template. Include a display of 
all the needed metadata and the tags that will correspond to the data in the template
file when it is converted.~~

~~3. The user will have the option to export the metadata, template and caption in various forms 
if they desire.~~

~~4. When the template looks correct the user can move onto a page where they can view the caption
and the image seperatly from the caption.~~


Beta Caption Writer (S.T.C.)
=====================================================
~~1. Receive and save a cube file (.cub) from the user as well as optionally taking in
a template cube.~~

~~2. Bring the user to a page with an editable template. Include a display of 
all the needed metadata and the tags that will correspond to the data in the template
file when it is converted.~~

~~3. The user will have the option to export the metadata and caption in various forms 
if they desire.~~

~~4. When the template looks correct the user can move onto a page where they can view the caption
and the image of the cube that they uploaded.~~

~~5. The user can use the check boxes on the image page~~ to add icons based on the metadata and can 
 adjust the location of the caption that appears over the figure.

 6. The user will have the ability to export the whole figure as it appears on screen to 
 multiple formats 
