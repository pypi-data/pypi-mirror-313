import os
import shutil
import mathwork  # Assuming mathwork package is installed

class Lab:
    def __init__(self, lab_number : str, lab_name):
        self.lab_number = lab_number
        self.lab_name = lab_name

    def get_pdf(self):
        # Fetch the path of the 'Lab Tasks' inside the installed mathwork package
        mathwork_path = os.path.dirname(mathwork.__file__)
        lab_tasks_path = os.path.join(mathwork_path, 'Lab Manuals')
        print("lab_manual_path: ", lab_tasks_path)

        # Check if the Lab Tasks folder exists
        if not os.path.exists(lab_tasks_path):
            return f"The 'Lab Manuals' folder does not exist in {mathwork_path}"

        # Search for the PDF file that matches the lab number and name
        for filename in os.listdir(lab_tasks_path):
            if filename.startswith('CV Lab-' + self.lab_number) and filename.endswith('.pdf'):
                file_path = os.path.join(lab_tasks_path, filename)
                shutil.copy(file_path, os.getcwd())  # Copy to current working directory
                return f"{self.lab_name} PDF copied to current directory: {filename}"
        
        return f"{self.lab_name} PDF not found"

class LabTasks:
    def copy_all(self):
        # Get the path of the 'Lab Tasks' folder inside mathwork package
        mathwork_path = os.path.dirname(mathwork.__file__)
        source_folder = os.path.join(mathwork_path, 'Lab Tasks')
        destination_folder = os.path.join(os.getcwd(), 'Lab Tasks')  # Current working directory + Lab Tasks folder
        
        # Check if the source folder exists
        if not os.path.exists(source_folder):
            return f"The source folder '{source_folder}' does not exist."
        
        # Create the destination folder 'Lab Tasks' if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            print(f"Created folder: {destination_folder}")
        
        # Iterate over all the files and subfolders in the Lab Tasks folder
        for item in os.listdir(source_folder):
            source_path = os.path.join(source_folder, item)
            destination_path = os.path.join(destination_folder, item)
            
            # If it's a directory, use shutil.copytree to copy the entire directory
            if os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path)
                print(f"Directory {source_path} copied to {destination_path}")
            
            # If it's a file, use shutil.copy to copy the file
            elif os.path.isfile(source_path):
                shutil.copy(source_path, destination_path)
                print(f"File {source_path} copied to {destination_path}")
        
        return "All files and directories from 'Lab Tasks' have been copied to 'Lab Tasks' folder in the current directory."
