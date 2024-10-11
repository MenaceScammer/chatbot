import streamlit as st
import openai
import pandas as pd

# Set OpenAI API key for GPT-based chatbot
openai.api_key = "..."  # Make sure to replace this with your actual key

# Placeholder dataset for demo purposes
meal_data = pd.DataFrame({
    "Meal": ["Grilled Chicken Salad", "Vegan Tofu Stir-fry", "Quinoa and Black Beans", "Oatmeal with Berries", "Whole Grain Pasta"],
    "Ingredients": ["Chicken, Lettuce, Olive Oil", "Tofu, Vegetables, Soy Sauce", "Quinoa, Black Beans, Corn", "Oats, Strawberries, Blueberries", "Pasta, Tomato Sauce, Spinach"],
    "Health_Benefits": ["Low calorie, High protein", "Vegan, High protein", "High fiber, Diabetic-friendly", "Rich in antioxidants, Diabetes-friendly", "High fiber, Good for heart health"],
    "Suitable_For": ["General", "Vegan", "Diabetic", "Diabetic", "Heart"]
})

# Define the Streamlit app
def main():
    st.title("AI-Powered Food Recommendation System for University Students")
    st.subheader("Personalized meal suggestions based on your dietary preferences and health conditions.")
    
    # Chatbot interaction
    with st.expander("Talk to the AI Chef!"):
        st.write("Ask me about meal ideas, or tell me ingredients you want to avoid.")
        user_input = st.text_input("Enter your message:")
        if user_input:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # or use "gpt-4" if you have access
                    messages=[{"role": "user", "content": user_input}],
                    max_tokens=150
                )
                st.write(f"AI Chef: {response['choices'][0]['message']['content']}")
            except Exception as e:
                st.write(f"An error occurred: {str(e)}")

    # User Preferences
    st.sidebar.header("Dietary Preferences")
    health_condition = st.sidebar.selectbox("Select your health condition", ("None", "Diabetes", "High Blood Pressure", "Allergies", "Vegan"))
    avoid_ingredients = st.sidebar.text_input("Enter ingredients to avoid (comma-separated):")
    avoid_list = avoid_ingredients.lower().split(",")

    # Filter meal recommendations based on preferences
    def recommend_meals(health_condition, avoid_list):
        filtered_meals = meal_data.copy()

        if health_condition != "None":
            filtered_meals = filtered_meals[filtered_meals["Suitable_For"].str.contains(health_condition, case=False, na=False)]

        if avoid_list:
            for ingredient in avoid_list:
                filtered_meals = filtered_meals[~filtered_meals["Ingredients"].str.contains(ingredient.strip(), case=False)]

        return filtered_meals

    # Display meal recommendations
    st.subheader("Recommended Meals")
    recommendations = recommend_meals(health_condition, avoid_list)
    
    if not recommendations.empty:
        for idx, meal in recommendations.iterrows():
            st.write(f"**{meal['Meal']}**")
            st.write(f"Ingredients: {meal['Ingredients']}")
            st.write(f"Health Benefits: {meal['Health_Benefits']}")
            st.write("---")
    else:
        st.write("No meals match your criteria.")

if __name__ == "__main__":
    main()
