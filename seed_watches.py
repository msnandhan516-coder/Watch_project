import django, os
os.environ['DJANGO_SETTINGS_MODULE']='watchproject.settings'
django.setup()
from myapp.models import watchstock
from django.core.files.base import ContentFile

hero_img = 'd:/watchproject/watchproject/watchproject/static/gshock_hero.png'

watches = [
    ('G-SHOCK GM-B2100', 'Casio G-SHOCK', 'Luxury', 32999, 15, 'Full Metal Stainless Steel. Octagonal bezel. Bluetooth. Solar powered.', True),
    ('G-SHOCK GD-350', 'Casio G-SHOCK', 'Sport', 8999, 25, 'World time. Shock resistant. LED flash alert. 200M water resistance.', False),
    ('G-SHOCK GA-2100', 'Casio G-SHOCK', 'Casual', 12999, 20, 'Carbon Core Guard. Ultra-thin profile. Analog-digital combo.', True),
    ('G-SHOCK Mudmaster GWG-2000', 'Casio G-SHOCK', 'Sport', 45999, 8, 'Triple sensor. Mud resistant. Tough Solar. GPS timekeeping.', False),
    ('G-SHOCK Rangeman GPR-H1000', 'Casio G-SHOCK', 'Sport', 89999, 5, 'GPS navigation. Heart rate monitor. Altitude/Barometer/Compass.', True),
    ('G-SHOCK Frogman GWF-A1000', 'Casio G-SHOCK', 'Luxury', 54999, 6, 'ISO 6425 dive watch. 200M water resistant. Carbon fiber reinforced.', False),
    ('G-SHOCK GA-700', 'Casio G-SHOCK', 'Casual', 7499, 30, 'Large face analog-digital. 200M water resistant. World time 48 cities.', False),
    ('G-SHOCK DW-5600', 'Casio G-SHOCK', 'Classic', 5999, 40, 'The original G-SHOCK. Square case. Digital. 200M water resistant.', False),
    ('G-SHOCK MTG-B3000', 'Casio G-SHOCK', 'Luxury', 68999, 4, 'Metal-Twisted G-SHOCK. Carbon fiber core guard. GPS Multiband 6.', True),
    ('G-SHOCK GBA-900', 'Casio G-SHOCK', 'Smart', 14999, 18, 'Step tracker. Bluetooth. Calendar. 200M water resistant.', False),
]

added = 0
with open(hero_img, 'rb') as f:
    img_bytes = f.read()

for (wname, brand, cat, price, qty, desc, featured) in watches:
    if not watchstock.objects.filter(wname=wname).exists():
        fname = wname.replace(' ', '_').replace('-', '') + '.png'
        img_content = ContentFile(img_bytes, name=fname)
        obj = watchstock(
            wname=wname, brand=brand, category=cat,
            price=price, qty=qty, description=desc, is_featured=featured
        )
        obj.photo.save(fname, img_content, save=False)
        obj.save()
        added += 1
        print('Added: ' + wname)
    else:
        print('Exists: ' + wname)

print('Done. Added ' + str(added) + '. Total: ' + str(watchstock.objects.count()))
