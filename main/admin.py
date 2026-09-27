from django.contrib import admin
from .models import Contact, MenuItem, Addon, Order, OrderItem, OrderItemAddon, Cart, CartItem, CartItemAddon


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'is_available',
        'created_at',
    )

    list_filter = (
        'category',
        'is_available',
    )

    search_fields = (
        'name',
        'description',
    )


@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'token_number',
        'customer_name',
        'customer_phone',
        'order_type',
        'status',
        'estimated_wait_minutes',
        'payment_method',
        'payment_status',
        'total',
        'created_at',
    )
    list_filter = ('status', 'order_type', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('token_number', 'customer_name', 'customer_phone', 'customer_email')
    inlines = [OrderItemInline]
    list_editable = ('status', 'estimated_wait_minutes')
    actions = ['mark_as_confirmed', 'mark_as_preparing', 'mark_as_ready', 'mark_as_completed']

    @admin.action(description="Mark selected orders as Confirmed")
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description="Mark selected orders as Preparing")
    def mark_as_preparing(self, request, queryset):
        queryset.update(status='preparing')

    @admin.action(description="Mark selected orders as Ready")
    def mark_as_ready(self, request, queryset):
        queryset.update(status='ready')

    @admin.action(description="Mark selected orders as Completed")
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'date',
    )
    search_fields = ('name', 'email', 'phone', 'message')
    list_filter = ('date',)
    date_hierarchy = 'date'


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'subtotal', 'total', 'created_at')
    search_fields = ('session_key', 'user__username')
    inlines = [CartItemInline]


