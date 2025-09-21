"""Convenience import so 'Shanghuyun_Platform.settings' loads dev settings by default.

This prevents errors when DJANGO_SETTINGS_MODULE is set to the package
('Shanghuyun_Platform.settings') instead of a concrete module like
'Shanghuyun_Platform.settings.dev'.
"""

from .dev import *  # noqa: F401,F403

