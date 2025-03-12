import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any

class RecipeManager:
    """Recipe manager that handles saving, loading, and manipulating recipes."""
    
    def __init__(self, file_path: str = "recipes.json"):
        """Initialize with the path to the recipe file."""
        self.file_path = file_path
        self.recipes = self._load_recipes()
    
    def _load_recipes(self) -> List[Dict[str, Any]]:
        """Load recipes from the JSON file."""
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error reading {self.file_path}. Starting with empty recipe list.")
            return []
    
    def _save_recipes(self) -> None:
        """Save recipes to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(self.recipes, file, indent=2)
    
    def add_recipe(self, name: str, ingredients: List[str], instructions: List[str], 
                  prep_time: int, cook_time: int, servings: int, tags: List[str]) -> None:
        """Add a new recipe to the collection."""
        #check if recipe with this name already exists
        if any(recipe['name'].lower() == name.lower() for recipe in self.recipes):
            print(f"Recipe '{name}' already exists. Use edit command to modify it.")
            return
        
        recipe = {
            'id': len(self.recipes) + 1,
            'name': name,
            'ingredients': ingredients,
            'instructions': instructions,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'servings': servings,
            'tags': tags,
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.recipes.append(recipe)
        self._save_recipes()
        print(f"Recipe '{name}' added successfully!")
    
    def edit_recipe(self, recipe_id: int, field: str, value: Any) -> bool:
        """Edit a specific field of a recipe."""
        for recipe in self.recipes:
            if recipe['id'] == recipe_id:
                if field in recipe:
                    recipe[field] = value
                    self._save_recipes()
                    print(f"Updated {field} for recipe '{recipe['name']}'")
                    return True
                else:
                    print(f"Field '{field}' does not exist in recipe.")
                    return False
        
        print(f"Recipe with ID {recipe_id} not found.")
        return False
    
    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete a recipe by ID."""
        for i, recipe in enumerate(self.recipes):
            if recipe['id'] == recipe_id:
                deleted = self.recipes.pop(i)
                self._save_recipes()
                print(f"Recipe '{deleted['name']}' deleted successfully!")
                return True
        
        print(f"Recipe with ID {recipe_id} not found.")
        return False
    
    def search_recipes(self, query: str) -> List[Dict[str, Any]]:
        """Search for recipes by name, ingredients, or tags."""
        query = query.lower()
        results = []
        
        for recipe in self.recipes:
            #search in name
            if query in recipe['name'].lower():
                results.append(recipe)
                continue
            
            #search in ingredients
            if any(query in ingredient.lower() for ingredient in recipe['ingredients']):
                results.append(recipe)
                continue
            
            #search in tags
            if any(query in tag.lower() for tag in recipe['tags']):
                results.append(recipe)
                continue
        
        return results
    
    def list_recipes(self) -> List[Dict[str, Any]]:
        """List all recipes."""
        return self.recipes
    
    def get_recipe(self, recipe_id: int) -> Optional[Dict[str, Any]]:
        """Get a recipe by ID."""
        for recipe in self.recipes:
            if recipe['id'] == recipe_id:
                return recipe
        return None


def display_recipe(recipe: Dict[str, Any]) -> None:
    """Display a recipe in a readable format."""
    print("\n" + "=" * 50)
    print(f"Recipe #{recipe['id']}: {recipe['name']}")
    print("=" * 50)
    
    print(f"\nPrep Time: {recipe['prep_time']} minutes")
    print(f"Cook Time: {recipe['cook_time']} minutes")
    print(f"Servings: {recipe['servings']}")
    
    print("\nIngredients:")
    for i, ingredient in enumerate(recipe['ingredients'], 1):
        print(f"  {i}. {ingredient}")
    
    print("\nInstructions:")
    for i, instruction in enumerate(recipe['instructions'], 1):
        print(f"  {i}. {instruction}")
    
    if recipe['tags']:
        print(f"\nTags: {', '.join(recipe['tags'])}")
    
    print(f"\nAdded on: {recipe['date_added']}")
    print("=" * 50 + "\n")


