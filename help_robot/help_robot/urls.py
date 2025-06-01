from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

# URLs sans préfixe de langue
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs avec préfixe de langue (/en/ ET /fr/)
urlpatterns += i18n_patterns(
    path('', include('errors.urls')),
    prefix_default_language=True  # IMPORTANT: Active /en/ pour l'anglais aussi
)