import os
from flask import Flask, jsonify

app = Flask(__name__)

USER_NAME = os.getenv("USER_NAME", "Guest")
INVENTORY_PATH = "/data/inventory.txt"

RECIPES = [
    {"name": "Cheese omelette", "ingredients": ["eggs", "cheese"]},
    {"name": "Pasta with tomato sauce", "ingredients": ["pasta", "tomatoes"]},
    {"name": "Pancakes", "ingredients": ["milk", "eggs", "flour"]},
    {"name": "Tomato salad", "ingredients": ["tomatoes", "cucumber", "onion"]},
    {"name": "Grilled cheese", "ingredients": ["bread", "cheese", "butter"]},
    {
        "name": "Vegetable stir-fry",
        "ingredients": ["broccoli", "carrots", "bell peppers", "soy sauce"],
    },
    {"name": "Fruit smoothie", "ingredients": ["banana", "berries", "yogurt", "honey"]},
    {
        "name": "Chicken salad",
        "ingredients": ["chicken", "lettuce", "tomatoes", "cucumber", "dressing"],
    },
]


def read_inventory():
    try:
        with open(INVENTORY_PATH, "r") as file:
            items = [line.strip().lower() for line in file.readlines() if line.strip()]
        return items
    except FileNotFoundError:
        return []


def suggest_recipe(inventory):
    available_ingredients = set(inventory)

    for recipe in RECIPES:
        required_ingredients = set(recipe["ingredients"])

        if required_ingredients.issubset(available_ingredients):
            return recipe["name"]

    if len(inventory) > 0:
        return "No exact recipe found, but you have: " + ", ".join(inventory)

    return "No ingredients found. Please update inventory.txt."


@app.route("/api")
def api():
    inventory = read_inventory()
    recipe = suggest_recipe(inventory)

    return jsonify(
        {
            "message": f"Hello {USER_NAME}!",
            "inventory": inventory,
            "suggested_recipe": recipe,
        }
    )


@app.route("/")
def home():
    return "Recipe app is running. Visit /api for recipe suggestions."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
