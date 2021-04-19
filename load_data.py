import pymongo
import pandas as pd
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 400000)
pd.set_option("display.width", 1000)

client = pymongo.MongoClient("mongodb+srv://NP:tOYXKh1oK35JIp0m@cluster0.vnniz.mongodb.net/stackoverflowsurvey?retryWrites=true&w=majority")

collection = client.stackoverflowsurvey.SO

insert = False

if insert is True:

    # Read and dict creation of survey Data
    survey_data = pd.read_csv('survey_data_modified.csv')
    survey_data.drop(columns='Unnamed: 0', inplace=True)
    survey_data = survey_data.to_dict(orient='split')
    # survey_data = pd.DataFrame().from_dict(survey_data, orient='index')

    # Read and dict creation of unique languages
    language_info = open("language_info_unique.txt", "r").read()
    language_info = sorted(language_info.split(','))
    language_info = {'index': language_info}
    records = [survey_data, language_info]

    # Delete any existing records
    delete_records = collection.delete_many({})
    # Insert survey data and language info into collection
    insert_data = collection.insert_many(records)

# .find() returns a list containing the documents.
survey_data = collection.find()[0]
language_info = collection.find()[1]['index']

# Create Dataframe using the dictionary keys returned by .find()
survey_data = pd.DataFrame(columns=survey_data['columns'], data=survey_data['data'])
client.close()
