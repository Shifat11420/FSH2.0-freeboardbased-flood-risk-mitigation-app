
#def home_equity_loan (home_condition= "Existing", federal_assistance= "No", investment_type="Loan", Ce=150, Cc=110, fc=2.3, down_payment=20, A=2000, r=3, t=10):
def home_equity_loan(inputs): 
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
    if inputs['home_condition'] == "Existing":
        cost_elevation = inputs['Ce'] * inputs['A']
        if inputs['federal_assistance'] == "Yes":
            return {"Federal_Assistance": cost_elevation}      # need revision here
        else:
            if inputs['investment_type'] == "No Loan":
                return {"Homeowner_Portion": cost_elevation}
            else:  
                r_ = inputs['r']/100
                monthly_loan_payment = cost_elevation * ((r_/12) / (1- ((1+(r_/12))**(-12*inputs['t']))))
                return {"Monthly_Payment": monthly_loan_payment}

    else:
        cost_freeboard = inputs['Cc'] * inputs['A'] * (inputs['fc']/100)
        if inputs['investment_type'] == "No Loan":
            return {"Homeowner_Portion": cost_freeboard}
        else:     
            if inputs['down_payment']<20:
                monthly_mortgage_insurance = (cost_freeboard - (cost_freeboard*inputs['down_payment']/100)) * 2/100   # need revision here
            else:
                monthly_mortgage_insurance = 0
            other_fees = 500     # need revision here
            r_ = inputs['r']/100
            monthly_loan_payment = ((cost_freeboard - cost_freeboard*inputs['down_payment']/100 ) * ((r_/12) / (1- ((1+(r_/12))**(-12*inputs['t']))))) + monthly_mortgage_insurance 
   
            down_payment_toreturn = other_fees + cost_freeboard*inputs['down_payment']/100
            return {"Down_Payment":down_payment_toreturn, "Monthly_Payment":monthly_loan_payment}
  