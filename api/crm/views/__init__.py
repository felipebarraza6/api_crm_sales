from .clients import ClientViewSet
from .orders import OrderViewSet, OrderItemViewSet, ShippingViewSet
from .payments import PaymentOrder, TypePayment
from .products import ProductViewSet, CategoryViewSet, InventoryViewSet, PriceViewSet
from .delivery import DeliveryViewSet
from .salesModule import SalesModuleViewSet
from .configs import ConfigViewSet
from .users import UserViewSet, ChangePasswordView