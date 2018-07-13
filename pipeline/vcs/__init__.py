class Git():
    def __init__(self, repo):
        self.__repo = repo

    def get_highest_tag(self):
        tag_names = list(map(lambda tag: tag.name, self.__repo.tags))
        sorted_tags = list(reversed(tag_names))
        return sorted_tags[0]