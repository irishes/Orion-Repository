# Official Team Orion Repository
-------------------------------
**Package Installation**
--------------------------
*First Step*<br>
Download Miniconda 3 isis3 Enviornment
Miniconda 3 installation found <a href= https://github.com/USGS-Astrogeology/ISIS3/blob/dev/README.md>here</a>

'miniconda3 isis3' must be installed in the host pc directory (miniconda3 = python 3.6)
$USER_HOME/mininconda3/envs/isis3

This can be achieved by follow the github install


*Step Two*<br>
Clone the Repository into prefered IDE w/ .iml file support (Pycharm Prefered)

*command line execution is currently untested*

***=====================================================***

**Running Package**
--------------------------
*First Step*<br>
Start the ISIS3 conda environment

`conda activate isis3` 


*Step Two*<br>
Start your IDE from the command line that is using ISIS3
<br> `pycharm-community`


*Step Three*<br>

Test ISIS3 basic command

`lowpass -h

-> 


FROM        = Null <br>
TO          = Null <br>
SAMPLES     = Null <br>
LINES       = Null <br>
LOW         = Null <br>
HIGH        = Null <br>
MINOPT      = (*COUNT, PERCENTAGE) <br>
MINIMUM     = 1 <br>
REPLACEMENT = (*CENTER, NULL) <br>
FILTER      = (*ALL, INSIDE, OUTSIDE) <br>
NULL        = TRUE <br>
HRS         = TRUE <br>
HIS         = TRUE <br>
LRS         = TRUE <br>
LIS         = TRUE <br>
`

*Step Five*<br>
Run the startup script and feed it a .cub file
Currently the webpage runs the isis3 command:

`campt from= <your cube file>`

***=====================================================***


##Basic 'Alpha' Caption Writer
----------------------------------

1. Receive and save a cube file (.cub) from the user
2. Display the first object block of the data *(ISIS CONNECTION HAS BEEN MADE)*
3. Export an image(png or tiff) of the cube in any resolution or size
