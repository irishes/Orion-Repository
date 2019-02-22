Official Team Orion Repository
=====================================================

Package Installation
--------------------------

###First Step<br>
Download Miniconda 3 ISIS3 Environment

You must have Miniconda ISIS3 installed in the path 
`$USER_HOME/mininconda3/envs/isis3`
And this can be done by following the install instructions found 
<a href= https://github.com/USGS-Astrogeology/ISIS3/blob/dev/README.md>
here for both the conda base environment isis3</a><br>'miniconda3 isis3'
 must be installed in the host pc directory (miniconda3 = python 3.6 or higher)
 The default install location for both programs should be sufficient. 

**Important: When the conda enviornament install asks you if you would like to add the conda 
path to your .bash file, you must put yes to give the main command line access to your conda 
commands**

This can be achieved by follow the github install


###Step Two
Clone the Repository into prefered IDE w/ .iml file support (Pycharm Prefered)

**command line execution is currently untested**

Running Package
=======================

###First Step<br>
Start the ISIS3 conda environment

`conda activate isis3` 



###Step Two<br>
Start your IDE from the command line that is using ISIS3

`pycharm-community` or `sudo pycharm-community` 

(depending on your installation)



###Step Three<br>
Test ISIS3 basic command
```
lowpass -h' 
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


###Step Five
Run the startup script and feed it a .cub file
Currently the webpage runs the isis3 command:

`campt from= <your cube>`


Basic 'Alpha' Caption Writer
=====================================================
1. Receive and save a cube file (.cub) from the user
2. Display the first object block of the data *(ISIS CONNECTION HAS BEEN MADE)*
3. Export an image(png or tiff) of the cube in any resolution or size


Alpha Caption Writer
=====================================================
1. Receive and save a cube file (.cub) from the user as well as optionally taking in
a template cube.

2. Bring the user to a page with an editable template. Include a display of 
all the needed metadata and the tags that will correspond to the data in the template
file when it is converted.

3. The user will have the option to export the metadata and caption in various forms 
if they desire.

4. When the template looks correct the user can move onto a page where they can view the caption
and the image of the cube that they uploaded.



Beta Caption Writer
=====================================================
1. Receive and save a cube file (.cub) from the user as well as optionally taking in
a template cube.

2. Bring the user to a page with an editable template. Include a display of 
all the needed metadata and the tags that will correspond to the data in the template
file when it is converted.

3. The user will have the option to export the metadata and caption in various forms 
if they desire.

4. When the template looks correct the user can move onto a page where they can view the caption
and the image of the cube that they uploaded.

5. The user can use the check boxes on the image page to add icons based on the metadata and can 
adjust the location of the caption that appears over the figure.

6. The user will be able to crop the image and add icons to the new figure

7. The user will have the ability to export the whole figure as it appears on screen to 
multiple formats 