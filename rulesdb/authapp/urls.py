from django.urls import path
from .views import signup_view, login_view, logout_view, panel_view, logs_view, notifications_view, rules_view, \
    notification_subscriptions_view, auth_home_view

urlpatterns = [
    path('', auth_home_view, name='auth_home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('panel/', panel_view, name='panel'),
    path('logs/', logs_view, name='logs'),
    path('notifications/', notifications_view, name='notifications'),
    path('notification_subscriptions/', notification_subscriptions_view, name='notification_subscriptions'),
    path('rules/', rules_view, name='rules'),
]
