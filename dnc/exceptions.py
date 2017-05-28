class OrganizationNotFound(Exception):
    def __init__(self):
        super(OrganizationNotFound, self).__init__('no organization for corresponding oid')


class ArticleNotFound(Exception):
    def __init__(self):
        super(ArticleNotFound, self).__init__('no article for corresponding oid and aid')
