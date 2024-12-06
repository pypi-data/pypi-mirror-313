import importlib
import json
import time
import requests


from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Type
from Illuminate.Collections.Collection import Collection
from Illuminate.Collections.helpers import collect
from Illuminate.Helpers.Util import Util
from Illuminate.Support.Str import Str
from Illuminate.Support.Facades.Route import Route
from Illuminate.Support.Facades.App import App
from Illuminate.Support.Facades.Config import Config
from Illuminate.Support.builtins import array_merge
from Illuminate.Support.helpers import with_
from djing.core.AuthorizesRequests import AuthorizesRequests
from djing.core.HandleRoutes import HandleRoutes
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Middlewares.RedirectIfAuthenticated import (
    RedirectIfAuthenticated,
)
from djing.core.InteractsWithEvents import InteractsWithEvents
from djing.core.Menu.Menu import Menu
from djing.core.PendingRouteRegistration import PendingRouteRegistration
from djing.core.Resource import Resource
from djing.core.ResourceCollection import ResourceCollection
from djing.core.Tool import Tool
from redis import Redis


class Djing(AuthorizesRequests, HandleRoutes, InteractsWithEvents):
    _main_menu_callback: Optional[Callable[[Any], Any]] = None
    _initial_path_callback: Optional[Callable[[Any], Any]] = None
    _sort_callback: Optional[Callable[[Any], Any]] = None
    _footer_callback: Optional[Callable[[Any], Any]] = None
    _with_authentication = False
    _with_breadcrumbs = False
    _global_search_enabled = True
    _resources: list = []
    _dashboards: list = []
    _tools: List[Tool] = []
    _json_variables: dict = {}
    _debounce = 0.5

    @classmethod
    def flush_state(cls):
        cls._main_menu_callback = None
        cls._initial_path_callback = None
        cls._sort_callback = None
        cls._footer_callback = None
        cls._with_authentication = False
        cls._with_breadcrumbs = False
        cls._global_search_enabled = True
        cls._resources = []
        cls._dashboards = []
        cls._tools = []
        cls._json_variables = {}
        cls._debounce = 0.5

    @classmethod
    def when_serving(cls, callback, default) -> Any:
        if App.bound(DjingRequest):
            return callback(App.make(DjingRequest))

        if callable(default):
            return default(App.make("request"))

    @classmethod
    def with_authentication(cls) -> "Djing":
        cls._with_authentication = True

        return cls()

    @classmethod
    def with_breadcrumbs(cls, with_breadcrumbs=True) -> Type["Djing"]:
        cls._with_breadcrumbs = with_breadcrumbs

        return cls

    @classmethod
    def breadcrumbs_enabled(cls) -> bool:
        status = (
            cls._with_breadcrumbs(App.make(DjingRequest))
            if callable(cls._with_breadcrumbs)
            else cls._with_breadcrumbs
        )

        return status

    @classmethod
    def without_global_search(cls) -> Type["Djing"]:
        cls._global_search_enabled = False

        return cls

    @classmethod
    def __resource_collection(cls) -> ResourceCollection:
        return ResourceCollection.make(cls._resources)

    @classmethod
    def authorized_resources(cls, request: DjingRequest) -> ResourceCollection:
        return cls.__resource_collection().authorized(request)

    @classmethod
    def globally_searchable_resources(
        cls, request: DjingRequest
    ) -> List[Tuple[Any, Any]]:
        return (
            cls.authorized_resources(request)
            .searchable()
            .sort_by(cls.sort_resources_with())
            .all()
        )

    @classmethod
    def has_globally_searchable_resources(cls) -> bool:
        return (
            collect(cls.globally_searchable_resources(App.make(DjingRequest))).count()
            > 0
        )

    @classmethod
    def main_menu(cls, callback: Callable[[Any], Any]) -> "Djing":
        cls._main_menu_callback = callback

        return cls()

    @classmethod
    def resolve_main_menu(cls, request: DjingRequest):
        default_main_menu = cls.default_main_menu(request)

        if cls._main_menu_callback:
            return Util.callback_with_dynamic_args(
                cls._main_menu_callback, [request, default_main_menu]
            )

        return default_main_menu

    @classmethod
    def default_main_menu(cls, request: DjingRequest):
        items = (
            with_(
                collect(cls.available_tools(request)),
                lambda tools: tools.map(lambda tool: tool.menu(request)),
            )
            .filter()
            .values()
            .all()
        )

        return Menu.make(items)

    @classmethod
    def logo(cls) -> Optional[str]:
        logo = Config.get("djing.brand_logo", None)

        logo_path = Path(logo) if logo else None

        if logo_path and logo_path.exists():
            return logo_path.read_text()

        return None

    @classmethod
    def brand_colors(cls) -> str:
        return (
            collect(Config.get("djing.brand_colors", None))
            .reject(lambda value, key: not value)
            .all()
        )

    @classmethod
    def username_field(cls) -> str:
        return Config.get("djing.auth.username_field", "username")

    @classmethod
    def path(cls) -> str:
        return Config.get("djing.path", "/djing-admin")

    @classmethod
    def base_directory(cls) -> str:
        return "djing_admin"

    @classmethod
    def app_directory(cls) -> str:
        return App.app_path("Djing")

    @classmethod
    def login_path(cls) -> str:
        path = cls.path()

        return f"{path}/login"

    @classmethod
    def initial_path(cls, callback: Callable[[Any], Any]) -> "Djing":
        cls._initial_path_callback = callback

        return cls()

    @classmethod
    def resolve_initial_path(cls, request: DjingRequest) -> str:
        initial_path = None

        if isinstance(cls._initial_path_callback, str):
            initial_path = cls._initial_path_callback

        if callable(cls._initial_path_callback):
            initial_path = cls._initial_path_callback(request)

        return initial_path if initial_path else "/dashboards/main"

    @classmethod
    def routes(cls):
        Route.alias_middleware("djing.guest", RedirectIfAuthenticated)

        return PendingRouteRegistration()

    @classmethod
    def tools(cls, tools: List[Tool]) -> "Djing":
        cls._tools = array_merge(cls._tools, tools)

        return cls()

    @classmethod
    def user(cls, request: DjingRequest):
        user = request.user()

        if user and user.is_authenticated:
            return user

        return None

    @classmethod
    def json_variables(cls, request: DjingRequest):
        items = (
            collect(cls._json_variables)
            .map(lambda item: item(request) if callable(item) else item)
            .all()
        )

        return items

    @classmethod
    def resource_information(cls, request: DjingRequest):
        def map_resources(resource: Type[Resource]):
            return {
                "uri_key": resource.uri_key(),
                "label": resource.label(),
                "singular_label": resource.singular_label(),
                "searchable": resource.is_searchable(),
                "per_page_options": resource.per_page_options(),
                "authorized_to_create": resource.authorized_to_create(request),
                "debound": resource.debounce * 1000,
            }

        collection = cls.__resource_collection()

        return collection.map(map_resources).values().all()

    @classmethod
    def footer(cls, callback: Callable[[Any], Any]) -> Type["Djing"]:
        cls._footer_callback = callback

        return cls

    @classmethod
    def default_footer(cls, request: DjingRequest):
        version = cls.version()
        year = datetime.now().year

        return f"""
            <p class="text-center">Powered by <a class="link-default" href="#">Djing</a> · v{version}</p>
            <p class="text-center">&copy; {year} Djing Inc.</p>
        """

    @classmethod
    def resolve_footer(cls, request: DjingRequest):
        if cls._footer_callback:
            return cls._footer_callback(request)

        return cls.default_footer(request)

    @classmethod
    def provide_to_script(cls, variables: Dict[str, Any]) -> "Djing":
        if not cls._json_variables:
            cls._json_variables = {
                "brand_logo": cls.logo(),
                "brand_colors": cls.brand_colors(),
                "auth": {
                    "username_field": cls.username_field(),
                },
                "with_authentication": cls._with_authentication,
                "breadcrumbs_enabled": cls.breadcrumbs_enabled(),
                "global_search_enabled": (
                    True
                    if cls._global_search_enabled
                    and cls.has_globally_searchable_resources()
                    else False
                ),
                "environment": App.make("env"),
                "base": Config.get("djing.path", "/djing-admin"),
                "debound": cls._debounce * 1000,
                "initial_path": lambda request: cls.resolve_initial_path(request),
                "login_path": cls.login_path(),
                "user_id": lambda request: (
                    cls.user(request).id if cls.user(request) else None
                ),
                "main_menu": lambda request: (
                    Menu.wrap(cls.resolve_main_menu(request))
                    if cls.user(request)
                    else []
                ),
                "resources": lambda request: cls.resource_information(request),
                "footer": lambda request: cls.resolve_footer(request),
            }

        cls._json_variables = array_merge(cls._json_variables, variables)

        return cls()

    @classmethod
    def version(cls):
        return "0.1.1"

    @classmethod
    def check_license_validity(cls) -> bool:
        status_code = cls.check_license()

        return status_code == 204

    @classmethod
    def update_license_info(
        cls,
        request: DjingRequest,
        cache: Redis,
        cache_key: str,
        cache_duration: timedelta,
    ) -> dict:
        try:
            response = requests.post(
                "http://proalgotrader.com/djing-api/license",
                {
                    "url": request.get_url(),
                    "key": Config.get("DJING_LICENSE_KEY", None),
                },
            )

            cache_data = {
                "status_code": response.status_code,
                "last_check": time.time(),
            }

            cache.set(cache_key, json.dumps(cache_data), cache_duration)

            return cache_data
        except Exception as e:
            raise e

    @classmethod
    def should_recheck(cls, cache_data: Any):
        last_check_time = datetime.fromtimestamp(cache_data.get("last_check"))

        return datetime.now() - last_check_time > timedelta(hours=24)

    @classmethod
    def check_license(cls) -> Tuple[str, bool]:
        request: DjingRequest = App.make("request")

        user = Djing.user(request)

        cache_key = f"license.{user}"

        cache_duration = timedelta(hours=24)

        cache = Redis(host="localhost", port=6379, db=0, decode_responses=True)

        cache_data_encoded: Any = cache.get(cache_key)

        cache_data = json.loads(cache_data_encoded) if cache_data_encoded else None

        if not cache_data or (cache_data and cls.should_recheck(cache_data)):
            cache_data = cls.update_license_info(
                request, cache, cache_key, cache_duration
            )

        return cache_data.get("status_code", 500)

    @classmethod
    def dashboards(cls, dashboards) -> "Djing":
        cls._dashboards = array_merge(cls._dashboards, dashboards)

        return cls()

    @classmethod
    def available_dashboards(cls, request: DjingRequest):
        items = (
            collect(cls._dashboards)
            .filter(lambda dashboard: dashboard.authorize(request))
            .all()
        )

        return items

    @classmethod
    def available_resources(cls, request: DjingRequest):
        collection = cls.authorized_resources(request)

        items = collection.sort(cls.sort_resources_with()).all()

        return items

    @classmethod
    def available_tools(cls, request: DjingRequest) -> List[Tool]:
        if not cls.user(request):
            return []

        return cls._tools

    @classmethod
    def boot_tools(cls, request: DjingRequest):
        collect(cls.available_tools(request)).each(lambda tool: tool.boot())

    @classmethod
    def resources(cls, resources) -> "Djing":
        cls._resources = array_merge(cls._resources, resources)

        return cls()

    @classmethod
    def all_available_dashboard_cards(cls, request: DjingRequest) -> Collection:
        items = (
            collect(cls._dashboards)
            .filter(lambda dashboard: dashboard.authorize(request))
            .flat_map(lambda dashboard: dashboard.cards())
            .unique()
            .filter(lambda dashboard: dashboard.authorize(request))
            .values()
        )

        return items

    @classmethod
    def resources_in(cls, resource_path: Path):
        try:
            app_path = str(resource_path).replace("/", ".")

            resources = []

            for module_path in resource_path.glob("*.py"):
                module_name = module_path.stem

                if module_name in ["Resource"]:
                    continue

                module = importlib.import_module(f"{app_path}.{module_name}")

                resource_class = getattr(module, module_name, None)

                if resource_class and issubclass(resource_class, Resource):
                    resources.append(resource_class)
                else:
                    raise Exception("Invalid resource class", module)

            cls.resources(collect(resources).sort().all())
        except Exception as e:
            print(e)

    @classmethod
    def humanize(cls, value) -> str:
        if isinstance(value, str):
            return Str.title(Str.snake(value, " "))

        return cls.humanize(value.__class__.__name__)

    @classmethod
    def grouped_resources_for_navigation(cls, request: DjingRequest):
        available_resources = cls.available_resources(request)

        return (
            ResourceCollection.make(available_resources)
            .grouped_for_navigation(request)
            .filter(lambda resource: resource.count())
        )

    @classmethod
    def sort_resources_by(cls, callback) -> "Djing":
        cls._sort_callback = callback

        return cls()

    @classmethod
    def sort_resources_with(cls):
        return (
            cls._sort_callback
            if cls._sort_callback
            else lambda resource: resource.label()
        )

    @classmethod
    def dashboard_for_key(cls, key, request: DjingRequest):
        return collect(cls._dashboards).first(
            lambda dashboard: dashboard.uri_key() == key
            and dashboard.authorize(request)
        )

    @classmethod
    def resource_for_key(cls, key):
        return cls.__resource_collection().first(
            lambda resource: resource.uri_key() == key
        )

    @classmethod
    def available_dashboard_cards_for_dashboard(cls, key, request: DjingRequest):
        def get_available_cards(dashboard):
            if not dashboard:
                return collect()

            return (
                collect(dashboard.cards())
                .filter(lambda card: card.authorize(request))
                .values()
            )

        return with_(cls.dashboard_for_key(key, request), get_available_cards)
