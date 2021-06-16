from rest_framework.routers import DefaultRouter

from core.views import CountryViewSet, RegionViewSet, CompetenceViewSet, OccupationViewSet, ProfileViewSet, \
    ProfileRecommendationViewSet, OutbreakViewSet, ProfileDeploymentsViewSet, UserViewSet, GroupViewSet

core_router = DefaultRouter()
core_router.register(r"country", CountryViewSet)
core_router.register(r"region", RegionViewSet)
core_router.register(r"competence", CompetenceViewSet)
core_router.register(r"occupation", OccupationViewSet)
core_router.register(r"profile", ProfileViewSet)
core_router.register(r"recommendation", ProfileRecommendationViewSet)
core_router.register(r"outbreak", OutbreakViewSet)
core_router.register(r"deployment", ProfileDeploymentsViewSet)
core_router.register(r"users", UserViewSet)
core_router.register(r"user-groups", GroupViewSet)
url_patterns = core_router.urls
url_patterns += [
    # path("request-otp/", views.request_otp, name="request_otp"),
]
