
# 🐔 Bird Counting and Weight Estimation from CCTV Video

A complete computer vision pipeline for **poultry bird counting and video-based weight estimation** using fixed-camera CCTV footage.  
The system takes a poultry CCTV video as input, detects and tracks birds over time, estimates bird counts, computes a **relative weight proxy**, and generates annotated video outputs.  
A **FastAPI service** is provided for easy video analysis through an API.

---

## ✅ Table of Contents

- [Setup & Installation](#setup--installation)
- [Project Structure](#project-structure)
- [Features](#features)
- [Running the System](#running-the-system)
- [API Usage](#api-usage)
- [Outputs](#outputs)
- [Weight Estimation Notes](#weight-estimation-notes)
- [Tools Used](#tools-used)
- [Author](#author)

---

##  Setup & Installation

### Prerequisites
- Linux OS
- Python 3.8 or higher
- pip package manager

### Create and Activate Virtual Environment
Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```
### Upgrade pip 
```bash
pip install --upgrade pip
```

### Install project dependencies
```bash
pip install -r requirements.txt

```
---
##  project structure

Bird_Counting_and_Weight_Estimation/
│
├── main.py
│   └── FastAPI application
│       - /health endpoint
│       - /analyze_video endpoint
│       - YOLO detection + tracking
│       - Bird counting & weight index logic
│
├── results/
│   ├── annotated_<video_id>.avi
│   │   └── Annotated output video
│   │       (bounding boxes, tracking IDs, count overlay)
│   │
│   ├── results_<video_id>.json
│   │   └── API output JSON
│   │       - counts over time
│   │       - sample tracks
│   │       - weight proxy/index
│   │
│   └── temp_<video_id>.mp4
│       └── Temporary uploaded video (auto-deleted)
│
├── models/
│   └── yolov8n.pt
│       └── Pretrained YOLOv8 model (COCO)
│
├── requirements.txt
│   └── Python dependencies
│       (fastapi, uvicorn, ultralytics, opencv-python, etc.)
│
│
└── sample_videos/   
    └── input_sample.mp4
        └── Provided CCTV video for testing

---
