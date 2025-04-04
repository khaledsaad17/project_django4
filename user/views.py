from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import connection
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
# from home import views

# Create your views here.

user_info = {"user_is_exist":False}


def login(request):
    
    message = {'message':'khaled','error':'False'}
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # print("\n\n\n\n")
        # print(password)
        # print("\n\n\n\n")
        confirm_password = request.POST.get("confirm_password")

        # التحقق من تطابق كلمتي المرور
        if password != confirm_password:
            # print("Passwords do not match!")
            messages.error(request, "Passwords do not match!")
            message = {'message':"Passwords do not match!","error":"true"}
            return render(request, "user/login_and_signup.html",message)

        # التأكد أن البريد الإلكتروني غير مسجل مسبقًا
        if User.objects.filter(email=email).exists():
            # print("Email already exists!")
            message = {'message':"Email already exists!","error":"true"}
            return render(request, "user/login_and_signup.html",message)

        # إنشاء مستخدم جديد وتخزينه في MySQL
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password)  # تشفير كلمة المرور
        )

        # messages.success(request, "Account created successfully!")
        message = {'message':"Account created successfully!","error":"true"}
        # print("Account created successfully!")
        return render(request, "user/login_and_signup.html",message)  # تغييرها إلى صفحة تسجيل الدخول المناسبة

    return render(request, "user/login_and_signup.html",message)
    # return render(request,'user/login_and_signup.html')
    
def enter_system(request):
     if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):  # لو كلمة المرور صحيحة
                message={'user_name':user.first_name,'error':'false'}
                
                # login(request, user)  # تسجيل دخول المستخدم
                # print("\n\n\nthe password is correct enjoy with login in \n\n\n")
                
                # user_check = authenticate(username=email, password=password)
                # print(user.id)
                # علشان البيانات تبقى متشافه ف اكتر من مكان 
                global user_info
                user_info={"first_name":user.first_name,
                            "last_name":user.last_name,
                            "user_id":user.id,
                            "user_is_exist":True,
                            "email":user.email}
                
                return render(request,'home/home.html',message)  # حوله للصفحة الرئيسية بعد تسجيل الدخول 
            else:
                message = {'message':"Incorrect password!","error":"true"}
                return render(request, "user/login_and_signup.html",message)# لو الباسورد غلط
                
        except User.DoesNotExist:
            message = {'message':"email is not exist","error":"true"}
            return render(request, "user/login_and_signup.html",message)  # لو الإيميل مش موجود في الداتا بيز
                                                                            # رجّع المستخدم لصفحة تسجيل الدخول لو فيه خطأ
                                                                            
def card(request):
    if not user_info['user_is_exist']:
            # print("user is exist => false ")
            return render(request,"user/login_and_signup.html")
    with connection.cursor() as cursor:
        
            cursor.execute(f"SELECT product_id,quantity FROM user_{user_info["user_id"]}_card ;")
            result = cursor.fetchall()
            # print(result)
            # print(result.__len__())
    # context={}
    list_of_product_and_quantity=[]
    total_price = 0
    for row in result:
        with connection.cursor() as cursor:
        
            cursor.execute(f"SELECT p_name,price,image_direction FROM products where id = {row[0]} ;")
            product_details = cursor.fetchall()
        # print(product_details[0][0])
        price = ( product_details[0][1] * row[1] )
        total_price += price
        r={'product_id':row[0],
           'product_quantity':row[1],
           'product_name':product_details[0][0],
           'product_price': price,
           'product_direction':product_details[0][2]}
        list_of_product_and_quantity.append(r)
    
    # Calculate tax (5%) and shipping
    tax = total_price * 0.05
    shipping = 15  # Fixed shipping cost
    final_total = total_price + tax + shipping
    
    context={
        'products': list_of_product_and_quantity,
        'subtotal': total_price,
        'tax': tax,
        'shipping': shipping,
        'total': final_total
    }
    # print(context)
            
            
    return render(request,"user/card.html",context)

@csrf_exempt
def update_quantity(request):
    if request.method == "POST":
        # print("\n\n\n\n it is done successfully of post")
        data = json.loads(request.body)
        product_id = data.get("product_id")
        new_quantity = data.get("quantity")
        cart_table_name = f"user_{user_info['user_id']}_card"

        with connection.cursor() as cursor:
            cursor.execute(f"""
                UPDATE {cart_table_name} 
                SET quantity = %s 
                WHERE product_id = %s
            """, [new_quantity, product_id])
        # print("\n\n\n\n it is done successfully")
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)    

@csrf_exempt
def remove_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        cart_table_name = f"user_{user_info['user_id']}_card"

        with connection.cursor() as cursor:
            cursor.execute(f"""
                DELETE FROM {cart_table_name} 
                WHERE product_id = %s
            """, [product_id])
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

def sign_out(request):
    global user_info
    user_info = {"user_is_exist": False}
    return redirect("login")

def checkout(request):
    if not user_info['user_is_exist']:
        return redirect("login")
        
    # Get cart total and other details
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT product_id,quantity FROM user_{user_info['user_id']}_card;")
        result = cursor.fetchall()
        # print("the checkout is done successfully")
        
    total_price = 0
    for row in result:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT price FROM products where id = {row[0]};")
            product_price = cursor.fetchone()[0]
            total_price += (product_price * row[1])
    
    tax = total_price * 0.05
    shipping = 15
    final_total = total_price + tax + shipping
    
    
    context = {
        'user_info': {
            'first_name': user_info['first_name'],
            'last_name': user_info['last_name'],
            'email': user_info['email']
        },
        'subtotal': total_price,
        'tax': tax,
        'shipping': shipping,
        'total': final_total
    }
    
    
    return render(request, "user/checkout.html", context)

def process_checkout(request):
    if request.method == "POST":
        # Get form data
        phone = request.POST.get("phone")
        street = request.POST.get("street")
        city = request.POST.get("city")
        state = request.POST.get("state")
        
        # Here you could save the order details to a new table if needed
        
        # Clear the user's cart
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM user_{user_info['user_id']}_card;")
        
        messages.success(request, "Order placed successfully!")
        return redirect("home")  # Redirect to home page after successful order
        
    return redirect("checkout")
    