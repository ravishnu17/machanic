from fastapi import APIRouter, Depends, HTTPException, status
import schema, db, modal
from Auth import auth
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta, date

app= APIRouter(
    tags=['Membership'],
    prefix='/membership'
)

@app.post('/addmembership')
def AddMembership(data:schema.Membership, db:Session= Depends(db.get_db)):
    membership_data= modal.Membership(**data.dict())
    db.add(membership_data)
    db.commit()
    db.refresh(membership_data)

    return membership_data

@app.get('/viewmembership', response_model=List[schema.ViewMembership])
def Get_membership(db:Session= Depends(db.get_db)):
    data= db.query(modal.Membership).all()
    
    return data

@app.put('/updatemembership/{id}')
def AddMembership(id:int,data:schema.Membership, db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    if(current_user['user_id']==1):
        membership_data= db.query(modal.Membership).filter(modal.Membership.id ==id )
        if membership_data.first():
            membership_data.update(data.dict(), synchronize_session= False)
            db.commit()
            return {"detail":"Updated successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

@app.post('/buymembership')
def buyMembership(data:schema.BuyMembership, db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    getMembershipData= db.query(modal.Membership).filter(modal.Membership.id == data.membership_id).first()
    
    get_user= db.query(modal.machanic_membership).filter(modal.machanic_membership.user_id == current_user['user_id'])
    if(get_user.first()):
        data.payment_status=True
        data.user_id= current_user['user_id']
        data.expires_on= date.today()+ timedelta(days=getMembershipData.validity)
        data.membership_name=getMembershipData.membership_name
        get_user.update(data.dict(), synchronize_session= False)
        db.commit()
        return {"detail":"Membership upgraded"}
    else:
        data.payment_status=True
        data.user_id= current_user['user_id']
        data.expires_on= date.today()+ timedelta(days=getMembershipData.validity)
        data.membership_name=getMembershipData.membership_name
        memberData= modal.machanic_membership(**data.dict())
        db.add(memberData)
        db.commit()
        
        return {"detail":"Membership added successfully"}
    
@app.get('/viewallmachanicmembership')
def getMachanicMembership(db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data= db.query(modal.machanic_membership).all()
    
    return data

@app.get('/viewmachanicmembership')
def getMachanicMembership(db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data= db.query(modal.machanic_membership).filter(modal.machanic_membership.user_id == current_user['user_id']).all()
    
    return data

@app.delete('/cancelmachanicmembership')
def getMachanicMembership( db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data= db.query(modal.machanic_membership).filter(modal.machanic_membership.user_id == current_user['user_id'])
    if data.first():
        data.delete(synchronize_session=False)
        db.commit()
        return {"detail":"Membership is removed"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
        
           