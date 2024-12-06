from __future__ import annotations

from collections.abc import Callable, Collection, Mapping, MutableMapping, Sequence
from typing import Annotated, Final, Literal, final, overload
from uuid import uuid4

import pandas as pd
from pydantic import Field
from typing_extensions import override

from ._aggregate_providers import AggregateProviders
from ._arrow_utils import get_data_types_from_arrow
from ._atoti_client import AtotiClient
from ._base_scenario_name import BASE_SCENARIO_NAME as _BASE_SCENARIO_NAME
from ._check_named_object_defined import check_named_object_defined
from ._collections import frozendict
from ._constant import Constant, ConstantValue
from ._context import Context
from ._data_type import DataType, is_temporal_type
from ._default_query_timeout import DEFAULT_QUERY_TIMEOUT as _DEFAULT_QUERY_TIMEOUT
from ._doc import doc
from ._docs_utils import QUERY_KWARGS as _QUERY_KWARGS
from ._generate_mdx import generate_mdx
from ._graphql_client import CreateJoinInput
from ._identification import (
    CubeIdentifier,
    HasIdentifier,
    HierarchyIdentifier,
    Identifier,
    IdentifierT_co,
    LevelIdentifier,
    MeasureIdentifier,
    TableIdentifier,
)
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._live_extension_unavailable_error import LiveExtensionUnavailableError
from ._masking.masking import Masking
from ._masking.masking_config import MaskingConfig
from ._pandas_utils import pandas_to_arrow
from ._query_explanation import QueryExplanation
from ._query_filter import QueryFilter
from ._shared_context import SharedContext
from ._stringify_mdx import stringify_mdx
from ._typing import Duration
from .agg import single_value
from .aggregate_provider import AggregateProvider
from .aggregates_cache import AggregatesCache
from .column import Column
from .hierarchies import Hierarchies
from .level import Level
from .levels import Levels
from .mdx_query_result import MdxQueryResult
from .measure import Measure
from .measures import Measures
from .table import Table

_DEFAULT_DATE_HIERARCHY_LEVELS = frozendict({"Year": "y", "Month": "M", "Day": "d"})


