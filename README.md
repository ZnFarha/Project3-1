# Project3-1
To run the project, please run BabyWatcherUI.py that can be found in the BabyWatcherUI Folder.
It will be run as a localhost application. You will be able to inspect it via your web browser.\
Note: The application will crash if it does not find anything in the image. If that does happen, please reload the page and input an image that actually has baby features that can be detected.


Before running the program, make sure you download the model and the cfg file you want to use from https://drive.google.com/drive/folders/1bVZF-2cE-Fuh3Fq47gJchgQyQMZfmhvZ?usp=sharing . 
Then place them in the correct folder (Model1000 or Model2000) and then change the paths accordingly in Run_Yolo.py .


To try out the HOG+SVM model, run the notebook 'Script - HOG approach.ipynb' in src/HOG
requirements:
pandas, numpy, cv2 (opencv), matplotlib, sklearn, skimage, pickle, tkinter
