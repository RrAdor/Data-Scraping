
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('scrape/', views.ScrapePortalView.as_view(), name='scrape_portal'),
    path('headlines/<str:portal>/', views.HeadlinesView.as_view(), name='headlines'),
    path('article/', views.ArticleView.as_view(), name='article'),
]