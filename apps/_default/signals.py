from allauth.account.signals import user_signed_up

from django.dispatch import receiver


@receiver(user_signed_up, dispatch_uid="post_user_signed_up")
def post_user_signed_up(request, user, **kwargs):
    user.is_staff = True
    user.save()
