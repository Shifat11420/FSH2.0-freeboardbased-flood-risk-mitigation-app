import pandas as pd
import numpy as np

risk_rating_2 = pd.DataFrame(columns=["Items","Inland Flood Buldings","Inland Flood Contents",
                  "Storm Surge Buldings","Storm Surge Contents",
                  "Tsunami Buldings","Tsunami Contents",
                  "Great Lakes Buldings","Great Lakes Contents",
                  "Coastal Erosion Buldings","Coastal Erosion Contents","All Perils (All Coverages)"],
                         index = range(0,58))
risk_rating_2['Items'] = ["Base Rate (per $1000 of Coverage Value)", "Distance to River","Elevation Relative to River by River Class","Drainage Area","Structural Relative Elevation","Distance to Coast","Distance to Ocean","Elevation", "Distance to Lake","Elevation Relative to Lake", "Territory (HUC12 & Barrier Island Indicator)",
                          "Geographic Rate by Peril & Coverage","Type of Use","Floor of Interest", "Foundation Type","First Floor Height by Foundation Design & Flood Vents","M&E above First Floor","Coverage Value Factor","Deductible & Limit to Coverage Value Ratio","Deductible to Coverage Value Ratio","Initial Deductible & ITV","Final Deductible & ITV",
                          "Concentration Risk","CRS Discount Percentage","CRS Discount Factor","Rate by Peril & Coverage","Rate (per $1000 of Building Value)", "Rate (per $1000 of Contents Value)", "Rate Weights by Coverage", "Weighted Deductible & ITV Factor (Building)","Weighted Deductible & ITV Factor (Contents)","Minimum Rate (per $1000 of Buildig Value)","Maximum Rate (per $1000 of Buildig Value)",
                          "Minimum Rate (per $1000 of Contents Value)","Maximum Rate (per $1000 of Contents Value)","Minimum Rate by Peril & Coverage (per $1000 of Coverage Value)","Maximum Rate by Peril & Coverage (per $1000 of Coverage Value)","Final Rate (per $1000 of Building Value)","Final Rate (per $1000 of Contents Value)", "Coverage Value in Thousands (Buildings)","Coverage Value in Thousands (Contents)",
                          "Initial Premium without Fees (Buildings)","Initial Premium without Fees (Contents)","Initial Premium without Fees","Prior Claims Premium","Premium excluding Fees & Expense Constant","Expense Constant", "Loss Constant", "Premium without Fees","ICC Premium","ICC Premium with CRS Discount","Subtotal","Reserve Fund Factor","Subtotal","Probation Surcharge","HFIAA Surcharge by Primary Residence Indicator",
                          "Federal Policy Fee", "Premium with Fees"]

