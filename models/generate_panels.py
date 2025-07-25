import os
import re
import google.generativeai as genai

# Configure the API key for the Generative AI service
genai.configure(api_key={API-key})

# Define the template for generating cartoon panels
template = """
You are a cartoon creator.

You will be given a short scenario, you must split it into 6 parts.
Each part will be a different cartoon panel.
For each cartoon panel, you will write a description of it with:
 - the characters in the panel, they must be described precisely each time
 - the background of the panel
The description should be only a word or group of words delimited by a comma, no sentence.
Always use the characters' descriptions instead of their names in the cartoon panel description.
You cannot use the same description twice.
You will also write the text of the panel.
The text should not be more than 2 small sentences.
Each sentence should start with the character's name.
Example input:
Characters: Adrien is a guy with blond hair wearing glasses. Vincent is a guy with black hair wearing a hat.
Adrien and vincent want to start a new product, and they create it in one night before presenting it to the board.

Example output:

# Panel 1
description: 2 guys, a blond hair guy wearing glasses, a dark hair guy wearing hat, sitting at the office, with computers
text:

Vincent: I think Generative AI are the future of the company.
Adrien: Let's create a new product with it.

# end

Short Scenario:
{scenario}

Split the scenario into 12 parts:
"
"""
# Function to generate panels using the generative AI model
def generate_panels(scenario):
    # Define the generative model
    model = genai.GenerativeModel('gemini-pro')

    # Format the prompt with the scenario
    formatted_prompt = template.format(scenario=scenario)

    # Generate the content using the model
    response = model.generate_content(formatted_prompt)

    # Extract the content from the response
    result = response.candidates[0].content.parts[0].text
    # print("result :",result)
    # candidates = response._result.candidates["candidates"]
    # print(candidates)
    # text_content = response.result['candidates'][0]['content']['parts'][0]['text']
    # print(result)
    # Extract panel information from the result
    return extract_panel_info(result)

# Function to extract panel information from the generated text
def extract_panel_info(text):
    panel_info_list = []
    panel_blocks = text.split('# Panel')
    print(panel_blocks)
    for block in panel_blocks:
        if block.strip():
            panel_info = {}

            # Extracting panel number
            panel_number = re.search(r'\d+', block)
            if panel_number is not None:
                panel_info['number'] = panel_number.group()

            # Extracting panel description
            panel_description = re.search(r'description: (.+)', block)
            if panel_description is not None:
                panel_info['description'] = panel_description.group(1).strip()

            # Extracting panel text
            panel_text = re.search(r'text:\n\n(.+?)\n', block, re.DOTALL)
            if panel_text is not None:
                panel_info['text'] = panel_text.group(1).strip()

            panel_info_list.append(panel_info)

    return panel_info_list