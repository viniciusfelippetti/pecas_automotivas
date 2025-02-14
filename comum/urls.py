from django.urls import path
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from comum.views import CarModelView, UserView
from comum.views.auth import SignInView, SignUpView, SignOutView
from comum.views.car_model import CarsModelPartView, RemovePartsCarModelView, AssociatePartsToCarModelsView
from comum.views.csv_upload import CSVUploadView
from comum.views.part import PartView, PartsCarModelView
from comum.views.user import AddUserGroupModelView

urlpatterns = [
    # Part
    path(
        "part/",
        PartView.as_view(),
        name="part",
    ),
    path(
        "part/<uuid:part_id>/",
        PartView.as_view(),
        name="manage-part",
    ),
    path(
        "parts/car-model/<uuid:car_model_id>/",
        PartsCarModelView.as_view(),
        name="parts-car-model",
    ),
    # Car Model
    path(
        "car-model/",
        CarModelView.as_view(),
        name="car-model",
    ),
    path(
        "car-model/<uuid:car_model_id>/",
        CarModelView.as_view(),
        name="manage-car-model",
    ),
    path(
        "cars-model/part/<uuid:part_id>/",
        CarsModelPartView.as_view(),
        name="cars-model-part",
    ),
    path(
        "car-model/remove-parts/<uuid:car_model_id>/",
        RemovePartsCarModelView.as_view(),
        name="cars-model-remove-parts",
    ),
    path(
        "car-model/associate-parts-cars-model/",
        AssociatePartsToCarModelsView.as_view(),
        name="associate-parts-cars-model",
    ),

# Part
    path(
        "user/",
        UserView.as_view(),
        name="user",
    ),
    path(
        "user/<uuid:user_id>/",
        UserView.as_view(),
        name="manage-user",
    ),
    path(
        "add-user-group/<uuid:user_id>/",
        AddUserGroupModelView.as_view(),
        name="add-user-group",
    ),
    #Auth
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("sign-out/", SignOutView.as_view(), name="sign-out"),
    #Token JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #CSV Upload
    path('upload_csv/', CSVUploadView.as_view(), name='upload_csv'),

]
