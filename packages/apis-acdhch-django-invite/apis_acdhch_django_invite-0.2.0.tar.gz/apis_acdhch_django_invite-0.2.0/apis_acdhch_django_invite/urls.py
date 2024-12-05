from django.urls import path

from apis_acdhch_django_invite.views import Invite

urlpatterns = [
    path("invite/<uuid:invite>", Invite.as_view()),
]
