from django.utils.translation import gettext_lazy as _
from django.db import models
import shortuuid
from users.models import CustomUser as User


class Category(models.Model):
    id = models.CharField(
        default=shortuuid.uuid, max_length=50, primary_key=True, editable=False
    )
    category_name = models.CharField(
        _("Category Name"), max_length=100, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return str(f"{self.category_name}")


class Product(models.Model):
    id = models.CharField(
        default=shortuuid.uuid, max_length=50, primary_key=True, editable=False
    )
    product_name = models.CharField(
        _("Product Name"), max_length=500, null=True, blank=True
    )
    description = models.TextField(_("Description"), null=True, blank=True)
    price = models.FloatField(_("Price"), null=True, blank=True)
    image = models.ImageField(
        _("Product Image"),
        upload_to="products/",
        default="products/default.jpg",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self) -> str:
        return str(f"{self.product_name}")


class Review(models.Model):
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    id = models.CharField(
        default=shortuuid.uuid, max_length=50, primary_key=True, editable=False
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    id = models.CharField(
        default=shortuuid.uuid, max_length=50, primary_key=True, editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.full_name + " cart")


class CartItem(models.Model):
    id = models.CharField(
        default=shortuuid.uuid, max_length=50, primary_key=True, editable=False
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    id = models.CharField(
        default=shortuuid.uuid, max_length=50, primary_key=True, editable=False
    )
    STATUS_INITIATED = "initiated"
    STATUS_PROCESSING = "processing"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = (
        (STATUS_INITIATED, "Initiated"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILED, "Failed"),
    )
    order = models.OneToOneField("Order", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pidx = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=STATUS_INITIATED
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pidx


class Order(models.Model):
    id = models.CharField(
        default=shortuuid.uuid, max_length=50, primary_key=True, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.full_name + " order")


class OrderItem(models.Model):
    id = models.CharField(
        default=shortuuid.uuid, max_length=50, primary_key=True, editable=False
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(f"{self.order.user.full_name} order for {self.product.product_name}")


class BillingAddress(models.Model):
    id = models.CharField(
        default=shortuuid.uuid, max_length=50, primary_key=True, editable=False
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"