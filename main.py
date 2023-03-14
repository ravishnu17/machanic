from fastapi import FastAPI, Depends
import db, modal, schema, utils
from sqlalchemy.orm import Session
from Routes import users, membership, services
# modal.base.metadata.create_all(bind= db.engine)

app= FastAPI()

app.include_router(users.app)
app.include_router(membership.app)
app.include_router(services.app)

@app.get('/')
def Sample():
    print(utils.encrypt("hello  "))
    return "Works well"


