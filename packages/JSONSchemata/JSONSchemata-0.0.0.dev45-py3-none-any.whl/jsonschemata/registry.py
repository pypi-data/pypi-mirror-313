from typing import Callable as _Callable
import referencing as _referencing
from referencing import jsonschema as _ref_jsonschema, retrieval as _ref_retrieval
import pkgdata as _pkgdata
import pyserials as _ps
import pylinks as _pl

from jsonschemata import edit as _edit


def make(
    dynamic: bool = False,
    crawl: bool = True,
    add_resources: list[dict | _referencing.Resource | tuple[str, dict | _referencing.Resource]] | None = None,
    add_resources_default_spec: _referencing.Specification = _ref_jsonschema.DRAFT202012,
    retrieval_func: _Callable[[str], str | _referencing.Resource] = None,
) -> _referencing.Registry:
    """Create a registry of all JSON schemas.

    Parameters
    ----------
    dynamic : bool, default: False
        If True, any reference that is not found in the registry will be
        [dynamically retrieved](https://referencing.readthedocs.io/en/stable/intro/#dynamically-retrieving-resources)
        and [cached](https://referencing.readthedocs.io/en/stable/intro/#caching).
        The retrieval works as follows:
        If the reference URI starts with "http" or "https", the URI is fetched using an HTTP GET request.
        Otherwise, the URI is assumed to be a local filepath,
        which can be either absolute or relative to the current working directory.
        You can also provide a custom retrieval function using the `retrieval_func` parameter.
    crawl : bool, default: True
        Pre [crawl](https://referencing.readthedocs.io/en/stable/api/#referencing.Registry.crawl)
        all resources so that the registry is
        [fully ready](https://referencing.readthedocs.io/en/stable/schema-packages/).
    add_resources: list[dict | referencing.Resource | tuple[str, dict | referencing.Resource]] | None, default: None
        A list of additional resources to add to the registry. Each resource can be a dictionary or
        a [`referencing.Resource`](https://referencing.readthedocs.io/en/stable/api/#referencing.Resource)
        object. If a resource does not have an "$id",
        the ID must be provided along with the resource as a tuple of (ID, resource).
    add_resources_default_spec: referencing.Specification, default: referencing.jsonschema.DRAFT202012
        The default specification to use when creating an additional resource from a dictionary.
    retrieval_func: Callable[[str], str | referencing.Resource], optional
        A custom retrieval function to use when `dynamic` is True.
        The function should take a URI as input and return the reference schema.
        If you want the retrieval function to also cache the retrieved references,
        the function must be decorated with the
        [`@referencing.retrieval.to_cached_resource`](https://referencing.readthedocs.io/en/stable/api/#referencing.retrieval.to_cached_resource)
        decorator, in which case the function must return the reference schema as a JSON string
        (cf. [Referencing Docs](https://referencing.readthedocs.io/en/stable/intro/#caching)).
        If the decorator is not used, the function must return the schema as a `referencing.Resource` instead.
        Note that this retrieval function will only be used when `dynamic` is set to `True`.
    Returns
    -------
    referencing.Registry
        A [`referencing.Registry`](https://referencing.readthedocs.io/en/stable/api/#referencing.Registry)
        object containing all resources.
    """

    @_ref_retrieval.to_cached_resource()
    def retrieve_url(uri: str) -> str:
        if uri.startswith(("http://", "https://")):
            return _pl.http.request(url=uri, response_type="str")
        return _ps.write.to_json_string(_ps.read.from_file(path=uri, toml_as_dict=True), sort_keys=False)

    schema_dir_path = _pkgdata.get_package_path_from_caller(top_level=True) / "_data"
    resources = []
    for schema_filepath in schema_dir_path.glob("**/*.yaml"):
        schema_dict = _ps.read.yaml_from_file(path=schema_filepath)
        _edit.required_last(schema_dict)
        schema = _referencing.Resource.from_contents(
            schema_dict, default_specification=_ref_jsonschema.DRAFT202012
        )
        resources.append(schema)

    id_resources: list[tuple[str, _referencing.Resource]] = []
    for add_resource in add_resources or []:
        resource_id = None
        if isinstance(add_resource, dict):
            add_resource = _referencing.Resource.from_contents(
                add_resource, default_specification=add_resources_default_spec
            )
        elif isinstance(add_resource, tuple):
            resource_id, resource_dict = add_resource
            add_resource = _referencing.Resource.from_contents(
                resource_dict, default_specification=add_resources_default_spec,
            )
        if resource_id:
            id_resources.append((resource_id, add_resource))
        else:
            resources.append(add_resource)

    registry = _referencing.Registry(
        retrieve=retrieval_func or retrieve_url
    ) if dynamic else _referencing.Registry()
    registry = resources @ registry
    if id_resources:
        registry = registry.with_resources(id_resources)
    if crawl:
        registry.crawl()
    return registry
