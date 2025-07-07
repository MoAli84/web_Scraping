import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime 
  
log_file = "log_file.txt" 
target_file = "transformed_data.csv" 

def extract_csv(source):
    dataframe = pd.read_csv(source)
    return dataframe

def extract_json(source):
    dataframe = pd.read_json(source,lines=True)
    return dataframe
def extract_xml(source):
    dataframe = pd.DataFrame(columns=[ 'car_model', 'year_of_manufacture', 'price', 'fuel'])
    tree = ET.parse(source)
    root = tree.getroot()
    for car in root:
        model = car.find('car_model').text
        year = int(car.find('year_of_manufacture').text)
        price = float(car.find('price').text)
        fuel = car.find('fuel').text
        row = {
            'car_model': model,
            'year_of_manufacture': year,
            'price': price,
            'fuel': fuel}
        dataframe = pd.concat([dataframe, pd.DataFrame([row])], ignore_index=True)
    return dataframe
def extract():
    extracted_data =pd.DataFrame(columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])
    for csvfile in glob.glob("*.csv"):
        extracted_data = pd.concat([extracted_data,pd.DataFrame(extract_csv(csvfile))], ignore_index=True)

    for jsonfile in glob.glob("*.json"):
        extracted_data = pd.concat([extracted_data,pd.DataFrame(extract_json(jsonfile))], ignore_index=True)    
    
    for xmlfile in glob.glob("*.xml"):
        extracted_data = pd.concat([extracted_data,pd.DataFrame(extract_xml(xmlfile))], ignore_index=True)
    return extracted_data


def transform(data):
    data["price"]= round(data.price , 2)
    return data 

def load_data(target_file, transformed_data): 
    transformed_data.to_csv(target_file) 


def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 

# Log the initialization of the ETL process 
log_progress("ETL Job Started") 
  
# Log the beginning of the Extraction process 
log_progress("Extract phase Started") 
extracted_data = extract() 
  
# Log the completion of the Extraction process 
log_progress("Extract phase Ended") 
  
# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data) 
print("Transformed Data") 
print(transformed_data) 
  
# Log the completion of the Transformation process 
log_progress("Transform phase Ended") 
  
# Log the beginning of the Loading process 
log_progress("Load phase Started") 
load_data(target_file,transformed_data) 
  
# Log the completion of the Loading process 
log_progress("Load phase Ended") 
  
# Log the completion of the ETL process 
log_progress("ETL Job Ended") 

