import argparse
import os
import subprocess
import sys

from shutil import which

# Checks if platform is macOS, if not raises an error
if sys.platform != 'darwin':
    print('ERROR: The following script runs only on macOS')
    sys.exit(1)

parser = argparse.ArgumentParser(description='IntelBluetoothFirmware de-chonker')
parser.add_argument('-v', '--verbose', action='store_true',help='Enable verbose')
args = parser.parse_args()

# Checks if the necessary tools are installed
if not os.path.exists('/Applications/Xcode.app/Contents/Developer') or not os.path.exists('/Library/Developer/CommandLineTools'):
    print('ERROR: Xcode does not appear to be installed. Please install it from App Store')
    sys.exit(1)

# If CLI tools are installed, git should be already installed. Probably gonna remove this if
if which('git') == None:
    print('ERROR: git does not appear to be installed. Please install it')
    sys.exit(1)

if not os.path.exists('IntelBluetoothFirmware'):
    subprocess.run(['git', 'clone', 'https://github.com/OpenIntelWireless/IntelBluetoothFirmware'], capture_output=not args.verbose)

os.chdir('IntelBluetoothFirmware')
if os.path.exists('IntelBluetoothFirmware/FwBinary.cpp'):
    print('Detected FwBinary.cpp. Removing it as it may contain old compressed firmwares...\n')
    subprocess.run(['rm','IntelBluetoothFirmware/FwBinary.cpp'], capture_output=not args.verbose)

if not os.path.exists('../Kexts'):
    print('Creating Kexts output folder...')
    subprocess.run(['mkdir', '../Kexts'], capture_output=not args.verbose)
else:
    print('Detected Kexts output folder. Removing it as it may contain old built kexts...\n')
    subprocess.run(['rm', '-r', '../Kexts'], capture_output=not args.verbose)

if not os.path.exists('MacKernelSDK'):
    print('WARNING: MacKernelSDK doesn\'t appear to be cloned. Cloning...\n')
    subprocess.run(['git', 'clone', 'https://github.com/acidanthera/MacKernelSDK.git'], capture_output=not args.verbose)


firmwares = [os.path.splitext(fw)[0] for fw in os.listdir('IntelBluetoothFirmware/fw') if not fw.endswith('.ddc')]

for firmware in firmwares:
    if os.path.exists('IntelBluetoothFirmware/FwBinary.cpp'):
        print('Detected FwBinary.cpp. Removing it as it may contain old compressed firmware...\n')
        subprocess.run(['rm','IntelBluetoothFirmware/FwBinary.cpp'], capture_output=not args.verbose)
    print(f'Building IntelBluetoothFirmware for {firmware}...\n')
    subprocess.run(['find', 'IntelBluetoothFirmware/fw', '-type', 'f', '-not', '-name', f'{firmware}.*', '-delete'], capture_output=not args.verbose)
    subprocess.run(['xcodebuild', '-project', 'IntelBluetoothFirmware.xcodeproj', '-target', 'IntelBluetoothFirmware', '-configuration', 'Release', '-sdk', 'macosx'], capture_output=not args.verbose)
    subprocess.run(['zip', '-r', f'build/Release/{firmware}.zip', '-D', 'build/Release/', '-x', 'build/Release/IntelBluetoothFirmware.kext.dSYM'], capture_output=not args.verbose)
    subprocess.run(['mv', f'build/Release/{firmware}.zip', '../Kexts'], capture_output=not args.verbose)
    subprocess.run(['git', 'reset', '--hard', 'HEAD'], capture_output=not args.verbose)
    subprocess.run(['rm', '-rf', 'build'], capture_output=not args.verbose)

