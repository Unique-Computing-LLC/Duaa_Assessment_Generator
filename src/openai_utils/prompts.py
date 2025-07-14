LECTURE_SLIDES_PROMPT = (
    "You are an expert educator. Given the following teacher guidelines, "
    "generate a JSON structure suitable for creating lecture slides. "
    "Since theese slides are for little kids of class KG. They should have related content, images, giff etc and less text and large words."
    "Teacher Guidelines:\n"
    "{teacher_guidelines}\n\n"
    "Return only the JSON."
)

COLOR_PALLETTE = """
Light Background: #FFF4ED
Primary Color: #6D3961
Secondary Color: #B3987F
Accent Colors: #FFB173, #896646
"""

AHMED_PROMPT = "A flat-style digital illustration of a young Muslim boy, aged 2.5 to 3 years, with no background, no outlines, and clean, soft color shading. He is wearing a bright long tunic and pants, with shoes. His skin tone is 'porcelain'. He wears a Muslim cap (taqiyah) on his head. The illustration should not have facial features and should follow an Islamic visual style suitable for educational content."

DUAA_PROMPT = "A flat-style digital illustration of a young Muslim girl, aged 2.5 to 3 years, with no background, no outlines, and clean, soft color shading. She is wearing a hijab and a dress, with pants and shoes. Her skin tone is 'porcelain'. The illustration should not have facial features and must follow an Islamic visual style suitable for educational content for children."

IMAGE_PROMPT = (
    "Create a flat-style digital illustration with bright colors and a cartoonish style suitable for young children. "
    "Main image description: {description}\n"
    "The illustration should have following hexa color #FFF4ED as the background, no outlines, flat style."
    "Do not include any text or names in the image. "
) 