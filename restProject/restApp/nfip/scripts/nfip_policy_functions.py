import pandas as pd
def homeowner_policy(path, inputs):
    #get insurance basic and additional amounts
    max_insurance_building =  pd.read_excel(path+'/Table 2 Maximum Amount Insurance Available Building.xlsx')
    max_insurance_contents =  pd.read_excel(path+'/Table 2 Maximum Amount Insurance Available Content.xlsx')    
    if inputs['program'] =='Regular':
        if inputs['ocupancy']=='Residential':
            default_basic_b = max_insurance_building.iloc[0]['Regular Program, Basic Insurance Limits, Building Coverage']
            default_additional_b = max_insurance_building.iloc[0]['Regular Program, Additional Insurance Limits, Building Coverage']
            default_basic_c = max_insurance_contents.iloc[0]['Regular Program, Basic Insurance Limits, Contents Coverage']
            default_additional_c = max_insurance_contents.iloc[0]['Regular Program, Additional Insurance Limits, Contents Coverage']
        else:
            default_basic_b = max_insurance_building.iloc[2]['Regular Program, Basic Insurance Limits, Building Coverage']
            default_additional_b = max_insurance_building.iloc[2]['Regular Program, Additional Insurance Limits, Building Coverage']
            default_basic_c = max_insurance_contents.iloc[1]['Regular Program, Basic Insurance Limits, Contents Coverage']
            default_additional_c = max_insurance_contents.iloc[1]['Regular Program, Additional Insurance Limits, Contents Coverage']
    #else statement will be for emergency program
    if inputs['building_coverage']>default_basic_b and inputs['building_coverage']<=default_basic_b+default_additional_b:
        basic_building_insurance = default_basic_b
        additional_building_insurance = inputs['building_coverage'] - default_basic_b
    elif inputs['building_coverage']<=default_basic_b:
        basic_building_insurance = inputs['building_coverage']
        additional_building_insurance = 0
    else:
        basic_building_insurance = default_basic_b
        additional_building_insurance = default_additional_b
        
    if inputs['contents_coverage']>default_basic_c and inputs['contents_coverage']<=default_basic_c+default_additional_c:
        basic_content_insurance = default_basic_c
        additional_content_insurance = inputs['contents_coverage'] - default_basic_c
    elif inputs['contents_coverage']<=default_basic_c:
        basic_content_insurance = inputs['contents_coverage']
        additional_content_insurance = 0
    else:
        basic_content_insurance = default_basic_c
        additional_content_insurance = default_additional_c
    ##################################################################
    #get the rates
    if inputs['flood_zone'] == 'AE' or inputs['flood_zone'] == 'A1-A30':
        if inputs['date_construction']== 'Post-Firm':      
            building_rate_table = pd.read_excel(path+'/Rate Table 3B Building Rates.xlsx')
            contents_rate_table = pd.read_excel(path+'/Rate Table 3B Contents Rates.xlsx')
            icc_table = 'Table 3B'            
            if inputs['ocupancy']=='Residential':
                if inputs['basement/enclosure']=='None':
                    if inputs['number_floors']>1: 
                        rate_part_b = '1+ Floor, No Basement/Enclosure/Crawlspace, 1-4 Family, '
                        rate_part_c = 'Lowest Floor ' +inputs['contents_location'] +', No Basement/Enclosure/Crawlspace, Residential, '
                    else:
                        rate_part_b = '1 Floor, No Basement/Enclosure/Crawlspace, 1-4 Family, '
                        rate_part_c = 'Lowest Floor ' +inputs['contents_location'] +', No Basement/Enclosure/Crawlspace, Residential, '
                else:
                    rate_part_b = '1+ Floor, With Basement/Enclosure/Crawlspace, 1-4 Family, '
                    rate_part_c = '1+ Floors, With Basement/Enclosure/Crawlspace, Residential, '               
            if inputs['ocupancy']=='Others' or inputs['ocupancy']=='Other Residential' or inputs['ocupancy']=='Non-Residential Business' or inputs['ocupancy']=='Other Non-Residential':
                if inputs['basement/enclosure']=='None':
                    if inputs['number_floors']>1: 
                        rate_part_b = '1+ Floor, No Basement/Enclosure/Crawlspace, Others, '
                        rate_part_c = 'Lowest Floor ' +inputs['contents_location'] +', No Basement/Enclosure/Crawlspace, Others, '
                    else:
                        rate_part_b = '1 Floor, No Basement/Enclosure/Crawlspace, Others, '
                        rate_part_c = 'Lowest Floor ' +inputs['contents_location'] +', No Basement/Enclosure/Crawlspace, Others, '
                else:
                    rate_part_b = '1+ Floor, With Basement/Enclosure/Crawlspace, Others, '
                    rate_part_c = '1+ Floors, With Basement/Enclosure/Crawlspace, Others, '     
        building_rates = building_rate_table.loc[building_rate_table[building_rate_table.columns[0]]==inputs['elevation_diff']]
        contents_rates = contents_rate_table.loc[contents_rate_table[contents_rate_table.columns[0]]==inputs['elevation_diff']]
        
        basic_rate_b = building_rates.iloc[0][rate_part_b+'Basic']
        additional_rate_b = building_rates.iloc[0][rate_part_b+'Additional']
        basic_rate_c = contents_rates.iloc[0][rate_part_c+'Basic']
        additional_rate_c = contents_rates.iloc[0][rate_part_c+'Additional']    
    
    if inputs['flood_zone'] == 'A':
        if inputs['basement/enclosure']=='None':      
            rate_table = pd.read_excel(path+'/Rate Table 3C.xlsx')
            icc_table = 'Table 3C'    
            if inputs['Type of EC'] ==  'BFE':
                rates= rate_table.loc[rate_table['Type of EC']==inputs['Type of EC']]
                elev_diff1 = ['+2 or more' if inputs['elevation_diff']>=2 else '0 to +1'][0]
                elev_diff2 = ['-1' if inputs['elevation_diff']==-1 else elev_diff1][0]
                rates2 = rates.loc[rates['Elevation Difference']==elev_diff2]
            elif inputs['Type of EC'] ==  'No BFE':
                rates= rate_table.loc[rate_table['Type of EC']==inputs['Type of EC']]
                elev_diff1 = ['+5 or more' if inputs['elevation_diff']>=5 else '+2 to +4'][0]
                elev_diff2 = ['+1' if inputs['elevation_diff']==1 else elev_diff1][0]
                rates2 = rates.loc[rates['Elevation Difference']==elev_diff2]
            elif inputs['Type of EC'] ==  'No EC':
                rates2 = rate_table.loc[rate_table['Type of EC']==inputs['Type of EC']]
            else:
                return (print('Please mention correct Elevation Certificate'))
                
        else:
            return (print('Submit for Rating'))
        
        if inputs['ocupancy']=='Residential':
                    rate_part_b = 'Building, Residential, '
                    rate_part_c = 'Contents, Residential, '
        if inputs['ocupancy']=='Others' or inputs['ocupancy']=='Other Residential' or inputs['ocupancy']=='Non-Residential Business' or inputs['ocupancy']=='Other Non-Residential':
                    rate_part_b = 'Building, Others, '
                    rate_part_c = 'Contents, Others, '
       
        basic_rate_b = rates2.iloc[0][rate_part_b+'Basic']
        additional_rate_b = rates2.iloc[0][rate_part_b+'Additional']
        basic_rate_c = rates2.iloc[0][rate_part_c+'Basic']
        additional_rate_c = rates2.iloc[0][rate_part_c+'Additional']    

    if inputs['flood_zone'] == 'VE' or inputs['flood_zone'] == 'V1-V30':
        if inputs['date_construction'] == '1981 Post-Firm':
            if inputs['basement/enclosure']=='None':
                rate_table = pd.read_excel(path+'/Rate Table 3E.xlsx')
                first_part = 'Elevated Buildings Free of Obstruction, '
                icc_table = 'Table 3E' 
            else:
                rate_table = pd.read_excel(path+'/Rate Table 3F.xlsx')
                first_part = 'Elevated Buildings With Obstruction, '
                icc_table = 'Table 3F' 
            rates = rate_table.loc[rate_table[rate_table.columns[0]]==inputs['elevation_diff']]
      
            rate_part_b = first_part + 'Building, Replacement cost ratio ' + inputs['Replacement cost ratio']
            if inputs['ocupancy']=='Residential':
                rate_part_c = first_part +'Contents, Residential'
            if inputs['ocupancy']=='Other Residential' or inputs['ocupancy']=='Non-Residential Business' or inputs['ocupancy']=='Other Non-Residential':
                rate_part_c = first_part +'Contents, Others'
            
            building_rates = rates.iloc[0][rate_part_b]
            contents_rates = rates.iloc[0][rate_part_c]
            basic_rate_b = building_rates
            additional_rate_b = building_rates
            basic_rate_c = contents_rates
            additional_rate_c =  contents_rates 
    
    ####Step 1
    annual_premium_building = basic_rate_b*(basic_building_insurance/100) + additional_rate_b*(additional_building_insurance/100) 
    annual_premium_contents = basic_rate_c*(basic_content_insurance/100) + additional_rate_c*(additional_content_insurance/100)     
    ###Step 2
    if inputs['ocupancy']=='Residential':
        deductible_factor_table = pd.read_excel(path+'/Rate Table 8B_Residential_Building+Contents.xlsx')
    else:
        deductible_factor_table = pd.read_excel(path+'/Rate Table 8B_Others_Building+Contents.xlsx')
    deductible_factors = deductible_factor_table[(deductible_factor_table['Deductible Building']==inputs['building_deductible']) & (deductible_factor_table['Deductible Contents']==inputs['contents_deductible'])]
    if inputs['date_construction']== 'Post-Firm' or inputs['date_construction'] == '1981 Post-Firm':
        deductible_factor = deductible_factors.iloc[0]['Pre-/Post-Firm Full-Risk']
    annual_subtotal = round(deductible_factor * (annual_premium_building+annual_premium_contents),0)
    ###Step 3
    #icc premium
    icc_premium_table = pd.read_excel(path+'/Rate Table 9.xlsx')
    icc_premiums = icc_premium_table.loc[icc_premium_table['Rate Table']==icc_table]
    if inputs['ocupancy']=='Residential':
        if inputs['building_coverage']<=230000:
            column_part =  '1-4 Family, Building Insurance, 1-230000'
        else:
            column_part =  '1-4 Family, Building Insurance, 230001-250000'
    else:
        if inputs['building_coverage']<=480000:
            column_part =  'Others, Building Insurance, 1-480000'
        else:
            column_part =  'Others, Building Insurance, 480001-500000'
    icc_premium = icc_premiums.iloc[0][column_part]
    subtotal_icc = annual_subtotal + icc_premium
    #CRS rating
    if inputs['CRS_Rating']>=1 and inputs['CRS_Rating']<=9:
        crs_premium_table = pd.read_excel(path+'/Table 2 CRS Premium Discounts by Class and Flood Zone.xlsx')
        crs_premiums = crs_premium_table.loc[crs_premium_table['Class']==inputs['CRS_Rating'] ]
     
        if inputs['flood_zone'] == 'AE' or inputs['flood_zone'] == 'A1-A30' or inputs['flood_zone'] == 'VE' or inputs['flood_zone'] == 'V1-V30' or inputs['flood_zone'] == 'AO'or inputs['flood_zone'] == 'AH':
            crs_premium = crs_premiums.iloc[0][1]
        else:
            crs_premium = crs_premiums.iloc[0][2]   
    else:
        crs_premium = 0
    subtotal_crs = (subtotal_icc) * (100-crs_premium)/100   
    #other fees
    RFA =  round(subtotal_crs * 0.18,0)          
    probation_surcharge = [0 if inputs['Probation']=='No' else 50][0]
    hfiaa_surcharge = [250 if inputs['Primary_residence'] =='No' else 25][0]
    fpf = 50
    total_amount_due = subtotal_crs + RFA + probation_surcharge + hfiaa_surcharge + fpf
    return round(total_amount_due,0)

