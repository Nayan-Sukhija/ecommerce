from django.db import models
from userlogin.models import UserProfile

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    for_women = models.BooleanField()
    for_men = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    main_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img_count = models.PositiveIntegerField(default=1)
    active_flag = models.BooleanField(default=True)
    size_xs = models.BooleanField(default=True)
    size_s = models.BooleanField(default=True)
    size_m = models.BooleanField(default=True)
    size_l = models.BooleanField(default=True)
    size_xl = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_image_range(self):
        return range(self.img_count)


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    address = models.TextField()
    order_no = models.IntegerField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # 0 -- ordered | 1 -- Packed and shipped | 2 -- Delivered
    status = models.IntegerField() 
    address = models.TextField()

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=25, null=True)
    price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product} in Order #{self.order.id}"
    
class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user}"
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=25, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product} in Cart for {self.cart.user}"
