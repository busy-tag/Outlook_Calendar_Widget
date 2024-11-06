import json

PRESET_COLOR_MAPPING = {
    "preset0": "#E33D47",  # Red
    "preset1": "#FE6F13",  # Orange
    "preset2": "#765534",  # Brown
    "preset3": "#FEE634",  # Yellow
    "preset4": "#37BD16",  # Green
    "preset5": "#469997",  # Teal
    "preset6": "#6D823C",  # Olive
    "preset7": "#5259FB",  # Blue
    "preset8": "#DA13FE",  # Purple
    "preset9": "#903B57",  # Cranberry
    "preset10": "#9B9B9D",  # Steel
    "preset11": "#505050",  # DarkSteel
    "preset12": "#808080",  # Gray
    "preset13": "#3C3D41",  # DarkGray
    "preset14": "#040404",  # Black
    "preset15": "#E33D47",  # DarkRed
    "preset16": "#F28A31",  # DarkOrange
    "preset17": "#A0744D",  # DarkBrown
    "preset18": "#FFC407",  # DarkYellow
    "preset19": "#3B7333",  # DarkGreen
    "preset20": "#13FEF3",  # DarkTeal
    "preset21": "#35592C",  # DarkOlive
    "preset22": "#5544C4",  # DarkBlue
    "preset23": "#6C357C",  # DarkPurple
    "preset24": "#F42BD6",  # DarkCranberry
}

def load_color_mapping(file_path='color_mapping.json'):
    with open(file_path, 'r') as f:
        return json.load(f)