# main file for running simulations

# import packages
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import pandas as pd

# import seperate .py-files into main
import functions as f
import plotting as p
from company import Company


# CONSTANTS
# simulation constants
std_dev = 2
avg_demand = 10
sim_time = 30
cost_stock = 0.5
cost_blog = 1
np.random.seed(42)

# Starting conditions/amounts for the companies
# Depends on the rules
init_amt_transp = 4
init_amt_wip = 4
init_amt_stock = 12
init_order = 4
# TBDD
init_cycle_stock = 8
init_safety_stock = 8

# Initialize the Company objects with corresponding attributes
# supplier has 'unlimited' stock and needs less info
supplier = Company("Supplier", init_order, init_amt_transp, init_amt_wip, 10000, 0, 0)
brewery = Company("Brewery", init_order, init_amt_transp, init_amt_wip, init_amt_stock, init_cycle_stock, init_safety_stock)
bottler = Company("Bottler", init_order, init_amt_transp, init_amt_wip, init_amt_stock, init_cycle_stock, init_safety_stock)
wholesaler = Company("Wholesaler", init_order, init_amt_transp, init_amt_wip, init_amt_stock, init_cycle_stock, init_safety_stock)
bar = Company("Bar", init_order, init_amt_transp, init_amt_wip, init_amt_stock, init_cycle_stock, init_safety_stock)

# List of Company objects
companies = [supplier, brewery, bottler, wholesaler, bar]

# SIMULATION
# start simulation, define starting vector and start weekly cycle
def sim():

    # loop for sim_time
    for i in range(1, sim_time+1):
        # marker for each week
        print(f"\n--- Week {i} ---")

        # Loop through each company to update the week
        for company in companies:
            # update current week in the company object
            company.week = i

        # Set customer demand for the bar
        demand_guest = int(f.generate_positive_normal(avg_demand, std_dev))
        # demand_guest = 8 if i > 7 else 4
        #demand_guest = 20
        # pass on demand to bar
        bar.order_cust = demand_guest

        # Loop through each company to process production and transport
        for company in companies:  # skip the first supplier
            # Move products from WIP into stock
            f.move_to_stock(company)
            # Move products from transport into WIP
            f.move_to_wip(company)

        for company in companies:
            # Calculate customer demand
            f.calc_demand_cust(company)
            # Calculate delivery amount
            del_amt = f.calc_delivery(company)
            # Dispatch order to the customer
            f.move_to_transp(company, companies, del_amt)

        for company in companies:
            # determine order amount from the supplier
            # f.calc_order_suppl_v1(company)
            f.calc_order_suppl_v2(company, bar)
        
        for company in companies[1:]:  # Skip supplier for weekly data storage
            # save the data in the history
            company.save_weekly_data()

        for company in reversed(companies[1:]):  # Start from the last and go backwards
            f.pass_order(company, companies)

    # PLOTTING
    # Print tables
    p.print_matrices_as_tables(brewery, bottler, wholesaler, bar)
    # plotting backlog and stock in four diagrams
    p.plot_combined_backlog_and_stock(brewery, bottler, wholesaler, bar)
    # plotting the costs of the four actors
    p.plot_costs_per_actor_and_supply_chain(brewery, bottler, wholesaler, bar)
    # # plotting the costs of the complete chain
    # p.plot_service_level(m_brew, m_bottl, m_wholes, m_bar)
    
    return
        
#RUN
sim()