@final
class Cube(HasIdentifier[CubeIdentifier], ReprJsonable):
    """Cube of a :class:`~atoti.Session`."""

    def __init__(
        self,
        identifier: CubeIdentifier,
        /,
        *,
        atoti_client: AtotiClient,
        get_widget_creation_code: Callable[[], str | None],
        java_api: JavaApi | None,
        session_id: str,
    ):
        self._atoti_client: Final = atoti_client
        self._get_widget_creation_code: Final = get_widget_creation_code
        self.__identifier: Final = identifier
        self.__java_api: Final = java_api
        self._session_id: Final = session_id

    @property
    @override
    def _identifier(self) -> CubeIdentifier:
        return self.__identifier

    @property
    def _fact_table_identifier(self) -> TableIdentifier:
        assert self._atoti_client._graphql_client
        cube = check_named_object_defined(
            self._atoti_client._graphql_client.get_cube_fact_table(
                cube_name=self.name,
            ).data_model.cube,
            "cube",
            self.name,
        )
        return TableIdentifier(cube.fact_table.name)

    @property
    def _java_api(self) -> JavaApi:
        if self.__java_api is None:
            raise LiveExtensionUnavailableError
        return self.__java_api

    @property
    def name(self) -> str:
        """Name of the cube."""
        return self._identifier.cube_name

    @property
    def hierarchies(self) -> Hierarchies:
        """Hierarchies of the cube."""
        return Hierarchies(
            atoti_client=self._atoti_client,
            cube_identifier=self._identifier,
            java_api=self.__java_api,
        )

    @property
    def levels(self) -> Levels:
        """Levels of the cube."""
        return Levels(
            atoti_client=self._atoti_client,
            cube_identifier=self._identifier,
            hierarchies=self.hierarchies,
            java_api=self.__java_api,
        )

    @property
    def measures(self) -> Measures:
        """Measures of the cube."""
        return Measures(
            atoti_client=self._atoti_client,
            cube_identifier=self._identifier,
            java_api=self.__java_api,
        )

    @property
    def aggregates_cache(self) -> AggregatesCache:
        """Aggregates cache of the cube."""
        return AggregatesCache(
            cube_identifier=self._identifier,
            get_capacity=self._java_api.get_aggregates_cache_capacity,
            set_capacity=self._java_api.set_aggregates_cache_capacity,
        )

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            {
                "Dimensions": self.hierarchies._repr_json_()[0],
                "Measures": self.measures._repr_json_()[0],
            },
            {"expanded": False, "root": self.name},
        )

    @property
    def shared_context(self) -> MutableMapping[str, str]:
        """Context values shared by all the users.

        Context values can also be set at query time, and per user, directly from the UI.
        The values in the shared context are the default ones for all the users.

        * ``queriesTimeLimit``

          The number of seconds after which a running query is cancelled and its resources reclaimed.
          Set to ``-1`` to remove the limit.
          Defaults to 30 seconds.

        * ``queriesResultLimit.intermediateLimit``

          The limit number of point locations for a single intermediate result.
          This works as a safe-guard to prevent queries from consuming too much memory, which is especially useful when going to production with several simultaneous users on the same server.
          Set to ``-1`` to remove the limit.

          Defaults to ``1_000_000`` if :ref:`ATOTI_LICENSE is set <how_tos/unlock_all_features:Declaring the ATOTI_LICENSE environment variable>`, and to no limit otherwise.

        * ``queriesResultLimit.transientLimit``

          Similar to *intermediateLimit* but across all the intermediate results of the same query.
          Set to ``-1`` to remove the limit.

          Defaults to ``10_000_000`` if :ref:`ATOTI_LICENSE is set <how_tos/unlock_all_features:Declaring the ATOTI_LICENSE environment variable>`, and to no limit otherwise.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("London", 240.0),
            ...         ("New York", 270.0),
            ...         ("Paris", 200.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(
            ...     df,
            ...     keys={"City"},
            ...     table_name="shared_context example",
            ... )
            >>> cube = session.create_cube(table)
            >>> cube.shared_context["queriesTimeLimit"] = 60
            >>> cube.shared_context["queriesResultLimit.intermediateLimit"] = 1000000
            >>> cube.shared_context["queriesResultLimit.transientLimit"] = 10000000
            >>> cube.shared_context
            {'queriesTimeLimit': '60', 'queriesResultLimit.transientLimit': '10000000', 'queriesResultLimit.intermediateLimit': '1000000'}

        """
        return SharedContext(cube_name=self.name, java_api=self._java_api)

    # Before making this public:
    # - Fix the security hole: values are masked on cube queries but can be requested with the database REST API.
    # - Make it consistent with the way `session.restrictions` are persisted.
    #   The restrictions are stored in the Content Server.
    #   Value masking is a similar concept.
    #   They should either be both stored in the Content Server or both kept in memory.
    # - Replacing `MaskingConfig(only=h1.isin(("foo",), exclude=h2.isin(("bar",))` with:
    #   `h1.isin(("foo",)) & ~h2.isin(("bar"),)`.
    # - Implementing `Masking._get_delegate()` and `Masking._delete_delegate_keys()` .
    @property
    def _value_masking(self) -> MutableMapping[str, MaskingConfig]:
        """Masking configuration.

        Masking configuration is used to hide sensitive data from users who do not have the required permissions to see it.
         It is applied to the cube's hierarchy members. Measures will return ``"No Access"`` for the members that are masked.

        Example:
            >>> session = tt.Session.start()
            >>> df = pd.DataFrame(
            ...     columns=["City", "Price", "Currency"],
            ...     data=[
            ...         ("London", 100, "GBP"),
            ...         ("Paris", 200, "EUR"),
            ...         ("Berlin", 300, "EUR"),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, keys={"City"}, table_name="cities")
            >>> cube = session.create_cube(table, name="Cube")
            >>> h = cube.hierarchies
            >>> cube._value_masking["ROLE_USER"] = MaskingConfig(
            ...     only=None,
            ...     exclude=h["City"].isin(("Paris",)),
            ... )
            >>> mdx = "SELECT NON EMPTY { [contributors.COUNT] } ON COLUMNS, NON EMPTY { cities.City.ALL.AllMember, cities.City.ALL.AllMember.Paris, cities.City.ALL.AllMember.London, cities.City.ALL.AllMember.Berlin } ON ROWS FROM [Cube]"
            >>> session.query_mdx(mdx)
                   contributors.COUNT
            City
            Paris           No Access
            London                  1
            Berlin                  1

            .. doctest::
                :hide:

                >>> del session

        """
        return Masking(cube_name=self.name, java_api=self._java_api)

    @property
    def aggregate_providers(self) -> MutableMapping[str, AggregateProvider]:
        return AggregateProviders(cube_name=self.name, java_api=self._java_api)

    def _join_distributed_cluster(
        self,
        *,
        application_name: str,
        query_cube_name: str,
        query_cube_url: str,
        query_cube_port: int | None,
        data_cube_url: str | None,
        data_cube_port: int | None,
        discovery_protocol_xml: str | None,
    ) -> None:
        """Join the distributed cluster at the given address for the given distributed cube."""
        self._java_api.join_distributed_cluster(
            application_name=application_name,
            query_cube_name=query_cube_name,
            query_cube_url=query_cube_url,
            query_cube_port=query_cube_port,
            data_cube_name=self.name,
            data_cube_url=data_cube_url,
            data_cube_port=data_cube_port,
            discovery_protocol_xml=discovery_protocol_xml,
        )
        self._java_api.refresh()

    def _get_data_types(
        self,
        identifiers: Collection[IdentifierT_co],
        /,
    ) -> dict[IdentifierT_co, DataType]:
        def get_data_type(identifier: Identifier, /) -> DataType:
            if isinstance(identifier, LevelIdentifier):
                return (
                    "String"
                    if identifier
                    == LevelIdentifier(HierarchyIdentifier("Epoch", "Epoch"), "Branch")
                    else self.levels[identifier.key].data_type
                )

            assert isinstance(identifier, MeasureIdentifier)
            measure = self.measures.get(identifier.measure_name)
            # The passed identifier can correspond to a calculated measure for which the type is unknown.
            return "Object" if measure is None else measure.data_type

        return {identifier: get_data_type(identifier) for identifier in identifiers}

    @overload
    def query(
        self,
        *measures: Measure,
        context: Context = ...,
        explain: Literal[False] = ...,
        filter: QueryFilter | None = ...,
        include_empty_rows: bool = ...,
        include_totals: bool = ...,
        levels: Sequence[Level] = (),
        mode: Literal["pretty"] = ...,
        scenario: str = ...,
        timeout: Duration = ...,
    ) -> MdxQueryResult: ...

    @overload
    def query(
        self,
        *measures: Measure,
        context: Context = ...,
        explain: Literal[False] = ...,
        filter: QueryFilter | None = ...,
        include_empty_rows: bool = ...,
        include_totals: bool = ...,
        levels: Sequence[Level] = (),
        mode: Literal["pretty", "raw"] = ...,
        scenario: str = ...,
        timeout: Duration = ...,
    ) -> pd.DataFrame: ...

    @overload
    def query(
        self,
        *measures: Measure,
        context: Context = ...,
        explain: Literal[True],
        filter: QueryFilter | None = ...,
        include_empty_rows: bool = ...,
        include_totals: bool = ...,
        levels: Sequence[Level] = (),
        mode: Literal["pretty", "raw"] = ...,
        scenario: str = ...,
        timeout: Duration = ...,
    ) -> QueryExplanation: ...

    @doc(
        **_QUERY_KWARGS,
        keys_argument='{"Continent", "Country", "Currency", "Year", "Month"}',
    )
    def query(
        self,
        *measures: Measure,
        context: Context = frozendict(),
        explain: bool = False,
        filter: QueryFilter | None = None,  # noqa: A002
        include_empty_rows: bool = False,
        include_totals: bool = False,
        levels: Sequence[Level] = (),
        mode: Literal["pretty", "raw"] = "pretty",
        scenario: str | None = None,
        timeout: Duration = _DEFAULT_QUERY_TIMEOUT,
    ) -> MdxQueryResult | pd.DataFrame | QueryExplanation:
        """Execute and MDX query.

        {widget_conversion}

        Args:
            measures: The measures to query.
            {context}
            {explain}
            filter: The filtering condition.

                Example:
                    .. doctest::
                        :hide:

                        >>> session = getfixture("default_session")

                    >>> df = pd.DataFrame(
                    ...     columns=["Continent", "Country", "Currency", "Year", "Month", "Price"],
                    ...     data=[
                    ...         ("Europe", "France", "EUR", 2023, 10, 200.0),
                    ...         ("Europe", "Germany", "EUR", 2024, 2, 150.0),
                    ...         ("Europe", "United Kingdom", "GBP", 2022, 10, 120.0),
                    ...         ("America", "United states", "USD", 2020, 5, 240.0),
                    ...         ("America", "Mexico", "MXN", 2021, 3, 270.0),
                    ...     ],
                    ... )
                    >>> table = session.read_pandas(
                    ...     df,
                    ...     keys={keys_argument},
                    ...     table_name="Prices",
                    ... )
                    >>> cube = session.create_cube(table)
                    >>> del cube.hierarchies["Continent"]
                    >>> del cube.hierarchies["Country"]
                    >>> cube.hierarchies["Geography"] = [
                    ...     table["Continent"],
                    ...     table["Country"],
                    ... ]
                    >>> del cube.hierarchies["Year"]
                    >>> del cube.hierarchies["Month"]
                    >>> cube.hierarchies["Date"] = [
                    ...     table["Year"],
                    ...     table["Month"],
                    ... ]
                    >>> cube.measures["American Price"] = tt.where(
                    ...     cube.levels["Continent"] == "America",
                    ...     cube.measures["Price.SUM"],
                    ... )
                    >>> h, l, m = cube.hierarchies, cube.levels, cube.measures

                    Single equality condition:

                    >>> cube.query(
                    ...     m["Price.SUM"],
                    ...     levels=[l["Country"]],
                    ...     filter=l["Continent"] == "Europe",
                    ... )
                                             Price.SUM
                    Continent Country
                    Europe    France            200.00
                              Germany           150.00
                              United Kingdom    120.00

                    Combined equality condition:

                    >>> cube.query(
                    ...     m["Price.SUM"],
                    ...     levels=[l["Country"], l["Currency"]],
                    ...     filter=((l["Continent"] == "Europe") & (l["Currency"] == "EUR")),
                    ... )
                                               Price.SUM
                    Continent Country Currency
                    Europe    France  EUR         200.00
                              Germany EUR         150.00

                    Hierarchy condition:

                    >>> cube.query(
                    ...     m["Price.SUM"],
                    ...     levels=[l["Country"]],
                    ...     filter=h["Geography"].isin(("America",), ("Europe", "Germany")),
                    ... )
                                            Price.SUM
                    Continent Country
                    America   Mexico           270.00
                              United states    240.00
                    Europe    Germany          150.00

                    Inequality condition:

                    >>> cube.query(
                    ...     m["Price.SUM"],
                    ...     levels=[l["Country"], l["Currency"]],
                    ...     # Equivalent to `filter=(l["Currency"] != "GBP") & (l["Currency"] != "MXN")`
                    ...     filter=~l["Currency"].isin("GBP", "MXN"),
                    ... )
                                                     Price.SUM
                    Continent Country       Currency
                    America   United states USD         240.00
                    Europe    France        EUR         200.00
                              Germany       EUR         150.00
                    >>> cube.query(
                    ...     m["Price.SUM"],
                    ...     levels=[l["Year"]],
                    ...     filter=l["Year"] >= 2022,
                    ... )
                         Price.SUM
                    Year
                    2022    120.00
                    2023    200.00
                    2024    150.00

                    Deep level of a multilevel hierarchy condition:

                    >>> cube.query(
                    ...     m["Price.SUM"],
                    ...     levels=[l["Month"]],
                    ...     filter=l["Month"] == 10,
                    ... )
                               Price.SUM
                    Year Month
                    2022 10       120.00
                    2023 10       200.00

            include_empty_rows: Whether to keep the rows where all the requested measures have no value.

                Example:
                    >>> cube.query(
                    ...     m["American Price"],
                    ...     levels=[l["Continent"]],
                    ...     include_empty_rows=True,
                    ... )
                              American Price
                    Continent
                    America           510.00
                    Europe

            include_totals: Whether to query the grand total and subtotals and keep them in the returned DataFrame.
                {totals}

                Example:
                    >>> cube.query(
                    ...     m["Price.SUM"],
                    ...     levels=[l["Country"], l["Currency"]],
                    ...     include_totals=True,
                    ... )
                                                      Price.SUM
                    Continent Country        Currency
                    Total                                980.00
                    America                              510.00
                              Mexico                     270.00
                                             MXN         270.00
                              United states              240.00
                                             USD         240.00
                    Europe                               470.00
                              France                     200.00
                                             EUR         200.00
                              Germany                    150.00
                                             EUR         150.00
                              United Kingdom             120.00
                                             GBP         120.00

            levels: The levels to split on.
                If ``None``, the value of the measures at the top of the cube is returned.
            {mode}

              {pretty}

                Example:
                    >>> cube.query(
                    ...     m["Price.SUM"],
                    ...     levels=[l["Continent"]],
                    ...     mode="pretty",
                    ... )
                              Price.SUM
                    Continent
                    America      510.00
                    Europe       470.00

              {raw}

                Example:
                    >>> cube.query(
                    ...     m["Price.SUM"],
                    ...     levels=[l["Continent"]],
                    ...     mode="raw",
                    ... )
                      Continent  Price.SUM
                    0   America      510.0
                    1    Europe      470.0

            scenario: The name of the scenario to query.
            {timeout}

        See Also:
            :meth:`atoti.Session.query_mdx`

        """
        level_identifiers = [level._identifier for level in levels]
        measure_identifiers = [measure._identifier for measure in measures]

        if explain:
            cube_discovery = self._atoti_client.get_cube_discovery()
            mdx_ast = generate_mdx(
                cube=cube_discovery.cubes[self.name],
                filter=filter,
                include_empty_rows=include_empty_rows,
                include_totals=include_totals,
                level_identifiers=level_identifiers,
                measure_identifiers=measure_identifiers,
                scenario=scenario,
            )
            mdx = stringify_mdx(mdx_ast)
            return self._atoti_client.explain_mdx_query(
                context=context,
                mdx=mdx,
                timeout=timeout,
            )

        def get_data_types(
            identifiers: Collection[IdentifierT_co],
            /,
            *,
            cube_name: str,
        ) -> dict[IdentifierT_co, DataType]:
            assert cube_name == self.name
            return self._get_data_types(identifiers)

        return self._atoti_client.execute_cube_query(
            context=context,
            cube_name=self.name,
            filter=filter,
            get_cube_discovery=self._atoti_client.get_cube_discovery,
            get_data_types=get_data_types,
            get_widget_creation_code=self._get_widget_creation_code,
            include_empty_rows=include_empty_rows,
            include_totals=include_totals,
            level_identifiers=level_identifiers,
            measure_identifiers=measure_identifiers,
            mode=mode,
            scenario_name=scenario,
            session_id=self._session_id,
            timeout=timeout,
        )

    def create_parameter_simulation(
        self,
        name: str,
        *,
        measures: Annotated[
            Mapping[str, ConstantValue | None],
            Field(min_length=1),
        ],
        levels: Sequence[Level] = (),
        base_scenario_name: str = _BASE_SCENARIO_NAME,
    ) -> Table:
        """Create a parameter simulation and its associated measures.

        Args:
            name: The name of the simulation.
              This is also the name of the corresponding table that will be created.
            measures: The mapping from the names of the created measures to their default value.
            levels: The levels to simulate on.
            base_scenario_name: The name of the base scenario.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> sales_table = session.read_csv(
            ...     TUTORIAL_RESOURCES_PATH / "sales.csv",
            ...     keys={"Sale ID"},
            ...     table_name="Sales",
            ... )
            >>> shops_table = session.read_csv(
            ...     TUTORIAL_RESOURCES_PATH / "shops.csv",
            ...     keys={"Shop ID"},
            ...     table_name="Shops",
            ... )
            >>> sales_table.join(shops_table, sales_table["Shop"] == shops_table["Shop ID"])
            >>> cube = session.create_cube(sales_table)
            >>> l, m = cube.levels, cube.measures

            Creating a parameter simulation on one level:

            >>> country_simulation = cube.create_parameter_simulation(
            ...     "Country simulation",
            ...     measures={"Country parameter": 1.0},
            ...     levels=[l["Country"]],
            ... )
            >>> country_simulation += ("France crash", "France", 0.8)
            >>> country_simulation.head()
                                  Country parameter
            Scenario     Country
            France crash France                 0.8

            * ``France crash`` is the name of the scenario.
            * ``France`` is the coordinate at which the value will be changed.
            * ``0.8`` is the value the :guilabel:`Country parameter` measure will have in this scenario.

            >>> m["Unparametrized turnover"] = tt.agg.sum(
            ...     sales_table["Unit price"] * sales_table["Quantity"]
            ... )
            >>> m["Turnover"] = tt.agg.sum(
            ...     m["Unparametrized turnover"] * m["Country parameter"],
            ...     scope=tt.OriginScope({l["Country"]}),
            ... )
            >>> cube.query(m["Turnover"], levels=[l["Country simulation"]])
                                  Turnover
            Country simulation
            Base                961,463.00
            France crash        889,854.60

            Drilldown to the :guilabel:`Country` level for more details:

            >>> cube.query(
            ...     m["Unparametrized turnover"],
            ...     m["Country parameter"],
            ...     m["Turnover"],
            ...     levels=[l["Country simulation"], l["Country"]],
            ... )
                                       Unparametrized turnover Country parameter    Turnover
            Country simulation Country
            Base               France               358,042.00              1.00  358,042.00
                               USA                  603,421.00              1.00  603,421.00
            France crash       France               358,042.00               .80  286,433.60
                               USA                  603,421.00              1.00  603,421.00

            Creating a parameter simulation on multiple levels:

            >>> size_simulation = cube.create_parameter_simulation(
            ...     "Size simulation",
            ...     measures={"Size parameter": 1.0},
            ...     levels=[l["Country"], l["Shop size"]],
            ... )
            >>> size_simulation += (
            ...     "Going local",
            ...     None,  # ``None`` serves as a wildcard matching any member value.
            ...     "big",
            ...     0.8,
            ... )
            >>> size_simulation += ("Going local", "USA", "small", 1.2)
            >>> m["Turnover"] = tt.agg.sum(
            ...     m["Unparametrized turnover"]
            ...     * m["Country parameter"]
            ...     * m["Size parameter"],
            ...     scope=tt.OriginScope({l["Country"], l["Shop size"]}),
            ... )
            >>> cube.query(
            ...     m["Turnover"],
            ...     levels=[l["Size simulation"], l["Shop size"]],
            ... )
                                         Turnover
            Size simulation Shop size
            Base            big        120,202.00
                            medium     356,779.00
                            small      484,482.00
            Going local     big         96,161.60
                            medium     356,779.00
                            small      547,725.20

            When several rules contain ``None``, the one where the first ``None`` appears last takes precedence.

            >>> size_simulation += ("Going France and Local", "France", None, 2)
            >>> size_simulation += ("Going France and Local", None, "small", 10)
            >>> cube.query(
            ...     m["Unparametrized turnover"],
            ...     m["Turnover"],
            ...     levels=[l["Country"], l["Shop size"]],
            ...     filter=l["Size simulation"] == "Going France and Local",
            ... )
                              Unparametrized turnover      Turnover
            Country Shop size
            France  big                     47,362.00     94,724.00
                    medium                 142,414.00    284,828.00
                    small                  168,266.00    336,532.00
            USA     big                     72,840.00     72,840.00
                    medium                 214,365.00    214,365.00
                    small                  316,216.00  3,162,160.00

            Creating a parameter simulation without levels:

            >>> crisis_simulation = cube.create_parameter_simulation(
            ...     "Global Simulation",
            ...     measures={"Global parameter": 1.0},
            ... )
            >>> crisis_simulation += ("Global Crisis", 0.9)
            >>> m["Turnover"] = m["Unparametrized turnover"] * m["Global parameter"]
            >>> cube.query(m["Turnover"], levels=[l["Global Simulation"]])
                                 Turnover
            Global Simulation
            Base               961,463.00
            Global Crisis      865,316.70

            Creating a parameter simulation with multiple measures:

            >>> multi_parameter_simulation = cube.create_parameter_simulation(
            ...     "Price And Quantity",
            ...     measures={
            ...         "Price parameter": 1.0,
            ...         "Quantity parameter": 1.0,
            ...     },
            ... )
            >>> multi_parameter_simulation += ("Price Up Quantity Down", 1.2, 0.8)
            >>> m["Simulated Price"] = (
            ...     tt.agg.single_value(sales_table["Unit price"]) * m["Price parameter"]
            ... )
            >>> m["Simulated Quantity"] = (
            ...     tt.agg.single_value(sales_table["Quantity"]) * m["Quantity parameter"]
            ... )
            >>> m["Turnover"] = tt.agg.sum_product(
            ...     m["Simulated Price"],
            ...     m["Simulated Quantity"],
            ...     scope=tt.OriginScope({l["Sale ID"]}),
            ... )
            >>> cube.query(m["Turnover"], levels=[l["Price And Quantity"]])
                                      Turnover
            Price And Quantity
            Base                    961,463.00
            Price Up Quantity Down  923,004.48

        """
        if any(level.name == "Scenario" for level in levels):
            raise ValueError(
                'Levels with the name "Scenario" cannot be used in parameter simulations.',
            )

        self._java_api.create_parameter_simulation(
            cube_name=self.name,
            simulation_name=name,
            level_identifiers=[level._identifier for level in levels],
            base_scenario_name=base_scenario_name,
            measures={
                MeasureIdentifier(measure_name): None
                if default_value is None
                else Constant.of(default_value)
                for measure_name, default_value in measures.items()
            },
        )
        return Table(
            TableIdentifier(name),
            atoti_client=self._atoti_client,
            java_api=self._java_api,
            scenario=None,
        )

    def create_parameter_hierarchy_from_column(self, name: str, column: Column) -> None:
        """Create a single-level hierarchy which dynamically takes its members from a column.

        Args:
            name: Name given to the created dimension, hierarchy and its single level.
            column: Column from which to take members.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     {
            ...         "Seller": ["Seller_1", "Seller_1", "Seller_2", "Seller_2"],
            ...         "ProductId": ["aBk3", "ceJ4", "aBk3", "ceJ4"],
            ...         "Price": [2.5, 49.99, 3.0, 54.99],
            ...     }
            ... )
            >>> table = session.read_pandas(df, table_name="Seller")
            >>> cube = session.create_cube(table)
            >>> l, m = cube.levels, cube.measures
            >>> cube.create_parameter_hierarchy_from_column("Competitor", table["Seller"])
            >>> m["Price"] = tt.agg.single_value(table["Price"])
            >>> m["Competitor price"] = tt.at(m["Price"], l["Seller"] == l["Competitor"])
            >>> cube.query(
            ...     m["Competitor price"],
            ...     levels=[l["Seller"], l["ProductId"]],
            ... )
                               Competitor price
            Seller   ProductId
            Seller_1 aBk3                  2.50
                     ceJ4                 49.99
            Seller_2 aBk3                  2.50
                     ceJ4                 49.99
            >>> cube.query(
            ...     m["Competitor price"],
            ...     levels=[l["Seller"], l["ProductId"]],
            ...     filter=l["Competitor"] == "Seller_2",
            ... )
                               Competitor price
            Seller   ProductId
            Seller_1 aBk3                  3.00
                     ceJ4                 54.99
            Seller_2 aBk3                  3.00
                     ceJ4                 54.99
        """
        self._java_api.create_analysis_hierarchy(
            name,
            column_identifier=column._identifier,
            cube_name=self.name,
        )
        self._java_api.refresh()

    def create_parameter_hierarchy_from_members(
        self,
        name: str,
        members: Sequence[ConstantValue],
        *,
        data_type: DataType | None = None,
        index_measure_name: str | None = None,
    ) -> None:
        """Create a single-level hierarchy with the given members.

        It can be used as a parameter hierarchy in advanced analyzes.

        Args:
            name: The name of hierarchy and its single level.
            members: The members of the hierarchy.
            data_type: The type with which the members will be stored.
                Automatically inferred by default.
            index_measure_name: The name of the indexing measure to create for this hierarchy, if any.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> df = pd.DataFrame(
            ...     {
            ...         "Seller": ["Seller_1", "Seller_2", "Seller_3"],
            ...         "Prices": [
            ...             [2.5, 49.99, 3.0, 54.99],
            ...             [2.6, 50.99, 2.8, 57.99],
            ...             [2.99, 44.99, 3.6, 59.99],
            ...         ],
            ...     }
            ... )
            >>> table = session.read_pandas(df, table_name="Seller prices")
            >>> cube = session.create_cube(table)
            >>> l, m = cube.levels, cube.measures
            >>> cube.create_parameter_hierarchy_from_members(
            ...     "ProductID",
            ...     ["aBk3", "ceJ4", "aBk5", "ceJ9"],
            ...     index_measure_name="Product index",
            ... )
            >>> m["Prices"] = tt.agg.single_value(table["Prices"])
            >>> m["Product price"] = m["Prices"][m["Product index"]]
            >>> cube.query(
            ...     m["Product price"],
            ...     levels=[l["Seller"], l["ProductID"]],
            ... )
                               Product price
            Seller   ProductID
            Seller_1 aBk3               2.50
                     aBk5               3.00
                     ceJ4              49.99
                     ceJ9              54.99
            Seller_2 aBk3               2.60
                     aBk5               2.80
                     ceJ4              50.99
                     ceJ9              57.99
            Seller_3 aBk3               2.99
                     aBk5               3.60
                     ceJ4              44.99
                     ceJ9              59.99

        """
        assert self._atoti_client._graphql_client

        index_column = f"{name} index"
        parameter_df = pd.DataFrame({name: members})
        data_types = get_data_types_from_arrow(
            pandas_to_arrow(parameter_df, data_types={})
        )
        if index_measure_name is not None:
            parameter_df[index_column] = list(range(len(members)))
            data_types[index_column] = "int"

        if data_type:
            data_types[name] = data_type
        elif all(
            isinstance(member, int) and -(2**31) <= member < 2**31 for member in members
        ):
            data_types[name] = "int"

        table_name = f"{name}-{uuid4()}"
        parameter_table_identifier = TableIdentifier(table_name)
        self._java_api.create_table(
            parameter_table_identifier,
            data_types=data_types,
            default_values={},
            is_parameter_table=True,
            keys=[name],
            partitioning=None,
        )
        parameter_table = Table(
            parameter_table_identifier,
            atoti_client=self._atoti_client,
            java_api=self._java_api,
            scenario=None,
        )
        parameter_table.load(parameter_df)

        self._atoti_client._graphql_client.create_join(
            CreateJoinInput(
                mapping_items=[],
                # Current limitation: only one join per {source,target} pair.
                name=parameter_table.name,
                source_table_identifier=self._fact_table_identifier._graphql_input,
                target_table_identifier=parameter_table._identifier._graphql_input,
            ),
        )

        if index_measure_name is not None:
            self.measures[index_measure_name] = single_value(
                parameter_table[index_column],
            )

        self.hierarchies[table_name, name].dimension = name
        self.hierarchies[name, name].slicing = True

        self._java_api.refresh()

    def create_date_hierarchy(
        self,
        name: str,
        *,
        column: Column,
        levels: Mapping[str, str] = _DEFAULT_DATE_HIERARCHY_LEVELS,
    ) -> None:
        """Create a multilevel date hierarchy based on a date column.

        The new levels are created by matching a `date pattern <https://docs.oracle.com/en/java/javase/15/docs/api/java.base/java/time/format/DateTimeFormatter.html#patterns>`_.
        Here is a non-exhaustive list of patterns that can be used:

        +---------+-----------------------------+---------+-----------------------------------+
        | Pattern | Description                 | Type    | Examples                          |
        +=========+=============================+=========+===================================+
        | y       | Year                        | Integer | ``2001, 2005, 2020``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | yyyy    | 4-digits year               | String  | ``"2001", "2005", "2020"``        |
        +---------+-----------------------------+---------+-----------------------------------+
        | M       | Month of the year (1 based) | Integer | ``1, 5, 12``                      |
        +---------+-----------------------------+---------+-----------------------------------+
        | MM      | 2-digits month              | String  | ``"01", "05", "12"``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | d       | Day of the month            | Integer | ``1, 15, 30``                     |
        +---------+-----------------------------+---------+-----------------------------------+
        | dd      | 2-digits day of the month   | String  | ``"01", "15", "30"``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | w       | Week number                 | Integer | ``1, 12, 51``                     |
        +---------+-----------------------------+---------+-----------------------------------+
        | Q       | Quarter                     | Integer | ``1, 2, 3, 4``                    |
        +---------+-----------------------------+---------+-----------------------------------+
        | QQQ     | Quarter prefixed with Q     | String  | ``"Q1", "Q2", "Q3", "Q4"``        |
        +---------+-----------------------------+---------+-----------------------------------+
        | H       | Hour of day (0-23)          | Integer | ``0, 12, 23``                     |
        +---------+-----------------------------+---------+-----------------------------------+
        | HH      | 2-digits hour of day        | String  | ``"00", "12", "23"``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | m       | Minute of hour              | Integer | ``0, 30, 59``                     |
        +---------+-----------------------------+---------+-----------------------------------+
        | mm      | 2-digits minute of hour     | String  | ``"00", "30", "59"``              |
        +---------+-----------------------------+---------+-----------------------------------+
        | s       | Second of minute            | Integer | ``0, 5, 55``                      |
        +---------+-----------------------------+---------+-----------------------------------+
        | ss      | 2-digits second of minute   | String  | ``"00", "05", "55"``              |
        +---------+-----------------------------+---------+-----------------------------------+

        Args:
            name: The name of the hierarchy to create.
            column: A table column containing a date or a datetime.
            levels: The mapping from the names of the levels to the patterns from which they will be created.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> from datetime import date
            >>> df = pd.DataFrame(
            ...     columns=["Date", "Quantity"],
            ...     data=[
            ...         (date(2020, 1, 10), 150.0),
            ...         (date(2020, 1, 20), 240.0),
            ...         (date(2019, 3, 17), 270.0),
            ...         (date(2019, 12, 12), 200.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, keys={"Date"}, table_name="Example")
            >>> cube = session.create_cube(table)
            >>> l, m = cube.levels, cube.measures
            >>> cube.create_date_hierarchy("Date parts", column=table["Date"])
            >>> cube.query(
            ...     m["Quantity.SUM"],
            ...     include_totals=True,
            ...     levels=[l["Year"], l["Month"], l["Day"]],
            ... )
                            Quantity.SUM
            Year  Month Day
            Total                 860.00
            2019                  470.00
                  3               270.00
                        17        270.00
                  12              200.00
                        12        200.00
            2020                  390.00
                  1               390.00
                        10        150.00
                        20        240.00

            The full date can also be added back as the last level of the hierarchy:

            >>> h = cube.hierarchies
            >>> h["Date parts"] = {**h["Date parts"], "Date": table["Date"]}
            >>> cube.query(
            ...     m["Quantity.SUM"],
            ...     include_totals=True,
            ...     levels=[l["Date parts", "Date"]],
            ... )
                                       Quantity.SUM
            Year  Month Day Date
            Total                            860.00
            2019                             470.00
                  3                          270.00
                        17                   270.00
                            2019-03-17       270.00
                  12                         200.00
                        12                   200.00
                            2019-12-12       200.00
            2020                             390.00
                  1                          390.00
                        10                   150.00
                            2020-01-10       150.00
                        20                   240.00
                            2020-01-20       240.00

            Data inserted into the table after the hierarchy creation will be automatically hierarchized:

            >>> table += (date(2021, 8, 30), 180.0)
            >>> cube.query(
            ...     m["Quantity.SUM"],
            ...     include_totals=True,
            ...     levels=[l["Date parts", "Date"]],
            ...     filter=l["Year"] == "2021",
            ... )
                                       Quantity.SUM
            Year  Month Day Date
            Total                            180.00
            2021                             180.00
                  8                          180.00
                        30                   180.00
                            2021-08-30       180.00

        """
        if not is_temporal_type(column.data_type):
            raise ValueError(
                f"Cannot create a date hierarchy from a column which is not temporal, column `{column.name}` is of type `{column.data_type}`.",
            )
        self._java_api.create_date_hierarchy(
            name,
            cube_name=self.name,
            column_identifier=column._identifier,
            levels=levels,
        )
        self._java_api.refresh()
