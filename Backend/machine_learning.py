import random

def determine_color():
    colors = ["blue", "red", "green", "yellow", "brown", "purple", "black", "white"]
    data = {
        "top_color": random.choice(colors),
        "bottom_color": random.choice(colors),
    }
    return data

def determine_employee_id():
    employee_id = 2
    data = {
        "employee_id": employee_id
    }
    return {"data": data, "status": "success"}

# # Example usage
# captured_colors = determine_color()
# print(captured_colors['top_color'])
