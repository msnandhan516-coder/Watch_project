from django.db import models
from datetime import date

orderchoice = (
    ("New Order", "New Order"),
    ("Processing", "Processing"),
    ("Shipped", "Shipped"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
)

CATEGORY_CHOICES = (
    ("Luxury", "Luxury"),
    ("Sport", "Sport"),
    ("Casual", "Casual"),
    ("Smart", "Smart"),
    ("Classic", "Classic"),
)


class signup(models.Model):
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    uname = models.CharField(max_length=30, null=True, blank=True, unique=True, default='user')
    pas = models.CharField(max_length=128)
    rights = models.CharField(max_length=10, default='U')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.uname or self.name


class watchstock(models.Model):
    wname = models.CharField("Watch Name", max_length=100, unique=True)
    brand = models.CharField(max_length=50, null=True, blank=True, default='')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Classic', null=True, blank=True)
    description = models.TextField(null=True, blank=True, default='')
    price = models.IntegerField()
    qty = models.IntegerField("Stock Quantity")
    photo = models.ImageField(upload_to='images/')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.wname


class watchcart(models.Model):
    slno = models.IntegerField()
    pname = models.CharField(max_length=100)
    rate = models.IntegerField()
    qty = models.IntegerField()
    total = models.IntegerField()
    userid = models.IntegerField()

    def __str__(self):
        return f"Cart #{self.id} - {self.pname}"


class watchsales(models.Model):
    salesno = models.IntegerField(unique=True)
    salesdate = models.DateField(default=date.today)
    userid = models.IntegerField()
    uname = models.CharField(max_length=100)
    shipment = models.CharField(max_length=500)
    phone = models.CharField(max_length=15)
    cardno = models.CharField(max_length=40)
    total = models.IntegerField()
    status = models.CharField(max_length=30, choices=orderchoice, default='New Order')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.salesno}"


class watchsalessub(models.Model):
    salesno = models.IntegerField()
    slno = models.IntegerField()
    pname = models.CharField(max_length=100)
    rate = models.IntegerField()
    qty = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return f"Sub #{self.id} - {self.pname}"
