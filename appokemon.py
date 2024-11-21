import requests

# Complete dictionary of type effectiveness
type_effectiveness = {
    "normal": {"strong": [], "weak": ["rock", "steel"], "no_effect": ["ghost"]},
    "fire": {"strong": ["grass", "ice", "bug", "steel"], "weak": ["water", "rock", "dragon"], "no_effect": []},
    "water": {"strong": ["fire", "rock", "ground"], "weak": ["grass", "electric"], "no_effect": []},
    "electric": {"strong": ["water", "flying"], "weak": ["grass", "dragon"], "no_effect": ["ground"]},
    "grass": {"strong": ["water", "rock", "ground"], "weak": ["fire", "flying", "bug", "dragon", "steel"], "no_effect": []},
    "ice": {"strong": ["dragon", "grass", "flying", "ground"], "weak": ["fire", "steel", "water", "ice"], "no_effect": []},
    "fighting": {"strong": ["normal", "ice", "rock", "dark", "steel"], "weak": ["flying", "psychic", "fairy"], "no_effect": ["ghost"]},
    "poison": {"strong": ["grass", "fairy"], "weak": ["poison", "ground", "rock", "ghost"], "no_effect": ["steel"]},
    "ground": {"strong": ["fire", "electric", "poison", "rock", "steel"], "weak": ["grass", "bug"], "no_effect": ["flying"]},
    "flying": {"strong": ["fighting", "bug", "grass"], "weak": ["rock", "electric", "ice"], "no_effect": []},
    "psychic": {"strong": ["fighting", "poison"], "weak": ["psychic", "steel"], "no_effect": ["dark"]},
    "bug": {"strong": ["grass", "psychic", "dark"], "weak": ["fire", "fighting", "flying", "ghost", "steel", "fairy"], "no_effect": []},
    "rock": {"strong": ["fire", "ice", "flying", "bug"], "weak": ["fighting", "ground", "steel"], "no_effect": []},
    "ghost": {"strong": ["ghost", "psychic"], "weak": ["dark"], "no_effect": ["normal"]},
    "dragon": {"strong": ["dragon"], "weak": ["steel", "fairy"], "no_effect": []},
    "dark": {"strong": ["psychic", "ghost"], "weak": ["fighting", "bug", "fairy"], "no_effect": []},
    "steel": {"strong": ["ice", "rock", "fairy"], "weak": ["fire", "water", "electric", "steel"], "no_effect": []},
    "fairy": {"strong": ["fighting", "dragon", "dark"], "weak": ["poison", "steel"], "no_effect": []},
}

# Function to query Pokémon type effectiveness
def query_type(pokemon_type):
    pokemon_type = pokemon_type.lower()
    if pokemon_type in type_effectiveness:
        strong_against = ', '.join(type_effectiveness[pokemon_type]["strong"])
        weak_against = ', '.join(type_effectiveness[pokemon_type]["weak"])
        no_effect = ', '.join(type_effectiveness[pokemon_type]["no_effect"])
        print(f"🔹 Type {pokemon_type.capitalize()}:")
        print(f"   ✅ Strong against: {strong_against}")
        print(f"   ❌ Weak against: {weak_against}")
        print(f"   🚫 No effect on: {no_effect}")
    else:
        print(f"❌ Type '{pokemon_type}' not found.")

# Function to get complete information of a Pokémon in English
def get_pokemon_info(name):
    try:
        # Get Pokémon species information
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
        species_response = requests.get(species_url)

        if species_response.status_code != 200:
            print(f"❌ Could not find information for Pokémon '{name}'.")
            return

        species_data = species_response.json()

        # Basic information
        pokemon_name = species_data['name']
        pokemon_id = species_data['id']
        
        # Description in English
        description = ""
        for entry in species_data['flavor_text_entries']:
            if entry['language']['name'] == 'en':
                description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                break

        # Get Pokémon data from the Pokémon endpoint
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        pokemon_response = requests.get(pokemon_url)

        if pokemon_response.status_code != 200:
            print(f"❌ Could not find detailed information for Pokémon '{name}'.")
            return

        pokemon_data = pokemon_response.json()

        # Types and abilities
        types = [type_info['type']['name'] for type_info in pokemon_data['types']]
        abilities = [ability['ability']['name'] for ability in pokemon_data['abilities']]
        
        # Stats
        stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
        
        # Moves
        moves = [move['move']['name'] for move in pokemon_data['moves'][:10]]  # First 10 moves
        
        # Image
        image_url = pokemon_data['sprites']['front_default']
        
        # Display Pokémon information
        print(f"\n🔹 Name: {pokemon_name.capitalize()}")
        print(f"🔹 ID: {pokemon_id}")
        print(f"🔹 Description: {description}")
        print(f"🔹 Types: {', '.join(types).capitalize()}")
        print(f"🔹 Abilities: {', '.join(abilities).capitalize()}")
        
        print("\n📊 Stats:")
        for stat, value in stats.items():
            print(f"  - {stat.capitalize()}: {value}")
        
        print("\n🎯 First 10 Moves:")
        for move in moves:
            print(f"  - {move.capitalize()}")

        # Query the effectiveness of the Pokémon's types
        for pokemon_type in types:
            query_type(pokemon_type)

    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to the API: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# Example usage
pokemon_name = input("Enter the name of a Pokémon: ")
get_pokemon_info(pokemon_name)
