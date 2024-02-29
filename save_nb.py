import os
import pandas as pd

cwd = os.getcwd()
file_path = os.path.join(cwd, 'nb_rows.txt')
csv_save_path = os.path.join(cwd, 'data.csv')

csv_path = 'C:/Users/Houssem/Downloads/CICFlowmeter/CICFlowmeter/bin/data/daily/2024-02-11_Flow.csv'


df = pd.read_csv(csv_path)

def update_nb_row(path,nb_rows):
    file = open(path, 'w').close()
    file = open(path, 'a')
    file.write(str(nb_rows))
    file.close()

update_nb_row(file_path, 40)


def save_csv(df,nb_rows,path):
    if(nb_rows==0):
        df.to_csv(path, index=False)
    else:
        df.to_csv(path, mode='a', header=False, index=False)


save_csv(df, 40, csv_save_path)



