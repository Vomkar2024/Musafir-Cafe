from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122, default="")
    email = models.EmailField(default="")
    phone = models.CharField(max_length=20, default="")
    message = models.TextField(default="")
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('drink', 'Drink'),
        ('dessert', 'Dessert'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='food'
    )
    image = models.ImageField(
        upload_to='menu/',
        blank=True,
        null=True
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Addon(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('dine_in', 'Dine In'),
        ('takeaway', 'Takeaway'),
        ('delivery', 'Delivery'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('gpay', 'GPay'),
        ('card', 'Debit/Credit Card'),
        ('cash', 'Cash'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='dine_in')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    addon_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cod_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')
    token_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    estimated_wait_minutes = models.IntegerField(default=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.token_number:
            self.token_number = f"A{100 + self.id}"
            super().save(update_fields=['token_number'])

    @property
    def next_status(self):
        flow = ['placed', 'confirmed', 'preparing', 'ready', 'completed']
        if self.status in flow:
            idx = flow.index(self.status)
            if idx < len(flow) - 1:
                return flow[idx + 1]
        return None

    @property
    def estimated_wait_display(self):
        if self.status == 'completed':
            return "Completed"
        elif self.status == 'cancelled':
            return "Cancelled"
        elif self.status == 'ready':
            return "Ready Now!"
        elif self.estimated_wait_minutes <= 0:
            return "Ready Soon"
        return f"{self.estimated_wait_minutes} minutes"

    def __str__(self):
        return f"Order #{self.token_number or self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name if self.menu_item else 'Unknown'}"

class OrderItemAddon(models.Model):
    order_item = models.ForeignKey(OrderItem, related_name='addons', on_delete=models.CASCADE)
    addon = models.ForeignKey(Addon, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.addon.name if self.addon else 'Unknown'}"

class Cart(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    addon_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cod_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_totals(self, payment_method='cash'):
        from decimal import Decimal
        subtotal = Decimal('0.00')
        addon_total = Decimal('0.00')
        unit_prices = []
        
        for item in self.items.all():
            item_price = item.menu_item.price
            subtotal += item_price * item.quantity
            for _ in range(item.quantity):
                unit_prices.append(item_price)
            
            for item_addon in item.addons.all():
                addon_total += item_addon.addon.price * item_addon.quantity

        total_quantity = len(unit_prices)
        if total_quantity > 5:
            unit_prices.sort(reverse=True)
            # Cart-wide pairwise BOGO: every 2nd item (index 1, 3, 5...) is free
            discount = sum(unit_prices[i] for i in range(1, total_quantity, 2))
        else:
            discount = Decimal('0.00')

        cod_charge = Decimal('20.00') if payment_method == 'cash' else Decimal('0.00')

        total = subtotal + addon_total + cod_charge - discount

        self.subtotal = subtotal
        self.addon_total = addon_total
        self.discount = discount
        self.cod_charge = cod_charge
        self.total = total
        self.save()

        return {
            'subtotal': subtotal,
            'addon_total': addon_total,
            'discount': discount,
            'cod_charge': cod_charge,
            'total': total,
        }

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"

class CartItemAddon(models.Model):
    cart_item = models.ForeignKey(CartItem, related_name='addons', on_delete=models.CASCADE)
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.addon.name}"
