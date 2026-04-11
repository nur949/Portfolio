from django.urls import path

from .views import home_page, managed_work_page, projects_page, superadmin_dashboard


urlpatterns = [
    path("", home_page, name="site-home"),
    path("projects/", projects_page, name="site-projects"),
    path("work/<slug:slug>/", managed_work_page, name="site-work-page"),
    path("superadmin/", superadmin_dashboard, name="site-superadmin"),
]
