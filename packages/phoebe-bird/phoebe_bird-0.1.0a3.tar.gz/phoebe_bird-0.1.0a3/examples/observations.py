import os

from phoebe_bird import Phoebe

client = Phoebe(
    api_key=os.environ.get("EBIRD_API_KEY"),
)


def observations() -> None:
    phoebes = client.data.observations.recent.species.retrieve("easpho", region_code="US-NY")

    print(phoebes)

    recent_checklists = client.data.observations.recent.list("US-NY")

    print(recent_checklists)


observations()
