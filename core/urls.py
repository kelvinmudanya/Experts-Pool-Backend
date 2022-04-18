from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import CountryViewSet, RegionViewSet, CompetenceViewSet, OccupationViewSet, ProfileViewSet, \
    ProfileRecommendationViewSet, OutbreakViewSet, ProfileDeploymentsViewSet, UserViewSet, GroupViewSet, \
    get_outbreak_options, ProfileCVViewSet, get_profile_deployments, CustomObtainTokenPairView, \
    OccupationCategoryViewSet, fetch_stats, AcademicQualificationTypeViewSet, ProfileAcademicQualificationViewSet, \
    OutbreakTypeViewSet, send_email, confirm_email, request_password_change, complete_password_change, \
    ProfileDeploymentReportViewSet, OutbreakReportViewSet

core_router = DefaultRouter()
core_router.register(r"country", CountryViewSet)
core_router.register(r"region", RegionViewSet)
core_router.register(r"competence", CompetenceViewSet)
core_router.register(r"occupation", OccupationViewSet)
core_router.register(r"academic-qualification-type", AcademicQualificationTypeViewSet)
core_router.register(r"occupation-category", OccupationCategoryViewSet)
core_router.register(r"profile", ProfileViewSet)
core_router.register(r"profile-academic-qualification", ProfileAcademicQualificationViewSet)
core_router.register(r"profile_cv", ProfileCVViewSet, basename="profile_cv")
core_router.register(r"deployment-report", ProfileDeploymentReportViewSet, basename="deployment_report")

core_router.register(r"recommendation", ProfileRecommendationViewSet)
core_router.register(r"outbreak", OutbreakViewSet)
core_router.register(r"outbreak-report", OutbreakReportViewSet, basename='outbreak_report')
core_router.register(r"outbreak-type", OutbreakTypeViewSet)
core_router.register(r"get_rdes", OutbreakViewSet)
core_router.register(r"deployment", ProfileDeploymentsViewSet)
core_router.register(r"users", UserViewSet)
core_router.register(r"user-groups", GroupViewSet)
url_patterns = core_router.urls
url_patterns += [
    path("send-email/", send_email, name="send_email"),
    path("confirm-email/<username>/<otp>", confirm_email, name="confirm_email"),
    path("request-password-change/", request_password_change, name="request_password_change"),
    path("complete-password-change/", complete_password_change, name="complete_password_change"),
    path("request-token/", CustomObtainTokenPairView.as_view(), name="request_otp"),
    path("fetch_stats/", fetch_stats, name="fetch_stats"),
    path("get_profile_deployments/<profile_id>/", get_profile_deployments, name="get_profile_deployments"),
    path("outbreak_options/", get_outbreak_options, name="get_outbreak_options")
]
