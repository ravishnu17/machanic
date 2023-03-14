from db import base
from sqlalchemy import String, Column, Integer, DateTime, func, Boolean, ForeignKey, BigInteger, Float, Date

# class Test(base):
#     __tablename__= "test"
#     id=Column(Integer,primary_key=True, nullable= False)
#     name= Column(String, nullable= False)
#     createdAt= Column(DateTime, nullable= False, server_default=func.now())

class Role(base):
    __tablename__= "tbl_role"
    role_id= Column(Integer, primary_key=True, nullable= False)
    role_name= Column(String, nullable=False)
    role_status= Column(Boolean, nullable=False , server_default='true')
    createdAt= Column(DateTime, nullable=False, server_default=func.now())

class Users(base):
    __tablename__= "tbl_users"
    user_id= Column(Integer, primary_key=True, nullable= False)
    role_id=Column(Integer, ForeignKey('tbl_role.role_id',ondelete='CASCADE'),nullable=False)
    name= Column(String, nullable= False)
    phone_no= Column(BigInteger, nullable= False)
    alternate_phone_no= Column(BigInteger)
    password= Column(String, nullable= False)
    street= Column(String, nullable= False)
    town_city= Column(String, nullable= False)
    district= Column(String, nullable= False)
    state= Column(String, nullable= False)
    pincode= Column(BigInteger, nullable= False)
    vehicle_name= Column(String)
    vehicle_no= Column(String)
    vehicle_make= Column(Integer)
    vehicle_brand= Column(String)
    driving_license_no= Column(String)
    description= Column(String)
    status= Column(Boolean, server_default='true')
    kyc= Column(String)
    location= Column(String)
    createdAt= Column(DateTime, nullable=False, server_default=func.now())

class Membership(base):
    __tablename__= "tbl_membership"
    id= Column(Integer, primary_key=True, nullable=False)
    membership_name= Column(String, nullable= False)
    Membership_price= Column(Float, nullable= False)
    validity= Column(Integer, nullable= False)
    validity_type= Column(String, nullable= False, server_default='days')
    customer_count= Column(Integer, nullable=False)
    createdAt= Column(DateTime, nullable=False, server_default=func.now())

class machanic_membership(base):
    __tablename__= "tbl_machanic_membership"
    
    id= Column(Integer, primary_key=True, nullable= False)
    user_id= Column(Integer,ForeignKey("tbl_users.user_id", ondelete="CASCADE"), nullable=False)
    membership_id= Column(Integer,ForeignKey("tbl_membership.id"), nullable=False)
    membership_name= Column(String, nullable= False)
    payment_status= Column(Boolean, nullable=False, server_default='false')
    paid_amount= Column(Float, nullable= False)
    purchase_date= Column(Date, nullable=False, server_default=func.now())
    expires_on= Column(Date, nullable=False)
    
    
class Services(base):
    __tablename__ = "tbl_services"
    
    id= Column(Integer, primary_key=True, nullable= False)
    user_id= Column(Integer,ForeignKey("tbl_users.user_id", ondelete="CASCADE"), nullable=False)
    user_name= Column(String, nullable= False)
    machanic_id= Column(Integer,ForeignKey("tbl_users.user_id", ondelete="CASCADE"), nullable=False)
    macahnic_name= Column(String, nullable= True)
    call_center_id= Column(Integer,ForeignKey("tbl_users.user_id", ondelete="CASCADE"), nullable=True)
    attender_name= Column(String, nullable= True)
    requested_date= Column(Date, nullable=False)
    service_type= Column(String, nullable=True)
    service_location= Column(String, nullable= False)
    comments= Column(String,nullable= True)
    Approved= Column(Boolean, nullable= False, server_default='false')
    service_status= Column(String, nullable= True)
    service_cost= Column(Float, nullable= True)
    

