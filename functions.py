# functions file for scripts

# import packages
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import pandas as pd

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

# save the vector data into matrix for KPI
def save_into_matrix(m_list, vector, v_list):
    m_list[v_list.index(vector)].append(vector.copy())
    return m_list

# move products from wip into stock
def move_to_stock(company):
    company.amt_stock += company.amt_wip
    company.amt_wip = 0

# move products from transport into wip
def move_to_wip(company):
    company.amt_wip = company.amt_transp
    company.amt_transp = 0

# calculate demand of customer (order current week + backlog)
def calc_demand_cust(company):
    company.demand_cust = company.order_cust + company.backlog

# pass the order (tbf propably)
def pass_order(company, companies):
    idx = companies.index(company)
    if idx > 0:  # Skip for supplier, which has no preceding company
        previous_company = companies[idx - 1]
        company.order_cust = previous_company.order_suppl

# calculate the amount to be delivered 
def calc_delivery(company):
    if company.amt_stock >= company.demand_cust:
        # complete demand is met
        delivery_amt = company.demand_cust
        company.amt_stock -= delivery_amt
        company.backlog = 0
    else:
        # only partial delivery due to shortage
        delivery_amt = company.amt_stock
        company.amt_stock = 0
        company.backlog += (company.demand_cust - delivery_amt)
    return delivery_amt

# dispatch products to transport in direction of customer
def move_to_transp(company, companies, del_amt):
    idx = companies.index(company)
    if idx < len(companies) - 1:  # Skip for the last company in line
        next_company = companies[idx + 1]
        company.delivered_cust = del_amt
        next_company.amt_transp = del_amt
  
# calculate the ordered amount
# TBD 
# version 1: order the amount that the customer took
def calc_order_suppl_v1(company):
    company.order_suppl = company.order_cust
