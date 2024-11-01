# functions file for plotting

# import packages
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import pandas as pd


# function to print the tables
def print_matrices_as_tables(brewery, bottler, wholesaler, bar):
    columns = ['Week', 'Order_Suppl', 'Amt_Transp', 'Amt_WIP', 'Amt_Stock', 
               'Order_Cust', 'Backlog_Cust', 'Demand_Cust', 'Delivered_Cust']
    # Convert each company's history to a DataFrame, filtering out cycle_stock and safety_stock
    df_brew = pd.DataFrame([row[:5] + row[7:] for row in brewery.history], columns=columns)
    df_bottl = pd.DataFrame([row[:5] + row[7:] for row in bottler.history], columns=columns)
    df_wholes = pd.DataFrame([row[:5] + row[7:] for row in wholesaler.history], columns=columns)
    df_bar = pd.DataFrame([row[:5] + row[7:] for row in bar.history], columns=columns)
    # Print each DataFrame as a table
    print("\nBrewery Table:")
    print(df_brew.to_string(index=False))
    print("\nBottler Table:")
    print(df_bottl.to_string(index=False))
    print("\nWholesaler Table:")
    print(df_wholes.to_string(index=False))
    print("\nBar Table:")
    print(df_bar.to_string(index=False))

# FUNCTION TO PLOT BACKLOG AND STOCK

def plot_combined_backlog_and_stock(m_brew, m_bottl, m_wholes, m_bar):
    # Define the figure and axes
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    # Extract week, backlog, and stock columns for each matrix
    weeks = [row[0] for row in m_brew]
    
    # Kombiniertes Array für Stock und Backlog
    combined_brew = [row[4] - row[8] for row in m_brew]  # Stock minus Backlog
    combined_bottl = [row[4] - row[8] for row in m_bottl]
    combined_wholes = [row[4] - row[8] for row in m_wholes]
    combined_bar = [row[4] - row[8] for row in m_bar]

    # Order of station
    order_brew = [row[1] for row in m_brew]
    order_bottl = [row[1] for row in m_bottl]
    order_wholes = [row[1] for row in m_wholes]
    order_bar = [row[1] for row in m_bar]

    # Plot combined Stock and Backlog
    axs[0].plot(weeks, combined_brew, label="Brewery Stock-Backlog", color='blue', marker='o')
    axs[0].plot(weeks, combined_bottl, label="Bottler Stock-Backlog", color='green', marker='s')
    axs[0].plot(weeks, combined_wholes, label="Wholesaler Stock-Backlog", color='orange', marker='^')
    axs[0].plot(weeks, combined_bar, label="Bar Stock-Backlog", color='red', marker='x')
    
    axs[0].set_title('Combined Stock and Backlog Over Time')
    axs[0].set_xlabel('Weeks')
    axs[0].set_ylabel('Net Stock (units)')
    axs[0].legend()
    axs[0].grid(True)

    # Plot Orders
    axs[1].plot(weeks, order_brew, label="Brewery Orders", color='blue', marker='o')
    axs[1].plot(weeks, order_bottl, label="Bottler Orders", color='green', marker='s')
    axs[1].plot(weeks, order_wholes, label="Wholesaler Orders", color='orange', marker='^')
    axs[1].plot(weeks, order_bar, label="Bar Orders", color='red', marker='x')
    
    axs[1].set_title('Orders Over Time')
    axs[1].set_xlabel('Weeks')
    axs[1].set_ylabel('Orders (units)')
    axs[1].legend()
    axs[1].grid(True)

    # Adjust the layout
    plt.tight_layout()
    plt.show()


# FUNCTION TO PLOT COSTS PER ACTOR AND ENTIRE SUPPLY CHAIN

