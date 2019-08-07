# Setting Up Raspebrry Pi to Control Servo
In this specific case,
  - Target Machine is a Raspberry Pi 3 running Raspbian GNU/Linux 10 (buster)
  - Servo Module is LX15D, with angle range of 0 - 240 degrees (0 - 1000 resepectfully)
<br/> <br/>


### Preparing the Raspberry Pi
Initial Raspberry Pi setup
1. Flush and install Raspbian on Raspberry Pi

2. Enable `ssh` and `serial` of Raspberry Pi via GUI tool `Raspberry -> Preferences -> Raspberry Pi Configuration` Or command line `sudo raspi-config`

3. Reboot to take affect of the change.

4. In a new Terimal, use command `ls -l /dev | grep serial` to view current Serial Configuration
  The following screen should be shown.
  <p align="center">
    <img src="https://github.com/UniKerogen/ShroomBot/blob/master/Supplemental%20Pictures/Setting%20Up%20Raspbeery%20Pi%20-%20Serial.png" width="50%"/>
  </p>
  
5. Use command `sudo nano /boot/config.txt` to edit config file

6. At the end of the config.txt, add `dtoverlay=pi3-miniuart-bt`

7. Save config.txt and reboot.

8. In a new Terminal, use command `ls -l /dev | grep serial` to view changed Serial Configuration
  The following screen should be shown.
  <p align="center">
    <img src="https://github.com/UniKerogen/ShroomBot/blob/master/Supplemental%20Pictures/Setting%20Up%20Raspbeery%20Pi%20-%20Serial2.png" width="50%"/>
  </p>
  
9. Use the following commands to disbale Serial Control on ttyAMA0
  ```
  sudo systemctl stop serial-getty@ttyAMA0.service
  sudo systemctl disable serial-getty@ttyAMA0.service
  ```
  
10. Use command `sudo nano /boot/cmdline.txt` to change cmdline.txt file

11. Delete text `consol=serial0,115200`

12. Save file and reboot.
