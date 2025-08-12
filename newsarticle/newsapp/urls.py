from django.urls import path
from .views import HomeView, ScrapePortalView, HeadlinesView, ArticleView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('scrape/', ScrapePortalView.as_view(), name='scrape_portal'),
    path('headlines/<str:portal>/', HeadlinesView.as_view(), name='headlines'),
    path('article/', ArticleView.as_view(), name='article'),
]