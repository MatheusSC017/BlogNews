from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db.models import Max, Count
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib import messages
from django.shortcuts import reverse, redirect, get_object_or_404
from django.utils import timezone
from . import models, forms
from report.models import Report
from utils.utils import verify_recaptcha


class Searches(ListView):
    """ Shows all the published searches """
    template_name = 'search/searches.html'
    model = models.Search
    context_object_name = 'searches'
    paginate_by = 5
    ordering = ['-publication_date', 'finish_date', ]

    def get_queryset(self):
        """ Make sure the search has been published and the publication date is less than or equal to now """
        qs = super().get_queryset()

        qs = qs.filter(published=True,
                       publication_date__lte=timezone.now())

        return qs

    def get_context_data(self, *args, **kwargs):
        """ Add the options of the questions and the number of votes """
        context = super().get_context_data(*args, **kwargs)

        searches = list()
        for search in context['searches']:
            options = models.Option.objects.filter(search=search.pk)
            options = options.annotate(
                vote=Count('vottinguseroption')
            )
            searches.append({'search': search,
                             'options': options,
                             'status': (search.finish_date > timezone.now()),
                             'max_vote': options.aggregate(Max('vote'))})
        context['searches'] = searches

        return context


class Search(DetailView):
    """ Show the question with its options and if is open to new answers """
    template_name = 'search/search.html'
    model = models.Search
    context_object_name = 'search'

    def get(self, request, *args, **kwargs):
        """ Show the question if it has been published and the publication data is less than or equal to now """
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if not context['search'].published or context['search'].publication_date > timezone.now():
            return redirect(reverse('search:searches'))

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """ Create or update the user votting """
        recaptcha_response = self.request.POST.get('g-recaptcha-response')

        if not verify_recaptcha(recaptcha_response):
            messages.warning(request, 'ReCaptcha inválido')
            return redirect(reverse('search:search', args=[kwargs.get('pk'), ]))

        if not request.user.is_authenticated:
            return redirect(reverse('user:login'))

        search = get_object_or_404(models.Search,
                                   pk=kwargs.get('pk'),
                                   published=True,
                                   publication_date__lte=timezone.now(),
                                   finish_date__gte=timezone.now())
        option = get_object_or_404(models.Option,
                                   pk=request.POST['optionChoice'],
                                   search=search.pk)
        votting = models.VottingUserOption.objects.filter(user=request.user.pk,
                                                          option__in=models.Option.objects.filter(
                                                              search=search.pk
                                                          ))
        if votting.count() == 0:
            models.VottingUserOption.objects.create(user=request.user,
                                                    option=option)
        else:
            votting = votting[0]
            votting.option = option
            votting.save()
        messages.success(request, 'Obrigado pelo voto')
        return redirect(reverse('search:search', args=[search.pk, ]))

    def get_context_data(self, *args, **kwargs):
        """
        Include the options and markers such as the user-selected option, the option with the most votes,
        and whether the question is open to new answers
        """
        context = super().get_context_data(*args, **kwargs)

        options = models.Option.objects.filter(search=context['search'].pk)
        options = options.annotate(
            vote=Count('vottinguseroption')
        )
        context['options'] = options
        context['max_vote'] = options.aggregate(Max('vote'))
        context['status'] = (context['search'].finish_date > timezone.now())
        if self.request.user.is_authenticated:
            context['vote'] = models.VottingUserOption.objects.filter(user=self.request.user.pk,
                                                                      option__in=options).first

        return context


