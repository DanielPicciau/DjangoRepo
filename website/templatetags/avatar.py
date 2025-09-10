from django import template
from django.utils.crypto import salted_hmac
from website.models import AVATAR_CHOICES

register = template.Library()


@register.filter(name='avatar_path')
def avatar_path(user):
    """Return a stable avatar path for a user.
    Prefers profile.avatar if present; otherwise choose deterministically
    from AVATAR_CHOICES using a hash of the username.
    """
    try:
        avatar = getattr(user, 'profile', None) and getattr(user.profile, 'avatar', '')
        if avatar:
            return avatar
    except Exception:
        pass
    # Deterministic pick based on username to avoid missing avatars
    key = salted_hmac('avatar-pick', user.username or 'anon').hexdigest()
    idx = int(key[:8], 16) % len(AVATAR_CHOICES)
    return AVATAR_CHOICES[idx]

