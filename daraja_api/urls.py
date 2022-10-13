from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRoutes),
    path('generateAcessToken/',views.viewTokenPassword),
    path('stk_push/', views.make_payment)
]