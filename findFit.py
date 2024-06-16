# Works if you give it a description instead of a title
# Easily editable to do anything with any CSV
import os
import pandas as pd
import sys
from openai import OpenAI
from tqdm import tqdm
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Initialize the OpenAI client with the API key from the environment variable
client = OpenAI(
    api_key=os.getenv('OPENAI_PROJ_KEY')
)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def evaluate_job_fit(job_title: str) -> float:
    messages = [
        {"role": "system", "content": "You will be shown a cell's value corresponding to a job title or description. Evaluate if it is a potential fit for someone who has a ___ degree from ___ in ____, experience in ______. The jobseeker has the following licenses: ___. She needs to make at least ___. Return a probability between 0 and 1 indicating the fit."},
        {"role": "user", "content": f"Job Title: {job_title}"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=messages,
        max_tokens=10,
        temperature=0
    )
    
    output = response.choices[0].message.content.strip()
    try:
        probability = float(output)
    except ValueError:
        probability = 0.0
    
    return probability

def process_csv(input_csv: str, output_csv: str, column_name: str):
    df = pd.read_csv(input_csv)
    
    if 'Fit Probability for Alexandra' not in df.columns:
        df['Fit Probability for Alexandra'] = 0.0

    start_index = df['Fit Probability for Alexandra'].eq(0.0).idxmax()

    with tqdm(total=len(df), initial=start_index, desc="Processing") as pbar:
        for index in range(start_index, len(df)):
            job_title = df.at[index, column_name]
            df.at[index, 'Fit Probability for Alexandra'] = evaluate_job_fit(job_title)
            pbar.update(1)
            df.to_csv("temp_results.csv", index=False)

    df.to_csv(output_csv, index=False)
    if os.path.exists("temp_results.csv"):
        os.remove("temp_results.csv")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python findFit.py <input_csv_path> <column_name>")
    else:
        input_csv_path = sys.argv[1]
        column_name = sys.argv[2]
        output_csv_path = 'job_titles_with_fit.csv'
        process_csv(input_csv_path, output_csv_path, column_name)
