from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('tracker_list', views.tracker_list, name='tracker_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("about/", views.about, name="about"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("api/get-product/<str:barcode>/", views.get_product_by_barcode),
    #url = reverse('update_product', kwargs={'pk': product_id})

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='core/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/password_reset_complete.html'), name='password_reset_complete'),

    # Tracker and inventory
    path('trackers/create/', views.tracker_create, name='tracker_create'),
    path('trackers/<int:tracker_id>/inventory/', views.inventory, name='inventory'),
    path('trackers/<int:tracker_id>/?sort=name', views.inventory, name='inventory'),
    path('trackers/<int:tracker_id>/inventory/?sort=quantity', views.inventory, name='inventory'),
    path('trackers/<int:tracker_id>/inventory/?sort=price', views.inventory, name='inventory'),
    path('trackers/<int:tracker_id>/add/', views.add_product, name='add_product'),
    path('trackers/<int:tracker_id>/sell/', views.sell_product, name='sell_product'),
    path('trackers/<int:tracker_id>/sales/', views.sales_records, name='sales_records'),
    path('trackers/<int:tracker_id>/dashboard/', views.dashboard, name='dashboard'),
    path('trackers/<int:tracker_id>/export/inventory/', views.export_inventory_csv, name='export_inventory_csv'),
    path('trackers/<int:tracker_id>/export/sales/', views.export_sales_csv, name='export_sales_csv'),
    path("/product/<int:pk>/update/", views.update_product, name="update_product"),
    path("product/<int:pk>/print_barcode/", views.print_barcode, name="print_barcode"),
    path("tracker/<int:tracker_id>/api/autocomplete/", views.autocomplete_products, name="autocomplete_products"),
    
]