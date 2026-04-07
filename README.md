# FileTrack

A Home Assistant custom component that monitors folders and exposes their total size as a sensor, along with file count and a `fileList` attribute. It is perfectly designed as a companion for the [Camera Gallery Card](https://github.com/TheScubadiver/camera-gallery-card), but can also be used as a standalone integration.

## Installation

### HACS (Recommended)
1. Add this repository as a custom repository in HACS.
2. Download **FileTrack** via HACS.
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration → FileTrack**. The setup completes instantly, no initial configuration needed.

---

## Usage & Configuration

How to make a sensor:

### Method 1 — Camera Gallery Card
Sensors are created directly from the **Camera Gallery Card editor** — no YAML, service calls, or manual setup required.

### Method 3 — YAML
Add sensors directly to your `configuration.yaml` file:

```yaml
sensor:
  - platform: filetrack
    name: Recordings
    folder: /media/frigate/clips
    sort: date
    recursive: false
```
*Note: Restart Home Assistant after adding YAML entries.*

---

## Configuration Options

| Option | Required | Default | Description |
| :--- | :---: | :---: | :--- |
| `name` | Yes | — | Sensor name |
| `folder` | Yes | — | Path to monitor |
| `sort` | No | `date` | `date`, `name`, or `size` |
| `recursive` | No | `false` | Include subdirectories (`true` or `false`) |

---

## Sensor Attributes

| Attribute | Description |
| :--- | :--- |
| `path` | Monitored folder path |
| `number_of_files` | File count |
| `fileList` | List of matched file paths |
| `sort` | Active sort order |

---

## Removing Sensors

* **UI/Service Sensors:** Go to **Settings → Devices & Services → FileTrack → Configure** to select and remove sensors added via the UI.
* **YAML Sensors:** Remove the relevant entries from your `configuration.yaml` file and restart Home Assistant.
