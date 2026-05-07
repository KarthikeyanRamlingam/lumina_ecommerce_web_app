from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product, Category, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, UserSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.all()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            qs = qs.filter(category__slug=category)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=400)

    user = User.objects.create_user(
        username=username, email=email, password=password,
        first_name=first_name, last_name=last_name
    )
    login(request, user)
    return Response(UserSerializer(user).data, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response(UserSerializer(user).data)
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({'message': 'Logged out'})

@api_view(['GET'])
def current_user(request):
    if request.user.is_authenticated:
        return Response(UserSerializer(request.user).data)
    return Response({'error': 'Not authenticated'}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    items = request.data.get('items', [])
    shipping_address = request.data.get('shipping_address', '')

    if not items:
        return Response({'error': 'No items in order'}, status=400)
    if not shipping_address:
        return Response({'error': 'Shipping address required'}, status=400)

    order = Order.objects.create(
        user=request.user,
        shipping_address=shipping_address,
        total_price=0
    )

    total = 0
    for item in items:
        try:
            product = Product.objects.get(id=item['product_id'])
            qty = item['quantity']
            if product.stock < qty:
                order.delete()
                return Response({'error': f'Insufficient stock for {product.name}'}, status=400)
            OrderItem.objects.create(order=order, product=product, quantity=qty, price=product.price)
            product.stock -= qty
            product.save()
            total += product.price * qty
        except Product.DoesNotExist:
            order.delete()
            return Response({'error': f"Product {item['product_id']} not found"}, status=400)

    order.total_price = total
    order.save()
    return Response(OrderSerializer(order).data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return Response(OrderSerializer(orders, many=True).data)
