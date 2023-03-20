from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
import db, modal, schema
from Auth import auth
from typing import List

app = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


#roles

@app.post('/addrole')
def add_role(data:List[schema.Role], db:Session=Depends(db.get_db), current_user=  Depends(auth.verify_token)):
    roleData= []
    for role in data:
        temp= modal.Role(**role.dict())
        roleData.append(temp)
    db.add_all(roleData)
    db.commit()
    return {
        "status_code":200,
        "response_status":"success",
        "Response_data":"Roles are added successfully"
        }

@app.get('/viewroles')
def viewRoles(db:Session= Depends(db.get_db), current_user=  Depends(auth.verify_token)):
    data= db.query(modal.Role).all()
    return {
        "status_code":200,
        "response_status":"success",
        "Response_data":data
        }

#users

@app.get('/getalluser/{usertype}')
def getAllUser(usertype:int, response:Response, db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    if(current_user['user_id']==1):
        data= db.query(modal.Users).filter(modal.Users.role_id !=1, modal.Users.role_id == usertype,   modal.Users.status == True).all()
        return {
            "status_code":200,
            "response_status":"success",
            "Response_data":data
        }
    else:
        response.status_code=status.HTTP_401_UNAUTHORIZED
        return {
            "status_code":401,
            "response_status":"failed",
            "Response_data":"Forbidden"
        }

@app.get('/getuser/{id}')
def getUser(id:int, response:Response, db:Session = Depends(db.get_db), current_user= Depends(auth.verify_token)):
    if(current_user['role_id'] == 1):
        data= db.query(modal.Users).filter(modal.Users.user_id == id, modal.Users.status == True).first()
        if data:
            return {
            "status_code":200,
            "response_status":"success",
            "Response_data":data
        }
        else:
            response.status_code=status.HTTP_401_UNAUTHORIZED
            return {
                "status_code":404,
                "response_status":"failed",
                "Response_data":"User not found"
            }
    else:
       response.status_code=status.HTTP_401_UNAUTHORIZED
       return {
            "status_code":401,
            "response_status":"failed",
            "Response_data":"Forbidden"
        }
       
#membership
@app.post('/addmembership')
def AddMembership(data:schema.Membership, db:Session= Depends(db.get_db)):
    membership_data= modal.Membership(**data.dict())
    db.add(membership_data)
    db.commit()
    db.refresh(membership_data)

    return {
        "status_code":200,
        "response_status":"success",
        "Response_data":membership_data
        }

@app.put('/updatemembership/{id}')
def AddMembership(id:int,data:schema.Membership, response:Response, db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    if(current_user['user_id']==1):
        membership_data= db.query(modal.Membership).filter(modal.Membership.id ==id )
        if membership_data.first():
            membership_data.update(data.dict(), synchronize_session= False)
            db.commit()
            return {
                "status_code":200,
                "response_status":"success",
                "Response_data":"Updated successfully"
            }
        else:
            response.status_code =status.HTTP_404_NOT_FOUND
            return{
                "status_code":404,
                "response_status":"failed",
                "Response_data":"Membership data not found"
            }
    else:
        response.status_code=status.HTTP_403_FORBIDDEN
        return{
            "status_code":403,
            "response_status":"failed",
            "Response_data":"Forbidden"
        }

@app.get('/viewallmachanicmembership')
def getMachanicMembership(db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data= db.query(modal.machanic_membership).all()
    for detail in data:
        user= db.query(modal.Users).filter(modal.Users.user_id == detail.user_id).first()
        detail.user_detail = user
    
    return {
            "status_code":200,
            "response_status":"success",
            "Response_data":data
        }