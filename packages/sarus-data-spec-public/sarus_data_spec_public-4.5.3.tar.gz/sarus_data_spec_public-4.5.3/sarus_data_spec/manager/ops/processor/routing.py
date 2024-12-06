import logging
import typing as t

import pyarrow as pa

from sarus_data_spec.manager.ops.base import (
    DatasetImplementation,
    DatasetStaticChecker,
    DataspecStaticChecker,
    ScalarImplementation,
)
from sarus_data_spec.manager.ops.processor.external.external_op import (  # noqa: E501
    ExternalDatasetOp,
    ExternalDatasetStaticChecker,
    ExternalOpImplementation,
    ExternalScalarOp,
    ExternalScalarStaticChecker,
    external_implementation,
)
import sarus_data_spec.protobuf as sp

try:
    from sarus_data_spec.manager.ops.processor.standard.differentiated_sample import (  # noqa: E501
        DifferentiatedSample,
        DifferentiatedSampleStaticChecker,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: DifferentiatedSampling not available.")

from sarus_data_spec.manager.ops.processor.standard.extract import (
    Extract,
    ExtractStaticChecker,
)
from sarus_data_spec.manager.ops.processor.standard.filter import (
    Filter,
    FilterStaticChecker,
)
from sarus_data_spec.manager.ops.processor.standard.get_item import (
    GetItem,
    GetItemStaticChecker,
)
from sarus_data_spec.manager.ops.processor.standard.select_table import (
    SelectTable,
    SelectTableStaticChecker,
)
from sarus_data_spec.manager.ops.processor.standard.project import (
    Project,
    ProjectStaticChecker,
)
from sarus_data_spec.manager.ops.processor.standard.to_small_data import (
    ToSmallData,
    ToSmallDataStaticChecker,
)
from sarus_data_spec.manager.ops.processor.standard.push_sql import (
    PushSQL,
    PushSQLStaticChecker,
)

try:
    from sarus_data_spec.manager.ops.processor.standard.sample import (
        Sample,
        SampleStaticChecker,
    )

except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: Sample not available.")


try:
    from sarus_data_spec.manager.ops.processor.standard.llm.fit_model import (
        FitModel,
        FitModelDP,
        FitModelDPStaticChecker,
        FitModelStaticChecker,
    )

except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: Fit model not available.")

try:
    from sarus_data_spec.manager.ops.processor.standard.llm.generate_from_model import (  # noqa: E501
        GenerateFromModel,
        GenerateFromModelStaticChecker,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: Generate from model not available.")

try:
    from sarus_data_spec.manager.ops.processor.standard.select_sql_op import (
        SelectSqlOp,
        SelectSqlStaticChecker,
    )

except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: SelectSQL not available.")

from sarus_data_spec.manager.ops.processor.standard.shuffle import (
    Shuffle,
    ShuffleStaticChecker,
)

try:
    from sarus_data_spec.manager.ops.processor.standard.protection_utils.privacy_unit_tracking_paths import (  # noqa: E501
        PrivacyUnitTrackingPaths,
        PrivacyUnitTrackingStaticChecker,
        PublicPaths,
        PublicPathStaticChecker,
    )
    from sarus_data_spec.manager.ops.processor.standard.protection_utils.protection import (  # noqa: E501
        ProtectedDataset,
        ProtectedDatasetStaticChecker,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: Protection not available.")

try:
    from sarus_data_spec.manager.ops.processor.standard.user_settings.automatic import (  # noqa: E501
        AutomaticUserSettings,
        AutomaticUserSettingsStaticChecker,
    )
    from sarus_data_spec.manager.ops.processor.standard.user_settings.user_settings import (  # noqa: E501
        UserSettingsDataset,
        UserSettingsStaticChecker,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: UserSettings not available.")
try:
    from sarus_data_spec.manager.ops.processor.standard.assign_budget import (  # noqa: E501
        AssignBudget,
        AssignBudgetStaticChecker,
    )
    from sarus_data_spec.manager.ops.processor.standard.budgets_ops import (  # noqa: E501
        AttributesBudget,
        AttributesBudgetStaticChecker,
        AutomaticBudget,
        AutomaticBudgetStaticChecker,
        SDBudget,
        SDBudgetStaticChecker,
    )

except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: Transforms with budgets not available.")
try:
    from sarus_data_spec.manager.ops.processor.standard.synthetic_data.synthetic import (  # noqa: E501
        Synthetic,
        SyntheticStaticChecker,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: Synthetic not available.")

try:
    from sarus_data_spec.manager.ops.processor.standard.derive_seed import (  # noqa: E501
        DeriveSeed,
        DeriveSeedStaticChecker,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: Seed transforms not available.")
try:
    from sarus_data_spec.manager.ops.processor.standard.group_by_pe import (  # noqa: E501
        GroupByPE,
        GroupByPEStaticChecker,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: GroupPE not available.")
try:
    from sarus_data_spec.manager.ops.processor.standard.user_settings.relationship_spec import (  # noqa: E501
        RelationshipSpecOp,
        RelationshipSpecOpStaticChecker,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: RelationshipSpec not available.")
try:
    from sarus_data_spec.manager.ops.processor.standard.user_settings.validated import (  # noqa: E501
        ValidatedUserTypeOp,
        ValidatedUserTypeOpStaticChecker,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: ValidatedUserType not available.")
try:
    from sarus_data_spec.manager.ops.processor.standard.error_estimation import (  # noqa: E501
        ErrorEstimation,
        ErrorEstimationStaticChecker,
    )
except ModuleNotFoundError:
    logger = logging.getLogger(__name__)
    logger.info("Transforms: ErrorEstimation not available.")

import sarus_data_spec.typing as st


def get_implementation(transform: st.Transform) -> ExternalOpImplementation:
    if not transform.is_external():
        raise NotImplementedError(
            "Cannot get implementation of internal transform."
        )
    return external_implementation(transform)


def get_dataset_op(
    transform: st.Transform,
) -> t.Tuple[t.Type[DatasetImplementation], t.Type[DatasetStaticChecker]]:
    if transform.is_external():
        return ExternalDatasetOp, ExternalDatasetStaticChecker
    elif transform.spec() == "sample":
        return Sample, SampleStaticChecker
    elif transform.spec() == "differentiated_sample":
        return DifferentiatedSample, DifferentiatedSampleStaticChecker
    elif transform.spec() == "to_small_data":
        return ToSmallData, ToSmallDataStaticChecker
    elif transform.spec() == "privacy_unit_tracking":
        return ProtectedDataset, ProtectedDatasetStaticChecker
    elif transform.spec() == "user_settings":
        return UserSettingsDataset, UserSettingsStaticChecker
    elif transform.spec() == "filter":
        return Filter, FilterStaticChecker
    elif transform.spec() == "project":
        return Project, ProjectStaticChecker
    elif transform.spec() == "shuffle":
        return Shuffle, ShuffleStaticChecker
    elif transform.spec() == "synthetic":
        return Synthetic, SyntheticStaticChecker
    elif transform.spec() == "get_item":
        return GetItem, GetItemStaticChecker
    elif transform.spec() == "select_table":
        return SelectTable, SelectTableStaticChecker
    elif transform.spec() == "assign_budget":
        return AssignBudget, AssignBudgetStaticChecker
    elif transform.spec() == "group_by_pe":
        return GroupByPE, GroupByPEStaticChecker
    elif transform.spec() == "select_sql":
        return SelectSqlOp, SelectSqlStaticChecker
    elif transform.spec() == "extract":
        return Extract, ExtractStaticChecker
    elif transform.spec() == "push_sql":
        return PushSQL, PushSQLStaticChecker
    elif transform.spec() == "generate_from_model":
        return GenerateFromModel, GenerateFromModelStaticChecker
    else:
        raise NotImplementedError(transform.spec())


def get_scalar_op(
    transform: st.Transform,
) -> t.Tuple[t.Type[ScalarImplementation], t.Type[DataspecStaticChecker]]:
    if transform.is_external():
        return ExternalScalarOp, ExternalScalarStaticChecker
    elif transform.name() == "automatic_privacy_unit_tracking_paths":
        # here we assume this transform is called
        # on a single dataset
        return PrivacyUnitTrackingPaths, PrivacyUnitTrackingStaticChecker
    elif transform.name() == "automatic_public_paths":
        # here we assume this transform is called
        # on a single dataset
        return PublicPaths, PublicPathStaticChecker
    elif transform.name() == "automatic_user_settings":
        return AutomaticUserSettings, AutomaticUserSettingsStaticChecker
    elif transform.name() == "automatic_budget":
        return AutomaticBudget, AutomaticBudgetStaticChecker
    elif transform.name() == "attributes_budget":
        return AttributesBudget, AttributesBudgetStaticChecker
    elif transform.name() == "sd_budget":
        return SDBudget, SDBudgetStaticChecker
    elif transform.name() == "derive_seed":
        return DeriveSeed, DeriveSeedStaticChecker
    elif transform.name() == "relationship_spec":
        return RelationshipSpecOp, RelationshipSpecOpStaticChecker
    elif transform.name() == "validated_user_type":
        return ValidatedUserTypeOp, ValidatedUserTypeOpStaticChecker
    elif transform.spec() == "error_estimation":
        return ErrorEstimation, ErrorEstimationStaticChecker
    elif transform.name() == "fit_model":
        return FitModel, FitModelStaticChecker
    elif transform.name() == "fit_model_dp":
        return FitModelDP, FitModelDPStaticChecker
    else:
        raise NotImplementedError(f"scalar_transformed for {transform}")


def get_op(
    dataspec: st.DataSpec,
) -> t.Union[
    t.Tuple[t.Type[ScalarImplementation], t.Type[DataspecStaticChecker]],
    t.Tuple[t.Type[DatasetImplementation], t.Type[DatasetStaticChecker]],
]:
    transform = dataspec.transform()
    if dataspec.prototype() == sp.Dataset:
        return get_dataset_op(transform)
    else:
        return get_scalar_op(transform)


class TransformedDataset(DatasetImplementation):
    def __init__(self, dataset: st.Dataset):
        super().__init__(dataset)
        transform = self.dataset.transform()
        ImplementationClass, StaticCheckerClass = get_dataset_op(transform)
        self.implementation = ImplementationClass(dataset)
        self.static_checker = StaticCheckerClass(dataset)

    async def private_queries(self) -> t.List[st.PrivateQuery]:
        return await self.static_checker.private_queries()

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        return await self.implementation.to_arrow(batch_size)

    async def schema(self) -> st.Schema:
        return await self.static_checker.schema()

    async def size(self) -> st.Size:
        return await self.implementation.size()

    async def multiplicity(self) -> st.Multiplicity:
        return await self.implementation.multiplicity()

    async def bounds(self) -> st.Bounds:
        return await self.implementation.bounds()

    async def marginals(self) -> st.Marginals:
        return await self.implementation.marginals()

    async def sql(
        self,
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        return await self.implementation.sql(
            query, dialect, batch_size, result_type
        )


class TransformedScalar(ScalarImplementation):
    def __init__(self, scalar: st.Scalar):
        super().__init__(scalar)
        transform = self.scalar.transform()
        ImplementationClass, StaticCheckerClass = get_scalar_op(transform)
        self.implementation = ImplementationClass(scalar)
        self.static_checker = StaticCheckerClass(scalar)

    async def value(self) -> t.Any:
        return await self.implementation.value()

    async def private_queries(self) -> t.List[st.PrivateQuery]:
        return await self.static_checker.private_queries()
