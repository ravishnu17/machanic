from fastapi import APIRouter, Depends, HTTPException, status
import schema, db, modal, utils
from sqlalchemy.orm import Session
from typing import List
from Auth import auth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

app= APIRouter(
    tags=['Users'],
    prefix='/user'
)

@app.post('/addrole')
def add_role(data:List[schema.Role], db:Session=Depends(db.get_db)):
    roleData= []
    for role in data:
        temp= modal.Role(**role.dict())
        roleData.append(temp)
    db.add_all(roleData)
    db.commit()
    return {"detail":"Data added successfully"}

@app.post('/adduser')
def add_user(data:schema.AddUser, db:Session= Depends(db.get_db)):
    checkUser= db.query(modal.Users).filter(modal.Users.phone_no== data.phone_no, modal.Users.role_id == data.role_id ).first()

    if checkUser:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already registered with this mobile number")
    
    data.password= utils.encrypt(data.password)
    userData= modal.Users(**data.dict())
    db.add(userData)
    db.commit()

    return {"detail":"Registered successfully"}

@app.post('/login')
def login(data:OAuth2PasswordRequestForm= Depends(), db:Session= Depends(db.get_db)):
    checkUser= db.query(modal.Users).filter(modal.Users.phone_no == data.username).first()
    if not checkUser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not utils.verify(data.password, checkUser.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
    
    temp_data={'user_id':checkUser.user_id,"name":checkUser.name}

    token= auth.Create_token(temp_data)

    return {"token_type":"bearer","access_token":token}

@app.get('/verifyuser')
def GetData( current_user= Depends(auth.verify_token)):
    return current_user

