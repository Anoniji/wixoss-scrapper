from helpers.ClassAsDict import classAsDict


class Image:
    def __init__(self, image_src_url=None, image_path=None):
        self.image_src_url = image_src_url
        self.image_path = image_path

    def asDict(self):
        classAsDict(self)

