# RecipeMnger
a command-line application for managing recipes, users can add, edit, delete, and search for recipes, storing them in a JSON


# Recipe Manager CLI

A command-line application for managing your recipe collection with support for adding, editing, deleting, and searching recipes.

## Features

- Store recipes in JSON format with detailed information
- Add new recipes with ingredients, instructions, and metadata
- List all recipes in your collection
- View detailed information for specific recipes
- Edit existing recipes
- Delete unwanted recipes
- Search through your recipe collection by name, ingredients, or tags

## Requirements

- Python 3.6 or higher

## Installation

1. Clone this repository or download the `recipe_manager.py` file
2. No additional dependencies are required as the application uses only Python standard libraries

## Usage

### Adding a Recipe

```bash
python recipe_manager.py add --name "Recipe Name" --ingredients "Ingredient 1" "Ingredient 2" --instructions "Step 1" "Step 2" --prep-time 10 --cook-time 20 --servings 4 --tags "tag1" "tag2"
```


### Listing All Recipes

To view all recipes with full details:
```bash
python recipe_manager.py list
```

For a compact list showing only IDs and names:
```bash
python recipe_manager.py list --compact
```

### Viewing a Specific Recipe

```bash
python recipe_manager.py view ID
```


### Editing a Recipe

```bash
python recipe_manager.py edit ID --field FIELD_NAME --value NEW_VALUE
```

Fields that can be edited:
- name
- ingredients
- instructions
- prep_time
- cook_time
- servings
- tags



### Deleting a Recipe

```bash
python recipe_manager.py delete ID
```


### Searching for Recipes

Search by name, ingredients, or tags:
```bash
python recipe_manager.py search QUERY
```


## Data Storage

Recipes are stored in a file named `recipes.json` in the same directory as the script.



## Contributing

Feel free to fork the repository.

## Future Enhancements

Possible features for future implementation:
- Recipe categories/collections
- Scaling recipes up or down based on desired servings
- Web interface
