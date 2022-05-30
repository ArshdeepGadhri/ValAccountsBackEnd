from django.urls import path

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.views import CreateAccountView, UpdateAccountView, AccountView, DeleteAccountView, ValorantAccountCreate, ValorantAccountDelete, ValorantAccountList, ValorantAdminAccountList, ValorantAccountSearch, ValorantAccountUpdate

app_name = 'accounts'
urlpatterns = [
    path('signup/', CreateAccountView.as_view(), name='signup'),
    path('update/', UpdateAccountView.as_view(), name='update'),
    path('profile/', AccountView.as_view(), name='profile'),
    path('signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('delete/', DeleteAccountView.as_view(), name='delete'),
    path('val/all/', ValorantAccountList.as_view(), name='list'),
    path('val/admin/all/', ValorantAdminAccountList.as_view(), name='admin_list'),
    path('val/search/<str:rank>/', ValorantAccountSearch.as_view(), name='search'), # val/search/str/
    path('val/search/', ValorantAccountSearch.as_view(), name='search'), # val/search?rank=str
    path('val/create/', ValorantAccountCreate.as_view(), name='create'),
    path('val/<int:id>/delete/', ValorantAccountDelete.as_view(), name='delete'),
    path('val/<int:id>/update/', ValorantAccountUpdate.as_view(), name='update')
]
