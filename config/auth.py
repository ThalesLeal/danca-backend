from urllib.parse import urlencode

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from django.conf import settings
from django.urls import reverse

staff = settings.STAFF_LIST
superusers = settings.SUPERUSER_LIST


class SSOAuthenticationBackend(OIDCAuthenticationBackend):
    def describe_user_by_claims(self, claims):
        username = claims.get("preferred_username")
        return f"username {username}"

    def filter_users_by_claims(self, claims):
        username = claims.get("preferred_username")
        if not username:
            return self.UserModel.objects.none()

        return self.UserModel.objects.filter(username=username)

    def create_user(self, claims):
        email = claims.get("email")
        username = self.get_username(claims)
        first_name = claims.get("given_name")
        last_name = claims.get("family_name")

        user = self.UserModel.objects.create_user(
            username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=username in staff or username in superusers,
            is_superuser=username in superusers
        )

        return user

    def get_username(self, claims):
        return claims.get("preferred_username")

    def update_user(self, user, claims):
        user.email = claims.get("email")
        user.first_name = claims.get("given_name")
        user.last_name = claims.get("family_name")

        user.is_staff = user.username in staff or user.username in superusers
        user.is_superuser = user.username in superusers

        user.save()
        return user


def get_post_logout_redirect_uri(request) -> str:
    if next_url := request.GET.get("next") or request.POST.get("next"):
        redirect_uri = next_url
    else:
        redirect_uri = settings.LOGOUT_REDIRECT_URL

    if not redirect_uri:
        redirect_uri = settings.LOGIN_URL
    elif redirect_uri.startswith("http://") or redirect_uri.startswith("https://"):
        return redirect_uri
    elif redirect_uri.startswith("/"):
        redirect_uri = redirect_uri
    else:
        redirect_uri = reverse(redirect_uri)

    return request.build_absolute_uri(redirect_uri)


def logout_url(request) -> str:
    sso_logout_url = settings.OIDC_OP_LOGOUT_ENDPOINT
    client_id = settings.SSO_CLIENT_ID
    id_token = request.session["oidc_id_token"]
    post_logout_redirect_uri = get_post_logout_redirect_uri(request)

    querystring = urlencode(
        {
            "client_id": client_id,
            "id_token_hint": id_token,
            "post_logout_redirect_uri": post_logout_redirect_uri,
        }
    )

    return f"{sso_logout_url}?{querystring}"
