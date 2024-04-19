import cv2


def write_exercises(img, exercises):
    if not exercises:
        return

    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_color = (0, 255, 0)
    text_color_bg = (0, 0, 255)

    max_text_width = 0
    total_text_height = 0

    for ex_name, ex_count in exercises.items():
        text = f'{ex_name}: {ex_count}'
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        if (text_w > max_text_width):
            max_text_width = text_w
        total_text_height += text_h + 5

        cv2.putText(img, text, (3, total_text_height),
                    font, font_scale, text_color, font_thickness)

    cv2.rectangle(img, (2, 2), (max_text_width+5,
                  total_text_height+5), text_color_bg)


def write_line(img, text, text_color, background_color):
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.5
    font_thickness = 1

    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size

    cv2.rectangle(img, (2, 2), (text_w+2, text_h+7), background_color, -1)
    cv2.putText(img, text, (3, text_h+5), font, font_scale,
                text_color, font_thickness)
