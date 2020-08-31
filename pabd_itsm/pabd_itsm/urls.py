from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.index),
    path('logout/', views.logout_view, name="logout"),
    path('login/', views.login_view, name="login"),
    path('assets/', views.assets),
    path('assets/assetDetails/', views.assetDetails),
    path('searchAssets/', views.searchAssets),
    path('persons/', views.persons),
    path('searchPersons/', views.searchPersons),
    path('persons/personDetails/', views.personDetails),
    path('tickets/create/', views.ticketCreate),
    path('tickets/queue/', views.ticketQueue),
    path('tickets/ticketDetails/', views.ticketDetails),
    path('tickets/solve/', views.ticketSolve),
    path('tickets/suspend/', views.ticketSuspend),
    path('tickets/take/', views.ticketTake),
    path('workJournal/newWorkRecord/', views.newWorkRecord)
]
