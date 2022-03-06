days = 31

sqlData = {
    'Living Room': [8.6, 7.0, 11.3, 8.1, 8.4, 9.4, 8.1, 8.8, 8.5, 8.2, 7.4, 8.9, 8.3, 7.8, 8.4, 6.8, 8.7, 6.6, 9.0, 7.3, 5.0, 9.7, 5.1, 4.6, 8.2, 7.9, 4.4, 7.4, 8.3, 6.7, 8.0],
    'Bedroom': [6.6, 6.9, 6.8, 7.9, 6.5, 6.4, 6.2, 6.3, 6.5, 7.3, 6.6, 7.8, 7.3, 7.3, 7.2, 7.1, 6.5, 7.9, 6.4, 6.7, 7.5, 6.8, 7.8, 7.7, 6.0, 7.4, 7.4, 6.0, 7.3, 6.7, 7.7],
    'Bathroom': [0.7, 1.7, 0.5, 0.8, 0.5, 1.0, 1.1, 0.8, 0.6, 1.4, 1.0, 1.4, 0.6, 1.0, 1.8, 0.8, 0.7, 1.9, 1.8, 1.7, 1.9, 1.5, 1.9, 1.9, 0.6, 2.0, 1.7, 1.9, 0.5, 1.7, 1.5],
    'Kitchen': [3.4, 3.0, 3.3, 3.8, 3.0, 3.6, 4.1, 4.1, 4.0, 3.3, 3.8, 3.4, 3.6, 4.3, 3.3, 3.3, 3.3, 3.9, 3.9, 3.3, 4.3, 3.4, 3.6, 4.1, 3.5, 3.1, 4.5, 3.8, 3.1, 3.4, 4.3],
}

colors = [["#4e73df", "#2e59d9"],
["#e74a3b", "#A8362C"],
["#36b9cc", "#247E8C"],
["#1cc88a", "#13875D"]]

data = {"bluetoothGraphDataset":[]}

# to generate time where no data recorded
outside = [24.0 for i in range(days)]

for count, label in enumerate(sqlData):
    data['bluetoothGraphDataset'].append(
        {"label":label, 
        "data":sqlData[label], 
        "backgroundColor":colors[count][0],
        "hoverBackgroundColor":colors[count][1]
    })

    for i in range(len(sqlData[label])):
        outside[i] = round(outside[i]-sqlData[label][i], 1)
        
data['bluetoothGraphDataset'].append(
    {"label":"Outside",
    "data":outside,
    "backgroundColor":"#C0CCC9",
    "hoverBackgroundColor":"#88908E"
})


# "bluetoothGraphDatasets": [{
#                 "label": "Living Room",
#                 "backgroundColor": "#4e73df",
#                 "hoverBackgroundColor": "#2e59d9",
#                 "data": 
#                 }, {
#                 "label": "Bedroom",
#                 "backgroundColor": "#e74a3b",
#                 "hoverBackgroundColor": "#A8362C",
#                 "data": 
#                 }, {
#                 "label": "Bathroom",
#                 "backgroundColor": "#36b9cc",
#                 "hoverBackgroundColor": "#247E8C",
#                 "data": 
#                 }, {
#                 "label": "Kitchen",
#                 "backgroundColor": "#1cc88a",
#                 "hoverBackgroundColor": "#13875D",
#                 "data": 
#                 }, {
#                 "label": "Outside",
#                 "backgroundColor": "#C0CCC9",
#                 "hoverBackgroundColor": "#88908E",
#                 "data": 
#                 }
#             ],