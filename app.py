import streamlit as st
import pandas as pd
import plotly.express as px
from crewai import Agent, Task, Crew
from langchain.tools import Tool
from typing import Dict, List
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


# Function to read CSV files
def read_csv(file_path):
    return pd.read_csv(file_path)


# Function to write CSV files
def write_file(data, file_path):
    pd.DataFrame(data).to_csv(file_path, index=False)


# Load data
inventory_df = read_csv("inventory.csv")
recipes_df = read_csv("recipes.csv")


# CrewAI Tool for querying recipes
class RecipeQueryTool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)  # Use ConfigDict here
    inventory_df: pd.DataFrame = Field(default_factory=pd.DataFrame)
    recipes_df: pd.DataFrame = Field(default_factory=pd.DataFrame)

    def run(self, ingredients: str, servings: int, prompt: str) -> List[Dict]:
        available_ingredients = set(self.inventory_df["name"].str.lower())

        if not ingredients:
            # Sort inventory by expiration date and quantity
            sorted_inventory = self.inventory_df.sort_values(
                ["expiration_date", "quantity"], ascending=[True, False]
            )
            ingredients = ",".join(sorted_inventory["name"].head(5).tolist())

        requested_ingredients = set(ingredients.lower().split(","))

        matching_recipes = []
        for _, recipe in self.recipes_df.iterrows():
            recipe_ingredients = set(
                ingredient.lower().strip()
                for ingredient in recipe["ingredients"].split(",")
            )
            if recipe_ingredients.issubset(
                available_ingredients
            ) and recipe_ingredients.intersection(requested_ingredients):
                matching_recipes.append(
                    {
                        "name": recipe["name"],
                        "ingredients": recipe["ingredients"],
                        "instructions": recipe["instructions"],
                        "servings": recipe["servings"],
                    }
                )

        return matching_recipes[: min(10, len(matching_recipes))]


# Create RecipeQueryTool instance
recipe_tool = RecipeQueryTool(inventory_df=inventory_df, recipes_df=recipes_df)

# Create Tool for CrewAI
recipe_query_tool = Tool(
    name="Recipe Query Tool",
    func=recipe_tool.run,
    description="A tool for querying recipes based on available ingredients, servings, and prompt",
)

# CrewAI Agent for recipe suggestions
recipe_agent = Agent(
    role="Recipe Suggester",
    goal="Suggest recipes based on available ingredients and user prompt",
    backstory="You are an expert chef who can suggest recipes based on available ingredients and user preferences.",
    tools=[recipe_query_tool],
    llm="ollama/llama3.1:8b",
)


# Function to update inventory
def update_inventory(recipe):
    global inventory_df
    recipe_ingredients = [
        ing.strip().lower() for ing in recipe["ingredients"].split(",")
    ]
    for ingredient in recipe_ingredients:
        inventory_item = inventory_df[inventory_df["name"].str.lower() == ingredient]
        if not inventory_item.empty:
            inventory_df.loc[
                inventory_item.index, "quantity"
            ] -= 1  # Decrease quantity by 1 (simplified)
    write_file(inventory_df, "inventory.csv")


# Set page config
st.set_page_config(page_title="Restaurant Inventory Management", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Inventory", "Recipe Suggestions", "Analytics"])

# Main content
st.title("Restaurant Inventory Management System")

if page == "Inventory":
    st.header("Inventory Management")
    st.dataframe(inventory_df)

    # Add new item form
    st.subheader("Add New Item")
    new_item = {}
    new_item["name"] = st.text_input("Item Name")
    new_item["quantity"] = st.number_input("Quantity", min_value=0.0, step=0.1)
    new_item["unit"] = st.selectbox("Unit", ["kg", "L", "pcs"])
    new_item["expiration_date"] = st.date_input("Expiration Date")
    new_item["category"] = st.text_input("Category")

    if st.button("Add Item"):
        new_item["ingredient_id"] = inventory_df["ingredient_id"].max() + 1
        inventory_df = pd.concat(
            [inventory_df, pd.DataFrame([new_item])], ignore_index=True
        )
        write_file(inventory_df, "inventory.csv")
        st.success("Item added successfully!")

elif page == "Recipe Suggestions":
    st.header("Recipe Suggestions")

    # Create a multiselect for ingredients from inventory
    available_ingredients = inventory_df["name"].tolist()
    selected_ingredients = st.multiselect(
        "Select ingredients (or leave empty to use oldest and most available):",
        options=available_ingredients,
    )

    if not selected_ingredients:
        st.info(
            "No ingredients selected. The system will use the oldest and most available ingredients."
        )

    ingredients = ",".join(selected_ingredients) if selected_ingredients else ""

    servings = st.number_input(
        "Number of servings:", min_value=1, max_value=10, value=4
    )
    prompt = st.text_input("Any specific preferences or dietary requirements?")

    if st.button("Get Recipe Suggestions"):
        task = Task(
            description=f"Suggest recipes using these ingredients: {ingredients}, for {servings} servings. Consider the prompt: {prompt}",
            expected_output="A list of recipe suggestions with their details.",
            agent=recipe_agent,
        )
        crew = Crew(agents=[recipe_agent], tasks=[task])
        result = crew.kickoff()

        st.write("AI Suggestions:", result)

        recipes = recipe_tool.run(ingredients, servings, prompt)

        if recipes:
            for recipe in recipes:
                st.subheader(recipe["name"])
                st.write(f"Ingredients: {recipe['ingredients']}")
                st.write(f"Instructions: {recipe['instructions']}")
                st.write(f"Servings: {recipe['servings']}")
                if st.button(f"Select {recipe['name']}"):
                    update_inventory(recipe)
                    st.success(f"Inventory updated based on {recipe['name']}")
        else:
            st.write("No matching recipes found.")

elif page == "Analytics":
    st.header("Inventory Analytics")

    # Simple bar chart of inventory quantities
    fig = px.bar(inventory_df, x="name", y="quantity", title="Current Inventory Levels")
    st.plotly_chart(fig)

    # Pie chart of inventory categories
    category_counts = inventory_df["category"].value_counts()
    fig2 = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="Inventory by Category",
    )
    st.plotly_chart(fig2)

# Footer
st.sidebar.markdown("---")
st.sidebar.text("Restaurant Inventory Management v0.1")
