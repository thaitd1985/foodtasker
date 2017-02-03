from rest_framework import serializers

from foodtaskerapp.models import Restaurant, Meal, Customer, Driver, Order, OrderDetails
from foodtaskerapp.haystackserializers import SearchResultSetSerializerMixin

class RestaurantSerializer(serializers.ModelSerializer, SearchResultSetSerializerMixin):
    logo = serializers.SerializerMethodField()

    def get_logo(self, restaurant):
        request = self.context.get('request')
        log_url = restaurant.logo.url
        return request.build_absolute_uri(log_url)

    class Meta:
        model = Restaurant
        fields = ("id", "name", "phone", "address", "logo")

class RestaurantSearchSerializer(serializers.ModelSerializer, SearchResultSetSerializerMixin):

    logo = serializers.SerializerMethodField()

    def get_logo(self, restaurant):
        request = self.context.get('request')
        log_url = restaurant.logo
        return request.build_absolute_uri(log_url)

    id = serializers.SerializerMethodField()

    def get_id(self, restaurant):
        return restaurant.pk
    class Meta:
        model = Restaurant
        fields = ("id", "name", "phone", "address", "logo")

class MealSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, meal):
        request = self.context.get('request')
        image_url = meal.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Meal
        fields = ("id", "name", "short_description", "image", "price")

# ORDER SERIALIZERS
class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source = "user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id", "name", "avatar", "phone", "address")

class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source = "user.get_full_name")

    class Meta:
        model = Driver
        fields = ("id", "name", "avatar", "phone", "address")

class OrderRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "phone", "address")

class OrderMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ("id", "name", "price")

class OrderDetailsSerializer(serializers.ModelSerializer):
    meal = OrderMealSerializer()
    class Meta:
        model = OrderDetails
        fields = ("id", "meal", "quantity", "sub_total")

class OrderSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    driver = OrderDriverSerializer()
    restaurant = OrderRestaurantSerializer()
    order_details = OrderDetailsSerializer(many = True)
    status = serializers.ReadOnlyField(source = "get_status_display")

    class Meta:
        model = Order
        fields = ("id", "customer", "restaurant", "driver", "order_details", "total", "status", "address")
