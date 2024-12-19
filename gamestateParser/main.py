# main.py

from lexer import Lexer
from parser import Parser

def parse_gamestate(file_path):
    with open(file_path, 'r', encoding='cp1252', errors='ignore') as file:
        content = file.read()

    lexer = Lexer(content)
    parser = Parser(lexer)
    ast = parser.parse()
    return ast

def extract_country_data(ast, country_tag):
    countries = ast.get('country')
    if not countries:
        print("No countries found in the data.")
        return None

    country_data = countries.get(country_tag)
    if not country_data:
        print(f"Country {country_tag} not found.")
        return None

    return country_data

def extract_all_countries(ast):
    countries = ast.get('country')
    if not countries:
        print("No countries found.")
        return None

    country_data = {}
    for tag, data in countries.items():
        country_info = {
            'treasury': data.get('treasury'),
            'manpower': data.get('manpower'),
            'stability': data.get('stability'),
            
        }
        country_data[tag] = country_info
    return country_data

if __name__ == '__main__':
    file_path = 'gamestate'  
    country_tag = 'FRA'  

    print("Parsing gamestate file...")
    ast = parse_gamestate(file_path)

    # Extract data for a specific country
    print(f"\nExtracting data for country '{country_tag}'...")
    country_data = extract_country_data(ast, country_tag)
    if country_data:
        treasury = country_data.get('treasury')
        manpower = country_data.get('manpower')
        stability = country_data.get('stability')
        print(f"Treasury: {treasury}")
        print(f"Manpower: {manpower}")
        print(f"Stability: {stability}")
        

    # Extract data for all countries
    print("\nExtracting data for all countries...")
    all_countries = extract_all_countries(ast)
    if all_countries:
        for tag, info in all_countries.items():
            print(f"Country {tag}: {info}")
