from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Like(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_by')
    to = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.by} likes {self.to}'
    
    class Meta:
        unique_together = ('by', 'to')
