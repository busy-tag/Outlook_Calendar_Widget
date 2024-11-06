class Event:
    def __init__(self, event_id, subject, start, start_date, end, categories, color=None, color_code=None):
        self.event_id = event_id
        self.subject = subject
        self.start = start
        self.start_date = start_date
        self.end = end
        self.categories = categories
        self.color = color
        self.color_code = color_code

    def __repr__(self):
        return f"Event(subject={self.subject}, start={self.start}, start_date={self.start_date}, end={self.end}, categories={self.categories}, color={self.color}, color_code={self.color_code})"