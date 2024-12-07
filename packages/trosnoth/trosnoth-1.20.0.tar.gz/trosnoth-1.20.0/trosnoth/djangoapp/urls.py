from django.urls import path

from . import views


app_name = 'trosnoth'
urlpatterns = [
    path('', views.index, name='index'),
    path('u/', views.userList, name='userlist'),
    path('u/<int:userId>/', views.userProfile, name='profile'),
    path('u/<int:userId>/<str:nick>/', views.userProfile, name='profile'),
    path('u/<str:username>/', views.profile_by_username, name='profile'),
    path('g/', views.gameList, name='gamelist'),
    path('g/csv', views.csv_games_list, name='csvgamelist'),
    path('g/<int:gameId>/', views.viewGame, name='viewgame'),
    path('t/<int:tournamentId>/', views.tournament, name='tournament'),
    path('a/<int:arenaId>/', views.manageArena, name='arena'),
    path('a/<int:arenaId>/delete/', views.deleteArena, name='delarena'),
    path('a/<int:arenaId>/scenario/', views.startLevel, name='scenario'),
    path('a/', views.arenas, name='arenas'),
    path('a/new/', views.newArena, name='newarena'),

    path('settings', views.serverSettings, name='settings'),
    path('logs/auth', views.auth_logs, name='authlogs'),
    path('logs/arena/<int:arena_id>', views.arena_logs, name='arenalogs'),
    path('logs/bots/<int:arena_id>', views.bot_logs, name='botlogs'),
    path('shutdown', views.shutdown, name='shutdown'),
    path('restart', views.restart, name='restart'),
    path('mu', views.manageUsers, name='manageusers'),
    path('tokenauth', views.tokenAuth, name='tokenauth'),
]

