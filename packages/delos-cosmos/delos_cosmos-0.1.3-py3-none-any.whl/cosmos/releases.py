"""Data structure for the different versions of the API."""

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel

from .endpoints import CosmosEndpoints, Endpoints


class Release(Enum):
    """Enum for the different versions of the API."""

    V1 = "v1"


class CosmosClientReleases(BaseModel):
    """Data structure for the different versions of the API."""

    version: Release
    release_date: datetime
    details: dict[str, Any]
    suffix: str
    available_endpoints: list[CosmosEndpoints]


first_release = CosmosClientReleases(
    version=Release.V1,
    details={
        "version": "v1",
        "release_date": "2024-11-20",
        "description": "Initial release of the API",
    },
    release_date=datetime(year=2024, month=11, day=20, tzinfo=UTC),
    suffix="/api/v1",
    available_endpoints=[
        Endpoints.STATUS.HEALTH,
        Endpoints.TRANSLATE.TRANSLATE_TEXT,
        Endpoints.TRANSLATE.TRANSLATE_FILE,
        Endpoints.WEB.SEARCH,
        Endpoints.FILES.PARSER,
        Endpoints.FILES.INDEX_CREATE,
        Endpoints.FILES.INDEX_ADD_FILES,
        Endpoints.FILES.INDEX_DELETE_FILES,
        Endpoints.FILES.INDEX_DELETE,
        Endpoints.FILES.INDEX_RESTORE,
        Endpoints.FILES.INDEX_ASK,
        Endpoints.FILES.INDEX_EMBED,
        Endpoints.FILES.INDEX_LIST,
        Endpoints.FILES.INDEX_DETAILS,
        Endpoints.LLM.CHAT,
        Endpoints.LLM.EMBED,
    ],
)

AllReleases: list[CosmosClientReleases] = []
AllReleases.append(first_release)
