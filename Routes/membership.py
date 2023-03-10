from fastapi import APIRouter, Depends
import schema, db, modal
from sqlalchemy.orm import Session
from typing import List

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