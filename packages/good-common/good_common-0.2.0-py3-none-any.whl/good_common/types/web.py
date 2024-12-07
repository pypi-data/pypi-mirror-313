from __future__ import annotations
from copy import deepcopy
import typing
from pydantic_core import Url
import tldextract
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from urllib.parse import urlencode, parse_qsl
from good_common.pipeline import Pipeline, Attribute
import courlan
import base64
from urllib.parse import urljoin
import orjson
from loguru import logger
from ._definitions import (
    DOMAIN_RULES,
    HTML_REDIRECT_DOMAINS,
    REGEXP_GLOBAL_CANONICAL_PARAMS,
    REGEXP_SHORT_URL_EXCLUSIONS,
    REGEXP_TRACKING_PARAMS,
    REGEXP_TRACKING_VALUES,
    SHORT_URL_PROVIDERS,
    SITE_STRUCTURE,
    VALID_DOMAIN_PORT,
    FILE_TYPE,
    ADULT_AND_VIDEOS,
    ALL_PATH_LANGS,
    ALL_PATH_LANGS_NO_TRAILING,
    HOST_LANG_FILTER,
    NAVIGATION_FILTER,
    NOTCRAWLABLE,
    INDEX_PAGE_FILTER,
)


class UrlParseConfig(typing.NamedTuple):
    remove_auth: bool = True
    remove_fragment: bool = True
    remove_standard_port: bool = True
    resolve_embedded_redirects: bool = False
    embedded_redirect_params = {"redirect", "redirect_to", "url"}
    canonical_params = {"id", "q", "v", "chash", "action"}
    force_https: bool = True
    short_url_exception_domains = {
        "fec.gov",
        "archive.is",
        "archive.org",
        "archive.today",
        "archive.ph",
    }


_default_config = UrlParseConfig()


