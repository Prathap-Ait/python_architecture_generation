from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import boto3

# Create a high-quality image, Pillow library is used to create architecture diagram
width = 1200
height = 650
image = Image.new('RGB', (width, height), 'white')  # Creates Background
draw = ImageDraw.Draw(image)

# Define colors
color_gray_border = "#A0A0A0"
color_gray_bg = "#F5F5F5"
color_blue = "#4472C4"
color_orange = "#ED7D31"
color_purple = "#7030A0"
color_green = "#70AD47"
color_black = "#000000"

# Load fonts - try to load system fonts, fallback to default (Pillow fonts)
try:
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
    font_normal = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
except:
    font_title = ImageFont.load_default()
    font_normal = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Helper function to draw rounded rectangle (for main boxes)
def draw_rounded_rectangle(draw, xy, radius=15, fill=None, outline=None, width=2):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill, outline=outline, width=0)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill, outline=outline, width=0)
    draw.pieslice([x1, y1, x1+radius*2, y1+radius*2], 180, 270, fill=fill, outline=outline)
    draw.pieslice([x2-radius*2, y1, x2, y1+radius*2], 270, 360, fill=fill, outline=outline)
    draw.pieslice([x1, y2-radius*2, x1+radius*2, y2], 90, 180, fill=fill, outline=outline)
    draw.pieslice([x2-radius*2, y2-radius*2, x2, y2], 0, 90, fill=fill, outline=outline)
    if outline:
        draw.arc([x1, y1, x1+radius*2, y1+radius*2], 180, 270, fill=outline, width=width)
        draw.arc([x2-radius*2, y1, x2, y1+radius*2], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-radius*2, x1+radius*2, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-radius*2, y2-radius*2, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1+radius, y1, x2-radius, y1], fill=outline, width=width)
        draw.line([x1+radius, y2, x2-radius, y2], fill=outline, width=width)
        draw.line([x1, y1+radius, x1, y2-radius], fill=outline, width=width)
        draw.line([x2, y1+radius, x2, y2-radius], fill=outline, width=width)

# NEW HELPER FUNCTION - Smooth curved corners for small boxes (NOT folded)
def draw_smooth_rounded_box(draw, xy, radius=5, fill=None, outline=None, width=1):
    """Draw a box with smooth curved corners - no folding effect"""
    x1, y1, x2, y2 = xy
    
    # Draw the main rectangles
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill, outline=None)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill, outline=None)
    
    # Draw the corner circles (filled)
    draw.ellipse([x1, y1, x1+radius*2, y1+radius*2], fill=fill, outline=None)
    draw.ellipse([x2-radius*2, y1, x2, y1+radius*2], fill=fill, outline=None)
    draw.ellipse([x1, y2-radius*2, x1+radius*2, y2], fill=fill, outline=None)
    draw.ellipse([x2-radius*2, y2-radius*2, x2, y2], fill=fill, outline=None)
    
    # Draw the outline if specified
    if outline:
        # Draw corner arcs
        draw.arc([x1, y1, x1+radius*2, y1+radius*2], 180, 270, fill=outline, width=width)
        draw.arc([x2-radius*2, y1, x2, y1+radius*2], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-radius*2, x1+radius*2, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-radius*2, y2-radius*2, x2, y2], 0, 90, fill=outline, width=width)
        
        # Draw straight lines
        draw.line([x1+radius, y1, x2-radius, y1], fill=outline, width=width)
        draw.line([x1+radius, y2, x2-radius, y2], fill=outline, width=width)
        draw.line([x1, y1+radius, x1, y2-radius], fill=outline, width=width)
        draw.line([x2, y1+radius, x2, y2-radius], fill=outline, width=width)

# Center offset to shift everything to center
x_offset = 80

# Define box positions
left_box = (30 + x_offset, 70, 290 + x_offset, 450)
top_middle_left = (310 + x_offset, 70, 545 + x_offset, 310)  # Changed from 370 to 310 to match top_middle_right height
top_middle_right = (565 + x_offset, 70, 800 + x_offset, 310)

gap = 15
start_x = 310 + x_offset
end_x = 800 + x_offset
total_width = end_x - start_x
box_width = int((total_width - 2 * gap) / 3)

small_box_1 = (start_x, 330, start_x + box_width, 445)
small_box_2 = (start_x + box_width + gap, 330, start_x + 2*box_width + gap, 445)
small_box_3 = (start_x + 2*box_width + 2*gap, 330, start_x + 3*box_width + 2*gap, 445)

bottom_box = (50 + x_offset, 455, 800 + x_offset, 600)
right_box_1 = (820 + x_offset, 70, 1020 + x_offset, 335)
right_box_2 = (820 + x_offset, 355, 1020 + x_offset, 600)

# Draw gradient line at top
for i in range(400):
    x_start = 400 + i
    color_val = int(180 - (i/400) * 50)
    draw.line([(x_start, 30), (x_start, 35)], fill=(color_val, color_val-20, color_val+20), width=2)

# Draw gradient line at top
for i in range(400):
    x_start = 400 + i
    color_val = int(180 - (i/400) * 50)
    draw.line([(x_start, 30), (x_start, 35)], fill=(color_val, color_val-20, color_val+20), width=2)

# ============================================================
# NEW: SINGLE JSON FOR ALL DYNAMIC SECTIONS
usecase_json = {
    "usecaseDetails": {
        "usecaseId": "",
        "department": [],
        "platform": [],
        "baseModelName": []
    },
    "bucketName": "",
    "folderName": ""
}
# ============================================================

# ----- Dynamic UI Tag/Chip Bar for Agentic AI Portals & UI top -----
def draw_centered_dyn_subboxes(draw, parent_box, items, box_color, text_color, outline_color, font, y_offset):
    if not items:
        return y_offset
    sub_box_height = 26
    sub_box_vgap = 8
    sub_box_hgap = 7
    min_sub_box_width = 70
    max_sub_box_width = 140

    # Calculate widths for each tag
    sub_box_widths = []
    for item in items:
        bbox = draw.textbbox((0, 0), item, font=font)
        width = min(max(bbox[2] - bbox[0] + 20, min_sub_box_width), max_sub_box_width)
        sub_box_widths.append(width)
    available_width = parent_box[2] - parent_box[0] - 40
    n = len(items)
    # Find per row
    for boxes_per_row in range(n, 0, -1):
        row_width = sum(sorted(sub_box_widths, reverse=True)[:boxes_per_row]) + (boxes_per_row - 1) * sub_box_hgap
        if row_width <= available_width or boxes_per_row == 1:
            break
    # Arrange into rows
    rows = []
    i = 0
    while i < n:
        row_count = min(boxes_per_row, n - i)
        rows.append(items[i:i + row_count])
        i += row_count
    num_rows = len(rows)
    content_height = num_rows * sub_box_height + (num_rows - 1) * sub_box_vgap
    parent_height = content_height + 12
    parent_box_xy = (
        parent_box[0] + 10,
        y_offset,
        parent_box[2] - 10,
        y_offset + parent_height
    )
    # Sub-boxes in rows, centered
    y_start = parent_box_xy[1] + 4
    item_idx = 0
    for row in rows:
        row_widths = sub_box_widths[item_idx:item_idx + len(row)]
        row_total_width = sum(row_widths) + (len(row) - 1) * sub_box_hgap
        x_start = parent_box_xy[0] + ((parent_box_xy[2] - parent_box_xy[0]) - row_total_width) // 2
        for i, item in enumerate(row):
            w = row_widths[i]
            x1 = x_start
            y1 = y_start
            x2 = x1 + w
            y2 = y1 + sub_box_height
            draw_smooth_rounded_box(draw, (x1, y1, x2, y2), radius=7, fill=box_color, outline=outline_color, width=2)
            bbox_item = draw.textbbox((0, 0), item, font=font)
            text_x = x1 + (w - (bbox_item[2] - bbox_item[0])) // 2
            text_y = y1 + (sub_box_height - (bbox_item[3] - bbox_item[1])) // 2
            draw.text((text_x, text_y), item, fill=text_color, font=font)
            x_start += w + sub_box_hgap
            item_idx += 1
        y_start += sub_box_height + sub_box_vgap
    return parent_box_xy[3]


