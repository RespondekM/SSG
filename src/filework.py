import os
import shutil
#   os.path.exists
#   os.listdir
#   os.path.join
#   os.path.isfile
#   os.mkdir
#   shutil.copy
#   shutil.rmtree

def target_path_cleanup(target_path="../public"):
    if os.path.exists(target_path):
        print (f"Will delete: {target_path} with the following files: {os.listdir(path=target_path)}")
        shutil.rmtree(target_path)
def copy_source_to_target(source_path="../static", target_path="../public"):
    if not os.path.exists(target_path):
        os.mkdir(target_path)
        print(f"Target_path {target_path} created")
    for object in os.listdir(source_path):
        object_with_path = f"{source_path}/{object}"
        target_with_path = f"{target_path}/{object}"
        if os.path.isfile(object_with_path):
            print("Is file:", object_with_path)
            shutil.copy(object_with_path,target_with_path)
        elif os.path.isdir(object_with_path):
            print("Is dir:", object_with_path)
            copy_source_to_target(object_with_path,target_with_path)

def main():
    target_path_cleanup()
    copy_source_to_target()

