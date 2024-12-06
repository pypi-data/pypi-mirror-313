# Tactigon Speech

![The tactigon team](https://avatars.githubusercontent.com/u/63020285?s=200&v=4)

This package add voice command functionalities to the Tactigon Skin using Bluetooth Low Energy. It is based on the Tactigon Gear.

## Architecture

Tactigon Speech is a class that inherits from the base TSkin class, which can be found in the [Tactigon Gear](https://pypi.org/project/tactigon-gear/).

Here's the definition of the architecture.

![Tactigon Speech architecture definition](https://www.thetactigon.com/wp/wp-content/uploads/2023/11/Architecture_Tactigon_Speech.png "Tactigon Speech architecture definition")

## Prerequisites
In order to use the Tactigon Gear the following prerequisites needs to be observed:

Tactigon Gear: >=5.0.3

Platforms:
 - Windows 10 (x86-64 CPU with AVX/FMA)
 - macOS >=12.0 (x86-64 CPU with AVX/FMA)

Python version: following versions has been used and tested. It is STRONGLY recommended to use these ones depending on platform.
   - Win10: 3.8.10
   - macOS: 3.8.10

It is recommended to create a dedicated python virtual environment and install the packages into the virtual environment:  
  * `python -m venv venv`
  * `pip install tactigon-speech`

Depending on your installation (Mac users) you may need to use `python3` and `pip3` instead of `python` and `pip` respectively

## Tactigon Gear complete reference
A complete reference to Tactigon Gear and the Tactigon Skin can be found at [Tactigon Gear](https://pypi.org/project/tactigon-gear/)

## Tactigon Speech examples
For a list of example you can go to [Tactigon SDK repository](https://github.com/TactigonTeam/Tactigon-SDK)