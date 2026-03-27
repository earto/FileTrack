# FileTrack

Custom Component for Home Assistant that monitors a folder and creates a sensor listing its files.

This component is a fork of the original [Files](https://github.com/TarheelGrad1998/files) integration, which has been archived by its creator. FileTrack has been adapted and maintained specifically for use with the [Camera Gallery Card](https://github.com/TheScubadiver/camera-gallery-card), allowing users to easily display and manage media files from Home Assistant.

## Installation
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Files must be placed in the `www` folder inside your Home Assistant configuration, ideally in a dedicated subfolder for better organization. FileTrack will periodically scan this folder for changes and update the sensor accordingly. It is based on the built-in Folder component.

You can install **FileTrack** via **HACS** (use the *Custom Repository* option), or install manually by following these steps:

1. **Create the custom components folder**  
   In your Home Assistant `config` directory (where `configuration.yaml` lives), create a folder named `custom_components`.

2. **Create the FileTrack folder**  
   Inside `custom_components`, create a folder named `filetrack`.

3. **Copy the component files**  
   Copy the following three files into the `filetrack` folder:  
   - `_init_.py`  
   - `manifest.json`  
   - `sensor.py`

4. **Restart Home Assistant**  
   This will load the new component.

5. **Create your media folder**  
   Inside the `www` folder, create a subfolder (for example, `images`) and place your media files there.

6. **Add the sensor to your configuration**  
   In your `configuration.yaml`, add:

   ```yaml
   - sensor:
       - platform: filetrack
         folder: /config/www/images
         filter: '**/*.jpg'
         name: gallery_images
         sort: date
         recursive: false
8. Restart Home Assistant
9. Check the sensor.gallery_images entity to see if the `fileList` attribute lists your files

### Configuration Variables

| Name | Type | Default | Description
| ---- | ---- | ------- | -----------
| platform | string | **Required** | `files`
| folder | string | **Required** | Folder to scan, must be /config/www/***
| name | string | **Required** | The entity ID for the sensor
| sort | string | **Optional** | One of 'name', 'date', or 'size';  Determines how files are sorted in the Gallery, `Default: date`
| recursive | boolean | **Optional** | True or False; If True, the pattern filter `**` will match any files and zero or more directories, subdirectories and symbolic links to directories. **Note:** Using the `**` pattern in large directory trees may consume an inordinate amount of time , `Default: False`  
