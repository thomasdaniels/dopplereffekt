


# --- main ----

print("Berechnung des Bahnradius aus den aktuellen TLE-Elementen")
print()

antwort = input("TLEs laden oder TLEs einkopieren (l / k) ? ")

if antwort=="l":
    id = int(input("NORAD-ID: "))
    with open(f"{str(id)}.txt") as file:
        lines = [line.rstrip() for line in file]
    name = lines[0]
    tle1 = lines[2]
    tle2 = lines[3]
    print(tle1)
    print(tle2)
else:
    tle1 = input("TLE Zeile 1: ")
    tle2 = input("TLE Zeile 2: ")
    
felder1 = tle1.split()	# Aufteilung der Einträge als Liste von Strings
felder2 = tle2.split()

MM1 = float(felder2[7])
MM2f = float(felder1[4])
MM3f = 0

print(MM1)
print(MM2f)
print(MM3f)

print("Bahnhöhe berechnen für welche Uhrzeit?")
h = float(input("Stunden:	"))
m = float(input("Minuten:	"))

t = (h+m/60)/24	# Tagesbruchteil zwischen 0 und 1
print(t)

MM = MM1 + MM2f*t + MM3f*t*t
print(f'Umläufe pro Tag:	{MM}')

P = 86400 / MM
print(f'Umlaufszeit / s:	{P}')

a = 21.61355*P**(2/3)
print(f"gr. Halbachse:		{a}")

h = a - 6378
print(f"Bahnhöhe / km:		{h}")
print()

mE = 5.9722e+24
gamma = 6.67259e-11
vth = (gamma*mE/(a*1000))**0.5
print(f"theor. Bahngeschwindigkeit: 	{vth:.2f}  m/s bzw. {vth*3.6:.2f} km/h")

          