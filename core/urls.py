from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import CountryViewSet, RegionViewSet, CompetenceViewSet, OccupationViewSet, ProfileViewSet, \
    ProfileRecommendationViewSet, OutbreakViewSet, ProfileDeploymentsViewSet, UserViewSet, GroupViewSet, \
    suggest_rdes, get_outbreak_options, ProfileCVViewSet, get_profile_deployments, CustomObtainTokenPairView, \
    OccupationCategoryViewSet

core_router = DefaultRouter()
core_router.register(r"country", CountryViewSet)
core_router.register(r"region", RegionViewSet)
core_router.register(r"competence", CompetenceViewSet)
core_router.register(r"occupation", OccupationViewSet)
core_router.register(r"occupation-category", OccupationCategoryViewSet)
core_router.register(r"profile", ProfileViewSet)
core_router.register(r"profile_cv", ProfileCVViewSet, basename="profile_cv")

core_router.register(r"recommendation", ProfileRecommendationViewSet)
core_router.register(r"outbreak", OutbreakViewSet)
core_router.register(r"deployment", ProfileDeploymentsViewSet)
core_router.register(r"users", UserViewSet)
core_router.register(r"user-groups", GroupViewSet)
url_patterns = core_router.urls
url_patterns += [
    path("request-token/", CustomObtainTokenPairView.as_view(), name="request_otp"),
    path("suggest_rdes/", suggest_rdes, name="suggest_rdes"),
    path("get_profile_deployments/<profile_id>/", get_profile_deployments, name="get_profile_deployments"),
    path("outbreak_options/", get_outbreak_options, name="get_outbreak_options")
]
