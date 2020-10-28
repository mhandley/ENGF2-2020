
mark = {'Name': 'Mark Handley',
        'Age': 157,
        'Room': '6.21'}
brad = {'Name': 'Brad Karp',
        'Age': None,
        'Room': '6.22'}
stefano = {'Name': 'Stefano Vissichio',
           'Age': 21,
           'Room': '6.19'}

courses = {'ENGF0002': mark, 
           'COMP0023': stefano,
           'COMP0019': brad}

print(courses['ENGF0002']['Name'])
print(courses['COMP0023']['Room'])
