from rest_framework.routers import SimpleRouter
from indicators import views

router = SimpleRouter()
router.register(
    r'indicator_sources', views.StgIndicatorReferenceViewSet, "indicator_sources")
router.register(
    r'indicators', views.StgIndicatorViewSet, "indicators")
router.register(
    r'indicator_domains', views.StgIndicatorDomainViewSet, "indicator_domains")
router.register(
    r'indicator_data', views.FactDataIndicatorViewSet, "indicator_data")
urlpatterns = router.urls