def main():
    """Main function to handle command line arguments and control the program flow."""
    parser = argparse.ArgumentParser(description="Recipe Manager - Manage your recipes from the command line")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    #add
    add_parser = subparsers.add_parser("add", help="Add a new recipe")
    add_parser.add_argument("--name", required=True, help="Recipe name")
    add_parser.add_argument("--ingredients", required=True, nargs="+", help="List of ingredients")
    add_parser.add_argument("--instructions", required=True, nargs="+", help="List of instructions")
    add_parser.add_argument("--prep-time", type=int, required=True, help="Preparation time in minutes")
    add_parser.add_argument("--cook-time", type=int, required=True, help="Cooking time in minutes")
    add_parser.add_argument("--servings", type=int, required=True, help="Number of servings")
    add_parser.add_argument("--tags", nargs="*", default=[], help="Tags for categorizing the recipe")
    
    #list
    list_parser = subparsers.add_parser("list", help="List all recipes")
    list_parser.add_argument("--compact", action="store_true", help="Show compact list (IDs and names only)")
    
    #view
    view_parser = subparsers.add_parser("view", help="View a specific recipe")
    view_parser.add_argument("id", type=int, help="Recipe ID to view")
    
    #edit recipe command
    edit_parser = subparsers.add_parser("edit", help="Edit a recipe")
    edit_parser.add_argument("id", type=int, help="Recipe ID to edit")
    edit_parser.add_argument("--field", required=True, choices=["name", "ingredients", "instructions", 
                                                              "prep_time", "cook_time", "servings", "tags"],
                           help="Field to edit")
    edit_parser.add_argument("--value", required=True, nargs="+", help="New value for the field")
    
    #delete recipe command
    delete_parser = subparsers.add_parser("delete", help="Delete a recipe")
    delete_parser.add_argument("id", type=int, help="Recipe ID to delete")
    
    #search recipes command
    search_parser = subparsers.add_parser("search", help="Search for recipes")
    search_parser.add_argument("query", help="Search query")
    
    #parse arguments
    args = parser.parse_args()
    
    #initialize
    manager = RecipeManager()
    
    #process all commands
    if args.command == "add":
        manager.add_recipe(
            name=args.name,
            ingredients=args.ingredients,
            instructions=args.instructions,
            prep_time=args.prep_time,
            cook_time=args.cook_time,
            servings=args.servings,
            tags=args.tags
        )
    
    elif args.command == "list":
        recipes = manager.list_recipes()
        if not recipes:
            print("No recipes found.")
        elif args.compact:
            print("\nRecipes:")
            for recipe in recipes:
                print(f"#{recipe['id']}: {recipe['name']}")
        else:
            for recipe in recipes:
                display_recipe(recipe)
    
    elif args.command == "view":
        recipe = manager.get_recipe(args.id)
        if recipe:
            display_recipe(recipe)
        else:
            print(f"Recipe with ID {args.id} not found.")
    
    elif args.command == "edit":
        #convert value on field type
        value = args.value
        if args.field in ["name"]:
            value = " ".join(args.value)
        elif args.field in ["ingredients", "instructions", "tags"]:
            value = args.value
        elif args.field in ["prep_time", "cook_time", "servings"]:
            try:
                value = int(args.value[0])
            except ValueError:
                print(f"Error: {args.field} must be a number")
                return
        
        manager.edit_recipe(args.id, args.field, value)
    
    elif args.command == "delete":
        confirm = input(f"Are you sure you want to delete recipe #{args.id}? (y/n): ")
        if confirm.lower() == 'y':
            manager.delete_recipe(args.id)
    
    elif args.command == "search":
        results = manager.search_recipes(args.query)
        if results:
            print(f"Found {len(results)} matching recipes:")
            for recipe in results:
                display_recipe(recipe)
        else:
            print(f"No recipes found matching '{args.query}'")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
