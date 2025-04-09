# WINscribe

WINscribe

WINscribe is a command-line tool for macOS that creates bootable Windows USB installers.

Written in a weekend. Hopefully it saves yours.

This isn’t a product. It’s a precision tool.

Use it quietly.


🛠 Features

Parses and extracts Windows ISO images

Splits .wim files using wimlib-imagex (for FAT32 compatibility)

Builds a USB-compatible file system under usb_files/

Handles missing dependencies with clarity and care

No GUI. No nonsense. Terminal-native.


📋 Requirements

macOS with Terminal access

Python 3.8+

pycdlib → pip3 install pycdlib

wimlib-imagex → install via brew install wimlib


🚀 Usage

Interactive mode (default)

Just run:

python3 winscribe.py

It will:

List available .iso files in the current directory

Prompt you for which one to use

Create usb_files/ and extract the filesystem

Split large .wim files if needed

Optional Flags

--iso         Provide the path to your ISO up front  
--output      Set a custom output directory (default is ./usb_files)  
--quiet       Suppress feedback messages  
--version     Show version + exit

Example:

python3 winscribe.py --iso ./Win11.iso --output ./usb --quiet


📂 Final Step (Manual)

After the script runs, you’ll find all necessary files inside the usb_files/ folder.

To complete the process:

Format your USB drive as ExFAT or FAT32

Copy the contents of usb_files/ to the USB drive

Not the folder—just its contents

Eject safely

You now have a bootable Windows installer


🙏 Support

If this saved you time or your weekend, consider supporting via https://buymeacoffee.com/hulllabs

Still here.
Still building.
Hull-Labs

