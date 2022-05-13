from django.urls import path
from api.mod.store import store_controller

urlpatterns = [
    path('store/getList', store_controller.get_list),
    path('store/getDetail', store_controller.get_detail),
    path('store/create', store_controller.create),
    path('store/update', store_controller.update),
    path('store/delete', store_controller.delete),
]
