
from django.contrib import admin
from django.urls import path, include
from core.urls import url_patterns as core_urls_patterns
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include([*core_urls_patterns])),
    path('admin/', admin.site.urls),
]
