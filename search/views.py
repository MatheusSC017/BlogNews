from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db.models import Max, Count
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib import messages
from django.shortcuts import reverse, redirect, get_object_or_404
from django.utils import timezone
from . import models, forms


class Searches(ListView):
    template_name = 'search/searches.html'
    model = models.Search
    context_object_name = 'searches'
    paginate_by = 5
    ordering = ['-publication_date_search', 'finish_date_search', ]

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(published_search=True,
                       publication_date_search__lte=timezone.now())

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        searches = list()
        for search in context['searches']:
            options = models.Option.objects.filter(search_option=search.pk)
            options = options.annotate(
                vote_option=Count('vottinguseroption')
            )
            searches.append({'search': search,
                             'options': options,
                             'status': (search.finish_date_search > timezone.now()),
                             'max_vote': options.aggregate(Max('vote_option'))})
        context['searches'] = searches

        return context


class Search(DetailView):
    template_name = 'search/search.html'
    model = models.Search
    context_object_name = 'search'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if not context['search'].published_search or context['search'].publication_date_search > timezone.now():
            return redirect(reverse('search:searches'))

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('user:login'))

        search = get_object_or_404(models.Search,
                                   pk=kwargs.get('pk'),
                                   published_search=True,
                                   publication_date_search__lte=timezone.now(),
                                   finish_date_search__gte=timezone.now())
        option = get_object_or_404(models.Option,
                                   pk=request.POST['optionChoice'],
                                   search_option=search.pk)
        votting = models.VottingUserOption.objects.filter(user_votting=request.user.pk,
                                                          option_votting__in=models.Option.objects.filter(
                                                              search_option=search.pk
                                                          ))
        if votting.count() == 0:
            models.VottingUserOption.objects.create(user_votting=request.user,
                                                    option_votting=option)
        else:
            votting = votting[0]
            votting.option_votting = option
            votting.save()
        messages.success(request, 'Obrigado pelo voto')
        return redirect(reverse('search:search', args=[search.pk, ]))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        options = models.Option.objects.filter(search_option=context['search'].pk)
        options = options.annotate(
            vote_option=Count('vottinguseroption')
        )
        context['options'] = options
        context['max_vote'] = options.aggregate(Max('vote_option'))
        context['status'] = (context['search'].finish_date_search > timezone.now())
        if self.request.user.is_authenticated:
            context['vote'] = models.VottingUserOption.objects.filter(user_votting=self.request.user.pk,
                                                                      option_votting__in=options)[0]

        return context


class UserSearches(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'search/user_searches.html'
    model = models.Search
    paginate_by = 20
    context_object_name = 'searches'
    ordering = ['-published_search', '-publication_date_search', 'finish_date_search']
    login_url = settings.LOGIN_URL
    permission_required = 'search.view_search'
    permission_denied_message = 'Necessário usuário autorizado'

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
    permission_denied_message = 'Necessário usuário autorizado'

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
    permission_denied_message = 'Necessário usuário autorizado'

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


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='search.delete_search')
def delete_search(request):
    if request.POST:
        search = get_object_or_404(models.Search, pk=request.POST.get('primary-key'), user_search=request.user)
        search.delete()
        messages.success(request, 'Pesquisa deletada')
    return redirect(reverse('search:user_search'))
