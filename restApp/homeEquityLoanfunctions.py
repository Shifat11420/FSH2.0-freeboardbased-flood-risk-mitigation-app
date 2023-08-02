
def home_equity_loan_function(home_condition, federal_assistance, investment_type, Ce, Cc, fc, down_payment, A, r, t):
#def home_equity_loan(inputs): 
    """
    Parameters
    ----------
    home_condition : Existing/New 
        The default is "Existing".
    federal_assistance : Yes/No
        The default is "No".
    investment_type : without loan/ loan
        The default is "Loan".
    Ce : Unit cost of elevation
        The default is 150.
    Cc : Unit cost of construction 
        The default is 110.
    fc : freeboard cost
        The default is 2.3.
    down_payment : input as %
        The default is 20%.
    A : Livable Area
        The default is 2000.
    r : interest rate
        The default is 3%.
    t : Loan period
        The default is 10 years.

    Returns
    -------
    Monthly/Total Amount in dollars
        
    """
    if str(home_condition) == "Existing":
        cost_elevation = Ce * A
        if str(federal_assistance) == "Yes":
            return {"Federal_Assistance": cost_elevation}      # need revision here
        else:
            if str(investment_type) == "No Loan":
                return {"Homeowner_Portion": cost_elevation}
            else:  
                r_ = r/100
                monthly_loan_payment = cost_elevation * ((r_/12) / (1- ((1+(r_/12))**(-12*t))))
                return {"Monthly_Payment": monthly_loan_payment}

    else:
        cost_freeboard = Cc * A * (fc/100)
        if str(investment_type) == "No Loan":
            return {"Homeowner_Portion": cost_freeboard}
        else:     
            if down_payment<20:
                monthly_mortgage_insurance = (cost_freeboard - (cost_freeboard*down_payment/100)) * 2/100   # need revision here
            else:
                monthly_mortgage_insurance = 0
            other_fees = 500     # need revision here
            r_ = r/100
            monthly_loan_payment = ((cost_freeboard - cost_freeboard*down_payment/100 ) * ((r_/12) / (1- ((1+(r_/12))**(-12*t))))) + monthly_mortgage_insurance 
   
            down_payment_toreturn = other_fees + cost_freeboard*down_payment/100
            return {"Down_Payment":down_payment_toreturn, "Monthly_Payment":monthly_loan_payment}
  