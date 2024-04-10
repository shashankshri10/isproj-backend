from ..dependencies import verify_token
from fastapi import APIRouter, Depends, HTTPException,Path
from fastapi.responses import FileResponse
from typing import Annotated
from app.models.motor import MotorData
from ..services.motor_service import MotorService

router = APIRouter(
    prefix="/motor",
    tags=["motor"],
    responses={404: {"description": "Not found"}},
)
motor_service=MotorService()

# add motors
@router.post("/add-motor/")
async def create_asset(motor_data:MotorData,user_id:Annotated[str,Depends(verify_token)]):
    try:
        res_dict = await motor_service.create_motor(motor_data,user_id)
        if res_dict["status"]:
            return {"message": res_dict["message"]}
        else:
            raise HTTPException(status_code=401, detail=res_dict["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# get all details of all motors
@router.get("/all-motor-ids")
async def get_allmotor_ids(user_id:Annotated[str,Depends(verify_token)]):
    try:
        res_dict = await motor_service.all_motors_list()
        if res_dict["status"]:
            return {"message": res_dict["message"],"rows":res_dict["rows"]}
        else:
            raise HTTPException(status_code=401, detail=res_dict["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# get motor_data by motor_id
@router.get("/motor-data/{motor_id}")
async def get_motor_data_route(
    user_id:Annotated[str,Depends(verify_token)],
    motor_id: Annotated[int,Path(title="motor_id")]
):
    try:
        res_dict = await motor_service.motor_data(motor_id)
        if res_dict["status"]:
            return {"message": res_dict["message"],"rows":res_dict["rows"]}
        else:
            raise HTTPException(status_code=401, detail=res_dict["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# get report for a motor id
@router.get("/report/{motor_id}")
async def get_report(
    user_id: Annotated[str, Depends(verify_token)],
    motor_id: Annotated[int, Path(title="motor_id")]
):
    try:
        res_dict = await motor_service.motor_report(motor_id=motor_id)
        if res_dict["status"]:
            file_path = res_dict["file_path"]
            return FileResponse(file_path, media_type='application/pdf')
        else:
            raise HTTPException(status_code=401, detail=res_dict["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))