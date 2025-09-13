"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(('api.router'))),

    path('', TemplateView.as_view(template_name='login.html'), name='home'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register_page'),
    path('profile/', TemplateView.as_view(template_name='profile_view.html'), name='profile_view_page'),
    path('profile/edit/', TemplateView.as_view(template_name='profile_update.html'), name='profile_update_page'),
    path('notes/', TemplateView.as_view(template_name='notes.html'), name='notes_page'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from accounts.utils import validate_reset_token

class ForgotPasswordView(TemplateView):
    template_name = 'forgot_password.html'

class ResetConfirmView(TemplateView):
    template_name = 'reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uid, token = kwargs['uid'], kwargs['token']
        user, db_token = validate_reset_token(uid, token)
        if not user or not db_token:
            # Redirect to invalid (create a simple invalid.html or handle in template)
            return HttpResponseRedirect('/login/?error=invalid_token')
        context['uid'] = uid
        context['token'] = token
        return context

urlpatterns += [
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-confirm/<uid>/<token>/', ResetConfirmView.as_view(), name='reset_confirm'),
]
