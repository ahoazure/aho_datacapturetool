"""translate_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include,re_path
from home import views
from django.conf.urls.i18n import i18n_patterns #added
from django.views.static import serve # hack to support display of uploaded files
from django.conf import settings # Facilitate viewing on browser pdf reader
from django.conf.urls.static import static # Facilitate display of static assets
from django.conf.urls import handler404 # display custom 404 error page
from rest_framework_simplejwt.views import (
TokenObtainPairView, TokenRefreshView,)
from rest_framework.documentation import (
    include_docs_urls, get_schemajs_view)
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='AHO Data Capture API Endpoints')

api_patterns = [
    path('', views.index, name='index'), # If no APi route load the login page
    path('', include(('regions.urls','regions'),namespace='regions')),
    path('', include(('indicators.urls','indicators'),namespace='indicators')),
    path('', include(('publications.urls','publications'),namespace='publications')),
    path('', include(('elements.urls', 'elements'), namespace='elements')),
    path('', include(('home.urls', 'home'), namespace='home')),
]
"""
This pattern was added on 25/10/2020 to allow setting of the base/root URL to
 include language selected from the login form once the used selects en, fror pt
 """
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), #Important for language selection
]

urlpatterns += i18n_patterns ( # must be python immutable list () and not []
    path('', views.index, name='index'),
    path('admin/', admin.site.urls,name='dashboard'),
    path('accounts/login/', views.login_view, name='login'),
    path('datawizard/', include('data_wizard.urls')), #for data import wizard
   #Reset and Changepassword urls
    path('password-reset/', auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(),
        name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),

   # API-based URL patterns for hitting KHRO endpoints for consuming data in JSON
    path('api/', include((api_patterns, 'api'), namespace='api')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/docs/', include_docs_urls(title='AHO-DCT', public=False)),
    path('api/schema/', get_schemajs_view(title='AHO-DCT', public=False)),
    path('api/swagger-docs/', schema_view),
    # Route that allows display of uploaded files when Debug=False in settings.py
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    prefix_default_language=False # Hide default language code (en) on all urls

)

# Routes for error handlers served by home view and htmls in templates/home/errors
handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'
