from pydantic import BaseModel

class Contact(BaseModel):
    name:str
    email:str
    subject:str
    message:str

class User(BaseModel):
    name:str
    email:str
    password:str
    type:int
   

class Product(BaseModel):
    id:int
    name:str
    email:str
    perhour:str
    amount:str
    description:str
    address:str
    equipment:str

class Order(BaseModel):
    user:str
    total:str
    address:str

# serializers
    
def serialize_products(objs):
    datas=[]
    for index,obj in enumerate(objs):
        data=dict()
        data['id']=obj[0]
        data['name']=obj[1]
        data['equipment']=obj[2]
        data['phone']=obj[3]
        data['email']=obj[4]
        data['description']=obj[5]
        data['image']=obj[6]
        data['amount']=obj[7]
        data['address']=obj[8]
        data['perhour']=obj[9]
        data['category']=obj[10]
        datas.append(data)
    return datas



def serialize_users(objs):
    datas=[]
    for obj in objs:
        data=dict()
        data['name']=obj[0]
        data['email']=obj[1]
        data['password']=obj[2]
        datas.append(data)
    return datas


def serialize_contact(objs):
    datas=[]
    for obj in objs:
        data=dict()
        data['name']=obj[0]
        data['email']=obj[1]
        data['subject']=obj[2]
        data['message']=obj[3]
        datas.append(data)
    return datas

def serialize_order(objs):
    datas=[]
    for index,obj in enumerate(objs):
        data=dict()
        data['id']=index
        data['user']=obj[0]
        data['product']=obj[1]
        data['address']=obj[2]
        data['total']=obj[3]
        data['date']=obj[4]
        datas.append(data)
    return datas


def serialize_product(objs):
    datas=[]
    for obj in objs:
        data=dict()
        data['id']=obj[0]
        data['name']=obj[1]
        data['equipment']=obj[2]
        data['phone']=obj[3]
        data['email']=obj[4]
        data['description']=obj[5]
        data['image']=obj[6]
        data['amount']=obj[7]
        data['address']=obj[8]
        data['perhour']=obj[9]
        data['category']=obj[10]
        datas.append(data)
    return datas