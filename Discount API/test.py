from urllib import response
import requests
import csv

BASE = "http://127.0.0.1:5000/"
#BASE = "http://allanchuang1.pythonanywhere.com/"

data = []

with open('course_info.csv', mode ='r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    for row in csv_reader:
        row_value = {'course_id': str(row['CourseCode']), 'course_name': str(row['CourseName']), 'description': str(row['Description']),
                    'GPA': int(row['\ufeffGPA']), 'ASS1': float(row['Assessment1']), 'ASS2': float(row['Assessment2']), 'ASS3': float(row['Assessment3']), 'Exam': float(row['Exam'])}
        data.append(row_value)

print(data)

for i in range(len(data)):
    response = requests.put(BASE + 'course/' + str(data[i]['course_id']), data[i])

"""

response = requests.get(BASE + 'course/csse2010')
print(response.json())
"""

#response = requests.patch(BASE + "video/2", {"views": 99})
#print(response.json())
