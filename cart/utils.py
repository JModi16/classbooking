from decimal import Decimal

from profiles.models import Instructor
from services.models import ExerciseClass


PACKAGE_OPTIONS = {
    'single': {
        'field': 'package_single_rate',
        'label': 'Single Session Package',
        'description': 'Pay as you go - perfect for trying out',
    },
    'pack5': {
        'field': 'package_5_rate',
        'label': '5 Session Package',
        'description': 'Great for short-term commitment',
    },
    'pack10': {
        'field': 'package_10_rate',
        'label': '10 Session Package',
        'description': 'Most popular - save more per session',
    },
    'monthly': {
        'field': 'package_monthly_rate',
        'label': 'Monthly Unlimited Package',
        'description': 'Unlimited classes for one month',
    },
    'private': {
        'field': 'hourly_rate',
        'label': 'Private 1-on-1 Session',
        'description': 'Personalized one-to-one session',
    },
}


def parse_cart_key(item_key):
    key = str(item_key)

    if key.isdigit():
        return 'class', int(key), None

    if key.startswith('pkg_'):
        parts = key.split('_', 2)
        if len(parts) == 3 and parts[1].isdigit():
            return 'package', int(parts[1]), parts[2]

    return None, None, None


def build_package_key(instructor_id, package_type):
    return f'pkg_{instructor_id}_{package_type}'


def get_package_option(instructor, package_type):
    option = PACKAGE_OPTIONS.get(package_type)
    if not option:
        return None

    value = getattr(instructor, option['field'], None)
    if value is None:
        return None

    return {
        'package_type': package_type,
        'field': option['field'],
        'label': option['label'],
        'description': option['description'],
        'price': Decimal(value),
    }


def build_cart_items(cart):
    cart_items = []
    total = Decimal('0.00')
    item_count = 0

    for item_key, raw_quantity in cart.items():
        item_type, object_id, package_type = parse_cart_key(item_key)
        if item_type is None:
            continue

        try:
            quantity = int(raw_quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            continue

        if item_type == 'class':
            try:
                exercise_class = ExerciseClass.objects.select_related('instructor').get(id=object_id)
            except ExerciseClass.DoesNotExist:
                continue

            available_spots = exercise_class.get_available_spots()
            effective_quantity = min(quantity, available_spots)
            if effective_quantity < 1:
                continue

            unit_price = Decimal(exercise_class.price)
            item_total = unit_price * effective_quantity
            total += item_total
            item_count += effective_quantity

            cart_items.append({
                'item_key': str(item_key),
                'item_type': 'class',
                'quantity': effective_quantity,
                'unit_price': unit_price,
                'item_total': item_total,
                'exercise_class': exercise_class,
                'class': exercise_class,
                'class_id': exercise_class.id,
                'available_spots': available_spots,
                'display_name': exercise_class.name,
                'instructor_name': exercise_class.instructor.get_display_name(),
            })
            continue

        try:
            instructor = Instructor.objects.select_related('user').get(id=object_id, is_active=True)
        except Instructor.DoesNotExist:
            continue

        package_option = get_package_option(instructor, package_type)
        if not package_option:
            continue

        unit_price = package_option['price']
        item_total = unit_price * quantity
        total += item_total
        item_count += quantity

        cart_items.append({
            'item_key': str(item_key),
            'item_type': 'package',
            'quantity': quantity,
            'unit_price': unit_price,
            'item_total': item_total,
            'instructor': instructor,
            'instructor_id': instructor.id,
            'package_type': package_option['package_type'],
            'package_label': package_option['label'],
            'description': package_option['description'],
            'display_name': package_option['label'],
            'instructor_name': instructor.get_display_name(),
        })

    return cart_items, total, item_count