# =========================================================================
# SECTION 1: LEFT BOX - Agentic AI Portals & UI
# =========================================================================
draw_smooth_rounded_box(draw, left_box, radius=15, fill=color_gray_bg, outline="#B4C7E7", width=2)

title_text = "Agentic AI Portals & UI"
bbox = draw.textbbox((0, 0), title_text, font=font_title)
title_width = bbox[2] - bbox[0]
title_x = left_box[0] + ((left_box[2] - left_box[0]) - title_width) // 2

# --- Dynamic UI tags/chips (below section title, above Agent Inventory) ---
ui_tag_items = usecase_json["usecaseDetails"]["department"]
ui_tags_y = left_box[1] + 30  # Adjust as per spacing in your section
draw_centered_dyn_subboxes(
    draw, left_box, ui_tag_items,
    box_color="#E8F4F8", text_color=color_blue, outline_color=color_blue,
    font=font_normal, y_offset=ui_tags_y
)
draw.text((title_x, left_box[1] + 6), title_text, fill=color_blue, font=font_title)

# === Moved Agent Inventory section down by +20px ===
agent_inv_y_offset = 20

draw_smooth_rounded_box(draw, (left_box[0] + 18, left_box[1] + 75 + agent_inv_y_offset, left_box[2] - 18, left_box[1] + 245 + agent_inv_y_offset), 
                       radius=10, fill='white', outline=color_gray_border, width=1)

inv_text = "Agent Inventory"
bbox = draw.textbbox((0, 0), inv_text, font=font_normal)
inv_width = bbox[2] - bbox[0]
inv_x = left_box[0] + 18 + ((left_box[2] - left_box[0] - 36) - inv_width) // 2
draw.text((inv_x, left_box[1] + 83 + agent_inv_y_offset), inv_text, fill=color_black, font=font_normal)

# POC | MVP | PROD tabs - CURVED EDGES
draw_smooth_rounded_box(draw, [left_box[0] + 28, left_box[1] + 113 + agent_inv_y_offset, left_box[0] + 78, left_box[1] + 133 + agent_inv_y_offset], 
                        radius=5, outline=color_gray_border, width=1)
draw.text((left_box[0] + 43, left_box[1] + 118 + agent_inv_y_offset), "POC", fill=color_black, font=font_small)

draw_smooth_rounded_box(draw, [left_box[0] + 93, left_box[1] + 113 + agent_inv_y_offset, left_box[0] + 143, left_box[1] + 133 + agent_inv_y_offset], 
                        radius=5, outline=color_gray_border, width=1)
draw.text((left_box[0] + 105, left_box[1] + 118 + agent_inv_y_offset), "MVP", fill=color_black, font=font_small)

draw_smooth_rounded_box(draw, [left_box[0] + 158, left_box[1] + 113 + agent_inv_y_offset, left_box[0] + 218, left_box[1] + 133 + agent_inv_y_offset], 
                        radius=5, outline=color_gray_border, width=1)
draw.text((left_box[0] + 168, left_box[1] + 118 + agent_inv_y_offset), "PROD", fill=color_black, font=font_small)

# Key Controls (KCI) - CURVED EDGES
draw_smooth_rounded_box(draw, [left_box[0] + 28, left_box[1] + 148 + agent_inv_y_offset, left_box[2] - 28, left_box[1] + 168 + agent_inv_y_offset], 
                        radius=5, fill='white', outline=color_orange, width=2)
draw.text((left_box[0] + 58, left_box[1] + 152 + agent_inv_y_offset), "Key Controls (KCI)", fill=color_black, font=font_small)

# Key Performance (KPI) - CURVED EDGES
draw_smooth_rounded_box(draw, [left_box[0] + 28, left_box[1] + 178 + agent_inv_y_offset, left_box[2] - 28, left_box[1] + 198 + agent_inv_y_offset], 
                        radius=5, fill='white', outline=color_blue, width=2)
draw.text((left_box[0] + 48, left_box[1] + 182 + agent_inv_y_offset), "Key Performance (KPI)", fill=color_black, font=font_small)

# Key Risks (KRI) - CURVED EDGES
draw_smooth_rounded_box(draw, [left_box[0] + 28, left_box[1] + 208 + agent_inv_y_offset, left_box[2] - 28, left_box[1] + 228 + agent_inv_y_offset], 
                        radius=5, fill='white', outline=color_green, width=2)
draw.text((left_box[0] + 63, left_box[1] + 212 + agent_inv_y_offset), "Key Risks (KRI)", fill=color_black, font=font_small)

# Agent Usage Section
usage_text = "Agent Usage"
bbox = draw.textbbox((0, 0), usage_text, font=font_normal)
usage_width = bbox[2] - bbox[0]
usage_x = left_box[0] + ((left_box[2] - left_box[0]) - usage_width) // 2
draw.text((usage_x, left_box[1] + 283), usage_text, fill=color_black, font=font_normal)

# Agent Usage boxes - CURVED EDGES
total_available_width = left_box[2] - left_box[0] - 50
box_width_usage = total_available_width // 3
box_height_usage = 38
box_gap = 5
y_start_usage = left_box[1] + 310

x_box1 = left_box[0] + 25
draw_smooth_rounded_box(draw, [x_box1, y_start_usage, x_box1 + box_width_usage, y_start_usage + box_height_usage], 
                        radius=6, fill='white', outline=color_gray_border, width=1)
pol_text = "Policies"
bbox = draw.textbbox((0, 0), pol_text, font=font_small)
pol_width = bbox[2] - bbox[0]
pol_x = x_box1 + (box_width_usage - pol_width) // 2
draw.text((pol_x, y_start_usage + 14), pol_text, fill=color_black, font=font_small)

x_box2 = x_box1 + box_width_usage + box_gap
draw_smooth_rounded_box(draw, [x_box2, y_start_usage, x_box2 + box_width_usage, y_start_usage + box_height_usage], 
                        radius=6, fill='white', outline=color_gray_border, width=1)
bbox1 = draw.textbbox((0, 0), "Terms and", font=font_small)
bbox2 = draw.textbbox((0, 0), "conditions", font=font_small)
terms_x1 = x_box2 + (box_width_usage - (bbox1[2] - bbox1[0])) // 2
terms_x2 = x_box2 + (box_width_usage - (bbox2[2] - bbox2[0])) // 2
draw.text((terms_x1, y_start_usage + 8), "Terms and", fill=color_black, font=font_small)
draw.text((terms_x2, y_start_usage + 22), "conditions", fill=color_black, font=font_small)

x_box3 = x_box2 + box_width_usage + box_gap
draw_smooth_rounded_box(draw, [x_box3, y_start_usage, x_box3 + box_width_usage, y_start_usage + box_height_usage], 
                        radius=6, fill='white', outline=color_gray_border, width=1)
bbox1 = draw.textbbox((0, 0), "User", font=font_small)
bbox2 = draw.textbbox((0, 0), "training", font=font_small)
user_x1 = x_box3 + (box_width_usage - (bbox1[2] - bbox1[0])) // 2
user_x2 = x_box3 + (box_width_usage - (bbox2[2] - bbox2[0])) // 2
draw.text((user_x1, y_start_usage + 8), "User", fill=color_black, font=font_small)
draw.text((user_x2, y_start_usage + 22), "training", fill=color_black, font=font_small)

