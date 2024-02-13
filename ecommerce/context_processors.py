from .models import Cart, CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            total = sum(item.quantity for item in cart_items)
            return {"cart_item_count": total}
        except Cart.DoesNotExist:
            return {"cart_item_count": 0}
    return {"cart_item_count": 0}