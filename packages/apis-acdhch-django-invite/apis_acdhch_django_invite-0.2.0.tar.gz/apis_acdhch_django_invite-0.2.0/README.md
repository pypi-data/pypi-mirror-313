# apis_acdhch_django_invite

Invite app for Django applications.

This app provides an invite link that only works with valid tokens. The invite tokens can be generated in Django's admin interface.
The invite endpoint is `/invite/<token>`.

# Installation

Add `apis_acdhch_django_invite` to your `INSTALLED_APPS`.
Include the apis-acdhch-django-invite urls in your `urls.py`:
```
urlpatterns += [path("", include("apis_acdhch_django_invite.urls")),]
```
