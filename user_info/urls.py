from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import manage_item

urlpatterns = {
    path('', manage_item, name="items"),
}
urlpatterns = format_suffix_patterns(urlpatterns)
