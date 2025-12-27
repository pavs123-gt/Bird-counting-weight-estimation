
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


```


Bird_Counting_and_Weight_Estimation/
│
├── main.py
│   └── FastAPI application with detection, tracking, counting, and weight logic
│
├── results/
│   ├── annotated_<video_id>.avi
│   ├── results_<video_id>.json
│   └── temp_<video_id>.mp4
│
├── models/
│   └── yolov8n.pt
│
├── requirements.txt
│
└── sample_videos/
    └── input_sample.mp4





```
---
## Features

- Bird detection and tracking using YOLOv8 with ByteTrack 
- Accurate bird counting over time with timestamp-based counts
- Weight estimation using bounding-box area as a proxy
- Annotated output video with bounding boxes, tracking IDs, and total count overlay
- FastAPI-based API with configurable parameters (fps_sample, conf_thresh, iou_thresh)
---

## Running the System

Follow the steps below to run the Bird Counting and Weight Estimation system locally.

### 1. Activate Virtual Environment (Optional but Recommended)

Activate the Python virtual environment before running the application.

```bash
source venv/bin/activate
```



### 2. Start the FastAPI Server

Run the FastAPI application using Uvicorn.

```bash
uvicorn app:app --reload
```

If the server starts successfully, you will see output similar to:

```text
Uvicorn running on http://127.0.0.1:8000
```



### 3. Verify Service Health

