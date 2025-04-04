from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import connection
from user import views

# Create your views here.

def medication_category(request):
    return render(request,'category/medication.html',{'user_info': views.user_info})

def haircare_category(request):
    return render(request,'category/haircare.html',{'user_info': views.user_info})

def Baby_Mom_category(request):
    return render(request,'category/Baby_Mom.html',{'user_info': views.user_info})

def makeup_category(request):
    return render(request,'category/makeup.html',{'user_info': views.user_info})

def skincare_category(request):
    return render(request,'category/skincare.html',{'user_info': views.user_info})



@require_POST
def toggle_favorite(request):
    if not views.user_info['user_is_exist']:
        return JsonResponse({
            'success': False,
            'message': 'Please login first'
        }, status=401)
    
    product_id = request.POST.get('product_id')
    user_id = views.user_info['user_id']
    table_name = f"fav_{user_id}"
    
    with connection.cursor() as cursor:
        # Create table if not exists
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        
        # Check if product exists
        cursor.execute("SELECT id FROM products WHERE id = %s", [product_id])
        if not cursor.fetchone():
            return JsonResponse({
                'success': False,
                'message': 'Product not found'
            }, status=404)
        
        # Check if favorite exists
        cursor.execute(f"SELECT id FROM {table_name} WHERE product_id = %s", [product_id])
        favorite = cursor.fetchone()
        
        if favorite:
            # Remove favorite
            cursor.execute(f"DELETE FROM {table_name} WHERE product_id = %s", [product_id])
            is_favorite = False
        else:
            # Add favorite
            cursor.execute(f"INSERT INTO {table_name} (product_id) VALUES (%s)", [product_id])
            is_favorite = True
    
    return JsonResponse({
        'success': True,
        'is_favorite': is_favorite
    })

def favorites(request):
    if not views.user_info['user_is_exist']:
        return redirect('login')
    
    user_id = views.user_info['user_id']
    table_name = f"fav_{user_id}"
    
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        if not cursor.fetchone():
            return render(request, 'Category/favorites.html', {'favorites': []})
        
        cursor.execute(f"""
            SELECT p.*, f.created_at 
            FROM products p 
            JOIN {table_name} f ON p.id = f.product_id 
        """)
        
        columns = [col[0] for col in cursor.description]
        favorites = [dict(zip(columns, row)) for row in cursor.fetchall()]
        # print(favorites)
    
    return render(request, 'Category/favorites.html', {'favorites': favorites,
                                                       'user_info': views.user_info})