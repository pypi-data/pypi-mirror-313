# Data

## Observations

Types:

```python
from phoebe_bird.types.data import Observation
```

### Recent

Types:

```python
from phoebe_bird.types.data.observations import RecentListResponse
```

Methods:

- <code title="get /data/obs/{regionCode}/recent">client.data.observations.recent.<a href="./src/phoebe_bird/resources/data/observations/recent/recent.py">list</a>(region_code, \*\*<a href="src/phoebe_bird/types/data/observations/recent_list_params.py">params</a>) -> <a href="./src/phoebe_bird/types/data/observations/recent_list_response.py">RecentListResponse</a></code>

#### Notable

Types:

```python
from phoebe_bird.types.data.observations.recent import NotableListResponse
```

Methods:

- <code title="get /data/obs/{regionCode}/recent/notable">client.data.observations.recent.notable.<a href="./src/phoebe_bird/resources/data/observations/recent/notable.py">list</a>(region_code, \*\*<a href="src/phoebe_bird/types/data/observations/recent/notable_list_params.py">params</a>) -> <a href="./src/phoebe_bird/types/data/observations/recent/notable_list_response.py">NotableListResponse</a></code>

#### Species

Types:

```python
from phoebe_bird.types.data.observations.recent import SpecieRetrieveResponse
```

Methods:

- <code title="get /data/obs/{regionCode}/recent/{speciesCode}">client.data.observations.recent.species.<a href="./src/phoebe_bird/resources/data/observations/recent/species.py">retrieve</a>(species_code, \*, region_code, \*\*<a href="src/phoebe_bird/types/data/observations/recent/specie_retrieve_params.py">params</a>) -> <a href="./src/phoebe_bird/types/data/observations/recent/specie_retrieve_response.py">SpecieRetrieveResponse</a></code>

#### Historic

Types:

```python
from phoebe_bird.types.data.observations.recent import HistoricListResponse
```

Methods:

- <code title="get /data/obs/{regionCode}/historic/{y}/{m}/{d}">client.data.observations.recent.historic.<a href="./src/phoebe_bird/resources/data/observations/recent/historic.py">list</a>(d, \*, region_code, y, m, \*\*<a href="src/phoebe_bird/types/data/observations/recent/historic_list_params.py">params</a>) -> <a href="./src/phoebe_bird/types/data/observations/recent/historic_list_response.py">HistoricListResponse</a></code>

### Geo

#### Recent

Types:

```python
from phoebe_bird.types.data.observations.geo import RecentListResponse
```

Methods:

- <code title="get /data/obs/geo/recent">client.data.observations.geo.recent.<a href="./src/phoebe_bird/resources/data/observations/geo/recent/recent.py">list</a>(\*\*<a href="src/phoebe_bird/types/data/observations/geo/recent_list_params.py">params</a>) -> <a href="./src/phoebe_bird/types/data/observations/geo/recent_list_response.py">RecentListResponse</a></code>

##### Species

Types:

```python
from phoebe_bird.types.data.observations.geo.recent import SpecieListResponse
```

Methods:

- <code title="get /data/obs/geo/recent/{speciesCode}">client.data.observations.geo.recent.species.<a href="./src/phoebe_bird/resources/data/observations/geo/recent/species.py">list</a>(species_code, \*\*<a href="src/phoebe_bird/types/data/observations/geo/recent/specie_list_params.py">params</a>) -> <a href="./src/phoebe_bird/types/data/observations/geo/recent/specie_list_response.py">SpecieListResponse</a></code>

##### Notable

Types:

```python
from phoebe_bird.types.data.observations.geo.recent import NotableListResponse
```

Methods:

- <code title="get /data/obs/geo/recent/notable">client.data.observations.geo.recent.notable.<a href="./src/phoebe_bird/resources/data/observations/geo/recent/notable.py">list</a>(\*\*<a href="src/phoebe_bird/types/data/observations/geo/recent/notable_list_params.py">params</a>) -> <a href="./src/phoebe_bird/types/data/observations/geo/recent/notable_list_response.py">NotableListResponse</a></code>

### Nearest

#### GeoSpecies

Types:

```python
from phoebe_bird.types.data.observations.nearest import GeoSpecieListResponse
```

Methods:

