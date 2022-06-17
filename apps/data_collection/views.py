from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
import src.connect as connect
import pandas as pd
from .query_list import *
import seaborn as sns
import matplotlib.pyplot as plt
from .forms import MyForm

conn = connect.connect_to_afdvh_database()
table_names_list = []
query_dict = {
    'three': get_data_by_query_three,
    'four': get_data_by_query_four,
}

normal_table_names = ['Energy Central', 'Year', 'Month', 'Year-Month', 'Customer', 'Energy Consumption']


def view_your_query(request, your_query):
    for key, value in query_dict.items():
        if key == your_query:
            df = pd.read_sql(sql=value, con=conn)

            # convert to dict and back to pandas to get round consuption
    query_one_dict = df.to_dict()
    test_list2 = {}
    test_list2 = query_one_dict.copy()
    for key, value in query_one_dict.items():
        if key == 'energy_consumption':
            for x, y in value.items():
                y = round((y / 100), 1)
                test_list2['energy_consumption'][x] = y
    df = pd.DataFrame.from_dict(test_list2)
    # print(type(df))

    plt.switch_backend(
        'AGG')  # The Anti-Grain Geometry (Agg) rendering engine, capable of rendering high-quality images
    plt.rcParams['axes.facecolor'] = '#C0C0C0'  # plot set color
    # plt.figure(figsize=(19.2, 10.8), dpi=91.79) # size 1920 x 1080, (dpi  not required)
    plt.figure(figsize=(25.6, 14.4))  # size 1920 x 1080, (dpi  not required)
    plt.grid(color='#fafade', linewidth=0.7)
    # plt.cla() # plt.cla() clears an axes, i.e. the currently active axes in the current figure.
    plt.title(get_ecentrals_name(df), fontsize=25)
    plt.xticks(rotation=65)

    sns.set(font_scale=1.5)  # axis font size (numbers, date)
    chart = sns.barplot(x='year_mo', y='energy_consumption', hue='customer', data=df)
    chart.patch.set_edgecolor('black')
    chart.patch.set_linewidth('4')
    chart.set_xlabel("Year-Month", fontsize=18)
    chart.set_ylabel("Energy Consumption (MWh)", fontsize=18)

    plt.savefig('static/data_collection_web/media/plot.png',
                bbox_inches='tight')  # bbox_inches='tight' remove white spaces around chart

    query_one_values = df.to_numpy()
    get_query_one_columns_names = query_one_dict.keys()

    consumptions = []
    # consumptions.clear()
    for key, value in query_one_dict.items():
        if key == 'energy_consumption':
            for x in value.values():
                consumptions.append(x)

    # =====================new form======================

    form = MyForm()
    form.fields['customer'].choices = get_customers(df)
    form.fields['from_year_mo'].choices = get_date(df)
    form.fields['to_year_mo'].choices = get_date(df)

    try:

        if request.method == 'POST':
            form = MyForm(request.POST)
            form.fields['customer'].choices = get_customers(df)
            form.fields['from_year_mo'].choices = get_date(df)
            form.fields['to_year_mo'].choices = get_date(df)

            if form.is_valid():
                plt.xticks(rotation=75)
                cd = form.cleaned_data  # here we getting data from web form choices as dictionary
                if cd['customer'] == 'SELECT ALL':
                    update_data = f"""
                        SELECT energy_central, year(time) as year,MONTH(time) as mo, 
                        CONCAT(YEAR([time]), '-', RIGHT(CONCAT('00', MONTH([time])), 2)) as year_mo, 
                        customer,  sum([value_current]) as energy_consumption FROM [operations].[energy_centrals_hourly] as table1 
                        INNER JOIN operations.autologic_description as table2 
                        on table1.source = table2.name_input 
                        where energy_central = '{get_ecentrals_name(df)}' and sales_category = 'Sales' and
                        CONCAT(YEAR([time]), '-', RIGHT(CONCAT('00', MONTH([time])), 2)) between '{cd['from_year_mo']}' and '{cd['to_year_mo']}'
                        group by customer, energy_central, month(time), year(time)
                        order by  year(time), month(time), customer"""
                else:
                    update_data = f"""
                        SELECT energy_central, year(time) as year,MONTH(time) as mo,
                        CONCAT(YEAR([time]), '-', RIGHT(CONCAT('00', MONTH([time])), 2)) as year_mo,
                        customer,  sum([value_current]) as energy_consumption
                        FROM [operations].[energy_centrals_hourly] as table1
                        INNER JOIN operations.autologic_description as table2
                        on table1.source = table2.name_input
                        where energy_central = '{get_ecentrals_name(df)}' and
                        sales_category = 'Sales' and customer = '{cd['customer']}' and
                        CONCAT(YEAR([time]), '-', RIGHT(CONCAT('00', MONTH([time])), 2)) between '{cd['from_year_mo']}' and '{cd['to_year_mo']}'
                        group by customer, energy_central, month(time), year(time)
                        order by  year(time), month(time), customer
                        """

                df = pd.read_sql(sql=update_data, con=conn)

                # convert to dict and back to pandas to get round consuption
                query_one_dict = df.to_dict()
                test_list2 = {}
                test_list2 = query_one_dict.copy()
                for key, value in query_one_dict.items():
                    if key == 'energy_consumption':
                        for x, y in value.items():
                            y = round((y / 100), 1)
                            test_list2['energy_consumption'][x] = y
                df = pd.DataFrame.from_dict(test_list2)
                plt.grid(color='#fafade', linewidth=0.7)

                plt.cla()  # plt.cla() clears an axes, i.e. the currently active axes in the current figure.
                chart.patch.set_edgecolor('black')
                chart.patch.set_linewidth('3')
                chart = sns.barplot(x='year_mo', y='energy_consumption', hue='customer', data=df)
                chart.set_xlabel("Year-Month", fontsize=18)
                chart.set_ylabel("Energy Consumption (MWh)", fontsize=18)
                # chart.set(ylim=(0, 100))
                plt.title(get_ecentrals_name(df), fontsize=20)
                plt.xticks(rotation=65)

                plt.savefig('static/data_collection_web/media/plot.png', bbox_inches='tight')

                query_one_dict = df.to_dict()
                query_one_values = df.to_numpy()
                get_query_one_columns_names = query_one_dict.keys()
                consumptions.clear()

                for key, value in query_one_dict.items():
                    if key == 'energy_consumption':
                        for x in value.values():
                            consumptions.append(x)

    except ValueError as e:
        print(e)
        messages.warning(request, '---- Wrong date selection !!! ----')

    # convert to numpy , for print in html as table 
    numpy_table = pd.DataFrame(test_list2)
    numpy_table = numpy_table.to_numpy()

    data = {
        # 'query_objects': query_one_values,
        'query_objects': numpy_table,
        'query_table_fields': get_query_one_columns_names,
        'query_name': your_query,
        'chart': chart,
        'e_central': get_ecentrals_name(df),
        'customer': get_customers(df),
        'dates': get_date(df),
        'year': get_year(df),
        'month': get_month(df),
        'form': form,
        'energy_consumption_sum': round(sum(consumptions), 0),
        'customers': get_customers_list(df),
        'normal_table_names': normal_table_names,
    }

    return render(request, 'view_request.html', data)


