from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls', namespace='user-api')),
    path('api/receipt/', include('receipt.urls', namespace='receipt-api'))
]

urlpatterns += static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)