class URL(str):
    _strict: bool = False
    __clickhouse_type__: typing.ClassVar[str] = "String"
    _url: Url

    @classmethod
    def build(
        cls,
        *,
        scheme: str,
        username: str | None = None,
        password: str | None = None,
        host: str,
        port: int | None = None,
        path: str | None = None,
        query: str
        | list[tuple[str, str]]
        | dict[str, str]
        | dict[str, tuple[str]]
        | None = None,
        # flat_delimiter: str = ',',
        fragment: str | None = None,
    ) -> typing.Self:
        _query = {}

        if isinstance(query, str) and len(query) > 0:
            _query = parse_qsl(query)

        elif isinstance(query, dict):
            # _query = {k: query[k] for k in sorted(query.keys())}
            _query = {k: query[k] for k in sorted(query.keys())}

        elif isinstance(query, list):
            _query = sorted(query, key=lambda x: x[0])

        _url = Url.build(
            scheme=scheme,
            username=username,
            password=password,
            host=host,
            port=port,
            path=path.lstrip("/") if path else None,
            query=urlencode(_query) if _query else None,
            fragment=fragment,
        )
        return cls(_url.unicode_string())

    def __new__(cls, url: str, strict: bool = False):
        _url = Url(url)
        instance = super().__new__(cls, _url.unicode_string())
        instance._url = _url
        instance._strict = strict
        return instance

    def __str__(self) -> str:
        return super().__str__()

    def join(self, *paths):
        _paths = ([self.path] if self.path else []) + list(paths)
        return URL.build(
            scheme=self.scheme,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            path="/".join(_paths),
            query=self.query_params(format="plain"),
            fragment=self.fragment,
        )

    def update(
        self,
        *,
        scheme: str | None = None,
        username: str | None = None,
        password: str | None = None,
        host: str | None = None,
        port: int | None = None,
        path: str | None = None,
        query: dict[str, typing.Any] | None = None,
        fragment: str | None = None,
    ):
        def _format_val(val):
            if isinstance(val, str) or isinstance(val, int) or isinstance(val, float):
                return val
            elif isinstance(val, list):
                return ",".join(val)
            else:
                return orjson.dumps(val).decode()

        # format query-string
        if query is not None:
            query = {
                k: _format_val(v) for k, v in sorted(query.items(), key=lambda x: x[0])
            }
        else:
            query = self.query_params(format="dict")

        return URL.build(
            scheme=scheme or self.scheme,
            username=username or self.username,
            password=password or self.password,
            host=host or self.host,
            port=port or self.port,
            path=path or self.path,
            query=query,
            fragment=fragment or self.fragment,
        )

    @classmethod
    def from_base_url(cls, base_url: str, url: str) -> URL:
        return URL(urljoin(base_url, url))

    @property
    def scheme(self) -> str:
        return self._url.scheme

    @property
    def username(self) -> str | None:
        return self._url.username

    @property
    def password(self) -> str | None:
        return self._url.password

    @property
    def host(self) -> str:
        if not self._url.host:
            if self._strict:
                raise ValueError("Host is not present in the URL")
            else:
                return ""
        return self._url.host

    @property
    def root_domain(self):
        return tldextract.extract(self.host).registered_domain

    @property
    def host_no_www(self) -> str:
        if self.host.startswith("www."):
            return self.host[4:]
        return self.host

    @property
    def unicode_host(self) -> str | None:
        return self._url.unicode_host()

    @property
    def port(self) -> int | None:
        return self._url.port

    @property
    def path(self) -> str:
        return self._url.path or ""

    @property
    def query(self) -> str:
        return self._url.query or ""

    @property
    def fragment(self) -> str | None:
        return self._url.fragment

    def query_params(
        self,
        format: typing.Literal["plain", "dict", "flattened"] = "plain",
        flat_delimiter: str = ",",
    ) -> list[tuple[str, str]] | dict[str, tuple[str]] | dict[str, str]:
        _params = self._url.query_params()
        if format == "plain":
            return _params
        else:
            _output = {}
            for key, value in _params:
                if key not in _output:
                    _output[key] = []
                _output[key].append(value)

            if format == "dict":
                return {key: tuple(value) for key, value in _output.items()}
            else:
                return {
                    key: flat_delimiter.join(value) if len(value) > 1 else value[0]
                    for key, value in _output.items()
                }

        return _params

    def unicode_string(self) -> str:
        return self._url.unicode_string()

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: typing.Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))

    def clean(self, config: UrlParseConfig = UrlParseConfig()) -> URL:
        return _url_cleaning_pipeline.run_sync(url=self, config=config).url

    def canonicalize(
        self, config: UrlParseConfig = UrlParseConfig(resolve_embedded_redirects=True)
    ) -> URL:
        if self.scheme in ("http", "https"):
            _url = _url_canonicalization_pipeline.run_sync(
                url=self, config=config
            ).url.clean()

            if _url.scheme == "http":
                _url = URL.build(
                    scheme="https",
                    host=_url.host_no_www,
                    path=_url.path,
                    query=_url.query,
                )
            return _url
        return self

    def is_short_url(self) -> bool:
        return any(
            provider == self.host
            for provider in SHORT_URL_PROVIDERS | HTML_REDIRECT_DOMAINS
        )

    def is_html_redirect(self) -> bool:
        return self.host in HTML_REDIRECT_DOMAINS

    def is_possible_short_url(self) -> bool:
        if self.path is None:
            return False
        if self.is_short_url():
            return True
        return all(
            [
                (
                    (len(self.host.replace(".", "")) < 10)
                    or (self.host.endswith(".link"))
                    or (self.host.startswith("on."))
                    or (self.host.startswith("go."))
                    or (self.host.startswith("l."))
                ),
                self.host not in _default_config.short_url_exception_domains,
                len(self.path.strip("/")) < 10,
                self.path.count("/") == 1,
            ]
        ) and not REGEXP_SHORT_URL_EXCLUSIONS.match(self.host)

    def is_adult(self) -> bool:
        return bool(ADULT_AND_VIDEOS.search(self))

    def is_homepage(self) -> bool:
        return bool(INDEX_PAGE_FILTER.match(self.path)) or self.path == "/"

    def is_not_crawlable(self) -> bool:
        return bool(NOTCRAWLABLE.search(self))

    def is_navigation_page(self) -> bool:
        return bool(NAVIGATION_FILTER.search(self))

    def is_valid_url(self) -> bool:
        return courlan.filters.is_valid_url(self)

    def lang_filter(
        self,
        language: str | None = None,
        strict: bool = False,
        trailing_slash: bool = True,
    ) -> bool:
        return courlan.filters.lang_filter(
            self, language=language, strict=strict, trailing_slash=trailing_slash
        )

    def type_filter(
        self,
        strict: bool = False,
        with_nav: bool = False,
    ) -> bool:
        return courlan.filters.type_filter(self, strict=strict, with_nav=with_nav)


