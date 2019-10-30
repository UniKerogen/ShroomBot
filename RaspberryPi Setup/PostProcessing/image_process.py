##############################################################
#   Libraries
##############################################################
import sys
import os
from PIL import Image
import numpy as np
import cv2


##############################################################
#   Variable Definition
##############################################################
TARGET_VALUE = [255, 0, 255]  # RGB 255, 0, 255
BOX_WIDTH = 18  # Pixels
RESULT_FILE = "result_center.txt"
PHYSICAL_WIDTH = 22  # inches
PHYSICAL_HEIGHT = 16.5  # inches


##############################################################
#   Class Definition
##############################################################
class PhotoProcess:
    def __init__(self, photo_name):
        self.image_name = photo_name
        self.image = Image.open(self.image_name)
        self.width, self.height = self.image.size
        self.pixel_values = list(self.image.getdata())
        if self.image.mode == 'RGB':
            self.channels = 3
        elif self.image.mode == 'L':
            self.channels = 1
        else:
            print("Error(602): Unknown mode: %s" % self.image.mode)
            exit(602)
        if os.path.isfile(RESULT_FILE):
            self.result_file = RESULT_FILE
            self.center_array = None
            self.count = 0
            initialized = False
            with open(self.result_file, "r") as f:
                for line in f.readlines():
                    temp = np.array([int(line.split(" ")[2]), int(line.split(" ")[3])])
                    if not initialized:
                        self.center_array = temp
                        initialized = True
                        self.count += 1
                    else:
                        self.center_array = np.row_stack([self.center_array, temp])
                        self.count += 1
        else:
            print("Error(603): Unable to read the result file")
            exit(603)

    # Generate and create a mask for box of the image
    def mask(self):
        # Read Image
        image = cv2.imread(self.image_name)
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # mask of Pink
        mask = cv2.inRange(hsv, (140, 140, 140), (160, 255, 255))
        # Slice
        imask = mask > 0
        # Sliced Image
        box = np.zeros_like(image, np.uint8)
        box[imask] = image[imask]
        # save
        cv2.imwrite("box.png", box)

    # Determine and pass out the center point of the box
    def center(self, passable=True):
        # Control Variable
        initialized = False
        physical_center = np.array([-1, -1])
        # Determine Physical Point
        for logical_center in self.center_array[:, :]:
            if not initialized:
                physical_center = np.array([logical_center[0] / self.width * PHYSICAL_WIDTH,
                                            logical_center[1] / self.height * PHYSICAL_HEIGHT])
                initialized = True
            else:
                physical_center = np.row_stack([physical_center,
                                                [logical_center[0] / self.width * PHYSICAL_WIDTH,
                                                 logical_center[1] / self.height * PHYSICAL_HEIGHT]])
        return physical_center


##############################################################
#   Function Prototype
##############################################################
def athletic(file_name):
    photo = PhotoProcess(photo_name=file_name)
    result = photo.center()
    print(result)


##############################################################
#   Main Function
##############################################################
def main(argc, argv):
    athletic(file_name=argv[0])


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error(605): Not enough input")
        os.system("python3 image_process.py -h")
    elif sys.argv[1] == "-h" or sys.argv[1] == "-help":
        print("Help Message")
        print("python3 image_process.py [FILE_NAME]")
        print("")
        print("Usage")
        print(" -h          | Print this help message")
        print(" [FILE_NAME] | Run program with selected file name")
    elif 0 < len(sys.argv)-1 < 2:
        if os.path.isfile(sys.argv[1]):
            main(len(sys.argv)-1, sys.argv[1:])
        else:
            print("Error(604): File does not exists")
    else:
        print("Error(601): Invalid Input")
        os.system("python3 image_process.py -h")
