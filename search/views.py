from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings
from . import models


class UserSearches(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'search/user_searches.html'
    model = models.Search
    paginate_by = 20
    context_object_name = 'searches'
    ordering = ['publication_date_search', 'finish_date_search']
    login_url = settings.LOGIN_URL
    permission_required = 'search.view_search'

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(user_search=self.request.user)

        return qs
