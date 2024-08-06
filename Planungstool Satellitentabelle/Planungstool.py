import urllib
import requests
import ephem
from datetime import datetime

# quick reference:
# https://rhodesmill.org/pyephem/quick.html
# http://celestrak.com/NORAD/elements/stations.txt






# api ohne Zugangsdate (NASA)
url = "https://tle.ivanstanojevic.me/api/tle/"


# array interessierender Satelliten, Norad IDs
# iss,  noaa15, 18 , 19, M2
sats = [25544,  25338, 28654, 33591, 40069] # iss,  noaa15, 18 , 19, M2
#sats = [7530, 24278, 40906, 40911, 44909, 50466, 53106, 56992, 59112, 60209, 43803] # ham radio sats

# nur Zeit ausgeben, Datum unterdrücken, "time only"
def to(d):
    h = d.tuple()[3]
    m = d.tuple()[4]
    s = d.tuple()[5]
    zeit = str(h)+":"+str(m)+":"+str(round(s))
    return zeit

# Winkel aus Grad, Minuten, Sekunden in Dezimalgrad
def winkel_in_dezimal(winkel_string):

    teile = winkel_string.split(":")
    grad = int(teile[0])
    minuten = int(teile[1])
    sekunden = float(teile[2])
    
    dezimalgrad = grad + (minuten / 60) + (sekunden / 3600)
    dezimalgrad = round(dezimalgrad, 2)
    return dezimalgrad

# Klasse für gettle zur gleichzeitigen Rückgabe von 4 Werten
class return_tle:
    def __init__(self,a,b,c,d):
        self.a=a
        self.b=b
        self.c=c
        self.d=d

# Func gibt 4 Werte zurück
def gettle(noradid):
    json_data = requests.get(url+str(noradid)).json()

    #print(json_data)

    json_name=json_data['name']
    #print (json_name)

    json_date=json_data['date']
    #print (json_date)

    json_line1=json_data['line1']
    #print (json_line1)

    json_line2=json_data['line2']
    #print (json_line2)
    
    t = return_tle(json_name, json_date, json_line1, json_line2)
    return t


# Sortiere die Liste basierend auf den extrahierten Datums- und Zeitangaben 
def sort_strings_by_custom_datetime(string_list):
    """
    Sortiert eine Liste von Strings basierend auf Datums- und Zeitangaben am Anfang der Strings.

    :param string_list: Liste von Strings mit Datums- und Zeitangaben am Anfang
    :return: Sortierte Liste von Strings
    """
    def extract_datetime(string):
        # Extrahiere den Datums- und Zeitteil
        datetime_str = string.split(None, 1)[0] + ' ' + string.split(None, 1)[1].split()[0]
        try:
            # Formatiere die Datums- und Zeitangaben so, dass sie immer zweistellig sind
            parts = datetime_str.split('/')
            year = parts[0]
            month_day_time = parts[1].split(' ')
            month = month_day_time[0] if len(month_day_time[0]) == 2 else f"0{month_day_time[0]}"
            day_time = parts[2].split(' ')
            day = day_time[0] if len(day_time[0]) == 2 else f"0{day_time[0]}"
            time = day_time[1]
            formatted_str = f"{year}/{month}/{day} {time}"
            datetime_obj = datetime.strptime(formatted_str, "%Y/%m/%d %H:%M:%S")
            return datetime_obj
        except ValueError:
            raise ValueError(f"Datum und Zeit im String '{string}' entsprechen nicht dem Format '%Y/%m/%d %H:%M:%S'")
    
    # Sortiere die Liste basierend auf den extrahierten Datums- und Zeitangaben
    sorted_list = sorted(string_list, key=extract_datetime)
    return sorted_list


# astronomische Daten
def astro():
    print("Astronomische Daten: (UTC)")
    moon = ephem.Moon(location)
    
    print("MA: "+str(location.next_rising(moon))+"	MU: "+str(location.next_setting(moon))+"	MP: "+str(round(moon.phase,1))+ "%")
    #print("MU: "+str(location.next_setting(moon)))
    #print("MP: "+str(round(moon.phase,1))+ "%")
    
    sun = ephem.Sun(location)  
    print("SA: "+str(location.next_rising(sun))+"	SU: "+str(location.next_setting(sun)))
    #print("SU: "+str(location.next_setting(sun)))
    print()


