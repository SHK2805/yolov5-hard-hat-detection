import os
import shutil


class DataTransformer:
    def __init__(self, old_root, new_root):
        self.old_root = old_root
        self.new_root = new_root
        self.old_folders = ["train", "test", "valid"]
        self.new_folders = ["images", "labels"]

        # Create the new folder structure
        self.create_new_folder_structure()

    def create_new_folder_structure(self):
        for new_folder in self.new_folders:
            os.makedirs(os.path.join(self.new_root, new_folder), exist_ok=True)
            for old_folder in self.old_folders:
                os.makedirs(os.path.join(self.new_root, new_folder, old_folder), exist_ok=True)

    def copy_files(self, src_folder, dest_folder, file_extension):
        for old_folder in self.old_folders:
            src_path = os.path.join(self.old_root, old_folder, src_folder)
            dest_path = os.path.join(self.new_root, dest_folder, old_folder)
            for file_name in os.listdir(src_path):
                if file_name.endswith(file_extension):
                    src_file = os.path.join(src_path, file_name)
                    dest_file = os.path.join(dest_path, file_name)
                    shutil.copy(src_file, dest_file)

    def validate_data(self):
        for old_folder in self.old_folders:
            images_path = os.path.join(self.new_root, "images", old_folder)
            labels_path = os.path.join(self.new_root, "labels", old_folder)
            images = {os.path.splitext(img)[0] for img in os.listdir(images_path) if img.endswith(".jpg")}
            labels = {os.path.splitext(lbl)[0] for lbl in os.listdir(labels_path) if lbl.endswith(".txt")}

            missing_labels = images - labels
            missing_images = labels - images

            if missing_labels:
                print(f"Missing labels for images in {old_folder}: {missing_labels}")
            if missing_images:
                print(f"Missing images for labels in {old_folder}: {missing_images}")

            if not missing_labels and not missing_images:
                print(f"All images and labels are matched in {old_folder}")

    def transform_data(self):
        # Copy images and labels
        self.copy_files("images", "images", ".jpg")
        self.copy_files("labels", "labels", ".txt")
        print("Files have been copied successfully!")

        # Validate the data
        self.validate_data()


# Usage example
old_root = "../artifacts/data_ingestion"
new_root = "../artifacts/data_transformation"

transformer = DataTransformer(old_root, new_root)
transformer.transform_data()
