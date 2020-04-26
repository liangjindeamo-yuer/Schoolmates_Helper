from django.db import models


class tasks_display_order(models.Model):
    reward_up = models.BooleanField(default=False)
    reward_down = models.BooleanField(default=False)

# Create your models here.
