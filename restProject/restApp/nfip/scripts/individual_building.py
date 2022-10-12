import os

path = r"F:/fsh-django-rest-api/restProject/restApp/nfip"
os.chdir(path+'/scripts')
from nfip_policy_functions import *

#get the inputs
inputs = {}
inputs['program'] = 'Regular'
inputs['flood_zone'] = 'A'
inputs['Type of EC'] =  'BFE' # for A-zone
inputs['date_construction'] =  'Post-Firm' 
#inputs['flood_zone'] = 'V'
#inputs['date_construction'] =  '1981 Post-Firm' #'1975-81 (Post-Firm)'
##Replacement cost ratio = Building coverage to replacement cost
#inputs['Replacement cost ratio'] = '0.75 or more' #'0.50 to 0.74', 'under 0.50  

inputs['ocupancy'] = 'Residential'
inputs['number_floors'] = 2
inputs['basement/enclosure'] = 'None'

if inputs['basement/enclosure'] == 'None':
    if inputs['number_floors'] == 1:
        inputs['contents_location'] = 'Only - Above Ground Level' #'Above Ground Level and Higher Floors'
    else:
        inputs['contents_location'] = 'Above Ground Level and Higher Floors' #'Above Ground Level and Higher Floors'

inputs['elevation_diff'] = 6
inputs['floodproofed'] = 'No'

inputs['building_coverage'] = 140000
inputs['contents_coverage'] = 70000
inputs['building_deductible'] = 1250
inputs['contents_deductible'] = 1250

inputs['CRS_Rating'] = 10
inputs['Probation'] = 'No'
inputs['Primary_residence'] = 'No'

#Esimate the premium
total_amount_due = homeowner_policy(path,inputs)
# total_amount_due = landlord_policy(path, inputs)
# total_amount_due = tenant_policy(path, inputs)

print("Homeowner premium = ",total_amount_due)
