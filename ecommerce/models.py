from django.utils.translation import gettext_lazy as _
from django.db import models
import shortuuid
from users.models import CustomUser as User


class Category(models.Model):
    id = models.CharField(
        default=shortuuid.uuid,max_length=50, primary_key=True, editable=False
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
        default=shortuuid.uuid, max_length=50,primary_key=True, editable=False
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
        default=shortuuid.uuid,max_length=50, primary_key=True, editable=False
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
