
import os,sys

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
#print(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffyEye.settings")
import django
django.setup()
from app01 import models

print(models.Temp.objects.all())