from django.shortcuts import render, get_object_or_404, redirect
from .models import Game

def game_list(request):
    query = request.GET.get('q', '').strip()
    selected_genres = request.GET.getlist('genres')

    games = Game.objects.all()
    if query:
        games = games.filter(title__icontains=query)

    if selected_genres:
        games = games.filter(genre__in=selected_genres)

    genres = (
        Game.objects.order_by('genre')
        .values_list('genre', flat=True)
        .distinct()
    )

    context = {
        'games': games,
        'query': query,
        'genres': genres,
        'selected_genres': selected_genres,
    }

    return render(request, 'games/game_list.html', context)


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)

    # Схожі ігри
    recommended = Game.objects.filter(
        genre=game.genre
    ).exclude(id=game.id)[:4]

    return render(request, 'games/game_detail.html', {
        'game': game,
        'recommended': recommended
    })


# ---------- Cart (session-based) ----------
def _get_cart(session):
    cart = session.get('cart')
    if not isinstance(cart, dict):
        cart = {}
    return cart


def cart_add(request, pk):
    # Add item to cart (increments quantity)
    game = get_object_or_404(Game, pk=pk)
    cart = _get_cart(request.session)
    key = str(game.pk)
    cart[key] = int(cart.get(key, 0)) + 1
    request.session['cart'] = cart
    # optional message framework could be used here
    next_url = request.POST.get('next') or request.GET.get('next') or 'cart'
    return redirect(next_url)


def cart_remove(request, pk):
    # Remove item completely from cart
    cart = _get_cart(request.session)
    key = str(pk)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
    next_url = request.POST.get('next') or request.GET.get('next') or 'cart'
    return redirect(next_url)


def cart_clear(request):
    request.session['cart'] = {}
    next_url = request.POST.get('next') or request.GET.get('next') or 'cart'
    return redirect(next_url)


def cart_view(request):
    cart = _get_cart(request.session)
    ids = [int(i) for i in cart.keys()]
    games_qs = Game.objects.filter(id__in=ids)
    game_map = {g.id: g for g in games_qs}
    items = []
    total = 0
    for sid, qty in cart.items():
        try:
            gid = int(sid)
            game = game_map.get(gid)
            if not game:
                continue
            qty = int(qty)
            subtotal = (game.price or 0) * qty
            total += subtotal
            items.append({
                'game': game,
                'qty': qty,
                'subtotal': subtotal,
            })
        except Exception:
            continue
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'games/cart.html', context)
