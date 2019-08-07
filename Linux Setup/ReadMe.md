# Preparation of Linux
In this specific case, 
  - Target machine is equipped with i5-4200U, GT750M, 6G, 500G.
  - Target System is Ubuntu 18.04 LTS


### Installing Linux
1. Set up Linux with a swap space of 2x of RAM size (Preferably with a clean install)
2. Update all packages
3. Install Graphic Driver
4. Install ssh-server for ssh services
5. Install git for git command support


### Installing Cuda Driver for Graphics Card
1. Get Cuda from [Cuda Developer](https://developer.nvidia.com/cuda-downloads)
2. Select _Linux_ -> _X86-64_ -> _Ubuntu_ -> _18.04_ -> _deb(network)_
3. In a new Terminal:
    ```
    cd Downloads
    sudo dpkg -i cuda-repo-ubuntu1804_10.1.168-1_amd64.deb
    sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
    sudo apt update
    sudo apt install cuda
    ```
    Now Cuda should be installing... (It takes a while)
4. Reboot after installation is finished
5. Verify Cuda installation via method provided by [Verify CUDA Installation](https://xcat-docs.readthedocs.io/en/stable/advanced/gpu/nvidia/verify_cuda_install.html) for Nvidia Driver version and Running a Cuda Sample
    ```
    cat /proc/driver/nvidia/version
    cd /usr/local/cuda-10.1/samples/
    make
    export PATH=/usr/local/cuda-10.1/bin:/usr/local/cuda-10.1/NsightCompute-2019.1${PATH:+:${PATH}}
    cd /usr/local/cuda-10.1/samples/bin/x86_64/linux/release
    ./deviceQuery
    ```
    Power9 and nvidia-persistenced should be running right after installation.
    The folllowing screen should be shown once the test is completed.
    <p align="center">
      <img src="https://github.com/UniKerogen/ShroomBot/blob/master/Supplemental%20Pictures/Cuda_Verification.png" width="50%"/>
    </p>
6. Include Nvidia Enviornment in Terminal Bashrc:
    ```
    cd ~
    nano .bashrc
    ```
7. At the end of file add the following lines:
    ```
    #Nvidia Enviornment Setup
    export PATH=/usr/local/cuda-10.1/bin:/usr/local/cuda-10.1/NsightCompute-2019.1${PATH:+:${PATH}}
    ```
8. After Installation clean-up:
    ```
    sudo apt update
    sudo apt upgrade
    sudo apt autoremove
    ```

    
### Installing Darknet
  More detailed instruction can be found [Installing Darknet](https://pjreddie.com/darknet/install/)
1. Installing from Darknet's github repository, in a *NEW* terminal:
    ```
    git clone https://github.com/pjreddie/darknet.git
    cd darknet
    ```
2. Modify the Makefile for GPU computing: `nano Makefile`
3. Find and change the line `GPU=0` to `GPU=1`, save and exit via bottom `control`+`x` and then `y` to save changes
4. Grab some weight file for darknet to function
    ```
    wget https://pjreddie.com/media/files/yolov3.weights
    wget https://pjreddie.com/media/files/darknet19.weights
    wget https://pjreddie.com/media/files/yolov3-tiny.weights
    wget http://pjreddie.com/media/files/vgg-conv.weights
    ```
5. Modify the yolov3.cfg file to specific GPU: `nano cfg/yolov3.cfg`
6. Change the starting couple lines to the following:
    ```
    batch=64
    subdivisions=64
    width=416
    height=416
    ```
7. Test darknet with sample imagine. The following image should be shown once test run is completed.
    `./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg`
    <p align="center">
      <img src="https://github.com/UniKerogen/ShroomBot/blob/master/Supplemental%20Pictures/Darkent_Test_Run.png" width="50%"/>
    </p>
8. Get Coco data sheets
    ```
    cp scripts/get_coco_dataset.sh data
    cd data
    bash get_coco_dataset.sh
    ```
9. Obtian Tiny Yolo3 Weight
    ```
    wget https://pjreddie.com/media/files/yolov3-tiny.weights
    ```
10. Obtain VOC data sets in preparation for training
    ```
    wget https://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar
    wget https://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar
    wget https://pjreddie.com/media/files/VOCtest_06-Nov-2007.tar
    tar xf VOCtrainval_11-May-2012.tar
    tar xf VOCtrainval_06-Nov-2007.tar
    tar xf VOCtest_06-Nov-2007.tar
    ```
11. Download pretrained convolution weights
    ```
    wget https://pjreddie.com/media/files/darknet53.conv.74
    ```
