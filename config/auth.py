from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from django.conf import settings
from django.urls import reverse


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
            is_staff=True,
        )

        user.set_unusable_password()
        return user

    def get_username(self, claims):
        return claims.get("preferred_username")

    def update_user(self, user, claims):
        user.email = claims.get("email")
        user.first_name = claims.get("given_name")
        user.last_name = claims.get("family_name")
        user.save()
        return user


def logout_url(request) -> str:
    sso_url = settings.SSO_OIDC_URL.rstrip("/")
    client_id = settings.SSO_CLIENT_ID
    id_token = request.session["oidc_id_token"]

    redirect_uri = f"{request.scheme}://{request.get_host()}"
    if settings.LOGOUT_REDIRECT_URL.startswith("/"):
        redirect_uri += settings.LOGOUT_REDIRECT_URL
    elif settings.LOGOUT_REDIRECT_URL.startswith("http"):
        redirect_uri = settings.LOGOUT_REDIRECT_URL
    else:
        redirect_uri += reverse(settings.LOGOUT_REDIRECT_URL)

    url = (
        f"{sso_url}/logout"
        f"?client_id={client_id}"
        f"&id_token_hint={id_token}"
        f"&post_logout_redirect_uri={redirect_uri}"
    )

    return url
