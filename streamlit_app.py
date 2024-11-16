import streamlit as st
import openai
import pandas as pd

# Set OpenAI API key for GPT-based chatbot
openai.api_key = "sk-SbeDydnmKdZqpfrDWFwkNVIoSlrP7jUVfpA1R2cU7KT3BlbkFJWD2uM1yfdhEi_oy23v9aIZSGKkD8u252ZjjI9XyFwA"  # Replace with your actual key

# Placeholder dataset for demo purposes, including image URLs
meal_data = pd.DataFrame({
    "Meal": ["Grilled Chicken Salad", "Vegan Tofu Stir-fry", "Quinoa and Black Beans", "Oatmeal with Berries", "Whole Grain Pasta"],
    "Ingredients": ["Chicken, Lettuce, Olive Oil", "Tofu, Vegetables, Soy Sauce", "Quinoa, Black Beans, Corn", "Oats, Strawberries, Blueberries", "Pasta, Tomato Sauce, Spinach"],
    "Health_Benefits": ["Low calorie, High protein", "Vegan, High protein", "High fiber, Diabetic-friendly", "Rich in antioxidants, Diabetes-friendly", "High fiber, Good for heart health"],
    "Suitable_For": ["General", "Vegan", "Diabetic", "Diabetic", "Heart"],
    "Image_URL": [
        "https://www.themediterraneandish.com/wp-content/uploads/2021/03/Greek-chicken-salad-recipe-6.jpg",
        "https://rainbowplantlife.com/wp-content/uploads/2023/01/tofu-stir-fry-cover-photo-1-of-1.jpg",
        "https://therecipewell.com/wp-content/uploads/2019/07/Quinoa-Black-Bean-Salad.jpg",
        "https://data.thefeedfeed.com/recommended/post_4491715.jpeg",
        "https://happyhealthymama.com/wp-content/uploads/2010/03/Penne-Pasta_-2.jpg"
    ]
})

# Define the Streamlit app
def main():
    # Add custom CSS for styling
    st.markdown("""
        <style>
            body {
                background-color: #f0f8ff;
                color: #333;
                font-family: 'Helvetica Neue', sans-serif;
            }
            h1 {
                color: white;
                font-size: 42px;
            }
            h2 {
                color: white;
                font-size: 18px;
            }
            .stTextInput>div>input {
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("MealFit")
    st.header("Personalized meal suggestions based on dietary preferences and health conditions for university students.")
    
    # Chatbot interaction
    with st.expander("Talk to the AI Chef!"):
        st.write("Ask me about meal ideas, or tell me ingredients you want to avoid.")
        user_input = st.text_input("Enter your message:")
        if user_input:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_input}],
                    max_tokens=150
                )
                st.write(f"**AI Chef:** {response['choices'][0]['message']['content']}")
            except Exception as e:
                st.write(f"An error occurred: {str(e)}")

    # User Preferences
    st.sidebar.header("Dietary Preferences")
    health_condition = st.sidebar.selectbox("Select your health condition", ("None", "Diabetes", "High Blood Pressure", "Allergies", "Vegan"))
    avoid_ingredients = st.sidebar.text_input("Enter ingredients to avoid (comma-separated):")
    avoid_list = avoid_ingredients.lower().split(",") if avoid_ingredients else []

    # Filter meal recommendations based on preferences
    def recommend_meals(health_condition, avoid_list):
        filtered_meals = meal_data.copy()

        # Filter meals based on health condition
        if health_condition != "None":
            filtered_meals = filtered_meals[filtered_meals["Suitable_For"].str.contains(health_condition, case=False, na=False)]

        # Filter out meals containing ingredients to avoid
        if avoid_list:
            for ingredient in avoid_list:
                filtered_meals = filtered_meals[~filtered_meals["Ingredients"].str.contains(ingredient.strip(), case=False)]

        return filtered_meals

    # Display meal recommendations
    st.subheader("Recommended Meals")
    recommendations = recommend_meals(health_condition, avoid_list)
    
    if not recommendations.empty:
        for idx, meal in recommendations.iterrows():
            with st.container():
                # Display the meal image
                st.image(meal['Image_URL'], caption=meal['Meal'], use_column_width=True)
                st.write(f"**Ingredients:** {meal['Ingredients']}")
                st.write(f"**Health Benefits:** {meal['Health_Benefits']}")
                st.write("---")
    else:
        st.write("No meals match your criteria.")

if __name__ == "__main__":
    main()
