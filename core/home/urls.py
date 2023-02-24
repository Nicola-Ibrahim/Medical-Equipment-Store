from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# from rest_framework.schemas import get_schema_view
# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("core.apps.accounts.urls"), name="accounts"),
    path("api/product/", include("core.apps.product.urls"), name="product"),
    path("api/order/", include("core.apps.order.urls"), name="order"),
    path("api/notification/", include("core.apps.notification.urls"), name="notification"),
    # path("docs/", include_docs_urls(title='MedicalStorApi'), name=""),
    # path('api/schema/', get_schema_view(
    #     title="MedicalStorApi",
    #     description="API for all the medical equipment store",
    #     version="1.0.0"
    # ), name='openapi-schema'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
