import BasicFunctions
import ImageCropper
import ImageProcessor


image_folder = BasicFunctions.resources_path+"/images/1"
csv_file = BasicFunctions.resources_path+"/images/emery-labels-1.csv"

#ImageCropper.crop_from_csv(csv_file, image_folder, True, True, False)
ImageProcessor.w(image_folder)