class UserSearches(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Shows all the user questions """
    template_name = 'search/user_searches.html'
    model = models.Search
    paginate_by = 20
    context_object_name = 'searches'
    ordering = ['-published', '-publication_date', 'finish_date']
    login_url = settings.LOGIN_URL
    permission_required = 'search.view_search'
    permission_denied_message = 'Necessário usuário autorizado'

    def get_queryset(self):
        """ Select only the user questions """
        qs = super().get_queryset()

        qs = qs.filter(user=self.request.user)

        return qs


class CreateSearch(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Page to create a new question """
    template_name = 'search/search_form.html'
    model = models.Search
    form_class = forms.SearchForm
    login_url = settings.LOGIN_URL
    permission_required = 'search.add_search'
    permission_denied_message = 'Necessário usuário autorizado'

    def get_context_data(self, *args, **kwargs):
        """ Add the option form to the context """
        context = super().get_context_data(*args, **kwargs)

        if kwargs.get('option_form'):
            context['option_form'] = kwargs.get('option_form')
        else:
            context['option_form'] = forms.OptionInlineForm()

        return context

    def form_valid(self, form):
        """ Make sure the form is valid and add the required fields """
        option_form = forms.OptionInlineForm(data=self.request.POST)

        if option_form.is_valid() and form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            option_form.instance = self.object
            option_form.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form, option_form)

    def form_invalid(self, form, option_form):
        """ Show again the page if the form is invalid """
        return self.render_to_response(
            self.get_context_data(
                form=form,
                option_form=option_form
            )
        )

    def get_success_url(self):
        """ Success message """
        messages.success(self.request, 'Pesquisa cadastrada')
        return reverse('search:user_search')


class UpdateSearch(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Page to update the selected question """
    template_name = 'search/search_form.html'
    model = models.Search
    form_class = forms.SearchForm
    login_url = settings.LOGIN_URL
    permission_required = 'search.change_search'
    permission_denied_message = 'Necessário usuário autorizado'

    def get(self, request, *args, **kwargs):
        """ Show the page is the question belongs to the user """
        self.object = self.get_object()

        if self.object.user != request.user:
            return redirect(reverse('search:user_search'))

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Make sure the question belongs to the user """
        self.object = self.get_object()

        if self.object.user != request.user:
            return redirect(reverse('search:user_search'))

        return super().post(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """ Add the option form to the context """
        context = super().get_context_data(*args, **kwargs)

        if kwargs.get('option_form'):
            context['option_form'] = kwargs.get('option_form')
        else:
            context['option_form'] = forms.OptionInlineForm(instance=self.object)

        return context

    def form_valid(self, form):
        """ Make sure the form is valid and add the required fields """
        option_form = forms.OptionInlineForm(data=self.request.POST, instance=self.object)

        if option_form.is_valid() and form.is_valid():
            self.object.save()
            option_form.instance = self.object
            option_form.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form, option_form)

    def form_invalid(self, form, option_form):
        """ Show the page again if the form is invalid """
        return self.render_to_response(
            self.get_context_data(
                form=form,
                option_form=option_form
            )
        )

    def get_success_url(self):
        """ Success message """
        messages.success(self.request, 'Pesquisa atualizada')
        return reverse('search:user_search')


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='search.delete_search')
def delete_search(request):
    """ Delete the user question """
    if request.POST:
        search = get_object_or_404(models.Search, pk=request.POST.get('primary-key'), user=request.user)
        search.delete()
        messages.success(request, 'Pesquisa deletada')
    return redirect(reverse('search:user_search'))


def register_report(request):
    if not request.POST:
        return redirect(reverse('search:searches'))

    pk = request.POST.get('primary-key')

    if not pk:
        messages.error(request, 'Pesquisa não encontrado')
        return redirect(reverse('search:searches'))

    search = get_object_or_404(models.Search, pk=pk, published=True)
    report_description = request.POST.get('report-description')

    if not report_description.strip():
        messages.error(request, 'A denúncia não pode estar vázia')
        return redirect(reverse('search:search', kwargs={'pk': pk, }))

    description = 'Pesquisa: {}, Autor: {} - {}'.format(pk, search.user, report_description)

    Report.objects.create(user=search.user, description=description)
    messages.success(request, 'Sua denúncia foi registrada')
    return redirect(reverse('search:search', kwargs={'pk': pk, }))
