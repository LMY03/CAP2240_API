from django.urls import path

from . import views

app_name = "ticketing"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"), #request list
    path("new-form/", views.RequestFormView.as_view(), name="new-form"),
    # path("new-form-submit/", views.new_form_submit, name="new-form-submit"),
    path("<int:pk>/details/", views.DetailView.as_view(), name="details"),
    # path("request-confirm/<int:id>/", views.request_confirm, name="request-confirm"),
    # path('home-filter/', views.home_filter_view, name='home-filter'),
    # path('student/home/', views.student_home, name='student_home'),
    # path('faculty/home/', views.faculty_home, name='faculty_home'),
    # path('tsg/home/', views.tsg_home, name='tsg_home'),
    # path('add_comment/<int:pk>/', views.add_comment, name='add_comment'),
]