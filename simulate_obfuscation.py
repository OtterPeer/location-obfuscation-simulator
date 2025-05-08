import numpy as np
import matplotlib.pyplot as plt

def seed_random(seed):
    x = np.sin(seed) * 10000
    def next_random():
        nonlocal x, seed
        next_seed = (x * seed) % 1000000
        seed = next_seed
        return next_seed / 1000000
    return next_random

def generate_private_key():
    return np.random.randint(0, 10**18)

def private_key_to_offset(private_key, max_offset_km):
    seed = private_key % 1000000
    random = seed_random(seed)
    random_offset_distance = int(random() * (max_offset_km - 1)) + 1
    km_to_deg = 1 / 111.32
    x_offset = (random() * 2 - 1) * max_offset_km * random_offset_distance * km_to_deg
    y_offset = (random() * 2 - 1) * max_offset_km * random_offset_distance * km_to_deg
    return {"xOffset": x_offset, "yOffset": y_offset}

def random_point_in_square(current_lon, current_lat, side_km):
    km_to_deg = 1 / 111.32
    x_offset = (np.random.random() * 2 - 1) * side_km * km_to_deg
    y_offset = (np.random.random() * 2 - 1) * side_km * km_to_deg
    return {"longitude": current_lon + x_offset, "latitude": current_lat + y_offset}

def dummy_location(true_lon, true_lat, private_key, initial_side_km):
    offset = private_key_to_offset(private_key, initial_side_km)
    current_lon = true_lon + offset["xOffset"]
    current_lat = true_lat + offset["yOffset"]
    point = random_point_in_square(current_lon, current_lat, initial_side_km)
    return point

true_lat, true_lon = 54.352448, 18.647599
n_simulations = 10000
initial_side_km = 2
private_key = generate_private_key()
obfuscated_lons = []
obfuscated_lats = []

for _ in range(n_simulations):
    result = dummy_location(true_lon, true_lat, private_key, initial_side_km)
    obfuscated_lons.append(result["longitude"])
    obfuscated_lats.append(result["latitude"])

km_to_deg = 111.32
distances = [np.sqrt(((lon - true_lon) * km_to_deg * np.cos(np.radians(true_lat)))**2 + ((lat - true_lat) * km_to_deg)**2) for lon, lat in zip(obfuscated_lons, obfuscated_lats)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.scatter(obfuscated_lons, obfuscated_lats, c='blue', alpha=0.5, label='Obfuscated Locations', s=10)
ax1.scatter([true_lon], [true_lat], c='red', marker='x', s=100, label='True Location')
ax1.set_title(f'Obfuscated Locations ({n_simulations} Simulations)')
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
ax1.legend()
ax1.grid(True)
ax1.axis('equal')

ax2.hist(distances, bins=50, color='blue', alpha=0.7, label='Distance Distribution')
ax2.set_title('Distance from True Location')
ax2.set_xlabel('Distance (km)')
ax2.set_ylabel('Frequency')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig(f'simulation{private_key}.png')