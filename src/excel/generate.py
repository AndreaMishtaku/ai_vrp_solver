import pandas as pd
import random
from datetime import datetime

locations=[
    {"id": 1, "name": "Genoa", "latitude": 44.4056, "longitude": 8.9463, "type": "NODE", "capacity": 0},
    {"id": 2, "name": "La Spezia", "latitude": 44.1025, "longitude": 9.8241, "type": "NODE", "capacity": 0},
    {"id": 3, "name": "Savona", "latitude": 44.3091, "longitude": 8.4771, "type": "NODE", "capacity": 0},
    {"id": 4, "name": "Sanremo", "latitude": 43.8159, "longitude": 7.7761, "type": "NODE", "capacity": 0},
    {"id": 5, "name": "Imperia", "latitude": 43.8897, "longitude": 8.0319, "type": "NODE", "capacity": 0},
    {"id": 6, "name": "Rapallo", "latitude": 44.3514, "longitude": 9.2303, "type": "NODE", "capacity": 0},
    {"id": 7, "name": "Chiavari", "latitude": 44.3162, "longitude": 9.3234, "type": "NODE", "capacity": 0},
    {"id": 8, "name": "Albenga", "latitude": 44.0493, "longitude": 8.2161, "type": "NODE", "capacity": 0},
    {"id": 9, "name": "Ventimiglia", "latitude": 43.7928, "longitude": 7.6077, "type": "NODE", "capacity": 0},
    {"id": 10, "name": "Sestri Levante", "latitude": 44.2735, "longitude": 9.3958, "type": "NODE", "capacity": 0},
    {"id": 11, "name": "Camogli", "latitude": 44.3462, "longitude": 9.1545, "type": "NODE", "capacity": 0},
    {"id": 12, "name": "Levanto", "latitude": 44.1705, "longitude": 9.6169, "type": "NODE", "capacity": 0},
    {"id": 13, "name": "Finale Ligure", "latitude": 44.1699, "longitude": 8.3363, "type": "NODE", "capacity": 0},
    {"id": 14, "name": "Alassio", "latitude": 44.0107, "longitude": 8.1704, "type": "NODE", "capacity": 0},
    {"id": 15, "name": "Portofino", "latitude": 44.3031, "longitude": 9.2095, "type": "NODE", "capacity": 0},
    {"id": 16, "name": "Bordighera", "latitude": 43.7849, "longitude": 7.6722, "type": "NODE", "capacity": 0},
    {"id": 17, "name": "Varazze", "latitude": 44.3598, "longitude": 8.5764, "type": "NODE", "capacity": 0},
    {"id": 18, "name": "Arenzano", "latitude": 44.4098, "longitude": 8.6806, "type": "NODE", "capacity": 0},
    {"id": 19, "name": "Bogliasco", "latitude": 44.3757, "longitude": 9.0488, "type": "NODE", "capacity": 0},
    {"id": 20, "name": "Santa Margherita Ligure", "latitude": 44.3319, "longitude": 9.2113, "type": "NODE", "capacity": 0},
    {"id": 21, "name": "Moneglia", "latitude": 44.2304, "longitude": 9.4723, "type": "NODE", "capacity": 0},
    {"id": 22, "name": "Noli", "latitude": 44.2134, "longitude": 8.4136, "type": "NODE", "capacity": 0},
    {"id": 23, "name": "Celle Ligure", "latitude": 44.3581, "longitude": 8.5515, "type": "NODE", "capacity": 0},
    {"id": 24, "name": "Zoagli", "latitude": 44.3298, "longitude": 9.2563, "type": "NODE", "capacity": 0},
    {"id": 25, "name": "Recco", "latitude": 44.3645, "longitude": 9.1364, "type": "NODE", "capacity": 0},
    {"id": 26, "name": "Cervo", "latitude": 43.9217, "longitude": 8.1184, "type": "NODE", "capacity": 0},
    {"id": 27, "name": "Dolceacqua", "latitude": 43.8541, "longitude": 7.6213, "type": "NODE", "capacity": 0},
    {"id": 28, "name": "Spotorno", "latitude": 44.2275, "longitude": 8.4248, "type": "NODE", "capacity": 0},
    {"id": 29, "name": "Varese Ligure", "latitude": 44.3897, "longitude": 9.5487, "type": "NODE", "capacity": 0},
    {"id": 30, "name": "Lerici", "latitude": 44.0794, "longitude": 9.9144, "type": "NODE", "capacity": 0},
    {"id": 31, "name": "Portovenere", "latitude": 44.0511, "longitude": 9.8319, "type": "NODE", "capacity": 0},
    {"id": 32, "name": "Pontinvrea", "latitude": 44.4103, "longitude": 8.4848, "type": "NODE", "capacity": 0},
    {"id": 33, "name": "Sassello", "latitude": 44.4835, "longitude": 8.5309, "type": "NODE", "capacity": 0},
    {"id": 34, "name": "Borgio Verezzi", "latitude": 44.1598, "longitude": 8.3083, "type": "NODE", "capacity": 0},
    {"id": 35, "name": "Riva Ligure", "latitude": 43.8494, "longitude": 7.8594, "type": "NODE", "capacity": 0},
    {"id": 36, "name": "Riomaggiore", "latitude": 44.0968, "longitude": 9.7353, "type": "NODE", "capacity": 0},
    {"id": 37, "name": "Monterosso al Mare", "latitude": 44.1474, "longitude": 9.6562, "type": "NODE", "capacity": 0},
    {"id": 38, "name": "Corniglia", "latitude": 44.1214, "longitude": 9.7124, "type": "NODE", "capacity": 0},
    {"id": 39, "name": "Vernazza", "latitude": 44.1341, "longitude": 9.6815, "type": "NODE", "capacity": 0},
    {"id": 40, "name": "Pignone", "latitude": 44.1779, "longitude": 9.6708, "type": "NODE", "capacity": 0},
    {"id": 41, "name": "Brugnato", "latitude": 44.2029, "longitude": 9.7032, "type": "NODE", "capacity": 0},
    {"id": 42, "name": "Lavagna", "latitude": 44.3159, "longitude": 9.3423, "type": "NODE", "capacity": 0},
    {"id": 43, "name": "Cogoleto", "latitude": 44.3979, "longitude": 8.6507, "type": "NODE", "capacity": 0},
    {"id": 44, "name": "Andora", "latitude": 43.9531, "longitude": 8.1409, "type": "NODE", "capacity": 0},
    {"id": 45, "name": "Voltri", "latitude": 44.4204, "longitude": 8.7616, "type": "NODE", "capacity": 0},
    {"id": 46, "name": "Pegli", "latitude": 44.4212, "longitude": 8.8055, "type": "NODE", "capacity": 0},
    {"id": 47, "name": "Quarto dei Mille", "latitude": 44.4024, "longitude": 8.9716, "type": "NODE", "capacity": 0},
    {"id": 48, "name": "Marina di Andora", "latitude": 43.9352, "longitude": 8.1504, "type": "NODE", "capacity": 0},
    {"id": 49, "name": "Pietra Ligure", "latitude": 44.1482, "longitude": 8.2786, "type": "NODE", "capacity": 0},
    {"id": 50, "name": "Albisola Superiore", "latitude": 44.3337, "longitude": 8.5155, "type": "NODE", "capacity": 0},
    {"id": 51, "name": "Milan", "latitude": 45.4642, "longitude": 9.1900, "type": "NODE", "capacity": 0},
    {"id": 52, "name": "Bergamo", "latitude": 45.6983, "longitude": 9.6773, "type": "NODE", "capacity": 0},
    {"id": 53, "name": "Brescia", "latitude": 45.5416, "longitude": 10.2118, "type": "NODE", "capacity": 0},
    {"id": 54, "name": "Monza", "latitude": 45.5845, "longitude": 9.2744, "type": "NODE", "capacity": 0},
    {"id": 55, "name": "Como", "latitude": 45.8090, "longitude": 9.0852, "type": "NODE", "capacity": 0},
    {"id": 56, "name": "Lecco", "latitude": 45.8566, "longitude": 9.3977, "type": "NODE", "capacity": 0},
    {"id": 57, "name": "Varese", "latitude": 45.8206, "longitude": 8.8250, "type": "NODE", "capacity": 0},
    {"id": 58, "name": "Cremona", "latitude": 45.1332, "longitude": 10.0227, "type": "NODE", "capacity": 0},
    {"id": 59, "name": "Pavia", "latitude": 45.1847, "longitude": 9.1582, "type": "NODE", "capacity": 0},
    {"id": 60, "name": "Mantua", "latitude": 45.1576, "longitude": 10.7914, "type": "NODE", "capacity": 0},
    {"id": 61, "name": "Sondrio", "latitude": 46.1699, "longitude": 9.8733, "type": "NODE", "capacity": 0},
    {"id": 62, "name": "Lodi", "latitude": 45.3154, "longitude": 9.5033, "type": "NODE", "capacity": 0},
    {"id": 63, "name": "Cinisello Balsamo", "latitude": 45.5614, "longitude": 9.2243, "type": "NODE", "capacity": 0},
    {"id": 64, "name": "Sesto San Giovanni", "latitude": 45.5343, "longitude": 9.2337, "type": "NODE", "capacity": 0},
    {"id": 65, "name": "Rho", "latitude": 45.5323, "longitude": 9.0373, "type": "NODE", "capacity": 0},
    {"id": 66, "name": "Legnano", "latitude": 45.5933, "longitude": 8.9173, "type": "NODE", "capacity": 0},
    {"id": 67, "name": "Gallarate", "latitude": 45.6604, "longitude": 8.7937, "type": "NODE", "capacity": 0},
    {"id": 68, "name": "Busto Arsizio", "latitude": 45.6117, "longitude": 8.8512, "type": "NODE", "capacity": 0},
    {"id": 69, "name": "Seregno", "latitude": 45.6580, "longitude": 9.2058, "type": "NODE", "capacity": 0},
    {"id": 70, "name": "Lissone", "latitude": 45.6128, "longitude": 9.2392, "type": "NODE", "capacity": 0},
    {"id": 71, "name": "Desio", "latitude": 45.6156, "longitude": 9.2078, "type": "NODE", "capacity": 0},
    {"id": 72, "name": "Brugherio", "latitude": 45.5522, "longitude": 9.3043, "type": "NODE", "capacity": 0},
    {"id": 73, "name": "Cernusco sul Naviglio", "latitude": 45.5219, "longitude": 9.3377, "type": "NODE", "capacity": 0},
    {"id": 74, "name": "Paderno Dugnano", "latitude": 45.5744, "longitude": 9.1642, "type": "NODE", "capacity": 0},
    {"id": 75, "name": "Cologno Monzese", "latitude": 45.5262, "longitude": 9.2737, "type": "NODE", "capacity": 0},
    {"id": 76, "name": "Corsico", "latitude": 45.4341, "longitude": 9.1184, "type": "NODE", "capacity": 0},
    {"id": 77, "name": "Rozzano", "latitude": 45.3849, "longitude": 9.1587, "type": "NODE", "capacity": 0},
    {"id": 78, "name": "Abbiategrasso", "latitude": 45.4023, "longitude": 8.9204, "type": "NODE", "capacity": 0},
    {"id": 79, "name": "Vigevano", "latitude": 45.3186, "longitude": 8.8584, "type": "NODE", "capacity": 0},
    {"id": 80, "name": "Gorgonzola", "latitude": 45.5324, "longitude": 9.4069, "type": "NODE", "capacity": 0},
    {"id": 81, "name": "Treviglio", "latitude": 45.5186, "longitude": 9.5918, "type": "NODE", "capacity": 0},
    {"id": 82, "name": "Crema", "latitude": 45.3641, "longitude": 9.6832, "type": "NODE", "capacity": 0},
    {"id": 83, "name": "Chiari", "latitude": 45.5353, "longitude": 9.9274, "type": "NODE", "capacity": 0},
    {"id": 84, "name": "Lonato del Garda", "latitude": 45.4611, "longitude": 10.4787, "type": "NODE", "capacity": 0},
    {"id": 85, "name": "Ghedi", "latitude": 45.4026, "longitude": 10.2773, "type": "NODE", "capacity": 0},
    {"id": 86, "name": "Montichiari", "latitude": 45.4147, "longitude": 10.3874, "type": "NODE", "capacity": 0},
    {"id": 87, "name": "Desenzano del Garda", "latitude": 45.4720, "longitude": 10.5346, "type": "NODE", "capacity": 0},
    {"id": 88, "name": "Sirmione", "latitude": 45.4831, "longitude": 10.6082, "type": "NODE", "capacity": 0},
    {"id": 89, "name": "Limone sul Garda", "latitude": 45.8163, "longitude": 10.7912, "type": "NODE", "capacity": 0},
    {"id": 90, "name": "Gardone Riviera", "latitude": 45.6223, "longitude": 10.5564, "type": "NODE", "capacity": 0},
    {"id": 91, "name": "Salò", "latitude": 45.6098, "longitude": 10.5299, "type": "NODE", "capacity": 0},
    {"id": 92, "name": "Ponte di Legno", "latitude": 46.2569, "longitude": 10.5097, "type": "NODE", "capacity": 0},
    {"id": 93, "name": "Iseo", "latitude": 45.6613, "longitude": 10.0504, "type": "NODE", "capacity": 0},
    {"id": 94, "name": "Lovere", "latitude": 45.8108, "longitude": 10.0798, "type": "NODE", "capacity": 0},
    {"id": 95, "name": "Pisogne", "latitude": 45.8032, "longitude": 10.1062, "type": "NODE", "capacity": 0},
    {"id": 96, "name": "Erbusco", "latitude": 45.6092, "longitude": 10.0137, "type": "NODE", "capacity": 0},
    {"id": 97, "name": "Castiglione delle Stiviere", "latitude": 45.3959, "longitude": 10.4951, "type": "NODE", "capacity": 0},
    {"id": 98, "name": "Casalmaggiore", "latitude": 44.9815, "longitude": 10.4197, "type": "NODE", "capacity": 0},
    {"id": 99, "name": "Darfo Boario Terme", "latitude": 45.8893, "longitude": 10.2174, "type": "NODE", "capacity": 0},
    {"id": 100, "name": "Orzinuovi", "latitude": 45.4021, "longitude": 9.9277, "type": "NODE", "capacity": 0}
  ]
def random_time_window():
    # Random start time
    start_hour = random.randint(5, 14)
    start_time = datetime(2024, 1, 1, start_hour, 0)

    # Random end time (must be after start time)
    end_hour = start_hour + random.randint(4, 8)  # End hour is at least 1 hour after start
    end_time = datetime(2024, 1, 1, end_hour, 0)

    # Format times as strings
    start_time_str = start_time.strftime("%H:%M")
    end_time_str = end_time.strftime("%H:%M")
    return f"{start_time_str}-{end_time_str}"

for location in locations:
    location['time']=random_time_window()

df = pd.DataFrame(locations)

# Save to Excel
file_path = "locations.xlsx"
df.to_excel(file_path, index=False)

