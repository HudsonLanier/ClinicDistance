import csv
testperson = ['1', '', '722 85 ST SW', 'T3H 1S6', 'T3H', 'CALGARY', 'AB', (51.0665226, -114.2094385)]
testperson2 = ['2', '', '1640 BLOOR ST W', 'M6P 1A7', 'M6P', 'TORONTO', 'ON', (43.6556336, -79.4564275)]
final_list = [testperson,
              testperson2]

correct_format = ['patient_id', 'pat_geo_cols', 'pat_geocode', 'pat_address', 'pat_postal_code',\
                  'pat_fsa', 'nearest_clinic_id', 'clinic_geo_cols', 'clinic_geocode', 'clinic_address',\
                  'clinic_postal_code' 'clinic_fsa', 'clinic_distance']

def format_data(patient):
    pass

#utput format: The output should be a csv of the following format: Patient_ID, Pat_Geo_Cols, Pat_Geocode,
# Pat_Address, Pat_Postal_Code, Pat_FSA, Nearest_Clinic_ID, Clinic_Geo_Cols, Clinic_Geocode, Clinic_Address,
# Clinic_Postal Code, Clinic_FSA, Clinic_Distance.


# need to have a value of the columns used to find the geocode of the clinic same for the patient
#need

with open('final_patients_list.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(final_list)