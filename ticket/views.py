# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import unicode_literals
from django.views.generic.edit import CreateView, UpdateView

from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group

from django.utils import timezone
from .models import TicketRequest
from .forms import TicketForm
from django.http import HttpResponseRedirect
from river.models import State



@login_required
def home(request):
    return render(request, 'ticket/home.html')


@login_required
def ticket_overview(request):
    #ticket = TicketRequest.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    ticket = TicketRequest.objects.filter(author=request.user).order_by('published_date')
    return render(request, 'ticket/ticket_overview.html', {'ticket': ticket})


@login_required
def ticket_new(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.published_date = timezone.now()
            ticket.save()
            return HttpResponseRedirect('/ticket/ticket_sent')
    form = TicketForm()
    return render(request, 'ticket/ticket_form.html', {'form': form, })


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(TicketRequest, pk=pk)
    return render(request, 'ticket/ticket_detail.html', {'ticket': ticket})


#@login_required
#def actions(request):
    #return render(request, 'ticket/actions.html')


@login_required
def denied(request):
    return render(request, 'ticket/denied.html')


# Declaration of a test function for the different user groups developer, Key user and Team Leader/Manager
def in_developer_group(user):
    if user:
        return user.groups.filter(name='Developer').count() == 1
    return False


def in_key_users_group(user):
    if user:
        return user.groups.filter(name='Key users').count() == 1
    return False


def in_team_leader_group(user):
    if user:
        return user.groups.filter(name='Team Leader Dep A').count() == 1
    return False


@login_required
@user_passes_test(in_team_leader_group, login_url='/ticket/denied/')
def ticket_process(request):
    # ticket = TicketRequest.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # ticket = TicketRequest.objects.filter(author=request.user).order_by('published_date')
    # ticket = TicketRequest.objects.filter(department = request.user.groups.filter(name='Key users')).order_by('published_date')
    ticket = TicketRequest.objects.filter(request.user.groups(name='Team Leader Dep A')).order_by('published_date')
    return render(request, 'ticket/ticket_process.html', {'ticket': ticket})


@login_required
@user_passes_test(in_developer_group, login_url='/ticket/denied/')
def actions(request):
    ticket = TicketRequest.objects.exclude(status='Open').order_by('published_date')
    return render(request, 'ticket/actions.html', {'ticket': ticket})


@login_required
@user_passes_test(in_developer_group, login_url='/ticket/denied/')
def dashboard(request):
    pie_chart = TicketRequest.objects.filter(published_date__lte=timezone.now()).order_by('published_date').count()
    pie_chart2 = TicketRequest.objects.filter(application_id=3).count(id)
    #ticket = TicketRequest.objects.exclude(status='Open').order_by('published_date')
    return render(request, 'ticket/dashboard.html',
                  {'pie_chart': pie_chart},
                  {'pie_chart2': pie_chart2})


#class IndexView(generic.ListView):
#    template_name = 'ticket/dashboard.html'
#    context_object_name = 'all_tickets'
#
#    def get_queryset(self):
#        return TicketRequest.objects.all().order_by('published_date')

#    def get_context_data(self, **kwargs):
#        context = super(IndexView, self).get_context_data(**kwargs)
#        context['Notebook'] = TicketRequest.objects.filter(application='Notebook').count()
#        # Add any other variables to the context here
#        return context



@login_required
def ticket_sent(request):
    return render(request, 'ticket/ticket_sent.html')


def proceed_ticket(request, ticket_id, next_state_id=None):
    ticket = get_object_or_404(TicketRequest, pk=ticket_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:

        ticket.proceed(request.user, next_state=next_state)
        return redirect(reverse('admin:ticket_ticketrequest_changelist'))
    except Exception as e:
        return HttpResponse(e.message)


# @login_required
def user_logout(request):
    logout(request)
    return render(request, 'ticket/registration/logout.html')


