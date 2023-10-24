# ShroomBot

## Overview
Senior Design Project for a group of us started in 2019. 
The aim of the project is to create a robot to pick mashroom in mashroom farms, so that it would work 24/7 with onboard cameras and algorithm to pick target mushrooms at its "perfect" time. It would also relief the pressure of worker shortage at the time.

## Files
- arm - Robot Arm Setup
- Linux Setup - training computer setup
- RaspberryPi Setup - onboard raspberrypi setup
- Supplemental Pictures - some supplemental pictures used in the project
- Yolo3Module - customized yolo3 modules
- design_files - robot design files

## Simulation Image Recognition Result
|                                      Original                                       |                                      Recognized Sample                                       |
|:---------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------:|
| ![](https://github.com/UniKerogen/ShroomBot/blob/master/Yolo3Module/peters/dummy.jpg) | ![](https://github.com/UniKerogen/ShroomBot/blob/master/Yolo3Module/peters/original_dummy.jpg) | 

## What I did in this Project
- Designed algorithms and trained machine learning modules using Tesnorflow, Python, C, and CUDA in both local machine for small batches of 5000 images and Amazon Web Servers (AWS) with large data that exceeding 20,000 images, with the purpose of identifing various types of mushrooms within photographs and live video feed.
- Crafted and optimized methods, algorithms, and structures based on aspects of the physical location of machines, interconnection speed within the network, and workflow analysis for both machines and the network, to achieve optimal data communication speed in between on-board modules and networked machines with validation during runtime.
- Collaboratively devised and revised computer model for the robot using Solidworks and AutoCAD. Architected software designs that incorporated machine learning, inter-process communications, hardware design, and arm mechanics for computer simulations and verification of both methmatical model and CAD model. 
- Delineated robot test criteria, test cases and test result validation for selected and automated functional tests of arm and vision systems. Developed remote robot monitoring algorithms and robot test data recording algorithms for documentation and version comparison during the robot’s testing phase.
