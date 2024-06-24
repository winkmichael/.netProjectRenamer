# .netProjectRenamer
.netProjectRenamer

Description:
The .netProjectRenamer is a Python script that automates the process of renaming a .NET project and all its recursive references. It is designed to simplify the task of renaming a project, which can be a tedious and error-prone process when done manually, especially for large projects with numerous files and directories.
Usage:
To use the .netProjectRenamer, follow these steps:

Open a terminal or command prompt.
Navigate to the directory where the projectRename.py script is located.
Run the script using the following command:

python3 projectRename.py -d "originalProjectDirectory" -f "originalProjectDirectory" -r "newProjectName"

Replace "originalProjectDirectory" with the path to the directory containing the original project you want to rename.
The second reference to "originalProjectDirectory" should be the actual name of the project directory.
Replace "newProjectName" with the desired new name for the project.


Notes:

The script will create a new directory with the specified new project name and copy all the files and directories from the original project directory to the new one.
The script will recursively traverse the new project directory and update all references to the original project name with the new project name. This includes file contents, file names, and directory names.
The script has been tested with .NET Xamarin and .NET MAUI projects, but it should work with other .NET project types as well.

Cautions and Warnings:

Before running the script, make sure you have a backup of your original project directory. Although the script creates a new directory and doesn't modify the original project directly, it's always a good practice to have a backup in case something goes wrong.
The script modifies files and directories, so it's recommended to run it with administrator privileges to avoid any access or corruption issues.
Double-check the original project directory path, original project name, and new project name before running the script to ensure they are correct.
Review the changes made by the script after it finishes execution to verify that the renaming process completed successfully and as expected.
