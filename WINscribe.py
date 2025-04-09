import os
import subprocess
import argparse
from shutil import which

# --- Dependency Checks ---
def check_dependency(cmd, install_hint):
    result = subprocess.run(['which', cmd], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Missing dependency: '{cmd}' not found in PATH.")
        print(f"Install with: {install_hint}")
        exit(1)

check_dependency("wimlib-imagex", "brew install wimlib")

try:
    import pycdlib
except ModuleNotFoundError:
    print("[ERROR] Missing dependency: pycdlib")
    print("Install with: pip3 install pycdlib")
    exit(1)

print("All required dependencies found. Continuing...\n")

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description="WINscribe - Bootable Windows USB creator for macOS")
parser.add_argument('--iso', help='Path to the Windows ISO file')
parser.add_argument('--output', help='Custom output directory (default is ./usb_files)', default=None)
parser.add_argument('--quiet', action='store_true', help='Suppress normal output')
parser.add_argument('--version', action='version', version='WINscribe v1.0')
args = parser.parse_args()

pwd = os.getcwd()
usb_files_path = args.output if args.output else os.path.join(pwd, "usb_files")
os.makedirs(usb_files_path, exist_ok=True)
os.makedirs(os.path.join(pwd, ".the_curtain"), exist_ok=True)

# List ISO files and prompt user if not provided
if not args.iso:
    print("\nISO images found:")
    for iso_file in os.listdir(pwd):
        if iso_file.endswith(".iso"):
            print(iso_file)
    print("\n")
    path_to_iso = os.path.join(pwd, input("Enter the name of the ISO file you want to use: \n"))
else:
    path_to_iso = os.path.abspath(args.iso)

if not os.path.isfile(path_to_iso):
    print(f"[ERROR] ISO not found: {path_to_iso}")
    exit(1)

iso = pycdlib.PyCdlib()
iso.open(path_to_iso)
if not args.quiet:
    print(f"\nContinuing with: {path_to_iso}\n")

for path, dirlist, files in iso.walk(udf_path='/'):
    for directory in dirlist:
        local_dir_path = os.path.join(f"{usb_files_path}{path}", directory)
        os.makedirs(local_dir_path, exist_ok=True)

    for file in files:
        full_path = os.path.join(path, file)
        if file.endswith("install.wim"):
            if not args.quiet:
                print(f"Reticulating splines: {path_to_iso}{full_path}")
            temp_wim_path = os.path.join(pwd, ".the_curtain", "temp_install.wim")
            iso.get_file_from_iso(local_path=temp_wim_path, udf_path=full_path)

            output_swm_path = os.path.join(usb_files_path, "sources", "install.swm")
            command = ['wimlib-imagex', 'split', temp_wim_path, output_swm_path, str(3800)]
            subprocess.run(command, capture_output=True, text=True)
            os.remove(temp_wim_path)
        else:
            iso.get_file_from_iso(local_path=os.path.join(f"{usb_files_path}{path}", file), udf_path=full_path)

iso.close()
print("
WINscribe complete. USB filesystem created.
")
print("Next step: copy the *contents* of the 'usb_files' folder—not the folder itself—onto your USB drive.")
print("Use Finder or drag-and-drop. Format the USB as ExFAT or FAT32 first, if needed.")
print("Once copied, eject the drive safely.
")
print("Still here.\nStill building.\nHull Labs")
