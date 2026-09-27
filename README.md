# MusafirCafe

Welcome to **MusafirCafe**, a Django-based web application for managing restaurant orders, menus, shopping carts, and order tracking.

## 12. Overall Architecture We'll Build

The finished project could look like:

```
MusafirCafe/
│
├── manage.py
│
├── MusafirCafe/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── main/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── services.py
│
├── template/
│   ├── base.html
│   ├── index.html
│   ├── menu.html
│   ├── about.html
│   ├── services.html
│   ├── contact.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_success.html
│   ├── order_status.html
│   └── admin_dashboard.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── db.sqlite3
```

And eventually:

```
                    ┌──────────────┐
                    │   Customer   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │     Menu     │
                    └──────┬───────┘
                           │
                       Add items
                           │
                           ▼
                    ┌──────────────┐
                    │     Cart     │
                    └──────┬───────┘
                           │
                    Add-ons / BOGO
                           │
                           ▼
                    ┌──────────────┐
                    │   Checkout   │
                    └──────┬───────┘
                           │
                  Payment method
                           │
                           ▼
                    ┌──────────────┐
                    │    Order     │
                    └──────┬───────┘
                           │
                           ▼
              ┌────────────────────────┐
              │ Restaurant Admin/Kitchen│
              └───────────┬────────────┘
                          │
                  Update order status
                          │
                          ▼
                  Customer tracking
```
