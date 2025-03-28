"""
URL configuration for RootReach project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from . import settings
from django.conf.urls.static import static
from .views import update_profile
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('product/',include('products.urls')),
    path('about/', views.about, name='about'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'), #new user
        #product page below
    path('product_page/<int:pk>', views.product_page, name='product_page'),
    path('category/<str:foo>/', views.category, name='category'),
    path('category_summary/',views.category_summary, name='category_summary'),

    path('cart/',include('cart.urls')),
                  # update user
# path('update/', views.update_user, name='update_user'),
path('profile/update/', update_profile, name='update_profile'),

path('search/', views.search, name='search'),
 #seller- zone
 path('seller-area/', views.seller_area, name='seller_area'),
    #crud - seller
 path('upload-product/', views.upload_product, name='upload_product'),
 path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
 path('upload-product/<int:product_id>/', views.upload_product, name='edit_product'),# For editing product

 path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
