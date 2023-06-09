from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.urls import url_patterns as core_urls_patterns
from rest_framework_simplejwt import views as jwt_views
from .views import confirm_email_html
from rest_framework.documentation import include_docs_urls

from eac_rde_backend import settings

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include([*core_urls_patterns])),
    path("confirm-email/<username>/<otp>", confirm_email_html, name="confirm_email_html"),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='EAC RDE API'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)