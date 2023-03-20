from fastapi import APIRouter, Depends, HTTPException, status, Response
import schema, db, modal
from Auth import auth
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta, date

app= APIRouter(
    tags=['Membership'],
    prefix='/membership'
)



@app.get('/viewmembership', response_model=schema.ViewMembership)
def Get_membership(db:Session= Depends(db.get_db)):
    data= db.query(modal.Membership).all()
    
    return {
        "status_code":200,
        "response_status":"success",
        "Response_data":data
        }

@app.post('/buymembership')
def buyMembership(data:schema.BuyMembership, db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    getMembershipData= db.query(modal.Membership).filter(modal.Membership.id == data.membership_id).first()
    
    get_user= db.query(modal.machanic_membership).filter(modal.machanic_membership.user_id == current_user['user_id'])
    if(get_user.first()):
        data.payment_status=True
        data.user_id= current_user['user_id']
        data.purchase_date= date.today()
        data.expires_on= date.today()+ timedelta(days=getMembershipData.validity)
        data.membership_name=getMembershipData.membership_name
        get_user.update(data.dict(), synchronize_session= False)
        db.commit()
        return {
            "status_code":200,
            "response_status":"success",
            "Response_data":"Membership upgraded"
        }
    else:
        data.payment_status=True
        data.user_id= current_user['user_id']
        data.expires_on= date.today()+ timedelta(days=getMembershipData.validity)
        data.membership_name=getMembershipData.membership_name
        memberData= modal.machanic_membership(**data.dict())
        db.add(memberData)
        db.commit()
        
        return {
            "status_code":200,
            "response_status":"success",
            "Response_data":"Membership added successfully"
        }

@app.get('/viewmachanicmembership')
def getMachanicMembership(db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data= db.query(modal.machanic_membership).filter(modal.machanic_membership.user_id == current_user['user_id']).first()
    
    return {
            "status_code":200,
            "response_status":"success",
            "Response_data":data
        }

@app.delete('/cancelmachanicmembership')
def getMachanicMembership(response:Response, db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data= db.query(modal.machanic_membership).filter(modal.machanic_membership.user_id == current_user['user_id'])
    if data.first():
        data.delete(synchronize_session=False)
        db.commit()
        return {
            "status_code":200,
            "response_status":"success",
            "Response_data":"Membership is cancelled"
        }
    else:
        response.status_code=status.HTTP_404_NOT_FOUND
        {
            "status_code":404,
            "response_status":"failed",
            "Response_data":"Membership data not found"
        }
        
           