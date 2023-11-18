import os
import sys
import subprocess
import xml.etree.ElementTree as ET

def main():
    print("Welcome to the Template App configuration script.")
    print("Please follow the steps to configure your project.")

    initial_working_directory = os.getcwd()  # Store the initial working directory

    # Step 1: Clone the Template App project
    choice1 = input("1. Do you want to clone this Template App project? (yes/no): ")
    if choice1.lower() == "yes":
        repo_url = "https://github.com/HamzaElalaouiElismaili/template_app_repo.git"
        cloned_folder_name = input("Enter the name for the cloned repository folder: ")
        subprocess.run(["git", "clone", repo_url, cloned_folder_name])
        os.chdir(cloned_folder_name)
    else:
        print("Thanks for using the configuration script.")
        sys.exit(0)

    # Step 2: Change the package name
    choice2 = input("2. Do you want to change the package name? (yes/no): ")
    if choice2.lower() == "yes":
        new_package_name = input("Please enter the new package name: ")
        os.chdir(initial_working_directory) 
        update_pubspec_yaml(new_package_name, cloned_folder_name)
        # update_android_manifest(new_package_name, cloned_folder_name)


    # Step 3: Generate the project
    choice3 = input("3. Do you want to generate the project? (yes/no): ")
    
    if choice3.lower() == "yes":
        os.chdir(cloned_folder_name)
        subprocess.run(["flutter", "clean"])
        subprocess.run(["flutter", "pub", "get"])
        subprocess.run(["dart", "pub", "global", "activate", "flutter_gen"])
        subprocess.run(["flutter", "gen-l10n"])
        subprocess.run(["flutter", "pub", "run", "build_runner", "build", "-d"])
        subprocess.run(["rm", "-Rf", ".git"])

    # Step 4: Open the project
    choice4 = input("4. Do you want to open the project? (yes/no): ")
    if choice4.lower() == "yes":
        if is_vscode_installed():
            subprocess.run(["code", "."])
        else:
            print("Visual Studio Code is not installed. Please open the project manually.")

    print("Configuration completed. Thank you!")

def update_pubspec_yaml(new_package_name, folder_name):
    pubspec_path = os.path.join(folder_name, "pubspec.yaml")
    print("Full path:", pubspec_path)
    print("Current working directory:", os.getcwd())


    with open(pubspec_path, "r") as file:
        lines = file.readlines()

    with open(pubspec_path, "w") as file:
        for line in lines:
            if line.strip().startswith("name:"):
                file.write(f"name: {new_package_name}\n")
            else:
                file.write(line)

def update_android_manifest(new_package_name, folder_name):
    manifest_file = os.path.join(folder_name, "android/app/src/main/AndroidManifest.xml")
    tree = ET.parse(manifest_file)
    root = tree.getroot()

    for elem in root.iter():
        if elem.tag.endswith("}manifest"):
            elem.set("package", new_package_name)

    tree.write(manifest_file)

def is_vscode_installed():
    try:
        subprocess.run(["code", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    main()
