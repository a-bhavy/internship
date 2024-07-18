class MongoDB:
    def _init_(self):
        self.client = None
        self.db = None
        self.collection = None

    def init_app(self, client):
        self.client = client
        self.db = self.client.get_database('internship')
        self.collection = self.db['resumes']

db = MongoDB()