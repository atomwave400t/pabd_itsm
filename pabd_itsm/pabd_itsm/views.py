# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from itsm.models import  Service_request, Work_journal, Asset, Status, ITSM_User
from itsm.itsm_forms import editUserForm, editServiceRequestForm, workJournalForm, editAssetForm, UserAuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta
import datetime
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import login, authenticate, logout
#Person
# Create your views here.

def index(request):
    return render(request, 'pabd_itsm/base.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home/')


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return HttpResponseRedirect('/home/')


    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            ulogin = request.POST['login']
            upassword = request.POST['password']
            print("przed")
            user = authenticate(login=ulogin, password=upassword)
            print(type(user), type(request))
            if user:
                print(type(user), type(request))
                login(request, user)
                return HttpResponseRedirect('/home/')

    else:
        form = UserAuthenticationForm()

    context['login_form'] = form

    return render(request, 'pabd_itsm/login.html', context)


def searchAssets(request):
    names = ['asset_owner_login','asset_business_unit','asset_serial_number','asset_title','asset_code_name','asset_status',
            'asset_type']
    if request.GET:
        if ('asset_owner_login' or 'asset_business_unit'
        or 'asset_serial_number' or 'asset_title'
        or 'asset_code_name' or 'asset_status' or 'asset_type') in request.GET:

            asset_owner_login = request.GET['asset_owner_login']
            asset_business_unit = request.GET['asset_business_unit']
            asset_serial_number = request.GET['asset_serial_number']
            asset_title = request.GET['asset_title']
            asset_code_name = request.GET['asset_code_name']
            asset_status = request.GET['asset_status']
            asset_type = request.GET['asset_type']
            all_assets = Asset.objects.filter(
            Q(title__icontains=asset_title) &
            Q(business_unit_id__name__icontains=asset_business_unit) &
            Q(serial_number__icontains=asset_serial_number) &
            Q(code_name__icontains=asset_code_name) &
            Q(status_id__name__icontains=asset_status) &
            Q(asset_type__name__icontains=asset_type) &
            Q(person_id__login__icontains=asset_owner_login))

            #all_assets = Asset.objects.all()
            print("cos sie udalo" + str(all_assets) + ", : " + asset_serial_number)
            return all_assets
        else:
            return []
    else:
        return []


def assets(request):
    searched_assets = searchAssets(request)
    if  searched_assets != []:
        return render(request, 'pabd_itsm/assets.html', {'searched_assets': searched_assets})
    else:
        return render(request, 'pabd_itsm/assets.html')


def assetDetails(request):
    asset_id = request.GET['asset_id']
    passed_object = Asset.objects.get(id=asset_id)
    form = editAssetForm(request.POST or None, instance=passed_object)
    if form.is_valid():
        newAsset = form.save()
        return HttpResponseRedirect('/assets/')

    else:
        print(form.errors)
        form_class = editAssetForm

    return render(request, 'pabd_itsm/assetDetails.html', {'form': form_class, 'asset': passed_object})



def ticketSolve(request):
    ticket_id = request.GET['ticket_id']
    ticket = Service_request.objects.get(id=ticket_id)
    status = Status.objects.get(name="SOLVED")

    ticket.status_id = status
    ticket.end_date = datetime.datetime.now()

    ticket.save()
    #ticket.status_id.save(force_update=True)

    print("po: "+str(ticket.status_id.name))
    print("Zrobilo sie")
    return HttpResponseRedirect("/tickets/queue/")


def ticketTake(request):
    ticket_id = request.GET['ticket_id']
    ticket = Service_request.objects.get(id=ticket_id)
    curr_user = ITSM_User.objects.get(login=request.user)
    ticket.owner_id = curr_user
    ticket.save()
    return HttpResponseRedirect("/tickets/ticketDetails/?ticket_id=" + str(ticket_id) + "&work_journal_page=1")


def newWorkRecord(request):
    ticket_id = request.GET['ticket_id']
    title = request.GET['work_record_title']
    description = request.GET['work_record_description']
    is_internal = False

    try:
        if request.GET['is_internal']:
            is_internal = True
    except MultiValueDictKeyError:
        is_internal = False

    ticket = Service_request.objects.get(id=ticket_id)
    person = ITSM_User.objects.get(login="krzysztof.kunysz")
    work_record=Work_journal(record_title=title, record_description=description,
                            service_request_id=ticket, is_internal=is_internal, author_id=person)
    work_record.save()

    return HttpResponseRedirect(("/tickets/ticketDetails/?ticket_id=" + str(ticket_id) + "&work_journal_page=1"))


def ticketSuspend(request):
    ticket_id = request.GET['ticket_id']
    suspend_time = request.POST['suspend_time']
    ticket = Service_request.objects.get(id=ticket_id)

    ticket.resume_date = datetime.datetime.now() + timedelta(hours=int(suspend_time))
    status = Status.objects.get(name="SUSPENDED")
    ticket.status_id = status
    ticket.save()

    return HttpResponseRedirect("/tickets/ticketDetails/?ticket_id=" + str(ticket_id) + "&work_journal_page=1")


