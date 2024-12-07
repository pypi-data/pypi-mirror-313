from .._sdk import client
from .._sdk.assess_metadata import AssessMetadata


def fetch_assess_model(model_id: str) -> AssessMetadata:
    response = client.httpx_client.get(f"/assess/models/{model_id}/")
    if not response.is_success:
        raise ValueError(f"Unable to fetch assess metadata for {model_id}: {response.content}")
    assess_metadata = AssessMetadata.from_data(response.json()["definition"]).or_die()

    return assess_metadata
