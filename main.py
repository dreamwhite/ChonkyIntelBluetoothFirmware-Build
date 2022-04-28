import os

os.chdir('IntelBluetoothFirmware')
os.system('rm IntelBluetoothFirmware/FwBinary.cpp')
firmwares = [fw[:-4] for fw in os.listdir('IntelBluetoothFirmware/fw') if not fw.endswith('.ddc')]

os.system('mkdir ../Kexts')
for firmware in firmwares:
    os.system(f'find IntelBluetoothFirmware/fw -type f -not -name "{firmware}.*" -delete')
    os.system('xcodebuild -project IntelBluetoothFirmware.xcodeproj -target fw_gen -configuration Release -sdk macosx')
    os.system('xcodebuild -project IntelBluetoothFirmware.xcodeproj -target IntelBluetoothFirmware -configuration Release -sdk macosx')
    os.system(f'zip -r build/Release/{firmware}.zip build/Release/*.kext')
    os.system(f'mv build/Release/{firmware}.zip ../Kexts')
    os.system('git reset --hard HEAD')
    os.system('rm -rf build')

