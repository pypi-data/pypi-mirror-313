# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel
from .shared.workspace import Workspace

__all__ = ["UpdateWorkspaceResponse"]


class UpdateWorkspaceResponse(BaseModel):
    data: Workspace
