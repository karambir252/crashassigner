class InvalidLineNumberException(Exception):
    pass


class FileContent:
    def __init__(self, data):
        self.data = data
        self.lines = data['text'].splitlines()

    def get_line_code(self, line_number):
        if line_number < 0 or line_number > len(self.lines):
            raise InvalidLineNumberException(line_number)
        return self.lines[line_number-1]

    def get_number_of_lines(self):
        return len(self.lines)
