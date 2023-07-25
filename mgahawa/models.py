from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class MainModel(models.Model):
    is_active = models.BooleanField(null=True, blank=True, default=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def softdelete(self):
        self.is_deleted = True
        self.is_active = False
        self.updated = pendulum.now()
        self.save()

    class Meta:
        abstract = True


class UserProfile(MainModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="profile")
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d',null=True, blank=True)

    def __str__(self):

        return self.user.email
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Restaurant(MainModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):

        return self.code

class Category(MainModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):

        return self.code

class FoodItems(MainModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d',null=True, blank=True)

    def __str__(self):

        return self.price

STATUS = (
    (1, 'pending'),
    (2, 'confirmed'),
    (3, 'delivered'),
    (4, 'rejected')
)

class Order(MainModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=10, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, null=True, blank=True)

    def __str__(self):

        return self.order_number


class OrderItem(MainModel):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(FoodItems, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):

        return self.order.id
    