def tenant_policy(path, inputs):
    #get insurance basic and additional amounts
    max_insurance_contents =  pd.read_excel(path+'/Table 2 Maximum Amount Insurance Available Content.xlsx')    
    if inputs['program'] =='Regular':
        if inputs['ocupancy']=='Residential':
            default_basic_c = max_insurance_contents.iloc[0]['Regular Program, Basic Insurance Limits, Contents Coverage']
            default_additional_c = max_insurance_contents.iloc[0]['Regular Program, Additional Insurance Limits, Contents Coverage']
        else:
            default_basic_c = max_insurance_contents.iloc[1]['Regular Program, Basic Insurance Limits, Contents Coverage']
            default_additional_c = max_insurance_contents.iloc[1]['Regular Program, Additional Insurance Limits, Contents Coverage']
    #else statement will be for emergency program       
    if inputs['contents_coverage']>default_basic_c and inputs['contents_coverage']<=default_basic_c+default_additional_c:
        basic_content_insurance = default_basic_c
        additional_content_insurance = inputs['contents_coverage'] - default_basic_c
    elif inputs['contents_coverage']<=default_basic_c:
        basic_content_insurance = inputs['contents_coverage']
        additional_content_insurance = 0
    else:
        basic_content_insurance = default_basic_c
        additional_content_insurance = default_additional_c
    ##################################################################
    #get the rates
    if inputs['flood_zone'] == 'AE' or inputs['flood_zone'] == 'A1-A30':
        if inputs['date_construction']== 'Post-Firm':      
            contents_rate_table = pd.read_excel(path+'/Rate Table 3B Contents Rates.xlsx')
                        
            if inputs['ocupancy']=='Residential':
                if inputs['basement/enclosure']=='None':
                    if inputs['number_floors']>1: 
                        rate_part_c = 'Lowest Floor ' +inputs['contents_location'] +', No Basement/Enclosure/Crawlspace, Residential, '
                    else:
                        rate_part_c = 'Lowest Floor ' +inputs['contents_location'] +', No Basement/Enclosure/Crawlspace, Residential, '
                else:
                    rate_part_c = '1+ Floors, With Basement/Enclosure/Crawlspace, Residential, '               
            if inputs['ocupancy']=='Others' or inputs['ocupancy']=='Other Residential' or inputs['ocupancy']=='Non-Residential Business' or inputs['ocupancy']=='Other Non-Residential':
                if inputs['basement/enclosure']=='None':
                    if inputs['number_floors']>1: 
                        rate_part_c = 'Lowest Floor ' +inputs['contents_location'] +', No Basement/Enclosure/Crawlspace, Others, '
                    else:
                        rate_part_c = 'Lowest Floor ' +inputs['contents_location'] +', No Basement/Enclosure/Crawlspace, Others, '
                else:
                    rate_part_c = '1+ Floors, With Basement/Enclosure/Crawlspace, Others, '     
        contents_rates = contents_rate_table.loc[contents_rate_table[contents_rate_table.columns[0]]==inputs['elevation_diff']]       
        basic_rate_c = contents_rates.iloc[0][rate_part_c+'Basic']
        additional_rate_c = contents_rates.iloc[0][rate_part_c+'Additional']    

    if inputs['flood_zone'] == 'VE' or inputs['flood_zone'] == 'V1-V30':
        if inputs['date_construction'] == '1981 Post-Firm':
            if inputs['basement/enclosure']=='None':
                rate_table = pd.read_excel(path+'/Rate Table 3E.xlsx')
                first_part = 'Elevated Buildings Free of Obstruction, '
                
            else:
                rate_table = pd.read_excel(path+'/Rate Table 3F.xlsx')
                first_part = 'Elevated Buildings With Obstruction, '
                
            rates = rate_table.loc[rate_table[rate_table.columns[0]]==inputs['elevation_diff']]
      
            if inputs['ocupancy']=='Residential':
                rate_part_c = first_part +'Contents, Residential'
            if inputs['ocupancy']=='Other Residential' or inputs['ocupancy']=='Non-Residential Business' or inputs['ocupancy']=='Other Non-Residential':
                rate_part_c = first_part +'Contents, Others'
            
            contents_rates = rates.iloc[0][rate_part_c]
            basic_rate_c = contents_rates
            additional_rate_c =  contents_rates 
            
    ####Step 1
    annual_premium_contents = basic_rate_c*(basic_content_insurance/100) + additional_rate_c*(additional_content_insurance/100)     
    ###Step 2
    if inputs['ocupancy']=='Residential':
        deductible_factor_table = pd.read_excel(path+'/Rate Table 8B_Residential_Contents.xlsx')
    else:
        deductible_factor_table = pd.read_excel(path+'/Rate Table 8B_Others_Contents.xlsx')
    deductible_factors = deductible_factor_table[(deductible_factor_table['Deductible Contents']==inputs['contents_deductible'])]
    if inputs['date_construction']== 'Post-Firm' or inputs['date_construction'] == '1981 Post-Firm':
        deductible_factor = deductible_factors.iloc[0]['Pre-/Post-Firm Full-Risk']
    
    annual_subtotal = round(deductible_factor * annual_premium_contents,0)
    ###Step 3
    RFA =  round(annual_subtotal * 0.18,0)          
    probation_surcharge = [0 if inputs['Probation']=='No'  else 50][0]
    hfiaa_surcharge = [250 if inputs['Primary_residence']=='No'  else 25][0]
    fpf = 25
    total_amount_due = annual_subtotal + RFA + probation_surcharge + hfiaa_surcharge + fpf
    return round(total_amount_due,0)

