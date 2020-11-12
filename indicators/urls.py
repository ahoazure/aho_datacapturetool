from rest_framework.routers import SimpleRouter
from indicators import views

router = SimpleRouter()
router.register(
    r'indicator_references', views.StgIndicatorReferenceViewSet, "indicator_references")
router.register(
    r'indicators', views.StgIndicatorViewSet, "indicators")
router.register(
    r'indicator_domains', views.StgIndicatorDomainViewSet, "indicator_domains")
router.register(
    r'indicator_data', views.FactDataIndicatorViewSet, "indicator_data")
urlpatterns = router.urls
