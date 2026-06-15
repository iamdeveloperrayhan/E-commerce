#!/usr/bin/env python
"""
Run with: python seed.py
Seeds Category, Product, and ProductVariant data.
Skips entries that already exist (idempotent).
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Category, Product, ProductVariant

CATEGORIES = [
    {'category_name': 'Electronics',  'slug': 'electronics'},
    {'category_name': 'Clothing',     'slug': 'clothing'},
    {'category_name': 'Books',        'slug': 'books'},
    {'category_name': 'Home & Garden','slug': 'home-garden'},
    {'category_name': 'Sports',       'slug': 'sports'},
]

PRODUCTS = [
    # Electronics
    {
        'product_name': 'Wireless Headphones',
        'category_slug': 'electronics',
        'slug': 'wireless-headphones',
        'description': 'Over-ear noise-cancelling wireless headphones with 30-hour battery life.',
        'price': '79.99',
        'variants': [
            {'color': 'Black', 'stock': 25},
            {'color': 'White', 'stock': 15},
        ],
    },
    {
        'product_name': 'Mechanical Keyboard',
        'category_slug': 'electronics',
        'slug': 'mechanical-keyboard',
        'description': 'Compact TKL mechanical keyboard with tactile brown switches and RGB backlight.',
        'price': '59.99',
        'variants': [
            {'color': 'Space Grey', 'stock': 20},
            {'color': 'White',      'stock': 10},
        ],
    },
    {
        'product_name': 'USB-C Hub',
        'category_slug': 'electronics',
        'slug': 'usb-c-hub',
        'description': '7-in-1 USB-C hub with HDMI, SD card reader, and 100W PD pass-through.',
        'price': '34.99',
        'variants': [
            {'color': 'Silver', 'stock': 40},
        ],
    },

    # Clothing
    {
        'product_name': 'Classic White T-Shirt',
        'category_slug': 'clothing',
        'slug': 'classic-white-tshirt',
        'description': '100% organic cotton crew-neck tee. Pre-shrunk. Machine washable.',
        'price': '19.99',
        'variants': [
            {'color': 'White', 'stock': 50},
            {'color': 'Grey',  'stock': 30},
        ],
    },
    {
        'product_name': 'Slim Fit Chinos',
        'category_slug': 'clothing',
        'slug': 'slim-fit-chinos',
        'description': 'Stretch-cotton slim fit chinos. Available in multiple colours.',
        'price': '44.99',
        'variants': [
            {'color': 'Navy',  'stock': 20},
            {'color': 'Khaki', 'stock': 25},
        ],
    },

    # Books
    {
        'product_name': 'Clean Code',
        'category_slug': 'books',
        'slug': 'clean-code',
        'description': 'A handbook of agile software craftsmanship by Robert C. Martin.',
        'price': '29.99',
        'variants': [
            {'color': 'Paperback', 'stock': 60},
        ],
    },
    {
        'product_name': 'The Pragmatic Programmer',
        'category_slug': 'books',
        'slug': 'pragmatic-programmer',
        'description': '20th anniversary edition. From journeyman to master.',
        'price': '34.99',
        'variants': [
            {'color': 'Paperback', 'stock': 45},
        ],
    },

    # Home & Garden
    {
        'product_name': 'Ceramic Plant Pot Set',
        'category_slug': 'home-garden',
        'slug': 'ceramic-plant-pot-set',
        'description': 'Set of 3 minimalist ceramic pots with drainage holes. Sizes: S, M, L.',
        'price': '24.99',
        'variants': [
            {'color': 'White', 'stock': 35},
            {'color': 'Terracotta', 'stock': 20},
        ],
    },

    # Sports
    {
        'product_name': 'Yoga Mat',
        'category_slug': 'sports',
        'slug': 'yoga-mat',
        'description': 'Non-slip 6mm thick TPE yoga mat with alignment lines. 183 × 61 cm.',
        'price': '27.99',
        'variants': [
            {'color': 'Purple', 'stock': 30},
            {'color': 'Blue',   'stock': 25},
            {'color': 'Black',  'stock': 20},
        ],
    },
    {
        'product_name': 'Resistance Band Set',
        'category_slug': 'sports',
        'slug': 'resistance-band-set',
        'description': 'Set of 5 latex resistance bands (10–50 lb). Includes carry bag.',
        'price': '18.99',
        'variants': [
            {'color': 'Mixed', 'stock': 50},
        ],
    },
]


def seed():
    print("Seeding categories...")
    categories = {}
    for data in CATEGORIES:
        obj, created = Category.objects.get_or_create(
            slug=data['slug'],
            defaults={'category_name': data['category_name']},
        )
        categories[data['slug']] = obj
        print(f"  {'Created' if created else 'Exists '} → {obj.category_name}")

    print("\nSeeding products & variants...")
    for data in PRODUCTS:
        category = categories[data['category_slug']]
        product, created = Product.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'product_name': data['product_name'],
                'category': category,
                'description': data['description'],
                'price': data['price'],
            },
        )
        print(f"  {'Created' if created else 'Exists '} → {product.product_name}")

        for v in data.get('variants', []):
            variant, v_created = ProductVariant.objects.get_or_create(
                product=product,
                color=v['color'],
                defaults={'stock': v['stock'], 'image': ''},
            )
            print(f"    {'Created' if v_created else 'Exists '} variant: {variant.color} (stock={variant.stock})")

    print("\nDone.")


if __name__ == '__main__':
    seed()
