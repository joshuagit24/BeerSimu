# functions file for scripts

# import packages
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import pandas as pd
from company import Company

# FUNCTIONS
def generate_positive_normal(mean, std_dev):
    # Set lower limit to 0, and use the standard deviation and mean for the normal distribution
    a = 0  # lower limit
    b = np.inf  # no upper limit
    # Calculate the truncation
    lower_limit = (a - mean) / std_dev
    upper_limit = (b - mean) / std_dev
    # Generate a random number from the truncated normal distribution
    return truncnorm.rvs(lower_limit, upper_limit, loc=mean, scale=std_dev)

# Move products from WIP into stock
def move_to_stock(company):
    print(f"{company.name} - Before move_to_stock: WIP={company.amt_wip}, Stock={company.amt_stock}")
    company.amt_stock += company.amt_wip
    company.amt_wip = 0
    print(f"{company.name} - After move_to_stock: WIP={company.amt_wip}, Stock={company.amt_stock}")

# Move products from transport into WIP
def move_to_wip(company):
    print(f"{company.name} - Before move_to_wip: Transport={company.amt_transp}, WIP={company.amt_wip}")
    company.amt_wip = company.amt_transp
    company.amt_transp = 0
    print(f"{company.name} - After move_to_wip: Transport={company.amt_transp}, WIP={company.amt_wip}")

# Calculate demand of customer (order current week + backlog)
def calc_demand_cust(company):
    company.demand_cust = company.order_cust + company.backlog
    print(f"{company.name} - Calculated demand: {company.demand_cust} (Order Cust: {company.order_cust}, Backlog: {company.backlog})")

# Calculate the amount to be delivered 
def calc_delivery(company):
    if company.amt_stock >= company.demand_cust:
        delivery_amt = company.demand_cust
        company.amt_stock -= delivery_amt
        company.backlog = 0
    else:
        delivery_amt = company.amt_stock
        company.amt_stock = 0
        company.backlog = (company.demand_cust - delivery_amt)
    print(f"{company.name} - Delivery amount: {delivery_amt}, Stock left: {company.amt_stock}, Backlog: {company.backlog}")
    return delivery_amt

# Dispatch products to transport in direction of customer
def move_to_transp(company, companies, del_amt):
    idx = companies.index(company)
    if idx < len(companies) - 1:  # Skip for the last company in line
        next_company = companies[idx + 1]
        company.delivered_cust = del_amt
        # company.amt_stock -= del_amt
        next_company.amt_transp = del_amt
        print(f"{company.name} - Dispatched {del_amt} to {next_company.name} (Transport={next_company.amt_transp})")
    else:
        # Special handling for Bar (last in line)
        company.delivered_cust = del_amt
        print(f"{company.name} - Delivered {del_amt} to customer")

# Calculate the ordered amount
# Version 1: order the amount that the customer took
def calc_order_suppl_v1(company):
    company.order_suppl = company.order_cust
    print(f"{company.name} - Calculated order to supplier: {company.order_suppl}")

# Version 2: order the amount that the bar-customer took
def calc_order_suppl_v2(company, bar):
    company.order_suppl = bar.order_cust
    print(f"{company.name} - Calculated order to supplier: {company.order_suppl}")


# Pass the order up the supply chain (from Bar towards Supplier)
def pass_order(company, companies):
    idx = companies.index(company)
    if idx > 0:  # Skip for supplier, which has no preceding company
        previous_company = companies[idx - 1]
        # Set the order_cust of the current company as order_suppl of the previous one
        previous_company.order_cust = company.order_suppl
        print(f"{previous_company.name} received order_suppl: {previous_company.order_suppl} from {company.name}")

