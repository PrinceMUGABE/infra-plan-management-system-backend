
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userApp.urls')),
    path('project/', include('projectApp.urls')),
    path('planner/', include('plannerApp.urls')),
    path('engineer/', include('engineerApp.urls')),
    path('stakeholder/', include('stakeholderApp.urls')),
    path('planned/', include('plannedProjectApp.urls')),
    path('funded_project/', include('funded_project_app.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)