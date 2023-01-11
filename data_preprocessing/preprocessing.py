import re
import pandas as pd
from database_management.database import *
import re
from datetime import datetime, timedelta


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