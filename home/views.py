from django.shortcuts import render
from django.http import HttpResponse
from user import views
from django.db import connection
from django.http import JsonResponse
# Create your views here.

def check_user_login():
    if views.user_info["user_is_exist"]: 
        message={'user_name':views.user_info["first_name"],'error':'false'}
    else:
        message={'user_name':'user.first_name','error':'true'}
    return message


def test(request):
    message=check_user_login()
    return render(request,'home/home.html',message)


def about(request):
    message=check_user_login()
    return render(request,'home/about.html',message)


def services(request):
    message=check_user_login()
    return render(request,'home/services.html',message)


def contact_us(request):
    message=check_user_login()
    return render(request,'home/contactus.html',message)

# def add_to_card(request):
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")  # المنتج اللي ضغط عليه
        
        if not views.user_info['user_is_exist']:
            # print("user is exist => false ")
            return JsonResponse({"message": "User not logged in", "error": True})

        # تحديد اسم الجدول الخاص بالمستخدم
        global card_table_name
        card_table_name = f"user_{views.user_info["user_id"]}_card"

        with connection.cursor() as cursor:
            # 1️⃣ إنشاء جدول الكارت لو مش موجود
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {card_table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL UNIQUE,
                    quantity INT NOT NULL
                )
            """)
             # 2️⃣ التحقق إذا كان المنتج موجودًا بالفعل في الكارت
            cursor.execute(f"SELECT quantity FROM {card_table_name} WHERE product_id = %s", [product_id])
            result = cursor.fetchone()

            if result:
                # 3️⃣ إذا كان المنتج موجودًا، يتم **زيادة الكمية**
                # print(result[0])
                # print("khaled saad")
                new_quantity = result[0] + 1
                cursor.execute(f"UPDATE {card_table_name} SET quantity = %s WHERE product_id = %s", [new_quantity, product_id])
                return JsonResponse({"message": f"Quantity updated to {new_quantity}", "error": False})
            else:
                # 4️⃣ إذا لم يكن المنتج موجودًا، يتم إضافته مع `quantity = 1`
                cursor.execute(f"INSERT INTO {card_table_name} (product_id, quantity) VALUES (%s, 1)", [product_id])
                return JsonResponse({"message": "Product added to cart with quantity 1", "error": False})


        return JsonResponse({"message": "Product added to cart!", "error": False})
    
    return JsonResponse({"message": "Invalid request", "error": True})