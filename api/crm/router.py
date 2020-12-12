"""CRM Routers."""

# Django
from django.urls import include, path
from django.conf.urls import url, include
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from api.crm import views

router = DefaultRouter()

router.register(r'clients', views.ClientViewSet, basename='clients')
# order
router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(r'orders-items', views.OrderItemViewSet, basename='orders-items')
router.register(r'orders-shippings', views.ShippingViewSet, basename='orders-shippings')
# payments
router.register(r'payments', views.PaymentOrder, basename='payments')
router.register(r'payments/order', views.PaymentOrder, basename='payments-order')
router.register(r'type-payments', views.TypePayment, basename='type-payment')
# finish payments
# products
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'products-categories', views.CategoryViewSet, basename='products-categories')
router.register(r'products-inventories', views.InventoryViewSet, basename='products-inventories')
router.register(r'products-prices', views.PriceViewSet, basename='products-prices')
# finish products
router.register(r'deliveries', views.DeliveryViewSet, basename='deliveries')
router.register(r'sales-module', views.SalesModuleViewSet, basename='sales-module')
router.register(r'config', views.ConfigViewSet, basename='config')
# Users
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('change_password/', views.ChangePasswordView.as_view(), name='change-password'),
]
