# Background Subtractor

A script I made using Python and OpenCV.<br/>
The script take video stream and a background file as input. The video stream can be:
- the webcam
- a video file
- or a succession of multiple images

The script will extract moving objects from the video, and merge them with the background in real time.

## Requirements

- python3
- pip3
- virtualenv

## Setup

```bash
virtualenv -p python3 venv
source venv/bin/activate
```

## Run

Run ```./script.py``` without any arguments to display the usage

## Examples

### Run with webcam

```bash
./script.py background.jpg
```

### Run with images

```bash
./script.py --images images-data/248.png background.jpg
```

### Run with video file

```bash
./script.py --video Video_003.Avi background.jpg
```
