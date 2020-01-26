class GithubBlame:
    def __init__(self, data):
        self.data = data
        self.ranges = data['ranges']
    
    def get_line_author(self, line_number):
        for file_range in self.ranges:
            if file_range['startingLine'] <= line_number <= file_range['endingLine']:
                return file_range['commit']['author']['user']['login']