
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view),
    path('login/', views.login_view),
    path('notes/get/', views.get_all_notes),
    path('notes/create/', views.create_note),
    path('notes/<int:id>/', views.get_note),
    path('notes/update/<int:id>/', views.update_note),
    path('notes/update/share/<int:id>/', views.share_note),
    # Add other URL patterns for the remaining endpoints
]
