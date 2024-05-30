from django.conf import settings

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from alerts.views import debug_email as debug_alerts_email
from users.views import debug_email as debug_users_email
from bugsink.app_settings import get_settings
from users.views import signup, confirm_email, resend_confirmation

from .views import home, trigger_error, favicon


admin.site.site_header = get_settings().SITE_TITLE
admin.site.site_title = get_settings().SITE_TITLE
admin.site.index_title = "Admin"  # everyone calls this the "admin" anyway. Let's set the title accordingly.


urlpatterns = [
    path('', home, name='home'),

    path("accounts/signup/", signup, name="signup"),
    path("accounts/resend-confirmation/", resend_confirmation, name="resend_confirmation"),
    path("accounts/confirm-email/<str:token>/", confirm_email, name="confirm_email"),

    path("accounts/login/", auth_views.LoginView.as_view(template_name="bugsink/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    path('api/', include('ingest.urls')),

    path('events/', include('events.urls')),
    path('issues/', include('issues.urls')),

    path('admin/', admin.site.urls),

    path("favicon.ico", favicon),
]

if settings.DEBUG:
    urlpatterns += [
        path('debug-alerts-email/<str:template_name>/', debug_alerts_email),
        path('debug-users-email/<str:template_name>/', debug_users_email),
        path('trigger-error/', trigger_error),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
