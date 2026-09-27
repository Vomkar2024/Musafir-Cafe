from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from .models import Contact, MenuItem, Order, OrderItem, Addon
from django.contrib import messages


def index(request):
    context = {
        "title": "Main"
    }
    return render(request, 'index.html', context)


def Menu(request):
    menu_items = MenuItem.objects.filter(
        is_available=True
    ).order_by('category', 'name')

    return render(
        request,
        'menu.html',
        {
            'menu_items': menu_items
        }
    )


def about(request):
    return render(request, 'About.html')


def services(request):
    return render(request, 'Services.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        contact_obj = Contact(name=name, email=email, phone=phone, message=message, date=datetime.today())
        contact_obj.save()

        messages.success(request, "We have received your message😊")
        
    return render(request, 'Contact.html')


def order_tracking(request, token=None):
    if not token:
        token = request.GET.get('token')

    order = None
    if token:
        token_str = token.strip()
        if token_str.startswith('#'):
            token_str = token_str[1:]
            
        order = Order.objects.filter(token_number__iexact=token_str).first()
        if not order and token_str.isdigit():
            order = Order.objects.filter(id=int(token_str)).first()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        if order:
            return JsonResponse({
                'success': True,
                'token_number': order.token_number,
                'customer_name': order.customer_name,
                'status': order.status,
                'status_display': order.get_status_display().upper(),
                'estimated_wait_display': order.estimated_wait_display,
                'estimated_wait_minutes': order.estimated_wait_minutes,
                'order_type_display': order.get_order_type_display(),
                'total': str(order.total),
            })
        else:
            return JsonResponse({'success': False, 'error': 'Order not found'}, status=404)

    return render(request, 'order_status.html', {
        'order': order,
        'search_token': token or ''
    })


def order_lookup(request):
    if request.method == 'POST':
        token = request.POST.get('token', '').strip()
        if token:
            return redirect('order_tracking', token=token)
    return redirect('order_tracking_home')


def kitchen_dashboard(request):
    orders = Order.objects.all().order_by('-created_at')
    
    # Simple count summary
    active_orders = orders.exclude(status__in=['completed', 'cancelled'])
    placed_count = orders.filter(status='placed').count()
    confirmed_count = orders.filter(status='confirmed').count()
    preparing_count = orders.filter(status='preparing').count()
    ready_count = orders.filter(status='ready').count()
    completed_count = orders.filter(status='completed').count()

    return render(request, 'kitchen_dashboard.html', {
        'orders': orders,
        'active_orders': active_orders,
        'placed_count': placed_count,
        'confirmed_count': confirmed_count,
        'preparing_count': preparing_count,
        'ready_count': ready_count,
        'completed_count': completed_count,
        'status_choices': Order.STATUS_CHOICES,
    })


def update_order_status(request, token):
    if request.method == 'POST':
        order = None
        if token.isdigit():
            order = Order.objects.filter(id=int(token)).first()
        if not order:
            order = get_object_or_404(Order, token_number__iexact=token)

        new_status = request.POST.get('status')
        wait_minutes = request.POST.get('estimated_wait_minutes')

        if new_status and new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
        
        if wait_minutes is not None and wait_minutes.isdigit():
            order.estimated_wait_minutes = int(wait_minutes)
            
        order.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
            return JsonResponse({
                'success': True,
                'token_number': order.token_number,
                'status': order.status,
                'status_display': order.get_status_display().upper(),
                'estimated_wait_display': order.estimated_wait_display,
                'estimated_wait_minutes': order.estimated_wait_minutes,
            })

        messages.success(request, f"Order #{order.token_number} status updated to {order.get_status_display().upper()}.")
        return redirect('kitchen_dashboard')

    return redirect('kitchen_dashboard')


def place_order(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', 'Guest Customer')
        customer_phone = request.POST.get('customer_phone', '')
        customer_email = request.POST.get('customer_email', '')
        order_type = request.POST.get('order_type', 'dine_in')
        payment_method = request.POST.get('payment_method', 'cash')
        wait_minutes = request.POST.get('estimated_wait_minutes', 15)

        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            order_type=order_type,
            payment_method=payment_method,
            status='placed',
            estimated_wait_minutes=int(wait_minutes) if str(wait_minutes).isdigit() else 15
        )

        # Process selected menu item if any
        menu_item_id = request.POST.get('menu_item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        total = 0.0
        if menu_item_id:
            menu_item = MenuItem.objects.filter(id=menu_item_id).first()
            if menu_item:
                unit_price = menu_item.price
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    unit_price=unit_price
                )
                total = float(unit_price) * quantity

        # If no item selected or total is 0, add demo items if present or fallback
        if total == 0:
            sample_items = MenuItem.objects.filter(is_available=True)[:2]
            for item in sample_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=1,
                    unit_price=item.price
                )
                total += float(item.price)

        order.subtotal = total
        order.total = total
        order.save()

        messages.success(request, f"Order #{order.token_number} placed successfully!")
        return redirect('order_tracking', token=order.token_number)

    menu_items = MenuItem.objects.filter(is_available=True)
    return render(request, 'place_order.html', {'menu_items': menu_items})


