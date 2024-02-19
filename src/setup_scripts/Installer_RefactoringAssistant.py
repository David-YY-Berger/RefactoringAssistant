import ctypes
import shutil
import os

import win32com.client

runner_exe_path = r"Y:\QA\Automation\RefactoringAssistant\runner.exe"
dest_dir_for_runner = os.path.join(os.path.expanduser('~\\AppData\\Local'), 'RefactoringAssistantHidden')
dest_path_for_runner = os.path.join(dest_dir_for_runner, 'RefactoringAssistant.exe')
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
icon_path = r"Y:\QA\Automation\RefactoringAssistant\refactoringImage.ico"


def main():

    print("Installing the exe file to: " + dest_path_for_runner)
    if not os.path.exists(dest_dir_for_runner):
        os.makedirs(dest_dir_for_runner)
    hide_path(dest_dir_for_runner)
    if not os.path.exists(runner_exe_path):
        raise FileNotFoundError(f"Could not find runner path! '{runner_exe_path}' ")
    if os.path.exists(dest_path_for_runner):
        os.remove(dest_path_for_runner)
    shutil.copyfile(runner_exe_path, dest_path_for_runner)
    hide_path(runner_exe_path)
    create_desktop_shortcut(dest_path_for_runner, 'RefactoringAssistant_Shortcut',  icon_path=icon_path)
    input("Success! \n"
          "Find the the application at: " + dest_dir_for_runner + "\n" +
          "Recommended to create a shortcut for the desktop (right click > 'Create Shortcut')\n"
          "Press any key to close the program :)")


def create_desktop_shortcut(target_path, shortcut_name, icon_path=None):
    path_for_shortcut = dest_dir_for_runner
    shortcut_path = os.path.join(path_for_shortcut, shortcut_name + ".lnk")

    # Create a ShellLinkObject
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    try:
        shortcut.TargetPath = target_path
        if icon_path:
            shortcut.IconLocation = icon_path
        shortcut.Save()
    except Exception as e:
        print(f"Exception occurred: {e}")
        if hasattr(e, 'winerror'):
            print(f"WinError: {e.winerror}")
        if hasattr(e, 'argerror'):
            print(f"ArgError: {e.argerror}")


def hide_path(path):
    attrs = ctypes.windll.kernel32.GetFileAttributesW(path)
    ctypes.windll.kernel32.SetFileAttributesW(path, attrs | 2)


if __name__ == "__main__":
    main()
