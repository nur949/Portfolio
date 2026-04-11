from django.urls import path

from .views import HealthCheckView, SiteContentView


urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("site-content/", SiteContentView.as_view(), name="site-content"),
]
