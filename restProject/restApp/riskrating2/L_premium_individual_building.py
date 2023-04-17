import pandas as pd
import numpy as np
risk_rating_2 = pd.DataFrame(columns=["Items","Inland Flood Fluvial Buldings","Inland Flood Fluvial Contents",
                                      "Inland Flood Pluvial Buldings","Inland Flood Pluvial Contents",
                                      "Storm Surge Buldings","Storm Surge Contents",
                                      "Tsunami Buldings","Tsunami Contents",
                                      "Great Lakes Buldings","Great Lakes Contents",
                                      "Coastal Erosion Buldings","Coastal Erosion Contents", "All Perils (All Coverages)"],
                         index = range(0,59))
risk_rating_2['Items'] = ["Base Rate (per $1000 of Coverage Value)", "Distance to River","Elevation Relative to River by River Class","Drainage Area","Leveed Structural Relative Elevation","Distance to Coast","Distance to Ocean","Elevation", "Distance to Lake","Elevation Relative to Lake","Levee Quality", "Territory (HUC12 & Levee ID Indicator)",
                          "Geographic Rate by Peril & Coverage","Type of Use","Floor of Interest", "Foundation Type","First Floor Height by Foundation Design & Flood Vents","M&E above First Floor","Coverage Value Factor","Deductible & Limit to Coverage Value Ratio","Deductible to Coverage Value Ratio","Initial Deductible & ITV","Final Deductible & ITV",
                          "Concentration Risk","CRS Discount Percentage","CRS Discount Factor","Rate by Peril & Coverage","Rate (per $1000 of Buildig Value)", "Rate (per $1000 of Contents Value)", "Rate Weights by Coverage", "Weighted Deductible & ITV Factor (Building)","Weighted Deductible & ITV Factor (Contents)","Minimum Rate (per $1000 of Buildig Value)","Maximum Rate (per $1000 of Buildig Value)",
                          "Minimum Rate (per $1000 of Contents Value)","Maximum Rate (per $1000 of Contents Value)","Minimum Rate by Peril & Coverage (per $1000 of Coverage Value)","Maximum Rate by Peril & Coverage (per $1000 of Coverage Value)","Final Rate (per $1000 of Building Value)","Final Rate (per $1000 of Contents Value)", "Coverage Value in Thousands (Buildings)","Coverage Value in Thousands (Contents)",
                          "Initial Premium without Fees (Buildings)","Initial Premium without Fees (Contents)","Initial Premium without Fees","Prior Claims Premium","Premium excluding Fees & Expense Constant","Expense Constant", "Loss Constant", "Premium without Fees","ICC Premium","ICC Premium with CRS Discount","Subtotal","Reserve Fund Factor","Subtotal","Probation Surcharge","HFIAA Surcharge by Primary Residence Indicator",
                          "Federal Policy Fee", "Premium with Fees"]

