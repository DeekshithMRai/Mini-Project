import shutil
from fastapi import APIRouter, File, Form,Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from datetime import datetime
from .db import db
from .models import Contact, serialize_contact, serialize_order, serialize_product, serialize_users,  serialize_products
from backend.models import User
router = APIRouter()


templates = Jinja2Templates(directory="templates")

# get requests

@router.get("/",response_class=HTMLResponse)
async def root(request:Request):
    data=dict(request.headers)
    return templates.TemplateResponse("index.html",context={"request":request})

@router.get('/contact',response_class=HTMLResponse)
async def contact_route(request:Request):
    return templates.TemplateResponse("contact.html",context={"request":request})

@router.get('/user-signin',response_class=HTMLResponse)
async def contact_route(request:Request):
    return templates.TemplateResponse("signup.html",context={"request":request})

@router.get('/admin',response_class=HTMLResponse)
async def contact_route(request:Request):
    query='''select * from users where type=1;'''
    cursor=db.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    data=serialize_users(result)
    print(data)
    return templates.TemplateResponse("admindetails.html",context={"request":request,"admin":data})

@router.get('/admin/users',response_class=HTMLResponse)
async def admin_user(request:Request):
    query = '''select * from users '''
    cursor=db.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    data=serialize_users(result)
    return templates.TemplateResponse("userdetails.html",context={"request":request,'users':data})

@router.get('/admin/contact',response_class=HTMLResponse)
async def admin_user(request:Request):
    query = '''select * from contact '''
    cursor=db.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    data=serialize_contact(result)
    return templates.TemplateResponse("contactdetails.html",context={"request":request,'contact':data})

@router.get('/admin/product',response_class=HTMLResponse)
async def admin_user(request:Request):
    query = '''select * from products_category '''
    cursor=db.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    data=serialize_product(result)
    return templates.TemplateResponse("productdetails.html",context={"request":request,'product':data})

@router.get('/admin/order',response_class=HTMLResponse)
async def admin_user(request:Request):
    query = '''select o.users,p.equipment,o.address,o.total,o.order_date from orders o, product p where p.id=o.product;  '''
    cursor=db.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    data=serialize_order(result)
    return templates.TemplateResponse("orderdetails.html",context={"request":request,'orders':data})

@router.get('/order/{pid}')
async def get_products(request:Request,pid:int):
    query='''select * from product where id=%s'''
    cursor=db.cursor()
    cursor.execute(query,(pid,))
    result=cursor.fetchone()
    data=serialize_products([result])
    return templates.TemplateResponse("order.html",context={"request":request,'product':data[0]})

@router.get('/vendor',response_class=HTMLResponse)
async def vendor_page(reqeust:Request):
    return templates.TemplateResponse('vendorDash.html',context={"request":reqeust})

@router.get('/vendor/add',response_class=HTMLResponse)
async def vendor_page(reqeust:Request):
    data=[]
    cursor=db.cursor()
    cursor.execute('''select * from category''')
    categories=cursor.fetchall()
    for i in categories:
        data.append({'id':i[1],'name':i[0]})
    return templates.TemplateResponse('upload.html',context={"request":reqeust,'categories':data})




# @router.post("/vendor/add")
# async def add_product(
#     name: str = Form(...),
#     equipment: str = Form(...),
#     phone: str = Form(...),
#     email: str = Form(...),
#     description: str = Form(...),
#     image: UploadFile = File(...),
#     amount: float = Form(...),
#     address: str = Form(...),
#     perhour: float = Form(...)
# ):
#     query= """
# INSERT INTO product (name, equipment, phone, email, description, image, amount, address, perhour)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
# """
#     try:
#         cursor=db.cursor()
#         cursor.execute(query,(name,equipment,phone, email, description, image.filename, amount, address, perhour))
#         db.commit()
#         with open(f"image/{image.filename}", "wb") as buffer:
#             shutil.copyfileobj(image.file, buffer)
#         return {'message':"product added successfully"}
#     except Exception as e:
#          return {"message": "Product was not added","error":str(e)}

