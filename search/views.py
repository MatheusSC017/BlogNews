from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.shortcuts import reverse, redirect, get_object_or_404
from . import models, forms


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


class CreateSearch(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'search/search_form.html'
    model = models.Search
    form_class = forms.SearchForm
    login_url = settings.LOGIN_URL
    permission_required = 'search.add_search'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if kwargs.get('option_form'):
            context['option_form'] = kwargs.get('option_form')
        else:
            context['option_form'] = forms.OptionInlineForm()

        return context

    def form_valid(self, form):
        option_form = forms.OptionInlineForm(data=self.request.POST)

        if option_form.is_valid() and form.is_valid():
            self.object = form.save(commit=False)
            self.object.user_search = self.request.user
            self.object.save()
            option_form.instance = self.object
            option_form.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form, option_form)

    def form_invalid(self, form, option_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                option_form=option_form
            )
        )

    def get_success_url(self):
        messages.success(self.request, 'Pesquisa cadastrada')
        return reverse('search:user_search')


class UpdateSearch(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'search/search_form.html'
    model = models.Search
    form_class = forms.SearchForm
    login_url = settings.LOGIN_URL
    permission_required = 'search.change_search'

    def get(self, request, pk, *args, **kwargs):
        get_object_or_404(models.Search, pk=pk, user_search=request.user)
        return super().get(pk, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if kwargs.get('option_form'):
            context['option_form'] = kwargs.get('option_form')
        else:
            context['option_form'] = forms.OptionInlineForm(instance=self.object)

        return context

    def form_valid(self, form):
        option_form = forms.OptionInlineForm(data=self.request.POST, instance=self.object)

        if option_form.is_valid() and form.is_valid():
            self.object.save()
            option_form.instance = self.object
            option_form.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form, option_form)

    def form_invalid(self, form, option_form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                option_form=option_form
            )
        )

    def get_success_url(self):
        messages.success(self.request, 'Pesquisa atualizada')
        return reverse('search:user_search')
