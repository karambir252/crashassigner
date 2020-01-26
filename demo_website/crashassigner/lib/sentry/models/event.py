class SentryEvent:
    def __init__(self, data):
        self.data = data
        self.id = data['id']
        self.metadata = data['metadata']
        self.dateCreated = data['dateCreated']
        self.title = data['title']
        self.type = data['type']
        self.user = data['user']

        # others
        self.filename = self.metadata['filename']

    def _get_error_data(self):
        return self.data['entries'][0]['data']['values'][0]['stacktrace']['frames'][-1]

    def get_file_full_path(self):
        error_data = self._get_error_data()
        return error_data['absPath']

    def get_crashed_line_number(self):
        error_data = self._get_error_data()
        return error_data['lineNo']

    def _get_context_lines(self):
        error_data = self._get_error_data()
        return error_data['context']

    def get_crashed_line_code(self):
        context = self._get_context_lines()
        crashed_line_number = self.get_crashed_line_number()
        for c in context:
            if c[0] == crashed_line_number:
                return ''.join(c[1:])

    def get_crashed_context_code(self):
        context = self._get_context_lines()
        return '\n'.join(
            ''.join(c[1:])
            for c in context
        )
