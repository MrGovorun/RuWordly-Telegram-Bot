from PIL import Image, ImageDraw, ImageFont


def text2pic(image, position, letter, code):
    fnt = ImageFont.truetype('UbuntuMono-Regular.ttf', 120)
    fill_color = ['#414042', 'white','#FFD600'][int(code)]
    text_color = ['white', 'black','black'][int(code)]
    x0 = 100*position + 10*position+130
    y0 = 70
    x1 = x0 + 100
    y1 = y0 + 140
    image.rounded_rectangle([x0, y0, x1, y1], radius = 10, width = 3, fill = fill_color)
    image.text((x0+20, y0), letter, font = fnt, fill=text_color)
    return image

def create_image(name, word, code):
    img = Image.new('RGB', (800, 280), color = '#1A2026')
    d = ImageDraw.Draw(img)
    for pos, (letter, code_num) in enumerate(zip(word,code)):
        d = text2pic(d, pos, letter, code_num)
    img.save(f'images/{name}.png')


create_image(1,'океан','10021')
