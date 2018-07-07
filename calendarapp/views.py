"""
===== 
views.py 
===== 

"""

from django.shortcuts import render, redirect
from django.views import View
from .forms import InterviewerForm, CandidateForm, QueryForm, RegistrationForm
from .models import InterviewerModel, CandidateModel, QueryRequest
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as authlogin
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.urls import reverse
from django.core.cache import cache
from .lib.analyzer import Analyzer
from calendarapp import config
from datetime import datetime



class Home(View):
    """
    ==============

    ``Home``
    ----------

    .. py:class:: Home()
    Home view which is responsible for the home page contents.

    .. note::
    .. todo::
    """
    def get(self, request, *args, **kwargs):
        """
        .. py:attribute:: get()
        Home's get method that is responsible for showing pages > 2
        for query requests and the very first time the home url is called. 
           :param request: request object
           :type request: request object
        .. note::
        .. todo::
        """
        page_num = int(request.GET.get('page', 0))
        form = QueryForm(self.request.GET)
        if page_num == 0 and request.user.is_superuser:
            return render(self.request,
                          'calendarapp/index.html',
                          {'form': form,
                           'base':'home'})

        elif request.user.is_superuser:
            all_pages = cache.get("all_pages")
            page_range = range(max(0, page_num - 3), min(all_pages.count, page_num + 3))
            page = all_pages.get_page(page_num)
            return render(self.request,
                      'calendarapp/index.html',
                        {'form': form,
                         'page': page,
                         'has_previous': page.has_previous(),
                         'page_range': page_range,
                         'error': '',
                         'has_other_pages': page.has_other_pages(),
                         'base':'home'})

        return render(self.request,
                    'calendarapp/index.html',
                    {'base':'home',
                     'error': """Wellcom, Please complete your registration process by
                                    adding your availability times.""",})

    def post(self, request, *args, **kwargs):
        """
        .. py:attribute:: post()
        Home's post method responsible for showin query results.
           :param request: request object
           :type request: request object
        .. note::
        .. todo::
        """
        form = QueryForm(self.request.POST)


        if form.is_valid():
            query = form.cleaned_data['query_type']
            candidate_email = form.cleaned_data['candidate']
            interviewer = form.cleaned_data['interviewer']
            analyzer = Analyzer()
            if query == 'AI':
                # The result here is a dictionary with pairs of
                # timestaps as keys and available interviewers
                # as values. If only candidate is provided otherwise
                # the same result for interviewer
                if candidate_email:
                    result = analyzer.available_interviewers(candidate, interviewer)
                else:
                    result = analyzer.available_candidates(candidate, interviewer)
                all_pages = Paginator(results, config.ROW_NUMBER)
                cache.set("all_pages", all_pages)
                page = all_pages.get_page(1)
                page_range = range(0, 3)
                return render(self.request,
                      'calendarapp/index.html',
                        {'form': form,
                         'page': all_pages.get_page(page),
                         'page': page,
                         'has_other_pages': page.has_other_pages(),
                         'has_previous': page.has_previous(),
                         'page_range': page_range,
                         'th_list': config.query_th,
                         'base':'home'})
            else:
                return render(self.request,
                      'calendarapp/index.html',
                        {'form': form,
                         'error': "Not implemented yet",
                         'base':'home'})


class Availability(View):
    """
    ==============

    ``Availability``
    ----------

    .. py:class:: Availability()
    Handling the requests come from availability url.

    .. note::
    .. todo::
    """
    def get(self, request, *args, **kwargs):
        """
        .. py:attribute:: get()
        load the availability page for inserting the respective
        data.
           :param request: request object
           :type request: request object
        .. note::
        .. todo::
        """
        if request.user.has_perm('calendarapp.interviewer'):
            form = InterviewerForm()
        elif not request.user.is_anonymous:
            form = CandidateForm()
        else:
            return render(self.request,
                      'calendarapp/index.html',
                        {'base':'home'})
        return render(self.request,
                      'calendarapp/availability.html',
                        {'form': form,
                         'base':'home'})
    
    def post(self, request, *args, **kwargs):
        """
        .. py:attribute:: post()
        post the respective availability data and act accordingly.
           :param request:
           :type request:
        .. note::
        .. todo::
        """
        if request.user.has_perm('calendarapp.interviewer'):
            model = InterviewerModel()
        else:
            model = CandidateModel()

        model.user = request.user
        # kwargs['available_dates'] is a list of timestap pairs
        # It can be converted to integers as:
        # [(int(i), int(j)) for i,j in kwargs['available_dates']]
        model.available_dates = kwargs['available_dates']
        model.save()

def login(request):
    """
    ==============

    ``login``
    ----------

    .. py:function:: login(['request'])
    Authemticate users that are already registered.
       :param request: request object
       :type request: request object
    .. note::
    .. todo::
    """
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        error = "An unhandeled error occurred! please contant Kasra that's his fault! ;))"
        try:
            user = authenticate(request, username=username, password=password)
        except KeyError:
            error = 'Fill in all fields!'
        else:
            if user is not None:
                # user is registered
                authlogin(request, user)
                return redirect(reverse('home'))
            else:
                error = "Invalid username and/or password!"
    return render(request,
                  'registration/login.html',
                  {'form': AuthenticationForm(),
                   'error': error})


def signup_view(request):
    """
    ==============

    ``signup_view``
    ----------

    .. py:function:: signup_view(['request'])
    Register users and create a candidate based on the new user.
       :param request: request object
       :type request: request object
    .. note::
    .. todo::
    """
    if request.method == 'POST':
        data = request.POST
        form = RegistrationForm(data)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            authlogin(request, new_user)
            model = CandidateModel()
            model.user = new_user
            model.available_dates = []
            model.save()
            return redirect(reverse('home'))
        else:
            return render(request,
                  'registration/signup.html',
                  {'form': form})
    return render(request,
                  'registration/signup.html',
                  {'form': RegistrationForm()})
