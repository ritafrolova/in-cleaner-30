from django.urls import path
from .views import SignUpView, profile_settings, home, create_order, user_orders, assign_order, create_report, \
    confirm_order, show_report, tinder, assign_tinder_order, delete_order

urlpatterns = [
    path('', home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('settings/', profile_settings, name='settings'),
    path('tinder/', tinder, name='tinder'),
    path('create-order/', create_order, name='create-order'),
    path('orders/', user_orders, name='user-orders'),
    path('assign-order/<int:order_id>', assign_order, name='assign-order'),
    path('create-report/<int:order_id>', create_report, name='create-report'),
    path('show-report/<int:report_id>', show_report, name='show-report'),
    path('confirm-order/<int:order_id>', confirm_order, name='confirm-order'),
    path('assign-order/tinder/<int:worker_id>', assign_tinder_order, name='assign-tinder-order'),
    path('delete-order/<int:order_id>', delete_order, name='delete-order'),
]
