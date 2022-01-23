from django.urls import path


from . import views


urlpatterns = [
    path('v1/users/query/', views.ListUsersView.as_view(), name='query-users-by-ids'),
]
