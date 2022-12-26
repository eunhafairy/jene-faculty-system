from django.db import models

# Create your models here.
"""
LOG EVENT TYPES :
Login - done
Logout - done
Registration - done
Profile update - done
Account deletion - done
Department create - done
Department edit - done
Department delete - done
Extensions create  - done
Extensions edit - done
Extensions delete - done
Extensions assign - done
Announcements create - done
Announcements edit - done
Announcements delete - done
Research create - done
Research edit - done
Research delete - done 
Subject create - done 
Subject edit - done 
Subject delete - done 
Subject assign

"""

class Log(models.Model):
    log_time = models.DateTimeField(auto_now_add=True)
    log_code = models.CharField(max_length=50)
    log_message = models.TextField()