#czeka do czasu skonczenia logowania
def assignTicketToMe(request, ticket_id, current_user):
    current_ticket = Service_request.objects.get(id=ticket_id)
    current_ticket.owner_id = current_user
    current_ticket.save()

    return HttpResponseRedirect("/tickets/ticketDetails/?ticket_id=" + str(ticket_id) + "&work_journal_page=1")


#kolejka zgloszen
def ticketQueue(request):
    new_requests = Service_request.objects.filter(Q(owner_id__isnull=True) & Q(status_id='NEW'))
    suspended_requests = Service_request.objects.filter(status_id='SUSPENDED')
    queued_requests = Service_request.objects.filter(Q(status_id='QUEUED') & Q(owner_id__isnull=True)).order_by('priority')

    your_tickets = Service_request.objects.filter(owner_id=request.user)

    return render(request, 'pabd_itsm/queue.html', {'new_requests': new_requests,
                                                    'suspended_requests': suspended_requests,
                                                    'queued_requests': queued_requests,
                                                    'your_tickets': your_tickets})


def workJournal(request, work_journal, page_num):
    paginator = Paginator(work_journal, 5)

    try:
        journal_records = paginator.page(page_num)
    except PageNotAnInteger:
        journal_records = paginator.page(1)
    except EmptyPage:
        journal_records = paginator.page(paginator.num_pages)

    return [journal_records, paginator.num_pages]



def ticketDetails(request):
    ticket_id = request.GET['ticket_id']

    if request.GET.get('work_journal_page'):
        page = request.GET['work_journal_page']
    else:
        page = 1

    passed_object = Service_request.objects.get(id=ticket_id)
    form = editServiceRequestForm(request.POST or None, instance=passed_object)
    work_journal_essentials = workJournal(request.GET, Work_journal.objects.filter(service_request_id=ticket_id).order_by('-creation_date'), page)
    work_journal = work_journal_essentials[0]
    work_journal_pages = work_journal_essentials[1]

    if passed_object.asset_id:
        asset = Asset.objects.get(id=passed_object.asset_id.id)
    else:
        asset = None

    if form.is_valid():
        newPerson = form.save()
        return HttpResponseRedirect(("/tickets/ticketDetails/?ticket_id=" + str(ticket_id) + "&work_journal_page=" + page))

    else:
        print(form.errors)
        form_class = editServiceRequestForm

    return render(request, 'pabd_itsm/ticketDetails.html', {'form': form_class,
                                                            'ticket': passed_object,
                                                            'work_journal': work_journal,
                                                            'asset': asset,
                                                            'journal_pages': work_journal_pages})


#wyszukiwanie uzytkownikow
def searchPersons(request):
    names = ['person_name','person_surname','person_login','person_type','person_business_unit','person_job_title']
    if request.GET:
        if ('person_name' or 'person_surname' or 'person_login' or 'person_type' or 'person_business_unit' or 'person_job_title') in request.GET:
            person_name = request.GET['person_name']
            person_surname = request.GET['person_surname']
            person_login = request.GET['person_login']
            person_type = request.GET['person_type']
            person_business_unit = request.GET['person_business_unit']
            person_job_title = request.GET['person_job_title']

            all_persons = ITSM_User.objects.filter(
            Q(name_id__name__icontains=person_name) &
            Q(surname__icontains=person_surname) &
            Q(login__icontains=person_login) &
            Q(user_type_id__name__icontains=person_type) &
            Q(business_unit_id__name__icontains=person_business_unit) &
            Q(job_title__icontains=person_job_title) )
            return all_persons
        else:
            return []
    else:
        return []


def personDetails(request):
    person_login = request.GET['person_login']
    passed_object = ITSM_User.objects.get(login=person_login)
    form = editUserForm(request.POST or None, instance=passed_object)
    if form.is_valid():
        newPerson = form.save()
        return HttpResponseRedirect('/persons/')

    else:
        print(form.errors)
        form_class = editUserForm

    return render(request, 'pabd_itsm/personDetails.html', {'form': form_class, 'person': passed_object})
    # dodac zakladanie calego uzytkownika


def ticketCreate(request):
    form = editServiceRequestForm(request.POST or None, initial={"status_id": "EXO_TEX_CRO"})
    if form.is_valid():
        newTicket = form.save()
        return HttpResponseRedirect('/tickets/queue/')
    else:
        print(form.errors)
        form_class = editServiceRequestForm

    return render(request, 'pabd_itsm/ticketCreate.html', {'form': form_class})


def persons(request):
    searched_persons = searchPersons(request)

    if  searched_persons != []:
        return render(request, 'pabd_itsm/persons.html', {'searched_persons': searched_persons})
    else:
        return render(request, 'pabd_itsm/persons.html')
