# ChonkyIntelBluetoothFirmware

The following guide will help you light that chonk `IntelBluetoothFirmware.kext`

## Requirements

- [XCode](https://developer.apple.com/xcode/)
- [IORegistryExplorer](https://github.com/utopia-team/IORegistryExplorer)
- [MacKernelSDK](https://github.com/acidanthera/MacKernelSDK)
- [IntelBluetoothFirmware](https://github.com/OpenIntelWireless/IntelBluetoothFirmware)

## How to proceed

After making sure that IntelBluetoothFirmware stock kext works without any additional edit you can light the firmware from ~ 7.2MB to less than 1MB :)


### Identify your firmware version

Open IORegistryExplorer and locate your BT device. You should have something like this:

![](/.assets/images/ioreg.png)

In my case, the firmware version is `ibt-17-16-1.sfi`

### Slim that fat boi IntelBluetoothFirmware

1. Clone IntelBluetoothFirmware and open the source project
2. Remove `FwBinary.cpp` from `$(source)/IntelBluetoothFirmware/IntelBluetoothFirmware` as it contains already compressed firmware files
3. Remove every firmware file in `$(source)/IntelBluetoothFirmware/IntelBluetoothFirmware/fw` except the one which name starts with the previously identified firmware name (e.g. in my case `ibt-17-16-1.sfi` and `ibt-17-16-1.ddc`)

![](/.assets/images/firmware.png)

4. Clone MacKernelSDK onto `$(source)` with `git clone https://github.com/acidanthera/MacKernelSDK.git`.
5. Open XCode and build the project with `Release` configuration using `⇧⌘R` and after it finishes building the project, replace the old `IntelBluetoothFirmware.kext` with the newly generated

# How to generate every single firmware

Run `python3 main.py` and see the magic happen.
Created kexts will be in `Kexts` folder

# Credits

- [Apple](https://apple.com) for [XCode](https://developer.apple.com/xcode/) and [IORegistryExplorer](https://github.com/utopia-team/IORegistryExplorer)
- [OpenIntelWireless](https://github.com/OpenIntelWireless) for [IntelBluetoothFirmware](https://github.com/OpenIntelWireless/IntelBluetoothFirmware)
- [Acidanthera](https://github.com/acidanthera) for [MacKernelSDK](https://github.com/acidanthera/MacKernelSDK)
