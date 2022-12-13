from datetime import datetime
from msilib.schema import Class
from unicodedata import category
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, middle_name, last_name, contact, tc, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            contact=contact,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, middle_name, last_name, contact, tc,  password=None):
        """
        Creates and saves a superuser with the given email, name, tc and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            contact=contact,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#  Custom User Model


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email',max_length=255, unique=True,)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    profile = models.FileField(upload_to='images/profile/', null=True)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(null=True)
    removed_at = models.DateTimeField(null=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name', 'contact', 'tc']


    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin


    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserAddress(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=40, null=True)
    city = models.CharField(max_length=15, null=False)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'app_users_address'


class Userpayment(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    payment_type = models.CharField(max_length=10)
    provider = models.CharField(max_length=20)
    account_no = models.PositiveIntegerField(null=True, blank=True)
    expiry = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'app_users_payment'


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'product_category'


class ProductInventory(models.Model):
    quantity = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'product_inventory'


class ProductDiscount(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=15, decimal_places=2)
    active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'product_discount'


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    category_id = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    inventory_id = models.ForeignKey(
        ProductInventory, on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField(null=True)
    discount_id = models.ForeignKey(
        ProductDiscount, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateField(auto_now_add=True)
    image = models.FileField(upload_to='shop/images', null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    @property
    def outofstock(self):
        product = self.inventory_id.quantity
        if product != 0:
            outofstock = False
        elif product == 0:
            outofstock = True
        return outofstock

    @property
    def discount(self):
        total = (float(self.discount_id.discount_percent) * self.price)/100
        return total

    @property
    def discountsale_price(self):
        discountsale_price = "%.2f" % (float(self.price) - self.discount)
        return discountsale_price

    class Meta:
        db_table = 'product'


class cartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    qunatity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    @property
    def get_total(self):
        total = self.product.price * self.qunatity
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.qunatity for item in orderitems])
        return total

    class Meta:
        db_table = 'cart_items'


class PaymentDetails(models.Model):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    provider = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pk

    class Meta:
        db_table = 'payment_details'


class OrderDetails(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    payment_id = models.ForeignKey(
        PaymentDetails, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pk

    class Meta:
        db_table = 'order_details'


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    order_id = models.ForeignKey(
        OrderDetails, on_delete=models.SET_NULL, blank=True, null=True)
    qunatity = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pk

    class Meta:
        db_table = 'order_items'
