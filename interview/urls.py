from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('schedule/',views.schedule_interview,name='schedule_interview'),
    path('interviewer/',views.interviewer_dashboard,name='interviewer_dashboard'),
    path('interviewer_list/',views.interviewer_list,name='interviewer_list'),
    path('feedback/<int:interview_id>',views.feedback,name='feedback'),
    path('candidate/',views.candidate_dashboard,name='candidate_dashboard'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('register/interviewer/',views.interviewer_register,name='interviewer_register'),
    path('register/candidate/', views.candidate_register, name='candidate_register'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete' ),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
    path('result/', views.result, name='result'),
    path('logout/', views.logout_view, name='logout'),
]