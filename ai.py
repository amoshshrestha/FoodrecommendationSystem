import openai
import pandas as pd

# Set your OpenAI GPT-3 API key
openai.api_key = 'YOUR_API_KEY'

# Load the CSV file containing food names
csv_path = 'path/to/your/food.csv'
df = pd.read_csv(csv_path)

# Define a function to categorize foods using GPT-3
def categorize_food(description):
    prompt = f"Given the description of the food: '{description}', categorize it into breakfast, lunch, or dinner."
    
    # Make a request to the GPT-3 API
    response = openai.Completion.create(
        engine="text-davinci-003",  # You may need to adjust the engine based on availability and requirements
        prompt=prompt,
        max_tokens=50  # Adjust based on the desired response length
    )

    # Extract the generated category from the GPT-3 response
    generated_category = response['choices'][0]['text'].strip()
    return generated_category

# Apply the categorize_food function to each food name in the DataFrame
df['Predicted Category'] = df['name'].apply(categorize_food)

# Display the results
print(df[['name', 'Predicted Category']])
