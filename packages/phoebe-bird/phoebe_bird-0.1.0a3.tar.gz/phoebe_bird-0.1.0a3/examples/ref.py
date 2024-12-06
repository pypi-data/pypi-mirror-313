import os

from phoebe_bird import Phoebe

client = Phoebe(
    api_key=os.environ.get("EBIRD_API_KEY"),
)


def ref() -> None:
    hotspot = client.ref.hotspot.info.retrieve("L99381")
    print(hotspot)

    speciesGroups = client.ref.taxonomy.species_groups.list("ebird")
    print(speciesGroups)

    locales = client.ref.taxonomy.locales.list()
    print(locales)


ref()
