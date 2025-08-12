# from django.db import models
# from django.utils import timezone

# class ScrapedArticle(models.Model):
#     headline = models.CharField(max_length=500)
#     url = models.URLField(max_length=1000)
#     body = models.TextField()
#     portal_name = models.CharField(max_length=100)
#     scraped_at = models.DateTimeField(default=timezone.now)
#     type = models.CharField(max_length=10, choices=[('article', 'Article'), ('video', 'Video')])
    
#     def __str__(self):
#         return self.headline

# class ScrapingTask(models.Model):
#     url = models.URLField(max_length=1000)
#     status = models.CharField(max_length=20, choices=[
#         ('pending', 'Pending'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#         ('failed', 'Failed')
#     ], default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     completed_at = models.DateTimeField(null=True, blank=True)
#     result_count = models.IntegerField(default=0)
    
#     def __str__(self):
#         return f"Task for {self.url}"