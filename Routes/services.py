from fastapi import APIRouter, Depends, HTTPException, status
import db, modal, schema
from Auth import auth
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

app= APIRouter(
    prefix='/service',
    tags=['Services']
)

@app.post('/findmachanic')
def findMachanic(data:schema.FindMachanic, db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    get_machanic= db.query(modal.Users).filter(
        func.upper(modal.Users.town_city).contains(data.town_city.upper()),
        func.upper(modal.Users.district).contains(data.district.upper()),
        func.upper(modal.Users.state).contains(data.state.upper()),
        modal.Users.pincode ==(data.pincode),
        modal.Users.role_id == 2
    ).order_by(modal.Users.user_id.desc()).all()
    
    for machanic in enumerate(get_machanic):
        check_plan=  db.query(modal.machanic_membership).filter(modal.machanic_membership.user_id == machanic[1].user_id ,modal.machanic_membership.expires_on<date.today()).first()
        
        if not check_plan:
            del get_machanic[machanic[0]]
        
    if get_machanic:
        return get_machanic
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Machanic not found in this location")

@app.post('/addservice')
def addService(data:schema.Service, db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data.user_id= current_user['user_id']
    data.user_name= current_user['name']
    
    serviceData= modal.Services(**data.dict())
    db.add(serviceData)
    db.commit()
    db.refresh(serviceData)
    
    return {"detail":"service requested successfully"}

@app.get('/viewrequest')
def ViewRequest(db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data= db.query(modal.Services).filter(modal.Services.machanic_id == current_user['user_id'], modal.Services.approved == False, modal.Services.service_status != "Cancelled").all()
    if data:
        return data
    else:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

@app.put('/acceptrequest/{id}')
def acceptRequest(id:int,db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data= db.query(modal.Services).filter(modal.Services.machanic_id == current_user['user_id'],modal.Services.id == id)
    
    if data.first():
        data.update({"approved":True}, synchronize_session= False)
        db.commit()
        return {"detail":"Request accepted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    
@app.put('/cancelrequest/{id}')
def acceptRequest(id:int,db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data= db.query(modal.Services).filter(modal.Services.machanic_id == current_user['user_id'],modal.Services.id == id)
    
    if data.first():
        data.update({"service_status":"Cancelled"}, synchronize_session= False)
        db.commit()
        return {"detail":"Request Rejected"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
 
@app.get('/viewservicehistory')
def GetServiceHistory(db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    print(current_user['role_id'])
    if(current_user['role_id'] == 2):
        get_data= db.query(modal.Services).filter(modal.Services.machanic_id == current_user['user_id'],modal.Services.approved == True).all()
    
        query = db.query(modal.Users)
        get_current_user= query.filter(modal.Users.user_id == current_user['user_id']).first()
        if(get_data):
            for data in get_data: 
                
                get_user= query.filter(modal.Users.user_id == data.user_id).first()
                data.customer_phone_no = get_user.phone_no
                data.machanic_phone_no = get_current_user.phone_no
            return get_data   
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    else:
  
        get_data= db.query(modal.Services).filter(modal.Services.user_id == current_user['user_id']).all()
        
        query = db.query(modal.Users)
        get_user= query.filter(modal.Users.user_id == current_user['user_id']).first()
        if(get_data):
            for data in get_data: 
                
                get_machanic= query.filter(modal.Users.user_id == data.machanic_id).first()
                data.machanic_phone_no = get_machanic.phone_no
                data.customer_phone_no = get_user.phone_no
            return get_data   
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
        
@app.delete('/removerequest/{id}')
def RemoveRequest(id:int,db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    data= db.query(modal.Services).filter(modal.Services.user_id == current_user['user_id'],modal.Services.id == id)
    
    if data.first():
        data.delete(synchronize_session= False)
        db.commit()
        return {"detail":"Service Cleared"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    
@app.put('/updaterequest/{id}')
def UpdateRequest(id:int, data:schema.Service, db:Session= Depends(db.get_db), current_user= Depends(auth.verify_token)):
    if(current_user['role_id'] == 2):
        serviceData= db.query(modal.Services).filter(modal.Services.id == id, modal.Services.machanic_id == current_user['user_id'])
    else:
        serviceData= db.query(modal.Services).filter(modal.Services.id == id, modal.Services.user_id == current_user['user_id'])
        
    
    if serviceData.first():
        serviceData.update(data.dict(), synchronize_session= False)
        db.commit()
        return {"detail":"Service updated"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    