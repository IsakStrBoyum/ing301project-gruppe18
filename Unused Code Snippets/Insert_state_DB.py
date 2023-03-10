"""

# add states for actuators from Sensor-data to new table called states run only first time
list_of_measurement = []
counter = 0
f = codecs.open('Data/Sensor-data', 'r', 'UTF-8')
for line in f:
    list_of_measurement.append(line)
f.close()

for meas in list_of_measurement:
    list_of_measurement[counter] = meas.split('\t')
    list_of_measurement[counter][1] = list_of_measurement[counter][1].split(' ', 1)[0]
    persistence.cursor.execute("INSERT INTO states (device, state) VALUES (?,?) ",
                               (list_of_measurement[counter][0], list_of_measurement[counter][1]))
    persistence.save()
    counter += 1

"""