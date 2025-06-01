# errors/models.py
from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ErrorCodeFanuc(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)
    title = models.CharField(max_length=200)
    cause_en = models.TextField()
    remedy_en = models.TextField()
    cause_fr = models.TextField()
    remedy_fr = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['code']
        verbose_name = "Fanuc Error Code"
        verbose_name_plural = "Fanuc Error Codes"
    
    def __str__(self):
        return f"{self.code} - {self.title}"