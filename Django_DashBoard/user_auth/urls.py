from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('create/', views.create_blog, name='create_blog'),
    path('update/<str:slug>', views.update_blog, name= 'update_blog'),
    path('blog_detail/<str:slug>', views.blog_detail, name = 'blog_detail'),
    path('',views.landingpage, name='Landing_Home_Page'),
    path('home',views.home, name='home'),
    path('category', views.category, name='category'),
    path('self_blog', views.self_blogs, name = 'self_blog'),
    # path ('event', views.events, name= 'event'),
    path('book',views.booking_view,name='book'),
    path('A_detail/<str:slug>',views.A_detail, name='A_detail'),
    path('doc',views.list_doctors,name='doc'),
    path('appointments', views.appointment, name= 'appointment'),
    path('get_available_slots/', views.get_available_slots,name='available'),
    path('appointment_requests/', views.filter_appointment,name='appointment_request'),
    path('appointment_accept/<str:slug>', views.appointment_accept,name='appointment_accept'),
    path('peerchat/<str:slug>', views.meeting_link,name='meeting_link')
    # path('appointment',views.AD,name= 'A_detail')
]
