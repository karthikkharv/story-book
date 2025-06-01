import io
import os
import warnings
import random
import requests
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import time
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# seed = random.randint(0, 1000000000)

def text_to_image(prompt):
    # Set up our initial generation parameters.
    with open("seed.txt",'r') as f:
        st = f.read()
    try:
        seed = int(st)
    except Exception as e:
        seed = random.randint(0, 1000000000)
        with open("seed.txt",'w')as f:
            f.write(str(seed))
    # def query(params):
    params={
        "inputs":prompt,
        "seed":seed
    }
    # prompt="rocket ship launching from forest with flower garden under a blue sky, masterful, ghibli",
    max_retries=3
    for attempt in range(max_retries):
        try:
            url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
            headers = {API_KEY_WITH_HEADER}  # Replace with your actual API key
            response = requests.post(url, headers=headers, json=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            answers = response.content
            img = Image.open(io.BytesIO(answers))
            return img 
        except requests.exceptions.RequestException as e:
                url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
                headers = {API_KEY_WITH_HEADER}  # Replace with your actual API key
                response = requests.post(url, headers=headers, json=params)
                response.raise_for_status()  # Raise an exception for HTTP errors
                answers = response.content
                img = Image.open(io.BytesIO(answers))
                return img
               

def get_image(prompt, max_retries=3, backoff_factor=1.0):
    params = {"inputs": prompt}
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}: Querying the image generation service...")
            return query(params)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            if attempt < max_retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                print(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print("Max retries reached. Exiting.")
                raise