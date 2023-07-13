import os
#############################
# path = "D:/Risk Rating 2.0/"
# xl = pd.ExcelFile(path+'fema_appendix-d-rating-factor-tables.xlsx')

# import os
# if not os.path.exists(path+"tables"):
#     os.mkdir(path+"tables")

# for sheet in xl.sheet_names:
#     df = pd.read_excel(xl,sheet_name=sheet)
#     df.to_excel(path+"tables/"+f"{sheet}.xls",index=False)
###########################
inputs = {}
###added variables to inputs
inputs['State'] = 'MI'
inputs['State (Long)'] = 'Michigan'
inputs['County'] = 'Bay County'
inputs['Levee'] = 'NL'
inputs['Levee System ID'] = ''
inputs['HUC12'] = '040801020106'
inputs['Barrier island indicator'] = 'No'
inputs['DTR'] = 420.8
inputs['ERR'] = 10.2
inputs['DA'] = 12.6
inputs['SRE'] = 4.2
inputs['DTC'] = "N/A"
inputs['DTO'] = "N/A"
inputs['Elevation'] = 585.3
inputs['DTL'] = 48.3
inputs['ERL'] = 6.2
inputs['River class'] = 'A'
inputs['Type of Use'] = 'Single-Family Home - Frame'
inputs['Single family home indicator'] = 'Yes'
inputs['Condo unit owner indicator'] = 'No'
inputs['Floor of interest'] = '1-2'
inputs['Foundation type'] = 'Slab' #'Elevated without Enclosure, Post, Pile, or Pier'
inputs['First floor height'] = 0.5
inputs['Foundation design'] = 'Closed, Wall'
inputs['Flood vents'] = 'No'
inputs['M&E'] = 'No'
inputs['Prior claims'] = 0
inputs['Coverage A value'] = 250000
inputs['Coverage C value'] = 100000
inputs['Coverage A limit'] = 250000
inputs['Coverage C limit'] = 100000
inputs['Coverage A deductible'] = 1250
inputs['Coverage C deductible'] = 1250
inputs['CRS discount'] = 15
inputs['Reserve fund'] = 1.15
inputs['Probation surcharge'] = 0
inputs['Primary residence indicator'] = 'Yes'
inputs['Federal policy fee'] = 50
inputs['ICC premium'] = 4

inputs['Prior Claim Rate'] = 2
inputs['Loss Constant'] = 130
inputs['Expense Constant'] = 62.99

path = r"C:\Computer backup\FloodSafeHome\Risk rating 2\Risk Rating 2 Calculator"
os.chdir(path+'/Scripts')

if inputs['Levee'] == 'NL':  
    from NL_premium_individual_building import *
    path1 = path+"/tables/" + inputs['Levee']+ "/"    
    if inputs['Barrier island indicator'] == 'Yes':
        path2 = path+"/tables/NL/BI/"
    else:
        path2 = path+"/tables/NL/Non-BI/"
    risk_rating_df = NL_premium(path,path1,path2,inputs)
    risk_rating_df.to_csv(path+ '/sample3.csv', index=False)


if inputs['Levee'] == 'L':   
    from L_premium_individual_building import *
    path1 = path+"/tables/" + inputs['Levee'] + "/"
    risk_rating_df = L_premium(path,path1,inputs)
    risk_rating_df.to_csv(path+ '/sample4.csv', index=False)

