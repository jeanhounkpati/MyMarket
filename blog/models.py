from django.db import models
from django.contrib.auth.models import User

class Plat(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique = True)
    description = models.TextField()
    image = models.ImageField(upload_to="plats")
    selling_price = models.PositiveIntegerField()

def __str__(self):
    return self.title


class Customer(models.Model):
    
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    full_name = models.CharField(max_length=200)
    address= models.CharField(max_length=200,null=True,blank =True)
    joined_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.full_name



class Admin(models.Model):
    
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    full_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    image = models.ImageField(upload_to="admin")

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    customer = models.ForeignKey( Customer , on_delete = models.SET_NULL,null =True,blank=True )
    total = models.PositiveIntegerField(default = 0)
    createdat = models.DateTimeField(auto_now_add = True)

def __str__(self):
    return 'Cart:' + str(self.id)
     

class CartPlat(models.Model):
    cart = models.ForeignKey( Cart ,on_delete = models.CASCADE)
    plat = models.ForeignKey( Plat ,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    rate = models.PositiveIntegerField()

def __str__(self):
    return 'Cart:' + str(self.cart.id) + 'CartPlat:' +str(self.id)
 
ORDER_STATUS = (
    ("Order Received","Order Received"),
    ("Order processing","Order processing"),
    ("On the way","On the way"),
    ("Order Completed","Order Completed"),
    ("Order Canceled","Order Canceled"),
    
)
    





class Order(models.Model):
    cart =models.OneToOneField(Cart,on_delete = models.CASCADE) 
    ordered_by =models.CharField(max_length=255)
    shipping_address =models.CharField(max_length=255)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null = True,blank = True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50,choices = ORDER_STATUS)
    createdat = models.DateTimeField(auto_now_add = True)

def __str__(self):
    return 'Order:' + str(self.id)



