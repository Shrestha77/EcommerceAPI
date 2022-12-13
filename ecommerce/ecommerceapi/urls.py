from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('changepassword/', views.UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', views.SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',views.UserPasswordResetView.as_view(), name='reset-password'),

    path('productcreate/', views.ProductListCreateAPIView.as_view(), name='product_create'),
    path('<int:pk>/productdetails/', views.ProductDetailsAPIView.as_view(),
         name='product_details'),
    path('<int:pk>/update/', views.ProductUpdateAPIView.as_view(), name='Product_update'),
    path('<int:pk>/delet/', views.ProductDestroyAPIView.as_view(),
         name='Product_delet')
]
