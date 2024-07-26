from fastapi import FastAPI
from Routes import users, membership, services, admin
# modal.base.metadata.create_all(bind= db.engine)
import requests, time

def restart():
    i=1
    while i < 5:
        try:
            requests.get('https://machanicapiuvicorn.onrender.com/')
        except:
            pass
        time.sleep(5)
        i+=1


app= FastAPI(
    on_shutdown=[restart]
)

app.include_router(users.app)
app.include_router(membership.app)
app.include_router(services.app)
app.include_router(admin.app)

@app.get('/')
def Sample():
    return "Works well"


