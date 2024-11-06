from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


def create_zoned_image(current_event_bg_color, next_event_bg_color):    
    width = 240
    height = 280
    
    top_zone_height = 50
    middle_zone_height = 175
    bottom_zone_height = 55
    
    top_zone_color = (0, 0, 0)
    
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    top_zone = (0, 0, width, top_zone_height)
    draw.rectangle(top_zone, fill=top_zone_color)

    middle_zone = (0, top_zone_height, width, top_zone_height + middle_zone_height)
    draw.rectangle(middle_zone, fill=current_event_bg_color)
    
    bottom_zone = (0, top_zone_height + middle_zone_height, width, height)
    draw.rectangle(bottom_zone, fill=next_event_bg_color)

    line_y_position = top_zone_height + middle_zone_height
    draw.line([(0, line_y_position), (width, line_y_position)], fill="black", width=3)
    
    return image

def split_text_to_fit(text, max_chars_per_line=15, extra_chars_next_line=10):
    first_line = text[:max_chars_per_line].strip()

    remaining_text = text[max_chars_per_line:].strip()
    if not remaining_text:
        return [first_line]

    second_line = remaining_text[:extra_chars_next_line].strip()

    if len(remaining_text) > extra_chars_next_line:
        second_line = second_line + "..."

    return [first_line, second_line]

def truncate_text(text, max_chars_per_line=15):
    if len(text) > max_chars_per_line:
        return text[:max_chars_per_line] + "..."
    return text

def draw_text_on_zoned_image(image, current_time, current_event, next_event):
    width = image.width
    top_zone_height = 60
    middle_zone_height = 165
    
    font_path = "MontserratBlack-3zOvZ.ttf"
    font_large = ImageFont.truetype(font_path, 24)
    font_small = ImageFont.truetype(font_path, 17)
    font_date = ImageFont.truetype(font_path, 17)
    
    draw = ImageDraw.Draw(image)

    bbox = draw.textbbox((0, 0), current_time, font=font_large)
    text_width = bbox[2] - bbox[0]
    x_position = (width - text_width) / 2
    draw.text((x_position, 10), current_time, font=font_large, fill="white")

    if current_event:
        if hasattr(current_event, 'start_date'):
            start_date_str = current_event.start_date.split('T')[0]
            start_datetime = datetime.strptime(start_date_str, "%Y-%m-%d")
            formatted_start_date = f"{start_datetime.strftime('%A, %B')} {start_datetime.day}" 
            
            bbox = draw.textbbox((0, 0), formatted_start_date, font=font_date)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) / 2
            draw.text((x_position, top_zone_height + 10), formatted_start_date, font=font_date, fill="black")
        
        if hasattr(current_event, 'start') and hasattr(current_event, 'end'):
            current_event_time = f"{current_event.start} - {current_event.end}"
            bbox = draw.textbbox((0, 0), current_event_time, font=font_large)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) / 2
            draw.text((x_position, top_zone_height + 35), current_event_time, font=font_large, fill="black")
        
        if hasattr(current_event, 'subject') and current_event.subject:
            lines = split_text_to_fit(current_event.subject, max_chars_per_line=15, extra_chars_next_line=10)
            y_position = top_zone_height + 85
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font_large)
                text_width = bbox[2] - bbox[0]
                x_position = (width - text_width) / 2
                draw.text((x_position, y_position), line, font=font_large, fill="black")
                y_position += 30
    else:
        no_event_text = "No current event"
        bbox = draw.textbbox((0, 0), no_event_text, font=font_large)
        text_width = bbox[2] - bbox[0]
        x_position = (width - text_width) / 2
        draw.text((x_position, top_zone_height + 85), no_event_text, font=font_large, fill="black")

    if next_event:
        if hasattr(next_event, 'start') and hasattr(next_event, 'end'):
            next_event_time = f"{next_event.start} - {next_event.end}"
            bbox = draw.textbbox((0, 0), next_event_time, font=font_small)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) / 2
            draw.text((x_position, top_zone_height + middle_zone_height + 5), next_event_time, font=font_small, fill="black")

        if hasattr(next_event, 'subject') and next_event.subject:
            truncated_text = truncate_text(next_event.subject, max_chars_per_line=15)
            bbox = draw.textbbox((0, 0), truncated_text, font=font_small)
            text_width = bbox[2] - bbox[0]
            x_position = (width - text_width) / 2
            draw.text((x_position, top_zone_height + middle_zone_height + 25), truncated_text, font=font_small, fill="black")
    else:
        no_next_event_text = "No upcoming event"
        bbox = draw.textbbox((0, 0), no_next_event_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        x_position = (width - text_width) / 2
        draw.text((x_position, top_zone_height + middle_zone_height + 25), no_next_event_text, font=font_small, fill="black")

    return image