def get_customers_list(df):
    customers = []
    for value in df.get('customer'):
        if value not in customers:
            customers.append(value)

    return customers


def get_customers(df):
    customers_list = []
    customers_to_tuple = []
    for value in df.get('customer'):
        if value not in customers_list:
            customers_list.append(value)
    for item in customers_list:
        customers_to_tuple.append([item, item])
    customers_to_tuple.append(['SELECT ALL', 'SELECT ALL'])
    customers = tuple(customers_to_tuple)
    return customers


def get_ecentrals_name(df):
    centrale = ''
    for value in df.get('energy_central'):
        centrale = value
    return centrale


def get_year(df):
    year_list = []
    year_to_tuple = []
    for value in df.get('year'):
        if value not in year_list:
            year_list.append(value)
    for item in year_list:
        year_to_tuple.append([item, item])
    year = tuple(year_to_tuple)
    return year


def get_to_year(df):
    year_list = []
    year_to_tuple = []
    for value in df.get('year'):
        if value not in year_list:
            year_list.append(value)
    for item in year_list:
        year_to_tuple.append([item, item])
    year = tuple(year_to_tuple)
    return year


def get_month(df):
    month_list = []
    month_to_tuple = []
    for value in df.get('mo'):
        if value not in month_list:
            month_list.append(value)
    for item in month_list:
        month_to_tuple.append([item, item])
    month_to_tuple.sort()
    month = tuple(month_to_tuple)
    return month


def get_to_month(df):
    month_list = []
    month_to_tuple = []
    for value in df.get('mo'):
        if value not in month_list:
            month_list.append(value)
    for item in month_list:
        month_to_tuple.append([item, item])
    month_to_tuple.sort()
    month = tuple(month_to_tuple)
    return month


def get_date(df):
    dates = []
    dates_to_tuple = []
    for value in df.get('year_mo'):
        # start = value[:4]
        # end = value[4:]
        # value = start + ' ' + end
        if value not in dates:
            dates.append(value)
    for item in dates:
        dates_to_tuple.append([item, item])
    dates_to_tuple.sort()
    dates = tuple(dates_to_tuple)

    return dates


def your_query_list(request):
    data = {
        'query_list': query_dict.keys(),
    }

    return render(request, 'show_special_request.html', data)


def get_tables_names_list(request):
    table_names_list.clear()
    get_operations_tables_names = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES
    """
    df = pd.read_sql(sql=get_operations_tables_names, con=conn)
    t_names = df.to_dict()

    for n in t_names.values():
        for x in n.values():
            if x != 'database_firewall_rules':
                table_names_list.append(x)

    data = {
        'table_names_list': table_names_list,
    }

    return render(request, 'show_all_tables.html', data)


def show_af_operations_model(request, table_name):
    sql_query = """
        SELECT TOP (400) * FROM operations.{}""".format(table_name)

    df = pd.read_sql(sql=sql_query, con=conn)
    var_to_numpy = df.to_numpy()
    dict = df.to_dict()
    get_columns_names = dict.keys()

    data = {
        'table_objects': var_to_numpy,
        'table_fields': get_columns_names,
        'table_name': table_name
    }

    return render(request, 'dinamic.html', data)


# future jobs

class HomePageView(TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'operating_status.html'


# charts.js extra job

def show_chart(request):
    data = {

    }
    return render(request, 'show_chart.html', data)
