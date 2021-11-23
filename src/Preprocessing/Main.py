import BasicFunctions
import ImageCropper


image_folder = BasicFunctions.resources_path+"/1"
csv_file = BasicFunctions.resources_path+"/emery-labels-1.csv"

ImageCropper.crop_from_csv(csv_file, image_folder, False, False, True)
