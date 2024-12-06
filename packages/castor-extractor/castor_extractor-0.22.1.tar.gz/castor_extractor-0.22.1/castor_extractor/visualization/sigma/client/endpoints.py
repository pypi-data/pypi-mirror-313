class SigmaEndpointFactory:
    """Wrapper class around all endpoints we're using"""

    DATASETS = "datasets"
    FILES = "files"
    MEMBERS = "members"
    WORKBOOKS = "workbooks"

    @classmethod
    def authentication(cls) -> str:
        return "v2/auth/token"

    @classmethod
    def datasets(cls) -> str:
        return f"v2/{cls.DATASETS}"

    @classmethod
    def elements(cls, workbook_id: str, page_id: str) -> str:
        return f"v2/{cls.WORKBOOKS}/{workbook_id}/pages/{page_id}/elements"

    @classmethod
    def files(cls) -> str:
        return f"v2/{cls.FILES}"

    @classmethod
    def lineage(cls, workbook_id: str, element_id: str) -> str:
        return f"v2/{cls.WORKBOOKS}/{workbook_id}/lineage/elements/{element_id}"

    @classmethod
    def members(cls) -> str:
        return f"v2/{cls.MEMBERS}"

    @classmethod
    def pages(cls, workbook_id: str) -> str:
        return f"v2/{cls.WORKBOOKS}/{workbook_id}/pages"

    @classmethod
    def queries(cls, workbook_id: str) -> str:
        return f"v2/{cls.WORKBOOKS}/{workbook_id}/queries"

    @classmethod
    def workbooks(cls) -> str:
        return f"v2/{cls.WORKBOOKS}"
