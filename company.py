class Company:
    def __init__(self, name, initial_order, amt_transp, amt_wip, amt_stock, cycle_stock, safety_stock):
        self.name = name
        self.week = 0
        self.order_cust = initial_order
        self.amt_transp = amt_transp
        self.amt_wip = amt_wip
        self.amt_stock = amt_stock
        self.order_suppl = initial_order
        self.backlog = 0
        self.demand_cust = initial_order
        self.delivered_cust = 0
        # preparation for later
        self.cycle_stock = cycle_stock
        self.safety_stock = safety_stock
        # making history
        self.history = []  # Stores weekly values as a list

    def save_weekly_data(self):
    # Speichert die wöchentlichen Werte als Liste und hängt sie an die history an
        self.history.append([
            self.week, self.order_cust, self.amt_transp, self.amt_wip, self.amt_stock,
            self.order_suppl, self.cycle_stock, self.safety_stock, self.backlog,
            self.demand_cust, self.delivered_cust
    ])

