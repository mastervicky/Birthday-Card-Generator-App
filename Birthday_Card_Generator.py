import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from datetime import date
import io

# function to create a growth graph based on the birth year
def create_growth_graph(birth_year):
    current_year = date.today().year
    year = list(range(birth_year, current_year +1))
    ages = [y - birth_year for y in year]

    fig, ax = plt.subplots(figsize = (4, 2))
    ax.plot(year, ages, marker='o', color='blue')
    ax.set_title('Growth Chart')
    ax.set_xlabel('Year')
    ax.set_ylabel('Age')
    ax.grid(True)

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    return Image.open(buf)

# funtion to add border + decorations to the card
def load_decor_image(filename, size=None):
    """ Helper to load and resize decoration images """
    img = Image.open(os.path.join("assets", filename)).convert("RGBA")
    if size:
        img = img.resize(size, Image.ANTIALIAS)
    return img

# function to create a birthday card
def create_card(name, birth_year, upload_photo=None):
    # Base canvas
    card = Image.new("RGBA", (800, 600), "lightyellow")
    draw = ImageDraw.Draw(card)
    # Font adjustment if needed
    try:
        font_title = ImageFont.truetype("arial.ttf", 60)
        font_msg = ImageFont.truetype("arial.ttf", 40)
    except:
        font_title = font_msg = None

    draw.text((50, 50), f"Happy Birthday {name}!", fill="darkred", font=font_title)
    draw.text((50, 120), "Wishing you many more years of joy, good health and success!", fill="black", font=font_msg)

    if upload_photo:
        photo = Image.open(upload_photo).resize((300, 300))
        card.paste(photo, (20, 150))

        chart = create_growth_graph(birth_year).resize((400, 200))
        card.paste(chart, (350, 150))

    # Golden border
    border_color = (212, 175, 55)  # RGB Gold color
    border_width = 20
    for i in range(border_width):
        draw.rectangle([i, i, 800 - i - 1, 600 - i - 1], outline=border_color)

    # Add decorative images
    background = load_decor_image("background.png", size=(100, 100))
    butterfly = load_decor_image("butterfly.png", size=(80, 80))
    balloons = load_decor_image("balloons.png", size=(120, 120))
    # Paste decorations
    card.paste(background, (50, 50), background)
    card.paste(butterfly, (600, 50), butterfly)
    card.paste(balloons, (700, 400), balloons)

    return card.convert("RGB")

# Streamlit Web UI
st.title("Birthday Card Generator")

name = st.text_input("Enter your name")
birth_year = st.number_input("Enter your year of birth", min_value=1900, max_value=date.today().year, value=2000)
photo = st.file_uploader("Upload your photo (JPEG or PNG)", type=["jpg", "jpeg", "png"])

if st.button("Generate Card"):
    if name and photo:
        card = create_card(name, birth_year, photo)
        st.image(card, caption="Your Birthday Card", use_column_width=True)

        buf = io.BytesIO()
        card.save(buf, format="PNG")
        st.download_button("Download Card", data=buf.getvalue(), file_name=f"{name}_birthday_card.png", mime="image/png")
    else:
        st.warning("Please enter your name and upload a photo.")