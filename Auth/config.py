from pydantic import BaseSettings

class Secrets(BaseSettings):
    dbname:str
    dbuser:str
    host:str
    port:int
    db_password:str
    db_url:str
    
    class Config:
        env_file= ".env"
        
secret= Secrets()