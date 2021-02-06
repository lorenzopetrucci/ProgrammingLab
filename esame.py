class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    
    def __init__(self, name):
        self.name = name
        
    def get_data(self):
        
        values = []
        
        try:
            my_file = open(self.name, 'r')
        except: 
            raise ExamException('Impossibile aprire il file')

        for line in my_file:
            
            elements = line.split(',')
                            
            try:
                epoch = int(elements[0])
                temperature = float(elements[1])
                
            except:
                continue
            
            values.append([epoch, temperature])
        
        my_file.close()

        return(values)
    
def daily_stats(time_series):
    
    try:
        time_series[0][0]
    except:
        raise ExamException('La lista deve avere almeno due colonne di valori')
    
    if (time_series[len(time_series) - 1][0] * time_series[0][0] < 0):
        raise ExamException('La lista contiene valori antecedenti e successivi al 01/01/1970')
    
    #if (time_series[len(time_series) - 1][0] - time_series[0][0] > 2629744):
        #raise ExamException('La lista contiene valori superiori al mese')

    daily_stats = []
    values = []
    
    current_day = time_series[0][0] // 86400
    current_hour = (time_series[0][0] % 86400) - 1
    max_value = time_series[0][1]
    min_value = time_series[0][1]
    average = time_series[0][1]
    
    for element in time_series:
        
        if (element[0] // 86400) == current_day:
            
            if (element[0] % 86400) <= current_hour:
                raise ExamException('Timestamp fuori ordine')
            
            values.append(element[1])
            
            if max_value < element[1]:
                max_value = element[1]
                
            elif min_value > element[1]:
                min_value = element[1]
                
            current_hour = element[0] % 86400
                
        elif (element[0] // 86400) < current_day:
            raise ExamException('Timestamp fuori ordine')
            
        else:
            average = sum(values) / len(values)

            daily_stats.append([min_value, max_value, average])
            
            current_day = element[0] // 86400
            current_hour = element[0] % 86400
            values = [element[1]]
            max_value = element[1]
            min_value = element[1]
            average = element[1]
            
    average = sum(values) / len(values)
    
    daily_stats.append([min_value, max_value, average])
    
    return(daily_stats)
        
time_series_file = CSVTimeSeriesFile('data.csv')
time_series = time_series_file.get_data()
print(daily_stats(time_series))
print(time_series)
#print(len(time_series))

#a = [1, 5, 7, 2]
#b = []
#print(daily_stats(a))        

