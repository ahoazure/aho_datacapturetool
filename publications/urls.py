from rest_framework.routers import SimpleRouter
from publications import views

router = SimpleRouter()
router.register(
    r'resource_types', views.StgResourceTypeViewSet, 'resource_type')
router.register(
    r'published_resources',views.StgKnowledgeProductViewSet,'published_resources')
router.register(
    r'product_domains', views.StgKnowledgeDomainViewSet,'product_domains')
urlpatterns = router.urls
