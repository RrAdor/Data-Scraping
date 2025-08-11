from django.urls import path
from .views import (
    index, login_view, signup, signin, logout, profile, 
    url_analysis, analyzer, headlines, analyze_content, clear_headlines
)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('analyze/', url_analysis, name='url_analysis'),
    path('headlines/', headlines, name='headlines'),
    path('analyze-content/', analyze_content, name='analyze_content'),
    path('clear-headlines/', clear_headlines, name='clear_headlines'),
    path('analyzer/', analyzer, name='analyzer'),
    path('analyzer/<str:document_id>/', analyzer, name='analyzer_with_id'),
]