- <code title="get /data/nearest/geo/recent/{speciesCode}">client.data.observations.nearest.geo_species.<a href="./src/phoebe_bird/resources/data/observations/nearest/geo_species.py">list</a>(species_code, \*\*<a href="src/phoebe_bird/types/data/observations/nearest/geo_specie_list_params.py">params</a>) -> <a href="./src/phoebe_bird/types/data/observations/nearest/geo_specie_list_response.py">GeoSpecieListResponse</a></code>

# Product

## Lists

Types:

```python
from phoebe_bird.types.product import ListRetrieveResponse
```

Methods:

- <code title="get /product/lists/{regionCode}">client.product.lists.<a href="./src/phoebe_bird/resources/product/lists/lists.py">retrieve</a>(region_code, \*\*<a href="src/phoebe_bird/types/product/list_retrieve_params.py">params</a>) -> <a href="./src/phoebe_bird/types/product/list_retrieve_response.py">ListRetrieveResponse</a></code>

### Historical

Types:

```python
from phoebe_bird.types.product.lists import HistoricalRetrieveResponse
```

Methods:

- <code title="get /product/lists/{regionCode}/{y}/{m}/{d}">client.product.lists.historical.<a href="./src/phoebe_bird/resources/product/lists/historical.py">retrieve</a>(d, \*, region_code, y, m, \*\*<a href="src/phoebe_bird/types/product/lists/historical_retrieve_params.py">params</a>) -> <a href="./src/phoebe_bird/types/product/lists/historical_retrieve_response.py">HistoricalRetrieveResponse</a></code>

## Top100

Types:

```python
from phoebe_bird.types.product import Top100RetrieveResponse
```

Methods:

- <code title="get /product/top100/{regionCode}/{y}/{m}/{d}">client.product.top100.<a href="./src/phoebe_bird/resources/product/top100.py">retrieve</a>(d, \*, region_code, y, m, \*\*<a href="src/phoebe_bird/types/product/top100_retrieve_params.py">params</a>) -> <a href="./src/phoebe_bird/types/product/top100_retrieve_response.py">Top100RetrieveResponse</a></code>

## Stats

Types:

```python
from phoebe_bird.types.product import StatRetrieveResponse
```

Methods:

- <code title="get /product/stats/{regionCode}/{y}/{m}/{d}">client.product.stats.<a href="./src/phoebe_bird/resources/product/stats.py">retrieve</a>(d, \*, region_code, y, m) -> <a href="./src/phoebe_bird/types/product/stat_retrieve_response.py">StatRetrieveResponse</a></code>

## SpeciesList

Types:

```python
from phoebe_bird.types.product import SpeciesListListResponse
```

Methods:

- <code title="get /product/spplist/{regionCode}">client.product.species_list.<a href="./src/phoebe_bird/resources/product/species_list.py">list</a>(region_code) -> <a href="./src/phoebe_bird/types/product/species_list_list_response.py">SpeciesListListResponse</a></code>

## Checklist

Types:

```python
from phoebe_bird.types.product import ChecklistViewResponse
```

Methods:

- <code title="get /product/checklist/view/{subId}">client.product.checklist.<a href="./src/phoebe_bird/resources/product/checklist.py">view</a>(sub_id) -> <a href="./src/phoebe_bird/types/product/checklist_view_response.py">ChecklistViewResponse</a></code>

# Ref

## Region

### Adjacent

Types:

```python
from phoebe_bird.types.ref.region import AdjacentListResponse
```

Methods:

- <code title="get /ref/adjacent/{regionCode}">client.ref.region.adjacent.<a href="./src/phoebe_bird/resources/ref/region/adjacent.py">list</a>(region_code) -> <a href="./src/phoebe_bird/types/ref/region/adjacent_list_response.py">AdjacentListResponse</a></code>

### Info

Types:

```python
from phoebe_bird.types.ref.region import InfoRetrieveResponse
```

Methods:

- <code title="get /ref/region/info/{regionCode}">client.ref.region.info.<a href="./src/phoebe_bird/resources/ref/region/info.py">retrieve</a>(region_code, \*\*<a href="src/phoebe_bird/types/ref/region/info_retrieve_params.py">params</a>) -> <a href="./src/phoebe_bird/types/ref/region/info_retrieve_response.py">InfoRetrieveResponse</a></code>

### List

Types:

```python
from phoebe_bird.types.ref.region import ListListResponse
```

Methods:

