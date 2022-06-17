get_data_by_query_one = """
        SELECT TOP (300)  [time],  sum(value) as energy, customer, energy_central
        FROM [operations].[energy_central_sales_hourly] as table1
	    INNER JOIN operations.autologic_description as table2
	    ON table1.source = table2.name_input
	    Group by energy_central, customer, [time]
	    order by [time], energy_central
    """
get_data_by_query_two = """
        SELECT TOP (300)  [time],  sum(value) as energy, customer
        FROM [operations].[energy_central_sales_hourly] as table1
	    INNER JOIN operations.autologic_description as table2
	    ON table1.source = table2.name_input
	    where energy_central = 'Torgvartalet Energisentral'
	    Group by customer, [time]
    """
get_data_by_query_three = """
        SELECT energy_central, year(time) as year,MONTH(time) as mo,
        CONCAT(year(time), format(MONTH(time),'-00')) as year_mo,
        customer,  sum([value_current]) as energy_consumption FROM [operations].[energy_centrals_hourly] as table1 
		INNER JOIN operations.autologic_description as table2 
		on table1.source = table2.name_input 
		where energy_central = 'Torgvartalet Energisentral' and sales_category = 'Sales' 
		group by customer, energy_central, month(time), year(time) 
		order by  year(time), month(time), customer 
    """

get_data_by_query_four = """
        SELECT energy_central, year(time) as year,MONTH(time) as mo, 
        CONCAT(year(time), format(MONTH(time),'-00')) as year_mo, 
        customer,  sum([value_current]) as energy_consumption FROM [operations].[energy_centrals_hourly] as table1 
		INNER JOIN operations.autologic_description as table2 
		on table1.source = table2.name_input 
		where energy_central = 'Billingstad Energisentral' and sales_category = 'Sales' 
		group by customer, energy_central, month(time), year(time) 
		order by  year(time), month(time), customer 
    """
