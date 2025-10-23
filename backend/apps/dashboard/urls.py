"""
URL configuration for dashboard app.
"""

from django.urls import path
from .views import DashboardStatsView, MyDashboardView

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('my/', MyDashboardView.as_view(), name='my-dashboard'),
]
