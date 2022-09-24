from django.urls import path
from .views import SnackCreateView, SnackDetailView, SnackListView, SnackDeleteView, SnackUpdateView

urlpatterns = [
    path('', SnackListView.as_view(), name='snack_list'),
    path('<int:pk>/', SnackDetailView.as_view(), name='snack_detail'),
    path('<int:pk>/delete/', SnackDeleteView.as_view(), name='snack_delete'),
    path('<int:pk>/update/', SnackUpdateView.as_view(), name='snack_update'),
    path('create/', SnackCreateView.as_view(), name='snack_create'),
]