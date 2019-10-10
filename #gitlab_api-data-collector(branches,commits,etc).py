import urllib3, json, array, csv, os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd

http = urllib3.PoolManager()

project_key = input("enter the project key :")

datevalue = datetime.strftime(datetime.now() - timedelta(10), '%Y-%m-%d')

print("From date : ")
print(datevalue)

with open('#repository.csv','rt') as f:
    data = csv.reader(f)
    for row in data:
        branch = row[2]
        word = branch.split(',') 
        for i in word:
            print("->"+str(i))
            url = "https://gitlab.com/api/v4/projects/"+str(row[1])+"/repository/commits?ref_name="+str(i)+"&per_page=10000&since="+datevalue
            response = http.request('GET', url , headers={"PRIVATE-TOKEN" : project_key})
            if response.status == 200:
                print("  status: success")
            else:
                print("  status: Failure")
            soup = BeautifulSoup(response.data, "html.parser")
            json_data = json.loads(soup.text)
            for j in json_data:
                url = "https://gitlab.com/api/v4/projects/"+str(row[1])+"/repository/commits/"+j['short_id']
                response = http.request('GET', url , headers={"PRIVATE-TOKEN" : project_key})
                json_data2 = json.loads(response.data)
                j.update({'stats': str(json_data2['stats'])})
                try:
                    j.update({'ref': str(json_data2['ref'])})
                except:
                    j.update({'ref': 'Null'})
            #
            #specify the path here
            #
            path = os.getcwd()+'\\#result\\'
            try:
                pd.read_json(json.dumps(json_data)).to_csv(path+str(row[0])+'_'+str(i)+'.csv', columns=['id',  'title',  'committer_name', 'committer_email', 'committed_date', 'stats', 'ref'])
            except:
                print(" ")
                if str(i):
                    print(str(i)+" has no commits")             
                print(" ")


