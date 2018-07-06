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
from .lib.analyzer import Analyzer
from calendarapp import config
from datetime import datetime



class Home(View):
    """
    ==============

    ``Home``
    ----------

    .. py:class:: Home()


    .. note::
    .. todo::
    """
    def get(self, request, *args, **kwargs):
        """
        .. py:attribute:: get()

           :param request:
           :type request:
        .. note::
        .. todo::
        """
        form = QueryForm(self.request.GET)
        if request.user.is_superuser:
            return render(self.request,
                      'calendarapp/index.html',
                        {'form': form,
                         'base':'home'})
        return render(self.request,
                    'calendarapp/availability.html',
                    {'base':'home',
                     'error': ''})

    def post(self, request, *args, **kwargs):
        """
        .. py:attribute:: post()

           :param request:
           :type request:
        .. note::
        .. todo::
        """
        form = QueryForm(self.request.POST)
        page = int(request.GET.get('page', 0))
        if page == 0:
            return render(self.request,
                          'calendarapp/index.html',
                          {'form': form,
                           'error': "Not implemented yet",
                           'base':'home'})

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
                    result = self.reformat(
                        analyzer.available_interviewers(candidate, interviewer)
                        )
                else:
                    result = self.reformat(
                        analyzer.available_candidates(candidate, interviewer)
                        )
                all_pages = Paginator(results, config.ROW_NUMBER)
                return render(self.request,
                      'calendarapp/index.html',
                        {'form': form,
                         'page': all_pages.get_page(page),
                         'result': result,
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


    .. note::
    .. todo::
    """
    def get(self, request, *args, **kwargs):
        """
        .. py:attribute:: get()

           :param request:
           :type request:
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

       :param request:
       :type request:
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

       :param request:
       :type request:
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
            return redirect(reverse('home'))
        else:
            return render(request,
                  'registration/signup.html',
                  {'form': form})
    return render(request,
                  'registration/signup.html',
                  {'form': RegistrationForm()})
