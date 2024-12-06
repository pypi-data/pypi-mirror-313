from django.urls import path

from . import views

urlpatterns = [
    path("upload/", views.UploadView.as_view(), name="portfolio upload"),
    path("gallery/", views.GalleryView.as_view(), name="portfolio gallery"),
    path("search/", views.SearchView.as_view(), name="portfolio search"),
    path("contact/", views.ContactView.as_view(), name="portfolio contact"),
    path("<str:slug>/", views.MediaDetailView.as_view(), name="media detail"),
    path("<str:slug>/edit/", views.MediaUpdateView.as_view(), name="media edit"),
    path("<str:slug>/delete/", views.MediaDeleteView.as_view(), name="media delete"),
]
