#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : PHO KHAING                                     |
#  | EMAIL: khaing.pho1991@gmail.com                       |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  | ROLE : Full-Stack Software Developer                  |
#  +-------------------------------------------------------+
#  | Released 13.3.2023.                                   |
#  +-------------------------------------------------------+

from ..role.models import Role


class AccessControl:
   user_id: int = ""
   module_name: str = ""
   action_name: str = ""
   
   role_name: str = ""
   
   def __init__(self, module_name, action_name):
      self.module_name = module_name
      self.action_name = action_name
   
   def hasAccessPermission(self, user_id, module_name, actions) -> bool:
      return True
   
   
   def hasAccessRole(self) -> bool:
      hasRole = Role.objects.filter(role_name_en__exact=self.module_name)
      return False
