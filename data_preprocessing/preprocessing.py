import re
import pandas as pd
from database_management.database import *
import re
from datetime import datetime, timedelta
from statistics import mean

def fix_date():
    # Select data from database
    df = select_data()
    # Get all index where date_publication is null
    index = df[df['date_publication'].isna()].index
    # Convert insert_time column to date
    df['insert_time'] = pd.to_datetime(df['insert_time'])
    # %%
    # Chech tags column an replace date_publication column
    for i in index:
        if re.search("heure", df.loc[i, "tags"][0]):
            df.loc[i, 'date_publication'] = df.loc[i, "insert_time"]
            # update value
            update_value("_id", df.loc[i, '_id'], "date_publication", df.loc[i, 'date_publication'])
        elif re.search("jour", df.loc[i, "tags"][0]):
            delai = int(re.findall('\d+', df.loc[i, "tags"][0])[0])
            # update value
            df.loc[i, 'date_publication'] = df.loc[i, 'insert_time'] - timedelta(days=delai)
            update_value("_id", df.loc[i, '_id'], "date_publication", df.loc[i, 'date_publication'])
        else:
            print(df.loc[i, "tags"][0])
    # Convert date_publication to date type
    df['date_publication'] = pd.to_datetime(df['date_publication'])
    return df

def extract_education_level():
    df = select_data_with_filter('niveau_etude', 'null')
    for i in range(0, len(df)):
        description = df.loc[i, 'description']['desc']
        if re.search('bachelor', description.lower()):
            df.loc[i, "niveau_etude"] = 3
            update_value('_id', df.loc[i, '_id'], 'niveau_etude', df.loc[i, "niveau_etude"])
        elif re.search("bac\+\d+", description.lower()):
            if len(re.findall("bac\+\d+", description.lower())) == 1:
                niveau_etude = re.findall("bac\+\d+", description.lower())[0]
                niveau_etude = int(re.findall('\d+', niveau_etude)[0])
                df.loc[i, "niveau_etude"] = niveau_etude
                update_value('_id', df.loc[i, '_id'], 'niveau_etude', df.loc[i, "niveau_etude"])
            else:
                niveau_etude = []
                for n in re.findall("bac\+\d+", description.lower()):
                    niveau_etude.append(int(re.findall('\d+', n)[0]))
                df.loc[i, "niveau_etude"] = int(mean(niveau_etude))
                update_value('_id', df.loc[i, '_id'], 'niveau_etude', df.loc[i, "niveau_etude"])
        elif re.search("bac\s*\+\s*\d+", description.lower()):
            if len(re.findall("bac\s*\+\s*\d+", description.lower())) == 1:
                niveau_etude = re.findall("bac\s*\+\s*\d+", description.lower())[0]
                niveau_etude = int(re.findall('\d+', niveau_etude)[0])
                df.loc[i, "niveau_etude"] = niveau_etude
                update_value('_id', df.loc[i, '_id'], 'niveau_etude', df.loc[i, "niveau_etude"])
            else:
                niveau_etude = []
                for n in re.findall("bac\s*\+\s*\d+", description.lower()):
                    niveau_etude.append(int(re.findall('\d+', n)[0]))
                df.loc[i, "niveau_etude"] = int(mean(niveau_etude))
                update_value('_id', df.loc[i, '_id'], 'niveau_etude', df.loc[i, "niveau_etude"])
        elif re.search("bac plus \d+", description.lower()):
            print(re.findall("bac plus \d+", description.lower()))
        elif re.search("ingénieur", description.lower()):
            df.loc[i, "niveau_etude"] = 5
            update_value('_id', df.loc[i, '_id'], 'niveau_etude', df.loc[i, "niveau_etude"])
        elif re.search("ingenieur", description.lower()):
            df.loc[i, "niveau_etude"] = 5
            update_value('_id', df.loc[i, '_id'], 'niveau_etude', df.loc[i, "niveau_etude"])
        elif re.search("engineer", description.lower()):
            df.loc[i, "niveau_etude"] = 5
            update_value('_id', df.loc[i, '_id'], 'niveau_etude', df.loc[i, "niveau_etude"])
        elif re.search("\bmasters\b", description.lower()):
            df.loc[i, "niveau_etude"] = 5
            update_value('_id', df.loc[i, '_id'], 'niveau_etude', df.loc[i, "niveau_etude"])
        elif re.search("technicien", description.lower()):
            df.loc[i, "niveau_etude"] = 3
            update_value('_id', df.loc[i, '_id'], 'niveau_etude', df.loc[i, "niveau_etude"])
    return df