Check whether the API is running correctly using the health endpoint.

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "OK"
}
```



### 4. Analyze a Video

Send a POST request to the `/analyze_video` endpoint with a poultry CCTV video file.

Basic example:

```bash
curl -X POST http://127.0.0.1:8000/analyze_video \
-F "file=@sample_video.mp4"
```

Example with optional parameters:

```bash
curl -X POST "http://127.0.0.1:8000/analyze_video?fps_sample=2&conf_thresh=0.1&iou_thresh=0.7" \
-F "file=@sample_video.mp4"
```


### 5. Output Generation

After processing is completed, the system automatically generates the following outputs:

- An annotated output video with bounding boxes, tracking IDs, and bird count overlay  
- A JSON file containing bird counts over time, sample tracking data, and weight estimation values  




### 6. Implementation Details

- Bird detection is performed using **YOLOv8**  
- Tracking is handled using **ByteTrack** with persistent tracking IDs  
- Bird count is calculated based on active tracking IDs per frame  
- Weight estimation is provided as a **relative index** derived from bounding box area  
- FPS sampling can be adjusted to balance accuracy and processing speed

---
## API Usage

The system exposes a minimal FastAPI service to analyze poultry CCTV videos for bird counting and weight estimation.

---

### Base URL

```
http://127.0.0.1:8000
```

---

### 1. Health Check Endpoint

Used to verify whether the API service is running.

**Endpoint**
```
GET /health
```

**Example Request**
```bash
curl http://127.0.0.1:8000/health
```

**Example Response**
```json
{
  "status": "OK"
}
```

---

### 2. Analyze Video Endpoint

Processes a poultry CCTV video and returns bird counts over time, tracking samples, weight estimation data, and generated artifacts.

**Endpoint**
```
POST /analyze_video
```

**Request Type**
```
multipart/form-data
```

**Required Parameter**
- `file` : Input poultry CCTV video file

**Optional Query Parameters**
- `fps_sample` (int): Process every Nth frame (default = 1)
- `conf_thresh` (float): Detection confidence threshold (default = 0.05)
- `iou_thresh` (float): IoU threshold for tracking (default = 0.7)

---

**Basic Example**
```bash
curl -X POST http://127.0.0.1:8000/analyze_video \
-F "file=@sample_video.mp4"
```

---

**Example with Optional Parameters**
```bash
curl -X POST "http://127.0.0.1:8000/analyze_video?fps_sample=2&conf_thresh=0.1&iou_thresh=0.7" \
-F "file=@sample_video.mp4"
```

---

### Response Structure

The API returns a JSON response containing the following fields:

- `counts`: Time series of bird counts (timestamp → count)
- `tracks_sample`: Sample tracking IDs with representative bounding boxes
- `weight_estimates`: Relative weight index per bird with method details
- `artifacts`: Names of generated output files (annotated video and JSON)




---

### Output Files

All generated artifacts are automatically saved in the `outputs/` directory after video processing is completed.

---
## Outputs

After processing a poultry CCTV video using the system, the following outputs are generated in the `outputs/` directory:

---

### 1. Annotated Video

- Filename: `annotated_<unique_id>.avi`  
- Description: The input video with bounding boxes drawn around detected birds, tracking IDs displayed, and total bird count overlaid on each frame.  
- Purpose: Provides visual confirmation of detection, tracking, and counting performance.

---

### 2. JSON Response File

- Filename: `results_<unique_id>.json`  
- Description: Contains structured data representing bird counts, sample tracking information, and weight estimation for each bird detected.  
- Purpose: Provides machine-readable output suitable for further analysis or integration with other systems.

**Sample JSON Content**

```json
{
  "counts": [
    {
      "timestamp": 0.0,
      "count": 12
    },
    {
      "timestamp": 1.0,
      "count": 14
    }
  ],
  "tracks_sample": {
    "3": {
      "bbox": [120, 85, 260, 210],
      "confidence": 0.87
    },
    "5": {
      "bbox": [300, 120, 380, 250],
      "confidence": 0.92
    }
  },
  "weight_estimates": {
    "unit": "index",
    "method": "bounding_box_area_proxy",
    "data": [
      {
        "id": 3,
        "frame": 0,
        "weight_index": 34.5
      },
      {
        "id": 5,
        "frame": 0,
        "weight_index": 28.7
      }
    ]
  },
  "artifacts": {
    "annotated_video": "annotated_<unique_id>.avi",
    "json": "results_<unique_id>.json"
  }
}
```

---

### Notes on Outputs

- Only one annotated demo video is required for submission.  
- JSON provides **all counts, tracking IDs, and weight proxies** in a structured format.  
- These outputs together demonstrate the **full end-to-end functionality** of detection, tracking, counting, and weight estimation.  
- All files are saved in the `outputs/` folder automatically after the `/analyze_video` API is called.

---
## Weight Estimation Notes

The weight estimation in this project is implemented as a **relative weight index**, derived from the **area of the bounding boxes** detected around each bird.

- **Methodology**:
  - For each detected bird, the bounding box area is calculated: `(width × height)`.
  - The area is normalized or scaled to produce a **weight index**.
  - This index is stored per frame in the JSON output.

- **Assumptions**:
  - Camera angle and height are fixed.
  - Birds are roughly uniform in shape.
  - True weight in grams is **not provided** in the dataset.

- **Conversion to grams**:
  - Requires **camera calibration** and a set of known bird weights.
  - A linear or regression-based mapping can convert the relative index to actual grams.

- **Usage**:
  - Provides a **proxy for weight trends over time**.
  - Useful for monitoring flock growth or detecting abnormalities in bird size distribution.

---
## Tools Used

The following tools and libraries were used to implement the Bird Counting and Weight Estimation system:

- **Python 3.10+** – Primary programming language for the project.
- **FastAPI** – To create the REST API for video analysis.
- **Uvicorn** – ASGI server to run the FastAPI application.
- **Ultralytics YOLOv8** – Pretrained object detection model for bird detection.
- **ByteTrack** – Tracking algorithm to assign stable IDs to detected birds.
- **OpenCV (cv2)** – Video reading, writing, and annotation.
- **NumPy** – Numerical computations and array operations.
- **Pathlib** – File and folder path management.
- **UUID** – Unique identifiers for temporary files and outputs.
- **JSON** – Structured output serialization for counts, tracks, and weight estimates.
---
## Author

**Pavani Linguberi**  

- Role: Candidate – Machine Learning / AI Engineer Internship  
- Email: [linguberipavani3@gmail.com]  
- GitHub: [https://github.com/your-username](https://github.com/pavs123-gt)  

