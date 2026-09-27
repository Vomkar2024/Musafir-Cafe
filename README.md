# MusafirCafe — Restaurant Management & Live Order Tracking System

Welcome to **MusafirCafe**, a full-stack Django web application designed for digital cafe and restaurant operations. MusafirCafe provides an end-to-end workflow covering customer menu browsing, online order placement, dynamic cart calculation with promotional discounts, live token-based order tracking, a real-time Kitchen Display System (KDS), and a custom admin portal.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [System Architecture & Data Flow](#-system-architecture--data-flow)
4. [Directory & File Structure](#-directory--file-structure)
5. [Complete Step-by-Step Implementation Walkthrough](#-complete-step-by-step-implementation-walkthrough)
   - [Step 1: Project Initialization & Configuration](#step-1-project-initialization--configuration)
   - [Step 2: Database Schema & Relational Models](#step-2-database-schema--relational-models)
   - [Step 3: URL Routing & Routing Architecture](#step-3-url-routing--routing-architecture)
   - [Step 4: Business Logic & View Controllers](#step-4-business-logic--view-controllers)
   - [Step 5: Frontend Templates & Real-Time Auto-Polling](#step-5-frontend-templates--real-time-auto-polling)
   - [Step 6: Customized Django Admin Portal](#step-6-customized-django-admin-portal)
   - [Step 7: Automated Unit Testing & QA](#step-7-automated-unit-testing--qa)
6. [Getting Started & Local Setup](#-getting-started--local-setup)
7. [Running Tests](#-running-tests)

---

## 🎯 Project Overview

**MusafirCafe** streamlines cafe ordering by eliminating physical queues and giving customers live updates on their food preparation status. Kitchen staff can manage incoming orders via a dedicated Kitchen Dashboard (KDS), updating statuses in real-time, while customers track their token progress on mobile or desktop screens with auto-refreshing status updates.

---

## ✨ Key Features

- 🍔 **Interactive Digital Menu**: Browse items organized by categories (*Food*, *Drink*) with availability toggles and pricing.
- 🛒 **Smart Cart & Calculation Engine**: Supports item add-ons, payment method adjustments (e.g. Cash on Delivery charge), and automated **Pairwise Buy-One-Get-One (BOGO)** discount calculation for orders over 5 items.
- 🎟️ **Automated Token Generation**: Auto-assigns unique order tracking tokens (e.g., `A101`, `A102`, `A103`) upon order placement based on database sequence.
- ⏱️ **Live Order Tracking Ticket**: Visual progress bar (`Placed` ➔ `Confirmed` ➔ `Preparing` ➔ `Ready` ➔ `Completed`) with dynamic wait time estimation.
- 🔄 **Real-Time Auto-Polling API**: Frontend asynchronous polling via JSON API endpoints (`?format=json`) updates status and time estimates without page reloads.
- 🍳 **Kitchen Display System (KDS)**: Kitchen staff dashboard displaying active orders, total counts per stage, and status control buttons.
- 🛡️ **Custom Django Admin Portal**: Custom header branding, inline item details, searchable filterable lists, and bulk status update actions.
- 💬 **Customer Feedback System**: Contact form with instant feedback message notifications.
- 🧪 **Comprehensive Unit Test Suite**: Verification of token generation, state machine transitions, template output, and API responses.

---

## 🏗️ System Architecture & Data Flow

```
                      ┌───────────────────────┐
                      │   Customer Frontend   │
                      └───────────┬───────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
  │ View Menu    │         │ Place Order  │         │ Track Ticket │
  └──────────────┘         └──────┬───────┘         └──────┬───────┘
                                  │                        │
                                  ▼                        │
                           ┌──────────────┐                │ (Auto-Polls JSON API)
                           │ Order Created│                │
                           │(Token: A101) │                │
                           └──────┬───────┘                │
                                  │                        │
                                  ▼                        ▼
                      ┌───────────────────────┐   ┌─────────────────┐
                      │ Kitchen Display (KDS) │──►│ Status Updates  │
                      └───────────────────────┘   └─────────────────┘
                                  │
                                  ▼
                      ┌───────────────────────┐
                      │ Django Admin Portal   │
                      └───────────────────────┘
```

---

## 📁 Directory & File Structure

```
Musafir-Cafe/
│
├── manage.py                   # Django command-line execution script
├── db.sqlite3                  # SQLite database file
│
├── MusafirCafe/                # Project Configuration Directory
│   ├── __init__.py
│   ├── asgi.py                 # ASGI configuration for async deployment
│   ├── wsgi.py                 # WSGI configuration for production deployment
│   ├── settings.py             # Core settings (apps, templates, static, DB)
│   └── urls.py                 # Root URL routing configuration
│
├── main/                       # Primary Application Directory
│   ├── __init__.py
│   ├── admin.py                # Customized Django Admin interfaces & actions
│   ├── apps.py                 # App configuration
│   ├── models.py               # ORM Models (MenuItem, Order, Cart, Addon, etc.)
│   ├── views.py                # Request handlers & JSON API endpoints
│   ├── urls.py                 # Application URL patterns
│   ├── tests.py                # Automated unit test suite
│   └── migrations/             # Database migration files
│
├── template/                   # HTML5 Templates (Jinja2 / Django Templates)
│   ├── base.html               # Master layout template (header, footer, nav)
│   ├── index.html              # Landing page
│   ├── menu.html               # Digital menu grid page
│   ├── place_order.html        # Customer checkout & ordering form
│   ├── order_status.html       # Dynamic order tracking ticket with JS auto-polling
│   ├── kitchen_dashboard.html  # Staff Kitchen Display System (KDS)
│   ├── contact.html            # Contact form page
│   ├── about.html              # About page
│   └── services.html           # Services summary page
│
└── static/                     # Static Assets
    ├── css/                    # Custom styling & stylesheets
    ├── js/                     # Custom JavaScript logic
    └── images/                 # Media & graphic assets
```

---

## 📖 Complete Step-by-Step Implementation Walkthrough

### Step 1: Project Initialization & Configuration

1. **Creating Project & App Structure**:
   - Initialized Django project named `MusafirCafe` and app named `main`.
2. **Configuring [`MusafirCafe/settings.py`](file:///e:/Download/College/Rubicon/Rubicon/MMS/Musafir-Cafe/MusafirCafe/settings.py)**:
   - **Installed Apps**: Added `main.apps.MainConfig` to `INSTALLED_APPS`.
   - **Templates Directory**: Updated `TEMPLATES` configuration to register `BASE_DIR / 'template'`.
   - **Static Files**: Added `STATICFILES_DIRS = [BASE_DIR / "static"]` and defined `STATIC_URL = 'static/'`.
   - **Database**: Configured default SQLite3 database (`db.sqlite3`).
   - **Email Backend**: Set `console.EmailBackend` for development notifications.

---

### Step 2: Database Schema & Relational Models

In [`main/models.py`](file:///e:/Download/College/Rubicon/Rubicon/MMS/Musafir-Cafe/main/models.py), nine relational models were created to store core domain data:

#### 1. `Contact` Model
Stores user messages submitted via the contact form:
- `name`, `email`, `phone`, `message`, and `date` (auto-generated timestamp).

#### 2. `MenuItem` Model
Represents items available on the cafe menu:
- `name`, `description`, `price`, `category` (choices: `food`, `drink`), `image`, `is_available` toggle, and `created_at`.

#### 3. `Addon` Model
Represents extra add-ons (e.g. Extra Cheese, Whipped Cream):
- `name`, `price`, `is_available`.

#### 4. `Order` Model
Central model representing customer orders:
- **Customer Info**: `customer_name`, `customer_phone`, `customer_email`.
- **Order Metadata**: `order_type` (`dine_in`, `takeaway`, `delivery`), `payment_method` (`gpay`, `card`, `cash`), `payment_status` (`pending`, `paid`, `failed`).
- **Financial Breakdown**: `subtotal`, `addon_total`, `discount`, `cod_charge`, `total`.
- **Status State Machine**: Choices: `placed`, `confirmed`, `preparing`, `ready`, `completed`, `cancelled`.
- **Token Assignment**: `token_number` field formatted as `A100 + id` (e.g., `A101`, `A102`). Overrides `save()` to auto-generate unique tokens upon order creation.
- **Helper Properties**:
  - `next_status`: Computes the next valid state transition step in the sequence `placed ➔ confirmed ➔ preparing ➔ ready ➔ completed`.
  - `estimated_wait_display`: Formats human-readable output (e.g., `"15 minutes"`, `"Ready Now!"`, `"Completed"`).

#### 5. `OrderItem` & `OrderItemAddon` Models
- `OrderItem`: Connects an `Order` to a `MenuItem` with `quantity` and frozen `unit_price`.
- `OrderItemAddon`: Connects an `OrderItem` to an `Addon` with `quantity` and price.

#### 6. `Cart`, `CartItem`, & `CartItemAddon` Models
- Supports cart sessions before order checkout.
- **Pairwise BOGO Discount Engine** in `Cart.calculate_totals()`:
  - If total items in cart > 5, sorts unit prices in descending order and provides every second item free (`sum(unit_prices[1::2])`).
  - Adds a ₹20 Cash on Delivery (`cod_charge`) if `payment_method == 'cash'`.

---

### Step 3: URL Routing & Routing Architecture

1. **Root URL Routing ([`MusafirCafe/urls.py`](file:///e:/Download/College/Rubicon/Rubicon/MMS/Musafir-Cafe/MusafirCafe/urls.py))**:
   - Directs `/admin/` to Django admin.
   - Delegates all root paths `''` to `main.urls`.

2. **Application URL Routing ([`main/urls.py`](file:///e:/Download/College/Rubicon/Rubicon/MMS/Musafir-Cafe/main/urls.py))**:
   ```python
   urlpatterns = [
       path("", views.index, name="main"),
       path("menu", views.Menu, name="menu"),
       path("about", views.about, name="about"),
       path("services", views.services, name="services"),
       path("contact", views.contact, name="contact"),
       path("order/", views.order_tracking, name="order_tracking_home"),
       path("order/lookup/", views.order_lookup, name="order_lookup"),
       path("order/<str:token>/", views.order_tracking, name="order_tracking"),
       path("order/<str:token>/update-status/", views.update_order_status, name="update_order_status"),
       path("kitchen/", views.kitchen_dashboard, name="kitchen_dashboard"),
       path("place-order/", views.place_order, name="place_order"),
   ]
   ```

---

### Step 4: Business Logic & View Controllers

Implemented in [`main/views.py`](file:///e:/Download/College/Rubicon/Rubicon/MMS/Musafir-Cafe/main/views.py):

- **`index(request)`**: Renders homepage.
- **`Menu(request)`**: Fetches all available menu items filtered by `is_available=True` sorted by category and name.
- **`contact(request)`**: Processes POST requests to save `Contact` submissions and sends a success flash message (`messages.success`).
- **`order_tracking(request, token=None)`**:
  - Handles token queries (e.g., `A101` or ID `1`).
  - Supports **Dual Response**: If requested via AJAX (`X-Requested-With` or `?format=json`), returns JSON payload containing token status, wait display, and total. Otherwise, renders `order_status.html`.
- **`order_lookup(request)`**: Processes search form input and redirects to `/order/<token>/`.
- **`kitchen_dashboard(request)`**: Renders kitchen staff interface with counts for `placed`, `confirmed`, `preparing`, `ready`, and `completed` orders.
- **`update_order_status(request, token)`**: Updates an order's preparation status and estimated wait time, supporting both form redirects and JSON responses for asynchronous kitchen actions.
- **`place_order(request)`**: Form handler for ordering food items. Creates `Order` and `OrderItem` records and redirects the customer directly to their live tracking ticket.

---

### Step 5: Frontend Templates & Real-Time Auto-Polling

Templates stored in [`template/`](file:///e:/Download/College/Rubicon/Rubicon/MMS/Musafir-Cafe/template/):

1. **`base.html`**: Provides layout structure, navbar links (Home, Menu, Place Order, Kitchen KDS, Contact), flash alerts banner, and footer.
2. **`order_status.html`**:
   - Displays customer token card, active step indicator, status badge, estimated wait timer, order summary, and price breakdown.
   - **JavaScript Auto-Polling Script**: Automatically fetches `/order/<token>/?format=json` every 10 seconds:
     ```javascript
     setInterval(function() {
         fetch(window.location.pathname + '?format=json', {
             headers: { 'X-Requested-With': 'XMLHttpRequest' }
         })
         .then(response => response.json())
         .then(data => {
             if (data.success) {
                 // Update status badge, progress bar step, and wait time text dynamically
             }
         });
     }, 10000);
     ```
3. **`kitchen_dashboard.html`**: Staff portal featuring quick action buttons (`Confirm`, `Start Preparing`, `Mark Ready`, `Complete`) for managing orders in real time.

---

### Step 6: Customized Django Admin Portal

Configured in [`main/admin.py`](file:///e:/Download/College/Rubicon/Rubicon/MMS/Musafir-Cafe/main/admin.py):

- **Branding Titles**:
  - `site_header = "Musafir Cafe Admin"`
  - `site_title = "Musafir Cafe Admin Portal"`
- **`OrderAdmin`**:
  - Displays token, customer name, phone, type, status, estimated wait minutes, payment method, payment status, and total.
  - Inlines `OrderItemInline` to view order items directly inside the order form.
  - Enables direct list editing (`list_editable = ('status', 'estimated_wait_minutes')`).
  - **Custom Bulk Actions**: `mark_as_confirmed`, `mark_as_preparing`, `mark_as_ready`, and `mark_as_completed`.

---

### Step 7: Automated Unit Testing & QA

Unit tests written in [`main/tests.py`](file:///e:/Download/College/Rubicon/Rubicon/MMS/Musafir-Cafe/main/tests.py):

1. `test_token_generation`: Verifies that created orders auto-generate token strings like `A101`.
2. `test_status_workflow`: Exercises full state progression from `placed` ➔ `confirmed` ➔ `preparing` ➔ `ready` ➔ `completed`.
3. `test_customer_order_tracking_html`: Tests order tracking ticket page rendering.
4. `test_customer_order_tracking_json_api`: Verifies AJAX/JSON API status auto-polling responses.
5. `test_kitchen_dashboard_view`: Ensures kitchen dashboard displays active orders.

---

## 🚀 Getting Started & Local Setup

### Prerequisites
- Python 3.10+
- pip & venv

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Musafir-Cafe
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Django**:
   ```bash
   pip install django
   ```

4. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser (Admin Access)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open your browser at `http://127.0.0.1:8000/`.

---

## 🧪 Running Tests

To run the automated test suite and ensure all system components function correctly:

```bash
python manage.py test
```

Expected Output:
```text
Ran 5 tests in 0.102s

OK
```
