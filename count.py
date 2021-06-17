
import glob

sum = 0

for filepath in glob.iglob('/Users/jiaweitchea/desktop/finproj/new_data/*.json'):
    fname1 = filepath.split("_")
    fname2 = fname1[-1].split("-")
    dataCount = fname2[0]

    if dataCount.isdigit():
        sum += int(dataCount)

#12549 + 100/75314
print("Total data:",sum)


import index2


filenames = index2.read_data_filenames()
json_files = index2.load_json_files(filenames)
backers_projects_urls = index2.backers_projects(json_files)



'''
import json
import pprint
f = open('data/data20_1.json','r')
data = json.load(f)

for backer_project in data:
    backer = backer_project[0]
    projects = backer_project[1]

    for project in projects:
        project = json.loads(project)
        project_url = project['urls']['web']['project']
        project_name = project['name']
        print(project_name)
        #break
'''


#print(data[0][1][0]['id'])
#print("===========================================")
#print(data[0][0])
