from datetime import datetime, timedelta
from app.models.motor import MotorData
# from app.models.login_user import LoginUser
from app.db import connect_to_pg,close_pg_connection
from ..utils.pdfgen import create_pdf_with_plots
# from jose import jwt
import os
import random

class MotorService:
    async def create_motor(self, motor_data:MotorData, user_id: int) -> dict:
        try:
            conn = await connect_to_pg()
            asset_data = motor_data.model_dump()
            asset_data['user_id'] = user_id
            asset_data['timestamp'] = datetime.now()
            query = '''
                INSERT INTO motor_details (timestamp, user_id, motor_id, power_rating, location)
                VALUES ($1, $2, $3, $4, $5)
            '''
            await conn.execute(query, asset_data['timestamp'], asset_data['user_id'], asset_data['motor_id'], asset_data['power_rating'], asset_data['location'])
            await close_pg_connection(conn)
            return {"status": True, "message": "Motor created successfully"}
        except Exception as e:
            return {"status": False, "message": str(e)}
        
    async def all_motors_list(self) -> dict:
        try:
            conn = await connect_to_pg()
            query='''SELECT * FROM motor_details;'''
            rows = await conn.fetch(query)
            await close_pg_connection(conn)
            return {"status": True, "message": "motor_ids fetched","rows":rows}
        except Exception as e:
            return {"status": False, "message": str(e)}
        
    async def motor_data(self,motor_id:int)-> dict:
        try:
            conn = await connect_to_pg()
            query='''SELECT * FROM motor_data WHERE motor_id = $1 ORDER BY timestamp DESC LIMIT 10;'''
            rows = await conn.fetch(query,motor_id)
            await close_pg_connection(conn)
            return {"status": True, "message": "motor_ids fetched","rows":rows}
        except Exception as e:
            return {"status": False, "message": str(e)}
    
    async def motor_report(self,motor_id:int) -> dict:
        try:
            conn = await connect_to_pg()
            query='''SELECT * FROM motor_data WHERE motor_id = $1 ORDER BY timestamp DESC LIMIT 10;'''
            rows = await conn.fetch(query,motor_id)
            motor_details= await conn.fetchrow('''SELECT motor_id, power_rating, location FROM motor_details WHERE motor_id=$1''', motor_id)
            timestamps = [obj["timestamp"] for obj in rows]
            current_values = [round(obj["current_value"], 2) for obj in rows]
            freq_values = [round(obj["frequency"], 2) for obj in rows]

            # code to handle pdf generation
            # Get the absolute path to the "reports" folder
            reports_folder = os.path.join(os.path.dirname(__file__), '..','..', 'reports')
            os.makedirs(reports_folder, exist_ok=True)  # Create the "reports" folder if it doesn't exist

            file_name = os.path.join(reports_folder, f"output-{motor_id}.pdf")
            create_pdf_with_plots(file_name, "Healthy", 0.82, timestamps, current_values, freq_values, motor_details=motor_details)

            return {"status": True, "message": "PDF report generated", "file_path": file_name}
        except Exception as e:
            return {"status": False, "message": str(e)}