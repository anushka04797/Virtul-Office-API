"""virtual_office_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from virtual_office_API import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("users.urls")),
    path('project/', include("projects.urls")),
    path('wbs/', include("wbs.urls")),
    path('evms/', include("evms.urls")),
    path('meetings/', include("meetings.urls")),

    path('docs/', include_docs_urls(title="Virtual Office", description="A Project management platform",
                                    permission_classes=(AllowAny,))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
