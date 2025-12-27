import cv2
import json
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Query
from ultralytics import YOLO

# -------------------- APP --------------------
app = FastAPI()

# -------------------- MODEL --------------------
MODEL = YOLO("yolov8n.pt")  # COCO pretrained

# -------------------- OUTPUT DIR --------------------
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/health")
def health():
    return {"status": "OK"}


@app.post("/analyze_video")
async def analyze_video(
    file: UploadFile = File(...),

    # REQUIRED OPTIONAL PARAMETERS
    fps_sample: int = Query(
        1,
        description="Process every Nth frame (1 = all frames)"
    ),
    conf_thresh: float = Query(
        0.05,
        description="YOLO confidence threshold"
    ),
    iou_thresh: float = Query(
        0.7,
        description="YOLO IoU threshold"
    ),
):
    # -------------------- PATHS --------------------
    video_id = uuid.uuid4().hex
    temp_video = OUTPUT_DIR / f"temp_{video_id}.mp4"
    annotated_video = OUTPUT_DIR / f"annotated_{video_id}.avi"
    json_path = OUTPUT_DIR / f"results_{video_id}.json"

    # -------------------- SAVE INPUT VIDEO --------------------
    with open(temp_video, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    cap = cv2.VideoCapture(str(temp_video))

    # -------------------- VIDEO WRITER (AVI FIX) --------------------
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps == 0:
        fps = 25

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter(
        str(annotated_video),
        fourcc,
        fps,
        (width, height)
    )

    if not writer.isOpened():
        raise RuntimeError(" VideoWriter failed to open")

    # -------------------- DATA CONTAINERS --------------------
    frame_id = 0
    counts = []
    tracks_sample = {}
    weight_data = []

    # -------------------- MAIN LOOP --------------------
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # FPS sampling
        if frame_id % fps_sample != 0:
            frame_id += 1
            continue

        # -------------------- YOLO DETECTION + TRACKING --------------------
        results = MODEL.track(
            frame,
            persist=True,
            conf=conf_thresh,
            iou=iou_thresh,
            imgsz=1280,
            tracker="bytetrack.yaml",
            verbose=False
        )[0]

        annotated = frame.copy()
        active_ids = set()

        #  IMPORTANT: DRAW BOXES EVEN IF IDS ARE MISSING
        if results.boxes is not None:
            boxes = results.boxes.xyxy.cpu().numpy()

            if results.boxes.id is not None:
                ids = results.boxes.id.cpu().numpy()
            else:
                ids = [-1] * len(boxes)

            confs = results.boxes.conf.cpu().numpy()

            for box, tid, conf in zip(boxes, ids, confs):
                x1, y1, x2, y2 = map(int, box)

                area = (x2 - x1) * (y2 - y1)
                weight_index = round(area / 1000, 2)

                tid = int(tid)
                active_ids.add(tid)

                # Draw bounding box
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)

                cv2.putText(
                    annotated,
                    f"ID:{tid} W:{weight_index}",
                    (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

                # Sample track examples
                if tid not in tracks_sample and len(tracks_sample) < 5:
                    tracks_sample[tid] = {
                        "bbox": [x1, y1, x2, y2],
                        "confidence": float(conf)
                    }

                weight_data.append({
                    "id": tid,
                    "frame": frame_id,
                    "weight_index": weight_index
                })

        # -------------------- COUNT --------------------
        count = len(active_ids)
        counts.append({
            "timestamp": round(frame_id / fps, 2),
            "count": count
        })

        cv2.putText(
            annotated,
            f"Total Birds: {count}",
            (40, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            3
        )

        writer.write(annotated)
        frame_id += 1

    # -------------------- CLEANUP --------------------
    cap.release()
    writer.release()
    temp_video.unlink()

    # -------------------- FINAL JSON --------------------
    with open(json_path, "w") as f:
        json.dump(
            {
                "counts": counts,
                "tracks_sample": tracks_sample,
                "weight_estimates": {
                    "unit": "index",
                    "method": "bounding_box_area_proxy",
                    "data": weight_data
                }
            },
            f,
            indent=2
        )

    # -------------------- API RESPONSE --------------------
    return {
        "counts": counts,
        "tracks_sample": tracks_sample,
        "weight_estimates": {
            "unit": "index",
            "method": "bounding_box_area_proxy",
            "note": "Convert to grams using calibration"
        },
        "artifacts": {
            "annotated_video": annotated_video.name,
            "json": json_path.name
        }
    }
