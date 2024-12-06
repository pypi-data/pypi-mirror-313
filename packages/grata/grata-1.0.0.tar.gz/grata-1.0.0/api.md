# Shared Types

```python
from grata.types import CompanyDetailed
```

# Bulk

Methods:

- <code title="post /api/v1.4/bulk/enrich/">client.bulk.<a href="./src/grata/resources/bulk.py">enrich</a>(\*\*<a href="src/grata/types/bulk_enrich_params.py">params</a>) -> <a href="./src/grata/types/shared/company_detailed.py">CompanyDetailed</a></code>

# Enrich

Methods:

- <code title="post /api/v1.4/enrich/">client.enrich.<a href="./src/grata/resources/enrich.py">create</a>(\*\*<a href="src/grata/types/enrich_create_params.py">params</a>) -> <a href="./src/grata/types/shared/company_detailed.py">CompanyDetailed</a></code>

# Lists

Methods:

- <code title="post /api/v1.4/lists/">client.lists.<a href="./src/grata/resources/lists.py">create</a>(\*\*<a href="src/grata/types/list_create_params.py">params</a>) -> <a href="./src/grata/types/shared/company_detailed.py">CompanyDetailed</a></code>
- <code title="get /api/v1.4/lists/{list_uid}/">client.lists.<a href="./src/grata/resources/lists.py">retrieve</a>(list_uid) -> <a href="./src/grata/types/shared/company_detailed.py">CompanyDetailed</a></code>
- <code title="patch /api/v1.4/lists/{list_uid}/">client.lists.<a href="./src/grata/resources/lists.py">update</a>(list_uid, \*\*<a href="src/grata/types/list_update_params.py">params</a>) -> <a href="./src/grata/types/shared/company_detailed.py">CompanyDetailed</a></code>
- <code title="get /api/v1.4/lists/">client.lists.<a href="./src/grata/resources/lists.py">list</a>(\*\*<a href="src/grata/types/list_list_params.py">params</a>) -> <a href="./src/grata/types/shared/company_detailed.py">CompanyDetailed</a></code>
- <code title="delete /api/v1.4/lists/{list_uid}/">client.lists.<a href="./src/grata/resources/lists.py">delete</a>(list_uid) -> None</code>
- <code title="post /api/v1.4/lists/{list_uid}/companies/">client.lists.<a href="./src/grata/resources/lists.py">companies</a>(list_uid, \*\*<a href="src/grata/types/list_companies_params.py">params</a>) -> <a href="./src/grata/types/shared/company_detailed.py">CompanyDetailed</a></code>

# Search

Types:

```python
from grata.types import CompanyBasic
```

Methods:

- <code title="post /api/v1.4/search/">client.search.<a href="./src/grata/resources/search.py">create</a>(\*\*<a href="src/grata/types/search_create_params.py">params</a>) -> <a href="./src/grata/types/company_basic.py">CompanyBasic</a></code>
- <code title="post /api/v1.4/search-similar/">client.search.<a href="./src/grata/resources/search.py">similar</a>(\*\*<a href="src/grata/types/search_similar_params.py">params</a>) -> <a href="./src/grata/types/company_basic.py">CompanyBasic</a></code>
