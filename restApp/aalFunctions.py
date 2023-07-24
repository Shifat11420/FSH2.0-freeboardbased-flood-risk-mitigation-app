import numpy as np
import random


def get_probability():
    return (random.uniform(0, 1))


def inv_flood_depth(x, u, a):
    return u - a * np.log(-(np.log(1-x)))


def aal_building(livableArea, buildingReplacementValue, ffh, gumbelLocation, gumbelScale, buildingLossFunction, insurance, coverageValueA=150000, deductibleValueA=1500, num_samples=50000):
    sum_of_str = 0
    sum_of_homeowner = 0
    sum_of_nfip = 0
    for i in range(num_samples):
        x = get_probability()
        d = inv_flood_depth(x, gumbelLocation, gumbelScale)
        ds = d - ffh

        build_dam = (buildingReplacementValue/100) * (np.interp(ds,
                                                                buildingLossFunction[buildingLossFunction.columns[0]], buildingLossFunction[buildingLossFunction.columns[1]]))
        # build_dam = ((0.0015*(ds**3)-0.3373*(ds**2)+9.0339*ds+15.413)/100) * building_value  #building loss in dollars
        if build_dam < 0:
            build_dam = 0  # if damage is negative, put 0
        if build_dam > buildingReplacementValue:
            build_dam = buildingReplacementValue
        str_dam = build_dam

        # loss allocation
        if insurance == "Yes":
            if str_dam < coverageValueA:
                str_deduct_owner = [
                    deductibleValueA if str_dam > deductibleValueA else str_dam][0]
                str_deduct_nfip = str_dam-str_deduct_owner
            elif str_dam > coverageValueA:
                str_deduct_owner = deductibleValueA + (str_dam-coverageValueA)
                str_deduct_nfip = str_dam-str_deduct_owner
        else:
            str_deduct_owner = str_dam
            str_deduct_nfip = 0

        sum_of_str += str_dam
        sum_of_homeowner += str_deduct_owner
        sum_of_nfip += str_deduct_nfip

    return [float(sum_of_str/num_samples), float(sum_of_homeowner/num_samples), float(sum_of_nfip/num_samples),]


def aal_contents(livableArea, buildingReplacementValue, ffh, gumbelLocation, gumbelScale, contentsLossFunction, insurance, coverageValueC=100000, deductibleValueC=1500, num_samples=50000):
    sum_of_str = 0
    sum_of_homeowner = 0
    sum_of_nfip = 0
    for i in range(num_samples):
        x = get_probability()
        d = inv_flood_depth(x, gumbelLocation, gumbelScale)
        ds = d - ffh

        cont_dam = (buildingReplacementValue/100) * (np.interp(ds,
                                                               contentsLossFunction[contentsLossFunction.columns[0]], contentsLossFunction[contentsLossFunction.columns[1]]))
        if cont_dam < 0:
            cont_dam = 0  # if damage is negative, put 0
        if cont_dam > buildingReplacementValue:
            cont_dam = buildingReplacementValue
        str_dam = cont_dam

        # loss allocation
        if insurance == "Yes":
            if str_dam < coverageValueC:
                str_deduct_owner = [
                    deductibleValueC if str_dam > deductibleValueC else str_dam][0]
                str_deduct_nfip = str_dam-str_deduct_owner
            elif str_dam > coverageValueC:
                str_deduct_owner = deductibleValueC + (str_dam-coverageValueC)
                str_deduct_nfip = str_dam-str_deduct_owner
        else:
            str_deduct_owner = str_dam
            str_deduct_nfip = 0

        sum_of_str += str_dam
        sum_of_homeowner += str_deduct_owner
        sum_of_nfip += str_deduct_nfip

    return [float(sum_of_str/num_samples), float(sum_of_homeowner/num_samples), float(sum_of_nfip/num_samples),]


def aal_others(livableArea, buildingReplacementValue, ffh, gumbelLocation, gumbelScale, unitDisplacementCost, unitMovingCost, num_samples=50000):
    Lr = 0
    Cd = 0
    Cm = 0
    # Ri = 0
    # Tri = 0
    Wh = 0
    for i in range(num_samples):
        x = get_probability()
        d = inv_flood_depth(x, gumbelLocation, gumbelScale)
        ds = d - ffh

        # Landlord Rental loss
        if ds <= 0:
            St = 0
        if 0 < ds <= 4:
            St = np.interp(ds, [0, 4], [9, 12])
        elif 4 < ds <= 8:
            St = np.interp(ds, [4, 8], [12, 15])
        elif ds > 8:
            St = 24

        # building_value_rent = (1+(fbcp/100)) * building_value
        # annual_rent = building_value_rent/22.07
        # building_value_fb = (1+(fbcp/100)) * building_value

        # current_rent =  buildingReplacementValue/22.07
        # annual_rent = current_rent * (1+(fbri/100))
        annual_rent = buildingReplacementValue/22.07
        # Landlord, Tenant Rental income/loss/increase (no income if restoration time is greater than a year)
        if St <= 0:
            rental_loss = 0
            # rental_income = annual_rent
            # tenant_rent_increase = annual_rent
        else:
            rental_loss = (St/12) * annual_rent
            # rental_income = (1-(St/12)) * annual_rent
            # tenant_rent_increase = (11/12) * annual_rent

        # if rental_income<0:
        #     rental_income = 0
        # Ri += rental_income
        Lr += rental_loss
        # Tri +=  tenant_rent_increase
        #######################
        # Displacement cost
        if ds > 0:
            displ_cost = unitDisplacementCost * 30
            Cd += displ_cost
        else:
            displ_cost = 0
        ######################
        # Moving cost
        if ds > 0:
            moving_cost = unitMovingCost * livableArea
            Cm += moving_cost
        else:
            moving_cost = 0
        ######################
        # Working hour loss
        if ds > 0:
            working_hour_lost = 40*1.45*29.81
            Wh += working_hour_lost
        else:
            working_hour_lost = 0

    return [float(Lr/num_samples), float(Cd/num_samples), float(Cm/num_samples), float(Wh/num_samples),]