def landlord_policy(path, inputs):
    #get insurance basic and additional amounts
    max_insurance_building =  pd.read_excel(path+'/Table 2 Maximum Amount Insurance Available Building.xlsx')
    if inputs['program'] =='Regular':
        if inputs['ocupancy']=='Residential':
            default_basic_b = max_insurance_building.iloc[0]['Regular Program, Basic Insurance Limits, Building Coverage']
            default_additional_b = max_insurance_building.iloc[0]['Regular Program, Additional Insurance Limits, Building Coverage']
        else:
            default_basic_b = max_insurance_building.iloc[2]['Regular Program, Basic Insurance Limits, Building Coverage']
            default_additional_b = max_insurance_building.iloc[2]['Regular Program, Additional Insurance Limits, Building Coverage']
    #else statement will be for emergency program
    if inputs['building_coverage']>default_basic_b and inputs['building_coverage']<=default_basic_b+default_additional_b:
        basic_building_insurance = default_basic_b
        additional_building_insurance = inputs['building_coverage'] - default_basic_b
    elif inputs['building_coverage']<=default_basic_b:
        basic_building_insurance = inputs['building_coverage']
        additional_building_insurance = 0
    else:
        basic_building_insurance = default_basic_b
        additional_building_insurance = default_additional_b
    ##################################################################
    #get the rates
    if inputs['flood_zone'] == 'AE' or inputs['flood_zone'] == 'A1-A30':
        if inputs['date_construction']== 'Post-Firm':      
            building_rate_table = pd.read_excel(path+'/Rate Table 3B Building Rates.xlsx')
            icc_table = 'Table 3B'            
            if inputs['ocupancy']=='Residential':
                if inputs['basement/enclosure']=='None':
                    if inputs['number_floors']>1: 
                        rate_part_b = '1+ Floor, No Basement/Enclosure/Crawlspace, 1-4 Family, '
                    else:
                        rate_part_b = '1 Floor, No Basement/Enclosure/Crawlspace, 1-4 Family, '
                else:
                    rate_part_b = '1+ Floor, With Basement/Enclosure/Crawlspace, 1-4 Family, '
            if inputs['ocupancy']=='Others' or inputs['ocupancy']=='Other Residential' or inputs['ocupancy']=='Non-Residential Business' or inputs['ocupancy']=='Other Non-Residential':
                if inputs['basement/enclosure']=='None':
                    if inputs['number_floors']>1: 
                        rate_part_b = '1+ Floor, No Basement/Enclosure/Crawlspace, Others, '
                    else:
                        rate_part_b = '1 Floor, No Basement/Enclosure/Crawlspace, Others, '
                else:
                    rate_part_b = '1+ Floor, With Basement/Enclosure/Crawlspace, Others, '
        building_rates = building_rate_table.loc[building_rate_table[building_rate_table.columns[0]]==inputs['elevation_diff']]
        
        basic_rate_b = building_rates.iloc[0][rate_part_b+'Basic']
        additional_rate_b = building_rates.iloc[0][rate_part_b+'Additional']

    if inputs['flood_zone'] == 'VE' or inputs['flood_zone'] == 'V1-V30':
        if inputs['date_construction'] == '1981 Post-Firm':
            if inputs['basement/enclosure']=='None':
                rate_table = pd.read_excel(path+'/Rate Table 3E.xlsx')
                first_part = 'Elevated Buildings Free of Obstruction, '
                icc_table = 'Table 3E' 
            else:
                rate_table = pd.read_excel(path+'/Rate Table 3F.xlsx')
                first_part = 'Elevated Buildings With Obstruction, '
                icc_table = 'Table 3F' 
            rates = rate_table.loc[rate_table[rate_table.columns[0]]==inputs['elevation_diff']]
      
            rate_part_b = first_part + 'Building, Replacement cost ratio ' + inputs['Replacement cost ratio']
            
            building_rates = rates.iloc[0][rate_part_b]
            basic_rate_b = building_rates
            additional_rate_b = building_rates
            
    ####Step 1
    annual_premium_building = basic_rate_b*(basic_building_insurance/100) + additional_rate_b*(additional_building_insurance/100) 
    ###Step 2
    if inputs['ocupancy']=='Residential':
        deductible_factor_table = pd.read_excel(path+'/Rate Table 8B_Residential_Building.xlsx')
    else:
        deductible_factor_table = pd.read_excel(path+'/Rate Table 8B_Others_Building.xlsx')
    deductible_factors = deductible_factor_table[deductible_factor_table['Deductible Building']==inputs['building_deductible']]
    if inputs['date_construction']== 'Post-Firm' or inputs['date_construction'] == '1981 Post-Firm':
        deductible_factor = deductible_factors.iloc[0]['Pre-/Post-Firm Full-Risk']
    annual_subtotal = round(deductible_factor * (annual_premium_building),0)
    ###Step 3
    #icc premium
    icc_premium_table = pd.read_excel(path+'/Rate Table 9.xlsx')
    icc_premiums = icc_premium_table.loc[icc_premium_table['Rate Table']==icc_table]
    if inputs['ocupancy']=='Residential':
        if inputs['building_coverage']<=230000:
            column_part =  '1-4 Family, Building Insurance, 1-230000'
        else:
            column_part =  '1-4 Family, Building Insurance, 230001-250000'
    else:
        if inputs['building_coverage']<=480000:
            column_part =  'Others, Building Insurance, 1-480000'
        else:
            column_part =  'Others, Building Insurance, 480001-500000'
    icc_premium = icc_premiums.iloc[0][column_part]
    subtotal_icc = annual_subtotal + icc_premium
    #CRS rating
    if inputs['CRS_Rating']>=1 and inputs['CRS_Rating']<=9:
        crs_premium_table = pd.read_excel(path+'/Table 2 CRS Premium Discounts by Class and Flood Zone.xlsx')
        crs_premiums = crs_premium_table.loc[crs_premium_table['Class']==inputs['CRS_Rating'] ]
     
        if inputs['flood_zone'] == 'AE' or inputs['flood_zone'] == 'A1-A30' or inputs['flood_zone'] == 'VE' or inputs['flood_zone'] == 'V1-V30' or inputs['flood_zone'] == 'AO'or inputs['flood_zone'] == 'AH':
            crs_premium = crs_premiums.iloc[0][1]
        else:
            crs_premium = crs_premiums.iloc[0][2]   
    else:
        crs_premium = 0
    subtotal_crs = (subtotal_icc) * (100-crs_premium)/100   
    #other fees
    RFA =  round(subtotal_crs * 0.18,0)          
    probation_surcharge = [0 if inputs['Probation']=='No' else 50][0]
    hfiaa_surcharge = [250 if inputs['Primary_residence'] =='No' else 25][0]
    fpf = 50
    total_amount_due = subtotal_crs + RFA + probation_surcharge + hfiaa_surcharge + fpf
    return round(total_amount_due,0)

