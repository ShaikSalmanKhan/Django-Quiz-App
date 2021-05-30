from django.urls import path
from App.views import home, quiz_page, save_to_database, result, dashboard

urlpatterns = [
    path('',home,name="home"),
    path('quiz_page', quiz_page,name="quiz"),
    path('save_to_database',save_to_database,name="save"),
    path('result_page',result,name="result"),
    path('dashboard_page',dashboard,name="dashboard"),
]
