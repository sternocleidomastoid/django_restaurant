from random import randrange

from django.contrib.auth.models import User

from restaurant.models import Ingredient, Inventory, MenuItemType, MenuItem, Sale, InventoryTopUp, Transaction
from mixer.backend.django import mixer


def populate():
    u = mixer.blend(User, username='admin', is_superuser=True)
    u.set_password('admin')
    u.save()
    m1 = mixer.blend(Inventory, name='oil', total=10, low_level_threshold=5, price=2, unit='ml')
    m2 = mixer.blend(Inventory, name='soy sauce', total=15, low_level_threshold=7, price=3, unit='ml')
    m3 = mixer.blend(Inventory, name='salt', total=100, low_level_threshold=20, price=1, unit='mg')
    mixer.blend(Inventory, name='chicken', total=80, low_level_threshold=25, price=10, unit='kg')
    mixer.blend(Inventory, name='pork', total=90, low_level_threshold=25, price=12, unit='kg')
    mixer.blend(Inventory, name='garlic', total=30, low_level_threshold=15, price=2, unit='pc')
    mixer.blend(Inventory, name='onion', total=100, low_level_threshold=25, price=2, unit='pc')
    c1=mixer.blend(Ingredient, name=m1, quantity=2)
    c2=mixer.blend(Ingredient, name=m2, quantity=3)
    c3=mixer.blend(Ingredient, name=m3, quantity=5)
    c4=mixer.blend(Ingredient, quantity=2)
    c5=mixer.blend(Ingredient, name=m1, quantity=3)
    c6=mixer.blend(Ingredient, name=m1, quantity=1.5)
    mixer.blend(Ingredient, name=m3, quantity=1.5)
    mixer.blend(Ingredient, quantity=4.5)
    mixer.blend(Ingredient, quantity=0.5)
    mixer.blend(MenuItem, name='chicken adobo', ingredients=[c1,c3], price=randrange(1, 21, 2), status='available')
    mixer.blend(MenuItem, name='pork adobo', ingredients=[c2, c5], price=randrange(1, 21, 2), status='available')
    mixer.blend(MenuItem, name='fried chicken', ingredients=[c3, c6], price=randrange(1, 21, 2), status='available')
    mixer.blend(MenuItem, name='pork stir fry', ingredients=[c3, c4], price=randrange(1, 21, 2), status='available')
    mixer.blend(MenuItem, name='porky', ingredients=[c1, c6, c5], price=randrange(1, 21, 2), status='available')
    mixer.blend(MenuItem, name='lemonade', ingredients=[c2], price=randrange(1, 21, 2), status='available')
