c = 299792458 # m/s

print("Relativgeschwndigkeit aus Dopplerverschiebung berechnen")
print()

f0 = float(input("Originalfrequenz:		"))
f =  float(input("verschobene Frequenz:		"))
print()

# modus = input("Annäherung oder Wegbewegung (a/w) ?	")
# print()


if f > f0:
    print("Satellit nähert sich Bodenstation")
    v = c * ((f/f0)**2-1) / ((f/f0)**2+1)	# Annäherung, falls f > f0
else:
    print("Satellit entfernt sich von der Bodenstation")
    v = c * (1-(f/f0)**2) / (1+(f/f0)**2)	# Wegflug




print(f"Relativgeschwindigkeit: 	{v:.2f}  m/s bzw. {v*3.6:.2f} km/h")