def NL_premium(path,path1,path2,inputs) :
    base_rate = pd.read_excel(path1+'BaseRates - '+inputs['Levee']+ '.xlsx')
    base_rate_data = (base_rate[(base_rate['Region']==inputs['State']) & (base_rate['Single Family Home Indicator']== inputs['Single family home indicator'])])
    segment = base_rate_data.iloc[0]['Segment']
    #inland flood
    risk_rating_2.iloc[0,1] = base_rate_data.iloc[0][3]
    risk_rating_2.iloc[0,2] = base_rate_data.iloc[0][4]
    #storm surge
    if inputs['Barrier island indicator'] == 'Yes':
        risk_rating_2.iloc[0,3] = base_rate_data.iloc[0][7]
        risk_rating_2.iloc[0,4] = base_rate_data.iloc[0][8]
    else:
        risk_rating_2.iloc[0,3] = base_rate_data.iloc[0][5]
        risk_rating_2.iloc[0,4] = base_rate_data.iloc[0][6]
    # tsunami   
    risk_rating_2.iloc[0,5] = base_rate_data.iloc[0][9]
    risk_rating_2.iloc[0,6] = base_rate_data.iloc[0][10]
    #great lake
    risk_rating_2.iloc[0,7] = base_rate_data.iloc[0][11]
    risk_rating_2.iloc[0,8] = base_rate_data.iloc[0][12]
    #coastal
    risk_rating_2.iloc[0,9] = base_rate_data.iloc[0][13]
    risk_rating_2.iloc[0,10] = base_rate_data.iloc[0][14]
    #####DTR
    dist_river = pd.read_excel(path1+'DTR - '+inputs['Levee']+ '.xlsx')
    dist_river = dist_river[(dist_river['Region']== 'Segment '+str(segment))]
    dist_river = dist_river.drop([dist_river.columns[0]],axis=1)
    dist_river = dist_river.astype('float64')
    
    if inputs['DTR'] == 'N/A':
        B = np.nan
    else:
        B = np.interp([inputs['DTR']],(dist_river[dist_river.columns[0]]),(dist_river[dist_river.columns[1]]))

    risk_rating_2.iloc[1,1] = round(float(B),4)
    risk_rating_2.iloc[1,2] = round(float(B),4)
    ####Elevation Relative ot River
    if segment != 5:
        elev_river = pd.read_excel(path1+'ElevRelRiver - '+inputs['Levee'] + ' - Seg 1-4.xlsx')
    else:
        elev_river = pd.read_excel(path1+'ElevRelRiver - '+inputs['Levee'] + ' - Seg 5.xlsx')
    
    elev_river = elev_river[(elev_river['River Class']== 'Class '+str(inputs['River class']))]
    elev_river = elev_river.drop([elev_river.columns[0]],axis=1)
    elev_river = elev_river.astype('float64')
    
    if inputs['ERR'] == 'N/A':
        C = np.nan
    else:
        C = np.interp([inputs['ERR']],(elev_river[elev_river.columns[0]]),(elev_river['IF Segment '+str(segment)]))
    
    risk_rating_2.iloc[2,1] = round(float(C),4)
    risk_rating_2.iloc[2,2] = round(float(C),4)
    #####Drainage Area
    if segment != 5:
        drainage = pd.read_excel(path1+'DrainageArea - '+inputs['Levee'] + ' - Seg 1-4.xlsx')
    else:
        drainage = pd.read_excel(path1+'DrainageArea - '+inputs['Levee'] + ' - Seg 5.xlsx')
    
    drainage = drainage.astype('float64')
    D = np.interp([inputs['DA']],(drainage[drainage.columns[0]]),(drainage['IF Segment '+str(segment)]))
    
    risk_rating_2.iloc[3,1] = round(float(D),4)
    risk_rating_2.iloc[3,2] = round(float(D),4)
    ########Str Elevation
    str_elev = pd.read_excel(path1+'StructRelElev - '+inputs['Levee']+ '.xlsx')
    str_elev = str_elev[(str_elev['Region']== 'Segment '+str(segment))]
    str_elev = str_elev.drop([str_elev.columns[0]],axis=1)
    str_elev = str_elev.astype('float64')
    E = np.interp([inputs['SRE']],(str_elev[str_elev.columns[0]]),(str_elev[str_elev.columns[1]]))
    
    risk_rating_2.iloc[4,1] = round(float(E),4)
    risk_rating_2.iloc[4,2] = round(float(E),4)
    #####DTC
    dtc_ce = pd.read_excel(path1+'DTC - CE - '+inputs['Levee']+ '.xlsx')
    dtc_ce = dtc_ce.astype('float64')
   
    if inputs['DTC'] == 'N/A':
        coast = np.nan
    else:
        coast = np.interp([inputs['DTC']],(dtc_ce[dtc_ce.columns[0]]),(dtc_ce[dtc_ce.columns[1]]))
    
    if segment != 3 and segment != 4 and inputs['DTC'] != 'N/A':
        dtc_others = pd.read_excel(path2+'DTC - '+inputs['Levee']+ '.xlsx')
        dtc_others = dtc_others[(dtc_others['Region']== 'Segment '+str(segment))]
        dtc_others = dtc_others.drop([dtc_others.columns[0]],axis=1)
        dtc_others = dtc_others.astype('float64')    
        storm = np.interp([inputs['DTC']],(dtc_others[dtc_others.columns[0]]),(dtc_others[dtc_others.columns[1]]))
        tsunami = np.interp([inputs['DTC']],(dtc_others[dtc_others.columns[0]]),(dtc_others[dtc_others.columns[2]]))
    else:
        storm = np.nan
        tsunami = np.nan
    
    risk_rating_2.iloc[5,3] = round(float(storm),4)
    risk_rating_2.iloc[5,4] = round(float(storm),4)
    risk_rating_2.iloc[5,5] = round(float(tsunami),4)
    risk_rating_2.iloc[5,6] = round(float(tsunami),4)
    risk_rating_2.iloc[5,9] = round(float(coast),4)
    risk_rating_2.iloc[5,10] = round(float(coast),4)
    ################DTO
    dto = pd.read_excel(path2+'DTO - '+inputs['Levee']+ '.xlsx')
    if segment != 3 and segment != 4 and inputs['DTO']!='N/A':
        dto = dto[(dto['Region']== 'Segment '+str(segment))]
        dto = dto.drop([dto.columns[0]],axis=1)
        dto = dto.astype('float64')
        storm = np.interp([inputs['DTO']],(dto[dto.columns[0]]),(dto[dto.columns[1]]))
        tsunami = np.interp([inputs['DTO']],(dto[dto.columns[0]]),(dto[dto.columns[2]]))
    else:
        storm = np.nan
        tsunami = np.nan
    risk_rating_2.iloc[6,3] = round(float(storm),4)
    risk_rating_2.iloc[6,4] = round(float(storm),4)
    risk_rating_2.iloc[6,5] = round(float(tsunami),4)
    risk_rating_2.iloc[6,6] = round(float(tsunami),4)
    ###############Elevation
    Elev = pd.read_excel(path2+'Elevation - '+inputs['Levee']+ '.xlsx')    
    if segment != 3 and segment != 4:
        Elev = Elev[(Elev['Region']== 'Segment '+str(segment))]
        Elev = Elev.drop([Elev.columns[0]],axis=1)
        Elev = Elev.astype('float64')
        storm = np.interp([inputs['Elevation']],(Elev[Elev.columns[0]]),(Elev[Elev.columns[1]]))
        tsunami = np.interp([inputs['Elevation']],(Elev[Elev.columns[0]]),(Elev[Elev.columns[2]]))
    else:
        storm = np.nan
        tsunami = np.nan
    risk_rating_2.iloc[7,3] = round(float(storm),4)
    risk_rating_2.iloc[7,4] = round(float(storm),4)
    risk_rating_2.iloc[7,5] = round(float(tsunami),4)
    risk_rating_2.iloc[7,6] = round(float(tsunami),4)
    ##################DTL
    dist_lake = pd.read_excel(path1+'DTL - '+inputs['Levee']+ '.xlsx')
    if inputs['DTL'] =='N/A':
        risk_rating_2.iloc[8,7] = 0.525
        risk_rating_2.iloc[8,8] = 0.525   
    else:
        I = np.interp([inputs['DTL']],(dist_lake[dist_lake.columns[0]]),(dist_lake[dist_lake.columns[1]]))
        risk_rating_2.iloc[8,7] = round(float(I),4)
        risk_rating_2.iloc[8,8] = round(float(I),4)
        
    ##############ElevLake
    elev_lake =  pd.read_excel(path1+'ElevRelLake - '+inputs['Levee']+ '.xlsx')  
    
    if inputs['DTL']=='N/A':
        risk_rating_2.iloc[9,7] = 0.004
        risk_rating_2.iloc[9,8] = 0.004
    
    else:
        J = np.interp([inputs['ERL']],(elev_lake[elev_lake.columns[0]]),(elev_lake[elev_lake.columns[1]]))
        risk_rating_2.iloc[9,7] = round(float(J),4)
        risk_rating_2.iloc[9,8] = round(float(J),4)   
    ################Territory
    territory = pd.read_excel(path+"/tables/"+'Territory - TSU'+ '.xlsx') 
    territory = territory[territory['HUC12'] == int(inputs['HUC12'])]
    
    if len(territory) == 0:
        risk_rating_2.iloc[10,5] = 0 #round(float((territory[territory.columns[1]]+territory[territory.columns[2]])/2),4)
        risk_rating_2.iloc[10,6] = 0 #round(float((territory[territory.columns[1]]+territory[territory.columns[2]])/2),4)
    else:
        risk_rating_2.iloc[10,5] = round(float((territory[territory.columns[1]])),4)
        risk_rating_2.iloc[10,6] = round(float((territory[territory.columns[1]])),4)
    
    territory = pd.read_excel(path+"/tables/"+'Territory - GL'+ '.xlsx') 
    territory = territory[territory['HUC12']== int(inputs['HUC12'])]
    if len(territory) == 0:
        risk_rating_2.iloc[10,7] = 0 #round(float((territory[territory.columns[3]]+territory[territory.columns[4]])/2),4)
        risk_rating_2.iloc[10,8] = 0 #round(float((territory[territory.columns[3]]+territory[territory.columns[4]])/2),4)
    else:
        risk_rating_2.iloc[10,7] = round(float((territory[territory.columns[1]])),4)
        risk_rating_2.iloc[10,8] = round(float((territory[territory.columns[1]])),4)
    ##
    territory = pd.read_excel(path2+'Territory - '+inputs['Levee']+ '.xlsx') 

    territory = territory[territory['HUC12'] == int(inputs['HUC12'])]
    risk_rating_2.iloc[10,1] = round(float((territory[territory.columns[1]])),4)
    risk_rating_2.iloc[10,2] = round(float((territory[territory.columns[1]])),4)
    risk_rating_2.iloc[10,3] = round(float((territory[territory.columns[2]])),4)
    risk_rating_2.iloc[10,4] = round(float((territory[territory.columns[2]])),4)
    #######################type of use
    type_use = pd.read_excel(path+"/tables/"+'Type of Use'+ '.xlsx') 
    type_use = type_use[type_use['Type of Use']== inputs['Type of Use']]
    
    risk_rating_2.iloc[12,1] = float((type_use[type_use.columns[1]]))
    risk_rating_2.iloc[12,2] = float((type_use[type_use.columns[1]]))
    risk_rating_2.iloc[12,3] = float((type_use[type_use.columns[2]]))
    risk_rating_2.iloc[12,4] = float((type_use[type_use.columns[2]]))
    risk_rating_2.iloc[12,5] = float((type_use[type_use.columns[3]]))
    risk_rating_2.iloc[12,6] = float((type_use[type_use.columns[3]]))
    risk_rating_2.iloc[12,7] = float((type_use[type_use.columns[4]]))
    risk_rating_2.iloc[12,8] = float((type_use[type_use.columns[4]]))
    ##########3##Floors of interest
    floor_int = pd.read_excel(path+"/tables/"+'Floors of Interest'+ '.xlsx') 
    
    floor_int = floor_int[(floor_int['Home Indicator']== inputs['Single family home indicator']) & 
                          (floor_int['Owner Indicator']== inputs['Condo unit owner indicator'])
                          & (floor_int['Interest']== inputs['Floor of interest'])]
    
    risk_rating_2.iloc[13][1:9] = float((floor_int[floor_int.columns[3]]))
    ##############Foundation type
    foundation = pd.read_excel(path+"/tables/"+'Foundation Type'+ '.xlsx') 
    foundation = foundation[(foundation['Foundation Type']== inputs['Foundation type'])]
    
    risk_rating_2.iloc[14][1:9] = float((foundation[foundation.columns[2]]))
    #############Height Design Vent
    First_floor_foundation_vent = pd.read_excel(path+"/tables/"+'First Floor Height'+ '.xlsx')
    if inputs['Foundation design'] == "Open, No Obstruction":
        First_floor_foundation_vent = pd.concat([First_floor_foundation_vent[First_floor_foundation_vent.columns[0]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[1]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[2]]],axis=1)
    if inputs['Foundation design'] == "Open, Obstruction":
        First_floor_foundation_vent = pd.concat([First_floor_foundation_vent[First_floor_foundation_vent.columns[0]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[3]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[4]]],axis=1)
    if inputs['Foundation design'] == "Closed Wall":
        First_floor_foundation_vent = pd.concat([First_floor_foundation_vent[First_floor_foundation_vent.columns[0]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[5]],
                                    First_floor_foundation_vent[First_floor_foundation_vent.columns[6]]],axis=1)
    
    if inputs['Flood vents'] == "Yes":
        First_floor_foundation_vent = First_floor_foundation_vent.drop([First_floor_foundation_vent.columns[2]],axis=1)
    if inputs['Flood vents'] == "No":
        First_floor_foundation_vent = First_floor_foundation_vent.drop([First_floor_foundation_vent.columns[1]],axis=1)
    
    P = np.interp([inputs['First floor height']],(First_floor_foundation_vent[First_floor_foundation_vent.columns[0]]),(First_floor_foundation_vent[First_floor_foundation_vent.columns[1]]))
    
    risk_rating_2.iloc[15][1:9] = round(float(P),4)
    ###############Machineries
    machineries = pd.read_excel(path+"/tables/"+'ME Above First Floor'+ '.xlsx')
    machineries = machineries[(machineries[machineries.columns[0]]== inputs['M&E'])]
    
    risk_rating_2.iloc[16][1:9] = float((machineries[machineries.columns[1]]))
    ############Coverage value
    building_value = pd.read_excel(path+"/tables/"+'Building Value'+ '.xlsx')
    content_value = pd.read_excel(path+"/tables/"+'Contents Value'+ '.xlsx')
    
    build = np.interp([inputs['Coverage A value']],(building_value[building_value.columns[0]]),(building_value[building_value.columns[1]]))
    content = np.interp([inputs['Coverage C value']],(content_value[content_value.columns[0]]),(content_value[content_value.columns[1]]))

    risk_rating_2.iloc[17,1] = round(float(build),4)
    risk_rating_2.iloc[17,2] = round(float(content),4)
    risk_rating_2.iloc[17,3] = round(float(build),4)
    risk_rating_2.iloc[17,4] = round(float(content),4)
    risk_rating_2.iloc[17,5] = round(float(build),4)
    risk_rating_2.iloc[17,6] = round(float(content),4)
    risk_rating_2.iloc[17,7] = round(float(build),4)
    risk_rating_2.iloc[17,8] = round(float(content),4)
    ##############Deductible & Limit to coverage value ratio
    deductible_limit_coverage_A = pd.read_excel(path+"/tables/"+'Deductible Limit ITV Cov A'+ '.xlsx')
    deductible_limit_coverage_C = pd.read_excel(path+"/tables/"+'Deductible Limit ITV Cov C'+ '.xlsx')
    
    ratio_A = max(min((inputs['Coverage A deductible'] + inputs['Coverage A limit']) / inputs['Coverage A value'], 1), 0)  
    ratio_C = max(min((inputs['Coverage C deductible'] + inputs['Coverage C limit']) / inputs['Coverage C value'], 1), 0)  
    
    S_build1 = np.interp([ratio_A],(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[0]]),(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[1]]))
    S_build2 = np.interp([ratio_A],(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[0]]),(deductible_limit_coverage_A[deductible_limit_coverage_A.columns[2]]))
    S_cont1 = np.interp([ratio_C],(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[0]]),(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[1]]))
    S_cont2 = np.interp([ratio_C],(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[0]]),(deductible_limit_coverage_C[deductible_limit_coverage_C.columns[2]]))
    
    risk_rating_2.iloc[18,1] = round(float(S_build1),4)
    risk_rating_2.iloc[18,2] = round(float(S_cont1),4)
    risk_rating_2.iloc[18,3] = round(float(S_build2),4)
    risk_rating_2.iloc[18,4] = round(float(S_cont2),4)
    risk_rating_2.iloc[18,5] = round(float(S_build2),4)
    risk_rating_2.iloc[18,6] = round(float(S_cont2),4)
    risk_rating_2.iloc[18,7] = round(float(S_build2),4)
    risk_rating_2.iloc[18,8] = round(float(S_cont2),4)
    risk_rating_2.iloc[18,9] = round(float(S_build2),4)
    risk_rating_2.iloc[18,10] = round(float(S_cont2),4)
    ##################
    deductible_coverage_A = pd.read_excel(path+"/tables/"+'Deductible ITV Cov A'+ '.xlsx')
    deductible_coverage_C = pd.read_excel(path+"/tables/"+'Deductible ITV Cov C'+ '.xlsx')
    
    ratio_A = max(min((inputs['Coverage A deductible']) / inputs['Coverage A limit'], 1), 0)  
    ratio_C = max(min((inputs['Coverage C deductible']) / inputs['Coverage C limit'], 1), 0)  
    
    S_build1 = np.interp([ratio_A],(deductible_coverage_A[deductible_coverage_A.columns[0]]),(deductible_coverage_A[deductible_coverage_A.columns[1]]))
    S_build2 = np.interp([ratio_A],(deductible_coverage_A[deductible_coverage_A.columns[0]]),(deductible_coverage_A[deductible_coverage_A.columns[2]]))
    S_cont1 = np.interp([ratio_C],(deductible_coverage_C[deductible_coverage_C.columns[0]]),(deductible_coverage_C[deductible_coverage_C.columns[1]]))
    S_cont2 = np.interp([ratio_C],(deductible_coverage_C[deductible_coverage_C.columns[0]]),(deductible_coverage_C[deductible_coverage_C.columns[2]]))
    
    risk_rating_2.iloc[19,1] = round(float(S_build1),4)
    risk_rating_2.iloc[19,2] = round(float(S_cont1),4)
    risk_rating_2.iloc[19,3] = round(float(S_build2),4)
    risk_rating_2.iloc[19,4] = round(float(S_cont2),4)
    risk_rating_2.iloc[19,5] = round(float(S_build2),4)
    risk_rating_2.iloc[19,6] = round(float(S_cont2),4)
    risk_rating_2.iloc[19,7] = round(float(S_build2),4)
    risk_rating_2.iloc[19,8] = round(float(S_cont2),4)
    risk_rating_2.iloc[19,9] = round(float(S_build2),4)
    risk_rating_2.iloc[19,10] = round(float(S_cont2),4)
    
    risk_rating_2.iloc[20][1:-1] = risk_rating_2.iloc[18][1:-1] - risk_rating_2.iloc[19][1:-1]
    #########
    if inputs['Coverage A limit'] == 0:
        risk_rating_2.iloc[21,1] = 0
        risk_rating_2.iloc[21,3] = 0
        risk_rating_2.iloc[21,5] = 0
        risk_rating_2.iloc[21,7] = 0
        risk_rating_2.iloc[21,9] = 0
    else:
        risk_rating_2.iloc[21,1] = max(0.001,risk_rating_2.iloc[20,1])
        risk_rating_2.iloc[21,3] = max(0.001,risk_rating_2.iloc[20,3])
        risk_rating_2.iloc[21,5] = max(0.001,risk_rating_2.iloc[20,5])
        risk_rating_2.iloc[21,7] = max(0.001,risk_rating_2.iloc[20,7])
        risk_rating_2.iloc[21,9] = max(0.001,risk_rating_2.iloc[20,9])
    
    if inputs['Coverage A limit'] == 0:
        risk_rating_2.iloc[21,2] = 0
        risk_rating_2.iloc[21,4] = 0
        risk_rating_2.iloc[21,6] = 0
        risk_rating_2.iloc[21,8] = 0
        risk_rating_2.iloc[21,10] = 0
    else:
        risk_rating_2.iloc[21,2] = max(0.001,risk_rating_2.iloc[20,2])
        risk_rating_2.iloc[21,4] = max(0.001,risk_rating_2.iloc[20,4])
        risk_rating_2.iloc[21,6] = max(0.001,risk_rating_2.iloc[20,6])
        risk_rating_2.iloc[21,8] = max(0.001,risk_rating_2.iloc[20,8])
        risk_rating_2.iloc[21,10] = max(0.001,risk_rating_2.iloc[20,10])
    #################Concentration Risk
    conc_risk_mapping = pd.read_excel(path+"/tables/"+'Concentration Risk Mapping'+ '.xlsx')
    conc_risk_mapping = conc_risk_mapping[(conc_risk_mapping[conc_risk_mapping.columns[0]]== inputs['State (Long)']) & (conc_risk_mapping[conc_risk_mapping.columns[1]]== inputs['County'])]
    msa = conc_risk_mapping.iloc[0][2]
    conc_risk = pd.read_excel(path+"/tables/"+'Concentration Risk'+ '.xlsx')
    conc_risk = conc_risk[(conc_risk[conc_risk.columns[0]]== msa)]
            
    risk_rating_2.iloc[22,1] = float(conc_risk[conc_risk.columns[2]])
    risk_rating_2.iloc[22,2] = float(conc_risk[conc_risk.columns[2]])
    risk_rating_2.iloc[22,3] = float(conc_risk[conc_risk.columns[3]])
    risk_rating_2.iloc[22,4] = float(conc_risk[conc_risk.columns[3]])
    ##########CRS disc
    risk_rating_2.iloc[23][1:] = float(inputs['CRS discount']/100)
    risk_rating_2.iloc[24][1:] = 1-float(inputs['CRS discount']/100)
    #########
    x= 1
    for i in range(1,11):
        risk_rating = risk_rating_2[risk_rating_2.columns[i]]
        for j in range(0,11):   
            y = risk_rating.iloc[j]
            if str(y)!= 'nan':
                x*=y
        risk_rating_2.iloc[11,i] = round(x,4)
        x = 1      
    x= 1
    for i in range(1,11):
        risk_rating = risk_rating_2[risk_rating_2.columns[i]]
        for j in range(11,18):   
            y = risk_rating.iloc[j]
            if str(y)!= 'nan':
                x*=y
        risk_rating_2.iloc[25,i] = round(x,4)
        x = 1      
    
    risk_rating_2.iloc[25][1:-1] =  (risk_rating_2.iloc[21][1:-1] * risk_rating_2.iloc[24][1:-1] * risk_rating_2.iloc[25][1:-1])
    risk_rating_2.iloc[25,1] = risk_rating_2.iloc[25,1] *risk_rating_2.iloc[22,1] 
    risk_rating_2.iloc[25,2] = risk_rating_2.iloc[25,2] *risk_rating_2.iloc[22,2] 
    risk_rating_2.iloc[25,3] = risk_rating_2.iloc[25,3] *risk_rating_2.iloc[22,3] 
    risk_rating_2.iloc[25,4] = risk_rating_2.iloc[25,4] *risk_rating_2.iloc[22,4] 
    ##########################
    Rate_of_building = round(( risk_rating_2.iloc[25,1] +
                        risk_rating_2.iloc[25,3] +
                        risk_rating_2.iloc[25,5] +
                        risk_rating_2.iloc[25,7] +
                        risk_rating_2.iloc[25,9] ),4)
    
    Rate_of_contents = round(( risk_rating_2.iloc[25,2] +
                        risk_rating_2.iloc[25,4] +
                        risk_rating_2.iloc[25,6] +
                        risk_rating_2.iloc[25,8] +
                        risk_rating_2.iloc[25,10] ),4)
    
    risk_rating_2.iloc[26,11] = Rate_of_building
    risk_rating_2.iloc[27,11] = Rate_of_contents

    risk_rating_2.iloc[28,1] = round((risk_rating_2.iloc[25,1]/ Rate_of_building )*100,4)
    risk_rating_2.iloc[28,3] = round((risk_rating_2.iloc[25,3]/ Rate_of_building)*100,4)
    risk_rating_2.iloc[28,5] = round((risk_rating_2.iloc[25,5]/ Rate_of_building)*100,4)
    risk_rating_2.iloc[28,7] = round((risk_rating_2.iloc[25,7]/ Rate_of_building)*100,4)
    risk_rating_2.iloc[28,9] = round((risk_rating_2.iloc[25,9]/ Rate_of_building)*100,4)
    risk_rating_2.iloc[28,2] = round((risk_rating_2.iloc[25,2]/ Rate_of_contents)*100,4)
    risk_rating_2.iloc[28,4] = round((risk_rating_2.iloc[25,4]/ Rate_of_contents)*100,4)
    risk_rating_2.iloc[28,6] = round((risk_rating_2.iloc[25,6]/ Rate_of_contents)*100,4)
    risk_rating_2.iloc[28,8] = round((risk_rating_2.iloc[25,8]/ Rate_of_contents)*100,4)
    risk_rating_2.iloc[28,10] = round((risk_rating_2.iloc[25,10]/ Rate_of_contents)*100,4)
    ######################
    weighted_deductible_building =  round((risk_rating_2.iloc[21,1] * risk_rating_2.iloc[28,1]+
                                    risk_rating_2.iloc[21,3] * risk_rating_2.iloc[28,3]+
                                    risk_rating_2.iloc[21,5] * risk_rating_2.iloc[28,5]+
                                    risk_rating_2.iloc[21,7] * risk_rating_2.iloc[28,7]+
                                    risk_rating_2.iloc[21,9] * risk_rating_2.iloc[28,9])/100,4)
    
    
    weighted_deductible_contents =  round((risk_rating_2.iloc[21,2] * risk_rating_2.iloc[28,2]+
                                    risk_rating_2.iloc[21,4] * risk_rating_2.iloc[28,4]+
                                    risk_rating_2.iloc[21,6] * risk_rating_2.iloc[28,6]+
                                    risk_rating_2.iloc[21,8] * risk_rating_2.iloc[28,8]+
                                    risk_rating_2.iloc[21,10] * risk_rating_2.iloc[28,10])/100,4)
    
    min_rate_building = round(0 * weighted_deductible_building,4)
    max_rate_building = round(15 * weighted_deductible_building,4)  
    min_rate_contents = round(0 * weighted_deductible_contents,4)
    max_rate_contents = round(15 * weighted_deductible_contents,4)  
    final_rate_building = min(max(Rate_of_building,min_rate_building),max_rate_building ) 
    final_rate_contents =  min(max(Rate_of_contents,min_rate_contents),max_rate_contents ) 
    
    risk_rating_2.iloc[29,11] = weighted_deductible_building
    risk_rating_2.iloc[30,11] = weighted_deductible_contents
    risk_rating_2.iloc[31,11] = min_rate_building
    risk_rating_2.iloc[32,11] = max_rate_building
    risk_rating_2.iloc[33,11] = min_rate_contents
    risk_rating_2.iloc[34,11] = max_rate_contents
    risk_rating_2.iloc[37,11] = final_rate_building
    risk_rating_2.iloc[38,11] = final_rate_contents
    
    coverage_building_thousands = inputs['Coverage A value']/1000 
    coverage_contents_thousands = inputs['Coverage C value']/1000 
    initial_premium_without_fees_building = final_rate_building * coverage_building_thousands
    initial_premium_without_fees_contents = final_rate_contents * coverage_contents_thousands
    initial_premium_without_fees = initial_premium_without_fees_building + initial_premium_without_fees_contents 
    prior_claim_premium = (inputs['Prior Claim Rate'] * coverage_building_thousands * weighted_deductible_building * max(0,inputs['Prior claims']-1))
    premium_exc_fees_expense = initial_premium_without_fees + prior_claim_premium
    premium_without_fees = premium_exc_fees_expense + inputs['Loss Constant']  + inputs['Expense Constant'] 
    icc_crs = inputs['ICC premium'] * (100-inputs['CRS discount'])/100
    subtotal = (premium_without_fees + icc_crs)
    
    risk_rating_2.iloc[39,11] = coverage_building_thousands
    risk_rating_2.iloc[40,11] = coverage_contents_thousands
    risk_rating_2.iloc[41,11] = initial_premium_without_fees_building
    risk_rating_2.iloc[42,11] = initial_premium_without_fees_contents
    risk_rating_2.iloc[43,11] = initial_premium_without_fees
    risk_rating_2.iloc[44,11] = prior_claim_premium
    risk_rating_2.iloc[45,11] = premium_exc_fees_expense
    risk_rating_2.iloc[46,11] = inputs['Expense Constant'] 
    risk_rating_2.iloc[47,11] = inputs['Loss Constant']
    risk_rating_2.iloc[48,11] = premium_without_fees
    risk_rating_2.iloc[49,11] = inputs['ICC premium']
    risk_rating_2.iloc[50,11] = icc_crs
    risk_rating_2.iloc[51,11] = subtotal
    risk_rating_2.iloc[52,11] = inputs['Reserve fund']

    subtotal = subtotal * inputs['Reserve fund']
    risk_rating_2.iloc[53,11] = subtotal
    risk_rating_2.iloc[54,11] = inputs['Probation surcharge']
    
    if inputs['Primary residence indicator'] == 'Yes':
        HFIAA_surcharge = 50    
    else:
        HFIAA_surcharge = 250    
    risk_rating_2.iloc[55,11] = HFIAA_surcharge
    risk_rating_2.iloc[56,11] = inputs['Federal policy fee']  
    premium = round(subtotal + inputs['Probation surcharge'] + HFIAA_surcharge + inputs['Federal policy fee']  ,2)
    risk_rating_2.iloc[57,11] = premium
    return risk_rating_2



