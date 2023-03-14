from pydantic import  BaseModel
from typing import Optional
from datetime import date

class AddUser(BaseModel):
    role_id:int
    name:str
    phone_no:int
    alternate_phone_no:Optional[int]
    password:str
    street:str
    town_city:str
    district:str
    state:str
    pincode:int
    vehicle_name:Optional[str]
    vehicle_no:Optional[str]
    vehicle_make:Optional[int]
    vehicle_brand:Optional[str]
    description:Optional[str]
    driving_license_no:Optional[str]
    kyc:Optional[str]
    location:Optional[str]
    
class EditUser(BaseModel):
    name:str
    phone_no:int
    alternate_phone_no:Optional[int]
    street:str
    town_city:str
    district:str
    state:str
    pincode:int
    vehicle_name:Optional[str]
    vehicle_no:Optional[str]
    vehicle_make:Optional[int]
    vehicle_brand:Optional[str]
    description:Optional[str]
    driving_license_no:Optional[str]
    kyc:Optional[str]
    location:Optional[str]

class Role(BaseModel):
    role_name:str

class Login(BaseModel):
    mobile_no:int
    password:str
    
class Membership(BaseModel):
    membership_name:str
    Membership_price:float
    validity:int
    customer_count:int

class ViewMembership(BaseModel):
    id:int
    membership_name:str
    Membership_price:float
    validity:int
    customer_count:int

    class Config:
        orm_mode= True
        
class BuyMembership(BaseModel):
    membership_id:int
    membership_name:Optional[str]
    user_id:Optional[int]
    paid_amount:float
    purchase_date:date
    payment_status:Optional[bool]
    expires_on:Optional[date]
    
class FindMachanic(BaseModel):
    town_city:str
    district:str
    state:str
    pincode:int
    
class Service(BaseModel):
    user_id:Optional[int]
    user_name : Optional[str]
    machanic_id:int
    macahnic_name: str
    call_center_id:Optional[int]
    attender_name: Optional[str]
    requested_date: date
    service_type: str
    service_location: str
    comments:Optional[str]
    Approved:Optional[bool]= False
    service_status: Optional[str]= 'Requested'
    service_cost: Optional[float]=0
    
