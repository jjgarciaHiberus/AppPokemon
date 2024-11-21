import requests

# Función para obtener la información completa de un Pokémon en español
def obtener_informacion_pokemon(nombre):
    # Primero obtenemos la información de la especie del Pokémon
    url_especie = f"https://pokeapi.co/api/v2/pokemon-species/{nombre.lower()}"
    response_especie = requests.get(url_especie)

    if response_especie.status_code == 200:
        especie_data = response_especie.json()

        # Información básica
        nombre_pokemon = especie_data['name']
        id_pokemon = especie_data['id']
        
        # Obtener los nombres y descripciones en español
        descripcion = ""
        for lengua in especie_data['flavor_text_entries']:
            if lengua['language']['name'] == 'es':  # Verificamos si el texto está en español
                descripcion = lengua['flavor_text']
                break

        # Obtener información del Pokémon desde el endpoint pokemon
        url_pokemon = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
        response_pokemon = requests.get(url_pokemon)

        if response_pokemon.status_code == 200:
            pokemon_data = response_pokemon.json()
            
            # Tipos y habilidades
            tipos = [tipo['type']['name'] for tipo in pokemon_data['types']]
            habilidades = [habilidad['ability']['name'] for habilidad in pokemon_data['abilities']]
            
            # Estadísticas
            stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
            
            # Movimientos
            movimientos = [mov['move']['name'] for mov in pokemon_data['moves'][:10]]  # Los primeros 10 movimientos
            
            # Imágenes
            imagen_url = pokemon_data['sprites']['front_default']
            
            # Mostrar la información
            print(f"\nNombre: {nombre_pokemon.capitalize()}")
            print(f"ID: {id_pokemon}")
            print(f"Descripción: {descripcion}")
            print(f"Tipos: {', '.join(tipos)}")
            print(f"Habilidades: {', '.join(habilidades)}")
            
            print("\nEstadísticas:")
            for stat, value in stats.items():
                print(f"{stat.capitalize()}: {value}")
            
            print("\nPrimeros 10 Movimientos:")
            for movimiento in movimientos:
                print(f"- {movimiento}")
            
            print(f"\nImagen: {imagen_url}")

        else:
            print(f"No se encontró información del Pokémon '{nombre}'.")

    else:
        print(f"No se encontró información para el Pokémon '{nombre}'.")

# Ejemplo de uso de la función
nombre_pokemon = input("Ingresa el nombre de un Pokémon (por ejemplo, 'pikachu'): ")
obtener_informacion_pokemon(nombre_pokemon)
