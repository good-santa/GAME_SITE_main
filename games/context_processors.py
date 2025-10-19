def cart(request):
    cart = request.session.get('cart') or {}
    try:
        count = sum(int(q) for q in cart.values()) if isinstance(cart, dict) else 0
    except Exception:
        count = 0
    return {
        'cart_count': count,
    }

