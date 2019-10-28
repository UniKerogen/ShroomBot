##############################################################
#   Libraries
##############################################################
import sys
import os
from PIL import Image

##############################################################
#   Variable Definition
##############################################################
DIRECTORY = os.getcwd()
DARKNET = "/home/parallels/darknet"


##############################################################
#   Class Definition
##############################################################
class peters526:
	def __init__(self, file_name=None):
		self.default_file = file_name
		self.cfg = DIRECTORY + "/cfg_tiny.cfg"
		self.weights = DIRECTORY + "/peters-5.2.6.weights"
		self.data = DIRECTORY + "/data_inmyhead.data"
		self.threshold = 0.3

	# Classify Function
	def classify(self, file_name, threshold=None, img_manipulated=False):
		# Determine Threshold
		if not threshold:
			if 0.1 <= threshold < 1:
				thres = threshold
			elif threshold < 0.1:
				while threshold < 0.1:
					threshold = threshold * 10
				thres = threshold
			else:
				while threshold >= 1:
					threshold = threshold / 10
				thres = threshold
		else:
			thres = self.threshold
		# Terminal Command
		os.chdir(DARKNET)
		darknet_command = "./darknet detector test " + self.data + " " + self.cfg + " " + self.weights + " " + DIRECTORY + "/" + file_name + " -thresh " + threshold
		os.system(darknet_command)
		os.chdir(DIRECTORY)

		# Copy Result pic to current folder
		predicted_file = DARKNET + "/predictions.jpg"
		if img_manipulated:
			traget = DIRECTORY + "/grey_scaled_" + file_name.split("_")[0] + ".jpg"
		else:
			traget = DIRECTORY + "/original_" + file_name.split(".")[0] + ".jpg"
		move_command = "mv " + predicted_file + " " + traget
		os.system(move_command)

		# Remove manipulated image file if exists
		if img_manipulated:
			os.remove(file_name)

	# Grey Scale Function
	def grey_scale(self, file_name):
		# Open and convert image
		image = Image.open(file_name).convert("LA")
		# Save image
		image.save(file_name.split(".")[0] + "_temp.png")
		# return the name of the save image
		return file_name.split(".")[0] + "_temp.png"

##############################################################
#   Function Prototype
##############################################################
def athletic(command, file_path, threshold=None):
    # Set Classifier
	peters = peters526(file_name=None)
	if command == "-r":
		peters.classify(file_name=file_path, threshold=threshold, img_manipulated=False)
	elif command == "-g":
		peters.classify(file_name=peters.grey_scale(file_name=file_name), threshold=threshold, img_manipulated=True)
	elif command == "-a":
		peters.classify(file_name=file_path, threshold=threshold, img_manipulated=False)
		peters.classify(file_name=peters.grey_scale(file_name=file_path), threshold=threshold, img_manipulated=True)
	else:
		print("Error(502): Invalid opertaion")
		os.system("python3 peters-v5.py -h")

##############################################################
#   Main Function
##############################################################
def main(argc, argv):
	print("Hello World!")
	if argc == 3:
		threshold = argv[2]
	else:
		threshold = None
	athletic(command=argv[0], file_path=argv[1], threshold=threshold)


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
	if sys.argv[1] == "-h" or sys.argv[1] == "-help":
		print("Help Message")
		print("python3 peters-v5.py [FUNCTION] [FILE_NAME(Optional)] [THRESHOLD(Optional)]")
		print("")
		print("Usage")
		print(" -h						| Print this help message")
		print(" -a [FILE] [THRESHOLD]	| Run with regular photo and grey scaled photo")
		print(" -g [FIlE] [THRESHOLD]	| Run with a grey scaled photo")
		print(" -r [FILE] [THRESHOLD]	| Run with input photo")
	elif 1 < len(sys.argv)-1 < 4:
		main(len(sys.argv)-1, sys.argv[1:])
	else:
		print("Error(501): Invalid Input")
		os.system("python3 peters-v5.py -h")
