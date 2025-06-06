from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_db
from app.models.AssetDefinition import AssetDefinition
from app.models.AssetQuestion import AssetQuestion
from app.models.Detection import Detection
from app.models.DetectionAnswer import DetectionAnswer
from app.models.User import User
from app.schemas.asset import AssetDefinitionCreate, AssetWithDetectionsOut
from app.schemas.detection import DetectionAnswerOut, DetectionOut

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("/users/")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.post("/")
async def create_asset_definition(
    asset_data: AssetDefinitionCreate, db: AsyncSession = Depends(get_db)
):
    asset = AssetDefinition(label=asset_data.label, user_id=1)

    db.add(asset)
    await db.flush()  # Get asset.id before inserting questions

    for q in asset_data.questions:
        question = AssetQuestion(
            asset_definition_id=asset.id, question_text=q.question_text
        )
        db.add(question)

    await db.commit()
    return {"id": asset.id, "label": asset.label}


@router.get("/map-view", response_model=list[AssetWithDetectionsOut])
async def get_asset_map_view(db: AsyncSession = Depends(get_db)):
    # For now, hardcoded user_id = 1
    result = await db.execute(
        select(AssetDefinition).where(AssetDefinition.user_id == 1)
    )
    assets = result.scalars().all()

    output = []
    for asset in assets:
        detections_result = await db.execute(
            select(Detection).where(Detection.asset_definition_id == asset.id)
        )
        detections = detections_result.scalars().all()

        detection_out_list = []
        for d in detections:
            answers_result = await db.execute(
                select(DetectionAnswer).where(DetectionAnswer.detection_id == d.id)
            )
            answers = answers_result.scalars().all()
            detection_out_list.append(
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

        output.append(
            AssetWithDetectionsOut(
                id=asset.id, label=asset.label, detections=detection_out_list
            )
        )

    return output
