import csv
import random
random.seed(10)

# Generating the data
weather_data = []
for i in range(10):
    high_temp = random.randint(15, 50)
    low_temp = random.randint(10, 25)
    feel_like = random.randint(10, 45)
    rain_rate = random.uniform(0, 10)
    humidity = random.uniform(20, 100)
    weather_data.append([high_temp, low_temp, feel_like, rain_rate, humidity])

# Write the data to a CSV file
with open('weather.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['High', 'Low', 'Feel_Like', 'RainRate', 'Humidity'])
    writer.writerows(weather_data)


#Q2


weather = []
#opening the file in read mode and running a loop to display all data
with open('weather.csv','r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        weather.append(row)
  

print(weather)
for i in weather:
    print(i)


#Q3

#creating 3 empty list to be used later
average_temperatures = []
high_temps = []
low_temps = []

#looping through all elements in the weather list and performing math on them and saving data 
for line in weather:
    hi_temp = int(line[0])
    low_temp = int(line[1])
    avg_temp = (hi_temp + low_temp) / 2
    average_temperatures.append(avg_temp)
    high_temps.append(hi_temp)
    low_temps.append(low_temp)

print("Average Temperatures:", average_temperatures)
print("Highest of Hi:", max(high_temps))
print("Lowest of Hi:", min(high_temps))
print("Highest of Low:", max(low_temps))
print("Lowest of Low:", min(low_temps))


#Q4


#again opening the files in write mode to make a new csv file to store different type of data
with open('weather_output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Day', 'Temp Avg'])
    #looping over the loop with an extrenal counter
    i = 0
    for _ in average_temperatures:
        writer.writerow([i+1, average_temperatures[i]])
        i=i+1
    writer.writerow(['Highest of Hi'])
    writer.writerow([max(high_temps)])
    writer.writerow(['Lowest of Hi'])
    writer.writerow([min(high_temps)])
    writer.writerow(['Highest of Low'])
    writer.writerow([max(low_temps)])
    writer.writerow(['Lowest of Low'])
    writer.writerow([min(low_temps)])


#Q5


#Q1 again


with open('weather.txt', mode='w') as file:
    file.write('Hi Low FeelLike RainRate Humidity\n')  # Header
    for data in weather_data:
        file.write(' '.join(map(str, data)) + '\n')


weather_list_txt = []


#Q2 again


with open('weather.txt', mode='r') as file:
    next(file)  # Skip the header
    for line in file:
        weather_list_txt.append(line.strip().split())

print(weather_list_txt)


#Q3 again


average_temperatures_txt = []
hi_temps_txt = []
low_temps_txt = []

for line in weather_list_txt:
    hi_temp = int(line[0])
    low_temp = int(line[1])
    avg_temp = (hi_temp + low_temp) / 2
    average_temperatures_txt.append(avg_temp)
    hi_temps_txt.append(hi_temp)
    low_temps_txt.append(low_temp)

highest_hi_txt = max(hi_temps_txt)
lowest_hi_txt = min(hi_temps_txt)
highest_low_txt = max(low_temps_txt)
lowest_low_txt = min(low_temps_txt)

print("Average Temperatures:", average_temperatures_txt)
print("Highest of Hi:", highest_hi_txt)
print("Lowest of Hi:", lowest_hi_txt)
print("Highest of Low:", highest_low_txt)
print("Lowest of Low:", lowest_low_txt)


#Q4 again


with open('weather_output.txt', mode='w') as file:
    file.write('Day Temp Avg\n')  # Header
    for i, avg_temp in enumerate(average_temperatures_txt, 1):
        file.write(f"{i} {avg_temp}\n")
    file.write('\n')
    file.write('Highest of Hi\n')
    file.write(f"{highest_hi_txt}\n")
    file.write('Lowest of Hi\n')
    file.write(f"{lowest_hi_txt}\n")
    file.write('Highest of Low\n')
    file.write(f"{highest_low_txt}\n")
    file.write('Lowest of Low\n')
    file.write(f"{lowest_low_txt}\n")
