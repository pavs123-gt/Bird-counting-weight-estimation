
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

```bash
python3 -m venv venv
source venv/bin/activate
---
### Upgrade pip (Optional but Recommended)

```bash
pip install --upgrade pip
---


