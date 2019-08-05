# Yolo3 Module Training
In this specific case,
  - Target machine is equipped with i5-4200U, GT750M, 6G, 500G.
  - Target System is Ubuntu 18.04 LTS
  - Prepartion for training module with 1 class only recognition
  - This is __very__ case sepcific
  - Current working directroy is `~/darknet/[XX]` where [XX] is the folder that stores all these files
<br/> <br/>


### Pre-Requirements
1. A large amount of photos for training purpose (> 600 per class)
2. A large amount of photos for validation purpose (> 600 per class)
<br/> <br/>


### Objectives
   - Generate .xml and .txt files for preprocessing
   - Generate .data and .cfg for comment input
<br/> <br/>


### Generate Image List
Obtain all image file names and store it within a signle txt file <br/>
  __*Current Working Directory: [XX]*__
1. Place all images fpr training purposes under folder *pic_train*
2. Rename images __numerically__
3. Save names under *pic_train* to a signle text file named *pic_list.txt*
<br/> <br/>


### Tagging Imagines
Using [ImageNet-Utils](https://github.com/UniKerogen/ImageNet_Utils) to properly tag pictures <br/>
__*Current Working Directory: NEW TERMINAL WINDOW*__
1. Grab the source
    `git clone --recursive https://github.com/tzutalin/ImageNet_Utils.git`
2. Starting the application GUI. Using `apt install` for missing commands and `pip install` for missing python modules
    ```
    cd ImageNet_Utils/
    git submodule init
    git submodule update --recursive
    sudo apt-get install pyqt4-dev-tools
    cd labelImgGUI
    make all
    ./labelImg.py
    ```
3. Once the GUI starts running, use it to label the image and save the xml file to the same directory
<br/> <br/>


### Generate Labels for Imagines
Convert xml information for all images into a txt file that darknet can understand <br/>
  __*Current Working Directory: [XX]*__
1. Make sure that images are stored in the *pic_train* folder
2. Make sure that *pic_list.txt* exists
3. Download and run *label_generate.py* <br/>
    `python3 label_generate.py`
4. All label now should be generated and stored in *pic_train* folder
<br/> <br/>


### Write the .data File
Provide darknet with information regarding general information <br/>
  __*Current Working Directory: [XX]*__
```
classes = 1
train = FULL_PASS_TO_FILE
valid = FULL_PASS_TO_FILE
names = FULL_PASS_TO_FILE
backup = backup/
```
See included file for example
<br/>


#### Prepare train.txt File
This file should include the __FULL PASS__ to the images inside of pic_train


#### Prepare test.txt File
This file should include the __FULL PASS__ to the images for testing purposes


#### Prepare obj.names File
This file should include the name of class (1 class per line) <br/>
__*NOTICE:*__ Class names need to be corresponding with tag names
<br/> <br/>

  
### Prepare the .cfg file
Provide darknet with correct configuration for training <br/>
  __*Current Working Directory: [XX]*__
1. Get `Class` where `Class` is the number of class in obj.names 
2. Calculate `Filter` where `Filter=(class+5)*3`
3. Copy original cfg files to current directory
    ```
    cp ../cfg/yolov3.cfg cfg_yolov3.cfg
    cp ..cfg/yolov3-tiny.cfg cfg_tiny.cfg
    ```
4. Change the following value in cfg_ting.cfg
    - Line 3: `batch=24`
    - Line 4: `subdivisions=8`
    - Line 127 & 171: `filter=[FILTER_CALUCLATED_IN_STEP_2]`
    - Line 135 & 177: `class={CLASS_OBTAINED_IN_STEP_1]`
5. Change the following value in cfg_yolov3.cfg
    - Line 3: `batch=24`
    - Line 4: `subdivisions=8`
    - Line 603, 689 & 776: `filter=[FILTER_CALUCLATED_IN_STEP_2]`
    - Line 610, 696 & 783: `class={CLASS_OBTAINED_IN_STEP_1]`
<br/>

  
__NOTICE:__ If `CUDA Error: out of memory`, try to change `batch=16` and `subdivision=16` in cfg OR to other value that may work on GPU <br/>
__NOTICE:__ Pick only one cfg file to use
<br/> <br/>

    
### Training the Module
Use the following command and wait for it to finish <br/>
  __*Current Working Directory: ~/darknet*__
```
./darknet detector train [PASS_TO_.data_FILE] [PASS_TO_.cfg_FILE] darknet53.conv.74
```
It should take a long while to complete....<br/><br/>


#### Additional Material
[Training YOLOv3 : Deep Learning based Custom Object Detector](https://www.learnopencv.com/training-yolov3-deep-learning-based-custom-object-detector) form Learn OpenCV
