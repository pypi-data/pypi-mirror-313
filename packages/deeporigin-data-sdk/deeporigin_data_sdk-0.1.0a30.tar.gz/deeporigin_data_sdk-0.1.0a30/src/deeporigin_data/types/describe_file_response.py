# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel
from .shared.file import File

__all__ = ["DescribeFileResponse"]


class DescribeFileResponse(BaseModel):
    data: File
