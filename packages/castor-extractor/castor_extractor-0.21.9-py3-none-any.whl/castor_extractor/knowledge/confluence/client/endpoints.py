class ConfluenceEndpointFactory:
    """
    Confluence rest api v2 endpoint factory.
    https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#about
    """

    API = "wiki/api/v2/"
    PAGES = "pages"
    USERS = "users-bulk"

    @classmethod
    def pages(cls) -> str:
        """
        Endpoint to fetch all pages.
        More: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-get
        """
        return f"{cls.API}{cls.PAGES}"

    @classmethod
    def users(cls) -> str:
        """
        Endpoint to fetch all user.
        More: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-user/#api-users-bulk-post
        """
        return f"{cls.API}{cls.USERS}"
