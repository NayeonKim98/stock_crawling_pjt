from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class InterestedStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interested_stocks')
    company_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
            constraints = [
            models.UniqueConstraint(fields=['user', 'company_name'], name='unique_user_company')
        ]
            
    def __str__(self):
        return f'{self.user.username} - {self.company_name}'