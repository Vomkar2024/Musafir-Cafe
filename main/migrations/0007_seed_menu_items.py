from django.db import migrations


def seed_menu_items(apps, schema_editor):
    MenuItem = apps.get_model('main', 'MenuItem')
    items = [
        {
            'name': 'Classic Cheese Pizza',
            'price': 99.00,
            'category': 'food',
            'description': 'Oven-baked pizza topped with rich tomato sauce and melted golden mozzarella. 🍕'
        },
        {
            'name': 'Creamy Herb Pasta',
            'price': 89.00,
            'category': 'food',
            'description': 'Delicious penne tossed in a creamy garlic white sauce with fresh herbs. 🍝'
        },
        {
            'name': 'Musafir Signature Burger',
            'price': 79.00,
            'category': 'food',
            'description': 'Juicy patty served in a toasted bun with crisp lettuce, cheese & secret sauce. 🍔'
        },
        {
            'name': 'Artisanal Cold Brew Coffee',
            'price': 69.00,
            'category': 'drink',
            'description': 'Freshly brewed Arabica beans chilled to perfection with a bold smooth profile. ☕'
        },
        {
            'name': 'Garden Harvest Salad',
            'price': 59.00,
            'category': 'food',
            'description': 'A refreshing blend of crisp greens, cherry tomatoes, olives & house vinaigrette. 🥗'
        },
        {
            'name': 'Special Musafir Cafe Combo',
            'price': 150.00,
            'category': 'food',
            'description': 'Special combo meal featuring Burger, Crispy Fries & Cold Brew Coffee! 🍔🍟☕'
        },
    ]
    for item in items:
        MenuItem.objects.update_or_create(
            name=item['name'],
            defaults={
                'price': item['price'],
                'category': item['category'],
                'description': item['description'],
                'is_available': True
            }
        )


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_contact_options_alter_menuitem_options_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_menu_items, reverse_func),
    ]
