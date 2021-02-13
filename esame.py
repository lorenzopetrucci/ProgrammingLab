class ExamException(Exception):
    pass

# Classe ispirata a quella fatta a lezione
class CSVTimeSeriesFile:
    
    def __init__(self, name):
        
        self.name = name
        
    def get_data(self):
        
        values = []
        
        # Controllo che il valore in input sia una stringa per evitare un 
        # eventuale int che verrebbe accettato come parametro a open()
        if isinstance(self.name, str):
            
            try:
                my_file = open(self.name, 'r')
            except: 
                raise ExamException('Impossibile aprire il file')
        
        else:
            raise ExamException('Il parametro passato non è una stringa')

        for line in my_file:
            
            elements = line.split(',')
            
            # Per ogni riga provo a convertire l'elemento prima della prima 
            # virgola in int e quello dopo in float, altrimenti salto la riga
            try:
                epoch = int(float(elements[0]))
                temperature = float(elements[1])
            except:
                continue
            
            # Controllo che il secondo valore (la temperatura) sia superiore
            # allo zero assoluto e in caso positivo lo aggiungo alla lista  
            if temperature > -273.15:
                values.append([epoch, temperature])
                
            # Controllo epoch duplicati o fuori ordine
            check_value = None
            for value in values:
                
                if check_value is None:
                    check_value = value[0]
                else:
                    if value[0] <= check_value:
                        raise ExamException('Timestamp duplicato o fuori ordine')
                
                check_value = value[0]
        
        my_file.close()

        return(values)

# Assegno all'argomento della funzione il valore None in modo che una chiamata 
# della funzione senza parametri venga comunque accettata ed intercettata nei
# controlli sucessivi
def daily_stats(time_series = None):
    
    # Controllo che la variabile passata sia una lista con almeno due colonne
    try:
        time_series[0][0]
    except:
        raise ExamException('L\'argomento della funzione dev\'essere una lista con almeno due colonne')
    
    # Non posso escludere a priori un epoch negativo. Nel caso tale valore sia in 
    # mezzo alla lista viene poi intercettato come 'Timestamp fuori ordine', ma nel
    # caso questo sia il primo valore della serie controllo che anche l'ultimo valore
    # sia negativo, in caso contrario significa che i valori coprono un periodo come 
    # minimo a cavallo tra due mesi, e quindi contrari alle specifiche date
    if (time_series[len(time_series) - 1][0] * time_series[0][0] < 0):
        raise ExamException('La lista contiene valori antecedenti e successivi al 01/01/1970')

    # Variabile per le statistiche giornaliere
    daily_stats = []
    
    # Variabile per le temperature di ogni giornata
    values = []
    
    # Variabile per capire se sono nello stesso giorno, 
    # inizializzata al primo epoch della lista
    current_day = time_series[0][0] // 86400
    
    # Statistiche giornaliere
    max_value = time_series[0][1]
    min_value = time_series[0][1]
    
    # Ciclo su ogni elemento della lista
    for element in time_series:
        
        # Caso in cui il giorno sia uguale
        if (element[0] // 86400) == current_day:
                                   
            # Aggiungo la temperatura alla lista
            values.append(element[1])
            
            # Se il valore in esame è superiore o inferiore a 
            # massimo o minimo attuali sostituisco i loro valori
            if max_value < element[1]:
                max_value = element[1]
                
            if min_value > element[1]:
                min_value = element[1]
        
        # Caso in cui passo al giorno successivo
        else:
            # Faccio la media dei valori del giorno appena concluso
            average = sum(values) / len(values)
            
            # Aggiungo le tre statistiche alla lista
            daily_stats.append([min_value, max_value, average])
            
            # Aggiorno il giorno ed il momento dei 
            # controlli a quelli attuali
            current_day = element[0] // 86400
            
            # Aggiungo la prima temperatura del nuovo giorno alla
            # lista e lo faccio diventare il nuovo massimo e minimo
            values = [element[1]]
            max_value = element[1]
            min_value = element[1]
    
    # Faccio la media e aggiungo le statistiche anche dell'ultima 
    # giornata controllata
    average = sum(values) / len(values)
    daily_stats.append([min_value, max_value, average])
    
    return(daily_stats)