@router.post("/vendor/add")
async def add_product(
    name: str = Form(...),
    equipment: str = Form(...),
    category: int = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    amount: float = Form(...),
    address: str = Form(...),
    perhour: float = Form(...),
):
    query = """
    INSERT INTO product (name, equipment, phone, email, description, image, amount, address, perhour,category)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
    """
    try:
        cursor = db.cursor()
        cursor.execute(query, (name, equipment, phone, email, description, image.filename, amount, address, perhour,category))
        db.commit()
        # Save the uploaded image to the server
        with open(f"static/image/{image.filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        return {"message": "Product added successfully"}
    except Exception as e:
        return {"message": "Product was not added", "error": str(e)}


@router.get('/vendor/orders') 
async def get_vendor_orders(reqeust:Request):
    query = '''select o.users,p.equipment,o.address,o.total,o.order_date from orders o, product p where p.id=o.product;  '''
    cursor=db.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    data=serialize_order(result)
    return templates.TemplateResponse('showOrders.html',context={"request":reqeust,'orders':data})

# spl get requests

@router.get('/vendors',response_class=HTMLResponse)
async def contact_route(request:Request):
    data=[]
    cursor=db.cursor()
    query='''select * from products_category'''
    cursor.execute(query)
    result=cursor.fetchall()
    data=serialize_products(result)
    return templates.TemplateResponse("pricing.html",context={"request":request,'products':data})


# post requests

@router.post('/contact')
async def save_contact(contact:Contact):
    cursor=db.cursor()
    query='''insert into contact values (%s,%s,%s,%s);'''
    try:
        cursor.execute(query,(contact.name, contact.email,contact.subject,contact.message))
        db.commit()
        return {'message':'contact saved'}
    except Exception as e:
        return {'message':'unable to save','exception':str(e)}
    

# spl post requests
    
@router.post('/user-signin',response_class=HTMLResponse)
async def handle_user(request:Request,email:str=Form(...),password:str=Form(...)):
    query = ''' select password,type from users where email=%s;'''
    cursor=db.cursor()
    cursor.execute(query,(email,))
    result=cursor.fetchone()
    print(result)
    if result[0]==password:
        if result[1]==1: # admin
            return templates.TemplateResponse("temp.html",context={"request":request,'user':email,'type':1})
        elif result[1]==2: # seller
            return templates.TemplateResponse("temp.html",context={"request":request,"type":2,'user':email})
        if result[1]==3: # user 
            return templates.TemplateResponse("temp.html",context={"request":request,'user':email,"type":3})
    else:
        return {'message':'invalid credentials'}

@router.post('/order/{pid}')
async def place_order(request:Request,pid:int,user:str=Form(...),total:str=Form(...),address:str=Form(...)):
    query='''insert into orders() values (%s,%s,%s,%s,%s);'''
    obj=datetime.now()
    try:
        print(user,pid,address)
        cursor=db.cursor()
        cursor.execute(query,(user,pid,address,total,f'{obj.year}-{obj.month}-{obj.day}'))
        db.commit()
        return templates.TemplateResponse("temp.html",context={"request":request,'user':user,"type":3})
    except Exception as e:
        return {'message':'order was not saved','error':str(e)}
    
    #register

@router.post('/login')
async def register(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    cursor = db.cursor()
    query = '''insert into users (name, email, password) values (%s, %s, %s);'''
    try:
        cursor.execute(query, (name, email, password))
        db.commit()
        return {'message': 'Registration Successful'}
    except Exception as e:
        return {'message': 'Registration not Successful', 'exception': str(e)}
    
@router.delete("/users/{email}")
async def delete_user(email: str):
    try:
        cursor = db.cursor()

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete user
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        db.commit()

        return {"message": f"User with email {email} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()