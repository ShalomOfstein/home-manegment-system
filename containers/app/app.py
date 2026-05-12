import os
from flask import Flask, jsonify

app = Flask(__name__)

USER_NAME = os.getenv("USER_NAME", "Guest")
INVENTORY_PATH = "/data/inventory.txt"


def read_inventory():
    try:
        with open(INVENTORY_PATH, "r") as file:
            items = [line.strip().lower() for line in file.readlines() if line.strip()]
        return items
    except FileNotFoundError:
        return []


def suggest_recipe(items):
    items_set = set(items)

    if {"eggs", "cheese"}.issubset(items_set):
        return "Omelette with cheese"

    if {"pasta", "tomatoes"}.issubset(items_set):
        return "Pasta with tomato sauce"

    if {"milk", "eggs"}.issubset(items_set):
        return "Pancakes"

    if items:
        return f"Simple meal using: {', '.join(items[:3])}"

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
