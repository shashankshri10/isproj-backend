import bcrypt
from datetime import datetime, timedelta
from app.models.user import User
from app.models.login_user import LoginUser
from app.db import connect_to_pg,close_pg_connection
from jose import jwt
import os
import random
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

class UserService:
    # Function to insert the user
    async def create_user(self, user: User) -> dict:
        if len(user.password) < 8:
            return {"status": False, "message":"Password is less than 8 characters"}
        hashed_password = await self.hash_password(user.password)
        user_data = user.model_dump()
        user_data['password'] = hashed_password
        user_data['timestamp']=datetime.now()
        user_id = random.randint(1, 1000)
        conn = await connect_to_pg()
        
        try:
            await conn.execute('''INSERT INTO users (timestamp, user_name, password, user_type, designation, email_id,user_id) VALUES ($1, $2, $3, $4, $5, $6, $7)''',
                           user_data['timestamp'], user_data['user_name'], user_data['password'], user_data['user_type'], user_data['designation'], user_data['email_id'], user_id)
            
            return {"status":True,"message":f"User created"}
        except Exception as e:
            return {"status":False,"message":f"{e}"}
        finally:
            await close_pg_connection(conn)
        

    async def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    # Login function

    async def authenticate_user(self, login_user: LoginUser) -> dict:
        conn = await connect_to_pg()
        try:
            user_data = await conn.fetchrow('''SELECT * FROM users WHERE email_id = $1''', login_user.email_id)
            
            if not user_data:
                return {"status": False, "message": "User not found"}
            
            hashed_password = user_data.get('password')
            if not await self.verify_password(login_user.password, hashed_password):
                return {"status": False, "message": "Incorrect password"}
            
            # Check secret key only for admin users
            if login_user.user_type == "admin":
                if login_user.secret_key != "gail@123":
                    return {"status": False, "message": "Incorrect secret key"}

            # Generate JWT token
            token = self.generate_jwt_token(str(user_data['user_id']))

            return {"status": True, "message": "Login successful", "token": token, "user_id": str(user_data["user_id"])}
        
        except Exception as e:
            return {"status": False, "message": str(e)}
        finally:
            await close_pg_connection(conn)

    async def find_user_by_email(self, email_id: str):
        conn = await connect_to_pg()
        try:
            user_data = await conn.fetchrow('''SELECT * FROM users WHERE email_id = $1''', email_id)
            return user_data
        except Exception as e:
            return None
        finally:
            await close_pg_connection(conn)


    def generate_jwt_token(self, user_id: str) -> str:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        # Replace 'your_secret_key' with your actual secret key
        return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))