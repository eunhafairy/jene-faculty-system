from reports.base import ModelReport
from .models import User

class UserReport(ModelReport):
    name = "Report - My Report"
    field_lookups = [("First Name", 'first_name'), ("Last Name", 'last_name') ,("Email", 'email')]
    queryset = User.objects.all()
