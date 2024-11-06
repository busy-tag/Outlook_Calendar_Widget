class OutlookCalendar:
    def __init__(self, name, color, hex_color, owner_name, owner_address, calendar_id):
        self.name = name
        self.color = color
        self.hex_color = hex_color
        self.owner_name = owner_name
        self.owner_address = owner_address
        self.id = calendar_id

    def __repr__(self):
        return (f"OutlookCalendar(Name: {self.name}, Color: {self.color}, Hex Color: {self.hex_color}, "
                f"Owner: {self.owner_name}, Owner Email: {self.owner_address}, ID: {self.id})")