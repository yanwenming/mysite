from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

app_name="account"

urlpatterns = [
    path('login/',auth_view.LoginView.as_view(template_name='account/login2.html'),name='user_login'), # 这里设置name，为了是在模板文件中，写name就能找到这个路由
    path('logout/',auth_view.LogoutView.as_view(template_name='account/logout.html'),name='user_logout'),
    path('register/',views.register,name='user_register'),
    path('password-change/',auth_view.PasswordChangeView.as_view(template_name="account/password_change_form.html",success_url="/account/password-change-done/"),name='password_change'),
    path('password-change-done/',auth_view.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"),name='password_change_done'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name="account/password_reset_form.html", email_template_name="account/password_reset_email.html", success_url='/account/password-reset-done/'), name='password_reset'),
    path('password-reset-done/', auth_view.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html", success_url='/account/password-reset-complete/'), name="password_reset_confirm"),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('my-information/',views.myself,name="my_information"),
    path('edit-my-information/',views.myself_edit,name="edit_my_information"),
    # path('my-image/',views.my_image,name="my_image"),
]