import sys
import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     os.path.pardir,
                                     os.path.pardir)
BASE = os.path.normcase(BASE)
sys.path.append(BASE)
from core  import manager_auth
manager_auth.manager_main()