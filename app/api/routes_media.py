import mimetypes
import shutil
import uuid
from pathlib import Path

import cv2
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.detect import detect
from app.db.database import get_db
from app.models.AssetDefinition import AssetDefinition
from app.models.Detection import Detection
from app.models.DetectionAnswer import DetectionAnswer
from app.models.Media import Media
from app.schemas.media import MediaOut

router = APIRouter(prefix="/media", tags=["Media"])

MEDIA_DIR = Path("media")
MEDIA_DIR.mkdir(exist_ok=True)

FRAME_DIR = MEDIA_DIR / "frames"
FRAME_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model=MediaOut)
async def upload_media(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    ext = Path(file.filename).suffix.lower()
    filename = f"{uuid.uuid4()}{ext}"
    file_path = MEDIA_DIR / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save media entry
    media = Media(filename=filename, user_id=1)
    db.add(media)
    await db.commit()
    await db.refresh(media)

    # Load user's asset definitions
    result = await db.execute(
        select(AssetDefinition).where(AssetDefinition.user_id == 1)
    )
    asset_defs = result.scalars().all()

    if not asset_defs:
        raise HTTPException(
            status_code=400, detail="No asset definitions found for user."
        )

    # Helper: run detect + save detections
    async def process_image(path: Path):
        with open(path, "rb") as f:
            image_bytes = f.read()

        detections = detect(image_bytes, asset_defs, metadata={"filename": path.name})
        for det in detections:
            d = Detection(
                asset_definition_id=asset_defs[0].id,
                media_id=media.id,
                x1=det["bbox"][0],
                y1=det["bbox"][1],
                x2=det["bbox"][2],
                y2=det["bbox"][3],
                coord_top_lat=det["coordinate_top"][0],
                coord_top_lng=det["coordinate_top"][1],
                coord_bot_lat=det["coordinate_bottom"][0],
                coord_bot_lng=det["coordinate_bottom"][1],
            )
            db.add(d)
            await db.flush()  # Needed to get d.id

            for answer_text in det["answers"]:
                db.add(DetectionAnswer(detection_id=d.id, answer_text=answer_text))

    # Check file type
    mime_type, _ = mimetypes.guess_type(file.filename)
    is_video = mime_type and mime_type.startswith("video")

    if is_video:
        video_capture = cv2.VideoCapture(str(file_path))
        if not video_capture.isOpened():
            raise HTTPException(status_code=400, detail="Could not open video file.")

        frame_index = 0
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            if frame_index % 30 == 0:
                frame_filename = f"{uuid.uuid4()}.jpg"
                frame_path = FRAME_DIR / frame_filename
                cv2.imwrite(str(frame_path), frame)
                await process_image(frame_path)
            frame_index += 1

        video_capture.release()
    else:
        await process_image(file_path)

    await db.commit()
    return media