def plot_costs_per_actor_and_supply_chain(m_brew, m_bottl, m_wholes, m_bar):
    # Extract week, backlog, and stock columns for each matrix
    weeks = [row[0] for row in m_brew]

    # Initialize cumulative cost lists for each actor and for the entire supply chain
    costs_brew = {'stock': [], 'backlog': [], 'total': []}
    costs_bottl = {'stock': [], 'backlog': [], 'total': []}
    costs_wholes = {'stock': [], 'backlog': [], 'total': []}
    costs_bar = {'stock': [], 'backlog': [], 'total': []}
    
    total_supply_chain_costs = {'stock': [], 'backlog': [], 'total': []}

    # Helper function to calculate costs
    def calculate_costs(matrix):
        stock_costs = []
        backlog_costs = []
        total_costs = []
        cum_stock = cum_backlog = cum_total = 0

        for row in matrix:
            stock_cost = row[4] * 0.5  # 0.5€ per unit of stock
            backlog_cost = row[8] * 1  # 1€ per unit of backlog
            total_cost = stock_cost + backlog_cost

            # Cumulative costs
            cum_stock += stock_cost
            cum_backlog += backlog_cost
            cum_total += total_cost

            stock_costs.append(cum_stock)
            backlog_costs.append(cum_backlog)
            total_costs.append(cum_total)

        return stock_costs, backlog_costs, total_costs

    # Calculate costs for each actor
    costs_brew['stock'], costs_brew['backlog'], costs_brew['total'] = calculate_costs(m_brew)
    costs_bottl['stock'], costs_bottl['backlog'], costs_bottl['total'] = calculate_costs(m_bottl)
    costs_wholes['stock'], costs_wholes['backlog'], costs_wholes['total'] = calculate_costs(m_wholes)
    costs_bar['stock'], costs_bar['backlog'], costs_bar['total'] = calculate_costs(m_bar)

    # Calculate total costs for the entire supply chain
    for i in range(len(weeks)):
        total_stock = costs_brew['stock'][i] + costs_bottl['stock'][i] + costs_wholes['stock'][i] + costs_bar['stock'][i]
        total_backlog = costs_brew['backlog'][i] + costs_bottl['backlog'][i] + costs_wholes['backlog'][i] + costs_bar['backlog'][i]
        total_total = costs_brew['total'][i] + costs_bottl['total'][i] + costs_wholes['total'][i] + costs_bar['total'][i]

        total_supply_chain_costs['stock'].append(total_stock)
        total_supply_chain_costs['backlog'].append(total_backlog)
        total_supply_chain_costs['total'].append(total_total)

    # print total costs of supply chain
    print(f"Total Cost of Supply Chain: ", total_total, " €")

    # Plot costs for each actor
    fig_actor, axs_actor = plt.subplots(4, 1, figsize=(10, 12))
    actors = ['Brewery', 'Bottler', 'Wholesaler', 'Bar']
    costs = [costs_brew, costs_bottl, costs_wholes, costs_bar]
    colors = ['blue', 'green', 'orange', 'red']

    for idx, actor in enumerate(actors):
        axs_actor[idx].plot(weeks, costs[idx]['stock'], label="Stock Costs", color=colors[idx], linestyle='--')
        axs_actor[idx].plot(weeks, costs[idx]['backlog'], label="Backlog Costs", color=colors[idx], linestyle=':')
        axs_actor[idx].plot(weeks, costs[idx]['total'], label="Total Costs", color=colors[idx])
        axs_actor[idx].set_title(f'{actor} Costs Over Time')
        axs_actor[idx].set_xlabel('Weeks')
        axs_actor[idx].set_ylabel('Cumulative Costs (€)')
        axs_actor[idx].legend()
        axs_actor[idx].grid(True)

    plt.tight_layout()
    plt.show()

    # Plot total costs for the entire supply chain
    fig_total, ax_total = plt.subplots(figsize=(10, 6))

    ax_total.plot(weeks, total_supply_chain_costs['stock'], label="Stock Costs", color='blue', linestyle='--')
    ax_total.plot(weeks, total_supply_chain_costs['backlog'], label="Backlog Costs", color='orange', linestyle=':')
    ax_total.plot(weeks, total_supply_chain_costs['total'], label="Total Costs", color='green')

    ax_total.set_title('Cumulative Costs of the Entire Supply Chain Over Time')
    ax_total.set_xlabel('Weeks')
    ax_total.set_ylabel('Cumulative Costs (€)')
    ax_total.legend()
    ax_total.grid(True)

    plt.tight_layout()
    plt.show()


# Funktion zum Berechnen des Servicelevels und zum Plotten
def plot_service_level(m_brew, m_bottl, m_wholes, m_bar):
    # Funktion zur Berechnung des Servicelevels für eine Matrix
    def calculate_service_level(matrix):
        demand = [row[9] for row in matrix]        # Spalte "demand_cust"
        delivered = [row[10] for row in matrix]    # Spalte "delivered_cust"
        
        service_level = [
            (delivered[i] / demand[i] * 100) if demand[i] != 0 else 100 
            for i in range(len(demand))
        ]
        return service_level

    # Servicelevel für jede Station berechnen
    service_level_brew = calculate_service_level(m_brew)
    service_level_bottl = calculate_service_level(m_bottl)
    service_level_wholes = calculate_service_level(m_wholes)
    service_level_bar = calculate_service_level(m_bar)

    # Plot des Servicelevels für jede Station
    weeks = np.arange(1, len(service_level_brew) + 1)

    plt.figure(figsize=(10, 6))

    # Linien für jede Station
    plt.plot(weeks, service_level_brew, label='Brewery', marker='o')
    plt.plot(weeks, service_level_bottl, label='Bottler', marker='x')
    plt.plot(weeks, service_level_wholes, label='Wholesaler', marker='s')
    plt.plot(weeks, service_level_bar, label='Bar', marker='d')

    # Zusätzliche Plot-Details
    plt.axhline(100, color='gray', linestyle='--', label='Ideal Service Level')
    plt.xlabel('Weeks')
    plt.ylabel('Service Level (%)')
    plt.title('Service Level over Time for Each Actor in the Supply Chain')
    plt.legend()
    plt.grid(True)

    # Plot anzeigen
    plt.show()