# hole und speichere TLEs
def getandsaveTLEs():
    for id in sats:

        try:
            x = gettle(id)
        except:
            print("Keine aktuellen TLE für " +str(id)+" erhalten!")
            exit() # oder mit return nur Funktion abbrechen und mit alten Daten weiterrechnen
        
        #print(x.a, x.b)		# Ausgabe Name, Datum der TLE 1 & 2
        #print(x.b)
        #print(x.c)	# TLE1
        #print(x.d)	# TLE2

        dateiname= f'{id}.txt'
        file = open(dateiname, 'w') # w überschreibt Vorhandenes, a hängt an
        file.write(x.a + "\n")
        file.write(x.b + "\n")
        file.write(x.c + "\n")
        file.write(x.d + "\n")
        file.close()

# main --------------------------------------------------

print("Planungstool für Satellitenüberflüge")
print()
j = input("Jahr:	")
m = input("Monat:	")
t = input("Tag:		")



location=ephem.Observer()
location.date = f'{j}/{m}/{t} 00:00:00' # in UTC
print()


b = input("Breitengrad:	")
l = input("Längengrad:	")
location.lat=b
location.long=l





if (input("TLEs neu herunterladen? ") == "j"):
    getandsaveTLEs()


# zu Testzwecken auslesen:
"""
with open("25544.txt") as file:
    lines = [line.rstrip() for line in file]

print(lines)
name = lines[0]
tle1 = lines[2]
tle2 = lines[3]
print(name, tle1, tle2)
"""

astro()


table=[]

passes = int(input("Wie viele Überflüge? "))
print()


print("AOS/UTC			Azimuth	AOS	   MAX/UTC	  MAX EL/°	   LOS/UTC	  Azimuth LOS    Name")		

for id in sats:

    """
    try:
        x = gettle(id)
    except:
        print("Keine aktuellen TLE für " +str(id)+" erhalten!")
    
    #print(x.a, x.b)		# Ausgabe Name, Datum der TLE 1 & 2
    #print(x.b)
    #print(x.c)	# TLE1
    #print(x.d)	# TLE2
    """

    location.date = datetime.now()

    with open(f"{str(id)}.txt") as file:
        lines = [line.rstrip() for line in file]
    name = lines[0]
    tle1 = lines[2]
    tle2 = lines[3]
    


    for p in range(passes):
     
        #SAT = ephem.readtle(x.a, x.c, x.d)
        SAT = ephem.readtle(name, tle1, tle2)
        info = location.next_pass(SAT)
    
        i0 = str(info[0])
        i1 = winkel_in_dezimal(str(info[1]))
        i2 = to(info[2])
        i3 = winkel_in_dezimal(str(info[3]))
        i4 = to(info[4])
        i5 = winkel_in_dezimal(str(info[5]))
        i6 = name
        print(f'{i0:<20}	{i1:>11}	{i2:>11}	{i3:>12}	{i4:>10}	{i5:>12}	{i6:<12}')
        row = f'{i0:<20}	{i1:>11}	{i2:>11}	{i3:>12}	{i4:>10}	{i5:>12}	{i6:<12}'
       
        table.append(row)
        
        location.date = info[4]


# zeitlich sortierte Tabelle ausgeben und als Datei speichern

print("---")
table = sort_strings_by_custom_datetime(table)

dateiname= f'{str(location.date).replace("/","-")}.txt'
file = open(dateiname, 'w') # w überschreibt Vorhandenes, a hängt an

file.write("AOS/UTC			Azimuth	AOS	   MAX/UTC	  MAX EL/°	   LOS/UTC	  Azimuth LOS    Name"+"\n")

for rows in table:
    print(rows)
    file.write(rows + "\n") 

file.close()




    #print(x.a)			# Name
    #print(info[0])     # Aufgangszeit
    #print(info[1])     # Azimuth bei Aufgang
    #print(info[2])     # Zeit des größten Höhe
    #print(info[3])     # größte Höhe in Grad
    #print(info[4])     # Untergangszeit
    #print(info[5])     # Azimuth bei Untergang
    #ISS.compute(location)
    #print(ISS.range)   # Entfernung
    #print(ISS.sublat)
    #print(ISS.sublong)
    #print("-----------------------")
    

