from django.urls import path
from .views import *


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('operating_status/', AboutPageView.as_view(), name='operating_status'), 
    path('tables/', get_tables_names_list, name='tables'),
    path('generated/<str:table_name>', show_af_operations_model, name='generate'),
    path('requests/', your_query_list, name='requests'),
    path('chart/', show_chart, name='chart'),  # this for js chart(not used)
    path('requests/<str:your_query>', view_your_query , name='your_query'),

]

