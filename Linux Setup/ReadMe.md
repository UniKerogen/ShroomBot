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
    ##sudo apt install nvidia-cuda-toolkit
    ```
    Now Cuda should be installing...
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
6. Include Nvidia Enviornment in Terminal Bashrc:
    `cd ~`
    `nano .bashrc`
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
3. Find and change the line `GPU=0` to `GPU=1`, save and exit via `control`+`x` and then `y`
4. 
