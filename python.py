""" Import Packages """
import pandas as pd

""" importing datasets """

sparcs =  pd.read_csv ('Data/CSV/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv', nrows=10000) #import Hospital Inpatient Discharges (SPARCS) CSV File (Reduce size of rows for coding stability)
 
nys_atlas = pd.read_csv ('Data/CSV/NY_2019_ADI_9 Digit Zip Code_v3.1.csv',nrows=10000) # Import the Neighborhood Atlas File (Reduce size of rows for coding stability)

""" View Colummns """
sparcs.columns # SPARCS Columns 

nys_atlas.columns # the Neighborhood Atlas

""" Clean File Columns """
 
# Clean SPARCS CSV Columns 

sparcs.columns = sparcs.columns.str.lower() # change all column names to lowercase

sparcs.columns = sparcs.columns.str.replace(' ', '_') # replace all whitespace in column names with an underscore

sparcs.columns = sparcs.columns.str.replace('[^A-Za-z0-9]+', '_') # remove all special characters and whitespace ' ' from a specific column 

# Clean NYS Atlas CSV Columns 

nys_atlas.columns = nys_atlas.columns.str.lower() # change all column names to lowercase

nys_atlas.columns = nys_atlas.columns.str.replace(' ', '_') # replace all whitespace in column names with an underscore

nys_atlas.columns = nys_atlas.columns.str.replace('[^A-Za-z0-9]+', '_') # remove all special characters and whitespace ' ' from a specific column 

""" Reduce Columns """

nys_atlas_small = nys_atlas[['zipid','gisjoin','adi_staternk']]

sparcs_small = sparcs[['health_service_area','facility_id','facility_name','zip_code_3_digits']]

""" Data Enrichment (By ZipCode) """

nys_atlas_small['zip_3'] = nys_atlas_small['zipid'].str.slice(1, 4) # Create a new column to generate a Common Key among excel files

 # Merge Files through left join 
combined_sparcs = nys_atlas_small.merge( 
sparcs_small, how = 'left', left_on = 'zip_3', right_on = 'zip_code_3_digits')

combined_sparcs = pd.merge(nys_atlas_small, sparcs_small,
how='left', left_on='zip_3', right_on='zip_code_3_digits')

combined_sparcs.columns # Confirm Merged columns 


print(combined_sparcs.sample(100))


combined_sparcs.dropna(inplace=True) # Remove NAN rows

###    Unfortunatly i am unable to merge the file properly, 
###    this may be due to the rows that are selected from the 
###    n=10000 does not contain the same foregin key 'Zip_code_3_Digits'

print(combined_sparcs.sample(100))

combined_sparcs.to_csv('data/clean/Combined_Sparcs.csv')


