from fastapi import APIRouter, Depends, HTTPException, status, Response
import schema, db, modal, utils
from sqlalchemy.orm import Session
from typing import List
from Auth import auth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

app= APIRouter(
    tags=['Users'],
    prefix='/user'
)


@app.post('/adduser')
def add_user(data:schema.AddUser,response:Response, db:Session= Depends(db.get_db)):
    checkUser= db.query(modal.Users).filter(modal.Users.phone_no== data.phone_no, modal.Users.role_id == data.role_id ).first()
    print("received data",data)
    if checkUser:
        print("filter in db", checkUser.__dict__)

        response.status_code=status.HTTP_409_CONFLICT
        return {
            "status_code":409,
            "response_status":"failed",
            "Response_data":"Already registered with this mobile number"
        }
    
    data.password= utils.encrypt(data.password)
    userData= modal.Users(**data.dict())
    db.add(userData)
    db.commit()

    return {
        "status_code":200,
        "response_status":"success",
        "Response_data":"Registered successfully"
        }

@app.post('/login/{id}')
def login(id:int,response:Response,data:OAuth2PasswordRequestForm= Depends(), db:Session= Depends(db.get_db)):
    checkUser= db.query(modal.Users).filter(modal.Users.phone_no == data.username, modal.Users.role_id== id).first()
    if not checkUser:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {
            "status_code":404,
            "response_status":"failed",
            "Response_data":"Invalid credentials"
        }
    
    if not utils.verify(data.password, checkUser.password):
        response.status_code=status.HTTP_403_FORBIDDEN
        return {
            "status_code":403,
            "response_status":"failed",
            "Response_data":"Incorrect password"
        }
    
    temp_data={'user_id':checkUser.user_id,"name":checkUser.name, 'role_id':checkUser.role_id}
    token= auth.Create_token(temp_data)
    return{"user_id":checkUser.user_id,"name":checkUser.name,"token_type":"bearer","access_token":token }

@app.get('/getuser')
def GetData(db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data = db.query(modal.Users).filter(modal.Users.user_id == current_user['user_id']).first()
    membership= db.query(modal.machanic_membership).filter(modal.machanic_membership.user_id == current_user['user_id']).first()
    if membership:
        data.membership_details= membership
    
    return {
        "status_code":200,
        "response_status":"success",
        "Response_data":data
        }

@app.put('/updateuser')
def UpdateUser(data:schema.EditUser, db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    query= db.query(modal.Users).filter(modal.Users.user_id == current_user['user_id'])

    if query.first():
        query.update(data.dict(), synchronize_session= False)
        db.commit()
        
        return {
            "status_code":200,
            "response_status":"success",
            "Response_data":"Data updated successfully"
        }

@app.delete('/deleteuser')
def DeleteUser(db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    query= db.query(modal.Users).filter(modal.Users.user_id == current_user['user_id'])

    if query.first():
        query.delete(synchronize_session= False)
        db.commit()
        
        return {
            "status_code":200,
            "response_status":"success",
            "Response_data":"User deleted successfully"
        }