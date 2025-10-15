from django.db import models

class Career(models.Model):
    username = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_datetime']
    
    def __str__(self):
        return f"{self.title} by {self.username}"