def _basic_clean(
    url: URL, config: UrlParseConfig
) -> typing.Annotated[URL, Attribute("url")]:
    _query = url.query_params(format="plain")
    return URL.build(
        scheme=url.scheme.lower() if not config.force_https else "https",
        username=url.username if not config.remove_auth else None,
        password=url.password if not config.remove_auth else None,
        host=url.host.lower(),
        port=url.port
        if url.port != 80 and url.port != 443 and not config.remove_standard_port
        else None,
        path=url.path,
        query=_query,
        fragment=url.fragment if not config.remove_fragment else None,
    )


def _domain_specific_url_rewrites(
    url: URL, config: UrlParseConfig
) -> typing.Annotated[URL, Attribute("url")]:
    """
    Some domains have predictable URL redirect structures that do not require resolving the URL.
    """
    match url:
        case URL(host="youtu.be", path=path) if path is not None:
            return URL.build(
                scheme="https",
                host="www.youtube.com",
                path="/watch",
                query=[("v", path[1:])],
            )

        case URL(host="discord.gg", path=path) if path is not None:
            return URL.build(
                scheme="https",
                host="discord.com",
                path="/invite/" + path[1:],
            )

        case URL(host="twitter.com", path=path) if path is not None:
            return URL.build(
                scheme="https",
                host="x.com",
                path=path[1:],
                query=url.query_params(format="plain"),
            )

    return url


def _resolve_embedded_redirects(url: URL, config: UrlParseConfig) -> URL:
    """
    Resolve embedded redirects in URLs.
    """
    query = url.query_params(format="flattened")
    no_www_domain = url.host.lstrip("www.")

    keys_of_interest = set()
    if config.resolve_embedded_redirects:
        keys_of_interest = config.embedded_redirect_params

    match (no_www_domain, query):
        case ("facebook.com", {"u": [u]}):
            return URL(u)

        case ("google.com", {"url": [u]}):
            return URL(u)

        case (str() as host, dict() as target_dict):
            for key, value in target_dict.items():
                if key in keys_of_interest:
                    if isinstance(value, str):
                        value = tuple([value])
                    for v in value:
                        if v.startswith("http"):
                            return URL(v)
                        elif v.startswith("//"):
                            return URL.build(
                                scheme=url.scheme,
                                host=host,
                                path=v[2:],
                            )
                        elif "/" not in value and isinstance(value, str):
                            try:
                                return URL(base64.urlsafe_b64decode(value).decode())
                            except Exception:
                                pass
                    # if value.startswith("http"):
                    #     return URL(value)
                    # elif value.startswith("//"):
                    #     return URL.build(
                    #         scheme=url.scheme,
                    #         host=host,
                    #         path=value[2:],
                    #     )
                    # elif "/" not in value and isinstance(value, str):
                    #     try:
                    #         return URL(base64.urlsafe_b64decode(value).decode())
                    #     except Exception:
                    #         pass
                    # else:
                    #     return URL.build(
                    #         scheme=url.scheme,
                    #         host=host,
                    #         path=value,
                    #     )

                    # return URL(value)

    return url


def _filter_canonical_params(url: URL, config: UrlParseConfig) -> URL:
    non_canonical_params = set()

    _config = deepcopy(config)

    domain_rules = DOMAIN_RULES[url.host] or {}

    if domain_rules.get("disable"):
        return url
    if domain_rules.get("canonical"):
        _config.canonical_params.update(domain_rules["canonical"])
    if domain_rules.get("non_canonical"):
        non_canonical_params.update(domain_rules["non_canonical"])
    if domain_rules.get("force_www") and not url.host.startswith("www."):
        _host = f"www.{url.host}"

    new_query_params = []

    for key, value in url.query_params(format="plain"):
        if key in _config.canonical_params:
            new_query_params.append((key, value))

        elif REGEXP_GLOBAL_CANONICAL_PARAMS.match(key) or (
            key not in non_canonical_params
            and not REGEXP_TRACKING_PARAMS.match(key)
            and not REGEXP_TRACKING_VALUES.match(value)
        ):
            new_query_params.append((key, value))
        else:
            pass

    return URL.build(
        scheme=url.scheme,
        username=url.username,
        password=url.password,
        host=url.host,
        port=url.port,
        path=url.path,
        query=new_query_params,
        fragment="",
    )


_url_cleaning_pipeline = Pipeline(_basic_clean, _domain_specific_url_rewrites)

_url_canonicalization_pipeline = Pipeline(
    _basic_clean,
    _domain_specific_url_rewrites,
    _resolve_embedded_redirects,
    _filter_canonical_params,
)


def to_url(url: str | URL) -> URL:
    if isinstance(url, URL):
        return url
    return URL(url)


__all__ = ["URL", "to_url"]
