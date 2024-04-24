class Restriction:
    def __init__(self, program_name, allowed_time, time_span, usage_time):
        self.program_name = program_name
        self.allowed_time = allowed_time
        self.time_span = time_span
        self.usage_time = usage_time

class TimeLimit:
    def __init__(self, start_time, end_time, allowed_time, time_span):
        self.start_time = start_time
        self.end_time = end_time
        self.allowed_time = allowed_time
        self.time_span = time_span

class ChildData:
    def __init__(self, parent_email, child_name, restrictions, time_limit):
        self.parent_email = parent_email
        self.child_name = child_name
        self.restrictions = restrictions
        self.time_limit = time_limit


class ParentData:
    def __init__(self, email, name):
        self.email = email
        self.name = name