def L_premium(path,path1,inputs):
    base_rate = pd.read_excel(path1+'BaseRates - '+inputs['Levee'] + '.xlsx')
    base_rate_data = (base_rate[(base_rate['Region']==inputs['State']) & (base_rate['Single Family Home Indicator']== inputs['Single family home indicator'])])
    #segment = base_rate_data.iloc[0]['Segment']
    #inland flood
    risk_rating_2.iloc[0,1] = base_rate_data.iloc[0][3]
    risk_rating_2.iloc[0,2] = base_rate_data.iloc[0][4]
    risk_rating_2.iloc[0,3] = base_rate_data.iloc[0][5]
    risk_rating_2.iloc[0,4] = base_rate_data.iloc[0][6]
    #storm surge
    risk_rating_2.iloc[0,5] = base_rate_data.iloc[0][7]
    risk_rating_2.iloc[0,6] = base_rate_data.iloc[0][8]
    # tsunami   
    risk_rating_2.iloc[0,7] = base_rate_data.iloc[0][9]
    risk_rating_2.iloc[0,8] = base_rate_data.iloc[0][10]
    #great lake
    risk_rating_2.iloc[0,9] = base_rate_data.iloc[0][11]
    risk_rating_2.iloc[0,10] = base_rate_data.iloc[0][12]
    #coastal
    risk_rating_2.iloc[0,11] = base_rate_data.iloc[0][13]
    risk_rating_2.iloc[0,12] = base_rate_data.iloc[0][14]
    #####DTR
    if inputs['DTR'] != 'N/A' and inputs['DTR'] <=1700:
        dist_river = pd.read_excel(path1+'DTR - '+inputs['Levee']+ '.xlsx')    
        B1 = np.interp([inputs['DTR']],(dist_river[dist_river.columns[0]]),(dist_river[dist_river.columns[1]]))
        B2 = np.interp([inputs['DTR']],(dist_river[dist_river.columns[0]]),(dist_river[dist_river.columns[2]]))
    risk_rating_2.iloc[1,1] = round(float(B1),4)
    risk_rating_2.iloc[1,2] = round(float(B1),4)
    risk_rating_2.iloc[1,3] = round(float(B2),4)
    risk_rating_2.iloc[1,4] = round(float(B2),4)
    ####Elevation Relative ot River   
    if inputs['ERR'] != 'N/A':
        elev_river = pd.read_excel(path1+'ElevRelRiver - '+inputs['Levee'] + '.xlsx')        
        elev_river = elev_river[(elev_river['River Class']== 'Class '+str(inputs['River class']))]
        elev_river = elev_river.drop([elev_river.columns[0]],axis=1)
        elev_river = elev_river.astype('float64')
        C1 = np.interp([inputs['ERR']],(elev_river[elev_river.columns[0]]),(elev_river[elev_river.columns[1]]))
        C2 = np.interp([inputs['ERR']],(elev_river[elev_river.columns[0]]),(elev_river[elev_river.columns[2]]))  
        risk_rating_2.iloc[2,1] = round(float(C1),4)
        risk_rating_2.iloc[2,2] = round(float(C1),4)
        risk_rating_2.iloc[2,3] = round(float(C2),4)
        risk_rating_2.iloc[2,4] = round(float(C2),4)
    #####Drainage Area
    risk_rating_2.iloc[3][1:5] = 1.0

    ########Str Elevation
    str_elev = pd.read_excel(path1+'StructRelElev - '+inputs['Levee']+ '.xlsx')
    str_elev = str_elev.astype('float64')
    E1 = np.interp([inputs['SRE']],(str_elev[str_elev.columns[0]]),(str_elev[str_elev.columns[1]]))
    E2 = np.interp([inputs['SRE']],(str_elev[str_elev.columns[0]]),(str_elev[str_elev.columns[2]]))
    
    risk_rating_2.iloc[4,1] = round(float(E1),4)
    risk_rating_2.iloc[4,2] = round(float(E1),4)
    risk_rating_2.iloc[4,3] = round(float(E2),4)
    risk_rating_2.iloc[4,4] = round(float(E2),4)
    #####DTC  
    if inputs['DTC'] != 'N/A':
        dtc_ce = pd.read_excel(path1+'DTC - CE - '+inputs['Levee']+ '.xlsx')
        dtc_ce = dtc_ce.astype('float64')
        coast = np.interp([inputs['DTC']],(dtc_ce[dtc_ce.columns[0]]),(dtc_ce[dtc_ce.columns[1]]))

        dtc_ss = pd.read_excel(path1+'DTC - SS - '+inputs['Levee']+ '.xlsx')
        if inputs['State'] != "LA":
            dtc_ss = dtc_ss[(dtc_ss['Region']== "Non-LA")]
        else:
            dtc_ss = dtc_ss[(dtc_ss['Region']== inputs['State'] )]
        dtc_ss = dtc_ss.drop([dtc_ss.columns[0]],axis=1)
        dtc_ss = dtc_ss.astype('float64')      
        storm = np.interp([inputs['DTC']],(dtc_ss[dtc_ss.columns[0]]),(dtc_ss[dtc_ss.columns[1]]))

        dtc_tsu = pd.read_excel(path1+'DTC - TSU - '+inputs['Levee']+ '.xlsx')
        dtc_tsu = dtc_tsu[(dtc_tsu['Region'] == inputs['State'])]
        if len(dtc_tsu)!=0:
            dtc_tsu = dtc_tsu.drop([dtc_tsu.columns[0]],axis=1)
            dtc_tsu = dtc_tsu.astype('float64')    
            tsunami = np.interp([inputs['DTC']],(dtc_tsu[dtc_tsu.columns[0]]),(dtc_tsu[dtc_tsu.columns[2]]))
        else:
            tsunami = np.nan
    
        risk_rating_2.iloc[5,5] = round(float(storm),4)
        risk_rating_2.iloc[5,6] = round(float(storm),4)
        risk_rating_2.iloc[5,7] = round(float(tsunami),4)
        risk_rating_2.iloc[5,8] = round(float(tsunami),4)
        risk_rating_2.iloc[5,11] = round(float(coast),4)
        risk_rating_2.iloc[5,12] = round(float(coast),4)
    ################DTO
    if inputs['DTO'] != 'N/A':
        dto = pd.read_excel(path1+'DTO - '+inputs['Levee']+ '.xlsx')
        dto = dto[(dto['Region']== inputs['State'])]
        if len(dto)!=0:
            dto = dto.drop([dto.columns[0]],axis=1)
            dto = dto.astype('float64')
            F = np.interp([inputs['DTO']],(dto[dto.columns[0]]),(dto[dto.columns[1]]))
            risk_rating_2.iloc[6,7] = round(float(F),4)
            risk_rating_2.iloc[6,8] = round(float(F),4)
    ###############Elevation
    Elev_ifss = pd.read_excel(path1+'Elevation - IFSS - '+inputs['Levee']+ '.xlsx')
    if inputs['State'] != "LA":
        Elev_ifss = Elev_ifss[(Elev_ifss['Region']== "Non-LA")]
    else:
        Elev_ifss = Elev_ifss[(Elev_ifss['Region']== inputs['State'])]
    
    Elev_ifss = Elev_ifss.drop([Elev_ifss.columns[0]],axis=1)
    Elev_ifss = Elev_ifss.astype('float64')    
    
    iff = np.interp([inputs['Elevation']],(Elev_ifss[Elev_ifss.columns[0]]),(Elev_ifss[Elev_ifss.columns[1]]))
    ifp = np.interp([inputs['Elevation']],(Elev_ifss[Elev_ifss.columns[0]]),(Elev_ifss[Elev_ifss.columns[2]]))
    ss = np.interp([inputs['Elevation']],(Elev_ifss[Elev_ifss.columns[0]]),(Elev_ifss[Elev_ifss.columns[3]]))
    
    Elev_tsu = pd.read_excel(path1+'Elevation - TSU - '+inputs['Levee']+ '.xlsx')
    Elev_tsu = Elev_tsu[(Elev_tsu['Region']== inputs['State'])]
    Elev_tsu = Elev_tsu.drop([Elev_tsu.columns[0]],axis=1)
    Elev_tsu = Elev_tsu.astype('float64')    

    if len(Elev_tsu) !=0:
        tsunami = np.interp([inputs['Elevation']],(Elev_tsu[Elev_tsu.columns[0]]),(Elev_tsu[Elev_tsu.columns[1]]))
    else:
        tsunami = np.nan
   
    risk_rating_2.iloc[7,1] = round(float(iff),4)
    risk_rating_2.iloc[7,2] = round(float(iff),4)
    risk_rating_2.iloc[7,3] = round(float(ifp),4)
    risk_rating_2.iloc[7,4] = round(float(ifp),4)
    risk_rating_2.iloc[7,5] = round(float(ss),4)
    risk_rating_2.iloc[7,6] = round(float(ss),4)
    risk_rating_2.iloc[7,7] = round(float(tsunami),4)
    risk_rating_2.iloc[7,8] = round(float(tsunami),4)
    ##################DTL
    
    if inputs['DTL']=='N/A':
        risk_rating_2.iloc[8,9] = 0.525
        risk_rating_2.iloc[8,10] = 0.525
    else:
        dist_lake = pd.read_excel(path1+'DTL - '+inputs['Levee']+ '.xlsx')
        I = np.interp([inputs['DTL']],(dist_lake[dist_lake.columns[0]]),(dist_lake[dist_lake.columns[1]]))
        risk_rating_2.iloc[8,9] = round(float(I),4)
        risk_rating_2.iloc[8,10] = round(float(I),4)
    ##############ElevLake
    if inputs['DTL']=='N/A':
        risk_rating_2.iloc[9,9] = 0.004
        risk_rating_2.iloc[9,10] = 0.004
    
    else:
        elev_lake =  pd.read_excel(path1+'ElevRelLake - '+inputs['Levee']+ '.xlsx')  
        J = np.interp([inputs['ERL']],(elev_lake[elev_lake.columns[0]]),(elev_lake[elev_lake.columns[1]]))
        risk_rating_2.iloc[9,9] = round(float(J),4)
        risk_rating_2.iloc[9,10] = round(float(J),4)   
    #############Levee Quality
    levee_qual =  pd.read_excel(path1+'Levee Quality - '+inputs['Levee']+ '.xlsx') 
    levee_qual = levee_qual.loc[levee_qual['Levee System ID'] == int(inputs['Levee System ID'])]
    
    iff = levee_qual[levee_qual.columns[3]]
    risk_rating_2.iloc[10,1] = round(float(iff),4)
    risk_rating_2.iloc[10,2] = round(float(iff),4)    
    ################Territory     
    territory = pd.read_excel(path+'/tables/Territory - TSU'+ '.xlsx') 
    territory = territory[territory['HUC12']== int(inputs['HUC12'])]
    if len(territory)!=0:
        risk_rating_2.iloc[11,7] = round(float(territory[territory.columns[1]]),4)
        risk_rating_2.iloc[11,8] = round(float(territory[territory.columns[1]]),4)
    territory = pd.read_excel(path+'/tables/Territory - GL'+ '.xlsx') 
    territory = territory[territory['HUC12']== int(inputs['HUC12'])]
    if len(territory)!=0:
        risk_rating_2.iloc[11,9] = round(float(territory[territory.columns[1]]),4)
        risk_rating_2.iloc[11,10] = round(float(territory[territory.columns[1]]),4)
 
    ##
    territory = pd.read_excel(path1+'Territory - IFSS - '+inputs['Levee']+ '.xlsx') 
    territory = territory[territory['HUC12']== int(inputs['HUC12'])]
    territory = territory[territory['Levee System ID']== int(inputs['Levee System ID'])]
    risk_rating_2.iloc[11,1] = round(float(territory[territory.columns[2]]),4)
    risk_rating_2.iloc[11,2] = round(float(territory[territory.columns[2]]),4)
    risk_rating_2.iloc[11,3] = round(float(territory[territory.columns[2]]),4)
    risk_rating_2.iloc[11,4] = round(float(territory[territory.columns[2]]),4)
    risk_rating_2.iloc[11,5] = round(float(territory[territory.columns[3]]),4)
    risk_rating_2.iloc[11,6] = round(float(territory[territory.columns[3]]),4)
    #######################type of use
    type_use = pd.read_excel(path+"/tables/"+'Type of Use'+ '.xlsx') 
    type_use = type_use[type_use['Type of Use']== inputs['Type of Use']]
      
    risk_rating_2.iloc[13][1:5] = float((type_use[type_use.columns[1]]))
    risk_rating_2.iloc[13,5] = float((type_use[type_use.columns[2]]))
    risk_rating_2.iloc[13,6] = float((type_use[type_use.columns[2]]))
    risk_rating_2.iloc[13,7] = float((type_use[type_use.columns[3]]))
    risk_rating_2.iloc[13,8] = float((type_use[type_use.columns[3]]))
    risk_rating_2.iloc[13,9] = float((type_use[type_use.columns[4]]))
    risk_rating_2.iloc[13,10] = float((type_use[type_use.columns[4]]))
    ##########3##Floors of interest
    floor_int = pd.read_excel(path+"/tables/"+'Floors of Interest'+ '.xlsx') 
    
    floor_int = floor_int[(floor_int['Home Indicator']== inputs['Single family home indicator']) & 
                          (floor_int['Owner Indicator']== inputs['Condo unit owner indicator'])
                          & (floor_int['Interest']== inputs['Floor of interest'])]
    
    risk_rating_2.iloc[14][1:11] = float((floor_int[floor_int.columns[3]]))
    ##############Foundation type
    foundation = pd.read_excel(path+"/tables/"+'Foundation Type'+ '.xlsx') 
    foundation = foundation[(foundation['Foundation Type']== inputs['Foundation type'])]

    risk_rating_2.iloc[15][1:11] = float((foundation[foundation.columns[1]]))
    #############Height Design Vent
    First_floor_foundation_vent = pd.read_excel(path+"/tables/"+'First Floor Height'+ '.xlsx')
    if inputs['Foundation design'] == "Open, No Obstruction":
        First_floor_foundation_vent = pd.concat([First_floor_foundation_vent[First_floor_foundation_vent.columns[0]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[1]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[2]]],axis=1)
    elif inputs['Foundation design'] == "Open, Obstruction":
        First_floor_foundation_vent = pd.concat([First_floor_foundation_vent[First_floor_foundation_vent.columns[0]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[3]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[4]]],axis=1)
    elif inputs['Foundation design'] == "Closed, Wall":
        First_floor_foundation_vent = pd.concat([First_floor_foundation_vent[First_floor_foundation_vent.columns[0]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[5]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[6]]],axis=1)
    
    if inputs['Flood vents'] == "Yes":
        First_floor_foundation_vent = First_floor_foundation_vent.drop([First_floor_foundation_vent.columns[2]],axis=1)
    if inputs['Flood vents'] == "No":
        First_floor_foundation_vent = First_floor_foundation_vent.drop([First_floor_foundation_vent.columns[1]],axis=1)
    
    P = np.interp([inputs['First floor height']],(First_floor_foundation_vent[First_floor_foundation_vent.columns[0]]),(First_floor_foundation_vent[First_floor_foundation_vent.columns[1]]))
    risk_rating_2.iloc[16][1:11] = round(float(P),4)

    ###############Machineries
    machineries = pd.read_excel(path+"/tables/"+'ME Above First Floor'+ '.xlsx')
    machineries = machineries[(machineries[machineries.columns[0]]== inputs['M&E'])]
    
    risk_rating_2.iloc[17][1:11] = float((machineries[machineries.columns[1]]))  
    ############Coverage value
    building_value = pd.read_excel(path+"/tables/"+'Building Value'+ '.xlsx')
    content_value = pd.read_excel(path+"/tables/"+'Contents Value'+ '.xlsx')
    
    build = np.interp([inputs['Coverage A value']],(building_value[building_value.columns[0]]),(building_value[building_value.columns[1]]))
    content = np.interp([inputs['Coverage C value']],(content_value[content_value.columns[0]]),(content_value[content_value.columns[1]]))
    
    risk_rating_2.iloc[18,1] = round(float(build),4)
    risk_rating_2.iloc[18,2] = round(float(content),4)
    risk_rating_2.iloc[18,3] = round(float(build),4)
    risk_rating_2.iloc[18,4] = round(float(content),4)
    risk_rating_2.iloc[18,5] = round(float(build),4)
    risk_rating_2.iloc[18,6] = round(float(content),4)
    risk_rating_2.iloc[18,7] = round(float(build),4)
    risk_rating_2.iloc[18,8] = round(float(content),4)
    risk_rating_2.iloc[18,9] = round(float(build),4)
    risk_rating_2.iloc[18,10] = round(float(content),4)
    risk_rating_2.iloc[18,11] = round(float(build),4)
    risk_rating_2.iloc[18,12] = round(float(content),4)
    ##############Deductible & Limit to coverage value ratio
    deductible_limit_coverage_A = pd.read_excel(path+"/tables/"+'Deductible Limit ITV Cov A'+ '.xlsx')
    deductible_limit_coverage_C = pd.read_excel(path+"/tables/"+'Deductible Limit ITV Cov C'+ '.xlsx')
    
    ratio_A = max(min((inputs['Coverage A deductible'] + inputs['Coverage A limit']) / inputs['Coverage A value'], 1), 0)  
    ratio_C = max(min((inputs['Coverage C deductible'] + inputs['Coverage C limit']) / inputs['Coverage C value'], 1), 0)  
    
    S_build1 = np.interp([ratio_A],(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[0]]),(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[1]]))
    S_build2 = np.interp([ratio_A],(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[0]]),(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[2]]))
    S_cont1 = np.interp([ratio_C],(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[0]]),(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[1]]))
    S_cont2 = np.interp([ratio_C],(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[0]]),(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[2]]))
    
    risk_rating_2.iloc[19,1] = round(float(S_build1),4)
    risk_rating_2.iloc[19,2] = round(float(S_cont1),4)
    risk_rating_2.iloc[19,3] = round(float(S_build1),4)
    risk_rating_2.iloc[19,4] = round(float(S_cont1),4)
    risk_rating_2.iloc[19,5] = round(float(S_build2),4)
    risk_rating_2.iloc[19,6] = round(float(S_cont2),4)
    risk_rating_2.iloc[19,7] = round(float(S_build2),4)
    risk_rating_2.iloc[19,8] = round(float(S_cont2),4)
    risk_rating_2.iloc[19,9] = round(float(S_build2),4)
    risk_rating_2.iloc[19,10] = round(float(S_cont2),4)
    risk_rating_2.iloc[19,11] = round(float(S_build2),4)
    risk_rating_2.iloc[19,12] = round(float(S_cont2),4)
    ##################
    deductible_coverage_A = pd.read_excel(path+"/tables/"+'Deductible ITV Cov A'+ '.xlsx')
    deductible_coverage_C = pd.read_excel(path+"/tables/"+'Deductible ITV Cov C'+ '.xlsx')
    
    ratio_A = max(min((inputs['Coverage A deductible']) / inputs['Coverage A value'], 1), 0)  
    ratio_C = max(min((inputs['Coverage C deductible']) / inputs['Coverage C value'], 1), 0)  
    
    S_build1 = np.interp([ratio_A],(deductible_coverage_A[deductible_coverage_A.columns[0]]),(deductible_coverage_A[deductible_coverage_A.columns[1]]))
    S_build2 = np.interp([ratio_A],(deductible_coverage_A[deductible_coverage_A.columns[0]]),(deductible_coverage_A[deductible_coverage_A.columns[2]]))
    S_cont1 = np.interp([ratio_C],(deductible_coverage_C[deductible_coverage_C.columns[0]]),(deductible_coverage_C[deductible_coverage_C.columns[1]]))
    S_cont2 = np.interp([ratio_C],(deductible_coverage_C[deductible_coverage_C.columns[0]]),(deductible_coverage_C[deductible_coverage_C.columns[2]]))
    
    risk_rating_2.iloc[20,1] = round(float(S_build1),4)
    risk_rating_2.iloc[20,2] = round(float(S_cont1),4)
    risk_rating_2.iloc[20,3] = round(float(S_build1),4)
    risk_rating_2.iloc[20,4] = round(float(S_cont1),4)
    risk_rating_2.iloc[20,5] = round(float(S_build2),4)
    risk_rating_2.iloc[20,6] = round(float(S_cont2),4)
    risk_rating_2.iloc[20,7] = round(float(S_build2),4)
    risk_rating_2.iloc[20,8] = round(float(S_cont2),4)
    risk_rating_2.iloc[20,9] = round(float(S_build2),4)
    risk_rating_2.iloc[20,10] = round(float(S_cont2),4)
    risk_rating_2.iloc[20,11] = round(float(S_build2),4)
    risk_rating_2.iloc[20,12] = round(float(S_cont2),4)
    
    risk_rating_2.iloc[21][1:-1] = risk_rating_2.iloc[19][1:-1] - risk_rating_2.iloc[20][1:-1]
    #########
    if inputs['Coverage A limit'] == 0:
        risk_rating_2.iloc[22,1] = 0
        risk_rating_2.iloc[22,3] = 0
        risk_rating_2.iloc[22,5] = 0
        risk_rating_2.iloc[22,7] = 0
        risk_rating_2.iloc[22,9] = 0
        risk_rating_2.iloc[22,11] = 0

    else:
        risk_rating_2.iloc[22,1] = max(0.001,risk_rating_2.iloc[21,1])
        risk_rating_2.iloc[22,3] = max(0.001,risk_rating_2.iloc[21,3])
        risk_rating_2.iloc[22,5] = max(0.001,risk_rating_2.iloc[21,5])
        risk_rating_2.iloc[22,7] = max(0.001,risk_rating_2.iloc[21,7])
        risk_rating_2.iloc[22,9] = max(0.001,risk_rating_2.iloc[21,9])
        risk_rating_2.iloc[22,11] = max(0.001,risk_rating_2.iloc[21,11])
    
    if inputs['Coverage A limit'] == 0:
        risk_rating_2.iloc[22,2] = 0
        risk_rating_2.iloc[22,4] = 0
        risk_rating_2.iloc[22,6] = 0
        risk_rating_2.iloc[22,8] = 0
        risk_rating_2.iloc[22,10] = 0
        risk_rating_2.iloc[22,12] = 0
    else:
        risk_rating_2.iloc[22,2] = max(0.001,risk_rating_2.iloc[21,2])
        risk_rating_2.iloc[22,4] = max(0.001,risk_rating_2.iloc[21,4])
        risk_rating_2.iloc[22,6] = max(0.001,risk_rating_2.iloc[21,6])
        risk_rating_2.iloc[22,8] = max(0.001,risk_rating_2.iloc[21,8])
        risk_rating_2.iloc[22,10] = max(0.001,risk_rating_2.iloc[21,10])
        risk_rating_2.iloc[22,12] = max(0.001,risk_rating_2.iloc[21,12])
    #################Concentration Risk
    conc_risk_mapping = pd.read_excel(path+"/tables/"+'Concentration Risk Mapping'+ '.xlsx')
    conc_risk_mapping = conc_risk_mapping[(conc_risk_mapping[conc_risk_mapping.columns[0]]== inputs['State (Long)']) & (conc_risk_mapping[conc_risk_mapping.columns[1]]== inputs['County'])]
    msa = conc_risk_mapping.iloc[0][2]
    conc_risk = pd.read_excel(path+"/tables/"+'Concentration Risk'+ '.xlsx')
    conc_risk = conc_risk[(conc_risk[conc_risk.columns[0]]== msa)]
            
    risk_rating_2.iloc[23,1] = float(conc_risk[conc_risk.columns[2]])
    risk_rating_2.iloc[23,2] = float(conc_risk[conc_risk.columns[2]])
    risk_rating_2.iloc[23,3] = float(conc_risk[conc_risk.columns[2]])
    risk_rating_2.iloc[23,4] = float(conc_risk[conc_risk.columns[2]])
    risk_rating_2.iloc[23,5] = float(conc_risk[conc_risk.columns[3]])
    risk_rating_2.iloc[23,6] = float(conc_risk[conc_risk.columns[3]])
    ##########CRS disc
    risk_rating_2.iloc[24][1:] = float(inputs['CRS discount']/100)
    risk_rating_2.iloc[25][1:] = 1-float(inputs['CRS discount']/100)
    #########3
    x= 1
    for i in range(1,13):
        risk_rating = risk_rating_2[risk_rating_2.columns[i]]
        for j in range(0,12):   
            y = risk_rating.iloc[j]
            if str(y)!= 'nan':
                x*=y
        risk_rating_2.iloc[12,i] = round(x,4)
        x = 1      
    x= 1
    for i in range(1,13):
        risk_rating = risk_rating_2[risk_rating_2.columns[i]]
        for j in range(12,19):   
            y = risk_rating.iloc[j]
            if str(y)!= 'nan':
                x*=y
        risk_rating_2.iloc[26,i] = round(x,4)
        x = 1      

    risk_rating_2.iloc[26][1:-1] =  (risk_rating_2.iloc[22][1:-1] * risk_rating_2.iloc[25][1:-1] * risk_rating_2.iloc[26][1:-1])
    risk_rating_2.iloc[26,1] = risk_rating_2.iloc[26,1] *risk_rating_2.iloc[23,1] 
    risk_rating_2.iloc[26,2] = risk_rating_2.iloc[26,2] *risk_rating_2.iloc[23,2] 
    risk_rating_2.iloc[26,3] = risk_rating_2.iloc[26,3] *risk_rating_2.iloc[23,3] 
    risk_rating_2.iloc[26,4] = risk_rating_2.iloc[26,4] *risk_rating_2.iloc[23,4] 
    risk_rating_2.iloc[26,5] = risk_rating_2.iloc[26,5] *risk_rating_2.iloc[23,5] 
    risk_rating_2.iloc[26,6] = risk_rating_2.iloc[26,6] *risk_rating_2.iloc[23,6] 
    ##########################
    Rate_of_building = round((risk_rating_2.iloc[26,1] +
                        risk_rating_2.iloc[26,3] +
                        risk_rating_2.iloc[26,5] +
                        risk_rating_2.iloc[26,7] +
                        risk_rating_2.iloc[26,9] +
                        risk_rating_2.iloc[26,11]),4)
    
    Rate_of_contents = round((risk_rating_2.iloc[26,2] +
                        risk_rating_2.iloc[26,4] +
                        risk_rating_2.iloc[26,6] +
                        risk_rating_2.iloc[26,8] +
                        risk_rating_2.iloc[26,10] +
                        risk_rating_2.iloc[26,12]),4)
    
    risk_rating_2.iloc[27,13] = Rate_of_building
    risk_rating_2.iloc[28,13] = Rate_of_contents
     
     
    risk_rating_2.iloc[29,1] = round((risk_rating_2.iloc[26,1]/ Rate_of_building )*100,4)
    risk_rating_2.iloc[29,3] = round((risk_rating_2.iloc[26,3]/ Rate_of_building)*100,4)
    risk_rating_2.iloc[29,5] = round((risk_rating_2.iloc[26,5]/ Rate_of_building)*100,4)
    risk_rating_2.iloc[29,7] = round((risk_rating_2.iloc[26,7]/ Rate_of_building)*100,4)
    risk_rating_2.iloc[29,9] = round((risk_rating_2.iloc[26,9]/ Rate_of_building)*100,4)
    risk_rating_2.iloc[29,11] = round((risk_rating_2.iloc[26,11]/ Rate_of_building)*100,4)
    risk_rating_2.iloc[29,2] = round((risk_rating_2.iloc[26,2]/ Rate_of_contents)*100,4)
    risk_rating_2.iloc[29,4] = round((risk_rating_2.iloc[26,4]/ Rate_of_contents)*100,4)
    risk_rating_2.iloc[29,6] = round((risk_rating_2.iloc[26,6]/ Rate_of_contents)*100,4)
    risk_rating_2.iloc[29,8] = round((risk_rating_2.iloc[26,8]/ Rate_of_contents)*100,4)
    risk_rating_2.iloc[29,10] = round((risk_rating_2.iloc[26,10]/ Rate_of_contents)*100,4)
    risk_rating_2.iloc[29,12] = round((risk_rating_2.iloc[26,12]/ Rate_of_contents)*100,4)

    ######################
    weighted_deductible_building =  round((risk_rating_2.iloc[22,1] * risk_rating_2.iloc[29,1]+
                                    risk_rating_2.iloc[22,3] * risk_rating_2.iloc[29,3]+
                                    risk_rating_2.iloc[22,5] * risk_rating_2.iloc[29,5]+
                                    risk_rating_2.iloc[22,7] * risk_rating_2.iloc[29,7]+
                                    risk_rating_2.iloc[22,9] * risk_rating_2.iloc[29,9]+
                                    risk_rating_2.iloc[22,11] * risk_rating_2.iloc[29,11])/100,4)
                
    
    weighted_deductible_contents =  round((risk_rating_2.iloc[22,2] * risk_rating_2.iloc[29,2]+
                                    risk_rating_2.iloc[22,4] * risk_rating_2.iloc[29,4]+
                                    risk_rating_2.iloc[22,6] * risk_rating_2.iloc[29,6]+
                                    risk_rating_2.iloc[22,8] * risk_rating_2.iloc[29,8]+
                                    risk_rating_2.iloc[22,10] * risk_rating_2.iloc[29,10]+
                                    risk_rating_2.iloc[22,12] * risk_rating_2.iloc[29,12])/100,4)
    
    min_rate_building = round(0 * weighted_deductible_building,4)
    max_rate_building = round(15 * weighted_deductible_building,4)
    min_rate_contents = round(0 * weighted_deductible_contents,4)
    max_rate_contents = round(15 * weighted_deductible_contents,4)
    final_rate_building = min(max(Rate_of_building,min_rate_building),max_rate_building ) 
    final_rate_contents =  min(max(Rate_of_contents,min_rate_contents),max_rate_contents ) 
    
    risk_rating_2.iloc[30,13] = weighted_deductible_building
    risk_rating_2.iloc[31,13] = weighted_deductible_contents
    risk_rating_2.iloc[32,13] = min_rate_building
    risk_rating_2.iloc[33,13] = max_rate_building
    risk_rating_2.iloc[34,13] = min_rate_contents
    risk_rating_2.iloc[35,13] = max_rate_contents
    risk_rating_2.iloc[38,13] = final_rate_building
    risk_rating_2.iloc[39,13] = final_rate_contents
    
    coverage_building_thousands = inputs['Coverage A value']/1000 
    coverage_contents_thousands = inputs['Coverage C value']/1000 
    risk_rating_2.iloc[40,13] = coverage_building_thousands
    risk_rating_2.iloc[41,13] = coverage_contents_thousands

    initial_premium_without_fees_building = final_rate_building * coverage_building_thousands
    initial_premium_without_fees_contents = final_rate_contents * coverage_contents_thousands
    initial_premium_without_fees = initial_premium_without_fees_building + initial_premium_without_fees_contents 
    prior_claim_premium = (inputs['Prior Claim Rate'] * coverage_building_thousands * weighted_deductible_building * max(0,inputs['Prior claims']-1))
    premium_exc_fees_expense = initial_premium_without_fees + prior_claim_premium
    premium_without_fees = premium_exc_fees_expense + inputs['Loss Constant']  + inputs['Expense Constant'] 
    icc_crs = inputs['ICC premium'] * (100-inputs['CRS discount'])/100
    subtotal = (premium_without_fees + icc_crs)
    
    risk_rating_2.iloc[42,13] = initial_premium_without_fees_building
    risk_rating_2.iloc[43,13] = initial_premium_without_fees_contents
    risk_rating_2.iloc[44,13] = initial_premium_without_fees
    risk_rating_2.iloc[45,13] = prior_claim_premium
    risk_rating_2.iloc[46,13] = premium_exc_fees_expense
    risk_rating_2.iloc[47,13] = inputs['Expense Constant'] 
    risk_rating_2.iloc[48,13] = inputs['Loss Constant'] 
    risk_rating_2.iloc[49,13] = premium_without_fees
    risk_rating_2.iloc[50,13] = inputs['ICC premium'] 
    risk_rating_2.iloc[51,13] = icc_crs
    risk_rating_2.iloc[52,13] = subtotal
    risk_rating_2.iloc[53,13] = inputs['Reserve fund']

    
    subtotal = subtotal * inputs['Reserve fund']
    risk_rating_2.iloc[54,13] = subtotal
    risk_rating_2.iloc[55,13] = inputs['Probation surcharge']

    if inputs['Primary residence indicator'] == 'Yes':
        HFIAA_surcharge = 50    
    else:
        HFIAA_surcharge = 250    
    risk_rating_2.iloc[56,13] = HFIAA_surcharge
    risk_rating_2.iloc[57,13] = inputs['Federal policy fee']  
    premium = round(subtotal + inputs['Probation surcharge'] + HFIAA_surcharge + inputs['Federal policy fee']  ,2)
    risk_rating_2.iloc[58,13] = premium
    return risk_rating_2



