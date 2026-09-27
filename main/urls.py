from django.contrib import admin
from django.urls import path
from main import views


admin.site.site_header = "Musafir Cafe Admin"
admin.site.site_title = "Musafir Cafe Admin Portal"
admin.site.index_title = "Welcome to Musafir Cafe Admin Portal"

urlpatterns = [
    path("", views.index, name="main"),
    path("menu/", views.menu, name="menu"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("order/", views.order_tracking, name="order_tracking_home"),
    path("order/lookup/", views.order_lookup, name="order_lookup"),
    path("order/<str:token>/", views.order_tracking, name="order_tracking"),
    path("order/<str:token>/update-status/", views.update_order_status, name="update_order_status"),
    path("kitchen/", views.kitchen_dashboard, name="kitchen_dashboard"),
    path("place-order/", views.place_order, name="place_order"),
]

