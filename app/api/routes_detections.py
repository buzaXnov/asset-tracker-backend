from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_db
from app.models.Detection import Detection
from app.models.DetectionAnswer import DetectionAnswer
from app.schemas.detection import DetectionAnswerOut, DetectionOut

router = APIRouter(prefix="/media", tags=["Media"])


@router.get("/{media_id}/detections", response_model=list[DetectionOut])
async def get_detections_for_media(media_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Detection).where(Detection.media_id == media_id))
    detections = result.scalars().all()

    if not detections:
        raise HTTPException(
            status_code=404, detail="No detections found for this media."
        )

    detection_out = []
    for d in detections:
        answers_result = await db.execute(
            select(DetectionAnswer).where(DetectionAnswer.detection_id == d.id)
        )
        answers = answers_result.scalars().all()
        detection_out.append(
            DetectionOut(
                id=d.id,
                bbox=[d.x1, d.y1, d.x2, d.y2],
                coordinate_top=[d.coord_top_lat, d.coord_top_lng],
                coordinate_bottom=[d.coord_bot_lat, d.coord_bot_lng],
                answers=[
                    DetectionAnswerOut(answer_text=a.answer_text) for a in answers
                ],
            )
        )

    return detection_out