- <code title="get /ref/region/list/{regionType}/{parentRegionCode}">client.ref.region.list.<a href="./src/phoebe_bird/resources/ref/region/list.py">list</a>(parent_region_code, \*, region_type, \*\*<a href="src/phoebe_bird/types/ref/region/list_list_params.py">params</a>) -> <a href="./src/phoebe_bird/types/ref/region/list_list_response.py">ListListResponse</a></code>

## Hotspot

Types:

```python
from phoebe_bird.types.ref import HotspotListResponse
```

Methods:

- <code title="get /ref/hotspot/{regionCode}">client.ref.hotspot.<a href="./src/phoebe_bird/resources/ref/hotspot/hotspot.py">list</a>(region_code, \*\*<a href="src/phoebe_bird/types/ref/hotspot_list_params.py">params</a>) -> <a href="./src/phoebe_bird/types/ref/hotspot_list_response.py">HotspotListResponse</a></code>

### Geo

Types:

```python
from phoebe_bird.types.ref.hotspot import GeoRetrieveResponse
```

Methods:

- <code title="get /ref/hotspot/geo">client.ref.hotspot.geo.<a href="./src/phoebe_bird/resources/ref/hotspot/geo.py">retrieve</a>(\*\*<a href="src/phoebe_bird/types/ref/hotspot/geo_retrieve_params.py">params</a>) -> <a href="./src/phoebe_bird/types/ref/hotspot/geo_retrieve_response.py">GeoRetrieveResponse</a></code>

### Info

Types:

```python
from phoebe_bird.types.ref.hotspot import InfoRetrieveResponse
```

Methods:

- <code title="get /ref/hotspot/info/{locId}">client.ref.hotspot.info.<a href="./src/phoebe_bird/resources/ref/hotspot/info.py">retrieve</a>(loc_id) -> <a href="./src/phoebe_bird/types/ref/hotspot/info_retrieve_response.py">InfoRetrieveResponse</a></code>

## Taxonomy

### Ebird

Types:

```python
from phoebe_bird.types.ref.taxonomy import EbirdRetrieveResponse
```

Methods:

- <code title="get /ref/taxonomy/ebird">client.ref.taxonomy.ebird.<a href="./src/phoebe_bird/resources/ref/taxonomy/ebird.py">retrieve</a>(\*\*<a href="src/phoebe_bird/types/ref/taxonomy/ebird_retrieve_params.py">params</a>) -> <a href="./src/phoebe_bird/types/ref/taxonomy/ebird_retrieve_response.py">EbirdRetrieveResponse</a></code>

### Forms

Types:

```python
from phoebe_bird.types.ref.taxonomy import FormListResponse
```

Methods:

- <code title="get /ref/taxon/forms/{speciesCode}">client.ref.taxonomy.forms.<a href="./src/phoebe_bird/resources/ref/taxonomy/forms.py">list</a>(species_code) -> <a href="./src/phoebe_bird/types/ref/taxonomy/form_list_response.py">FormListResponse</a></code>

### Locales

Types:

```python
from phoebe_bird.types.ref.taxonomy import LocaleListResponse
```

Methods:

- <code title="get /ref/taxa-locales/ebird">client.ref.taxonomy.locales.<a href="./src/phoebe_bird/resources/ref/taxonomy/locales.py">list</a>() -> <a href="./src/phoebe_bird/types/ref/taxonomy/locale_list_response.py">LocaleListResponse</a></code>

### Versions

Types:

```python
from phoebe_bird.types.ref.taxonomy import VersionListResponse
```

Methods:

- <code title="get /ref/taxonomy/versions">client.ref.taxonomy.versions.<a href="./src/phoebe_bird/resources/ref/taxonomy/versions.py">list</a>() -> <a href="./src/phoebe_bird/types/ref/taxonomy/version_list_response.py">VersionListResponse</a></code>

### SpeciesGroups

Types:

```python
from phoebe_bird.types.ref.taxonomy import SpeciesGroupListResponse
```

Methods:

- <code title="get /ref/sppgroup/{speciesGrouping}">client.ref.taxonomy.species_groups.<a href="./src/phoebe_bird/resources/ref/taxonomy/species_groups.py">list</a>(species_grouping, \*\*<a href="src/phoebe_bird/types/ref/taxonomy/species_group_list_params.py">params</a>) -> <a href="./src/phoebe_bird/types/ref/taxonomy/species_group_list_response.py">SpeciesGroupListResponse</a></code>
