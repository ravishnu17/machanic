from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import db, modal, schema
from Auth import auth

app = APIRouter(
    prefix='/admin',
    tags=['Admin']
)

@app.get('/userlist/{id}')
def getMachaniclist(id:int, db:Session = Depends(db.get_db), current_user= Depends(auth.verify_token)):
    if(current_user['role_id'] == 1):
        data= db.query(modal.Users).filter(modal.Users.role_id == id).all()
        if data:
            return data
        else:
            raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="data not found")
    else:
       raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Forbidden") 