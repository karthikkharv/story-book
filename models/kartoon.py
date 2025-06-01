import json
from cretepdf import create_pdf_from_images
from generate_panels import generate_panels
from stability_ai import text_to_image
from add_text import add_text_to_panel
from create_strip import create_strip

# ==========================================================================================

# SCENARIO = """
# Characters: Adrien is a guy with blond hair. Vincent is a guy with black hair.
# Adrien and Vincent work at the office and want to start a new product, and they create it in one night before presenting it to the board.
# """
# SCENARIO = """
# Characters: Peter is a tall guy with blond hair. Steven is a small guy with black hair.
# Peter and Steven walk together in new york when aliens attack the city. They are afraid and try to run for their lives. The army arrive and save them.
# they want to eat meal . once they get out of the car . they seen police men following them .
# safety made for they ."""

with open("story.txt", 'r', encoding='utf-8') as file:
        SCENARIO = file.read()
# with open("story.txt",'w')as f:
#   pass
# print(SCENARIO)

STYLE = "american comic, colored"

# ==========================================================================================

print(f"Generate panels with style '{STYLE}' for this scenario: \n {SCENARIO}")

panels = generate_panels(SCENARIO)
import os

path = "\output\\"
for i in os.listdir(path):
   if(i.endswith(".png")):
      os.remove(path+i)


with open('output/panels.json', 'w') as outfile:
  json.dump(panels, outfile)

# with open('output/panels.json') as json_file:
#   panels = json.load(json_file)

panel_images = []
i=0
for panel in panels:
  # print(panel)
  i+1
  panel_prompt = panel["description"] + ", cartoon box, " + STYLE
  print(f"Generate panel {panel['number']} with prompt: {panel_prompt}")
  # print(panel["description"])
  panel_image = text_to_image(panel_prompt)
  try:
    panel_image_with_text = add_text_to_panel(panel["text"], panel_image)
  except Exception as e:
    panel_image_with_text = add_text_to_panel(panel["description"], panel_image)
  panel_image_with_text.save(f"output/panel-{panel['number']}.png")
  panel_images.append(panel_image_with_text)
  # if(i%6==0):
  #   create_strip(panel_images).save(f"output/strip{i}.png")
image_dir = "output\\"

# Generate the PDF
output_path = "output2.pdf"
create_pdf_from_images(image_dir,output_path)