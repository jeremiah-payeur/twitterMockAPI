

class Tweet:

    def __init__(self, user, text, time=None, id=None):
        """Initialize object with text and user id"""
        self.text = text
        self.user = user
        self.time = time
        self.id = id
        return


class Follow:

    def __init__(self, user, follow):
        """Initialize following object to insert into table"""
        self.user = user
        self.follow = follow
        return