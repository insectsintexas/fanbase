from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from app.views import frontpage, post_detail, signup, user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", frontpage),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("<slug:slug>/", post_detail, name="post_detail"),

]