# ============================================================================
# SECTION 2: TOP MIDDLE LEFT - Agentic AI Data platforms (PERFECT LAYOUT)
# ============================================================================
draw_smooth_rounded_box(draw, top_middle_left, radius=15, fill=color_gray_bg, outline="#B4C7E7", width=2)

# Title - Centered at top
title_text = "Agentic AI Data platforms"
bbox = draw.textbbox((0, 0), title_text, font=font_title)
title_width = bbox[2] - bbox[0]
title_x = top_middle_left[0] + ((top_middle_left[2] - top_middle_left[0]) - title_width) // 2
draw.text((title_x, top_middle_left[1] + 6), title_text, fill=color_orange, font=font_title)

# LEFT COLUMN - Three data type boxes stacked vertically
left_col_x = top_middle_left[0] + 15
left_col_width = 105
box_height = 24
y_pos = top_middle_left[1] + 32

# Unstructured data
draw_smooth_rounded_box(draw, [left_col_x, y_pos, left_col_x + left_col_width, y_pos + box_height], 
                        radius=8, fill='white', outline=color_gray_border, width=1)
bbox = draw.textbbox((0, 0), "Unstructured data", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = left_col_x + (left_col_width - text_width) // 2
draw.text((text_x, y_pos + 8), "Unstructured data", fill=color_black, font=font_small)

# Structured data
y_pos += box_height + 6
draw_smooth_rounded_box(draw, [left_col_x, y_pos, left_col_x + left_col_width, y_pos + box_height], 
                        radius=8, fill='white', outline=color_gray_border, width=1)
bbox = draw.textbbox((0, 0), "Structured data", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = left_col_x + (left_col_width - text_width) // 2
draw.text((text_x, y_pos + 8), "Structured data", fill=color_black, font=font_small)

# Events & Jobs
y_pos += box_height + 6
draw_smooth_rounded_box(draw, [left_col_x, y_pos, left_col_x + left_col_width, y_pos + box_height], 
                        radius=8, fill='white', outline=color_gray_border, width=1)
bbox = draw.textbbox((0, 0), "Events & Jobs", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = left_col_x + (left_col_width - text_width) // 2
draw.text((text_x, y_pos + 8), "Events & Jobs", fill=color_black, font=font_small)

# MIDDLE SECTION - Data annotations & Vector DB (MOVED BETWEEN LEFT BOXES AND GOLDEN DATASET)
middle_x = left_col_x + left_col_width + 10  # Position right after the three boxes
middle_y = top_middle_left[1] + 80  # Vertical center position

# Data annotations text
draw.text((middle_x, middle_y), "Data", fill=color_black, font=font_small)
draw.text((middle_x - 5, middle_y + 12), "annotations", fill=color_black, font=font_small)

# Icon placeholder (between texts)
draw.text((middle_x + 15, middle_y + 25), "📊", fill=color_orange, font=font_normal)

# Vector DB text - MOVED TO RIGHT END AND UPWARDSIntegrate 
vector_db_x = top_middle_left[2] - 60  # Right end position
vector_db_y = top_middle_left[1] + 110  # Moved down slightly from 90 to 105
draw.text((vector_db_x, vector_db_y), "Vector DB", fill=color_black, font=font_small)

# RIGHT COLUMN - Golden Dataset box (SMALLER, MOVED UP & RIGHT)
right_col_x = top_middle_left[0] + 160
right_col_width = top_middle_left[2] - right_col_x - 10
golden_height = 38

# Golden Dataset - Prominent box with orange border
golden_y = top_middle_left[1] + 35
draw_smooth_rounded_box(draw, [right_col_x, golden_y, right_col_x + right_col_width, golden_y + golden_height], 
                        radius=10, fill='#FFF5E6', outline=color_orange, width=3)
bbox1 = draw.textbbox((0, 0), "Golden", font=font_small)
bbox2 = draw.textbbox((0, 0), "Dataset", font=font_small)
text_x1 = right_col_x + (right_col_width - (bbox1[2] - bbox1[0])) // 2
text_x2 = right_col_x + (right_col_width - (bbox2[2] - bbox2[0])) // 2
draw.text((text_x1, golden_y + 8), "Golden", fill=color_black, font=font_small)
draw.text((text_x2, golden_y + 22), "Dataset", fill=color_black, font=font_small)

# RIGHT SIDE - Memory boxes (Episodic & Long-term) - MOVED TO RIGHT END
memory_box_width = 135
memory_box_height = 24
memory_x = top_middle_left[2] - memory_box_width - 15
memory_y_start = vector_db_y + 25  # Changed from top_middle_left[1] + 172 to be under Vector DB

# --- Load icons for memory boxes (outer left) ---
db_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/DB.png"
file_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/File+storage.png"
try:
    db_icon_response = requests.get(db_icon_url)
    db_icon_img = Image.open(BytesIO(db_icon_response.content)).convert("RGBA")
    db_icon_img = db_icon_img.resize((38, 38), Image.LANCZOS)
except Exception as e:
    db_icon_img = None

try:
    file_icon_response = requests.get(file_icon_url)
    file_icon_img = Image.open(BytesIO(file_icon_response.content)).convert("RGBA")
    file_icon_img = file_icon_img.resize((38, 38), Image.LANCZOS)
except Exception as e:
    file_icon_img = None

# Position for the icons (outer left of both boxes, vertically centered)
icons_x = memory_x - 50  # 50px to the left of the memory boxes
icons_y1 = memory_y_start - 8  # align vertically with Episodic memory box
icons_y2 = memory_y_start + memory_box_height + 8  # align vertically with Long-term memory box

if db_icon_img:
    image.paste(db_icon_img, (icons_x, icons_y1), db_icon_img)
if file_icon_img:
    image.paste(file_icon_img, (icons_x, icons_y2), file_icon_img)

# Episodic memory - RIGHT SIDE
draw_smooth_rounded_box(draw, [memory_x, memory_y_start, memory_x + memory_box_width, memory_y_start + memory_box_height], 
                        radius=10, fill='white', outline=color_gray_border, width=1)
bbox = draw.textbbox((0, 0), "Episodic memory", font=font_normal)
text_width = bbox[2] - bbox[0]
text_x = memory_x + (memory_box_width - text_width) // 2
draw.text((text_x, memory_y_start + 7), "Episodic memory", fill=color_black, font=font_normal)

# Long-term memory - RIGHT SIDE
memory_y_start += memory_box_height + 8
draw_smooth_rounded_box(draw, [memory_x, memory_y_start, memory_x + memory_box_width, memory_y_start + memory_box_height], 
                        radius=10, fill='white', outline=color_gray_border, width=1)
bbox = draw.textbbox((0, 0), "Long-term memory", font=font_normal)
text_width = bbox[2] - bbox[0]
text_x = memory_x + (memory_box_width - text_width) // 2
draw.text((text_x, memory_y_start + 7), "Long-term memory", fill=color_black, font=font_normal)

# BOTTOM - Data Quality & governance (FULL WIDTH - STYLED LIKE KPI BOX)
governance_y = memory_y_start + memory_box_height + 10
governance_height = 30
full_width = top_middle_left[2] - top_middle_left[0] - 30

draw_smooth_rounded_box(draw, [top_middle_left[0] + 15, governance_y, top_middle_left[2] - 15, governance_y + governance_height], 
                        radius=12, fill='white', outline=color_blue, width=2)
bbox = draw.textbbox((0, 0), "Data Quality & governance", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = top_middle_left[0] + 15 + (full_width - text_width) // 2
draw.text((text_x, governance_y + 11), "Data Quality & governance", fill=color_black, font=font_small)

# ============================================================================
# SECTION 3: TOP MIDDLE RIGHT - Agentic AI Solution
# ============================================================================

box_xy = top_middle_right
draw_smooth_rounded_box(draw, box_xy, radius=15, fill=color_gray_bg, outline="#B4C7E7", width=2)

# Title centered at the top
title_text = "Agentic AI Solution"
bbox = draw.textbbox((0, 0), title_text, font=font_title)
title_width = bbox[2] - bbox[0]
title_x = box_xy[0] + ((box_xy[2] - box_xy[0]) - title_width) // 2
draw.text((title_x, box_xy[1] + 10), title_text, fill=color_black, font=font_title)

def draw_compact_centered_subboxes(parent_box, label, items, box_color, text_color, outline_color, font, y_offset):
    if not items:
        return y_offset  # Do nothing if items is empty
    # Parameters for compact boxes
    sub_box_height = 26
    sub_box_vgap = 7
    sub_box_hgap = 7
    min_sub_box_width = 70
    max_sub_box_width = 110
    # Calculate widths for each item
    sub_box_widths = []
    for item in items:
        bbox = draw.textbbox((0, 0), item, font=font)
        width = min(max(bbox[2] - bbox[0] + 16, min_sub_box_width), max_sub_box_width)
        sub_box_widths.append(width)
    # Calculate how many boxes fit per row
    available_width = parent_box[2] - parent_box[0] - 40
    n = len(items)
    for boxes_per_row in range(n, 0, -1):
        row_width = sum(sorted(sub_box_widths, reverse=True)[:boxes_per_row]) + (boxes_per_row - 1) * sub_box_hgap
        if row_width <= available_width or boxes_per_row == 1:
            break
    # Arrange items into rows
    rows = []
    i = 0
    while i < n:
        row_count = min(boxes_per_row, n - i)
        rows.append(items[i:i + row_count])
        i += row_count
    # Calculate parent box height
    num_rows = len(rows)
    content_height = num_rows * sub_box_height + (num_rows - 1) * sub_box_vgap
    parent_height = content_height + 38  # Space for label
    parent_box_xy = (
        parent_box[0] + 16,
        y_offset,
        parent_box[2] - 16,
        y_offset + parent_height
    )
    draw_rounded_rectangle(draw, parent_box_xy, radius=10, fill='white', outline=color_gray_border, width=1)

    # Draw label (vertically centered if possible)
    bbox_label = draw.textbbox((0, 0), label, font=font)
    label_width = bbox_label[2] - bbox_label[0]
    label_x = parent_box_xy[0] + ((parent_box_xy[2] - parent_box_xy[0]) - label_width) // 2
    label_y = parent_box_xy[1] + 6
    draw.text((label_x, label_y), label, fill=color_black, font=font)
    # Draw sub-boxes in rows, centered
    y_start = parent_box_xy[1] + 28
    item_idx = 0
    for row in rows:
        row_widths = sub_box_widths[item_idx:item_idx + len(row)]
        row_total_width = sum(row_widths) + (len(row) - 1) * sub_box_hgap
        x_start = parent_box_xy[0] + ((parent_box_xy[2] - parent_box_xy[0]) - row_total_width) // 2
        for i, item in enumerate(row):
            w = row_widths[i]
            x1 = x_start
            y1 = y_start
            x2 = x1 + w
            y2 = y1 + sub_box_height
            draw_smooth_rounded_box(draw, (x1, y1, x2, y2), radius=8, fill=box_color, outline=outline_color, width=2)
            bbox_item = draw.textbbox((0, 0), item, font=font)
            text_x = x1 + (w - (bbox_item[2] - bbox_item[0])) // 2
            text_y = y1 + (sub_box_height - (bbox_item[3] - bbox_item[1])) // 2
            draw.text((text_x, text_y), item, fill=text_color, font=font)
            x_start += w + sub_box_hgap
            item_idx += 1
        y_start += sub_box_height + sub_box_vgap
    return parent_box_xy[3]

# --- Agent runtimes sub-box ---
platforms = usecase_json["usecaseDetails"]["platform"]
next_y = box_xy[1] + 38
next_y = draw_compact_centered_subboxes(
    box_xy, "Agent runtimes", platforms,
    box_color='#E8F4F8', text_color=color_blue, outline_color=color_blue,
    font=font_normal, y_offset=next_y
)

# --- Agent tools sub-box ---
next_y += 10  # gap between sections
draw_compact_centered_subboxes(
    box_xy, "Agent tools", platforms,
    box_color='#FFF8E8', text_color=color_orange, outline_color=color_orange,
    font=font_normal, y_offset=next_y
) 

# ============================================================================
# Cloud Services Section (Inside Agentic AI Solution) - FINALIZED
# ============================================================================

# Cloud provider icon mapping
CLOUD_ICON_MAP = {
    "aws": "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/AWS.png",
    "gcp": "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/GCP+-+Icon.png",
    "azure": "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/azure-icon.svg"
}

def normalize_cloud_provider(platform_name):
    """Normalize platform name to detect cloud provider"""
    normalized = platform_name.lower().strip()
    # AWS variations
    aws_keywords = ["aws", "amazon", "bedrock", "sagemaker", "ec2"]
    if any(keyword in normalized for keyword in aws_keywords):
        return "AWS"
    # GCP variations
    gcp_keywords = ["gcp", "google", "vertex", "bigquery", "cloud platform"]
    if any(keyword in normalized for keyword in gcp_keywords):
        return "GCP"
    # Azure variations
    azure_keywords = ["azure", "microsoft", "openai"]
    if any(keyword in normalized for keyword in azure_keywords):
        return "Azure"
    return None

def draw_cloud_services_section(parent_box, platforms, y_offset):
    """Draw Cloud Services section with dynamic cloud provider icons"""
    if not platforms:
        return y_offset
    # Filter and match cloud providers from platform data
    cloud_providers = []
    cloud_icons = []
    for platform in platforms:
        provider = normalize_cloud_provider(platform)
        if provider and provider not in cloud_providers:  # Avoid duplicates
            cloud_providers.append(provider)
            cloud_icons.append(CLOUD_ICON_MAP[provider.lower()])
    if not cloud_providers:
        return y_offset
    # Box dimensions
    section_height = 80
    parent_box_xy = (
        parent_box[0] + 16,
        y_offset,
        parent_box[2] - 16,
        y_offset + section_height
    )
    draw_rounded_rectangle(draw, parent_box_xy, radius=10, fill='white', outline=color_gray_border, width=1)
    # Draw label
    label = "Cloud Services"
    bbox_label = draw.textbbox((0, 0), label, font=font_normal)
    label_width = bbox_label[2] - bbox_label[0]
    label_x = parent_box_xy[0] + ((parent_box_xy[2] - parent_box_xy[0]) - label_width) // 2
    label_y = parent_box_xy[1] + 6
    draw.text((label_x, label_y), label, fill=color_black, font=font_normal)
    # Load and display cloud icons
    icon_size = 40
    icon_gap = 15
    total_icon_width = len(cloud_icons) * icon_size + (len(cloud_icons) - 1) * icon_gap
    start_x = parent_box_xy[0] + ((parent_box_xy[2] - parent_box_xy[0]) - total_icon_width) // 2
    icon_y = parent_box_xy[1] + 32
    for i, icon_url in enumerate(cloud_icons):
        try:
            if icon_url.endswith('.svg'):
                # For SVG, draw placeholder with provider name
                icon_x = start_x + i * (icon_size + icon_gap)
                draw_smooth_rounded_box(draw, [icon_x, icon_y, icon_x + icon_size, icon_y + icon_size],
                                        radius=5, fill='#E8F5FF', outline=color_blue, width=2)
                text = cloud_providers[i]
                bbox = draw.textbbox((0, 0), text, font=font_small)
                text_width = bbox[2] - bbox[0]
                text_x = icon_x + (icon_size - text_width) // 2
                draw.text((text_x, icon_y + 15), text, fill=color_blue, font=font_small)
            else:
                # Load PNG/JPG icon
                response = requests.get(icon_url, timeout=5)
                cloud_icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
                cloud_icon_img = cloud_icon_img.resize((icon_size, icon_size), Image.LANCZOS)
                icon_x = start_x + i * (icon_size + icon_gap)
                image.paste(cloud_icon_img, (icon_x, icon_y), cloud_icon_img)
        except Exception as e:
            print(f"Error loading icon {icon_url}: {e}")
            # Draw fallback placeholder
            icon_x = start_x + i * (icon_size + icon_gap)
            draw_smooth_rounded_box(draw, [icon_x, icon_y, icon_x + icon_size, icon_y + icon_size],
                                    radius=5, fill='#F0F0F0', outline=color_gray_border, width=1)
            text = cloud_providers[i]
            bbox = draw.textbbox((0, 0), text, font=font_small)
            text_width = bbox[2] - bbox[0]
            text_x = icon_x + (icon_size - text_width) // 2
            draw.text((text_x, icon_y + 15), text, fill=color_black, font=font_small)
    return parent_box_xy[3]

# Draw Cloud Services section (adds 10px gap, then draws section)
next_y += 10
next_y = draw_cloud_services_section(box_xy, platforms, next_y)

# ============================================================================
# SECTION 4: SMALL BOX 1 - SDLC / Deployment
# ============================================================================
draw_smooth_rounded_box(draw, small_box_1, radius=10, fill=color_gray_bg, outline="#B4C7E7", width=2)

title_text = "SDLC / Deployment"
bbox = draw.textbbox((0, 0), title_text, font=font_small)
title_width = bbox[2] - bbox[0]
title_x = small_box_1[0] + ((small_box_1[2] - small_box_1[0]) - title_width) // 2
draw.text((title_x, small_box_1[1] + 4), title_text, fill=color_purple, font=font_small)

box_height = 22
y_start = small_box_1[1] + 28
box_spacing = 5

# IAC guardrails - CURVED
draw_smooth_rounded_box(draw, [small_box_1[0] + 10, y_start, small_box_1[2] - 10, y_start + box_height], 
                        radius=5, fill='white', outline=color_purple, width=1)
bbox = draw.textbbox((0, 0), "IAC guardrails", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = small_box_1[0] + 10 + ((small_box_1[2] - small_box_1[0] - 20) - text_width) // 2
draw.text((text_x, y_start + 7), "IAC guardrails", fill=color_black, font=font_small)

y_start += box_height + box_spacing
draw_smooth_rounded_box(draw, [small_box_1[0] + 10, y_start, small_box_1[2] - 10, y_start + box_height], 
                        radius=5, fill='white', outline=color_purple, width=1)
bbox = draw.textbbox((0, 0), "Vulnerability scanners", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = small_box_1[0] + 10 + ((small_box_1[2] - small_box_1[0] - 20) - text_width) // 2
draw.text((text_x, y_start + 7), "Vulnerability scanners", fill=color_black, font=font_small)

y_start += box_height + box_spacing
draw_smooth_rounded_box(draw, [small_box_1[0] + 10, y_start, small_box_1[2] - 10, y_start + box_height], 
                        radius=5, fill='white', outline=color_purple, width=1)
bbox = draw.textbbox((0, 0), "Deployment gating", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = small_box_1[0] + 10 + ((small_box_1[2] - small_box_1[0] - 20) - text_width) // 2
draw.text((text_x, y_start + 7), "Deployment gating", fill=color_black, font=font_small)

# ============================================================================
# SECTION 5: SMALL BOX 2 - Agent Security
# ============================================================================
draw_smooth_rounded_box(draw, small_box_2, radius=10, fill=color_gray_bg, outline="#B4C7E7", width=2)

title_text = "Agent Security"
bbox = draw.textbbox((0, 0), title_text, font=font_small)
title_width = bbox[2] - bbox[0]
title_x = small_box_2[0] + ((small_box_2[2] - small_box_2[0]) - title_width) // 2
draw.text((title_x, small_box_2[1] + 4), title_text, fill=color_orange, font=font_small)

total_width = small_box_2[2] - small_box_2[0] - 16
box_width = (total_width - 6) // 2
box_height = 30
y_start = small_box_2[1] + 28
x_gap = 6
y_gap = 7

x1_left = small_box_2[0] + 8
x1_right = x1_left + box_width + x_gap

# Agent Identity - CURVED
draw_smooth_rounded_box(draw, [x1_left, y_start, x1_left + box_width, y_start + box_height], 
                        radius=6, fill='white', outline=color_gray_border, width=1)
bbox = draw.textbbox((0, 0), "Agent Identity", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = x1_left + (box_width - text_width) // 2
draw.text((text_x, y_start + 11), "Agent Identity", fill=color_black, font=font_small)

# Agent Gateway - CURVED
draw_smooth_rounded_box(draw, [x1_right, y_start, x1_right + box_width, y_start + box_height], 
                        radius=6, fill='white', outline=color_gray_border, width=1)
bbox1 = draw.textbbox((0, 0), "Agent", font=font_small)
bbox2 = draw.textbbox((0, 0), "Gateway", font=font_small)
text_x1 = x1_right + (box_width - (bbox1[2] - bbox1[0])) // 2
text_x2 = x1_right + (box_width - (bbox2[2] - bbox2[0])) // 2
draw.text((text_x1, y_start + 5), "Agent", fill=color_black, font=font_small)
draw.text((text_x2, y_start + 17), "Gateway", fill=color_black, font=font_small)

y_start += box_height + y_gap

# Human in the loop - CURVED
draw_smooth_rounded_box(draw, [x1_left, y_start, x1_left + box_width, y_start + box_height], 
                        radius=6, fill='white', outline=color_gray_border, width=1)
bbox1 = draw.textbbox((0, 0), "Human in", font=font_small)
bbox2 = draw.textbbox((0, 0), "the loop", font=font_small)
text_x1 = x1_left + (box_width - (bbox1[2] - bbox1[0])) // 2
text_x2 = x1_left + (box_width - (bbox2[2] - bbox2[0])) // 2
draw.text((text_x1, y_start + 5), "Human in", fill=color_black, font=font_small)
draw.text((text_x2, y_start + 17), "the loop", fill=color_black, font=font_small)

# Agent Guardrails - CURVED
draw_smooth_rounded_box(draw, [x1_right, y_start, x1_right + box_width, y_start + box_height], 
                        radius=6, fill='white', outline=color_gray_border, width=1)
bbox1 = draw.textbbox((0, 0), "Agent", font=font_small)
bbox2 = draw.textbbox((0, 0), "Guardrails", font=font_small)
text_x1 = x1_right + (box_width - (bbox1[2] - bbox1[0])) // 2
text_x2 = x1_right + (box_width - (bbox2[2] - bbox2[0])) // 2
draw.text((text_x1, y_start + 5), "Agent", fill=color_black, font=font_small)
draw.text((text_x2, y_start + 17), "Guardrails", fill=color_black, font=font_small)

# ============================================================================
# SECTION 6: SMALL BOX 3 - Observability
# ============================================================================
draw_smooth_rounded_box(draw, small_box_3, radius=10, fill=color_gray_bg, outline="#B4C7E7", width=2)

title_text = "Observability"
bbox = draw.textbbox((0, 0), title_text, font=font_small)
title_width = bbox[2] - bbox[0]
title_x = small_box_3[0] + ((small_box_3[2] - small_box_3[0]) - title_width) // 2
draw.text((title_x, small_box_3[1] + 4), title_text, fill=color_black, font=font_small)

box_height = 22
y_start = small_box_3[1] + 28
box_spacing = 5

# Agent KPI metrics - CURVED
draw_smooth_rounded_box(draw, [small_box_3[0] + 10, y_start, small_box_3[2] - 10, y_start + box_height], 
                        radius=5, fill='white', outline=color_gray_border, width=1)
bbox = draw.textbbox((0, 0), "Agent KPI metrics", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = small_box_3[0] + 10 + ((small_box_3[2] - small_box_3[0] - 20) - text_width) // 2
draw.text((text_x, y_start + 7), "Agent KPI metrics", fill=color_black, font=font_small)

y_start += box_height + box_spacing
draw_smooth_rounded_box(draw, [small_box_3[0] + 10, y_start, small_box_3[2] - 10, y_start + box_height], 
                        radius=5, fill='white', outline=color_gray_border, width=1)
bbox = draw.textbbox((0, 0), "TCO / ROI metrics", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = small_box_3[0] + 10 + ((small_box_3[2] - small_box_3[0] - 20) - text_width) // 2
draw.text((text_x, y_start + 7), "TCO / ROI metrics", fill=color_black, font=font_small)

y_start += box_height + box_spacing
draw_smooth_rounded_box(draw, [small_box_3[0] + 10, y_start, small_box_3[2] - 10, y_start + box_height], 
                        radius=5, fill='white', outline=color_gray_border, width=1)
bbox = draw.textbbox((0, 0), "Drift monitoring", font=font_small)
text_width = bbox[2] - bbox[0]
text_x = small_box_3[0] + 10 + ((small_box_3[2] - small_box_3[0] - 20) - text_width) // 2
draw.text((text_x, y_start + 7), "Drift monitoring", fill=color_black, font=font_small)

# ============================================================================
# SECTION 7: BOTTOM BOX - AI Governance
# ============================================================================
draw_smooth_rounded_box(draw, bottom_box, radius=15, fill=color_gray_bg, outline="#8796EB", width=2)
# AI Governance heading - BIGGER FONT
ai_gov_text = "AI Governance"
try:
    font_title_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)  # Increased from 13 to 15
except:
    font_title_large = font_title
draw.text((bottom_box[0] + 8, bottom_box[1] + 8), ai_gov_text, fill=color_orange, font=font_title_large)

# Define box dimensions
box_width = 210  # Width for each box
box_height_row1 = 25  # Height for first row
box_height_row2 = 33  # Height for second row (taller for 2-line text)
x_start = bottom_box[0] + 15  # Start from left with small margin
x_gap = 15  # Gap between boxes
y_row1 = bottom_box[1] + 42  # First row Y position
y_row2 = y_row1 + box_height_row1 + 10  # Second row Y position

# First Row - 3 boxes aligned from left
# Box 1 - AI Standard & Controls with icon
x_box1 = x_start
draw_smooth_rounded_box(draw, [x_box1, y_row1, x_box1 + box_width, y_row1 + box_height_row1], 
                        radius=5, fill='white', outline="#87CEEB", width=1)

# Load the icon
ai_std_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/AI-STD.png"
try:
    response = requests.get(ai_std_icon_url)
    ai_std_icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    ai_std_icon_img = ai_std_icon_img.resize((18, 18), Image.LANCZOS)
except Exception as e:
    ai_std_icon_img = None

# Calculate icon and text positions
icon_margin_left = 8
icon_y = y_row1 + (box_height_row1 - 18) // 2
text_gap = 6  # gap between icon and text

bbox = draw.textbbox((0, 0), "AI Standard & Controls", font=font_small)
text_width = bbox[2] - bbox[0]
# Place text after icon and gap
# Center the text+icon group in the box
total_content_width = 18 + text_gap + text_width
content_x = x_box1 + (box_width - total_content_width) // 2
icon_x = content_x
text_x = icon_x + 18 + text_gap

# Paste icon if loaded
if ai_std_icon_img:
    image.paste(ai_std_icon_img, (int(icon_x), int(icon_y)), ai_std_icon_img)
draw.text((int(text_x), y_row1 + 8), "AI Standard & Controls", fill=color_black, font=font_small)

# Box 2 - Cyber risk register with icon
x_box2 = x_box1 + box_width + x_gap
draw_smooth_rounded_box(draw, [x_box2, y_row1, x_box2 + box_width, y_row1 + box_height_row1], 
                        radius=5, fill='white', outline="#8796EB", width=1)

# Load the icon
cyber_risk_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/CRR.png"
try:
    response = requests.get(cyber_risk_icon_url)
    cyber_risk_icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    cyber_risk_icon_img = cyber_risk_icon_img.resize((18, 18), Image.LANCZOS)
except Exception as e:
    cyber_risk_icon_img = None

icon_margin_left = 8
icon_y = y_row1 + (box_height_row1 - 18) // 2
text_gap = 6  # gap between icon and text

bbox = draw.textbbox((0, 0), "Cyber risk register", font=font_small)
text_width = bbox[2] - bbox[0]
total_content_width = 18 + text_gap + text_width
content_x = x_box2 + (box_width - total_content_width) // 2
icon_x = content_x
text_x = icon_x + 18 + text_gap

if cyber_risk_icon_img:
    image.paste(cyber_risk_icon_img, (int(icon_x), int(icon_y)), cyber_risk_icon_img)
draw.text((int(text_x), y_row1 + 8), "Cyber risk register", fill=color_black, font=font_small)

# Box 3 - AI TCO/ROI with icon
x_box3 = x_box2 + box_width + x_gap
draw_smooth_rounded_box(draw, [x_box3, y_row1, x_box3 + box_width, y_row1 + box_height_row1], 
                        radius=5, fill='white', outline="#8796EB", width=1)

# Load the icon
ai_tco_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/AI-TCO+%26+ROI.png"
try:
    response = requests.get(ai_tco_icon_url)
    ai_tco_icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    ai_tco_icon_img = ai_tco_icon_img.resize((18, 18), Image.LANCZOS)
except Exception as e:
    ai_tco_icon_img = None

icon_margin_left = 8
icon_y = y_row1 + (box_height_row1 - 18) // 2
text_gap = 6  # gap between icon and text

bbox = draw.textbbox((0, 0), "AI TCO/ROI", font=font_small)
text_width = bbox[2] - bbox[0]
total_content_width = 18 + text_gap + text_width
content_x = x_box3 + (box_width - total_content_width) // 2
icon_x = content_x
text_x = icon_x + 18 + text_gap

if ai_tco_icon_img:
    image.paste(ai_tco_icon_img, (int(icon_x), int(icon_y)), ai_tco_icon_img)
draw.text((int(text_x), y_row1 + 8), "AI TCO/ROI", fill=color_black, font=font_small)

# Second Row - 3 boxes aligned from left
draw.text((text_x1, y_row2 + 6), "Agent Performance", fill=color_black, font=font_small)
# Box 4 - Agent Performance thresholds (KPI) with icon
x_box4 = x_start
draw_smooth_rounded_box(draw, [x_box4, y_row2, x_box4 + box_width, y_row2 + box_height_row2], 
                        radius=5, fill='white', outline="#8796EB", width=1)

# Load the icon
agent_threshold_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/Agent+Threshold.png"
try:
    response = requests.get(agent_threshold_icon_url)
    agent_threshold_icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    agent_threshold_icon_img = agent_threshold_icon_img.resize((18, 18), Image.LANCZOS)
except Exception as e:
    agent_threshold_icon_img = None

# Multi-line text
lines = ["Agent Performance", "thresholds (KPI)"]
text_gap = 6  # gap between icon and text
icon_w = 18
icon_h = 18

# Calculate text width and height
line_widths = [draw.textbbox((0, 0), line, font=font_small)[2] - draw.textbbox((0, 0), line, font=font_small)[0] for line in lines]
text_width = max(line_widths)
total_text_height = sum([draw.textbbox((0, 0), line, font=font_small)[3] - draw.textbbox((0, 0), line, font=font_small)[1] for line in lines])

total_content_width = icon_w + text_gap + text_width
content_x = x_box4 + (box_width - total_content_width) // 2
icon_x = content_x
icon_y = y_row2 + (box_height_row2 - icon_h) // 2

text_x = icon_x + icon_w + text_gap
text_y = y_row2 + (box_height_row2 - total_text_height) // 2

# Paste icon if loaded
if agent_threshold_icon_img:
    image.paste(agent_threshold_icon_img, (int(icon_x), int(icon_y)), agent_threshold_icon_img)
# Draw multi-line text
for i, line in enumerate(lines):
    bbox_line = draw.textbbox((0, 0), line, font=font_small)
    draw.text((int(text_x), int(text_y)), line, fill=color_black, font=font_small)
    text_y += bbox_line[3] - bbox_line[1]

draw.text((text_x, y_row2 + 13), "AI risk register", fill=color_black, font=font_small)
# Box 5 - AI risk register with icon
x_box5 = x_box4 + box_width + x_gap
draw_smooth_rounded_box(draw, [x_box5, y_row2, x_box5 + box_width, y_row2 + box_height_row2], 
                        radius=5, fill='white', outline="#8796EB", width=1)

# Load the icon
ai_risk_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/AI+Risk.png"
try:
    response = requests.get(ai_risk_icon_url)
    ai_risk_icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    ai_risk_icon_img = ai_risk_icon_img.resize((18, 18), Image.LANCZOS)
except Exception as e:
    ai_risk_icon_img = None

icon_margin_left = 8
icon_y = y_row2 + (box_height_row2 - 18) // 2
text_gap = 6  # gap between icon and text

bbox = draw.textbbox((0, 0), "AI risk register", font=font_small)
text_width = bbox[2] - bbox[0]
total_content_width = 18 + text_gap + text_width
content_x = x_box5 + (box_width - total_content_width) // 2
icon_x = content_x
text_x = icon_x + 18 + text_gap

if ai_risk_icon_img:
    image.paste(ai_risk_icon_img, (int(icon_x), int(icon_y)), ai_risk_icon_img)
draw.text((int(text_x), y_row2 + 13), "AI risk register", fill=color_black, font=font_small)

draw.text((text_x1, y_row2 + 6), "3rd party risk", fill=color_black, font=font_small)
draw.text((text_x2, y_row2 + 19), "management", fill=color_black, font=font_small)
# Box 6 - 3rd party risk management with icon
x_box6 = x_box5 + box_width + x_gap
draw_smooth_rounded_box(draw, [x_box6, y_row2, x_box6 + box_width, y_row2 + box_height_row2], 
                        radius=5, fill='white', outline="#8796EB", width=1)

# Load the icon
third_party_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/3rd+party+risk.png"
try:
    response = requests.get(third_party_icon_url)
    third_party_icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    third_party_icon_img = third_party_icon_img.resize((18, 18), Image.LANCZOS)
except Exception as e:
    third_party_icon_img = None

# Multi-line text
lines = ["3rd party risk", "management"]
text_gap = 6  # gap between icon and text
icon_w = 18
icon_h = 18

# Calculate text width and height
line_widths = [draw.textbbox((0, 0), line, font=font_small)[2] - draw.textbbox((0, 0), line, font=font_small)[0] for line in lines]
text_width = max(line_widths)
total_text_height = sum([draw.textbbox((0, 0), line, font=font_small)[3] - draw.textbbox((0, 0), line, font=font_small)[1] for line in lines])

total_content_width = icon_w + text_gap + text_width
content_x = x_box6 + (box_width - total_content_width) // 2
icon_x = content_x
icon_y = y_row2 + (box_height_row2 - icon_h) // 2

text_x = icon_x + icon_w + text_gap
text_y = y_row2 + (box_height_row2 - total_text_height) // 2

# Paste icon if loaded
if third_party_icon_img:
    image.paste(third_party_icon_img, (int(icon_x), int(icon_y)), third_party_icon_img)
# Draw multi-line text
for i, line in enumerate(lines):
    bbox_line = draw.textbbox((0, 0), line, font=font_small)
    draw.text((int(text_x), int(text_y)), line, fill=color_black, font=font_small)
    text_y += bbox_line[3] - bbox_line[1]

# ============================================================================
# SECTION 8: RIGHT BOX 1 - LLM Providers
# ============================================================================
draw_smooth_rounded_box(draw, right_box_1, radius=15, fill=color_gray_bg, outline="#B4C7E7", width=2)

title_text = "LLM Providers"
bbox = draw.textbbox((0, 0), title_text, font=font_title)
title_width = bbox[2] - bbox[0]
title_x = right_box_1[0] + ((right_box_1[2] - right_box_1[0]) - title_width) // 2
draw.text((title_x, right_box_1[1] + 10), title_text, fill=color_orange, font=font_title)

def draw_llm_compact_subboxes(parent_box, items, box_color, text_color, outline_color, font, y_offset):
    if not items:
        return y_offset  # Do nothing if items is empty

    sub_box_height = 26
    sub_box_vgap = 7
    sub_box_hgap = 7
    min_sub_box_width = 70
    max_sub_box_width = 110

    # Calculate widths for each item
    sub_box_widths = []
    for item in items:
        bbox = draw.textbbox((0, 0), item, font=font)
        width = min(max(bbox[2] - bbox[0] + 16, min_sub_box_width), max_sub_box_width)
        sub_box_widths.append(width)

    # Calculate how many boxes fit per row
    available_width = parent_box[2] - parent_box[0] - 40
    n = len(items)
    for boxes_per_row in range(n, 0, -1):
        row_width = sum(sorted(sub_box_widths, reverse=True)[:boxes_per_row]) + (boxes_per_row - 1) * sub_box_hgap
        if row_width <= available_width or boxes_per_row == 1:
            break

    # Arrange items into rows
    rows = []
    i = 0
    while i < n:
        row_count = min(boxes_per_row, n - i)
        rows.append(items[i:i + row_count])
        i += row_count

    # Calculate parent box height
    num_rows = len(rows)
    content_height = num_rows * sub_box_height + (num_rows - 1) * sub_box_vgap
    parent_height = content_height + 20  # Space for padding

    parent_box_xy = (
        parent_box[0] + 16,
        y_offset,
        parent_box[2] - 16,
        y_offset + parent_height
    )
    draw_rounded_rectangle(draw, parent_box_xy, radius=10, fill='white', outline=color_gray_border, width=1)

    # Draw sub-boxes in rows, centered
    y_start = parent_box_xy[1] + 10
    item_idx = 0

    for row in rows:
        row_widths = sub_box_widths[item_idx:item_idx + len(row)]
        row_total_width = sum(row_widths) + (len(row) - 1) * sub_box_hgap
        x_start = parent_box_xy[0] + ((parent_box_xy[2] - parent_box_xy[0]) - row_total_width) // 2

        for i, item in enumerate(row):
            w = row_widths[i]
            x1 = x_start
            y1 = y_start
            x2 = x1 + w
            y2 = y1 + sub_box_height

            draw_smooth_rounded_box(draw, (x1, y1, x2, y2), radius=8, fill=box_color, outline=outline_color, width=2)

            bbox_item = draw.textbbox((0, 0), item, font=font)
            text_x = x1 + (w - (bbox_item[2] - bbox_item[0])) // 2
            text_y = y1 + (sub_box_height - (bbox_item[3] - bbox_item[1])) // 2
            draw.text((text_x, text_y), item, fill=text_color, font=font)

            x_start += w + sub_box_hgap
            item_idx += 1

        y_start += sub_box_height + sub_box_vgap

    return parent_box_xy[3]

# --- LLM Providers sub-boxes ---
llm_items = usecase_json["usecaseDetails"]["baseModelName"]
next_y_llm = draw_llm_compact_subboxes(
    right_box_1, llm_items,
    box_color='#E8F4F8', text_color=color_blue, outline_color=color_blue,
    font=font_normal, y_offset=right_box_1[1] + 38
)

# Custom LLM - Parallelogram (below dynamic content)
para_y1 = next_y_llm + 15 if llm_items else right_box_1[1] + 60
para_y2 = para_y1 + 40
para_left_offset = 15

parallelogram_points = [
    (right_box_1[0] + 30 + para_left_offset, para_y1),
    (right_box_1[2] - 30 + para_left_offset, para_y1),
    (right_box_1[2] - 30, para_y2),
    (right_box_1[0] + 30, para_y2)
]

draw.polygon(parallelogram_points, fill='white', outline=color_blue)
for i in range(len(parallelogram_points)):
    start = parallelogram_points[i]
    end = parallelogram_points[(i + 1) % len(parallelogram_points)]
    draw.line([start, end], fill=color_blue, width=2)

custom_text = "Custom LLM"
bbox = draw.textbbox((0, 0), custom_text, font=font_normal)
custom_width = bbox[2] - bbox[0]
custom_x = right_box_1[0] + ((right_box_1[2] - right_box_1[0]) - custom_width) // 2 + 8
draw.text((custom_x, para_y1 + 14), custom_text, fill=color_black, font=font_normal)

# Fine Tuning - Rounded Rectangle
round_y1 = para_y2 + 20
round_y2 = round_y1 + 40
draw_smooth_rounded_box(draw, [right_box_1[0] + 30, round_y1, right_box_1[2] - 30, round_y2], 
                        radius=20, fill='white', outline=color_gray_border, width=1)
fine_text = "Fine Tuning"
bbox = draw.textbbox((0, 0), fine_text, font=font_normal)
fine_width = bbox[2] - bbox[0]
fine_x = right_box_1[0] + ((right_box_1[2] - right_box_1[0]) - fine_width) // 2
draw.text((fine_x, round_y1 + 14), fine_text, fill=color_black, font=font_normal)

# ============================================================================
# SECTION 9: RIGHT BOX 2 - Agent Development
# ============================================================================
draw_smooth_rounded_box(draw, right_box_2, radius=15, fill=color_gray_bg, outline="#B4C7E7", width=2)
draw.text((right_box_2[0] + 28, right_box_2[1] + 8), "Agent Development", fill=color_blue, font=font_title)

# --- Prompt Engineering box with icon ---
icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/Prompt+engineering.png"
try:
    response = requests.get(icon_url)
    icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    icon_img = icon_img.resize((22, 22), Image.LANCZOS)
except Exception as e:
    icon_img = None

box_x1 = right_box_2[0] + 15
box_y1 = right_box_2[1] + 52
box_x2 = right_box_2[2] - 15
box_y2 = right_box_2[1] + 77
draw_smooth_rounded_box(draw, [box_x1, box_y1, box_x2, box_y2], radius=6, fill='white', outline=color_gray_border, width=1)

icon_offset_x = 10
icon_offset_y = 3
text_offset_x = 40

if icon_img:
    image.paste(icon_img, (box_x1 + icon_offset_x, box_y1 + icon_offset_y), icon_img)
draw.text((box_x1 + text_offset_x, box_y1 + 8), "Prompt Engineering", fill=color_black, font=font_small)


# --- Prompt Tuning box with icon ---
prompt_tuning_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/Prompt+Tuning.png"
try:
    response = requests.get(prompt_tuning_icon_url)
    prompt_tuning_icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    prompt_tuning_icon_img = prompt_tuning_icon_img.resize((22, 22), Image.LANCZOS)
except Exception as e:
    prompt_tuning_icon_img = None

pt_box_x1 = right_box_2[0] + 15
pt_box_y1 = right_box_2[1] + 92
pt_box_x2 = right_box_2[2] - 15
pt_box_y2 = right_box_2[1] + 117
draw_smooth_rounded_box(draw, [pt_box_x1, pt_box_y1, pt_box_x2, pt_box_y2], radius=6, fill='white', outline=color_gray_border, width=1)

if prompt_tuning_icon_img:
    image.paste(prompt_tuning_icon_img, (pt_box_x1 + icon_offset_x, pt_box_y1 + icon_offset_y), prompt_tuning_icon_img)
draw.text((pt_box_x1 + text_offset_x, pt_box_y1 + 8), "- Prompt Tuning", fill=color_black, font=font_small)


# --- Code Generations box with icon ---
code_gen_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/Code+Generations.png"
try:
    response = requests.get(code_gen_icon_url)
    code_gen_icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    code_gen_icon_img = code_gen_icon_img.resize((22, 22), Image.LANCZOS)
except Exception as e:
    code_gen_icon_img = None

cg_box_x1 = right_box_2[0] + 15
cg_box_y1 = right_box_2[1] + 132
cg_box_x2 = right_box_2[2] - 15
cg_box_y2 = right_box_2[1] + 157
draw_smooth_rounded_box(draw, [cg_box_x1, cg_box_y1, cg_box_x2, cg_box_y2], radius=6, fill='white', outline=color_gray_border, width=1)

if code_gen_icon_img:
    image.paste(code_gen_icon_img, (cg_box_x1 + icon_offset_x, cg_box_y1 + icon_offset_y), code_gen_icon_img)
draw.text((cg_box_x1 + text_offset_x, cg_box_y1 + 8), "- Code Generations", fill=color_black, font=font_small)


# --- Model Evals box with icon ---
model_eval_icon_url = "https://fusefy-general.s3.us-east-1.amazonaws.com/generic-diagram/Model+Eval.png"
try:
    response = requests.get(model_eval_icon_url)
    model_eval_icon_img = Image.open(BytesIO(response.content)).convert("RGBA")
    model_eval_icon_img = model_eval_icon_img.resize((22, 22), Image.LANCZOS)
except Exception as e:
    model_eval_icon_img = None

me_box_x1 = right_box_2[0] + 15
me_box_y1 = right_box_2[1] + 172
me_box_x2 = right_box_2[2] - 15
me_box_y2 = right_box_2[1] + 197
draw_smooth_rounded_box(draw, [me_box_x1, me_box_y1, me_box_x2, me_box_y2], radius=6, fill='white', outline=color_gray_border, width=1)

if model_eval_icon_img:
    image.paste(model_eval_icon_img, (me_box_x1 + icon_offset_x, me_box_y1 + icon_offset_y), model_eval_icon_img)
draw.text((me_box_x1 + text_offset_x, me_box_y1 + 8), "- Model Evals", fill=color_black, font=font_small)

# Save the image locally first
# local_filename = 'architecture_diagram_with_content.png'
# image.save(local_filename, 'PNG', quality=95)

# =========================
# UPLOAD TO S3 FUNCTIONALITY
# =========================
def upload_image_to_s3(image, bucket_name, folder_name, object_name='architecture_diagram_with_content.png'):
    """Uploads the PIL image to S3 bucket/folder using boto3 (from memory)"""
    if not bucket_name:
        print("❌ S3 bucket name not provided in JSON.")
        return
    if not folder_name:
        print("❌ S3 folder name not provided in JSON.")
        return
    s3_key = f"{folder_name}/{object_name}"
    try:
        s3 = boto3.client('s3')
        img_bytes = BytesIO()
        image.save(img_bytes, format='PNG', quality=95)
        img_bytes.seek(0)
        s3.upload_fileobj(img_bytes, bucket_name, s3_key)
        print(f"✅ Architecture diagram uploaded to S3: s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"❌ Failed to upload to S3: {e}")

# Get S3 info from JSON
bucket_name = usecase_json.get("bucketName", "")
folder_name = usecase_json.get("folderName", "")

# Upload the image to S3
upload_image_to_s3(image, bucket_name, folder_name)

print("✅ Architecture diagram with smooth curved edges generated successfully!")
