from rest_framework.routers import DefaultRouter

from core.views import CountryViewSet, RegionViewSet, CompetenceViewSet, OccupationViewSet, ProfileViewSet, \
    ProfileRecommendationViewSet, OutbreakViewSet, ProfileDeploymentsViewSet

core_router = DefaultRouter()
core_router.register(r"country", CountryViewSet)
core_router.register(r"country", RegionViewSet)
core_router.register(r"country", CompetenceViewSet)
core_router.register(r"country", OccupationViewSet)
core_router.register(r"country", ProfileViewSet)
core_router.register(r"country", ProfileRecommendationViewSet)
core_router.register(r"country", OutbreakViewSet)
core_router.register(r"country", ProfileDeploymentsViewSet)
url_patterns = core_router.urls
url_patterns += [
    # path("request-otp/", views.request_otp, name="request_otp"),
]
