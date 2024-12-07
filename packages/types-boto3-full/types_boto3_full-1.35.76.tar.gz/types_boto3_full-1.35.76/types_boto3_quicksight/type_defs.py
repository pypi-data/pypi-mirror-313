"""
Type annotations for quicksight service type definitions.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/type_defs/)

Usage::

    ```python
    from types_boto3_quicksight.type_defs import AccountCustomizationTypeDef

    data: AccountCustomizationTypeDef = ...
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AggTypeType,
    AnalysisErrorTypeType,
    AnalysisFilterAttributeType,
    ArcThicknessOptionsType,
    ArcThicknessType,
    AssetBundleExportFormatType,
    AssetBundleExportJobDataSourcePropertyToOverrideType,
    AssetBundleExportJobFolderPropertyToOverrideType,
    AssetBundleExportJobStatusType,
    AssetBundleExportJobVPCConnectionPropertyToOverrideType,
    AssetBundleImportFailureActionType,
    AssetBundleImportJobStatusType,
    AssignmentStatusType,
    AuthenticationMethodOptionType,
    AuthenticationTypeType,
    AuthorSpecifiedAggregationType,
    AxisBindingType,
    BarChartOrientationType,
    BarsArrangementType,
    BaseMapStyleTypeType,
    BoxPlotFillStyleType,
    BrandStatusType,
    BrandVersionStatusType,
    CategoricalAggregationFunctionType,
    CategoryFilterFunctionType,
    CategoryFilterMatchOperatorType,
    CategoryFilterTypeType,
    ColorFillTypeType,
    ColumnDataRoleType,
    ColumnDataSubTypeType,
    ColumnDataTypeType,
    ColumnOrderingTypeType,
    ColumnRoleType,
    ColumnTagNameType,
    CommitModeType,
    ComparisonMethodType,
    ComparisonMethodTypeType,
    ConditionalFormattingIconSetTypeType,
    ConstantTypeType,
    ContributionAnalysisDirectionType,
    ContributionAnalysisSortTypeType,
    CrossDatasetTypesType,
    CustomContentImageScalingConfigurationType,
    CustomContentTypeType,
    DashboardBehaviorType,
    DashboardErrorTypeType,
    DashboardFilterAttributeType,
    DashboardsQAStatusType,
    DashboardUIStateType,
    DataLabelContentType,
    DataLabelOverlapType,
    DataLabelPositionType,
    DataSetFilterAttributeType,
    DataSetImportModeType,
    DatasetParameterValueTypeType,
    DataSourceErrorInfoTypeType,
    DataSourceFilterAttributeType,
    DataSourceTypeType,
    DateAggregationFunctionType,
    DayOfTheWeekType,
    DayOfWeekType,
    DefaultAggregationType,
    DisplayFormatType,
    EditionType,
    EmbeddingIdentityTypeType,
    FileFormatType,
    FilterClassType,
    FilterNullOptionType,
    FilterOperatorType,
    FilterVisualScopeType,
    FolderFilterAttributeType,
    FolderTypeType,
    FontDecorationType,
    FontStyleType,
    FontWeightNameType,
    ForecastComputationSeasonalityType,
    FunnelChartMeasureDataLabelStyleType,
    GeneratedAnswerStatusType,
    GeospatialColorStateType,
    GeoSpatialDataRoleType,
    GeospatialLayerTypeType,
    GeospatialMapNavigationType,
    GeospatialSelectedPointStyleType,
    HistogramBinTypeType,
    HorizontalTextAlignmentType,
    IconType,
    IdentityTypeType,
    ImageCustomActionTriggerType,
    IncludeFolderMembersType,
    IncludeGeneratedAnswerType,
    IncludeQuickSightQIndexType,
    IngestionErrorTypeType,
    IngestionRequestSourceType,
    IngestionRequestTypeType,
    IngestionStatusType,
    IngestionTypeType,
    InputColumnDataTypeType,
    JoinTypeType,
    KPISparklineTypeType,
    KPIVisualStandardLayoutTypeType,
    LayerCustomActionTriggerType,
    LayoutElementTypeType,
    LegendPositionType,
    LineChartLineStyleType,
    LineChartMarkerShapeType,
    LineChartTypeType,
    LineInterpolationType,
    LookbackWindowSizeUnitType,
    MapZoomModeType,
    MaximumMinimumComputationTypeType,
    MemberTypeType,
    MissingDataTreatmentOptionType,
    NamedEntityAggTypeType,
    NamedFilterAggTypeType,
    NamedFilterTypeType,
    NamespaceErrorTypeType,
    NamespaceStatusType,
    NegativeValueDisplayModeType,
    NetworkInterfaceStatusType,
    NullFilterOptionType,
    NumberScaleType,
    NumericEqualityMatchOperatorType,
    NumericSeparatorSymbolType,
    OtherCategoriesType,
    PanelBorderStyleType,
    PaperOrientationType,
    PaperSizeType,
    ParameterValueTypeType,
    PersonalizationModeType,
    PivotTableConditionalFormattingScopeRoleType,
    PivotTableDataPathTypeType,
    PivotTableFieldCollapseStateType,
    PivotTableMetricPlacementType,
    PivotTableRowsLayoutType,
    PivotTableSubtotalLevelType,
    PluginVisualAxisNameType,
    PrimaryValueDisplayTypeType,
    PropertyRoleType,
    PropertyUsageType,
    PurchaseModeType,
    QAResultTypeType,
    QSearchStatusType,
    QueryExecutionModeType,
    RadarChartAxesRangeScaleType,
    RadarChartShapeType,
    ReferenceLineLabelHorizontalPositionType,
    ReferenceLineLabelVerticalPositionType,
    ReferenceLinePatternTypeType,
    ReferenceLineSeriesTypeType,
    ReferenceLineValueLabelRelativePositionType,
    RefreshIntervalType,
    RelativeDateTypeType,
    RelativeFontSizeType,
    ResizeOptionType,
    ResourceStatusType,
    ReviewedAnswerErrorCodeType,
    RoleType,
    RowLevelPermissionFormatVersionType,
    RowLevelPermissionPolicyType,
    SectionPageBreakStatusType,
    SelectedTooltipTypeType,
    ServiceTypeType,
    SharingModelType,
    SheetContentTypeType,
    SheetControlDateTimePickerTypeType,
    SheetControlListTypeType,
    SheetControlSliderTypeType,
    SheetImageScalingTypeType,
    SimpleNumericalAggregationFunctionType,
    SimpleTotalAggregationFunctionType,
    SmallMultiplesAxisPlacementType,
    SmallMultiplesAxisScaleType,
    SnapshotFileFormatTypeType,
    SnapshotFileSheetSelectionScopeType,
    SnapshotJobStatusType,
    SortDirectionType,
    SpecialValueType,
    StarburstProductTypeType,
    StatusType,
    StyledCellTypeType,
    TableBorderStyleType,
    TableCellImageScalingConfigurationType,
    TableOrientationType,
    TableTotalsPlacementType,
    TableTotalsScrollStatusType,
    TemplateErrorTypeType,
    TextQualifierType,
    TextWrapType,
    ThemeTypeType,
    TimeGranularityType,
    TooltipTargetType,
    TooltipTitleTypeType,
    TopBottomComputationTypeType,
    TopBottomSortOrderType,
    TopicFilterAttributeType,
    TopicFilterOperatorType,
    TopicIRFilterFunctionType,
    TopicIRFilterTypeType,
    TopicNumericSeparatorSymbolType,
    TopicRefreshStatusType,
    TopicRelativeDateFilterFunctionType,
    TopicScheduleTypeType,
    TopicSortDirectionType,
    TopicTimeGranularityType,
    TopicUserExperienceVersionType,
    UndefinedSpecifiedValueTypeType,
    URLTargetConfigurationType,
    UserRoleType,
    ValidationStrategyModeType,
    ValueWhenUnsetOptionType,
    VerticalTextAlignmentType,
    VisibilityType,
    VisualCustomActionTriggerType,
    VisualRoleType,
    VPCConnectionAvailabilityStatusType,
    VPCConnectionResourceStatusType,
    WidgetStatusType,
    WordCloudCloudLayoutType,
    WordCloudWordCasingType,
    WordCloudWordOrientationType,
    WordCloudWordPaddingType,
    WordCloudWordScalingType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccountCustomizationTypeDef",
    "AccountInfoTypeDef",
    "AccountSettingsTypeDef",
    "ActiveIAMPolicyAssignmentTypeDef",
    "AdHocFilteringOptionTypeDef",
    "AggFunctionOutputTypeDef",
    "AggFunctionTypeDef",
    "AggFunctionUnionTypeDef",
    "AggregationFunctionTypeDef",
    "AggregationPartitionByTypeDef",
    "AggregationSortConfigurationTypeDef",
    "AmazonElasticsearchParametersTypeDef",
    "AmazonOpenSearchParametersTypeDef",
    "AnalysisDefaultsTypeDef",
    "AnalysisDefinitionOutputTypeDef",
    "AnalysisDefinitionTypeDef",
    "AnalysisErrorTypeDef",
    "AnalysisSearchFilterTypeDef",
    "AnalysisSourceEntityTypeDef",
    "AnalysisSourceTemplateTypeDef",
    "AnalysisSummaryTypeDef",
    "AnalysisTypeDef",
    "AnchorDateConfigurationTypeDef",
    "AnchorTypeDef",
    "AnonymousUserDashboardEmbeddingConfigurationTypeDef",
    "AnonymousUserDashboardFeatureConfigurationsTypeDef",
    "AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef",
    "AnonymousUserEmbeddingExperienceConfigurationTypeDef",
    "AnonymousUserGenerativeQnAEmbeddingConfigurationTypeDef",
    "AnonymousUserQSearchBarEmbeddingConfigurationTypeDef",
    "AnonymousUserSnapshotJobResultTypeDef",
    "ApplicationThemeTypeDef",
    "ArcAxisConfigurationTypeDef",
    "ArcAxisDisplayRangeTypeDef",
    "ArcConfigurationTypeDef",
    "ArcOptionsTypeDef",
    "AssetBundleCloudFormationOverridePropertyConfigurationOutputTypeDef",
    "AssetBundleCloudFormationOverridePropertyConfigurationTypeDef",
    "AssetBundleExportJobAnalysisOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobAnalysisOverridePropertiesTypeDef",
    "AssetBundleExportJobAnalysisOverridePropertiesUnionTypeDef",
    "AssetBundleExportJobDashboardOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobDashboardOverridePropertiesTypeDef",
    "AssetBundleExportJobDashboardOverridePropertiesUnionTypeDef",
    "AssetBundleExportJobDataSetOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobDataSetOverridePropertiesTypeDef",
    "AssetBundleExportJobDataSetOverridePropertiesUnionTypeDef",
    "AssetBundleExportJobDataSourceOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobDataSourceOverridePropertiesTypeDef",
    "AssetBundleExportJobDataSourceOverridePropertiesUnionTypeDef",
    "AssetBundleExportJobErrorTypeDef",
    "AssetBundleExportJobFolderOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobFolderOverridePropertiesTypeDef",
    "AssetBundleExportJobFolderOverridePropertiesUnionTypeDef",
    "AssetBundleExportJobRefreshScheduleOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobRefreshScheduleOverridePropertiesTypeDef",
    "AssetBundleExportJobRefreshScheduleOverridePropertiesUnionTypeDef",
    "AssetBundleExportJobResourceIdOverrideConfigurationTypeDef",
    "AssetBundleExportJobSummaryTypeDef",
    "AssetBundleExportJobThemeOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobThemeOverridePropertiesTypeDef",
    "AssetBundleExportJobThemeOverridePropertiesUnionTypeDef",
    "AssetBundleExportJobVPCConnectionOverridePropertiesOutputTypeDef",
    "AssetBundleExportJobVPCConnectionOverridePropertiesTypeDef",
    "AssetBundleExportJobVPCConnectionOverridePropertiesUnionTypeDef",
    "AssetBundleExportJobValidationStrategyTypeDef",
    "AssetBundleExportJobWarningTypeDef",
    "AssetBundleImportJobAnalysisOverrideParametersTypeDef",
    "AssetBundleImportJobAnalysisOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobAnalysisOverridePermissionsTypeDef",
    "AssetBundleImportJobAnalysisOverridePermissionsUnionTypeDef",
    "AssetBundleImportJobAnalysisOverrideTagsOutputTypeDef",
    "AssetBundleImportJobAnalysisOverrideTagsTypeDef",
    "AssetBundleImportJobAnalysisOverrideTagsUnionTypeDef",
    "AssetBundleImportJobDashboardOverrideParametersTypeDef",
    "AssetBundleImportJobDashboardOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobDashboardOverridePermissionsTypeDef",
    "AssetBundleImportJobDashboardOverridePermissionsUnionTypeDef",
    "AssetBundleImportJobDashboardOverrideTagsOutputTypeDef",
    "AssetBundleImportJobDashboardOverrideTagsTypeDef",
    "AssetBundleImportJobDashboardOverrideTagsUnionTypeDef",
    "AssetBundleImportJobDataSetOverrideParametersTypeDef",
    "AssetBundleImportJobDataSetOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobDataSetOverridePermissionsTypeDef",
    "AssetBundleImportJobDataSetOverridePermissionsUnionTypeDef",
    "AssetBundleImportJobDataSetOverrideTagsOutputTypeDef",
    "AssetBundleImportJobDataSetOverrideTagsTypeDef",
    "AssetBundleImportJobDataSetOverrideTagsUnionTypeDef",
    "AssetBundleImportJobDataSourceCredentialPairTypeDef",
    "AssetBundleImportJobDataSourceCredentialsTypeDef",
    "AssetBundleImportJobDataSourceOverrideParametersOutputTypeDef",
    "AssetBundleImportJobDataSourceOverrideParametersTypeDef",
    "AssetBundleImportJobDataSourceOverrideParametersUnionTypeDef",
    "AssetBundleImportJobDataSourceOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobDataSourceOverridePermissionsTypeDef",
    "AssetBundleImportJobDataSourceOverridePermissionsUnionTypeDef",
    "AssetBundleImportJobDataSourceOverrideTagsOutputTypeDef",
    "AssetBundleImportJobDataSourceOverrideTagsTypeDef",
    "AssetBundleImportJobDataSourceOverrideTagsUnionTypeDef",
    "AssetBundleImportJobErrorTypeDef",
    "AssetBundleImportJobFolderOverrideParametersTypeDef",
    "AssetBundleImportJobFolderOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobFolderOverridePermissionsTypeDef",
    "AssetBundleImportJobFolderOverridePermissionsUnionTypeDef",
    "AssetBundleImportJobFolderOverrideTagsOutputTypeDef",
    "AssetBundleImportJobFolderOverrideTagsTypeDef",
    "AssetBundleImportJobFolderOverrideTagsUnionTypeDef",
    "AssetBundleImportJobOverrideParametersOutputTypeDef",
    "AssetBundleImportJobOverrideParametersTypeDef",
    "AssetBundleImportJobOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobOverridePermissionsTypeDef",
    "AssetBundleImportJobOverrideTagsOutputTypeDef",
    "AssetBundleImportJobOverrideTagsTypeDef",
    "AssetBundleImportJobOverrideValidationStrategyTypeDef",
    "AssetBundleImportJobRefreshScheduleOverrideParametersOutputTypeDef",
    "AssetBundleImportJobRefreshScheduleOverrideParametersTypeDef",
    "AssetBundleImportJobRefreshScheduleOverrideParametersUnionTypeDef",
    "AssetBundleImportJobResourceIdOverrideConfigurationTypeDef",
    "AssetBundleImportJobSummaryTypeDef",
    "AssetBundleImportJobThemeOverrideParametersTypeDef",
    "AssetBundleImportJobThemeOverridePermissionsOutputTypeDef",
    "AssetBundleImportJobThemeOverridePermissionsTypeDef",
    "AssetBundleImportJobThemeOverridePermissionsUnionTypeDef",
    "AssetBundleImportJobThemeOverrideTagsOutputTypeDef",
    "AssetBundleImportJobThemeOverrideTagsTypeDef",
    "AssetBundleImportJobThemeOverrideTagsUnionTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideParametersOutputTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideParametersTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideParametersUnionTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideTagsOutputTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideTagsTypeDef",
    "AssetBundleImportJobVPCConnectionOverrideTagsUnionTypeDef",
    "AssetBundleImportJobWarningTypeDef",
    "AssetBundleImportSourceDescriptionTypeDef",
    "AssetBundleImportSourceTypeDef",
    "AssetBundleResourceLinkSharingConfigurationOutputTypeDef",
    "AssetBundleResourceLinkSharingConfigurationTypeDef",
    "AssetBundleResourceLinkSharingConfigurationUnionTypeDef",
    "AssetBundleResourcePermissionsOutputTypeDef",
    "AssetBundleResourcePermissionsTypeDef",
    "AssetBundleResourcePermissionsUnionTypeDef",
    "AssetOptionsTypeDef",
    "AthenaParametersTypeDef",
    "AttributeAggregationFunctionTypeDef",
    "AuroraParametersTypeDef",
    "AuroraPostgreSqlParametersTypeDef",
    "AuthorizedTargetsByServiceTypeDef",
    "AwsIotAnalyticsParametersTypeDef",
    "AxisDataOptionsOutputTypeDef",
    "AxisDataOptionsTypeDef",
    "AxisDataOptionsUnionTypeDef",
    "AxisDisplayMinMaxRangeTypeDef",
    "AxisDisplayOptionsOutputTypeDef",
    "AxisDisplayOptionsTypeDef",
    "AxisDisplayOptionsUnionTypeDef",
    "AxisDisplayRangeOutputTypeDef",
    "AxisDisplayRangeTypeDef",
    "AxisDisplayRangeUnionTypeDef",
    "AxisLabelOptionsTypeDef",
    "AxisLabelReferenceOptionsTypeDef",
    "AxisLinearScaleTypeDef",
    "AxisLogarithmicScaleTypeDef",
    "AxisScaleTypeDef",
    "AxisTickLabelOptionsTypeDef",
    "BarChartAggregatedFieldWellsOutputTypeDef",
    "BarChartAggregatedFieldWellsTypeDef",
    "BarChartAggregatedFieldWellsUnionTypeDef",
    "BarChartConfigurationOutputTypeDef",
    "BarChartConfigurationTypeDef",
    "BarChartConfigurationUnionTypeDef",
    "BarChartFieldWellsOutputTypeDef",
    "BarChartFieldWellsTypeDef",
    "BarChartFieldWellsUnionTypeDef",
    "BarChartSortConfigurationOutputTypeDef",
    "BarChartSortConfigurationTypeDef",
    "BarChartSortConfigurationUnionTypeDef",
    "BarChartVisualOutputTypeDef",
    "BarChartVisualTypeDef",
    "BarChartVisualUnionTypeDef",
    "BatchCreateTopicReviewedAnswerRequestRequestTypeDef",
    "BatchCreateTopicReviewedAnswerResponseTypeDef",
    "BatchDeleteTopicReviewedAnswerRequestRequestTypeDef",
    "BatchDeleteTopicReviewedAnswerResponseTypeDef",
    "BigQueryParametersTypeDef",
    "BinCountOptionsTypeDef",
    "BinWidthOptionsTypeDef",
    "BlobTypeDef",
    "BodySectionConfigurationOutputTypeDef",
    "BodySectionConfigurationTypeDef",
    "BodySectionConfigurationUnionTypeDef",
    "BodySectionContentOutputTypeDef",
    "BodySectionContentTypeDef",
    "BodySectionContentUnionTypeDef",
    "BodySectionDynamicCategoryDimensionConfigurationOutputTypeDef",
    "BodySectionDynamicCategoryDimensionConfigurationTypeDef",
    "BodySectionDynamicCategoryDimensionConfigurationUnionTypeDef",
    "BodySectionDynamicNumericDimensionConfigurationOutputTypeDef",
    "BodySectionDynamicNumericDimensionConfigurationTypeDef",
    "BodySectionDynamicNumericDimensionConfigurationUnionTypeDef",
    "BodySectionRepeatConfigurationOutputTypeDef",
    "BodySectionRepeatConfigurationTypeDef",
    "BodySectionRepeatConfigurationUnionTypeDef",
    "BodySectionRepeatDimensionConfigurationOutputTypeDef",
    "BodySectionRepeatDimensionConfigurationTypeDef",
    "BodySectionRepeatDimensionConfigurationUnionTypeDef",
    "BodySectionRepeatPageBreakConfigurationTypeDef",
    "BookmarksConfigurationsTypeDef",
    "BorderStyleTypeDef",
    "BoxPlotAggregatedFieldWellsOutputTypeDef",
    "BoxPlotAggregatedFieldWellsTypeDef",
    "BoxPlotAggregatedFieldWellsUnionTypeDef",
    "BoxPlotChartConfigurationOutputTypeDef",
    "BoxPlotChartConfigurationTypeDef",
    "BoxPlotChartConfigurationUnionTypeDef",
    "BoxPlotFieldWellsOutputTypeDef",
    "BoxPlotFieldWellsTypeDef",
    "BoxPlotFieldWellsUnionTypeDef",
    "BoxPlotOptionsTypeDef",
    "BoxPlotSortConfigurationOutputTypeDef",
    "BoxPlotSortConfigurationTypeDef",
    "BoxPlotSortConfigurationUnionTypeDef",
    "BoxPlotStyleOptionsTypeDef",
    "BoxPlotVisualOutputTypeDef",
    "BoxPlotVisualTypeDef",
    "BoxPlotVisualUnionTypeDef",
    "BrandColorPaletteTypeDef",
    "BrandDefinitionTypeDef",
    "BrandDetailTypeDef",
    "BrandElementStyleTypeDef",
    "BrandSummaryTypeDef",
    "CalculatedColumnTypeDef",
    "CalculatedFieldTypeDef",
    "CalculatedMeasureFieldTypeDef",
    "CancelIngestionRequestRequestTypeDef",
    "CancelIngestionResponseTypeDef",
    "CapabilitiesTypeDef",
    "CascadingControlConfigurationOutputTypeDef",
    "CascadingControlConfigurationTypeDef",
    "CascadingControlConfigurationUnionTypeDef",
    "CascadingControlSourceTypeDef",
    "CastColumnTypeOperationTypeDef",
    "CategoricalDimensionFieldTypeDef",
    "CategoricalMeasureFieldTypeDef",
    "CategoryDrillDownFilterOutputTypeDef",
    "CategoryDrillDownFilterTypeDef",
    "CategoryDrillDownFilterUnionTypeDef",
    "CategoryFilterConfigurationOutputTypeDef",
    "CategoryFilterConfigurationTypeDef",
    "CategoryFilterConfigurationUnionTypeDef",
    "CategoryFilterOutputTypeDef",
    "CategoryFilterTypeDef",
    "CategoryFilterUnionTypeDef",
    "CategoryInnerFilterOutputTypeDef",
    "CategoryInnerFilterTypeDef",
    "CategoryInnerFilterUnionTypeDef",
    "CellValueSynonymOutputTypeDef",
    "CellValueSynonymTypeDef",
    "CellValueSynonymUnionTypeDef",
    "ChartAxisLabelOptionsOutputTypeDef",
    "ChartAxisLabelOptionsTypeDef",
    "ChartAxisLabelOptionsUnionTypeDef",
    "ClusterMarkerConfigurationTypeDef",
    "ClusterMarkerTypeDef",
    "CollectiveConstantEntryTypeDef",
    "CollectiveConstantOutputTypeDef",
    "CollectiveConstantTypeDef",
    "CollectiveConstantUnionTypeDef",
    "ColorScaleOutputTypeDef",
    "ColorScaleTypeDef",
    "ColorScaleUnionTypeDef",
    "ColorsConfigurationOutputTypeDef",
    "ColorsConfigurationTypeDef",
    "ColorsConfigurationUnionTypeDef",
    "ColumnConfigurationOutputTypeDef",
    "ColumnConfigurationTypeDef",
    "ColumnConfigurationUnionTypeDef",
    "ColumnDescriptionTypeDef",
    "ColumnGroupColumnSchemaTypeDef",
    "ColumnGroupOutputTypeDef",
    "ColumnGroupSchemaOutputTypeDef",
    "ColumnGroupSchemaTypeDef",
    "ColumnGroupSchemaUnionTypeDef",
    "ColumnGroupTypeDef",
    "ColumnGroupUnionTypeDef",
    "ColumnHierarchyOutputTypeDef",
    "ColumnHierarchyTypeDef",
    "ColumnHierarchyUnionTypeDef",
    "ColumnIdentifierTypeDef",
    "ColumnLevelPermissionRuleOutputTypeDef",
    "ColumnLevelPermissionRuleTypeDef",
    "ColumnLevelPermissionRuleUnionTypeDef",
    "ColumnSchemaTypeDef",
    "ColumnSortTypeDef",
    "ColumnTagTypeDef",
    "ColumnTooltipItemTypeDef",
    "ComboChartAggregatedFieldWellsOutputTypeDef",
    "ComboChartAggregatedFieldWellsTypeDef",
    "ComboChartAggregatedFieldWellsUnionTypeDef",
    "ComboChartConfigurationOutputTypeDef",
    "ComboChartConfigurationTypeDef",
    "ComboChartConfigurationUnionTypeDef",
    "ComboChartFieldWellsOutputTypeDef",
    "ComboChartFieldWellsTypeDef",
    "ComboChartFieldWellsUnionTypeDef",
    "ComboChartSortConfigurationOutputTypeDef",
    "ComboChartSortConfigurationTypeDef",
    "ComboChartSortConfigurationUnionTypeDef",
    "ComboChartVisualOutputTypeDef",
    "ComboChartVisualTypeDef",
    "ComboChartVisualUnionTypeDef",
    "ComparativeOrderOutputTypeDef",
    "ComparativeOrderTypeDef",
    "ComparativeOrderUnionTypeDef",
    "ComparisonConfigurationTypeDef",
    "ComparisonFormatConfigurationTypeDef",
    "ComputationTypeDef",
    "ConditionalFormattingColorOutputTypeDef",
    "ConditionalFormattingColorTypeDef",
    "ConditionalFormattingColorUnionTypeDef",
    "ConditionalFormattingCustomIconConditionTypeDef",
    "ConditionalFormattingCustomIconOptionsTypeDef",
    "ConditionalFormattingGradientColorOutputTypeDef",
    "ConditionalFormattingGradientColorTypeDef",
    "ConditionalFormattingGradientColorUnionTypeDef",
    "ConditionalFormattingIconDisplayConfigurationTypeDef",
    "ConditionalFormattingIconSetTypeDef",
    "ConditionalFormattingIconTypeDef",
    "ConditionalFormattingSolidColorTypeDef",
    "ContextMenuOptionTypeDef",
    "ContributionAnalysisDefaultOutputTypeDef",
    "ContributionAnalysisDefaultTypeDef",
    "ContributionAnalysisDefaultUnionTypeDef",
    "ContributionAnalysisFactorTypeDef",
    "ContributionAnalysisTimeRangesOutputTypeDef",
    "ContributionAnalysisTimeRangesTypeDef",
    "ContributionAnalysisTimeRangesUnionTypeDef",
    "CreateAccountCustomizationRequestRequestTypeDef",
    "CreateAccountCustomizationResponseTypeDef",
    "CreateAccountSubscriptionRequestRequestTypeDef",
    "CreateAccountSubscriptionResponseTypeDef",
    "CreateAnalysisRequestRequestTypeDef",
    "CreateAnalysisResponseTypeDef",
    "CreateBrandRequestRequestTypeDef",
    "CreateBrandResponseTypeDef",
    "CreateColumnsOperationOutputTypeDef",
    "CreateColumnsOperationTypeDef",
    "CreateColumnsOperationUnionTypeDef",
    "CreateCustomPermissionsRequestRequestTypeDef",
    "CreateCustomPermissionsResponseTypeDef",
    "CreateDashboardRequestRequestTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateDataSetRequestRequestTypeDef",
    "CreateDataSetResponseTypeDef",
    "CreateDataSourceRequestRequestTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateFolderMembershipRequestRequestTypeDef",
    "CreateFolderMembershipResponseTypeDef",
    "CreateFolderRequestRequestTypeDef",
    "CreateFolderResponseTypeDef",
    "CreateGroupMembershipRequestRequestTypeDef",
    "CreateGroupMembershipResponseTypeDef",
    "CreateGroupRequestRequestTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateIAMPolicyAssignmentRequestRequestTypeDef",
    "CreateIAMPolicyAssignmentResponseTypeDef",
    "CreateIngestionRequestRequestTypeDef",
    "CreateIngestionResponseTypeDef",
    "CreateNamespaceRequestRequestTypeDef",
    "CreateNamespaceResponseTypeDef",
    "CreateRefreshScheduleRequestRequestTypeDef",
    "CreateRefreshScheduleResponseTypeDef",
    "CreateRoleMembershipRequestRequestTypeDef",
    "CreateRoleMembershipResponseTypeDef",
    "CreateTemplateAliasRequestRequestTypeDef",
    "CreateTemplateAliasResponseTypeDef",
    "CreateTemplateRequestRequestTypeDef",
    "CreateTemplateResponseTypeDef",
    "CreateThemeAliasRequestRequestTypeDef",
    "CreateThemeAliasResponseTypeDef",
    "CreateThemeRequestRequestTypeDef",
    "CreateThemeResponseTypeDef",
    "CreateTopicRefreshScheduleRequestRequestTypeDef",
    "CreateTopicRefreshScheduleResponseTypeDef",
    "CreateTopicRequestRequestTypeDef",
    "CreateTopicResponseTypeDef",
    "CreateTopicReviewedAnswerTypeDef",
    "CreateVPCConnectionRequestRequestTypeDef",
    "CreateVPCConnectionResponseTypeDef",
    "CredentialPairTypeDef",
    "CurrencyDisplayFormatConfigurationTypeDef",
    "CustomActionFilterOperationOutputTypeDef",
    "CustomActionFilterOperationTypeDef",
    "CustomActionFilterOperationUnionTypeDef",
    "CustomActionNavigationOperationTypeDef",
    "CustomActionSetParametersOperationOutputTypeDef",
    "CustomActionSetParametersOperationTypeDef",
    "CustomActionSetParametersOperationUnionTypeDef",
    "CustomActionURLOperationTypeDef",
    "CustomColorTypeDef",
    "CustomContentConfigurationTypeDef",
    "CustomContentVisualOutputTypeDef",
    "CustomContentVisualTypeDef",
    "CustomContentVisualUnionTypeDef",
    "CustomFilterConfigurationTypeDef",
    "CustomFilterListConfigurationOutputTypeDef",
    "CustomFilterListConfigurationTypeDef",
    "CustomFilterListConfigurationUnionTypeDef",
    "CustomNarrativeOptionsTypeDef",
    "CustomParameterValuesOutputTypeDef",
    "CustomParameterValuesTypeDef",
    "CustomParameterValuesUnionTypeDef",
    "CustomPermissionsTypeDef",
    "CustomSqlOutputTypeDef",
    "CustomSqlTypeDef",
    "CustomSqlUnionTypeDef",
    "CustomValuesConfigurationOutputTypeDef",
    "CustomValuesConfigurationTypeDef",
    "CustomValuesConfigurationUnionTypeDef",
    "DashboardErrorTypeDef",
    "DashboardPublishOptionsTypeDef",
    "DashboardSearchFilterTypeDef",
    "DashboardSourceEntityTypeDef",
    "DashboardSourceTemplateTypeDef",
    "DashboardSummaryTypeDef",
    "DashboardTypeDef",
    "DashboardVersionDefinitionOutputTypeDef",
    "DashboardVersionDefinitionTypeDef",
    "DashboardVersionSummaryTypeDef",
    "DashboardVersionTypeDef",
    "DashboardVisualIdTypeDef",
    "DashboardVisualPublishOptionsTypeDef",
    "DashboardVisualResultTypeDef",
    "DataAggregationTypeDef",
    "DataBarsOptionsTypeDef",
    "DataColorPaletteOutputTypeDef",
    "DataColorPaletteTypeDef",
    "DataColorPaletteUnionTypeDef",
    "DataColorTypeDef",
    "DataFieldSeriesItemTypeDef",
    "DataLabelOptionsOutputTypeDef",
    "DataLabelOptionsTypeDef",
    "DataLabelOptionsUnionTypeDef",
    "DataLabelTypeTypeDef",
    "DataPathColorTypeDef",
    "DataPathLabelTypeTypeDef",
    "DataPathSortOutputTypeDef",
    "DataPathSortTypeDef",
    "DataPathSortUnionTypeDef",
    "DataPathTypeTypeDef",
    "DataPathValueTypeDef",
    "DataPointDrillUpDownOptionTypeDef",
    "DataPointMenuLabelOptionTypeDef",
    "DataPointTooltipOptionTypeDef",
    "DataSetConfigurationOutputTypeDef",
    "DataSetConfigurationTypeDef",
    "DataSetConfigurationUnionTypeDef",
    "DataSetIdentifierDeclarationTypeDef",
    "DataSetReferenceTypeDef",
    "DataSetRefreshPropertiesTypeDef",
    "DataSetSchemaOutputTypeDef",
    "DataSetSchemaTypeDef",
    "DataSetSchemaUnionTypeDef",
    "DataSetSearchFilterTypeDef",
    "DataSetSummaryTypeDef",
    "DataSetTypeDef",
    "DataSetUsageConfigurationTypeDef",
    "DataSourceCredentialsTypeDef",
    "DataSourceErrorInfoTypeDef",
    "DataSourceParametersOutputTypeDef",
    "DataSourceParametersTypeDef",
    "DataSourceParametersUnionTypeDef",
    "DataSourceSearchFilterTypeDef",
    "DataSourceSummaryTypeDef",
    "DataSourceTypeDef",
    "DatabricksParametersTypeDef",
    "DatasetMetadataOutputTypeDef",
    "DatasetMetadataTypeDef",
    "DatasetMetadataUnionTypeDef",
    "DatasetParameterOutputTypeDef",
    "DatasetParameterTypeDef",
    "DatasetParameterUnionTypeDef",
    "DateAxisOptionsTypeDef",
    "DateDimensionFieldTypeDef",
    "DateMeasureFieldTypeDef",
    "DateTimeDatasetParameterDefaultValuesOutputTypeDef",
    "DateTimeDatasetParameterDefaultValuesTypeDef",
    "DateTimeDatasetParameterDefaultValuesUnionTypeDef",
    "DateTimeDatasetParameterOutputTypeDef",
    "DateTimeDatasetParameterTypeDef",
    "DateTimeDatasetParameterUnionTypeDef",
    "DateTimeDefaultValuesOutputTypeDef",
    "DateTimeDefaultValuesTypeDef",
    "DateTimeDefaultValuesUnionTypeDef",
    "DateTimeFormatConfigurationTypeDef",
    "DateTimeHierarchyOutputTypeDef",
    "DateTimeHierarchyTypeDef",
    "DateTimeHierarchyUnionTypeDef",
    "DateTimeParameterDeclarationOutputTypeDef",
    "DateTimeParameterDeclarationTypeDef",
    "DateTimeParameterDeclarationUnionTypeDef",
    "DateTimeParameterOutputTypeDef",
    "DateTimeParameterTypeDef",
    "DateTimeParameterUnionTypeDef",
    "DateTimePickerControlDisplayOptionsTypeDef",
    "DateTimeValueWhenUnsetConfigurationOutputTypeDef",
    "DateTimeValueWhenUnsetConfigurationTypeDef",
    "DateTimeValueWhenUnsetConfigurationUnionTypeDef",
    "DecimalDatasetParameterDefaultValuesOutputTypeDef",
    "DecimalDatasetParameterDefaultValuesTypeDef",
    "DecimalDatasetParameterDefaultValuesUnionTypeDef",
    "DecimalDatasetParameterOutputTypeDef",
    "DecimalDatasetParameterTypeDef",
    "DecimalDatasetParameterUnionTypeDef",
    "DecimalDefaultValuesOutputTypeDef",
    "DecimalDefaultValuesTypeDef",
    "DecimalDefaultValuesUnionTypeDef",
    "DecimalParameterDeclarationOutputTypeDef",
    "DecimalParameterDeclarationTypeDef",
    "DecimalParameterDeclarationUnionTypeDef",
    "DecimalParameterOutputTypeDef",
    "DecimalParameterTypeDef",
    "DecimalParameterUnionTypeDef",
    "DecimalPlacesConfigurationTypeDef",
    "DecimalValueWhenUnsetConfigurationTypeDef",
    "DefaultDateTimePickerControlOptionsTypeDef",
    "DefaultFilterControlConfigurationOutputTypeDef",
    "DefaultFilterControlConfigurationTypeDef",
    "DefaultFilterControlConfigurationUnionTypeDef",
    "DefaultFilterControlOptionsOutputTypeDef",
    "DefaultFilterControlOptionsTypeDef",
    "DefaultFilterControlOptionsUnionTypeDef",
    "DefaultFilterDropDownControlOptionsOutputTypeDef",
    "DefaultFilterDropDownControlOptionsTypeDef",
    "DefaultFilterDropDownControlOptionsUnionTypeDef",
    "DefaultFilterListControlOptionsOutputTypeDef",
    "DefaultFilterListControlOptionsTypeDef",
    "DefaultFilterListControlOptionsUnionTypeDef",
    "DefaultFormattingTypeDef",
    "DefaultFreeFormLayoutConfigurationTypeDef",
    "DefaultGridLayoutConfigurationTypeDef",
    "DefaultInteractiveLayoutConfigurationTypeDef",
    "DefaultNewSheetConfigurationTypeDef",
    "DefaultPaginatedLayoutConfigurationTypeDef",
    "DefaultRelativeDateTimeControlOptionsTypeDef",
    "DefaultSectionBasedLayoutConfigurationTypeDef",
    "DefaultSliderControlOptionsTypeDef",
    "DefaultTextAreaControlOptionsTypeDef",
    "DefaultTextFieldControlOptionsTypeDef",
    "DeleteAccountCustomizationRequestRequestTypeDef",
    "DeleteAccountCustomizationResponseTypeDef",
    "DeleteAccountSubscriptionRequestRequestTypeDef",
    "DeleteAccountSubscriptionResponseTypeDef",
    "DeleteAnalysisRequestRequestTypeDef",
    "DeleteAnalysisResponseTypeDef",
    "DeleteBrandAssignmentRequestRequestTypeDef",
    "DeleteBrandAssignmentResponseTypeDef",
    "DeleteBrandRequestRequestTypeDef",
    "DeleteBrandResponseTypeDef",
    "DeleteCustomPermissionsRequestRequestTypeDef",
    "DeleteCustomPermissionsResponseTypeDef",
    "DeleteDashboardRequestRequestTypeDef",
    "DeleteDashboardResponseTypeDef",
    "DeleteDataSetRefreshPropertiesRequestRequestTypeDef",
    "DeleteDataSetRefreshPropertiesResponseTypeDef",
    "DeleteDataSetRequestRequestTypeDef",
    "DeleteDataSetResponseTypeDef",
    "DeleteDataSourceRequestRequestTypeDef",
    "DeleteDataSourceResponseTypeDef",
    "DeleteDefaultQBusinessApplicationRequestRequestTypeDef",
    "DeleteDefaultQBusinessApplicationResponseTypeDef",
    "DeleteFolderMembershipRequestRequestTypeDef",
    "DeleteFolderMembershipResponseTypeDef",
    "DeleteFolderRequestRequestTypeDef",
    "DeleteFolderResponseTypeDef",
    "DeleteGroupMembershipRequestRequestTypeDef",
    "DeleteGroupMembershipResponseTypeDef",
    "DeleteGroupRequestRequestTypeDef",
    "DeleteGroupResponseTypeDef",
    "DeleteIAMPolicyAssignmentRequestRequestTypeDef",
    "DeleteIAMPolicyAssignmentResponseTypeDef",
    "DeleteIdentityPropagationConfigRequestRequestTypeDef",
    "DeleteIdentityPropagationConfigResponseTypeDef",
    "DeleteNamespaceRequestRequestTypeDef",
    "DeleteNamespaceResponseTypeDef",
    "DeleteRefreshScheduleRequestRequestTypeDef",
    "DeleteRefreshScheduleResponseTypeDef",
    "DeleteRoleCustomPermissionRequestRequestTypeDef",
    "DeleteRoleCustomPermissionResponseTypeDef",
    "DeleteRoleMembershipRequestRequestTypeDef",
    "DeleteRoleMembershipResponseTypeDef",
    "DeleteTemplateAliasRequestRequestTypeDef",
    "DeleteTemplateAliasResponseTypeDef",
    "DeleteTemplateRequestRequestTypeDef",
    "DeleteTemplateResponseTypeDef",
    "DeleteThemeAliasRequestRequestTypeDef",
    "DeleteThemeAliasResponseTypeDef",
    "DeleteThemeRequestRequestTypeDef",
    "DeleteThemeResponseTypeDef",
    "DeleteTopicRefreshScheduleRequestRequestTypeDef",
    "DeleteTopicRefreshScheduleResponseTypeDef",
    "DeleteTopicRequestRequestTypeDef",
    "DeleteTopicResponseTypeDef",
    "DeleteUserByPrincipalIdRequestRequestTypeDef",
    "DeleteUserByPrincipalIdResponseTypeDef",
    "DeleteUserCustomPermissionRequestRequestTypeDef",
    "DeleteUserCustomPermissionResponseTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DeleteUserResponseTypeDef",
    "DeleteVPCConnectionRequestRequestTypeDef",
    "DeleteVPCConnectionResponseTypeDef",
    "DescribeAccountCustomizationRequestRequestTypeDef",
    "DescribeAccountCustomizationResponseTypeDef",
    "DescribeAccountSettingsRequestRequestTypeDef",
    "DescribeAccountSettingsResponseTypeDef",
    "DescribeAccountSubscriptionRequestRequestTypeDef",
    "DescribeAccountSubscriptionResponseTypeDef",
    "DescribeAnalysisDefinitionRequestRequestTypeDef",
    "DescribeAnalysisDefinitionResponseTypeDef",
    "DescribeAnalysisPermissionsRequestRequestTypeDef",
    "DescribeAnalysisPermissionsResponseTypeDef",
    "DescribeAnalysisRequestRequestTypeDef",
    "DescribeAnalysisResponseTypeDef",
    "DescribeAssetBundleExportJobRequestRequestTypeDef",
    "DescribeAssetBundleExportJobResponseTypeDef",
    "DescribeAssetBundleImportJobRequestRequestTypeDef",
    "DescribeAssetBundleImportJobResponseTypeDef",
    "DescribeBrandAssignmentRequestRequestTypeDef",
    "DescribeBrandAssignmentResponseTypeDef",
    "DescribeBrandPublishedVersionRequestRequestTypeDef",
    "DescribeBrandPublishedVersionResponseTypeDef",
    "DescribeBrandRequestRequestTypeDef",
    "DescribeBrandResponseTypeDef",
    "DescribeCustomPermissionsRequestRequestTypeDef",
    "DescribeCustomPermissionsResponseTypeDef",
    "DescribeDashboardDefinitionRequestRequestTypeDef",
    "DescribeDashboardDefinitionResponseTypeDef",
    "DescribeDashboardPermissionsRequestRequestTypeDef",
    "DescribeDashboardPermissionsResponseTypeDef",
    "DescribeDashboardRequestRequestTypeDef",
    "DescribeDashboardResponseTypeDef",
    "DescribeDashboardSnapshotJobRequestRequestTypeDef",
    "DescribeDashboardSnapshotJobResponseTypeDef",
    "DescribeDashboardSnapshotJobResultRequestRequestTypeDef",
    "DescribeDashboardSnapshotJobResultResponseTypeDef",
    "DescribeDashboardsQAConfigurationRequestRequestTypeDef",
    "DescribeDashboardsQAConfigurationResponseTypeDef",
    "DescribeDataSetPermissionsRequestRequestTypeDef",
    "DescribeDataSetPermissionsResponseTypeDef",
    "DescribeDataSetRefreshPropertiesRequestRequestTypeDef",
    "DescribeDataSetRefreshPropertiesResponseTypeDef",
    "DescribeDataSetRequestRequestTypeDef",
    "DescribeDataSetResponseTypeDef",
    "DescribeDataSourcePermissionsRequestRequestTypeDef",
    "DescribeDataSourcePermissionsResponseTypeDef",
    "DescribeDataSourceRequestRequestTypeDef",
    "DescribeDataSourceResponseTypeDef",
    "DescribeDefaultQBusinessApplicationRequestRequestTypeDef",
    "DescribeDefaultQBusinessApplicationResponseTypeDef",
    "DescribeFolderPermissionsRequestDescribeFolderPermissionsPaginateTypeDef",
    "DescribeFolderPermissionsRequestRequestTypeDef",
    "DescribeFolderPermissionsResponseTypeDef",
    "DescribeFolderRequestRequestTypeDef",
    "DescribeFolderResolvedPermissionsRequestDescribeFolderResolvedPermissionsPaginateTypeDef",
    "DescribeFolderResolvedPermissionsRequestRequestTypeDef",
    "DescribeFolderResolvedPermissionsResponseTypeDef",
    "DescribeFolderResponseTypeDef",
    "DescribeGroupMembershipRequestRequestTypeDef",
    "DescribeGroupMembershipResponseTypeDef",
    "DescribeGroupRequestRequestTypeDef",
    "DescribeGroupResponseTypeDef",
    "DescribeIAMPolicyAssignmentRequestRequestTypeDef",
    "DescribeIAMPolicyAssignmentResponseTypeDef",
    "DescribeIngestionRequestRequestTypeDef",
    "DescribeIngestionResponseTypeDef",
    "DescribeIpRestrictionRequestRequestTypeDef",
    "DescribeIpRestrictionResponseTypeDef",
    "DescribeKeyRegistrationRequestRequestTypeDef",
    "DescribeKeyRegistrationResponseTypeDef",
    "DescribeNamespaceRequestRequestTypeDef",
    "DescribeNamespaceResponseTypeDef",
    "DescribeQPersonalizationConfigurationRequestRequestTypeDef",
    "DescribeQPersonalizationConfigurationResponseTypeDef",
    "DescribeQuickSightQSearchConfigurationRequestRequestTypeDef",
    "DescribeQuickSightQSearchConfigurationResponseTypeDef",
    "DescribeRefreshScheduleRequestRequestTypeDef",
    "DescribeRefreshScheduleResponseTypeDef",
    "DescribeRoleCustomPermissionRequestRequestTypeDef",
    "DescribeRoleCustomPermissionResponseTypeDef",
    "DescribeTemplateAliasRequestRequestTypeDef",
    "DescribeTemplateAliasResponseTypeDef",
    "DescribeTemplateDefinitionRequestRequestTypeDef",
    "DescribeTemplateDefinitionResponseTypeDef",
    "DescribeTemplatePermissionsRequestRequestTypeDef",
    "DescribeTemplatePermissionsResponseTypeDef",
    "DescribeTemplateRequestRequestTypeDef",
    "DescribeTemplateResponseTypeDef",
    "DescribeThemeAliasRequestRequestTypeDef",
    "DescribeThemeAliasResponseTypeDef",
    "DescribeThemePermissionsRequestRequestTypeDef",
    "DescribeThemePermissionsResponseTypeDef",
    "DescribeThemeRequestRequestTypeDef",
    "DescribeThemeResponseTypeDef",
    "DescribeTopicPermissionsRequestRequestTypeDef",
    "DescribeTopicPermissionsResponseTypeDef",
    "DescribeTopicRefreshRequestRequestTypeDef",
    "DescribeTopicRefreshResponseTypeDef",
    "DescribeTopicRefreshScheduleRequestRequestTypeDef",
    "DescribeTopicRefreshScheduleResponseTypeDef",
    "DescribeTopicRequestRequestTypeDef",
    "DescribeTopicResponseTypeDef",
    "DescribeUserRequestRequestTypeDef",
    "DescribeUserResponseTypeDef",
    "DescribeVPCConnectionRequestRequestTypeDef",
    "DescribeVPCConnectionResponseTypeDef",
    "DestinationParameterValueConfigurationOutputTypeDef",
    "DestinationParameterValueConfigurationTypeDef",
    "DestinationParameterValueConfigurationUnionTypeDef",
    "DimensionFieldTypeDef",
    "DisplayFormatOptionsTypeDef",
    "DonutCenterOptionsTypeDef",
    "DonutOptionsTypeDef",
    "DrillDownFilterOutputTypeDef",
    "DrillDownFilterTypeDef",
    "DrillDownFilterUnionTypeDef",
    "DropDownControlDisplayOptionsTypeDef",
    "DynamicDefaultValueTypeDef",
    "EmptyVisualOutputTypeDef",
    "EmptyVisualTypeDef",
    "EmptyVisualUnionTypeDef",
    "EntityTypeDef",
    "ErrorInfoTypeDef",
    "ExasolParametersTypeDef",
    "ExcludePeriodConfigurationTypeDef",
    "ExplicitHierarchyOutputTypeDef",
    "ExplicitHierarchyTypeDef",
    "ExplicitHierarchyUnionTypeDef",
    "ExportHiddenFieldsOptionTypeDef",
    "ExportToCSVOptionTypeDef",
    "ExportWithHiddenFieldsOptionTypeDef",
    "FailedKeyRegistrationEntryTypeDef",
    "FieldBasedTooltipOutputTypeDef",
    "FieldBasedTooltipTypeDef",
    "FieldBasedTooltipUnionTypeDef",
    "FieldFolderOutputTypeDef",
    "FieldFolderTypeDef",
    "FieldFolderUnionTypeDef",
    "FieldLabelTypeTypeDef",
    "FieldSeriesItemTypeDef",
    "FieldSortOptionsTypeDef",
    "FieldSortTypeDef",
    "FieldTooltipItemTypeDef",
    "FilledMapAggregatedFieldWellsOutputTypeDef",
    "FilledMapAggregatedFieldWellsTypeDef",
    "FilledMapAggregatedFieldWellsUnionTypeDef",
    "FilledMapConditionalFormattingOptionOutputTypeDef",
    "FilledMapConditionalFormattingOptionTypeDef",
    "FilledMapConditionalFormattingOptionUnionTypeDef",
    "FilledMapConditionalFormattingOutputTypeDef",
    "FilledMapConditionalFormattingTypeDef",
    "FilledMapConditionalFormattingUnionTypeDef",
    "FilledMapConfigurationOutputTypeDef",
    "FilledMapConfigurationTypeDef",
    "FilledMapConfigurationUnionTypeDef",
    "FilledMapFieldWellsOutputTypeDef",
    "FilledMapFieldWellsTypeDef",
    "FilledMapFieldWellsUnionTypeDef",
    "FilledMapShapeConditionalFormattingOutputTypeDef",
    "FilledMapShapeConditionalFormattingTypeDef",
    "FilledMapShapeConditionalFormattingUnionTypeDef",
    "FilledMapSortConfigurationOutputTypeDef",
    "FilledMapSortConfigurationTypeDef",
    "FilledMapSortConfigurationUnionTypeDef",
    "FilledMapVisualOutputTypeDef",
    "FilledMapVisualTypeDef",
    "FilledMapVisualUnionTypeDef",
    "FilterAggMetricsTypeDef",
    "FilterControlOutputTypeDef",
    "FilterControlTypeDef",
    "FilterControlUnionTypeDef",
    "FilterCrossSheetControlOutputTypeDef",
    "FilterCrossSheetControlTypeDef",
    "FilterCrossSheetControlUnionTypeDef",
    "FilterDateTimePickerControlTypeDef",
    "FilterDropDownControlOutputTypeDef",
    "FilterDropDownControlTypeDef",
    "FilterDropDownControlUnionTypeDef",
    "FilterGroupOutputTypeDef",
    "FilterGroupTypeDef",
    "FilterGroupUnionTypeDef",
    "FilterListConfigurationOutputTypeDef",
    "FilterListConfigurationTypeDef",
    "FilterListConfigurationUnionTypeDef",
    "FilterListControlOutputTypeDef",
    "FilterListControlTypeDef",
    "FilterListControlUnionTypeDef",
    "FilterOperationSelectedFieldsConfigurationOutputTypeDef",
    "FilterOperationSelectedFieldsConfigurationTypeDef",
    "FilterOperationSelectedFieldsConfigurationUnionTypeDef",
    "FilterOperationTargetVisualsConfigurationOutputTypeDef",
    "FilterOperationTargetVisualsConfigurationTypeDef",
    "FilterOperationTargetVisualsConfigurationUnionTypeDef",
    "FilterOperationTypeDef",
    "FilterOutputTypeDef",
    "FilterRelativeDateTimeControlTypeDef",
    "FilterScopeConfigurationOutputTypeDef",
    "FilterScopeConfigurationTypeDef",
    "FilterScopeConfigurationUnionTypeDef",
    "FilterSelectableValuesOutputTypeDef",
    "FilterSelectableValuesTypeDef",
    "FilterSelectableValuesUnionTypeDef",
    "FilterSliderControlTypeDef",
    "FilterTextAreaControlTypeDef",
    "FilterTextFieldControlTypeDef",
    "FilterTypeDef",
    "FilterUnionTypeDef",
    "FolderMemberTypeDef",
    "FolderSearchFilterTypeDef",
    "FolderSummaryTypeDef",
    "FolderTypeDef",
    "FontConfigurationTypeDef",
    "FontSizeTypeDef",
    "FontTypeDef",
    "FontWeightTypeDef",
    "ForecastComputationTypeDef",
    "ForecastConfigurationOutputTypeDef",
    "ForecastConfigurationTypeDef",
    "ForecastConfigurationUnionTypeDef",
    "ForecastScenarioOutputTypeDef",
    "ForecastScenarioTypeDef",
    "ForecastScenarioUnionTypeDef",
    "FormatConfigurationTypeDef",
    "FreeFormLayoutCanvasSizeOptionsTypeDef",
    "FreeFormLayoutConfigurationOutputTypeDef",
    "FreeFormLayoutConfigurationTypeDef",
    "FreeFormLayoutConfigurationUnionTypeDef",
    "FreeFormLayoutElementBackgroundStyleTypeDef",
    "FreeFormLayoutElementBorderStyleTypeDef",
    "FreeFormLayoutElementOutputTypeDef",
    "FreeFormLayoutElementTypeDef",
    "FreeFormLayoutElementUnionTypeDef",
    "FreeFormLayoutScreenCanvasSizeOptionsTypeDef",
    "FreeFormSectionLayoutConfigurationOutputTypeDef",
    "FreeFormSectionLayoutConfigurationTypeDef",
    "FreeFormSectionLayoutConfigurationUnionTypeDef",
    "FunnelChartAggregatedFieldWellsOutputTypeDef",
    "FunnelChartAggregatedFieldWellsTypeDef",
    "FunnelChartAggregatedFieldWellsUnionTypeDef",
    "FunnelChartConfigurationOutputTypeDef",
    "FunnelChartConfigurationTypeDef",
    "FunnelChartConfigurationUnionTypeDef",
    "FunnelChartDataLabelOptionsTypeDef",
    "FunnelChartFieldWellsOutputTypeDef",
    "FunnelChartFieldWellsTypeDef",
    "FunnelChartFieldWellsUnionTypeDef",
    "FunnelChartSortConfigurationOutputTypeDef",
    "FunnelChartSortConfigurationTypeDef",
    "FunnelChartSortConfigurationUnionTypeDef",
    "FunnelChartVisualOutputTypeDef",
    "FunnelChartVisualTypeDef",
    "FunnelChartVisualUnionTypeDef",
    "GaugeChartArcConditionalFormattingOutputTypeDef",
    "GaugeChartArcConditionalFormattingTypeDef",
    "GaugeChartArcConditionalFormattingUnionTypeDef",
    "GaugeChartColorConfigurationTypeDef",
    "GaugeChartConditionalFormattingOptionOutputTypeDef",
    "GaugeChartConditionalFormattingOptionTypeDef",
    "GaugeChartConditionalFormattingOptionUnionTypeDef",
    "GaugeChartConditionalFormattingOutputTypeDef",
    "GaugeChartConditionalFormattingTypeDef",
    "GaugeChartConditionalFormattingUnionTypeDef",
    "GaugeChartConfigurationOutputTypeDef",
    "GaugeChartConfigurationTypeDef",
    "GaugeChartConfigurationUnionTypeDef",
    "GaugeChartFieldWellsOutputTypeDef",
    "GaugeChartFieldWellsTypeDef",
    "GaugeChartFieldWellsUnionTypeDef",
    "GaugeChartOptionsTypeDef",
    "GaugeChartPrimaryValueConditionalFormattingOutputTypeDef",
    "GaugeChartPrimaryValueConditionalFormattingTypeDef",
    "GaugeChartPrimaryValueConditionalFormattingUnionTypeDef",
    "GaugeChartVisualOutputTypeDef",
    "GaugeChartVisualTypeDef",
    "GaugeChartVisualUnionTypeDef",
    "GenerateEmbedUrlForAnonymousUserRequestRequestTypeDef",
    "GenerateEmbedUrlForAnonymousUserResponseTypeDef",
    "GenerateEmbedUrlForRegisteredUserRequestRequestTypeDef",
    "GenerateEmbedUrlForRegisteredUserResponseTypeDef",
    "GenerateEmbedUrlForRegisteredUserWithIdentityRequestRequestTypeDef",
    "GenerateEmbedUrlForRegisteredUserWithIdentityResponseTypeDef",
    "GeneratedAnswerResultTypeDef",
    "GeoSpatialColumnGroupOutputTypeDef",
    "GeoSpatialColumnGroupTypeDef",
    "GeoSpatialColumnGroupUnionTypeDef",
    "GeospatialCategoricalColorOutputTypeDef",
    "GeospatialCategoricalColorTypeDef",
    "GeospatialCategoricalColorUnionTypeDef",
    "GeospatialCategoricalDataColorTypeDef",
    "GeospatialCircleRadiusTypeDef",
    "GeospatialCircleSymbolStyleOutputTypeDef",
    "GeospatialCircleSymbolStyleTypeDef",
    "GeospatialCircleSymbolStyleUnionTypeDef",
    "GeospatialColorOutputTypeDef",
    "GeospatialColorTypeDef",
    "GeospatialColorUnionTypeDef",
    "GeospatialCoordinateBoundsTypeDef",
    "GeospatialDataSourceItemTypeDef",
    "GeospatialGradientColorOutputTypeDef",
    "GeospatialGradientColorTypeDef",
    "GeospatialGradientColorUnionTypeDef",
    "GeospatialGradientStepColorTypeDef",
    "GeospatialHeatmapColorScaleOutputTypeDef",
    "GeospatialHeatmapColorScaleTypeDef",
    "GeospatialHeatmapColorScaleUnionTypeDef",
    "GeospatialHeatmapConfigurationOutputTypeDef",
    "GeospatialHeatmapConfigurationTypeDef",
    "GeospatialHeatmapConfigurationUnionTypeDef",
    "GeospatialHeatmapDataColorTypeDef",
    "GeospatialLayerColorFieldOutputTypeDef",
    "GeospatialLayerColorFieldTypeDef",
    "GeospatialLayerColorFieldUnionTypeDef",
    "GeospatialLayerDefinitionOutputTypeDef",
    "GeospatialLayerDefinitionTypeDef",
    "GeospatialLayerDefinitionUnionTypeDef",
    "GeospatialLayerItemOutputTypeDef",
    "GeospatialLayerItemTypeDef",
    "GeospatialLayerItemUnionTypeDef",
    "GeospatialLayerJoinDefinitionOutputTypeDef",
    "GeospatialLayerJoinDefinitionTypeDef",
    "GeospatialLayerJoinDefinitionUnionTypeDef",
    "GeospatialLayerMapConfigurationOutputTypeDef",
    "GeospatialLayerMapConfigurationTypeDef",
    "GeospatialLayerMapConfigurationUnionTypeDef",
    "GeospatialLineLayerOutputTypeDef",
    "GeospatialLineLayerTypeDef",
    "GeospatialLineLayerUnionTypeDef",
    "GeospatialLineStyleOutputTypeDef",
    "GeospatialLineStyleTypeDef",
    "GeospatialLineStyleUnionTypeDef",
    "GeospatialLineSymbolStyleOutputTypeDef",
    "GeospatialLineSymbolStyleTypeDef",
    "GeospatialLineSymbolStyleUnionTypeDef",
    "GeospatialLineWidthTypeDef",
    "GeospatialMapAggregatedFieldWellsOutputTypeDef",
    "GeospatialMapAggregatedFieldWellsTypeDef",
    "GeospatialMapAggregatedFieldWellsUnionTypeDef",
    "GeospatialMapConfigurationOutputTypeDef",
    "GeospatialMapConfigurationTypeDef",
    "GeospatialMapConfigurationUnionTypeDef",
    "GeospatialMapFieldWellsOutputTypeDef",
    "GeospatialMapFieldWellsTypeDef",
    "GeospatialMapFieldWellsUnionTypeDef",
    "GeospatialMapStateTypeDef",
    "GeospatialMapStyleOptionsTypeDef",
    "GeospatialMapStyleTypeDef",
    "GeospatialMapVisualOutputTypeDef",
    "GeospatialMapVisualTypeDef",
    "GeospatialMapVisualUnionTypeDef",
    "GeospatialNullDataSettingsTypeDef",
    "GeospatialNullSymbolStyleTypeDef",
    "GeospatialPointLayerOutputTypeDef",
    "GeospatialPointLayerTypeDef",
    "GeospatialPointLayerUnionTypeDef",
    "GeospatialPointStyleOptionsOutputTypeDef",
    "GeospatialPointStyleOptionsTypeDef",
    "GeospatialPointStyleOptionsUnionTypeDef",
    "GeospatialPointStyleOutputTypeDef",
    "GeospatialPointStyleTypeDef",
    "GeospatialPointStyleUnionTypeDef",
    "GeospatialPolygonLayerOutputTypeDef",
    "GeospatialPolygonLayerTypeDef",
    "GeospatialPolygonLayerUnionTypeDef",
    "GeospatialPolygonStyleOutputTypeDef",
    "GeospatialPolygonStyleTypeDef",
    "GeospatialPolygonStyleUnionTypeDef",
    "GeospatialPolygonSymbolStyleOutputTypeDef",
    "GeospatialPolygonSymbolStyleTypeDef",
    "GeospatialPolygonSymbolStyleUnionTypeDef",
    "GeospatialSolidColorTypeDef",
    "GeospatialStaticFileSourceTypeDef",
    "GeospatialWindowOptionsTypeDef",
    "GetDashboardEmbedUrlRequestRequestTypeDef",
    "GetDashboardEmbedUrlResponseTypeDef",
    "GetSessionEmbedUrlRequestRequestTypeDef",
    "GetSessionEmbedUrlResponseTypeDef",
    "GlobalTableBorderOptionsTypeDef",
    "GradientColorOutputTypeDef",
    "GradientColorTypeDef",
    "GradientColorUnionTypeDef",
    "GradientStopTypeDef",
    "GridLayoutCanvasSizeOptionsTypeDef",
    "GridLayoutConfigurationOutputTypeDef",
    "GridLayoutConfigurationTypeDef",
    "GridLayoutConfigurationUnionTypeDef",
    "GridLayoutElementTypeDef",
    "GridLayoutScreenCanvasSizeOptionsTypeDef",
    "GroupMemberTypeDef",
    "GroupSearchFilterTypeDef",
    "GroupTypeDef",
    "GrowthRateComputationTypeDef",
    "GutterStyleTypeDef",
    "HeaderFooterSectionConfigurationOutputTypeDef",
    "HeaderFooterSectionConfigurationTypeDef",
    "HeaderFooterSectionConfigurationUnionTypeDef",
    "HeatMapAggregatedFieldWellsOutputTypeDef",
    "HeatMapAggregatedFieldWellsTypeDef",
    "HeatMapAggregatedFieldWellsUnionTypeDef",
    "HeatMapConfigurationOutputTypeDef",
    "HeatMapConfigurationTypeDef",
    "HeatMapConfigurationUnionTypeDef",
    "HeatMapFieldWellsOutputTypeDef",
    "HeatMapFieldWellsTypeDef",
    "HeatMapFieldWellsUnionTypeDef",
    "HeatMapSortConfigurationOutputTypeDef",
    "HeatMapSortConfigurationTypeDef",
    "HeatMapSortConfigurationUnionTypeDef",
    "HeatMapVisualOutputTypeDef",
    "HeatMapVisualTypeDef",
    "HeatMapVisualUnionTypeDef",
    "HistogramAggregatedFieldWellsOutputTypeDef",
    "HistogramAggregatedFieldWellsTypeDef",
    "HistogramAggregatedFieldWellsUnionTypeDef",
    "HistogramBinOptionsTypeDef",
    "HistogramConfigurationOutputTypeDef",
    "HistogramConfigurationTypeDef",
    "HistogramConfigurationUnionTypeDef",
    "HistogramFieldWellsOutputTypeDef",
    "HistogramFieldWellsTypeDef",
    "HistogramFieldWellsUnionTypeDef",
    "HistogramVisualOutputTypeDef",
    "HistogramVisualTypeDef",
    "HistogramVisualUnionTypeDef",
    "IAMPolicyAssignmentSummaryTypeDef",
    "IAMPolicyAssignmentTypeDef",
    "IdentifierTypeDef",
    "IdentityCenterConfigurationTypeDef",
    "ImageConfigurationTypeDef",
    "ImageCustomActionOperationOutputTypeDef",
    "ImageCustomActionOperationTypeDef",
    "ImageCustomActionOperationUnionTypeDef",
    "ImageCustomActionOutputTypeDef",
    "ImageCustomActionTypeDef",
    "ImageCustomActionUnionTypeDef",
    "ImageInteractionOptionsTypeDef",
    "ImageMenuOptionTypeDef",
    "ImageSetConfigurationTypeDef",
    "ImageSetTypeDef",
    "ImageSourceTypeDef",
    "ImageStaticFileTypeDef",
    "ImageTypeDef",
    "IncrementalRefreshTypeDef",
    "IngestionTypeDef",
    "InnerFilterOutputTypeDef",
    "InnerFilterTypeDef",
    "InnerFilterUnionTypeDef",
    "InputColumnTypeDef",
    "InsightConfigurationOutputTypeDef",
    "InsightConfigurationTypeDef",
    "InsightConfigurationUnionTypeDef",
    "InsightVisualOutputTypeDef",
    "InsightVisualTypeDef",
    "InsightVisualUnionTypeDef",
    "IntegerDatasetParameterDefaultValuesOutputTypeDef",
    "IntegerDatasetParameterDefaultValuesTypeDef",
    "IntegerDatasetParameterDefaultValuesUnionTypeDef",
    "IntegerDatasetParameterOutputTypeDef",
    "IntegerDatasetParameterTypeDef",
    "IntegerDatasetParameterUnionTypeDef",
    "IntegerDefaultValuesOutputTypeDef",
    "IntegerDefaultValuesTypeDef",
    "IntegerDefaultValuesUnionTypeDef",
    "IntegerParameterDeclarationOutputTypeDef",
    "IntegerParameterDeclarationTypeDef",
    "IntegerParameterDeclarationUnionTypeDef",
    "IntegerParameterOutputTypeDef",
    "IntegerParameterTypeDef",
    "IntegerParameterUnionTypeDef",
    "IntegerValueWhenUnsetConfigurationTypeDef",
    "InvalidTopicReviewedAnswerTypeDef",
    "ItemsLimitConfigurationTypeDef",
    "JiraParametersTypeDef",
    "JoinInstructionTypeDef",
    "JoinKeyPropertiesTypeDef",
    "KPIActualValueConditionalFormattingOutputTypeDef",
    "KPIActualValueConditionalFormattingTypeDef",
    "KPIActualValueConditionalFormattingUnionTypeDef",
    "KPIComparisonValueConditionalFormattingOutputTypeDef",
    "KPIComparisonValueConditionalFormattingTypeDef",
    "KPIComparisonValueConditionalFormattingUnionTypeDef",
    "KPIConditionalFormattingOptionOutputTypeDef",
    "KPIConditionalFormattingOptionTypeDef",
    "KPIConditionalFormattingOptionUnionTypeDef",
    "KPIConditionalFormattingOutputTypeDef",
    "KPIConditionalFormattingTypeDef",
    "KPIConditionalFormattingUnionTypeDef",
    "KPIConfigurationOutputTypeDef",
    "KPIConfigurationTypeDef",
    "KPIConfigurationUnionTypeDef",
    "KPIFieldWellsOutputTypeDef",
    "KPIFieldWellsTypeDef",
    "KPIFieldWellsUnionTypeDef",
    "KPIOptionsTypeDef",
    "KPIPrimaryValueConditionalFormattingOutputTypeDef",
    "KPIPrimaryValueConditionalFormattingTypeDef",
    "KPIPrimaryValueConditionalFormattingUnionTypeDef",
    "KPIProgressBarConditionalFormattingOutputTypeDef",
    "KPIProgressBarConditionalFormattingTypeDef",
    "KPIProgressBarConditionalFormattingUnionTypeDef",
    "KPISortConfigurationOutputTypeDef",
    "KPISortConfigurationTypeDef",
    "KPISortConfigurationUnionTypeDef",
    "KPISparklineOptionsTypeDef",
    "KPIVisualLayoutOptionsTypeDef",
    "KPIVisualOutputTypeDef",
    "KPIVisualStandardLayoutTypeDef",
    "KPIVisualTypeDef",
    "KPIVisualUnionTypeDef",
    "LabelOptionsTypeDef",
    "LayerCustomActionOperationOutputTypeDef",
    "LayerCustomActionOperationTypeDef",
    "LayerCustomActionOperationUnionTypeDef",
    "LayerCustomActionOutputTypeDef",
    "LayerCustomActionTypeDef",
    "LayerCustomActionUnionTypeDef",
    "LayerMapVisualOutputTypeDef",
    "LayerMapVisualTypeDef",
    "LayerMapVisualUnionTypeDef",
    "LayoutConfigurationOutputTypeDef",
    "LayoutConfigurationTypeDef",
    "LayoutConfigurationUnionTypeDef",
    "LayoutOutputTypeDef",
    "LayoutTypeDef",
    "LayoutUnionTypeDef",
    "LegendOptionsTypeDef",
    "LineChartAggregatedFieldWellsOutputTypeDef",
    "LineChartAggregatedFieldWellsTypeDef",
    "LineChartAggregatedFieldWellsUnionTypeDef",
    "LineChartConfigurationOutputTypeDef",
    "LineChartConfigurationTypeDef",
    "LineChartConfigurationUnionTypeDef",
    "LineChartDefaultSeriesSettingsTypeDef",
    "LineChartFieldWellsOutputTypeDef",
    "LineChartFieldWellsTypeDef",
    "LineChartFieldWellsUnionTypeDef",
    "LineChartLineStyleSettingsTypeDef",
    "LineChartMarkerStyleSettingsTypeDef",
    "LineChartSeriesSettingsTypeDef",
    "LineChartSortConfigurationOutputTypeDef",
    "LineChartSortConfigurationTypeDef",
    "LineChartSortConfigurationUnionTypeDef",
    "LineChartVisualOutputTypeDef",
    "LineChartVisualTypeDef",
    "LineChartVisualUnionTypeDef",
    "LineSeriesAxisDisplayOptionsOutputTypeDef",
    "LineSeriesAxisDisplayOptionsTypeDef",
    "LineSeriesAxisDisplayOptionsUnionTypeDef",
    "LinkSharingConfigurationOutputTypeDef",
    "LinkSharingConfigurationTypeDef",
    "ListAnalysesRequestListAnalysesPaginateTypeDef",
    "ListAnalysesRequestRequestTypeDef",
    "ListAnalysesResponseTypeDef",
    "ListAssetBundleExportJobsRequestListAssetBundleExportJobsPaginateTypeDef",
    "ListAssetBundleExportJobsRequestRequestTypeDef",
    "ListAssetBundleExportJobsResponseTypeDef",
    "ListAssetBundleImportJobsRequestListAssetBundleImportJobsPaginateTypeDef",
    "ListAssetBundleImportJobsRequestRequestTypeDef",
    "ListAssetBundleImportJobsResponseTypeDef",
    "ListBrandsRequestListBrandsPaginateTypeDef",
    "ListBrandsRequestRequestTypeDef",
    "ListBrandsResponseTypeDef",
    "ListControlDisplayOptionsTypeDef",
    "ListControlSearchOptionsTypeDef",
    "ListControlSelectAllOptionsTypeDef",
    "ListCustomPermissionsRequestListCustomPermissionsPaginateTypeDef",
    "ListCustomPermissionsRequestRequestTypeDef",
    "ListCustomPermissionsResponseTypeDef",
    "ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef",
    "ListDashboardVersionsRequestRequestTypeDef",
    "ListDashboardVersionsResponseTypeDef",
    "ListDashboardsRequestListDashboardsPaginateTypeDef",
    "ListDashboardsRequestRequestTypeDef",
    "ListDashboardsResponseTypeDef",
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    "ListDataSetsRequestRequestTypeDef",
    "ListDataSetsResponseTypeDef",
    "ListDataSourcesRequestListDataSourcesPaginateTypeDef",
    "ListDataSourcesRequestRequestTypeDef",
    "ListDataSourcesResponseTypeDef",
    "ListFolderMembersRequestListFolderMembersPaginateTypeDef",
    "ListFolderMembersRequestRequestTypeDef",
    "ListFolderMembersResponseTypeDef",
    "ListFoldersForResourceRequestListFoldersForResourcePaginateTypeDef",
    "ListFoldersForResourceRequestRequestTypeDef",
    "ListFoldersForResourceResponseTypeDef",
    "ListFoldersRequestListFoldersPaginateTypeDef",
    "ListFoldersRequestRequestTypeDef",
    "ListFoldersResponseTypeDef",
    "ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef",
    "ListGroupMembershipsRequestRequestTypeDef",
    "ListGroupMembershipsResponseTypeDef",
    "ListGroupsRequestListGroupsPaginateTypeDef",
    "ListGroupsRequestRequestTypeDef",
    "ListGroupsResponseTypeDef",
    "ListIAMPolicyAssignmentsForUserRequestListIAMPolicyAssignmentsForUserPaginateTypeDef",
    "ListIAMPolicyAssignmentsForUserRequestRequestTypeDef",
    "ListIAMPolicyAssignmentsForUserResponseTypeDef",
    "ListIAMPolicyAssignmentsRequestListIAMPolicyAssignmentsPaginateTypeDef",
    "ListIAMPolicyAssignmentsRequestRequestTypeDef",
    "ListIAMPolicyAssignmentsResponseTypeDef",
    "ListIdentityPropagationConfigsRequestRequestTypeDef",
    "ListIdentityPropagationConfigsResponseTypeDef",
    "ListIngestionsRequestListIngestionsPaginateTypeDef",
    "ListIngestionsRequestRequestTypeDef",
    "ListIngestionsResponseTypeDef",
    "ListNamespacesRequestListNamespacesPaginateTypeDef",
    "ListNamespacesRequestRequestTypeDef",
    "ListNamespacesResponseTypeDef",
    "ListRefreshSchedulesRequestRequestTypeDef",
    "ListRefreshSchedulesResponseTypeDef",
    "ListRoleMembershipsRequestListRoleMembershipsPaginateTypeDef",
    "ListRoleMembershipsRequestRequestTypeDef",
    "ListRoleMembershipsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef",
    "ListTemplateAliasesRequestRequestTypeDef",
    "ListTemplateAliasesResponseTypeDef",
    "ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef",
    "ListTemplateVersionsRequestRequestTypeDef",
    "ListTemplateVersionsResponseTypeDef",
    "ListTemplatesRequestListTemplatesPaginateTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "ListTemplatesResponseTypeDef",
    "ListThemeAliasesRequestRequestTypeDef",
    "ListThemeAliasesResponseTypeDef",
    "ListThemeVersionsRequestListThemeVersionsPaginateTypeDef",
    "ListThemeVersionsRequestRequestTypeDef",
    "ListThemeVersionsResponseTypeDef",
    "ListThemesRequestListThemesPaginateTypeDef",
    "ListThemesRequestRequestTypeDef",
    "ListThemesResponseTypeDef",
    "ListTopicRefreshSchedulesRequestRequestTypeDef",
    "ListTopicRefreshSchedulesResponseTypeDef",
    "ListTopicReviewedAnswersRequestRequestTypeDef",
    "ListTopicReviewedAnswersResponseTypeDef",
    "ListTopicsRequestRequestTypeDef",
    "ListTopicsResponseTypeDef",
    "ListUserGroupsRequestListUserGroupsPaginateTypeDef",
    "ListUserGroupsRequestRequestTypeDef",
    "ListUserGroupsResponseTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListUsersRequestRequestTypeDef",
    "ListUsersResponseTypeDef",
    "ListVPCConnectionsRequestRequestTypeDef",
    "ListVPCConnectionsResponseTypeDef",
    "LoadingAnimationTypeDef",
    "LocalNavigationConfigurationTypeDef",
    "LogicalTableOutputTypeDef",
    "LogicalTableSourceTypeDef",
    "LogicalTableTypeDef",
    "LogicalTableUnionTypeDef",
    "LogoConfigurationTypeDef",
    "LogoSetConfigurationTypeDef",
    "LogoSetTypeDef",
    "LogoTypeDef",
    "LongFormatTextTypeDef",
    "LookbackWindowTypeDef",
    "ManifestFileLocationTypeDef",
    "MappedDataSetParameterTypeDef",
    "MarginStyleTypeDef",
    "MariaDbParametersTypeDef",
    "MaximumLabelTypeTypeDef",
    "MaximumMinimumComputationTypeDef",
    "MeasureFieldTypeDef",
    "MemberIdArnPairTypeDef",
    "MetricComparisonComputationTypeDef",
    "MinimumLabelTypeTypeDef",
    "MissingDataConfigurationTypeDef",
    "MySqlParametersTypeDef",
    "NamedEntityDefinitionMetricOutputTypeDef",
    "NamedEntityDefinitionMetricTypeDef",
    "NamedEntityDefinitionMetricUnionTypeDef",
    "NamedEntityDefinitionOutputTypeDef",
    "NamedEntityDefinitionTypeDef",
    "NamedEntityDefinitionUnionTypeDef",
    "NamedEntityRefTypeDef",
    "NamespaceErrorTypeDef",
    "NamespaceInfoV2TypeDef",
    "NavbarStyleTypeDef",
    "NegativeFormatTypeDef",
    "NegativeValueConfigurationTypeDef",
    "NestedFilterOutputTypeDef",
    "NestedFilterTypeDef",
    "NestedFilterUnionTypeDef",
    "NetworkInterfaceTypeDef",
    "NewDefaultValuesOutputTypeDef",
    "NewDefaultValuesTypeDef",
    "NewDefaultValuesUnionTypeDef",
    "NullValueFormatConfigurationTypeDef",
    "NumberDisplayFormatConfigurationTypeDef",
    "NumberFormatConfigurationTypeDef",
    "NumericAxisOptionsOutputTypeDef",
    "NumericAxisOptionsTypeDef",
    "NumericAxisOptionsUnionTypeDef",
    "NumericEqualityDrillDownFilterTypeDef",
    "NumericEqualityFilterOutputTypeDef",
    "NumericEqualityFilterTypeDef",
    "NumericEqualityFilterUnionTypeDef",
    "NumericFormatConfigurationTypeDef",
    "NumericRangeFilterOutputTypeDef",
    "NumericRangeFilterTypeDef",
    "NumericRangeFilterUnionTypeDef",
    "NumericRangeFilterValueTypeDef",
    "NumericSeparatorConfigurationTypeDef",
    "NumericalAggregationFunctionTypeDef",
    "NumericalDimensionFieldTypeDef",
    "NumericalMeasureFieldTypeDef",
    "OAuthParametersTypeDef",
    "OracleParametersTypeDef",
    "OutputColumnTypeDef",
    "OverrideDatasetParameterOperationOutputTypeDef",
    "OverrideDatasetParameterOperationTypeDef",
    "OverrideDatasetParameterOperationUnionTypeDef",
    "PaginationConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "PaletteTypeDef",
    "PanelConfigurationTypeDef",
    "PanelTitleOptionsTypeDef",
    "ParameterControlOutputTypeDef",
    "ParameterControlTypeDef",
    "ParameterControlUnionTypeDef",
    "ParameterDateTimePickerControlTypeDef",
    "ParameterDeclarationOutputTypeDef",
    "ParameterDeclarationTypeDef",
    "ParameterDeclarationUnionTypeDef",
    "ParameterDropDownControlOutputTypeDef",
    "ParameterDropDownControlTypeDef",
    "ParameterDropDownControlUnionTypeDef",
    "ParameterListControlOutputTypeDef",
    "ParameterListControlTypeDef",
    "ParameterListControlUnionTypeDef",
    "ParameterSelectableValuesOutputTypeDef",
    "ParameterSelectableValuesTypeDef",
    "ParameterSelectableValuesUnionTypeDef",
    "ParameterSliderControlTypeDef",
    "ParameterTextAreaControlTypeDef",
    "ParameterTextFieldControlTypeDef",
    "ParametersOutputTypeDef",
    "ParametersTypeDef",
    "ParametersUnionTypeDef",
    "PercentVisibleRangeTypeDef",
    "PercentageDisplayFormatConfigurationTypeDef",
    "PercentileAggregationTypeDef",
    "PeriodOverPeriodComputationTypeDef",
    "PeriodToDateComputationTypeDef",
    "PhysicalTableOutputTypeDef",
    "PhysicalTableTypeDef",
    "PhysicalTableUnionTypeDef",
    "PieChartAggregatedFieldWellsOutputTypeDef",
    "PieChartAggregatedFieldWellsTypeDef",
    "PieChartAggregatedFieldWellsUnionTypeDef",
    "PieChartConfigurationOutputTypeDef",
    "PieChartConfigurationTypeDef",
    "PieChartConfigurationUnionTypeDef",
    "PieChartFieldWellsOutputTypeDef",
    "PieChartFieldWellsTypeDef",
    "PieChartFieldWellsUnionTypeDef",
    "PieChartSortConfigurationOutputTypeDef",
    "PieChartSortConfigurationTypeDef",
    "PieChartSortConfigurationUnionTypeDef",
    "PieChartVisualOutputTypeDef",
    "PieChartVisualTypeDef",
    "PieChartVisualUnionTypeDef",
    "PivotFieldSortOptionsOutputTypeDef",
    "PivotFieldSortOptionsTypeDef",
    "PivotFieldSortOptionsUnionTypeDef",
    "PivotTableAggregatedFieldWellsOutputTypeDef",
    "PivotTableAggregatedFieldWellsTypeDef",
    "PivotTableAggregatedFieldWellsUnionTypeDef",
    "PivotTableCellConditionalFormattingOutputTypeDef",
    "PivotTableCellConditionalFormattingTypeDef",
    "PivotTableCellConditionalFormattingUnionTypeDef",
    "PivotTableConditionalFormattingOptionOutputTypeDef",
    "PivotTableConditionalFormattingOptionTypeDef",
    "PivotTableConditionalFormattingOptionUnionTypeDef",
    "PivotTableConditionalFormattingOutputTypeDef",
    "PivotTableConditionalFormattingScopeTypeDef",
    "PivotTableConditionalFormattingTypeDef",
    "PivotTableConditionalFormattingUnionTypeDef",
    "PivotTableConfigurationOutputTypeDef",
    "PivotTableConfigurationTypeDef",
    "PivotTableConfigurationUnionTypeDef",
    "PivotTableDataPathOptionOutputTypeDef",
    "PivotTableDataPathOptionTypeDef",
    "PivotTableDataPathOptionUnionTypeDef",
    "PivotTableFieldCollapseStateOptionOutputTypeDef",
    "PivotTableFieldCollapseStateOptionTypeDef",
    "PivotTableFieldCollapseStateOptionUnionTypeDef",
    "PivotTableFieldCollapseStateTargetOutputTypeDef",
    "PivotTableFieldCollapseStateTargetTypeDef",
    "PivotTableFieldCollapseStateTargetUnionTypeDef",
    "PivotTableFieldOptionTypeDef",
    "PivotTableFieldOptionsOutputTypeDef",
    "PivotTableFieldOptionsTypeDef",
    "PivotTableFieldOptionsUnionTypeDef",
    "PivotTableFieldSubtotalOptionsTypeDef",
    "PivotTableFieldWellsOutputTypeDef",
    "PivotTableFieldWellsTypeDef",
    "PivotTableFieldWellsUnionTypeDef",
    "PivotTableOptionsOutputTypeDef",
    "PivotTableOptionsTypeDef",
    "PivotTableOptionsUnionTypeDef",
    "PivotTablePaginatedReportOptionsTypeDef",
    "PivotTableRowsLabelOptionsTypeDef",
    "PivotTableSortByOutputTypeDef",
    "PivotTableSortByTypeDef",
    "PivotTableSortByUnionTypeDef",
    "PivotTableSortConfigurationOutputTypeDef",
    "PivotTableSortConfigurationTypeDef",
    "PivotTableSortConfigurationUnionTypeDef",
    "PivotTableTotalOptionsOutputTypeDef",
    "PivotTableTotalOptionsTypeDef",
    "PivotTableTotalOptionsUnionTypeDef",
    "PivotTableVisualOutputTypeDef",
    "PivotTableVisualTypeDef",
    "PivotTableVisualUnionTypeDef",
    "PivotTotalOptionsOutputTypeDef",
    "PivotTotalOptionsTypeDef",
    "PivotTotalOptionsUnionTypeDef",
    "PluginVisualConfigurationOutputTypeDef",
    "PluginVisualConfigurationTypeDef",
    "PluginVisualConfigurationUnionTypeDef",
    "PluginVisualFieldWellOutputTypeDef",
    "PluginVisualFieldWellTypeDef",
    "PluginVisualFieldWellUnionTypeDef",
    "PluginVisualItemsLimitConfigurationTypeDef",
    "PluginVisualOptionsOutputTypeDef",
    "PluginVisualOptionsTypeDef",
    "PluginVisualOptionsUnionTypeDef",
    "PluginVisualOutputTypeDef",
    "PluginVisualPropertyTypeDef",
    "PluginVisualSortConfigurationOutputTypeDef",
    "PluginVisualSortConfigurationTypeDef",
    "PluginVisualSortConfigurationUnionTypeDef",
    "PluginVisualTableQuerySortOutputTypeDef",
    "PluginVisualTableQuerySortTypeDef",
    "PluginVisualTableQuerySortUnionTypeDef",
    "PluginVisualTypeDef",
    "PluginVisualUnionTypeDef",
    "PostgreSqlParametersTypeDef",
    "PredefinedHierarchyOutputTypeDef",
    "PredefinedHierarchyTypeDef",
    "PredefinedHierarchyUnionTypeDef",
    "PredictQAResultsRequestRequestTypeDef",
    "PredictQAResultsResponseTypeDef",
    "PrestoParametersTypeDef",
    "ProgressBarOptionsTypeDef",
    "ProjectOperationOutputTypeDef",
    "ProjectOperationTypeDef",
    "ProjectOperationUnionTypeDef",
    "PutDataSetRefreshPropertiesRequestRequestTypeDef",
    "PutDataSetRefreshPropertiesResponseTypeDef",
    "QAResultTypeDef",
    "QueryExecutionOptionsTypeDef",
    "QueueInfoTypeDef",
    "RadarChartAggregatedFieldWellsOutputTypeDef",
    "RadarChartAggregatedFieldWellsTypeDef",
    "RadarChartAggregatedFieldWellsUnionTypeDef",
    "RadarChartAreaStyleSettingsTypeDef",
    "RadarChartConfigurationOutputTypeDef",
    "RadarChartConfigurationTypeDef",
    "RadarChartConfigurationUnionTypeDef",
    "RadarChartFieldWellsOutputTypeDef",
    "RadarChartFieldWellsTypeDef",
    "RadarChartFieldWellsUnionTypeDef",
    "RadarChartSeriesSettingsTypeDef",
    "RadarChartSortConfigurationOutputTypeDef",
    "RadarChartSortConfigurationTypeDef",
    "RadarChartSortConfigurationUnionTypeDef",
    "RadarChartVisualOutputTypeDef",
    "RadarChartVisualTypeDef",
    "RadarChartVisualUnionTypeDef",
    "RangeConstantTypeDef",
    "RangeEndsLabelTypeTypeDef",
    "RdsParametersTypeDef",
    "RedshiftIAMParametersOutputTypeDef",
    "RedshiftIAMParametersTypeDef",
    "RedshiftIAMParametersUnionTypeDef",
    "RedshiftParametersOutputTypeDef",
    "RedshiftParametersTypeDef",
    "RedshiftParametersUnionTypeDef",
    "ReferenceLineCustomLabelConfigurationTypeDef",
    "ReferenceLineDataConfigurationTypeDef",
    "ReferenceLineDynamicDataConfigurationTypeDef",
    "ReferenceLineLabelConfigurationTypeDef",
    "ReferenceLineStaticDataConfigurationTypeDef",
    "ReferenceLineStyleConfigurationTypeDef",
    "ReferenceLineTypeDef",
    "ReferenceLineValueLabelConfigurationTypeDef",
    "RefreshConfigurationTypeDef",
    "RefreshFrequencyTypeDef",
    "RefreshScheduleOutputTypeDef",
    "RefreshScheduleTypeDef",
    "RegisterUserRequestRequestTypeDef",
    "RegisterUserResponseTypeDef",
    "RegisteredCustomerManagedKeyTypeDef",
    "RegisteredUserConsoleFeatureConfigurationsTypeDef",
    "RegisteredUserDashboardEmbeddingConfigurationTypeDef",
    "RegisteredUserDashboardFeatureConfigurationsTypeDef",
    "RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef",
    "RegisteredUserEmbeddingExperienceConfigurationTypeDef",
    "RegisteredUserGenerativeQnAEmbeddingConfigurationTypeDef",
    "RegisteredUserQSearchBarEmbeddingConfigurationTypeDef",
    "RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef",
    "RelationalTableOutputTypeDef",
    "RelationalTableTypeDef",
    "RelationalTableUnionTypeDef",
    "RelativeDateTimeControlDisplayOptionsTypeDef",
    "RelativeDatesFilterOutputTypeDef",
    "RelativeDatesFilterTypeDef",
    "RelativeDatesFilterUnionTypeDef",
    "RenameColumnOperationTypeDef",
    "ResourcePermissionOutputTypeDef",
    "ResourcePermissionTypeDef",
    "ResourcePermissionUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreAnalysisRequestRequestTypeDef",
    "RestoreAnalysisResponseTypeDef",
    "RollingDateConfigurationTypeDef",
    "RowAlternateColorOptionsOutputTypeDef",
    "RowAlternateColorOptionsTypeDef",
    "RowAlternateColorOptionsUnionTypeDef",
    "RowInfoTypeDef",
    "RowLevelPermissionDataSetTypeDef",
    "RowLevelPermissionTagConfigurationOutputTypeDef",
    "RowLevelPermissionTagConfigurationTypeDef",
    "RowLevelPermissionTagRuleTypeDef",
    "S3BucketConfigurationTypeDef",
    "S3ParametersTypeDef",
    "S3SourceOutputTypeDef",
    "S3SourceTypeDef",
    "S3SourceUnionTypeDef",
    "SameSheetTargetVisualConfigurationOutputTypeDef",
    "SameSheetTargetVisualConfigurationTypeDef",
    "SameSheetTargetVisualConfigurationUnionTypeDef",
    "SankeyDiagramAggregatedFieldWellsOutputTypeDef",
    "SankeyDiagramAggregatedFieldWellsTypeDef",
    "SankeyDiagramAggregatedFieldWellsUnionTypeDef",
    "SankeyDiagramChartConfigurationOutputTypeDef",
    "SankeyDiagramChartConfigurationTypeDef",
    "SankeyDiagramChartConfigurationUnionTypeDef",
    "SankeyDiagramFieldWellsOutputTypeDef",
    "SankeyDiagramFieldWellsTypeDef",
    "SankeyDiagramFieldWellsUnionTypeDef",
    "SankeyDiagramSortConfigurationOutputTypeDef",
    "SankeyDiagramSortConfigurationTypeDef",
    "SankeyDiagramSortConfigurationUnionTypeDef",
    "SankeyDiagramVisualOutputTypeDef",
    "SankeyDiagramVisualTypeDef",
    "SankeyDiagramVisualUnionTypeDef",
    "ScatterPlotCategoricallyAggregatedFieldWellsOutputTypeDef",
    "ScatterPlotCategoricallyAggregatedFieldWellsTypeDef",
    "ScatterPlotCategoricallyAggregatedFieldWellsUnionTypeDef",
    "ScatterPlotConfigurationOutputTypeDef",
    "ScatterPlotConfigurationTypeDef",
    "ScatterPlotConfigurationUnionTypeDef",
    "ScatterPlotFieldWellsOutputTypeDef",
    "ScatterPlotFieldWellsTypeDef",
    "ScatterPlotFieldWellsUnionTypeDef",
    "ScatterPlotSortConfigurationTypeDef",
    "ScatterPlotUnaggregatedFieldWellsOutputTypeDef",
    "ScatterPlotUnaggregatedFieldWellsTypeDef",
    "ScatterPlotUnaggregatedFieldWellsUnionTypeDef",
    "ScatterPlotVisualOutputTypeDef",
    "ScatterPlotVisualTypeDef",
    "ScatterPlotVisualUnionTypeDef",
    "ScheduleRefreshOnEntityTypeDef",
    "ScrollBarOptionsTypeDef",
    "SearchAnalysesRequestRequestTypeDef",
    "SearchAnalysesRequestSearchAnalysesPaginateTypeDef",
    "SearchAnalysesResponseTypeDef",
    "SearchDashboardsRequestRequestTypeDef",
    "SearchDashboardsRequestSearchDashboardsPaginateTypeDef",
    "SearchDashboardsResponseTypeDef",
    "SearchDataSetsRequestRequestTypeDef",
    "SearchDataSetsRequestSearchDataSetsPaginateTypeDef",
    "SearchDataSetsResponseTypeDef",
    "SearchDataSourcesRequestRequestTypeDef",
    "SearchDataSourcesRequestSearchDataSourcesPaginateTypeDef",
    "SearchDataSourcesResponseTypeDef",
    "SearchFoldersRequestRequestTypeDef",
    "SearchFoldersRequestSearchFoldersPaginateTypeDef",
    "SearchFoldersResponseTypeDef",
    "SearchGroupsRequestRequestTypeDef",
    "SearchGroupsRequestSearchGroupsPaginateTypeDef",
    "SearchGroupsResponseTypeDef",
    "SearchTopicsRequestRequestTypeDef",
    "SearchTopicsRequestSearchTopicsPaginateTypeDef",
    "SearchTopicsResponseTypeDef",
    "SecondaryValueOptionsTypeDef",
    "SectionAfterPageBreakTypeDef",
    "SectionBasedLayoutCanvasSizeOptionsTypeDef",
    "SectionBasedLayoutConfigurationOutputTypeDef",
    "SectionBasedLayoutConfigurationTypeDef",
    "SectionBasedLayoutConfigurationUnionTypeDef",
    "SectionBasedLayoutPaperCanvasSizeOptionsTypeDef",
    "SectionLayoutConfigurationOutputTypeDef",
    "SectionLayoutConfigurationTypeDef",
    "SectionLayoutConfigurationUnionTypeDef",
    "SectionPageBreakConfigurationTypeDef",
    "SectionStyleTypeDef",
    "SelectedSheetsFilterScopeConfigurationOutputTypeDef",
    "SelectedSheetsFilterScopeConfigurationTypeDef",
    "SelectedSheetsFilterScopeConfigurationUnionTypeDef",
    "SemanticEntityTypeOutputTypeDef",
    "SemanticEntityTypeTypeDef",
    "SemanticEntityTypeUnionTypeDef",
    "SemanticTypeOutputTypeDef",
    "SemanticTypeTypeDef",
    "SemanticTypeUnionTypeDef",
    "SeriesItemTypeDef",
    "ServiceNowParametersTypeDef",
    "SessionTagTypeDef",
    "SetParameterValueConfigurationOutputTypeDef",
    "SetParameterValueConfigurationTypeDef",
    "SetParameterValueConfigurationUnionTypeDef",
    "ShapeConditionalFormatOutputTypeDef",
    "ShapeConditionalFormatTypeDef",
    "ShapeConditionalFormatUnionTypeDef",
    "SharedViewConfigurationsTypeDef",
    "SheetControlInfoIconLabelOptionsTypeDef",
    "SheetControlLayoutConfigurationOutputTypeDef",
    "SheetControlLayoutConfigurationTypeDef",
    "SheetControlLayoutConfigurationUnionTypeDef",
    "SheetControlLayoutOutputTypeDef",
    "SheetControlLayoutTypeDef",
    "SheetControlLayoutUnionTypeDef",
    "SheetControlsOptionTypeDef",
    "SheetDefinitionOutputTypeDef",
    "SheetDefinitionTypeDef",
    "SheetDefinitionUnionTypeDef",
    "SheetElementConfigurationOverridesTypeDef",
    "SheetElementRenderingRuleTypeDef",
    "SheetImageOutputTypeDef",
    "SheetImageScalingConfigurationTypeDef",
    "SheetImageSourceTypeDef",
    "SheetImageStaticFileSourceTypeDef",
    "SheetImageTooltipConfigurationTypeDef",
    "SheetImageTooltipTextTypeDef",
    "SheetImageTypeDef",
    "SheetImageUnionTypeDef",
    "SheetLayoutElementMaximizationOptionTypeDef",
    "SheetStyleTypeDef",
    "SheetTextBoxTypeDef",
    "SheetTypeDef",
    "SheetVisualScopingConfigurationOutputTypeDef",
    "SheetVisualScopingConfigurationTypeDef",
    "SheetVisualScopingConfigurationUnionTypeDef",
    "ShortFormatTextTypeDef",
    "SignupResponseTypeDef",
    "SimpleClusterMarkerTypeDef",
    "SingleAxisOptionsTypeDef",
    "SliderControlDisplayOptionsTypeDef",
    "SlotTypeDef",
    "SmallMultiplesAxisPropertiesTypeDef",
    "SmallMultiplesOptionsTypeDef",
    "SnapshotAnonymousUserRedactedTypeDef",
    "SnapshotAnonymousUserTypeDef",
    "SnapshotConfigurationOutputTypeDef",
    "SnapshotConfigurationTypeDef",
    "SnapshotDestinationConfigurationOutputTypeDef",
    "SnapshotDestinationConfigurationTypeDef",
    "SnapshotDestinationConfigurationUnionTypeDef",
    "SnapshotFileGroupOutputTypeDef",
    "SnapshotFileGroupTypeDef",
    "SnapshotFileGroupUnionTypeDef",
    "SnapshotFileOutputTypeDef",
    "SnapshotFileSheetSelectionOutputTypeDef",
    "SnapshotFileSheetSelectionTypeDef",
    "SnapshotFileSheetSelectionUnionTypeDef",
    "SnapshotFileTypeDef",
    "SnapshotFileUnionTypeDef",
    "SnapshotJobErrorInfoTypeDef",
    "SnapshotJobResultErrorInfoTypeDef",
    "SnapshotJobResultFileGroupTypeDef",
    "SnapshotJobResultTypeDef",
    "SnapshotJobS3ResultTypeDef",
    "SnapshotS3DestinationConfigurationTypeDef",
    "SnapshotUserConfigurationRedactedTypeDef",
    "SnapshotUserConfigurationTypeDef",
    "SnowflakeParametersTypeDef",
    "SpacingTypeDef",
    "SparkParametersTypeDef",
    "SpatialStaticFileTypeDef",
    "SqlServerParametersTypeDef",
    "SslPropertiesTypeDef",
    "StarburstParametersTypeDef",
    "StartAssetBundleExportJobRequestRequestTypeDef",
    "StartAssetBundleExportJobResponseTypeDef",
    "StartAssetBundleImportJobRequestRequestTypeDef",
    "StartAssetBundleImportJobResponseTypeDef",
    "StartDashboardSnapshotJobRequestRequestTypeDef",
    "StartDashboardSnapshotJobResponseTypeDef",
    "StartDashboardSnapshotJobScheduleRequestRequestTypeDef",
    "StartDashboardSnapshotJobScheduleResponseTypeDef",
    "StatePersistenceConfigurationsTypeDef",
    "StaticFileS3SourceOptionsTypeDef",
    "StaticFileSourceTypeDef",
    "StaticFileTypeDef",
    "StaticFileUrlSourceOptionsTypeDef",
    "StringDatasetParameterDefaultValuesOutputTypeDef",
    "StringDatasetParameterDefaultValuesTypeDef",
    "StringDatasetParameterDefaultValuesUnionTypeDef",
    "StringDatasetParameterOutputTypeDef",
    "StringDatasetParameterTypeDef",
    "StringDatasetParameterUnionTypeDef",
    "StringDefaultValuesOutputTypeDef",
    "StringDefaultValuesTypeDef",
    "StringDefaultValuesUnionTypeDef",
    "StringFormatConfigurationTypeDef",
    "StringParameterDeclarationOutputTypeDef",
    "StringParameterDeclarationTypeDef",
    "StringParameterDeclarationUnionTypeDef",
    "StringParameterOutputTypeDef",
    "StringParameterTypeDef",
    "StringParameterUnionTypeDef",
    "StringValueWhenUnsetConfigurationTypeDef",
    "SubtotalOptionsOutputTypeDef",
    "SubtotalOptionsTypeDef",
    "SubtotalOptionsUnionTypeDef",
    "SucceededTopicReviewedAnswerTypeDef",
    "SuccessfulKeyRegistrationEntryTypeDef",
    "TableAggregatedFieldWellsOutputTypeDef",
    "TableAggregatedFieldWellsTypeDef",
    "TableAggregatedFieldWellsUnionTypeDef",
    "TableBorderOptionsTypeDef",
    "TableCellConditionalFormattingOutputTypeDef",
    "TableCellConditionalFormattingTypeDef",
    "TableCellConditionalFormattingUnionTypeDef",
    "TableCellImageSizingConfigurationTypeDef",
    "TableCellStyleTypeDef",
    "TableConditionalFormattingOptionOutputTypeDef",
    "TableConditionalFormattingOptionTypeDef",
    "TableConditionalFormattingOptionUnionTypeDef",
    "TableConditionalFormattingOutputTypeDef",
    "TableConditionalFormattingTypeDef",
    "TableConditionalFormattingUnionTypeDef",
    "TableConfigurationOutputTypeDef",
    "TableConfigurationTypeDef",
    "TableConfigurationUnionTypeDef",
    "TableFieldCustomIconContentTypeDef",
    "TableFieldCustomTextContentTypeDef",
    "TableFieldImageConfigurationTypeDef",
    "TableFieldLinkConfigurationTypeDef",
    "TableFieldLinkContentConfigurationTypeDef",
    "TableFieldOptionTypeDef",
    "TableFieldOptionsOutputTypeDef",
    "TableFieldOptionsTypeDef",
    "TableFieldOptionsUnionTypeDef",
    "TableFieldURLConfigurationTypeDef",
    "TableFieldWellsOutputTypeDef",
    "TableFieldWellsTypeDef",
    "TableFieldWellsUnionTypeDef",
    "TableInlineVisualizationTypeDef",
    "TableOptionsOutputTypeDef",
    "TableOptionsTypeDef",
    "TableOptionsUnionTypeDef",
    "TablePaginatedReportOptionsTypeDef",
    "TablePinnedFieldOptionsOutputTypeDef",
    "TablePinnedFieldOptionsTypeDef",
    "TablePinnedFieldOptionsUnionTypeDef",
    "TableRowConditionalFormattingOutputTypeDef",
    "TableRowConditionalFormattingTypeDef",
    "TableRowConditionalFormattingUnionTypeDef",
    "TableSideBorderOptionsTypeDef",
    "TableSortConfigurationOutputTypeDef",
    "TableSortConfigurationTypeDef",
    "TableSortConfigurationUnionTypeDef",
    "TableStyleTargetTypeDef",
    "TableUnaggregatedFieldWellsOutputTypeDef",
    "TableUnaggregatedFieldWellsTypeDef",
    "TableUnaggregatedFieldWellsUnionTypeDef",
    "TableVisualOutputTypeDef",
    "TableVisualTypeDef",
    "TableVisualUnionTypeDef",
    "TagColumnOperationOutputTypeDef",
    "TagColumnOperationTypeDef",
    "TagColumnOperationUnionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagResourceResponseTypeDef",
    "TagTypeDef",
    "TemplateAliasTypeDef",
    "TemplateErrorTypeDef",
    "TemplateSourceAnalysisTypeDef",
    "TemplateSourceEntityTypeDef",
    "TemplateSourceTemplateTypeDef",
    "TemplateSummaryTypeDef",
    "TemplateTypeDef",
    "TemplateVersionDefinitionOutputTypeDef",
    "TemplateVersionDefinitionTypeDef",
    "TemplateVersionSummaryTypeDef",
    "TemplateVersionTypeDef",
    "TeradataParametersTypeDef",
    "TextAreaControlDisplayOptionsTypeDef",
    "TextConditionalFormatOutputTypeDef",
    "TextConditionalFormatTypeDef",
    "TextConditionalFormatUnionTypeDef",
    "TextControlPlaceholderOptionsTypeDef",
    "TextFieldControlDisplayOptionsTypeDef",
    "ThemeAliasTypeDef",
    "ThemeConfigurationOutputTypeDef",
    "ThemeConfigurationTypeDef",
    "ThemeErrorTypeDef",
    "ThemeSummaryTypeDef",
    "ThemeTypeDef",
    "ThemeVersionSummaryTypeDef",
    "ThemeVersionTypeDef",
    "ThousandSeparatorOptionsTypeDef",
    "TileLayoutStyleTypeDef",
    "TileStyleTypeDef",
    "TimeBasedForecastPropertiesTypeDef",
    "TimeEqualityFilterOutputTypeDef",
    "TimeEqualityFilterTypeDef",
    "TimeEqualityFilterUnionTypeDef",
    "TimeRangeDrillDownFilterOutputTypeDef",
    "TimeRangeDrillDownFilterTypeDef",
    "TimeRangeDrillDownFilterUnionTypeDef",
    "TimeRangeFilterOutputTypeDef",
    "TimeRangeFilterTypeDef",
    "TimeRangeFilterUnionTypeDef",
    "TimeRangeFilterValueOutputTypeDef",
    "TimeRangeFilterValueTypeDef",
    "TimeRangeFilterValueUnionTypeDef",
    "TimestampTypeDef",
    "TooltipItemTypeDef",
    "TooltipOptionsOutputTypeDef",
    "TooltipOptionsTypeDef",
    "TooltipOptionsUnionTypeDef",
    "TopBottomFilterOutputTypeDef",
    "TopBottomFilterTypeDef",
    "TopBottomFilterUnionTypeDef",
    "TopBottomMoversComputationTypeDef",
    "TopBottomRankedComputationTypeDef",
    "TopicCalculatedFieldOutputTypeDef",
    "TopicCalculatedFieldTypeDef",
    "TopicCalculatedFieldUnionTypeDef",
    "TopicCategoryFilterConstantOutputTypeDef",
    "TopicCategoryFilterConstantTypeDef",
    "TopicCategoryFilterConstantUnionTypeDef",
    "TopicCategoryFilterOutputTypeDef",
    "TopicCategoryFilterTypeDef",
    "TopicCategoryFilterUnionTypeDef",
    "TopicColumnOutputTypeDef",
    "TopicColumnTypeDef",
    "TopicColumnUnionTypeDef",
    "TopicConfigOptionsTypeDef",
    "TopicConstantValueOutputTypeDef",
    "TopicConstantValueTypeDef",
    "TopicConstantValueUnionTypeDef",
    "TopicDateRangeFilterTypeDef",
    "TopicDetailsOutputTypeDef",
    "TopicDetailsTypeDef",
    "TopicFilterOutputTypeDef",
    "TopicFilterTypeDef",
    "TopicFilterUnionTypeDef",
    "TopicIRComparisonMethodTypeDef",
    "TopicIRContributionAnalysisOutputTypeDef",
    "TopicIRContributionAnalysisTypeDef",
    "TopicIRContributionAnalysisUnionTypeDef",
    "TopicIRFilterOptionOutputTypeDef",
    "TopicIRFilterOptionTypeDef",
    "TopicIRFilterOptionUnionTypeDef",
    "TopicIRGroupByTypeDef",
    "TopicIRMetricOutputTypeDef",
    "TopicIRMetricTypeDef",
    "TopicIRMetricUnionTypeDef",
    "TopicIROutputTypeDef",
    "TopicIRTypeDef",
    "TopicIRUnionTypeDef",
    "TopicNamedEntityOutputTypeDef",
    "TopicNamedEntityTypeDef",
    "TopicNamedEntityUnionTypeDef",
    "TopicNumericEqualityFilterTypeDef",
    "TopicNumericRangeFilterTypeDef",
    "TopicRangeFilterConstantTypeDef",
    "TopicRefreshDetailsTypeDef",
    "TopicRefreshScheduleOutputTypeDef",
    "TopicRefreshScheduleSummaryTypeDef",
    "TopicRefreshScheduleTypeDef",
    "TopicRelativeDateFilterTypeDef",
    "TopicReviewedAnswerTypeDef",
    "TopicSearchFilterTypeDef",
    "TopicSingularFilterConstantTypeDef",
    "TopicSortClauseTypeDef",
    "TopicSummaryTypeDef",
    "TopicTemplateOutputTypeDef",
    "TopicTemplateTypeDef",
    "TopicTemplateUnionTypeDef",
    "TopicVisualOutputTypeDef",
    "TopicVisualTypeDef",
    "TopicVisualUnionTypeDef",
    "TotalAggregationComputationTypeDef",
    "TotalAggregationFunctionTypeDef",
    "TotalAggregationOptionTypeDef",
    "TotalOptionsOutputTypeDef",
    "TotalOptionsTypeDef",
    "TotalOptionsUnionTypeDef",
    "TransformOperationOutputTypeDef",
    "TransformOperationTypeDef",
    "TransformOperationUnionTypeDef",
    "TreeMapAggregatedFieldWellsOutputTypeDef",
    "TreeMapAggregatedFieldWellsTypeDef",
    "TreeMapAggregatedFieldWellsUnionTypeDef",
    "TreeMapConfigurationOutputTypeDef",
    "TreeMapConfigurationTypeDef",
    "TreeMapConfigurationUnionTypeDef",
    "TreeMapFieldWellsOutputTypeDef",
    "TreeMapFieldWellsTypeDef",
    "TreeMapFieldWellsUnionTypeDef",
    "TreeMapSortConfigurationOutputTypeDef",
    "TreeMapSortConfigurationTypeDef",
    "TreeMapSortConfigurationUnionTypeDef",
    "TreeMapVisualOutputTypeDef",
    "TreeMapVisualTypeDef",
    "TreeMapVisualUnionTypeDef",
    "TrendArrowOptionsTypeDef",
    "TrinoParametersTypeDef",
    "TwitterParametersTypeDef",
    "TypographyOutputTypeDef",
    "TypographyTypeDef",
    "TypographyUnionTypeDef",
    "UIColorPaletteTypeDef",
    "UnaggregatedFieldTypeDef",
    "UniqueValuesComputationTypeDef",
    "UntagColumnOperationOutputTypeDef",
    "UntagColumnOperationTypeDef",
    "UntagColumnOperationUnionTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UntagResourceResponseTypeDef",
    "UpdateAccountCustomizationRequestRequestTypeDef",
    "UpdateAccountCustomizationResponseTypeDef",
    "UpdateAccountSettingsRequestRequestTypeDef",
    "UpdateAccountSettingsResponseTypeDef",
    "UpdateAnalysisPermissionsRequestRequestTypeDef",
    "UpdateAnalysisPermissionsResponseTypeDef",
    "UpdateAnalysisRequestRequestTypeDef",
    "UpdateAnalysisResponseTypeDef",
    "UpdateApplicationWithTokenExchangeGrantRequestRequestTypeDef",
    "UpdateApplicationWithTokenExchangeGrantResponseTypeDef",
    "UpdateBrandAssignmentRequestRequestTypeDef",
    "UpdateBrandAssignmentResponseTypeDef",
    "UpdateBrandPublishedVersionRequestRequestTypeDef",
    "UpdateBrandPublishedVersionResponseTypeDef",
    "UpdateBrandRequestRequestTypeDef",
    "UpdateBrandResponseTypeDef",
    "UpdateCustomPermissionsRequestRequestTypeDef",
    "UpdateCustomPermissionsResponseTypeDef",
    "UpdateDashboardLinksRequestRequestTypeDef",
    "UpdateDashboardLinksResponseTypeDef",
    "UpdateDashboardPermissionsRequestRequestTypeDef",
    "UpdateDashboardPermissionsResponseTypeDef",
    "UpdateDashboardPublishedVersionRequestRequestTypeDef",
    "UpdateDashboardPublishedVersionResponseTypeDef",
    "UpdateDashboardRequestRequestTypeDef",
    "UpdateDashboardResponseTypeDef",
    "UpdateDashboardsQAConfigurationRequestRequestTypeDef",
    "UpdateDashboardsQAConfigurationResponseTypeDef",
    "UpdateDataSetPermissionsRequestRequestTypeDef",
    "UpdateDataSetPermissionsResponseTypeDef",
    "UpdateDataSetRequestRequestTypeDef",
    "UpdateDataSetResponseTypeDef",
    "UpdateDataSourcePermissionsRequestRequestTypeDef",
    "UpdateDataSourcePermissionsResponseTypeDef",
    "UpdateDataSourceRequestRequestTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "UpdateDefaultQBusinessApplicationRequestRequestTypeDef",
    "UpdateDefaultQBusinessApplicationResponseTypeDef",
    "UpdateFolderPermissionsRequestRequestTypeDef",
    "UpdateFolderPermissionsResponseTypeDef",
    "UpdateFolderRequestRequestTypeDef",
    "UpdateFolderResponseTypeDef",
    "UpdateGroupRequestRequestTypeDef",
    "UpdateGroupResponseTypeDef",
    "UpdateIAMPolicyAssignmentRequestRequestTypeDef",
    "UpdateIAMPolicyAssignmentResponseTypeDef",
    "UpdateIdentityPropagationConfigRequestRequestTypeDef",
    "UpdateIdentityPropagationConfigResponseTypeDef",
    "UpdateIpRestrictionRequestRequestTypeDef",
    "UpdateIpRestrictionResponseTypeDef",
    "UpdateKeyRegistrationRequestRequestTypeDef",
    "UpdateKeyRegistrationResponseTypeDef",
    "UpdatePublicSharingSettingsRequestRequestTypeDef",
    "UpdatePublicSharingSettingsResponseTypeDef",
    "UpdateQPersonalizationConfigurationRequestRequestTypeDef",
    "UpdateQPersonalizationConfigurationResponseTypeDef",
    "UpdateQuickSightQSearchConfigurationRequestRequestTypeDef",
    "UpdateQuickSightQSearchConfigurationResponseTypeDef",
    "UpdateRefreshScheduleRequestRequestTypeDef",
    "UpdateRefreshScheduleResponseTypeDef",
    "UpdateRoleCustomPermissionRequestRequestTypeDef",
    "UpdateRoleCustomPermissionResponseTypeDef",
    "UpdateSPICECapacityConfigurationRequestRequestTypeDef",
    "UpdateSPICECapacityConfigurationResponseTypeDef",
    "UpdateTemplateAliasRequestRequestTypeDef",
    "UpdateTemplateAliasResponseTypeDef",
    "UpdateTemplatePermissionsRequestRequestTypeDef",
    "UpdateTemplatePermissionsResponseTypeDef",
    "UpdateTemplateRequestRequestTypeDef",
    "UpdateTemplateResponseTypeDef",
    "UpdateThemeAliasRequestRequestTypeDef",
    "UpdateThemeAliasResponseTypeDef",
    "UpdateThemePermissionsRequestRequestTypeDef",
    "UpdateThemePermissionsResponseTypeDef",
    "UpdateThemeRequestRequestTypeDef",
    "UpdateThemeResponseTypeDef",
    "UpdateTopicPermissionsRequestRequestTypeDef",
    "UpdateTopicPermissionsResponseTypeDef",
    "UpdateTopicRefreshScheduleRequestRequestTypeDef",
    "UpdateTopicRefreshScheduleResponseTypeDef",
    "UpdateTopicRequestRequestTypeDef",
    "UpdateTopicResponseTypeDef",
    "UpdateUserCustomPermissionRequestRequestTypeDef",
    "UpdateUserCustomPermissionResponseTypeDef",
    "UpdateUserRequestRequestTypeDef",
    "UpdateUserResponseTypeDef",
    "UpdateVPCConnectionRequestRequestTypeDef",
    "UpdateVPCConnectionResponseTypeDef",
    "UploadSettingsTypeDef",
    "UserTypeDef",
    "VPCConnectionSummaryTypeDef",
    "VPCConnectionTypeDef",
    "ValidationStrategyTypeDef",
    "VisibleRangeOptionsTypeDef",
    "VisualAxisSortOptionTypeDef",
    "VisualCustomActionOperationOutputTypeDef",
    "VisualCustomActionOperationTypeDef",
    "VisualCustomActionOperationUnionTypeDef",
    "VisualCustomActionOutputTypeDef",
    "VisualCustomActionTypeDef",
    "VisualCustomActionUnionTypeDef",
    "VisualInteractionOptionsTypeDef",
    "VisualMenuOptionTypeDef",
    "VisualOptionsTypeDef",
    "VisualOutputTypeDef",
    "VisualPaletteOutputTypeDef",
    "VisualPaletteTypeDef",
    "VisualPaletteUnionTypeDef",
    "VisualSubtitleLabelOptionsTypeDef",
    "VisualTitleLabelOptionsTypeDef",
    "VisualTypeDef",
    "VisualUnionTypeDef",
    "VpcConnectionPropertiesTypeDef",
    "WaterfallChartAggregatedFieldWellsOutputTypeDef",
    "WaterfallChartAggregatedFieldWellsTypeDef",
    "WaterfallChartAggregatedFieldWellsUnionTypeDef",
    "WaterfallChartColorConfigurationTypeDef",
    "WaterfallChartConfigurationOutputTypeDef",
    "WaterfallChartConfigurationTypeDef",
    "WaterfallChartConfigurationUnionTypeDef",
    "WaterfallChartFieldWellsOutputTypeDef",
    "WaterfallChartFieldWellsTypeDef",
    "WaterfallChartFieldWellsUnionTypeDef",
    "WaterfallChartGroupColorConfigurationTypeDef",
    "WaterfallChartOptionsTypeDef",
    "WaterfallChartSortConfigurationOutputTypeDef",
    "WaterfallChartSortConfigurationTypeDef",
    "WaterfallChartSortConfigurationUnionTypeDef",
    "WaterfallVisualOutputTypeDef",
    "WaterfallVisualTypeDef",
    "WaterfallVisualUnionTypeDef",
    "WhatIfPointScenarioOutputTypeDef",
    "WhatIfPointScenarioTypeDef",
    "WhatIfPointScenarioUnionTypeDef",
    "WhatIfRangeScenarioOutputTypeDef",
    "WhatIfRangeScenarioTypeDef",
    "WhatIfRangeScenarioUnionTypeDef",
    "WordCloudAggregatedFieldWellsOutputTypeDef",
    "WordCloudAggregatedFieldWellsTypeDef",
    "WordCloudAggregatedFieldWellsUnionTypeDef",
    "WordCloudChartConfigurationOutputTypeDef",
    "WordCloudChartConfigurationTypeDef",
    "WordCloudChartConfigurationUnionTypeDef",
    "WordCloudFieldWellsOutputTypeDef",
    "WordCloudFieldWellsTypeDef",
    "WordCloudFieldWellsUnionTypeDef",
    "WordCloudOptionsTypeDef",
    "WordCloudSortConfigurationOutputTypeDef",
    "WordCloudSortConfigurationTypeDef",
    "WordCloudSortConfigurationUnionTypeDef",
    "WordCloudVisualOutputTypeDef",
    "WordCloudVisualTypeDef",
    "WordCloudVisualUnionTypeDef",
    "YAxisOptionsTypeDef",
)


class AccountCustomizationTypeDef(TypedDict):
    DefaultTheme: NotRequired[str]
    DefaultEmailCustomizationTemplate: NotRequired[str]


class AccountInfoTypeDef(TypedDict):
    AccountName: NotRequired[str]
    Edition: NotRequired[EditionType]
    NotificationEmail: NotRequired[str]
    AuthenticationType: NotRequired[str]
    AccountSubscriptionStatus: NotRequired[str]
    IAMIdentityCenterInstanceArn: NotRequired[str]


class AccountSettingsTypeDef(TypedDict):
    AccountName: NotRequired[str]
    Edition: NotRequired[EditionType]
    DefaultNamespace: NotRequired[str]
    NotificationEmail: NotRequired[str]
    PublicSharingEnabled: NotRequired[bool]
    TerminationProtectionEnabled: NotRequired[bool]


class ActiveIAMPolicyAssignmentTypeDef(TypedDict):
    AssignmentName: NotRequired[str]
    PolicyArn: NotRequired[str]


class AdHocFilteringOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class AggFunctionOutputTypeDef(TypedDict):
    Aggregation: NotRequired[AggTypeType]
    AggregationFunctionParameters: NotRequired[Dict[str, str]]
    Period: NotRequired[TopicTimeGranularityType]
    PeriodField: NotRequired[str]


class AggFunctionTypeDef(TypedDict):
    Aggregation: NotRequired[AggTypeType]
    AggregationFunctionParameters: NotRequired[Mapping[str, str]]
    Period: NotRequired[TopicTimeGranularityType]
    PeriodField: NotRequired[str]


class AttributeAggregationFunctionTypeDef(TypedDict):
    SimpleAttributeAggregation: NotRequired[Literal["UNIQUE_VALUE"]]
    ValueForMultipleValues: NotRequired[str]


class AggregationPartitionByTypeDef(TypedDict):
    FieldName: NotRequired[str]
    TimeGranularity: NotRequired[TimeGranularityType]


class ColumnIdentifierTypeDef(TypedDict):
    DataSetIdentifier: str
    ColumnName: str


class AmazonElasticsearchParametersTypeDef(TypedDict):
    Domain: str


class AmazonOpenSearchParametersTypeDef(TypedDict):
    Domain: str


class AssetOptionsTypeDef(TypedDict):
    Timezone: NotRequired[str]
    WeekStart: NotRequired[DayOfTheWeekType]


class CalculatedFieldTypeDef(TypedDict):
    DataSetIdentifier: str
    Name: str
    Expression: str


class DataSetIdentifierDeclarationTypeDef(TypedDict):
    Identifier: str
    DataSetArn: str


class QueryExecutionOptionsTypeDef(TypedDict):
    QueryExecutionMode: NotRequired[QueryExecutionModeType]


class EntityTypeDef(TypedDict):
    Path: NotRequired[str]


class AnalysisSearchFilterTypeDef(TypedDict):
    Operator: NotRequired[FilterOperatorType]
    Name: NotRequired[AnalysisFilterAttributeType]
    Value: NotRequired[str]


class DataSetReferenceTypeDef(TypedDict):
    DataSetPlaceholder: str
    DataSetArn: str


class AnalysisSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    AnalysisId: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ResourceStatusType]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class AnchorDateConfigurationTypeDef(TypedDict):
    AnchorOption: NotRequired[Literal["NOW"]]
    ParameterName: NotRequired[str]


class AnchorTypeDef(TypedDict):
    AnchorType: NotRequired[Literal["TODAY"]]
    TimeGranularity: NotRequired[TimeGranularityType]
    Offset: NotRequired[int]


class SharedViewConfigurationsTypeDef(TypedDict):
    Enabled: bool


class DashboardVisualIdTypeDef(TypedDict):
    DashboardId: str
    SheetId: str
    VisualId: str


class AnonymousUserGenerativeQnAEmbeddingConfigurationTypeDef(TypedDict):
    InitialTopicId: str


class AnonymousUserQSearchBarEmbeddingConfigurationTypeDef(TypedDict):
    InitialTopicId: str


class ArcAxisDisplayRangeTypeDef(TypedDict):
    Min: NotRequired[float]
    Max: NotRequired[float]


class ArcConfigurationTypeDef(TypedDict):
    ArcAngle: NotRequired[float]
    ArcThickness: NotRequired[ArcThicknessOptionsType]


class ArcOptionsTypeDef(TypedDict):
    ArcThickness: NotRequired[ArcThicknessType]


class AssetBundleExportJobAnalysisOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: List[Literal["Name"]]


class AssetBundleExportJobDashboardOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: List[Literal["Name"]]


class AssetBundleExportJobDataSetOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: List[Literal["Name"]]


class AssetBundleExportJobDataSourceOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: List[AssetBundleExportJobDataSourcePropertyToOverrideType]


class AssetBundleExportJobFolderOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: List[AssetBundleExportJobFolderPropertyToOverrideType]


class AssetBundleExportJobRefreshScheduleOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: List[Literal["StartAfterDateTime"]]


class AssetBundleExportJobResourceIdOverrideConfigurationTypeDef(TypedDict):
    PrefixForAllResources: NotRequired[bool]


class AssetBundleExportJobThemeOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: List[Literal["Name"]]


class AssetBundleExportJobVPCConnectionOverridePropertiesOutputTypeDef(TypedDict):
    Arn: str
    Properties: List[AssetBundleExportJobVPCConnectionPropertyToOverrideType]


class AssetBundleExportJobAnalysisOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[Literal["Name"]]


class AssetBundleExportJobDashboardOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[Literal["Name"]]


class AssetBundleExportJobDataSetOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[Literal["Name"]]


class AssetBundleExportJobDataSourceOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[AssetBundleExportJobDataSourcePropertyToOverrideType]


AssetBundleExportJobErrorTypeDef = TypedDict(
    "AssetBundleExportJobErrorTypeDef",
    {
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "Message": NotRequired[str],
    },
)


class AssetBundleExportJobFolderOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[AssetBundleExportJobFolderPropertyToOverrideType]


class AssetBundleExportJobRefreshScheduleOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[Literal["StartAfterDateTime"]]


class AssetBundleExportJobSummaryTypeDef(TypedDict):
    JobStatus: NotRequired[AssetBundleExportJobStatusType]
    Arn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    AssetBundleExportJobId: NotRequired[str]
    IncludeAllDependencies: NotRequired[bool]
    ExportFormat: NotRequired[AssetBundleExportFormatType]
    IncludePermissions: NotRequired[bool]
    IncludeTags: NotRequired[bool]


class AssetBundleExportJobThemeOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[Literal["Name"]]


class AssetBundleExportJobVPCConnectionOverridePropertiesTypeDef(TypedDict):
    Arn: str
    Properties: Sequence[AssetBundleExportJobVPCConnectionPropertyToOverrideType]


class AssetBundleExportJobValidationStrategyTypeDef(TypedDict):
    StrictModeForAllResources: NotRequired[bool]


class AssetBundleExportJobWarningTypeDef(TypedDict):
    Arn: NotRequired[str]
    Message: NotRequired[str]


class AssetBundleImportJobAnalysisOverrideParametersTypeDef(TypedDict):
    AnalysisId: str
    Name: NotRequired[str]


class AssetBundleResourcePermissionsOutputTypeDef(TypedDict):
    Principals: List[str]
    Actions: List[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: str


class AssetBundleImportJobDashboardOverrideParametersTypeDef(TypedDict):
    DashboardId: str
    Name: NotRequired[str]


class AssetBundleImportJobDataSetOverrideParametersTypeDef(TypedDict):
    DataSetId: str
    Name: NotRequired[str]


class AssetBundleImportJobDataSourceCredentialPairTypeDef(TypedDict):
    Username: str
    Password: str


class SslPropertiesTypeDef(TypedDict):
    DisableSsl: NotRequired[bool]


class VpcConnectionPropertiesTypeDef(TypedDict):
    VpcConnectionArn: str


AssetBundleImportJobErrorTypeDef = TypedDict(
    "AssetBundleImportJobErrorTypeDef",
    {
        "Arn": NotRequired[str],
        "Type": NotRequired[str],
        "Message": NotRequired[str],
    },
)


class AssetBundleImportJobFolderOverrideParametersTypeDef(TypedDict):
    FolderId: str
    Name: NotRequired[str]
    ParentFolderArn: NotRequired[str]


class AssetBundleImportJobRefreshScheduleOverrideParametersOutputTypeDef(TypedDict):
    DataSetId: str
    ScheduleId: str
    StartAfterDateTime: NotRequired[datetime]


class AssetBundleImportJobResourceIdOverrideConfigurationTypeDef(TypedDict):
    PrefixForAllResources: NotRequired[str]


class AssetBundleImportJobThemeOverrideParametersTypeDef(TypedDict):
    ThemeId: str
    Name: NotRequired[str]


class AssetBundleImportJobVPCConnectionOverrideParametersOutputTypeDef(TypedDict):
    VPCConnectionId: str
    Name: NotRequired[str]
    SubnetIds: NotRequired[List[str]]
    SecurityGroupIds: NotRequired[List[str]]
    DnsResolvers: NotRequired[List[str]]
    RoleArn: NotRequired[str]


class AssetBundleImportJobOverrideValidationStrategyTypeDef(TypedDict):
    StrictModeForAllResources: NotRequired[bool]


TimestampTypeDef = Union[datetime, str]


class AssetBundleImportJobSummaryTypeDef(TypedDict):
    JobStatus: NotRequired[AssetBundleImportJobStatusType]
    Arn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    AssetBundleImportJobId: NotRequired[str]
    FailureAction: NotRequired[AssetBundleImportFailureActionType]


class AssetBundleImportJobVPCConnectionOverrideParametersTypeDef(TypedDict):
    VPCConnectionId: str
    Name: NotRequired[str]
    SubnetIds: NotRequired[Sequence[str]]
    SecurityGroupIds: NotRequired[Sequence[str]]
    DnsResolvers: NotRequired[Sequence[str]]
    RoleArn: NotRequired[str]


class AssetBundleImportJobWarningTypeDef(TypedDict):
    Arn: NotRequired[str]
    Message: NotRequired[str]


class AssetBundleImportSourceDescriptionTypeDef(TypedDict):
    Body: NotRequired[str]
    S3Uri: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class AssetBundleResourcePermissionsTypeDef(TypedDict):
    Principals: Sequence[str]
    Actions: Sequence[str]


class AthenaParametersTypeDef(TypedDict):
    WorkGroup: NotRequired[str]
    RoleArn: NotRequired[str]


class AuroraParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class AuroraPostgreSqlParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class AuthorizedTargetsByServiceTypeDef(TypedDict):
    Service: NotRequired[ServiceTypeType]
    AuthorizedTargets: NotRequired[List[str]]


class AwsIotAnalyticsParametersTypeDef(TypedDict):
    DataSetName: str


class DateAxisOptionsTypeDef(TypedDict):
    MissingDateVisibility: NotRequired[VisibilityType]


class AxisDisplayMinMaxRangeTypeDef(TypedDict):
    Minimum: NotRequired[float]
    Maximum: NotRequired[float]


class AxisLinearScaleTypeDef(TypedDict):
    StepCount: NotRequired[int]
    StepSize: NotRequired[float]


class AxisLogarithmicScaleTypeDef(TypedDict):
    Base: NotRequired[float]


class ItemsLimitConfigurationTypeDef(TypedDict):
    ItemsLimit: NotRequired[int]
    OtherCategories: NotRequired[OtherCategoriesType]


class InvalidTopicReviewedAnswerTypeDef(TypedDict):
    AnswerId: NotRequired[str]
    Error: NotRequired[ReviewedAnswerErrorCodeType]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class SucceededTopicReviewedAnswerTypeDef(TypedDict):
    AnswerId: NotRequired[str]


class BatchDeleteTopicReviewedAnswerRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    AnswerIds: NotRequired[Sequence[str]]


class BigQueryParametersTypeDef(TypedDict):
    ProjectId: str
    DataSetRegion: NotRequired[str]


class BinCountOptionsTypeDef(TypedDict):
    Value: NotRequired[int]


class BinWidthOptionsTypeDef(TypedDict):
    Value: NotRequired[float]
    BinCountLimit: NotRequired[int]


class SectionAfterPageBreakTypeDef(TypedDict):
    Status: NotRequired[SectionPageBreakStatusType]


class BookmarksConfigurationsTypeDef(TypedDict):
    Enabled: bool


class BorderStyleTypeDef(TypedDict):
    Show: NotRequired[bool]


class BoxPlotStyleOptionsTypeDef(TypedDict):
    FillStyle: NotRequired[BoxPlotFillStyleType]


class PaginationConfigurationTypeDef(TypedDict):
    PageSize: int
    PageNumber: int


class PaletteTypeDef(TypedDict):
    Foreground: NotRequired[str]
    Background: NotRequired[str]


class BrandSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    BrandId: NotRequired[str]
    BrandName: NotRequired[str]
    Description: NotRequired[str]
    BrandStatus: NotRequired[BrandStatusType]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class CalculatedColumnTypeDef(TypedDict):
    ColumnName: str
    ColumnId: str
    Expression: str


class CalculatedMeasureFieldTypeDef(TypedDict):
    FieldId: str
    Expression: str


class CancelIngestionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    IngestionId: str


class CapabilitiesTypeDef(TypedDict):
    ExportToCsv: NotRequired[Literal["DENY"]]
    ExportToExcel: NotRequired[Literal["DENY"]]
    CreateAndUpdateThemes: NotRequired[Literal["DENY"]]
    AddOrRunAnomalyDetectionForAnalyses: NotRequired[Literal["DENY"]]
    ShareAnalyses: NotRequired[Literal["DENY"]]
    CreateAndUpdateDatasets: NotRequired[Literal["DENY"]]
    ShareDatasets: NotRequired[Literal["DENY"]]
    SubscribeDashboardEmailReports: NotRequired[Literal["DENY"]]
    CreateAndUpdateDashboardEmailReports: NotRequired[Literal["DENY"]]
    ShareDashboards: NotRequired[Literal["DENY"]]
    CreateAndUpdateThresholdAlerts: NotRequired[Literal["DENY"]]
    RenameSharedFolders: NotRequired[Literal["DENY"]]
    CreateSharedFolders: NotRequired[Literal["DENY"]]
    CreateAndUpdateDataSources: NotRequired[Literal["DENY"]]
    ShareDataSources: NotRequired[Literal["DENY"]]
    ViewAccountSPICECapacity: NotRequired[Literal["DENY"]]
    CreateSPICEDataset: NotRequired[Literal["DENY"]]


class CastColumnTypeOperationTypeDef(TypedDict):
    ColumnName: str
    NewColumnType: ColumnDataTypeType
    SubType: NotRequired[ColumnDataSubTypeType]
    Format: NotRequired[str]


class CustomFilterConfigurationTypeDef(TypedDict):
    MatchOperator: CategoryFilterMatchOperatorType
    NullOption: FilterNullOptionType
    CategoryValue: NotRequired[str]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    ParameterName: NotRequired[str]


class CustomFilterListConfigurationOutputTypeDef(TypedDict):
    MatchOperator: CategoryFilterMatchOperatorType
    NullOption: FilterNullOptionType
    CategoryValues: NotRequired[List[str]]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]


class FilterListConfigurationOutputTypeDef(TypedDict):
    MatchOperator: CategoryFilterMatchOperatorType
    CategoryValues: NotRequired[List[str]]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    NullOption: NotRequired[FilterNullOptionType]


class CellValueSynonymOutputTypeDef(TypedDict):
    CellValue: NotRequired[str]
    Synonyms: NotRequired[List[str]]


class CellValueSynonymTypeDef(TypedDict):
    CellValue: NotRequired[str]
    Synonyms: NotRequired[Sequence[str]]


class SimpleClusterMarkerTypeDef(TypedDict):
    Color: NotRequired[str]


class CollectiveConstantEntryTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    Value: NotRequired[str]


class CollectiveConstantOutputTypeDef(TypedDict):
    ValueList: NotRequired[List[str]]


class CollectiveConstantTypeDef(TypedDict):
    ValueList: NotRequired[Sequence[str]]


class DataColorTypeDef(TypedDict):
    Color: NotRequired[str]
    DataValue: NotRequired[float]


class CustomColorTypeDef(TypedDict):
    Color: str
    FieldValue: NotRequired[str]
    SpecialValue: NotRequired[SpecialValueType]


ColumnDescriptionTypeDef = TypedDict(
    "ColumnDescriptionTypeDef",
    {
        "Text": NotRequired[str],
    },
)


class ColumnGroupColumnSchemaTypeDef(TypedDict):
    Name: NotRequired[str]


class GeoSpatialColumnGroupOutputTypeDef(TypedDict):
    Name: str
    Columns: List[str]
    CountryCode: NotRequired[Literal["US"]]


class ColumnLevelPermissionRuleOutputTypeDef(TypedDict):
    Principals: NotRequired[List[str]]
    ColumnNames: NotRequired[List[str]]


class ColumnLevelPermissionRuleTypeDef(TypedDict):
    Principals: NotRequired[Sequence[str]]
    ColumnNames: NotRequired[Sequence[str]]


class ColumnSchemaTypeDef(TypedDict):
    Name: NotRequired[str]
    DataType: NotRequired[str]
    GeographicRole: NotRequired[str]


class ComparativeOrderOutputTypeDef(TypedDict):
    UseOrdering: NotRequired[ColumnOrderingTypeType]
    SpecifedOrder: NotRequired[List[str]]
    TreatUndefinedSpecifiedValues: NotRequired[UndefinedSpecifiedValueTypeType]


class ComparativeOrderTypeDef(TypedDict):
    UseOrdering: NotRequired[ColumnOrderingTypeType]
    SpecifedOrder: NotRequired[Sequence[str]]
    TreatUndefinedSpecifiedValues: NotRequired[UndefinedSpecifiedValueTypeType]


class ConditionalFormattingSolidColorTypeDef(TypedDict):
    Expression: str
    Color: NotRequired[str]


class ConditionalFormattingCustomIconOptionsTypeDef(TypedDict):
    Icon: NotRequired[IconType]
    UnicodeIcon: NotRequired[str]


class ConditionalFormattingIconDisplayConfigurationTypeDef(TypedDict):
    IconDisplayOption: NotRequired[Literal["ICON_ONLY"]]


class ConditionalFormattingIconSetTypeDef(TypedDict):
    Expression: str
    IconSetType: NotRequired[ConditionalFormattingIconSetTypeType]


class ContextMenuOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class ContributionAnalysisFactorTypeDef(TypedDict):
    FieldName: NotRequired[str]


class CreateAccountSubscriptionRequestRequestTypeDef(TypedDict):
    AuthenticationMethod: AuthenticationMethodOptionType
    AwsAccountId: str
    AccountName: str
    NotificationEmail: str
    Edition: NotRequired[EditionType]
    ActiveDirectoryName: NotRequired[str]
    Realm: NotRequired[str]
    DirectoryId: NotRequired[str]
    AdminGroup: NotRequired[Sequence[str]]
    AuthorGroup: NotRequired[Sequence[str]]
    ReaderGroup: NotRequired[Sequence[str]]
    AdminProGroup: NotRequired[Sequence[str]]
    AuthorProGroup: NotRequired[Sequence[str]]
    ReaderProGroup: NotRequired[Sequence[str]]
    FirstName: NotRequired[str]
    LastName: NotRequired[str]
    EmailAddress: NotRequired[str]
    ContactNumber: NotRequired[str]
    IAMIdentityCenterInstanceArn: NotRequired[str]


class SignupResponseTypeDef(TypedDict):
    IAMUser: NotRequired[bool]
    userLoginName: NotRequired[str]
    accountName: NotRequired[str]
    directoryType: NotRequired[str]


class ValidationStrategyTypeDef(TypedDict):
    Mode: ValidationStrategyModeType


class ResourcePermissionTypeDef(TypedDict):
    Principal: str
    Actions: Sequence[str]


class DataSetUsageConfigurationTypeDef(TypedDict):
    DisableUseAsDirectQuerySource: NotRequired[bool]
    DisableUseAsImportedSource: NotRequired[bool]


class RowLevelPermissionDataSetTypeDef(TypedDict):
    Arn: str
    PermissionPolicy: RowLevelPermissionPolicyType
    Namespace: NotRequired[str]
    FormatVersion: NotRequired[RowLevelPermissionFormatVersionType]
    Status: NotRequired[StatusType]


class CreateFolderMembershipRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    MemberId: str
    MemberType: MemberTypeType


class FolderMemberTypeDef(TypedDict):
    MemberId: NotRequired[str]
    MemberType: NotRequired[MemberTypeType]


class CreateGroupMembershipRequestRequestTypeDef(TypedDict):
    MemberName: str
    GroupName: str
    AwsAccountId: str
    Namespace: str


class GroupMemberTypeDef(TypedDict):
    Arn: NotRequired[str]
    MemberName: NotRequired[str]


class CreateGroupRequestRequestTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str
    Description: NotRequired[str]


class GroupTypeDef(TypedDict):
    Arn: NotRequired[str]
    GroupName: NotRequired[str]
    Description: NotRequired[str]
    PrincipalId: NotRequired[str]


class CreateIAMPolicyAssignmentRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssignmentName: str
    AssignmentStatus: AssignmentStatusType
    Namespace: str
    PolicyArn: NotRequired[str]
    Identities: NotRequired[Mapping[str, Sequence[str]]]


class CreateIngestionRequestRequestTypeDef(TypedDict):
    DataSetId: str
    IngestionId: str
    AwsAccountId: str
    IngestionType: NotRequired[IngestionTypeType]


class CreateRoleMembershipRequestRequestTypeDef(TypedDict):
    MemberName: str
    AwsAccountId: str
    Namespace: str
    Role: RoleType


class CreateTemplateAliasRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    AliasName: str
    TemplateVersionNumber: int


class TemplateAliasTypeDef(TypedDict):
    AliasName: NotRequired[str]
    Arn: NotRequired[str]
    TemplateVersionNumber: NotRequired[int]


class CreateThemeAliasRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    AliasName: str
    ThemeVersionNumber: int


class ThemeAliasTypeDef(TypedDict):
    Arn: NotRequired[str]
    AliasName: NotRequired[str]
    ThemeVersionNumber: NotRequired[int]


class DecimalPlacesConfigurationTypeDef(TypedDict):
    DecimalPlaces: int


class NegativeValueConfigurationTypeDef(TypedDict):
    DisplayMode: NegativeValueDisplayModeType


class NullValueFormatConfigurationTypeDef(TypedDict):
    NullString: str


class LocalNavigationConfigurationTypeDef(TypedDict):
    TargetSheetId: str


class CustomActionURLOperationTypeDef(TypedDict):
    URLTemplate: str
    URLTarget: URLTargetConfigurationType


class CustomFilterListConfigurationTypeDef(TypedDict):
    MatchOperator: CategoryFilterMatchOperatorType
    NullOption: FilterNullOptionType
    CategoryValues: NotRequired[Sequence[str]]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]


class CustomNarrativeOptionsTypeDef(TypedDict):
    Narrative: str


class CustomParameterValuesOutputTypeDef(TypedDict):
    StringValues: NotRequired[List[str]]
    IntegerValues: NotRequired[List[int]]
    DecimalValues: NotRequired[List[float]]
    DateTimeValues: NotRequired[List[datetime]]


InputColumnTypeDef = TypedDict(
    "InputColumnTypeDef",
    {
        "Name": str,
        "Type": InputColumnDataTypeType,
        "SubType": NotRequired[ColumnDataSubTypeType],
    },
)


class DataPointDrillUpDownOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class DataPointMenuLabelOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class DataPointTooltipOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class ExportToCSVOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class ExportWithHiddenFieldsOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class SheetControlsOptionTypeDef(TypedDict):
    VisibilityState: NotRequired[DashboardUIStateType]


class SheetLayoutElementMaximizationOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class VisualAxisSortOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class VisualMenuOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class DashboardSearchFilterTypeDef(TypedDict):
    Operator: FilterOperatorType
    Name: NotRequired[DashboardFilterAttributeType]
    Value: NotRequired[str]


class DashboardSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    DashboardId: NotRequired[str]
    Name: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    PublishedVersionNumber: NotRequired[int]
    LastPublishedTime: NotRequired[datetime]


class DashboardVersionSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    VersionNumber: NotRequired[int]
    Status: NotRequired[ResourceStatusType]
    SourceEntityArn: NotRequired[str]
    Description: NotRequired[str]


class ExportHiddenFieldsOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class DashboardVisualResultTypeDef(TypedDict):
    DashboardId: NotRequired[str]
    DashboardName: NotRequired[str]
    SheetId: NotRequired[str]
    SheetName: NotRequired[str]
    VisualId: NotRequired[str]
    VisualTitle: NotRequired[str]
    VisualSubtitle: NotRequired[str]
    DashboardUrl: NotRequired[str]


class DataAggregationTypeDef(TypedDict):
    DatasetRowDateGranularity: NotRequired[TopicTimeGranularityType]
    DefaultDateColumnName: NotRequired[str]


class DataBarsOptionsTypeDef(TypedDict):
    FieldId: str
    PositiveColor: NotRequired[str]
    NegativeColor: NotRequired[str]


class DataColorPaletteOutputTypeDef(TypedDict):
    Colors: NotRequired[List[str]]
    MinMaxGradient: NotRequired[List[str]]
    EmptyFillColor: NotRequired[str]


class DataColorPaletteTypeDef(TypedDict):
    Colors: NotRequired[Sequence[str]]
    MinMaxGradient: NotRequired[Sequence[str]]
    EmptyFillColor: NotRequired[str]


class DataPathLabelTypeTypeDef(TypedDict):
    FieldId: NotRequired[str]
    FieldValue: NotRequired[str]
    Visibility: NotRequired[VisibilityType]


class FieldLabelTypeTypeDef(TypedDict):
    FieldId: NotRequired[str]
    Visibility: NotRequired[VisibilityType]


class MaximumLabelTypeTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class MinimumLabelTypeTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class RangeEndsLabelTypeTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class DataPathTypeTypeDef(TypedDict):
    PivotTableDataPathType: NotRequired[PivotTableDataPathTypeType]


class DataSetSearchFilterTypeDef(TypedDict):
    Operator: FilterOperatorType
    Name: DataSetFilterAttributeType
    Value: str


class FieldFolderOutputTypeDef(TypedDict):
    description: NotRequired[str]
    columns: NotRequired[List[str]]


OutputColumnTypeDef = TypedDict(
    "OutputColumnTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Type": NotRequired[ColumnDataTypeType],
        "SubType": NotRequired[ColumnDataSubTypeType],
    },
)
DataSourceErrorInfoTypeDef = TypedDict(
    "DataSourceErrorInfoTypeDef",
    {
        "Type": NotRequired[DataSourceErrorInfoTypeType],
        "Message": NotRequired[str],
    },
)


class DatabricksParametersTypeDef(TypedDict):
    Host: str
    Port: int
    SqlEndpointPath: str


class ExasolParametersTypeDef(TypedDict):
    Host: str
    Port: int


class JiraParametersTypeDef(TypedDict):
    SiteBaseUrl: str


class MariaDbParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class MySqlParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class OracleParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class PostgreSqlParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class PrestoParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Catalog: str


class RdsParametersTypeDef(TypedDict):
    InstanceId: str
    Database: str


class ServiceNowParametersTypeDef(TypedDict):
    SiteBaseUrl: str


class SparkParametersTypeDef(TypedDict):
    Host: str
    Port: int


class SqlServerParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class TeradataParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Database: str


class TrinoParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Catalog: str


class TwitterParametersTypeDef(TypedDict):
    Query: str
    MaxRows: int


class DataSourceSearchFilterTypeDef(TypedDict):
    Operator: FilterOperatorType
    Name: DataSourceFilterAttributeType
    Value: str


DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "Arn": NotRequired[str],
        "DataSourceId": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[DataSourceTypeType],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
    },
)


class DateTimeDatasetParameterDefaultValuesOutputTypeDef(TypedDict):
    StaticValues: NotRequired[List[datetime]]


class RollingDateConfigurationTypeDef(TypedDict):
    Expression: str
    DataSetIdentifier: NotRequired[str]


class DateTimeValueWhenUnsetConfigurationOutputTypeDef(TypedDict):
    ValueWhenUnsetOption: NotRequired[ValueWhenUnsetOptionType]
    CustomValue: NotRequired[datetime]


class MappedDataSetParameterTypeDef(TypedDict):
    DataSetIdentifier: str
    DataSetParameterName: str


class DateTimeParameterOutputTypeDef(TypedDict):
    Name: str
    Values: List[datetime]


class SheetControlInfoIconLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    InfoIconText: NotRequired[str]


class DecimalDatasetParameterDefaultValuesOutputTypeDef(TypedDict):
    StaticValues: NotRequired[List[float]]


class DecimalDatasetParameterDefaultValuesTypeDef(TypedDict):
    StaticValues: NotRequired[Sequence[float]]


class DecimalValueWhenUnsetConfigurationTypeDef(TypedDict):
    ValueWhenUnsetOption: NotRequired[ValueWhenUnsetOptionType]
    CustomValue: NotRequired[float]


class DecimalParameterOutputTypeDef(TypedDict):
    Name: str
    Values: List[float]


class DecimalParameterTypeDef(TypedDict):
    Name: str
    Values: Sequence[float]


class FilterSelectableValuesOutputTypeDef(TypedDict):
    Values: NotRequired[List[str]]


class DeleteAccountCustomizationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: NotRequired[str]


class DeleteAccountSubscriptionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str


class DeleteAnalysisRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str
    RecoveryWindowInDays: NotRequired[int]
    ForceDeleteWithoutRecovery: NotRequired[bool]


class DeleteBrandAssignmentRequestRequestTypeDef(TypedDict):
    AwsAccountId: str


class DeleteBrandRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str


class DeleteCustomPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    CustomPermissionsName: str


class DeleteDashboardRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    VersionNumber: NotRequired[int]


class DeleteDataSetRefreshPropertiesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class DeleteDataSetRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class DeleteDataSourceRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSourceId: str


class DeleteDefaultQBusinessApplicationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: NotRequired[str]


class DeleteFolderMembershipRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    MemberId: str
    MemberType: MemberTypeType


class DeleteFolderRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str


class DeleteGroupMembershipRequestRequestTypeDef(TypedDict):
    MemberName: str
    GroupName: str
    AwsAccountId: str
    Namespace: str


class DeleteGroupRequestRequestTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str


class DeleteIAMPolicyAssignmentRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssignmentName: str
    Namespace: str


class DeleteIdentityPropagationConfigRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Service: ServiceTypeType


class DeleteNamespaceRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str


class DeleteRefreshScheduleRequestRequestTypeDef(TypedDict):
    DataSetId: str
    AwsAccountId: str
    ScheduleId: str


class DeleteRoleCustomPermissionRequestRequestTypeDef(TypedDict):
    Role: RoleType
    AwsAccountId: str
    Namespace: str


class DeleteRoleMembershipRequestRequestTypeDef(TypedDict):
    MemberName: str
    Role: RoleType
    AwsAccountId: str
    Namespace: str


class DeleteTemplateAliasRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    AliasName: str


class DeleteTemplateRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    VersionNumber: NotRequired[int]


class DeleteThemeAliasRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    AliasName: str


class DeleteThemeRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    VersionNumber: NotRequired[int]


class DeleteTopicRefreshScheduleRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    DatasetId: str


class DeleteTopicRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str


class DeleteUserByPrincipalIdRequestRequestTypeDef(TypedDict):
    PrincipalId: str
    AwsAccountId: str
    Namespace: str


class DeleteUserCustomPermissionRequestRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str


class DeleteUserRequestRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str


class DeleteVPCConnectionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    VPCConnectionId: str


class DescribeAccountCustomizationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: NotRequired[str]
    Resolved: NotRequired[bool]


class DescribeAccountSettingsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeAccountSubscriptionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeAnalysisDefinitionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str


class DescribeAnalysisPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str


class ResourcePermissionOutputTypeDef(TypedDict):
    Principal: str
    Actions: List[str]


class DescribeAnalysisRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str


class DescribeAssetBundleExportJobRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssetBundleExportJobId: str


class DescribeAssetBundleImportJobRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssetBundleImportJobId: str


class DescribeBrandAssignmentRequestRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeBrandPublishedVersionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str


class DescribeBrandRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str
    VersionId: NotRequired[str]


class DescribeCustomPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    CustomPermissionsName: str


class DescribeDashboardDefinitionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    VersionNumber: NotRequired[int]
    AliasName: NotRequired[str]


class DescribeDashboardPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str


class DescribeDashboardRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    VersionNumber: NotRequired[int]
    AliasName: NotRequired[str]


class DescribeDashboardSnapshotJobRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    SnapshotJobId: str


class DescribeDashboardSnapshotJobResultRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    SnapshotJobId: str


class SnapshotJobErrorInfoTypeDef(TypedDict):
    ErrorMessage: NotRequired[str]
    ErrorType: NotRequired[str]


class DescribeDashboardsQAConfigurationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeDataSetPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class DescribeDataSetRefreshPropertiesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class DescribeDataSetRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class DescribeDataSourcePermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSourceId: str


class DescribeDataSourceRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSourceId: str


class DescribeDefaultQBusinessApplicationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeFolderPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Namespace: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeFolderRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str


class DescribeFolderResolvedPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Namespace: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class FolderTypeDef(TypedDict):
    FolderId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    FolderType: NotRequired[FolderTypeType]
    FolderPath: NotRequired[List[str]]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    SharingModel: NotRequired[SharingModelType]


class DescribeGroupMembershipRequestRequestTypeDef(TypedDict):
    MemberName: str
    GroupName: str
    AwsAccountId: str
    Namespace: str


class DescribeGroupRequestRequestTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str


class DescribeIAMPolicyAssignmentRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssignmentName: str
    Namespace: str


class IAMPolicyAssignmentTypeDef(TypedDict):
    AwsAccountId: NotRequired[str]
    AssignmentId: NotRequired[str]
    AssignmentName: NotRequired[str]
    PolicyArn: NotRequired[str]
    Identities: NotRequired[Dict[str, List[str]]]
    AssignmentStatus: NotRequired[AssignmentStatusType]


class DescribeIngestionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    IngestionId: str


class DescribeIpRestrictionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeKeyRegistrationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DefaultKeyOnly: NotRequired[bool]


class RegisteredCustomerManagedKeyTypeDef(TypedDict):
    KeyArn: NotRequired[str]
    DefaultKey: NotRequired[bool]


class DescribeNamespaceRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str


class DescribeQPersonalizationConfigurationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeQuickSightQSearchConfigurationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str


class DescribeRefreshScheduleRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    ScheduleId: str


class DescribeRoleCustomPermissionRequestRequestTypeDef(TypedDict):
    Role: RoleType
    AwsAccountId: str
    Namespace: str


class DescribeTemplateAliasRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    AliasName: str


class DescribeTemplateDefinitionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    VersionNumber: NotRequired[int]
    AliasName: NotRequired[str]


class DescribeTemplatePermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str


class DescribeTemplateRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    VersionNumber: NotRequired[int]
    AliasName: NotRequired[str]


class DescribeThemeAliasRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    AliasName: str


class DescribeThemePermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str


class DescribeThemeRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    VersionNumber: NotRequired[int]
    AliasName: NotRequired[str]


class DescribeTopicPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str


class DescribeTopicRefreshRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    RefreshId: str


class TopicRefreshDetailsTypeDef(TypedDict):
    RefreshArn: NotRequired[str]
    RefreshId: NotRequired[str]
    RefreshStatus: NotRequired[TopicRefreshStatusType]


class DescribeTopicRefreshScheduleRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    DatasetId: str


class TopicRefreshScheduleOutputTypeDef(TypedDict):
    IsEnabled: bool
    BasedOnSpiceSchedule: bool
    StartingAt: NotRequired[datetime]
    Timezone: NotRequired[str]
    RepeatAt: NotRequired[str]
    TopicScheduleType: NotRequired[TopicScheduleTypeType]


class DescribeTopicRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str


class DescribeUserRequestRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str


class UserTypeDef(TypedDict):
    Arn: NotRequired[str]
    UserName: NotRequired[str]
    Email: NotRequired[str]
    Role: NotRequired[UserRoleType]
    IdentityType: NotRequired[IdentityTypeType]
    Active: NotRequired[bool]
    PrincipalId: NotRequired[str]
    CustomPermissionsName: NotRequired[str]
    ExternalLoginFederationProviderType: NotRequired[str]
    ExternalLoginFederationProviderUrl: NotRequired[str]
    ExternalLoginId: NotRequired[str]


class DescribeVPCConnectionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    VPCConnectionId: str


class NegativeFormatTypeDef(TypedDict):
    Prefix: NotRequired[str]
    Suffix: NotRequired[str]


class DonutCenterOptionsTypeDef(TypedDict):
    LabelVisibility: NotRequired[VisibilityType]


class ListControlSelectAllOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "Type": NotRequired[IngestionErrorTypeType],
        "Message": NotRequired[str],
    },
)


class ExcludePeriodConfigurationTypeDef(TypedDict):
    Amount: int
    Granularity: TimeGranularityType
    Status: NotRequired[WidgetStatusType]


class FailedKeyRegistrationEntryTypeDef(TypedDict):
    Message: str
    StatusCode: int
    SenderFault: bool
    KeyArn: NotRequired[str]


class FieldFolderTypeDef(TypedDict):
    description: NotRequired[str]
    columns: NotRequired[Sequence[str]]


class FieldSortTypeDef(TypedDict):
    FieldId: str
    Direction: SortDirectionType


class FieldTooltipItemTypeDef(TypedDict):
    FieldId: str
    Label: NotRequired[str]
    Visibility: NotRequired[VisibilityType]
    TooltipTarget: NotRequired[TooltipTargetType]


class GeospatialMapStyleOptionsTypeDef(TypedDict):
    BaseMapStyle: NotRequired[BaseMapStyleTypeType]


class IdentifierTypeDef(TypedDict):
    Identity: str


class FilterListConfigurationTypeDef(TypedDict):
    MatchOperator: CategoryFilterMatchOperatorType
    CategoryValues: NotRequired[Sequence[str]]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    NullOption: NotRequired[FilterNullOptionType]


class SameSheetTargetVisualConfigurationOutputTypeDef(TypedDict):
    TargetVisuals: NotRequired[List[str]]
    TargetVisualOptions: NotRequired[Literal["ALL_VISUALS"]]


class FilterOperationTypeDef(TypedDict):
    ConditionExpression: str


class FilterSelectableValuesTypeDef(TypedDict):
    Values: NotRequired[Sequence[str]]


class FolderSearchFilterTypeDef(TypedDict):
    Operator: NotRequired[FilterOperatorType]
    Name: NotRequired[FolderFilterAttributeType]
    Value: NotRequired[str]


class FolderSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    FolderId: NotRequired[str]
    Name: NotRequired[str]
    FolderType: NotRequired[FolderTypeType]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    SharingModel: NotRequired[SharingModelType]


class FontSizeTypeDef(TypedDict):
    Relative: NotRequired[RelativeFontSizeType]
    Absolute: NotRequired[str]


class FontWeightTypeDef(TypedDict):
    Name: NotRequired[FontWeightNameType]


class FontTypeDef(TypedDict):
    FontFamily: NotRequired[str]


class TimeBasedForecastPropertiesTypeDef(TypedDict):
    PeriodsForward: NotRequired[int]
    PeriodsBackward: NotRequired[int]
    UpperBoundary: NotRequired[float]
    LowerBoundary: NotRequired[float]
    PredictionInterval: NotRequired[int]
    Seasonality: NotRequired[int]


class WhatIfPointScenarioOutputTypeDef(TypedDict):
    Date: datetime
    Value: float


class WhatIfRangeScenarioOutputTypeDef(TypedDict):
    StartDate: datetime
    EndDate: datetime
    Value: float


class FreeFormLayoutScreenCanvasSizeOptionsTypeDef(TypedDict):
    OptimizedViewPortWidth: str


class FreeFormLayoutElementBackgroundStyleTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    Color: NotRequired[str]


class FreeFormLayoutElementBorderStyleTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    Color: NotRequired[str]


class LoadingAnimationTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class GaugeChartColorConfigurationTypeDef(TypedDict):
    ForegroundColor: NotRequired[str]
    BackgroundColor: NotRequired[str]


class SessionTagTypeDef(TypedDict):
    Key: str
    Value: str


class GeneratedAnswerResultTypeDef(TypedDict):
    QuestionText: NotRequired[str]
    AnswerStatus: NotRequired[GeneratedAnswerStatusType]
    TopicId: NotRequired[str]
    TopicName: NotRequired[str]
    Restatement: NotRequired[str]
    QuestionId: NotRequired[str]
    AnswerId: NotRequired[str]
    QuestionUrl: NotRequired[str]


class GeoSpatialColumnGroupTypeDef(TypedDict):
    Name: str
    Columns: Sequence[str]
    CountryCode: NotRequired[Literal["US"]]


class GeospatialCategoricalDataColorTypeDef(TypedDict):
    Color: str
    DataValue: str


class GeospatialCircleRadiusTypeDef(TypedDict):
    Radius: NotRequired[float]


class GeospatialLineWidthTypeDef(TypedDict):
    LineWidth: NotRequired[float]


class GeospatialSolidColorTypeDef(TypedDict):
    Color: str
    State: NotRequired[GeospatialColorStateType]


class GeospatialCoordinateBoundsTypeDef(TypedDict):
    North: float
    South: float
    West: float
    East: float


class GeospatialStaticFileSourceTypeDef(TypedDict):
    StaticFileId: str


class GeospatialGradientStepColorTypeDef(TypedDict):
    Color: str
    DataValue: float


class GeospatialHeatmapDataColorTypeDef(TypedDict):
    Color: str


class GeospatialMapStyleTypeDef(TypedDict):
    BaseMapStyle: NotRequired[BaseMapStyleTypeType]
    BackgroundColor: NotRequired[str]
    BaseMapVisibility: NotRequired[VisibilityType]


class GeospatialNullSymbolStyleTypeDef(TypedDict):
    FillColor: NotRequired[str]
    StrokeColor: NotRequired[str]
    StrokeWidth: NotRequired[float]


class GetDashboardEmbedUrlRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    IdentityType: EmbeddingIdentityTypeType
    SessionLifetimeInMinutes: NotRequired[int]
    UndoRedoDisabled: NotRequired[bool]
    ResetDisabled: NotRequired[bool]
    StatePersistenceEnabled: NotRequired[bool]
    UserArn: NotRequired[str]
    Namespace: NotRequired[str]
    AdditionalDashboardIds: NotRequired[Sequence[str]]


class GetSessionEmbedUrlRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    EntryPoint: NotRequired[str]
    SessionLifetimeInMinutes: NotRequired[int]
    UserArn: NotRequired[str]


class TableBorderOptionsTypeDef(TypedDict):
    Color: NotRequired[str]
    Thickness: NotRequired[int]
    Style: NotRequired[TableBorderStyleType]


class GradientStopTypeDef(TypedDict):
    GradientOffset: float
    DataValue: NotRequired[float]
    Color: NotRequired[str]


class GridLayoutScreenCanvasSizeOptionsTypeDef(TypedDict):
    ResizeOption: ResizeOptionType
    OptimizedViewPortWidth: NotRequired[str]


class GridLayoutElementTypeDef(TypedDict):
    ElementId: str
    ElementType: LayoutElementTypeType
    ColumnSpan: int
    RowSpan: int
    ColumnIndex: NotRequired[int]
    RowIndex: NotRequired[int]


class GroupSearchFilterTypeDef(TypedDict):
    Operator: Literal["StartsWith"]
    Name: Literal["GROUP_NAME"]
    Value: str


class GutterStyleTypeDef(TypedDict):
    Show: NotRequired[bool]


class IAMPolicyAssignmentSummaryTypeDef(TypedDict):
    AssignmentName: NotRequired[str]
    AssignmentStatus: NotRequired[AssignmentStatusType]


class IdentityCenterConfigurationTypeDef(TypedDict):
    EnableIdentityPropagation: NotRequired[bool]


class ImageSourceTypeDef(TypedDict):
    PublicUrl: NotRequired[str]
    S3Uri: NotRequired[str]


class ImageMenuOptionTypeDef(TypedDict):
    AvailabilityStatus: NotRequired[DashboardBehaviorType]


class LookbackWindowTypeDef(TypedDict):
    ColumnName: str
    Size: int
    SizeUnit: LookbackWindowSizeUnitType


class QueueInfoTypeDef(TypedDict):
    WaitingOnIngestion: str
    QueuedIngestion: str


class RowInfoTypeDef(TypedDict):
    RowsIngested: NotRequired[int]
    RowsDropped: NotRequired[int]
    TotalRowsInDataset: NotRequired[int]


class IntegerDatasetParameterDefaultValuesOutputTypeDef(TypedDict):
    StaticValues: NotRequired[List[int]]


class IntegerDatasetParameterDefaultValuesTypeDef(TypedDict):
    StaticValues: NotRequired[Sequence[int]]


class IntegerValueWhenUnsetConfigurationTypeDef(TypedDict):
    ValueWhenUnsetOption: NotRequired[ValueWhenUnsetOptionType]
    CustomValue: NotRequired[int]


class IntegerParameterOutputTypeDef(TypedDict):
    Name: str
    Values: List[int]


class IntegerParameterTypeDef(TypedDict):
    Name: str
    Values: Sequence[int]


class JoinKeyPropertiesTypeDef(TypedDict):
    UniqueKey: NotRequired[bool]


KPISparklineOptionsTypeDef = TypedDict(
    "KPISparklineOptionsTypeDef",
    {
        "Type": KPISparklineTypeType,
        "Visibility": NotRequired[VisibilityType],
        "Color": NotRequired[str],
        "TooltipVisibility": NotRequired[VisibilityType],
    },
)


class ProgressBarOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class SecondaryValueOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class TrendArrowOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


KPIVisualStandardLayoutTypeDef = TypedDict(
    "KPIVisualStandardLayoutTypeDef",
    {
        "Type": KPIVisualStandardLayoutTypeType,
    },
)


class LineChartLineStyleSettingsTypeDef(TypedDict):
    LineVisibility: NotRequired[VisibilityType]
    LineInterpolation: NotRequired[LineInterpolationType]
    LineStyle: NotRequired[LineChartLineStyleType]
    LineWidth: NotRequired[str]


class LineChartMarkerStyleSettingsTypeDef(TypedDict):
    MarkerVisibility: NotRequired[VisibilityType]
    MarkerShape: NotRequired[LineChartMarkerShapeType]
    MarkerSize: NotRequired[str]
    MarkerColor: NotRequired[str]


class MissingDataConfigurationTypeDef(TypedDict):
    TreatmentOption: NotRequired[MissingDataTreatmentOptionType]


class ListAnalysesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAssetBundleExportJobsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListAssetBundleImportJobsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListBrandsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListControlSearchOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class ListCustomPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListDashboardVersionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDashboardsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDataSetsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDataSourcesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFolderMembersRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class MemberIdArnPairTypeDef(TypedDict):
    MemberId: NotRequired[str]
    MemberArn: NotRequired[str]


class ListFoldersForResourceRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ResourceArn: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListFoldersRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListGroupMembershipsRequestRequestTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListGroupsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIAMPolicyAssignmentsForUserRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    UserName: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIAMPolicyAssignmentsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    AssignmentStatus: NotRequired[AssignmentStatusType]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListIdentityPropagationConfigsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListIngestionsRequestRequestTypeDef(TypedDict):
    DataSetId: str
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListNamespacesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListRefreshSchedulesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str


class ListRoleMembershipsRequestRequestTypeDef(TypedDict):
    Role: RoleType
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str


class ListTemplateAliasesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListTemplateVersionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class TemplateVersionSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    VersionNumber: NotRequired[int]
    CreatedTime: NotRequired[datetime]
    Status: NotRequired[ResourceStatusType]
    Description: NotRequired[str]


class ListTemplatesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class TemplateSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    TemplateId: NotRequired[str]
    Name: NotRequired[str]
    LatestVersionNumber: NotRequired[int]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class ListThemeAliasesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListThemeVersionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ThemeVersionSummaryTypeDef(TypedDict):
    VersionNumber: NotRequired[int]
    Arn: NotRequired[str]
    Description: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    Status: NotRequired[ResourceStatusType]


ListThemesRequestRequestTypeDef = TypedDict(
    "ListThemesRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "Type": NotRequired[ThemeTypeType],
    },
)


class ThemeSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    ThemeId: NotRequired[str]
    LatestVersionNumber: NotRequired[int]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class ListTopicRefreshSchedulesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str


class ListTopicReviewedAnswersRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str


class ListTopicsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class TopicSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    TopicId: NotRequired[str]
    Name: NotRequired[str]
    UserExperienceVersion: NotRequired[TopicUserExperienceVersionType]


class ListUserGroupsRequestRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListUsersRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListVPCConnectionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class LongFormatTextTypeDef(TypedDict):
    PlainText: NotRequired[str]
    RichText: NotRequired[str]


class ManifestFileLocationTypeDef(TypedDict):
    Bucket: str
    Key: str


class MarginStyleTypeDef(TypedDict):
    Show: NotRequired[bool]


class NamedEntityDefinitionMetricOutputTypeDef(TypedDict):
    Aggregation: NotRequired[NamedEntityAggTypeType]
    AggregationFunctionParameters: NotRequired[Dict[str, str]]


class NamedEntityDefinitionMetricTypeDef(TypedDict):
    Aggregation: NotRequired[NamedEntityAggTypeType]
    AggregationFunctionParameters: NotRequired[Mapping[str, str]]


class NamedEntityRefTypeDef(TypedDict):
    NamedEntityName: NotRequired[str]


NamespaceErrorTypeDef = TypedDict(
    "NamespaceErrorTypeDef",
    {
        "Type": NotRequired[NamespaceErrorTypeType],
        "Message": NotRequired[str],
    },
)


class NetworkInterfaceTypeDef(TypedDict):
    SubnetId: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    ErrorMessage: NotRequired[str]
    Status: NotRequired[NetworkInterfaceStatusType]
    NetworkInterfaceId: NotRequired[str]


class NewDefaultValuesOutputTypeDef(TypedDict):
    StringStaticValues: NotRequired[List[str]]
    DecimalStaticValues: NotRequired[List[float]]
    DateTimeStaticValues: NotRequired[List[datetime]]
    IntegerStaticValues: NotRequired[List[int]]


class NumericRangeFilterValueTypeDef(TypedDict):
    StaticValue: NotRequired[float]
    Parameter: NotRequired[str]


class ThousandSeparatorOptionsTypeDef(TypedDict):
    Symbol: NotRequired[NumericSeparatorSymbolType]
    Visibility: NotRequired[VisibilityType]


class PercentileAggregationTypeDef(TypedDict):
    PercentileValue: NotRequired[float]


class StringParameterOutputTypeDef(TypedDict):
    Name: str
    Values: List[str]


class PercentVisibleRangeTypeDef(TypedDict):
    From: NotRequired[float]
    To: NotRequired[float]


class PivotTableConditionalFormattingScopeTypeDef(TypedDict):
    Role: NotRequired[PivotTableConditionalFormattingScopeRoleType]


class PivotTablePaginatedReportOptionsTypeDef(TypedDict):
    VerticalOverflowVisibility: NotRequired[VisibilityType]
    OverflowColumnHeaderVisibility: NotRequired[VisibilityType]


class PivotTableFieldOptionTypeDef(TypedDict):
    FieldId: str
    CustomLabel: NotRequired[str]
    Visibility: NotRequired[VisibilityType]


class PivotTableFieldSubtotalOptionsTypeDef(TypedDict):
    FieldId: NotRequired[str]


class PivotTableRowsLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    CustomLabel: NotRequired[str]


class RowAlternateColorOptionsOutputTypeDef(TypedDict):
    Status: NotRequired[WidgetStatusType]
    RowAlternateColors: NotRequired[List[str]]
    UsePrimaryBackgroundColor: NotRequired[WidgetStatusType]


class PluginVisualItemsLimitConfigurationTypeDef(TypedDict):
    ItemsLimit: NotRequired[int]


class PluginVisualPropertyTypeDef(TypedDict):
    Name: NotRequired[str]
    Value: NotRequired[str]


class PredictQAResultsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    QueryText: str
    IncludeQuickSightQIndex: NotRequired[IncludeQuickSightQIndexType]
    IncludeGeneratedAnswer: NotRequired[IncludeGeneratedAnswerType]
    MaxTopicsToConsider: NotRequired[int]


class ProjectOperationOutputTypeDef(TypedDict):
    ProjectedColumns: List[str]


class ProjectOperationTypeDef(TypedDict):
    ProjectedColumns: Sequence[str]


class RadarChartAreaStyleSettingsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class RangeConstantTypeDef(TypedDict):
    Minimum: NotRequired[str]
    Maximum: NotRequired[str]


class RedshiftIAMParametersOutputTypeDef(TypedDict):
    RoleArn: str
    DatabaseUser: NotRequired[str]
    DatabaseGroups: NotRequired[List[str]]
    AutoCreateDatabaseUser: NotRequired[bool]


class RedshiftIAMParametersTypeDef(TypedDict):
    RoleArn: str
    DatabaseUser: NotRequired[str]
    DatabaseGroups: NotRequired[Sequence[str]]
    AutoCreateDatabaseUser: NotRequired[bool]


class ReferenceLineCustomLabelConfigurationTypeDef(TypedDict):
    CustomLabel: str


class ReferenceLineStaticDataConfigurationTypeDef(TypedDict):
    Value: float


ReferenceLineStyleConfigurationTypeDef = TypedDict(
    "ReferenceLineStyleConfigurationTypeDef",
    {
        "Pattern": NotRequired[ReferenceLinePatternTypeType],
        "Color": NotRequired[str],
    },
)


class ScheduleRefreshOnEntityTypeDef(TypedDict):
    DayOfWeek: NotRequired[DayOfWeekType]
    DayOfMonth: NotRequired[str]


class StatePersistenceConfigurationsTypeDef(TypedDict):
    Enabled: bool


class RegisteredUserGenerativeQnAEmbeddingConfigurationTypeDef(TypedDict):
    InitialTopicId: NotRequired[str]


class RegisteredUserQSearchBarEmbeddingConfigurationTypeDef(TypedDict):
    InitialTopicId: NotRequired[str]


class RenameColumnOperationTypeDef(TypedDict):
    ColumnName: str
    NewColumnName: str


class RestoreAnalysisRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str
    RestoreToFolders: NotRequired[bool]


class RowAlternateColorOptionsTypeDef(TypedDict):
    Status: NotRequired[WidgetStatusType]
    RowAlternateColors: NotRequired[Sequence[str]]
    UsePrimaryBackgroundColor: NotRequired[WidgetStatusType]


class RowLevelPermissionTagRuleTypeDef(TypedDict):
    TagKey: str
    ColumnName: str
    TagMultiValueDelimiter: NotRequired[str]
    MatchAllValue: NotRequired[str]


class S3BucketConfigurationTypeDef(TypedDict):
    BucketName: str
    BucketPrefix: str
    BucketRegion: str


class UploadSettingsTypeDef(TypedDict):
    Format: NotRequired[FileFormatType]
    StartFromRow: NotRequired[int]
    ContainsHeader: NotRequired[bool]
    TextQualifier: NotRequired[TextQualifierType]
    Delimiter: NotRequired[str]


class SameSheetTargetVisualConfigurationTypeDef(TypedDict):
    TargetVisuals: NotRequired[Sequence[str]]
    TargetVisualOptions: NotRequired[Literal["ALL_VISUALS"]]


class TopicSearchFilterTypeDef(TypedDict):
    Operator: TopicFilterOperatorType
    Name: TopicFilterAttributeType
    Value: str


class SpacingTypeDef(TypedDict):
    Top: NotRequired[str]
    Bottom: NotRequired[str]
    Left: NotRequired[str]
    Right: NotRequired[str]


class SheetVisualScopingConfigurationOutputTypeDef(TypedDict):
    SheetId: str
    Scope: FilterVisualScopeType
    VisualIds: NotRequired[List[str]]


class SemanticEntityTypeOutputTypeDef(TypedDict):
    TypeName: NotRequired[str]
    SubTypeName: NotRequired[str]
    TypeParameters: NotRequired[Dict[str, str]]


class SemanticEntityTypeTypeDef(TypedDict):
    TypeName: NotRequired[str]
    SubTypeName: NotRequired[str]
    TypeParameters: NotRequired[Mapping[str, str]]


class SemanticTypeOutputTypeDef(TypedDict):
    TypeName: NotRequired[str]
    SubTypeName: NotRequired[str]
    TypeParameters: NotRequired[Dict[str, str]]
    TruthyCellValue: NotRequired[str]
    TruthyCellValueSynonyms: NotRequired[List[str]]
    FalseyCellValue: NotRequired[str]
    FalseyCellValueSynonyms: NotRequired[List[str]]


class SemanticTypeTypeDef(TypedDict):
    TypeName: NotRequired[str]
    SubTypeName: NotRequired[str]
    TypeParameters: NotRequired[Mapping[str, str]]
    TruthyCellValue: NotRequired[str]
    TruthyCellValueSynonyms: NotRequired[Sequence[str]]
    FalseyCellValue: NotRequired[str]
    FalseyCellValueSynonyms: NotRequired[Sequence[str]]


class SheetTextBoxTypeDef(TypedDict):
    SheetTextBoxId: str
    Content: NotRequired[str]


class SheetElementConfigurationOverridesTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


class SheetImageScalingConfigurationTypeDef(TypedDict):
    ScalingType: NotRequired[SheetImageScalingTypeType]


class SheetImageStaticFileSourceTypeDef(TypedDict):
    StaticFileId: str


class SheetImageTooltipTextTypeDef(TypedDict):
    PlainText: NotRequired[str]


class SheetVisualScopingConfigurationTypeDef(TypedDict):
    SheetId: str
    Scope: FilterVisualScopeType
    VisualIds: NotRequired[Sequence[str]]


class ShortFormatTextTypeDef(TypedDict):
    PlainText: NotRequired[str]
    RichText: NotRequired[str]


class YAxisOptionsTypeDef(TypedDict):
    YAxis: Literal["PRIMARY_Y_AXIS"]


class SlotTypeDef(TypedDict):
    SlotId: NotRequired[str]
    VisualId: NotRequired[str]


class SmallMultiplesAxisPropertiesTypeDef(TypedDict):
    Scale: NotRequired[SmallMultiplesAxisScaleType]
    Placement: NotRequired[SmallMultiplesAxisPlacementType]


class SnapshotAnonymousUserRedactedTypeDef(TypedDict):
    RowLevelPermissionTagKeys: NotRequired[List[str]]


class SnapshotFileSheetSelectionOutputTypeDef(TypedDict):
    SheetId: str
    SelectionScope: SnapshotFileSheetSelectionScopeType
    VisualIds: NotRequired[List[str]]


class SnapshotFileSheetSelectionTypeDef(TypedDict):
    SheetId: str
    SelectionScope: SnapshotFileSheetSelectionScopeType
    VisualIds: NotRequired[Sequence[str]]


class SnapshotJobResultErrorInfoTypeDef(TypedDict):
    ErrorMessage: NotRequired[str]
    ErrorType: NotRequired[str]


class StartDashboardSnapshotJobScheduleRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    ScheduleId: str


class StaticFileS3SourceOptionsTypeDef(TypedDict):
    BucketName: str
    ObjectKey: str
    Region: str


class StaticFileUrlSourceOptionsTypeDef(TypedDict):
    Url: str


class StringDatasetParameterDefaultValuesOutputTypeDef(TypedDict):
    StaticValues: NotRequired[List[str]]


class StringDatasetParameterDefaultValuesTypeDef(TypedDict):
    StaticValues: NotRequired[Sequence[str]]


class StringValueWhenUnsetConfigurationTypeDef(TypedDict):
    ValueWhenUnsetOption: NotRequired[ValueWhenUnsetOptionType]
    CustomValue: NotRequired[str]


class StringParameterTypeDef(TypedDict):
    Name: str
    Values: Sequence[str]


class TableStyleTargetTypeDef(TypedDict):
    CellType: StyledCellTypeType


class SuccessfulKeyRegistrationEntryTypeDef(TypedDict):
    KeyArn: str
    StatusCode: int


class TableCellImageSizingConfigurationTypeDef(TypedDict):
    TableCellImageScalingConfiguration: NotRequired[TableCellImageScalingConfigurationType]


class TablePaginatedReportOptionsTypeDef(TypedDict):
    VerticalOverflowVisibility: NotRequired[VisibilityType]
    OverflowColumnHeaderVisibility: NotRequired[VisibilityType]


class TableFieldCustomIconContentTypeDef(TypedDict):
    Icon: NotRequired[Literal["LINK"]]


class TablePinnedFieldOptionsOutputTypeDef(TypedDict):
    PinnedLeftFields: NotRequired[List[str]]


class TablePinnedFieldOptionsTypeDef(TypedDict):
    PinnedLeftFields: NotRequired[Sequence[str]]


class TemplateSourceTemplateTypeDef(TypedDict):
    Arn: str


class TextControlPlaceholderOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]


UIColorPaletteTypeDef = TypedDict(
    "UIColorPaletteTypeDef",
    {
        "PrimaryForeground": NotRequired[str],
        "PrimaryBackground": NotRequired[str],
        "SecondaryForeground": NotRequired[str],
        "SecondaryBackground": NotRequired[str],
        "Accent": NotRequired[str],
        "AccentForeground": NotRequired[str],
        "Danger": NotRequired[str],
        "DangerForeground": NotRequired[str],
        "Warning": NotRequired[str],
        "WarningForeground": NotRequired[str],
        "Success": NotRequired[str],
        "SuccessForeground": NotRequired[str],
        "Dimension": NotRequired[str],
        "DimensionForeground": NotRequired[str],
        "Measure": NotRequired[str],
        "MeasureForeground": NotRequired[str],
    },
)
ThemeErrorTypeDef = TypedDict(
    "ThemeErrorTypeDef",
    {
        "Type": NotRequired[Literal["INTERNAL_FAILURE"]],
        "Message": NotRequired[str],
    },
)


class TopicConfigOptionsTypeDef(TypedDict):
    QBusinessInsightsEnabled: NotRequired[bool]


TopicIRComparisonMethodTypeDef = TypedDict(
    "TopicIRComparisonMethodTypeDef",
    {
        "Type": NotRequired[ComparisonMethodTypeType],
        "Period": NotRequired[TopicTimeGranularityType],
        "WindowSize": NotRequired[int],
    },
)
VisualOptionsTypeDef = TypedDict(
    "VisualOptionsTypeDef",
    {
        "type": NotRequired[str],
    },
)


class TopicSingularFilterConstantTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    SingularConstant: NotRequired[str]


class TotalAggregationFunctionTypeDef(TypedDict):
    SimpleTotalAggregationFunction: NotRequired[SimpleTotalAggregationFunctionType]


class UntagColumnOperationOutputTypeDef(TypedDict):
    ColumnName: str
    TagNames: List[ColumnTagNameType]


class UntagColumnOperationTypeDef(TypedDict):
    ColumnName: str
    TagNames: Sequence[ColumnTagNameType]


class UntagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateAccountSettingsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DefaultNamespace: str
    NotificationEmail: NotRequired[str]
    TerminationProtectionEnabled: NotRequired[bool]


class UpdateApplicationWithTokenExchangeGrantRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str


class UpdateBrandAssignmentRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandArn: str


class UpdateBrandPublishedVersionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str
    VersionId: str


class UpdateDashboardLinksRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    LinkEntities: Sequence[str]


class UpdateDashboardPublishedVersionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    VersionNumber: int


class UpdateDashboardsQAConfigurationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardsQAStatus: DashboardsQAStatusType


class UpdateDefaultQBusinessApplicationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ApplicationId: str
    Namespace: NotRequired[str]


class UpdateFolderRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Name: str


class UpdateGroupRequestRequestTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str
    Description: NotRequired[str]


class UpdateIAMPolicyAssignmentRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssignmentName: str
    Namespace: str
    AssignmentStatus: NotRequired[AssignmentStatusType]
    PolicyArn: NotRequired[str]
    Identities: NotRequired[Mapping[str, Sequence[str]]]


class UpdateIdentityPropagationConfigRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Service: ServiceTypeType
    AuthorizedTargets: NotRequired[Sequence[str]]


class UpdateIpRestrictionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    IpRestrictionRuleMap: NotRequired[Mapping[str, str]]
    VpcIdRestrictionRuleMap: NotRequired[Mapping[str, str]]
    VpcEndpointIdRestrictionRuleMap: NotRequired[Mapping[str, str]]
    Enabled: NotRequired[bool]


class UpdatePublicSharingSettingsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    PublicSharingEnabled: NotRequired[bool]


class UpdateQPersonalizationConfigurationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    PersonalizationMode: PersonalizationModeType


class UpdateQuickSightQSearchConfigurationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    QSearchStatus: QSearchStatusType


class UpdateRoleCustomPermissionRequestRequestTypeDef(TypedDict):
    CustomPermissionsName: str
    Role: RoleType
    AwsAccountId: str
    Namespace: str


class UpdateSPICECapacityConfigurationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    PurchaseMode: PurchaseModeType


class UpdateTemplateAliasRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    AliasName: str
    TemplateVersionNumber: int


class UpdateThemeAliasRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    AliasName: str
    ThemeVersionNumber: int


class UpdateUserCustomPermissionRequestRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str
    CustomPermissionsName: str


class UpdateUserRequestRequestTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str
    Email: str
    Role: UserRoleType
    CustomPermissionsName: NotRequired[str]
    UnapplyCustomPermissions: NotRequired[bool]
    ExternalLoginFederationProviderType: NotRequired[str]
    CustomFederationProviderUrl: NotRequired[str]
    ExternalLoginId: NotRequired[str]


class UpdateVPCConnectionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    VPCConnectionId: str
    Name: str
    SubnetIds: Sequence[str]
    SecurityGroupIds: Sequence[str]
    RoleArn: str
    DnsResolvers: NotRequired[Sequence[str]]


class WaterfallChartGroupColorConfigurationTypeDef(TypedDict):
    PositiveBarColor: NotRequired[str]
    NegativeBarColor: NotRequired[str]
    TotalBarColor: NotRequired[str]


class WaterfallChartOptionsTypeDef(TypedDict):
    TotalBarLabel: NotRequired[str]


class WordCloudOptionsTypeDef(TypedDict):
    WordOrientation: NotRequired[WordCloudWordOrientationType]
    WordScaling: NotRequired[WordCloudWordScalingType]
    CloudLayout: NotRequired[WordCloudCloudLayoutType]
    WordCasing: NotRequired[WordCloudWordCasingType]
    WordPadding: NotRequired[WordCloudWordPaddingType]
    MaximumStringLength: NotRequired[int]


class UpdateAccountCustomizationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AccountCustomization: AccountCustomizationTypeDef
    Namespace: NotRequired[str]


AggFunctionUnionTypeDef = Union[AggFunctionTypeDef, AggFunctionOutputTypeDef]


class AxisLabelReferenceOptionsTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef


class CascadingControlSourceTypeDef(TypedDict):
    SourceSheetControlId: NotRequired[str]
    ColumnToMatch: NotRequired[ColumnIdentifierTypeDef]


class CategoryDrillDownFilterOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    CategoryValues: List[str]


class CategoryDrillDownFilterTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    CategoryValues: Sequence[str]


class ContributionAnalysisDefaultOutputTypeDef(TypedDict):
    MeasureFieldId: str
    ContributorDimensions: List[ColumnIdentifierTypeDef]


class ContributionAnalysisDefaultTypeDef(TypedDict):
    MeasureFieldId: str
    ContributorDimensions: Sequence[ColumnIdentifierTypeDef]


class DynamicDefaultValueTypeDef(TypedDict):
    DefaultValueColumn: ColumnIdentifierTypeDef
    UserNameColumn: NotRequired[ColumnIdentifierTypeDef]
    GroupNameColumn: NotRequired[ColumnIdentifierTypeDef]


class FilterOperationSelectedFieldsConfigurationOutputTypeDef(TypedDict):
    SelectedFields: NotRequired[List[str]]
    SelectedFieldOptions: NotRequired[Literal["ALL_FIELDS"]]
    SelectedColumns: NotRequired[List[ColumnIdentifierTypeDef]]


class FilterOperationSelectedFieldsConfigurationTypeDef(TypedDict):
    SelectedFields: NotRequired[Sequence[str]]
    SelectedFieldOptions: NotRequired[Literal["ALL_FIELDS"]]
    SelectedColumns: NotRequired[Sequence[ColumnIdentifierTypeDef]]


class NumericEqualityDrillDownFilterTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Value: float


class ParameterSelectableValuesOutputTypeDef(TypedDict):
    Values: NotRequired[List[str]]
    LinkToDataSetColumn: NotRequired[ColumnIdentifierTypeDef]


class ParameterSelectableValuesTypeDef(TypedDict):
    Values: NotRequired[Sequence[str]]
    LinkToDataSetColumn: NotRequired[ColumnIdentifierTypeDef]


class TimeRangeDrillDownFilterOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    RangeMinimum: datetime
    RangeMaximum: datetime
    TimeGranularity: TimeGranularityType


AnalysisErrorTypeDef = TypedDict(
    "AnalysisErrorTypeDef",
    {
        "Type": NotRequired[AnalysisErrorTypeType],
        "Message": NotRequired[str],
        "ViolatedEntities": NotRequired[List[EntityTypeDef]],
    },
)
DashboardErrorTypeDef = TypedDict(
    "DashboardErrorTypeDef",
    {
        "Type": NotRequired[DashboardErrorTypeType],
        "Message": NotRequired[str],
        "ViolatedEntities": NotRequired[List[EntityTypeDef]],
    },
)
TemplateErrorTypeDef = TypedDict(
    "TemplateErrorTypeDef",
    {
        "Type": NotRequired[TemplateErrorTypeType],
        "Message": NotRequired[str],
        "ViolatedEntities": NotRequired[List[EntityTypeDef]],
    },
)


class SearchAnalysesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[AnalysisSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class AnalysisSourceTemplateTypeDef(TypedDict):
    DataSetReferences: Sequence[DataSetReferenceTypeDef]
    Arn: str


class DashboardSourceTemplateTypeDef(TypedDict):
    DataSetReferences: Sequence[DataSetReferenceTypeDef]
    Arn: str


class TemplateSourceAnalysisTypeDef(TypedDict):
    Arn: str
    DataSetReferences: Sequence[DataSetReferenceTypeDef]


class AnonymousUserDashboardFeatureConfigurationsTypeDef(TypedDict):
    SharedView: NotRequired[SharedViewConfigurationsTypeDef]


class AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef(TypedDict):
    InitialDashboardVisualId: DashboardVisualIdTypeDef


class RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef(TypedDict):
    InitialDashboardVisualId: DashboardVisualIdTypeDef


class ArcAxisConfigurationTypeDef(TypedDict):
    Range: NotRequired[ArcAxisDisplayRangeTypeDef]
    ReserveRange: NotRequired[int]


class AssetBundleCloudFormationOverridePropertyConfigurationOutputTypeDef(TypedDict):
    ResourceIdOverrideConfiguration: NotRequired[
        AssetBundleExportJobResourceIdOverrideConfigurationTypeDef
    ]
    VPCConnections: NotRequired[
        List[AssetBundleExportJobVPCConnectionOverridePropertiesOutputTypeDef]
    ]
    RefreshSchedules: NotRequired[
        List[AssetBundleExportJobRefreshScheduleOverridePropertiesOutputTypeDef]
    ]
    DataSources: NotRequired[List[AssetBundleExportJobDataSourceOverridePropertiesOutputTypeDef]]
    DataSets: NotRequired[List[AssetBundleExportJobDataSetOverridePropertiesOutputTypeDef]]
    Themes: NotRequired[List[AssetBundleExportJobThemeOverridePropertiesOutputTypeDef]]
    Analyses: NotRequired[List[AssetBundleExportJobAnalysisOverridePropertiesOutputTypeDef]]
    Dashboards: NotRequired[List[AssetBundleExportJobDashboardOverridePropertiesOutputTypeDef]]
    Folders: NotRequired[List[AssetBundleExportJobFolderOverridePropertiesOutputTypeDef]]


AssetBundleExportJobAnalysisOverridePropertiesUnionTypeDef = Union[
    AssetBundleExportJobAnalysisOverridePropertiesTypeDef,
    AssetBundleExportJobAnalysisOverridePropertiesOutputTypeDef,
]
AssetBundleExportJobDashboardOverridePropertiesUnionTypeDef = Union[
    AssetBundleExportJobDashboardOverridePropertiesTypeDef,
    AssetBundleExportJobDashboardOverridePropertiesOutputTypeDef,
]
AssetBundleExportJobDataSetOverridePropertiesUnionTypeDef = Union[
    AssetBundleExportJobDataSetOverridePropertiesTypeDef,
    AssetBundleExportJobDataSetOverridePropertiesOutputTypeDef,
]
AssetBundleExportJobDataSourceOverridePropertiesUnionTypeDef = Union[
    AssetBundleExportJobDataSourceOverridePropertiesTypeDef,
    AssetBundleExportJobDataSourceOverridePropertiesOutputTypeDef,
]
AssetBundleExportJobFolderOverridePropertiesUnionTypeDef = Union[
    AssetBundleExportJobFolderOverridePropertiesTypeDef,
    AssetBundleExportJobFolderOverridePropertiesOutputTypeDef,
]
AssetBundleExportJobRefreshScheduleOverridePropertiesUnionTypeDef = Union[
    AssetBundleExportJobRefreshScheduleOverridePropertiesTypeDef,
    AssetBundleExportJobRefreshScheduleOverridePropertiesOutputTypeDef,
]
AssetBundleExportJobThemeOverridePropertiesUnionTypeDef = Union[
    AssetBundleExportJobThemeOverridePropertiesTypeDef,
    AssetBundleExportJobThemeOverridePropertiesOutputTypeDef,
]
AssetBundleExportJobVPCConnectionOverridePropertiesUnionTypeDef = Union[
    AssetBundleExportJobVPCConnectionOverridePropertiesTypeDef,
    AssetBundleExportJobVPCConnectionOverridePropertiesOutputTypeDef,
]


class AssetBundleImportJobAnalysisOverridePermissionsOutputTypeDef(TypedDict):
    AnalysisIds: List[str]
    Permissions: AssetBundleResourcePermissionsOutputTypeDef


class AssetBundleImportJobDataSetOverridePermissionsOutputTypeDef(TypedDict):
    DataSetIds: List[str]
    Permissions: AssetBundleResourcePermissionsOutputTypeDef


class AssetBundleImportJobDataSourceOverridePermissionsOutputTypeDef(TypedDict):
    DataSourceIds: List[str]
    Permissions: AssetBundleResourcePermissionsOutputTypeDef


class AssetBundleImportJobFolderOverridePermissionsOutputTypeDef(TypedDict):
    FolderIds: List[str]
    Permissions: NotRequired[AssetBundleResourcePermissionsOutputTypeDef]


class AssetBundleImportJobThemeOverridePermissionsOutputTypeDef(TypedDict):
    ThemeIds: List[str]
    Permissions: AssetBundleResourcePermissionsOutputTypeDef


class AssetBundleResourceLinkSharingConfigurationOutputTypeDef(TypedDict):
    Permissions: NotRequired[AssetBundleResourcePermissionsOutputTypeDef]


class AssetBundleImportJobAnalysisOverrideTagsOutputTypeDef(TypedDict):
    AnalysisIds: List[str]
    Tags: List[TagTypeDef]


class AssetBundleImportJobAnalysisOverrideTagsTypeDef(TypedDict):
    AnalysisIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobDashboardOverrideTagsOutputTypeDef(TypedDict):
    DashboardIds: List[str]
    Tags: List[TagTypeDef]


class AssetBundleImportJobDashboardOverrideTagsTypeDef(TypedDict):
    DashboardIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobDataSetOverrideTagsOutputTypeDef(TypedDict):
    DataSetIds: List[str]
    Tags: List[TagTypeDef]


class AssetBundleImportJobDataSetOverrideTagsTypeDef(TypedDict):
    DataSetIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobDataSourceOverrideTagsOutputTypeDef(TypedDict):
    DataSourceIds: List[str]
    Tags: List[TagTypeDef]


class AssetBundleImportJobDataSourceOverrideTagsTypeDef(TypedDict):
    DataSourceIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobFolderOverrideTagsOutputTypeDef(TypedDict):
    FolderIds: List[str]
    Tags: List[TagTypeDef]


class AssetBundleImportJobFolderOverrideTagsTypeDef(TypedDict):
    FolderIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobThemeOverrideTagsOutputTypeDef(TypedDict):
    ThemeIds: List[str]
    Tags: List[TagTypeDef]


class AssetBundleImportJobThemeOverrideTagsTypeDef(TypedDict):
    ThemeIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobVPCConnectionOverrideTagsOutputTypeDef(TypedDict):
    VPCConnectionIds: List[str]
    Tags: List[TagTypeDef]


class AssetBundleImportJobVPCConnectionOverrideTagsTypeDef(TypedDict):
    VPCConnectionIds: Sequence[str]
    Tags: Sequence[TagTypeDef]


class CreateAccountCustomizationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AccountCustomization: AccountCustomizationTypeDef
    Namespace: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateNamespaceRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    IdentityStore: Literal["QUICKSIGHT"]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateVPCConnectionRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    VPCConnectionId: str
    Name: str
    SubnetIds: Sequence[str]
    SecurityGroupIds: Sequence[str]
    RoleArn: str
    DnsResolvers: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class RegisterUserRequestRequestTypeDef(TypedDict):
    IdentityType: IdentityTypeType
    Email: str
    UserRole: UserRoleType
    AwsAccountId: str
    Namespace: str
    IamArn: NotRequired[str]
    SessionName: NotRequired[str]
    UserName: NotRequired[str]
    CustomPermissionsName: NotRequired[str]
    ExternalLoginFederationProviderType: NotRequired[str]
    CustomFederationProviderUrl: NotRequired[str]
    ExternalLoginId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class TagResourceRequestRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class AssetBundleImportJobDataSourceCredentialsTypeDef(TypedDict):
    CredentialPair: NotRequired[AssetBundleImportJobDataSourceCredentialPairTypeDef]
    SecretArn: NotRequired[str]


class OAuthParametersTypeDef(TypedDict):
    TokenProviderUrl: str
    OAuthScope: NotRequired[str]
    IdentityProviderVpcConnectionProperties: NotRequired[VpcConnectionPropertiesTypeDef]
    IdentityProviderResourceUri: NotRequired[str]


class AssetBundleImportJobRefreshScheduleOverrideParametersTypeDef(TypedDict):
    DataSetId: str
    ScheduleId: str
    StartAfterDateTime: NotRequired[TimestampTypeDef]


class CustomParameterValuesTypeDef(TypedDict):
    StringValues: NotRequired[Sequence[str]]
    IntegerValues: NotRequired[Sequence[int]]
    DecimalValues: NotRequired[Sequence[float]]
    DateTimeValues: NotRequired[Sequence[TimestampTypeDef]]


class DateTimeDatasetParameterDefaultValuesTypeDef(TypedDict):
    StaticValues: NotRequired[Sequence[TimestampTypeDef]]


class DateTimeParameterTypeDef(TypedDict):
    Name: str
    Values: Sequence[TimestampTypeDef]


class DateTimeValueWhenUnsetConfigurationTypeDef(TypedDict):
    ValueWhenUnsetOption: NotRequired[ValueWhenUnsetOptionType]
    CustomValue: NotRequired[TimestampTypeDef]


class NewDefaultValuesTypeDef(TypedDict):
    StringStaticValues: NotRequired[Sequence[str]]
    DecimalStaticValues: NotRequired[Sequence[float]]
    DateTimeStaticValues: NotRequired[Sequence[TimestampTypeDef]]
    IntegerStaticValues: NotRequired[Sequence[int]]


class TimeRangeDrillDownFilterTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    RangeMinimum: TimestampTypeDef
    RangeMaximum: TimestampTypeDef
    TimeGranularity: TimeGranularityType


class TopicRefreshScheduleTypeDef(TypedDict):
    IsEnabled: bool
    BasedOnSpiceSchedule: bool
    StartingAt: NotRequired[TimestampTypeDef]
    Timezone: NotRequired[str]
    RepeatAt: NotRequired[str]
    TopicScheduleType: NotRequired[TopicScheduleTypeType]


class WhatIfPointScenarioTypeDef(TypedDict):
    Date: TimestampTypeDef
    Value: float


class WhatIfRangeScenarioTypeDef(TypedDict):
    StartDate: TimestampTypeDef
    EndDate: TimestampTypeDef
    Value: float


AssetBundleImportJobVPCConnectionOverrideParametersUnionTypeDef = Union[
    AssetBundleImportJobVPCConnectionOverrideParametersTypeDef,
    AssetBundleImportJobVPCConnectionOverrideParametersOutputTypeDef,
]


class AssetBundleImportSourceTypeDef(TypedDict):
    Body: NotRequired[BlobTypeDef]
    S3Uri: NotRequired[str]


AssetBundleResourcePermissionsUnionTypeDef = Union[
    AssetBundleResourcePermissionsTypeDef, AssetBundleResourcePermissionsOutputTypeDef
]


class AxisDisplayRangeOutputTypeDef(TypedDict):
    MinMax: NotRequired[AxisDisplayMinMaxRangeTypeDef]
    DataDriven: NotRequired[Dict[str, Any]]


class AxisDisplayRangeTypeDef(TypedDict):
    MinMax: NotRequired[AxisDisplayMinMaxRangeTypeDef]
    DataDriven: NotRequired[Mapping[str, Any]]


class AxisScaleTypeDef(TypedDict):
    Linear: NotRequired[AxisLinearScaleTypeDef]
    Logarithmic: NotRequired[AxisLogarithmicScaleTypeDef]


class ScatterPlotSortConfigurationTypeDef(TypedDict):
    ScatterPlotLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class CancelIngestionResponseTypeDef(TypedDict):
    Arn: str
    IngestionId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAccountCustomizationResponseTypeDef(TypedDict):
    Arn: str
    AwsAccountId: str
    Namespace: str
    AccountCustomization: AccountCustomizationTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAnalysisResponseTypeDef(TypedDict):
    Arn: str
    AnalysisId: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCustomPermissionsResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDashboardResponseTypeDef(TypedDict):
    Arn: str
    VersionArn: str
    DashboardId: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataSetResponseTypeDef(TypedDict):
    Arn: str
    DataSetId: str
    IngestionArn: str
    IngestionId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataSourceResponseTypeDef(TypedDict):
    Arn: str
    DataSourceId: str
    CreationStatus: ResourceStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFolderResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    FolderId: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIAMPolicyAssignmentResponseTypeDef(TypedDict):
    AssignmentName: str
    AssignmentId: str
    AssignmentStatus: AssignmentStatusType
    PolicyArn: str
    Identities: Dict[str, List[str]]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateIngestionResponseTypeDef(TypedDict):
    Arn: str
    IngestionId: str
    IngestionStatus: IngestionStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateNamespaceResponseTypeDef(TypedDict):
    Arn: str
    Name: str
    CapacityRegion: str
    CreationStatus: NamespaceStatusType
    IdentityStore: Literal["QUICKSIGHT"]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRefreshScheduleResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    ScheduleId: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRoleMembershipResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTemplateResponseTypeDef(TypedDict):
    Arn: str
    VersionArn: str
    TemplateId: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateThemeResponseTypeDef(TypedDict):
    Arn: str
    VersionArn: str
    ThemeId: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTopicRefreshScheduleResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    DatasetArn: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTopicResponseTypeDef(TypedDict):
    Arn: str
    TopicId: str
    RefreshArn: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVPCConnectionResponseTypeDef(TypedDict):
    Arn: str
    VPCConnectionId: str
    CreationStatus: VPCConnectionResourceStatusType
    AvailabilityStatus: VPCConnectionAvailabilityStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAccountCustomizationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAccountSubscriptionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteAnalysisResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    AnalysisId: str
    DeletionTime: datetime
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBrandAssignmentResponseTypeDef(TypedDict):
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteBrandResponseTypeDef(TypedDict):
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCustomPermissionsResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDashboardResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    DashboardId: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataSetRefreshPropertiesResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataSetResponseTypeDef(TypedDict):
    Arn: str
    DataSetId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataSourceResponseTypeDef(TypedDict):
    Arn: str
    DataSourceId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDefaultQBusinessApplicationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFolderMembershipResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFolderResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    FolderId: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGroupMembershipResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteGroupResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIAMPolicyAssignmentResponseTypeDef(TypedDict):
    AssignmentName: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteIdentityPropagationConfigResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteNamespaceResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRefreshScheduleResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    ScheduleId: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRoleCustomPermissionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteRoleMembershipResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTemplateAliasResponseTypeDef(TypedDict):
    Status: int
    TemplateId: str
    AliasName: str
    Arn: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTemplateResponseTypeDef(TypedDict):
    RequestId: str
    Arn: str
    TemplateId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteThemeAliasResponseTypeDef(TypedDict):
    AliasName: str
    Arn: str
    RequestId: str
    Status: int
    ThemeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteThemeResponseTypeDef(TypedDict):
    Arn: str
    RequestId: str
    Status: int
    ThemeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTopicRefreshScheduleResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    DatasetArn: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTopicResponseTypeDef(TypedDict):
    Arn: str
    TopicId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteUserByPrincipalIdResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteUserCustomPermissionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteUserResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVPCConnectionResponseTypeDef(TypedDict):
    Arn: str
    VPCConnectionId: str
    DeletionStatus: VPCConnectionResourceStatusType
    AvailabilityStatus: VPCConnectionAvailabilityStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountCustomizationResponseTypeDef(TypedDict):
    Arn: str
    AwsAccountId: str
    Namespace: str
    AccountCustomization: AccountCustomizationTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountSettingsResponseTypeDef(TypedDict):
    AccountSettings: AccountSettingsTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountSubscriptionResponseTypeDef(TypedDict):
    AccountInfo: AccountInfoTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBrandAssignmentResponseTypeDef(TypedDict):
    RequestId: str
    BrandArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDashboardsQAConfigurationResponseTypeDef(TypedDict):
    DashboardsQAStatus: DashboardsQAStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDefaultQBusinessApplicationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ApplicationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIpRestrictionResponseTypeDef(TypedDict):
    AwsAccountId: str
    IpRestrictionRuleMap: Dict[str, str]
    VpcIdRestrictionRuleMap: Dict[str, str]
    VpcEndpointIdRestrictionRuleMap: Dict[str, str]
    Enabled: bool
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeQPersonalizationConfigurationResponseTypeDef(TypedDict):
    PersonalizationMode: PersonalizationModeType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeQuickSightQSearchConfigurationResponseTypeDef(TypedDict):
    QSearchStatus: QSearchStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRoleCustomPermissionResponseTypeDef(TypedDict):
    CustomPermissionsName: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class GenerateEmbedUrlForAnonymousUserResponseTypeDef(TypedDict):
    EmbedUrl: str
    Status: int
    RequestId: str
    AnonymousUserArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class GenerateEmbedUrlForRegisteredUserResponseTypeDef(TypedDict):
    EmbedUrl: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GenerateEmbedUrlForRegisteredUserWithIdentityResponseTypeDef(TypedDict):
    EmbedUrl: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetDashboardEmbedUrlResponseTypeDef(TypedDict):
    EmbedUrl: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetSessionEmbedUrlResponseTypeDef(TypedDict):
    EmbedUrl: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAnalysesResponseTypeDef(TypedDict):
    AnalysisSummaryList: List[AnalysisSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAssetBundleExportJobsResponseTypeDef(TypedDict):
    AssetBundleExportJobSummaryList: List[AssetBundleExportJobSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListAssetBundleImportJobsResponseTypeDef(TypedDict):
    AssetBundleImportJobSummaryList: List[AssetBundleImportJobSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListFoldersForResourceResponseTypeDef(TypedDict):
    Status: int
    Folders: List[str]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListIAMPolicyAssignmentsForUserResponseTypeDef(TypedDict):
    ActiveAssignments: List[ActiveIAMPolicyAssignmentTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListIdentityPropagationConfigsResponseTypeDef(TypedDict):
    Services: List[AuthorizedTargetsByServiceTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListRoleMembershipsResponseTypeDef(TypedDict):
    MembersList: List[str]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class PutDataSetRefreshPropertiesResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class RestoreAnalysisResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    AnalysisId: str
    RequestId: str
    RestorationFailedFolderArns: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class SearchAnalysesResponseTypeDef(TypedDict):
    AnalysisSummaryList: List[AnalysisSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class StartAssetBundleExportJobResponseTypeDef(TypedDict):
    Arn: str
    AssetBundleExportJobId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class StartAssetBundleImportJobResponseTypeDef(TypedDict):
    Arn: str
    AssetBundleImportJobId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class StartDashboardSnapshotJobResponseTypeDef(TypedDict):
    Arn: str
    SnapshotJobId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class StartDashboardSnapshotJobScheduleResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UntagResourceResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccountCustomizationResponseTypeDef(TypedDict):
    Arn: str
    AwsAccountId: str
    Namespace: str
    AccountCustomization: AccountCustomizationTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccountSettingsResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAnalysisResponseTypeDef(TypedDict):
    Arn: str
    AnalysisId: str
    UpdateStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateApplicationWithTokenExchangeGrantResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrandAssignmentResponseTypeDef(TypedDict):
    RequestId: str
    BrandArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrandPublishedVersionResponseTypeDef(TypedDict):
    RequestId: str
    VersionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCustomPermissionsResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDashboardLinksResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    DashboardArn: str
    LinkEntities: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDashboardPublishedVersionResponseTypeDef(TypedDict):
    DashboardId: str
    DashboardArn: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDashboardResponseTypeDef(TypedDict):
    Arn: str
    VersionArn: str
    DashboardId: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDashboardsQAConfigurationResponseTypeDef(TypedDict):
    DashboardsQAStatus: DashboardsQAStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataSetPermissionsResponseTypeDef(TypedDict):
    DataSetArn: str
    DataSetId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataSetResponseTypeDef(TypedDict):
    Arn: str
    DataSetId: str
    IngestionArn: str
    IngestionId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataSourcePermissionsResponseTypeDef(TypedDict):
    DataSourceArn: str
    DataSourceId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDataSourceResponseTypeDef(TypedDict):
    Arn: str
    DataSourceId: str
    UpdateStatus: ResourceStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDefaultQBusinessApplicationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFolderResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    FolderId: str
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIAMPolicyAssignmentResponseTypeDef(TypedDict):
    AssignmentName: str
    AssignmentId: str
    PolicyArn: str
    Identities: Dict[str, List[str]]
    AssignmentStatus: AssignmentStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIdentityPropagationConfigResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIpRestrictionResponseTypeDef(TypedDict):
    AwsAccountId: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePublicSharingSettingsResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQPersonalizationConfigurationResponseTypeDef(TypedDict):
    PersonalizationMode: PersonalizationModeType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateQuickSightQSearchConfigurationResponseTypeDef(TypedDict):
    QSearchStatus: QSearchStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRefreshScheduleResponseTypeDef(TypedDict):
    Status: int
    RequestId: str
    ScheduleId: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRoleCustomPermissionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSPICECapacityConfigurationResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTemplateResponseTypeDef(TypedDict):
    TemplateId: str
    Arn: str
    VersionArn: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateThemeResponseTypeDef(TypedDict):
    ThemeId: str
    Arn: str
    VersionArn: str
    CreationStatus: ResourceStatusType
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTopicRefreshScheduleResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    DatasetArn: str
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTopicResponseTypeDef(TypedDict):
    TopicId: str
    Arn: str
    RefreshArn: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserCustomPermissionResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateVPCConnectionResponseTypeDef(TypedDict):
    Arn: str
    VPCConnectionId: str
    UpdateStatus: VPCConnectionResourceStatusType
    AvailabilityStatus: VPCConnectionAvailabilityStatusType
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class BatchCreateTopicReviewedAnswerResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    SucceededAnswers: List[SucceededTopicReviewedAnswerTypeDef]
    InvalidAnswers: List[InvalidTopicReviewedAnswerTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDeleteTopicReviewedAnswerResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    SucceededAnswers: List[SucceededTopicReviewedAnswerTypeDef]
    InvalidAnswers: List[InvalidTopicReviewedAnswerTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class HistogramBinOptionsTypeDef(TypedDict):
    SelectedBinType: NotRequired[HistogramBinTypeType]
    BinCount: NotRequired[BinCountOptionsTypeDef]
    BinWidth: NotRequired[BinWidthOptionsTypeDef]
    StartValue: NotRequired[float]


class BodySectionRepeatPageBreakConfigurationTypeDef(TypedDict):
    After: NotRequired[SectionAfterPageBreakTypeDef]


class SectionPageBreakConfigurationTypeDef(TypedDict):
    After: NotRequired[SectionAfterPageBreakTypeDef]


class TileStyleTypeDef(TypedDict):
    Border: NotRequired[BorderStyleTypeDef]


class BoxPlotOptionsTypeDef(TypedDict):
    StyleOptions: NotRequired[BoxPlotStyleOptionsTypeDef]
    OutlierVisibility: NotRequired[VisibilityType]
    AllDataPointsVisibility: NotRequired[VisibilityType]


BrandColorPaletteTypeDef = TypedDict(
    "BrandColorPaletteTypeDef",
    {
        "Primary": NotRequired[PaletteTypeDef],
        "Secondary": NotRequired[PaletteTypeDef],
        "Accent": NotRequired[PaletteTypeDef],
        "Measure": NotRequired[PaletteTypeDef],
        "Dimension": NotRequired[PaletteTypeDef],
        "Success": NotRequired[PaletteTypeDef],
        "Info": NotRequired[PaletteTypeDef],
        "Warning": NotRequired[PaletteTypeDef],
        "Danger": NotRequired[PaletteTypeDef],
    },
)


class NavbarStyleTypeDef(TypedDict):
    GlobalNavbar: NotRequired[PaletteTypeDef]
    ContextualNavbar: NotRequired[PaletteTypeDef]


class ListBrandsResponseTypeDef(TypedDict):
    Brands: List[BrandSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateColumnsOperationOutputTypeDef(TypedDict):
    Columns: List[CalculatedColumnTypeDef]


class CreateColumnsOperationTypeDef(TypedDict):
    Columns: Sequence[CalculatedColumnTypeDef]


class CreateCustomPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    CustomPermissionsName: str
    Capabilities: NotRequired[CapabilitiesTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CustomPermissionsTypeDef(TypedDict):
    Arn: NotRequired[str]
    CustomPermissionsName: NotRequired[str]
    Capabilities: NotRequired[CapabilitiesTypeDef]


class UpdateCustomPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    CustomPermissionsName: str
    Capabilities: NotRequired[CapabilitiesTypeDef]


class CategoryFilterConfigurationOutputTypeDef(TypedDict):
    FilterListConfiguration: NotRequired[FilterListConfigurationOutputTypeDef]
    CustomFilterListConfiguration: NotRequired[CustomFilterListConfigurationOutputTypeDef]
    CustomFilterConfiguration: NotRequired[CustomFilterConfigurationTypeDef]


CellValueSynonymUnionTypeDef = Union[CellValueSynonymTypeDef, CellValueSynonymOutputTypeDef]


class ClusterMarkerTypeDef(TypedDict):
    SimpleClusterMarker: NotRequired[SimpleClusterMarkerTypeDef]


class TopicConstantValueOutputTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    Value: NotRequired[str]
    Minimum: NotRequired[str]
    Maximum: NotRequired[str]
    ValueList: NotRequired[List[CollectiveConstantEntryTypeDef]]


class TopicConstantValueTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    Value: NotRequired[str]
    Minimum: NotRequired[str]
    Maximum: NotRequired[str]
    ValueList: NotRequired[Sequence[CollectiveConstantEntryTypeDef]]


class TopicCategoryFilterConstantOutputTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    SingularConstant: NotRequired[str]
    CollectiveConstant: NotRequired[CollectiveConstantOutputTypeDef]


CollectiveConstantUnionTypeDef = Union[CollectiveConstantTypeDef, CollectiveConstantOutputTypeDef]


class ColorScaleOutputTypeDef(TypedDict):
    Colors: List[DataColorTypeDef]
    ColorFillType: ColorFillTypeType
    NullValueColor: NotRequired[DataColorTypeDef]


class ColorScaleTypeDef(TypedDict):
    Colors: Sequence[DataColorTypeDef]
    ColorFillType: ColorFillTypeType
    NullValueColor: NotRequired[DataColorTypeDef]


class ColorsConfigurationOutputTypeDef(TypedDict):
    CustomColors: NotRequired[List[CustomColorTypeDef]]


class ColorsConfigurationTypeDef(TypedDict):
    CustomColors: NotRequired[Sequence[CustomColorTypeDef]]


class ColumnTagTypeDef(TypedDict):
    ColumnGeographicRole: NotRequired[GeoSpatialDataRoleType]
    ColumnDescription: NotRequired[ColumnDescriptionTypeDef]


class ColumnGroupSchemaOutputTypeDef(TypedDict):
    Name: NotRequired[str]
    ColumnGroupColumnSchemaList: NotRequired[List[ColumnGroupColumnSchemaTypeDef]]


class ColumnGroupSchemaTypeDef(TypedDict):
    Name: NotRequired[str]
    ColumnGroupColumnSchemaList: NotRequired[Sequence[ColumnGroupColumnSchemaTypeDef]]


class ColumnGroupOutputTypeDef(TypedDict):
    GeoSpatialColumnGroup: NotRequired[GeoSpatialColumnGroupOutputTypeDef]


ColumnLevelPermissionRuleUnionTypeDef = Union[
    ColumnLevelPermissionRuleTypeDef, ColumnLevelPermissionRuleOutputTypeDef
]


class DataSetSchemaOutputTypeDef(TypedDict):
    ColumnSchemaList: NotRequired[List[ColumnSchemaTypeDef]]


class DataSetSchemaTypeDef(TypedDict):
    ColumnSchemaList: NotRequired[Sequence[ColumnSchemaTypeDef]]


ComparativeOrderUnionTypeDef = Union[ComparativeOrderTypeDef, ComparativeOrderOutputTypeDef]


class ConditionalFormattingCustomIconConditionTypeDef(TypedDict):
    Expression: str
    IconOptions: ConditionalFormattingCustomIconOptionsTypeDef
    Color: NotRequired[str]
    DisplayConfiguration: NotRequired[ConditionalFormattingIconDisplayConfigurationTypeDef]


class CreateAccountSubscriptionResponseTypeDef(TypedDict):
    SignupResponse: SignupResponseTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFolderRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Name: NotRequired[str]
    FolderType: NotRequired[FolderTypeType]
    ParentFolderArn: NotRequired[str]
    Permissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SharingModel: NotRequired[SharingModelType]


class UpdateAnalysisPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]


class UpdateDashboardPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    GrantLinkPermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    RevokeLinkPermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]


class UpdateDataSetPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]


class UpdateDataSourcePermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSourceId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]


class UpdateFolderPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]


class UpdateTemplatePermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]


class UpdateThemePermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]


class UpdateTopicPermissionsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    GrantPermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    RevokePermissions: NotRequired[Sequence[ResourcePermissionTypeDef]]


class DataSetSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    DataSetId: NotRequired[str]
    Name: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    ImportMode: NotRequired[DataSetImportModeType]
    RowLevelPermissionDataSet: NotRequired[RowLevelPermissionDataSetTypeDef]
    RowLevelPermissionTagConfigurationApplied: NotRequired[bool]
    ColumnLevelPermissionRulesApplied: NotRequired[bool]


class CreateFolderMembershipResponseTypeDef(TypedDict):
    Status: int
    FolderMember: FolderMemberTypeDef
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateGroupMembershipResponseTypeDef(TypedDict):
    GroupMember: GroupMemberTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGroupMembershipResponseTypeDef(TypedDict):
    GroupMember: GroupMemberTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListGroupMembershipsResponseTypeDef(TypedDict):
    GroupMemberList: List[GroupMemberTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateGroupResponseTypeDef(TypedDict):
    Group: GroupTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeGroupResponseTypeDef(TypedDict):
    Group: GroupTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListGroupsResponseTypeDef(TypedDict):
    GroupList: List[GroupTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListUserGroupsResponseTypeDef(TypedDict):
    GroupList: List[GroupTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchGroupsResponseTypeDef(TypedDict):
    GroupList: List[GroupTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateGroupResponseTypeDef(TypedDict):
    Group: GroupTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTemplateAliasResponseTypeDef(TypedDict):
    TemplateAlias: TemplateAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTemplateAliasResponseTypeDef(TypedDict):
    TemplateAlias: TemplateAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTemplateAliasesResponseTypeDef(TypedDict):
    TemplateAliasList: List[TemplateAliasTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateTemplateAliasResponseTypeDef(TypedDict):
    TemplateAlias: TemplateAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateThemeAliasResponseTypeDef(TypedDict):
    ThemeAlias: ThemeAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeThemeAliasResponseTypeDef(TypedDict):
    ThemeAlias: ThemeAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListThemeAliasesResponseTypeDef(TypedDict):
    ThemeAliasList: List[ThemeAliasTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateThemeAliasResponseTypeDef(TypedDict):
    ThemeAlias: ThemeAliasTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CustomActionNavigationOperationTypeDef(TypedDict):
    LocalNavigationConfiguration: NotRequired[LocalNavigationConfigurationTypeDef]


CustomFilterListConfigurationUnionTypeDef = Union[
    CustomFilterListConfigurationTypeDef, CustomFilterListConfigurationOutputTypeDef
]


class CustomValuesConfigurationOutputTypeDef(TypedDict):
    CustomValues: CustomParameterValuesOutputTypeDef
    IncludeNullValue: NotRequired[bool]


class CustomSqlOutputTypeDef(TypedDict):
    DataSourceArn: str
    Name: str
    SqlQuery: str
    Columns: NotRequired[List[InputColumnTypeDef]]


class CustomSqlTypeDef(TypedDict):
    DataSourceArn: str
    Name: str
    SqlQuery: str
    Columns: NotRequired[Sequence[InputColumnTypeDef]]


class RelationalTableOutputTypeDef(TypedDict):
    DataSourceArn: str
    Name: str
    InputColumns: List[InputColumnTypeDef]
    Catalog: NotRequired[str]
    Schema: NotRequired[str]


class RelationalTableTypeDef(TypedDict):
    DataSourceArn: str
    Name: str
    InputColumns: Sequence[InputColumnTypeDef]
    Catalog: NotRequired[str]
    Schema: NotRequired[str]


class VisualInteractionOptionsTypeDef(TypedDict):
    VisualMenuOption: NotRequired[VisualMenuOptionTypeDef]
    ContextMenuOption: NotRequired[ContextMenuOptionTypeDef]


class SearchDashboardsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DashboardSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class ListDashboardsResponseTypeDef(TypedDict):
    DashboardSummaryList: List[DashboardSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchDashboardsResponseTypeDef(TypedDict):
    DashboardSummaryList: List[DashboardSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListDashboardVersionsResponseTypeDef(TypedDict):
    DashboardVersionSummaryList: List[DashboardVersionSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DashboardVisualPublishOptionsTypeDef(TypedDict):
    ExportHiddenFieldsOption: NotRequired[ExportHiddenFieldsOptionTypeDef]


class TableInlineVisualizationTypeDef(TypedDict):
    DataBars: NotRequired[DataBarsOptionsTypeDef]


DataColorPaletteUnionTypeDef = Union[DataColorPaletteTypeDef, DataColorPaletteOutputTypeDef]


class DataLabelTypeTypeDef(TypedDict):
    FieldLabelType: NotRequired[FieldLabelTypeTypeDef]
    DataPathLabelType: NotRequired[DataPathLabelTypeTypeDef]
    RangeEndsLabelType: NotRequired[RangeEndsLabelTypeTypeDef]
    MinimumLabelType: NotRequired[MinimumLabelTypeTypeDef]
    MaximumLabelType: NotRequired[MaximumLabelTypeTypeDef]


class DataPathValueTypeDef(TypedDict):
    FieldId: NotRequired[str]
    FieldValue: NotRequired[str]
    DataPathType: NotRequired[DataPathTypeTypeDef]


class SearchDataSetsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DataSetSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SearchDataSourcesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DataSourceSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SearchDataSourcesResponseTypeDef(TypedDict):
    DataSourceSummaries: List[DataSourceSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DateTimeDatasetParameterOutputTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    TimeGranularity: NotRequired[TimeGranularityType]
    DefaultValues: NotRequired[DateTimeDatasetParameterDefaultValuesOutputTypeDef]


class TimeRangeFilterValueOutputTypeDef(TypedDict):
    StaticValue: NotRequired[datetime]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]
    Parameter: NotRequired[str]


class TimeRangeFilterValueTypeDef(TypedDict):
    StaticValue: NotRequired[TimestampTypeDef]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]
    Parameter: NotRequired[str]


class DecimalDatasetParameterOutputTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[DecimalDatasetParameterDefaultValuesOutputTypeDef]


DecimalDatasetParameterDefaultValuesUnionTypeDef = Union[
    DecimalDatasetParameterDefaultValuesTypeDef, DecimalDatasetParameterDefaultValuesOutputTypeDef
]
DecimalParameterUnionTypeDef = Union[DecimalParameterTypeDef, DecimalParameterOutputTypeDef]


class DescribeAnalysisPermissionsResponseTypeDef(TypedDict):
    AnalysisId: str
    AnalysisArn: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDataSetPermissionsResponseTypeDef(TypedDict):
    DataSetArn: str
    DataSetId: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDataSourcePermissionsResponseTypeDef(TypedDict):
    DataSourceArn: str
    DataSourceId: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFolderPermissionsResponseTypeDef(TypedDict):
    Status: int
    FolderId: str
    Arn: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeFolderResolvedPermissionsResponseTypeDef(TypedDict):
    Status: int
    FolderId: str
    Arn: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeTemplatePermissionsResponseTypeDef(TypedDict):
    TemplateId: str
    TemplateArn: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeThemePermissionsResponseTypeDef(TypedDict):
    ThemeId: str
    ThemeArn: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTopicPermissionsResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class LinkSharingConfigurationOutputTypeDef(TypedDict):
    Permissions: NotRequired[List[ResourcePermissionOutputTypeDef]]


ResourcePermissionUnionTypeDef = Union[ResourcePermissionTypeDef, ResourcePermissionOutputTypeDef]


class UpdateAnalysisPermissionsResponseTypeDef(TypedDict):
    AnalysisArn: str
    AnalysisId: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateFolderPermissionsResponseTypeDef(TypedDict):
    Status: int
    Arn: str
    FolderId: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTemplatePermissionsResponseTypeDef(TypedDict):
    TemplateId: str
    TemplateArn: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateThemePermissionsResponseTypeDef(TypedDict):
    ThemeId: str
    ThemeArn: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTopicPermissionsResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFolderPermissionsRequestDescribeFolderPermissionsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    Namespace: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeFolderResolvedPermissionsRequestDescribeFolderResolvedPermissionsPaginateTypeDef(
    TypedDict
):
    AwsAccountId: str
    FolderId: str
    Namespace: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAnalysesRequestListAnalysesPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetBundleExportJobsRequestListAssetBundleExportJobsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetBundleImportJobsRequestListAssetBundleImportJobsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBrandsRequestListBrandsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCustomPermissionsRequestListCustomPermissionsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDashboardVersionsRequestListDashboardVersionsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDashboardsRequestListDashboardsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSetsRequestListDataSetsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSourcesRequestListDataSourcesPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFolderMembersRequestListFolderMembersPaginateTypeDef(TypedDict):
    AwsAccountId: str
    FolderId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFoldersForResourceRequestListFoldersForResourcePaginateTypeDef(TypedDict):
    AwsAccountId: str
    ResourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFoldersRequestListFoldersPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupMembershipsRequestListGroupMembershipsPaginateTypeDef(TypedDict):
    GroupName: str
    AwsAccountId: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListGroupsRequestListGroupsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIAMPolicyAssignmentsForUserRequestListIAMPolicyAssignmentsForUserPaginateTypeDef(
    TypedDict
):
    AwsAccountId: str
    UserName: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIAMPolicyAssignmentsRequestListIAMPolicyAssignmentsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    AssignmentStatus: NotRequired[AssignmentStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIngestionsRequestListIngestionsPaginateTypeDef(TypedDict):
    DataSetId: str
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNamespacesRequestListNamespacesPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRoleMembershipsRequestListRoleMembershipsPaginateTypeDef(TypedDict):
    Role: RoleType
    AwsAccountId: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTemplateAliasesRequestListTemplateAliasesPaginateTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTemplateVersionsRequestListTemplateVersionsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTemplatesRequestListTemplatesPaginateTypeDef(TypedDict):
    AwsAccountId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThemeVersionsRequestListThemeVersionsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListThemesRequestListThemesPaginateTypeDef = TypedDict(
    "ListThemesRequestListThemesPaginateTypeDef",
    {
        "AwsAccountId": str,
        "Type": NotRequired[ThemeTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListUserGroupsRequestListUserGroupsPaginateTypeDef(TypedDict):
    UserName: str
    AwsAccountId: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListUsersRequestListUsersPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchAnalysesRequestSearchAnalysesPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[AnalysisSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchDashboardsRequestSearchDashboardsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DashboardSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchDataSetsRequestSearchDataSetsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DataSetSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchDataSourcesRequestSearchDataSourcesPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[DataSourceSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeFolderResponseTypeDef(TypedDict):
    Status: int
    Folder: FolderTypeDef
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIAMPolicyAssignmentResponseTypeDef(TypedDict):
    IAMPolicyAssignment: IAMPolicyAssignmentTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeKeyRegistrationResponseTypeDef(TypedDict):
    AwsAccountId: str
    KeyRegistration: List[RegisteredCustomerManagedKeyTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateKeyRegistrationRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    KeyRegistration: Sequence[RegisteredCustomerManagedKeyTypeDef]


class DescribeTopicRefreshResponseTypeDef(TypedDict):
    RefreshDetails: TopicRefreshDetailsTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTopicRefreshScheduleResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    DatasetArn: str
    RefreshSchedule: TopicRefreshScheduleOutputTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class TopicRefreshScheduleSummaryTypeDef(TypedDict):
    DatasetId: NotRequired[str]
    DatasetArn: NotRequired[str]
    DatasetName: NotRequired[str]
    RefreshSchedule: NotRequired[TopicRefreshScheduleOutputTypeDef]


class DescribeUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListUsersResponseTypeDef(TypedDict):
    UserList: List[UserTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class RegisterUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    UserInvitationUrl: str
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateUserResponseTypeDef(TypedDict):
    User: UserTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class DisplayFormatOptionsTypeDef(TypedDict):
    UseBlankCellFormat: NotRequired[bool]
    BlankCellFormat: NotRequired[str]
    DateFormat: NotRequired[str]
    DecimalSeparator: NotRequired[TopicNumericSeparatorSymbolType]
    GroupingSeparator: NotRequired[str]
    UseGrouping: NotRequired[bool]
    FractionDigits: NotRequired[int]
    Prefix: NotRequired[str]
    Suffix: NotRequired[str]
    UnitScaler: NotRequired[NumberScaleType]
    NegativeFormat: NotRequired[NegativeFormatTypeDef]
    CurrencySymbol: NotRequired[str]


class DonutOptionsTypeDef(TypedDict):
    ArcOptions: NotRequired[ArcOptionsTypeDef]
    DonutCenterOptions: NotRequired[DonutCenterOptionsTypeDef]


FieldFolderUnionTypeDef = Union[FieldFolderTypeDef, FieldFolderOutputTypeDef]


class FilterAggMetricsTypeDef(TypedDict):
    MetricOperand: NotRequired[IdentifierTypeDef]
    Function: NotRequired[AggTypeType]
    SortDirection: NotRequired[TopicSortDirectionType]


class TopicSortClauseTypeDef(TypedDict):
    Operand: NotRequired[IdentifierTypeDef]
    SortDirection: NotRequired[TopicSortDirectionType]


FilterListConfigurationUnionTypeDef = Union[
    FilterListConfigurationTypeDef, FilterListConfigurationOutputTypeDef
]


class FilterOperationTargetVisualsConfigurationOutputTypeDef(TypedDict):
    SameSheetTargetVisualConfiguration: NotRequired[SameSheetTargetVisualConfigurationOutputTypeDef]


FilterSelectableValuesUnionTypeDef = Union[
    FilterSelectableValuesTypeDef, FilterSelectableValuesOutputTypeDef
]


class SearchFoldersRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[FolderSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SearchFoldersRequestSearchFoldersPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[FolderSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFoldersResponseTypeDef(TypedDict):
    Status: int
    FolderSummaryList: List[FolderSummaryTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchFoldersResponseTypeDef(TypedDict):
    Status: int
    FolderSummaryList: List[FolderSummaryTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class FontConfigurationTypeDef(TypedDict):
    FontSize: NotRequired[FontSizeTypeDef]
    FontDecoration: NotRequired[FontDecorationType]
    FontColor: NotRequired[str]
    FontWeight: NotRequired[FontWeightTypeDef]
    FontStyle: NotRequired[FontStyleType]
    FontFamily: NotRequired[str]


class TypographyOutputTypeDef(TypedDict):
    FontFamilies: NotRequired[List[FontTypeDef]]


class TypographyTypeDef(TypedDict):
    FontFamilies: NotRequired[Sequence[FontTypeDef]]


class ForecastScenarioOutputTypeDef(TypedDict):
    WhatIfPointScenario: NotRequired[WhatIfPointScenarioOutputTypeDef]
    WhatIfRangeScenario: NotRequired[WhatIfRangeScenarioOutputTypeDef]


class FreeFormLayoutCanvasSizeOptionsTypeDef(TypedDict):
    ScreenCanvasSizeOptions: NotRequired[FreeFormLayoutScreenCanvasSizeOptionsTypeDef]


class SnapshotAnonymousUserTypeDef(TypedDict):
    RowLevelPermissionTags: NotRequired[Sequence[SessionTagTypeDef]]


class QAResultTypeDef(TypedDict):
    ResultType: NotRequired[QAResultTypeType]
    DashboardVisual: NotRequired[DashboardVisualResultTypeDef]
    GeneratedAnswer: NotRequired[GeneratedAnswerResultTypeDef]


GeoSpatialColumnGroupUnionTypeDef = Union[
    GeoSpatialColumnGroupTypeDef, GeoSpatialColumnGroupOutputTypeDef
]


class GeospatialMapStateTypeDef(TypedDict):
    Bounds: NotRequired[GeospatialCoordinateBoundsTypeDef]
    MapNavigation: NotRequired[GeospatialMapNavigationType]


class GeospatialWindowOptionsTypeDef(TypedDict):
    Bounds: NotRequired[GeospatialCoordinateBoundsTypeDef]
    MapZoomMode: NotRequired[MapZoomModeType]


class GeospatialDataSourceItemTypeDef(TypedDict):
    StaticFileDataSource: NotRequired[GeospatialStaticFileSourceTypeDef]


class GeospatialHeatmapColorScaleOutputTypeDef(TypedDict):
    Colors: NotRequired[List[GeospatialHeatmapDataColorTypeDef]]


class GeospatialHeatmapColorScaleTypeDef(TypedDict):
    Colors: NotRequired[Sequence[GeospatialHeatmapDataColorTypeDef]]


class GeospatialNullDataSettingsTypeDef(TypedDict):
    SymbolStyle: GeospatialNullSymbolStyleTypeDef


class TableSideBorderOptionsTypeDef(TypedDict):
    InnerVertical: NotRequired[TableBorderOptionsTypeDef]
    InnerHorizontal: NotRequired[TableBorderOptionsTypeDef]
    Left: NotRequired[TableBorderOptionsTypeDef]
    Right: NotRequired[TableBorderOptionsTypeDef]
    Top: NotRequired[TableBorderOptionsTypeDef]
    Bottom: NotRequired[TableBorderOptionsTypeDef]


class GradientColorOutputTypeDef(TypedDict):
    Stops: NotRequired[List[GradientStopTypeDef]]


class GradientColorTypeDef(TypedDict):
    Stops: NotRequired[Sequence[GradientStopTypeDef]]


class GridLayoutCanvasSizeOptionsTypeDef(TypedDict):
    ScreenCanvasSizeOptions: NotRequired[GridLayoutScreenCanvasSizeOptionsTypeDef]


class SearchGroupsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    Filters: Sequence[GroupSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SearchGroupsRequestSearchGroupsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    Filters: Sequence[GroupSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIAMPolicyAssignmentsResponseTypeDef(TypedDict):
    IAMPolicyAssignments: List[IAMPolicyAssignmentSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ImageConfigurationTypeDef(TypedDict):
    Source: NotRequired[ImageSourceTypeDef]


class ImageTypeDef(TypedDict):
    Source: NotRequired[ImageSourceTypeDef]
    GeneratedImageUrl: NotRequired[str]


class ImageInteractionOptionsTypeDef(TypedDict):
    ImageMenuOption: NotRequired[ImageMenuOptionTypeDef]


class IncrementalRefreshTypeDef(TypedDict):
    LookbackWindow: LookbackWindowTypeDef


class IngestionTypeDef(TypedDict):
    Arn: str
    IngestionStatus: IngestionStatusType
    CreatedTime: datetime
    IngestionId: NotRequired[str]
    ErrorInfo: NotRequired[ErrorInfoTypeDef]
    RowInfo: NotRequired[RowInfoTypeDef]
    QueueInfo: NotRequired[QueueInfoTypeDef]
    IngestionTimeInSeconds: NotRequired[int]
    IngestionSizeInBytes: NotRequired[int]
    RequestSource: NotRequired[IngestionRequestSourceType]
    RequestType: NotRequired[IngestionRequestTypeType]


class IntegerDatasetParameterOutputTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[IntegerDatasetParameterDefaultValuesOutputTypeDef]


IntegerDatasetParameterDefaultValuesUnionTypeDef = Union[
    IntegerDatasetParameterDefaultValuesTypeDef, IntegerDatasetParameterDefaultValuesOutputTypeDef
]
IntegerParameterUnionTypeDef = Union[IntegerParameterTypeDef, IntegerParameterOutputTypeDef]
JoinInstructionTypeDef = TypedDict(
    "JoinInstructionTypeDef",
    {
        "LeftOperand": str,
        "RightOperand": str,
        "Type": JoinTypeType,
        "OnClause": str,
        "LeftJoinKeyProperties": NotRequired[JoinKeyPropertiesTypeDef],
        "RightJoinKeyProperties": NotRequired[JoinKeyPropertiesTypeDef],
    },
)


class KPIVisualLayoutOptionsTypeDef(TypedDict):
    StandardLayout: NotRequired[KPIVisualStandardLayoutTypeDef]


class LineChartDefaultSeriesSettingsTypeDef(TypedDict):
    AxisBinding: NotRequired[AxisBindingType]
    LineStyleSettings: NotRequired[LineChartLineStyleSettingsTypeDef]
    MarkerStyleSettings: NotRequired[LineChartMarkerStyleSettingsTypeDef]


class LineChartSeriesSettingsTypeDef(TypedDict):
    LineStyleSettings: NotRequired[LineChartLineStyleSettingsTypeDef]
    MarkerStyleSettings: NotRequired[LineChartMarkerStyleSettingsTypeDef]


class ListFolderMembersResponseTypeDef(TypedDict):
    Status: int
    FolderMemberList: List[MemberIdArnPairTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTemplateVersionsResponseTypeDef(TypedDict):
    TemplateVersionSummaryList: List[TemplateVersionSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTemplatesResponseTypeDef(TypedDict):
    TemplateSummaryList: List[TemplateSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListThemeVersionsResponseTypeDef(TypedDict):
    ThemeVersionSummaryList: List[ThemeVersionSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListThemesResponseTypeDef(TypedDict):
    ThemeSummaryList: List[ThemeSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTopicsResponseTypeDef(TypedDict):
    TopicsSummaries: List[TopicSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchTopicsResponseTypeDef(TypedDict):
    TopicSummaryList: List[TopicSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class VisualSubtitleLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    FormatText: NotRequired[LongFormatTextTypeDef]


class S3ParametersTypeDef(TypedDict):
    ManifestFileLocation: ManifestFileLocationTypeDef
    RoleArn: NotRequired[str]


class TileLayoutStyleTypeDef(TypedDict):
    Gutter: NotRequired[GutterStyleTypeDef]
    Margin: NotRequired[MarginStyleTypeDef]


class NamedEntityDefinitionOutputTypeDef(TypedDict):
    FieldName: NotRequired[str]
    PropertyName: NotRequired[str]
    PropertyRole: NotRequired[PropertyRoleType]
    PropertyUsage: NotRequired[PropertyUsageType]
    Metric: NotRequired[NamedEntityDefinitionMetricOutputTypeDef]


NamedEntityDefinitionMetricUnionTypeDef = Union[
    NamedEntityDefinitionMetricTypeDef, NamedEntityDefinitionMetricOutputTypeDef
]


class NamespaceInfoV2TypeDef(TypedDict):
    Name: NotRequired[str]
    Arn: NotRequired[str]
    CapacityRegion: NotRequired[str]
    CreationStatus: NotRequired[NamespaceStatusType]
    IdentityStore: NotRequired[Literal["QUICKSIGHT"]]
    NamespaceError: NotRequired[NamespaceErrorTypeDef]
    IamIdentityCenterApplicationArn: NotRequired[str]
    IamIdentityCenterInstanceArn: NotRequired[str]


class VPCConnectionSummaryTypeDef(TypedDict):
    VPCConnectionId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    VPCId: NotRequired[str]
    SecurityGroupIds: NotRequired[List[str]]
    DnsResolvers: NotRequired[List[str]]
    Status: NotRequired[VPCConnectionResourceStatusType]
    AvailabilityStatus: NotRequired[VPCConnectionAvailabilityStatusType]
    NetworkInterfaces: NotRequired[List[NetworkInterfaceTypeDef]]
    RoleArn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class VPCConnectionTypeDef(TypedDict):
    VPCConnectionId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    VPCId: NotRequired[str]
    SecurityGroupIds: NotRequired[List[str]]
    DnsResolvers: NotRequired[List[str]]
    Status: NotRequired[VPCConnectionResourceStatusType]
    AvailabilityStatus: NotRequired[VPCConnectionAvailabilityStatusType]
    NetworkInterfaces: NotRequired[List[NetworkInterfaceTypeDef]]
    RoleArn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]


class OverrideDatasetParameterOperationOutputTypeDef(TypedDict):
    ParameterName: str
    NewParameterName: NotRequired[str]
    NewDefaultValues: NotRequired[NewDefaultValuesOutputTypeDef]


class NumericSeparatorConfigurationTypeDef(TypedDict):
    DecimalSeparator: NotRequired[NumericSeparatorSymbolType]
    ThousandsSeparator: NotRequired[ThousandSeparatorOptionsTypeDef]


class NumericalAggregationFunctionTypeDef(TypedDict):
    SimpleNumericalAggregation: NotRequired[SimpleNumericalAggregationFunctionType]
    PercentileAggregation: NotRequired[PercentileAggregationTypeDef]


class ParametersOutputTypeDef(TypedDict):
    StringParameters: NotRequired[List[StringParameterOutputTypeDef]]
    IntegerParameters: NotRequired[List[IntegerParameterOutputTypeDef]]
    DecimalParameters: NotRequired[List[DecimalParameterOutputTypeDef]]
    DateTimeParameters: NotRequired[List[DateTimeParameterOutputTypeDef]]


class VisibleRangeOptionsTypeDef(TypedDict):
    PercentRange: NotRequired[PercentVisibleRangeTypeDef]


class PluginVisualOptionsOutputTypeDef(TypedDict):
    VisualProperties: NotRequired[List[PluginVisualPropertyTypeDef]]


class PluginVisualOptionsTypeDef(TypedDict):
    VisualProperties: NotRequired[Sequence[PluginVisualPropertyTypeDef]]


ProjectOperationUnionTypeDef = Union[ProjectOperationTypeDef, ProjectOperationOutputTypeDef]


class RadarChartSeriesSettingsTypeDef(TypedDict):
    AreaStyleSettings: NotRequired[RadarChartAreaStyleSettingsTypeDef]


class TopicRangeFilterConstantTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    RangeConstant: NotRequired[RangeConstantTypeDef]


class RedshiftParametersOutputTypeDef(TypedDict):
    Database: str
    Host: NotRequired[str]
    Port: NotRequired[int]
    ClusterId: NotRequired[str]
    IAMParameters: NotRequired[RedshiftIAMParametersOutputTypeDef]
    IdentityCenterConfiguration: NotRequired[IdentityCenterConfigurationTypeDef]


RedshiftIAMParametersUnionTypeDef = Union[
    RedshiftIAMParametersTypeDef, RedshiftIAMParametersOutputTypeDef
]


class RefreshFrequencyTypeDef(TypedDict):
    Interval: RefreshIntervalType
    RefreshOnDay: NotRequired[ScheduleRefreshOnEntityTypeDef]
    Timezone: NotRequired[str]
    TimeOfTheDay: NotRequired[str]


class RegisteredUserConsoleFeatureConfigurationsTypeDef(TypedDict):
    StatePersistence: NotRequired[StatePersistenceConfigurationsTypeDef]
    SharedView: NotRequired[SharedViewConfigurationsTypeDef]


class RegisteredUserDashboardFeatureConfigurationsTypeDef(TypedDict):
    StatePersistence: NotRequired[StatePersistenceConfigurationsTypeDef]
    SharedView: NotRequired[SharedViewConfigurationsTypeDef]
    Bookmarks: NotRequired[BookmarksConfigurationsTypeDef]


RowAlternateColorOptionsUnionTypeDef = Union[
    RowAlternateColorOptionsTypeDef, RowAlternateColorOptionsOutputTypeDef
]


class RowLevelPermissionTagConfigurationOutputTypeDef(TypedDict):
    TagRules: List[RowLevelPermissionTagRuleTypeDef]
    Status: NotRequired[StatusType]
    TagRuleConfigurations: NotRequired[List[List[str]]]


class RowLevelPermissionTagConfigurationTypeDef(TypedDict):
    TagRules: Sequence[RowLevelPermissionTagRuleTypeDef]
    Status: NotRequired[StatusType]
    TagRuleConfigurations: NotRequired[Sequence[Sequence[str]]]


class SnapshotS3DestinationConfigurationTypeDef(TypedDict):
    BucketConfiguration: S3BucketConfigurationTypeDef


class S3SourceOutputTypeDef(TypedDict):
    DataSourceArn: str
    InputColumns: List[InputColumnTypeDef]
    UploadSettings: NotRequired[UploadSettingsTypeDef]


class S3SourceTypeDef(TypedDict):
    DataSourceArn: str
    InputColumns: Sequence[InputColumnTypeDef]
    UploadSettings: NotRequired[UploadSettingsTypeDef]


SameSheetTargetVisualConfigurationUnionTypeDef = Union[
    SameSheetTargetVisualConfigurationTypeDef, SameSheetTargetVisualConfigurationOutputTypeDef
]


class SearchTopicsRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[TopicSearchFilterTypeDef]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[int]


class SearchTopicsRequestSearchTopicsPaginateTypeDef(TypedDict):
    AwsAccountId: str
    Filters: Sequence[TopicSearchFilterTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SectionBasedLayoutPaperCanvasSizeOptionsTypeDef(TypedDict):
    PaperSize: NotRequired[PaperSizeType]
    PaperOrientation: NotRequired[PaperOrientationType]
    PaperMargin: NotRequired[SpacingTypeDef]


class SectionStyleTypeDef(TypedDict):
    Height: NotRequired[str]
    Padding: NotRequired[SpacingTypeDef]


class SelectedSheetsFilterScopeConfigurationOutputTypeDef(TypedDict):
    SheetVisualScopingConfigurations: NotRequired[
        List[SheetVisualScopingConfigurationOutputTypeDef]
    ]


SemanticEntityTypeUnionTypeDef = Union[SemanticEntityTypeTypeDef, SemanticEntityTypeOutputTypeDef]
SemanticTypeUnionTypeDef = Union[SemanticTypeTypeDef, SemanticTypeOutputTypeDef]


class SheetElementRenderingRuleTypeDef(TypedDict):
    Expression: str
    ConfigurationOverrides: SheetElementConfigurationOverridesTypeDef


class SheetImageSourceTypeDef(TypedDict):
    SheetImageStaticFileSource: NotRequired[SheetImageStaticFileSourceTypeDef]


class SheetImageTooltipConfigurationTypeDef(TypedDict):
    TooltipText: NotRequired[SheetImageTooltipTextTypeDef]
    Visibility: NotRequired[VisibilityType]


SheetVisualScopingConfigurationUnionTypeDef = Union[
    SheetVisualScopingConfigurationTypeDef, SheetVisualScopingConfigurationOutputTypeDef
]


class VisualTitleLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    FormatText: NotRequired[ShortFormatTextTypeDef]


class SingleAxisOptionsTypeDef(TypedDict):
    YAxisOptions: NotRequired[YAxisOptionsTypeDef]


class TopicTemplateOutputTypeDef(TypedDict):
    TemplateType: NotRequired[str]
    Slots: NotRequired[List[SlotTypeDef]]


class TopicTemplateTypeDef(TypedDict):
    TemplateType: NotRequired[str]
    Slots: NotRequired[Sequence[SlotTypeDef]]


class SnapshotUserConfigurationRedactedTypeDef(TypedDict):
    AnonymousUsers: NotRequired[List[SnapshotAnonymousUserRedactedTypeDef]]


class SnapshotFileOutputTypeDef(TypedDict):
    SheetSelections: List[SnapshotFileSheetSelectionOutputTypeDef]
    FormatType: SnapshotFileFormatTypeType


SnapshotFileSheetSelectionUnionTypeDef = Union[
    SnapshotFileSheetSelectionTypeDef, SnapshotFileSheetSelectionOutputTypeDef
]


class StaticFileSourceTypeDef(TypedDict):
    UrlOptions: NotRequired[StaticFileUrlSourceOptionsTypeDef]
    S3Options: NotRequired[StaticFileS3SourceOptionsTypeDef]


class StringDatasetParameterOutputTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[StringDatasetParameterDefaultValuesOutputTypeDef]


StringDatasetParameterDefaultValuesUnionTypeDef = Union[
    StringDatasetParameterDefaultValuesTypeDef, StringDatasetParameterDefaultValuesOutputTypeDef
]
StringParameterUnionTypeDef = Union[StringParameterTypeDef, StringParameterOutputTypeDef]


class UpdateKeyRegistrationResponseTypeDef(TypedDict):
    FailedKeyRegistration: List[FailedKeyRegistrationEntryTypeDef]
    SuccessfulKeyRegistration: List[SuccessfulKeyRegistrationEntryTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class TableFieldImageConfigurationTypeDef(TypedDict):
    SizingOptions: NotRequired[TableCellImageSizingConfigurationTypeDef]


TablePinnedFieldOptionsUnionTypeDef = Union[
    TablePinnedFieldOptionsTypeDef, TablePinnedFieldOptionsOutputTypeDef
]


class TopicNumericEqualityFilterTypeDef(TypedDict):
    Constant: NotRequired[TopicSingularFilterConstantTypeDef]
    Aggregation: NotRequired[NamedFilterAggTypeType]


class TopicRelativeDateFilterTypeDef(TypedDict):
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    RelativeDateFilterFunction: NotRequired[TopicRelativeDateFilterFunctionType]
    Constant: NotRequired[TopicSingularFilterConstantTypeDef]


class TotalAggregationOptionTypeDef(TypedDict):
    FieldId: str
    TotalAggregationFunction: TotalAggregationFunctionTypeDef


UntagColumnOperationUnionTypeDef = Union[
    UntagColumnOperationTypeDef, UntagColumnOperationOutputTypeDef
]


class WaterfallChartColorConfigurationTypeDef(TypedDict):
    GroupColorConfiguration: NotRequired[WaterfallChartGroupColorConfigurationTypeDef]


class CascadingControlConfigurationOutputTypeDef(TypedDict):
    SourceControls: NotRequired[List[CascadingControlSourceTypeDef]]


class CascadingControlConfigurationTypeDef(TypedDict):
    SourceControls: NotRequired[Sequence[CascadingControlSourceTypeDef]]


CategoryDrillDownFilterUnionTypeDef = Union[
    CategoryDrillDownFilterTypeDef, CategoryDrillDownFilterOutputTypeDef
]
ContributionAnalysisDefaultUnionTypeDef = Union[
    ContributionAnalysisDefaultTypeDef, ContributionAnalysisDefaultOutputTypeDef
]


class DateTimeDefaultValuesOutputTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[List[datetime]]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]


class DateTimeDefaultValuesTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[Sequence[TimestampTypeDef]]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]


class DecimalDefaultValuesOutputTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[List[float]]


class DecimalDefaultValuesTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[Sequence[float]]


class IntegerDefaultValuesOutputTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[List[int]]


class IntegerDefaultValuesTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[Sequence[int]]


class StringDefaultValuesOutputTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[List[str]]


class StringDefaultValuesTypeDef(TypedDict):
    DynamicValue: NotRequired[DynamicDefaultValueTypeDef]
    StaticValues: NotRequired[Sequence[str]]


FilterOperationSelectedFieldsConfigurationUnionTypeDef = Union[
    FilterOperationSelectedFieldsConfigurationTypeDef,
    FilterOperationSelectedFieldsConfigurationOutputTypeDef,
]
ParameterSelectableValuesUnionTypeDef = Union[
    ParameterSelectableValuesTypeDef, ParameterSelectableValuesOutputTypeDef
]


class DrillDownFilterOutputTypeDef(TypedDict):
    NumericEqualityFilter: NotRequired[NumericEqualityDrillDownFilterTypeDef]
    CategoryFilter: NotRequired[CategoryDrillDownFilterOutputTypeDef]
    TimeRangeFilter: NotRequired[TimeRangeDrillDownFilterOutputTypeDef]


class AnalysisSourceEntityTypeDef(TypedDict):
    SourceTemplate: NotRequired[AnalysisSourceTemplateTypeDef]


class DashboardSourceEntityTypeDef(TypedDict):
    SourceTemplate: NotRequired[DashboardSourceTemplateTypeDef]


class TemplateSourceEntityTypeDef(TypedDict):
    SourceAnalysis: NotRequired[TemplateSourceAnalysisTypeDef]
    SourceTemplate: NotRequired[TemplateSourceTemplateTypeDef]


class AnonymousUserDashboardEmbeddingConfigurationTypeDef(TypedDict):
    InitialDashboardId: str
    EnabledFeatures: NotRequired[Sequence[Literal["SHARED_VIEW"]]]
    DisabledFeatures: NotRequired[Sequence[Literal["SHARED_VIEW"]]]
    FeatureConfigurations: NotRequired[AnonymousUserDashboardFeatureConfigurationsTypeDef]


class DescribeAssetBundleExportJobResponseTypeDef(TypedDict):
    JobStatus: AssetBundleExportJobStatusType
    DownloadUrl: str
    Errors: List[AssetBundleExportJobErrorTypeDef]
    Arn: str
    CreatedTime: datetime
    AssetBundleExportJobId: str
    AwsAccountId: str
    ResourceArns: List[str]
    IncludeAllDependencies: bool
    ExportFormat: AssetBundleExportFormatType
    CloudFormationOverridePropertyConfiguration: (
        AssetBundleCloudFormationOverridePropertyConfigurationOutputTypeDef
    )
    RequestId: str
    Status: int
    IncludePermissions: bool
    IncludeTags: bool
    ValidationStrategy: AssetBundleExportJobValidationStrategyTypeDef
    Warnings: List[AssetBundleExportJobWarningTypeDef]
    IncludeFolderMemberships: bool
    IncludeFolderMembers: IncludeFolderMembersType
    ResponseMetadata: ResponseMetadataTypeDef


class AssetBundleCloudFormationOverridePropertyConfigurationTypeDef(TypedDict):
    ResourceIdOverrideConfiguration: NotRequired[
        AssetBundleExportJobResourceIdOverrideConfigurationTypeDef
    ]
    VPCConnections: NotRequired[
        Sequence[AssetBundleExportJobVPCConnectionOverridePropertiesUnionTypeDef]
    ]
    RefreshSchedules: NotRequired[
        Sequence[AssetBundleExportJobRefreshScheduleOverridePropertiesUnionTypeDef]
    ]
    DataSources: NotRequired[Sequence[AssetBundleExportJobDataSourceOverridePropertiesUnionTypeDef]]
    DataSets: NotRequired[Sequence[AssetBundleExportJobDataSetOverridePropertiesUnionTypeDef]]
    Themes: NotRequired[Sequence[AssetBundleExportJobThemeOverridePropertiesUnionTypeDef]]
    Analyses: NotRequired[Sequence[AssetBundleExportJobAnalysisOverridePropertiesUnionTypeDef]]
    Dashboards: NotRequired[Sequence[AssetBundleExportJobDashboardOverridePropertiesUnionTypeDef]]
    Folders: NotRequired[Sequence[AssetBundleExportJobFolderOverridePropertiesUnionTypeDef]]


class AssetBundleImportJobDashboardOverridePermissionsOutputTypeDef(TypedDict):
    DashboardIds: List[str]
    Permissions: NotRequired[AssetBundleResourcePermissionsOutputTypeDef]
    LinkSharingConfiguration: NotRequired[AssetBundleResourceLinkSharingConfigurationOutputTypeDef]


AssetBundleImportJobAnalysisOverrideTagsUnionTypeDef = Union[
    AssetBundleImportJobAnalysisOverrideTagsTypeDef,
    AssetBundleImportJobAnalysisOverrideTagsOutputTypeDef,
]
AssetBundleImportJobDashboardOverrideTagsUnionTypeDef = Union[
    AssetBundleImportJobDashboardOverrideTagsTypeDef,
    AssetBundleImportJobDashboardOverrideTagsOutputTypeDef,
]
AssetBundleImportJobDataSetOverrideTagsUnionTypeDef = Union[
    AssetBundleImportJobDataSetOverrideTagsTypeDef,
    AssetBundleImportJobDataSetOverrideTagsOutputTypeDef,
]
AssetBundleImportJobDataSourceOverrideTagsUnionTypeDef = Union[
    AssetBundleImportJobDataSourceOverrideTagsTypeDef,
    AssetBundleImportJobDataSourceOverrideTagsOutputTypeDef,
]
AssetBundleImportJobFolderOverrideTagsUnionTypeDef = Union[
    AssetBundleImportJobFolderOverrideTagsTypeDef,
    AssetBundleImportJobFolderOverrideTagsOutputTypeDef,
]
AssetBundleImportJobThemeOverrideTagsUnionTypeDef = Union[
    AssetBundleImportJobThemeOverrideTagsTypeDef, AssetBundleImportJobThemeOverrideTagsOutputTypeDef
]


class AssetBundleImportJobOverrideTagsOutputTypeDef(TypedDict):
    VPCConnections: NotRequired[List[AssetBundleImportJobVPCConnectionOverrideTagsOutputTypeDef]]
    DataSources: NotRequired[List[AssetBundleImportJobDataSourceOverrideTagsOutputTypeDef]]
    DataSets: NotRequired[List[AssetBundleImportJobDataSetOverrideTagsOutputTypeDef]]
    Themes: NotRequired[List[AssetBundleImportJobThemeOverrideTagsOutputTypeDef]]
    Analyses: NotRequired[List[AssetBundleImportJobAnalysisOverrideTagsOutputTypeDef]]
    Dashboards: NotRequired[List[AssetBundleImportJobDashboardOverrideTagsOutputTypeDef]]
    Folders: NotRequired[List[AssetBundleImportJobFolderOverrideTagsOutputTypeDef]]


AssetBundleImportJobVPCConnectionOverrideTagsUnionTypeDef = Union[
    AssetBundleImportJobVPCConnectionOverrideTagsTypeDef,
    AssetBundleImportJobVPCConnectionOverrideTagsOutputTypeDef,
]


class SnowflakeParametersTypeDef(TypedDict):
    Host: str
    Database: str
    Warehouse: str
    AuthenticationType: NotRequired[AuthenticationTypeType]
    DatabaseAccessControlRole: NotRequired[str]
    OAuthParameters: NotRequired[OAuthParametersTypeDef]


class StarburstParametersTypeDef(TypedDict):
    Host: str
    Port: int
    Catalog: str
    ProductType: NotRequired[StarburstProductTypeType]
    DatabaseAccessControlRole: NotRequired[str]
    AuthenticationType: NotRequired[AuthenticationTypeType]
    OAuthParameters: NotRequired[OAuthParametersTypeDef]


AssetBundleImportJobRefreshScheduleOverrideParametersUnionTypeDef = Union[
    AssetBundleImportJobRefreshScheduleOverrideParametersTypeDef,
    AssetBundleImportJobRefreshScheduleOverrideParametersOutputTypeDef,
]
CustomParameterValuesUnionTypeDef = Union[
    CustomParameterValuesTypeDef, CustomParameterValuesOutputTypeDef
]
DateTimeDatasetParameterDefaultValuesUnionTypeDef = Union[
    DateTimeDatasetParameterDefaultValuesTypeDef, DateTimeDatasetParameterDefaultValuesOutputTypeDef
]
DateTimeParameterUnionTypeDef = Union[DateTimeParameterTypeDef, DateTimeParameterOutputTypeDef]
DateTimeValueWhenUnsetConfigurationUnionTypeDef = Union[
    DateTimeValueWhenUnsetConfigurationTypeDef, DateTimeValueWhenUnsetConfigurationOutputTypeDef
]
NewDefaultValuesUnionTypeDef = Union[NewDefaultValuesTypeDef, NewDefaultValuesOutputTypeDef]
TimeRangeDrillDownFilterUnionTypeDef = Union[
    TimeRangeDrillDownFilterTypeDef, TimeRangeDrillDownFilterOutputTypeDef
]


class CreateTopicRefreshScheduleRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    DatasetArn: str
    RefreshSchedule: TopicRefreshScheduleTypeDef
    DatasetName: NotRequired[str]


class UpdateTopicRefreshScheduleRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    DatasetId: str
    RefreshSchedule: TopicRefreshScheduleTypeDef


WhatIfPointScenarioUnionTypeDef = Union[
    WhatIfPointScenarioTypeDef, WhatIfPointScenarioOutputTypeDef
]
WhatIfRangeScenarioUnionTypeDef = Union[
    WhatIfRangeScenarioTypeDef, WhatIfRangeScenarioOutputTypeDef
]


class AssetBundleImportJobAnalysisOverridePermissionsTypeDef(TypedDict):
    AnalysisIds: Sequence[str]
    Permissions: AssetBundleResourcePermissionsUnionTypeDef


class AssetBundleImportJobDataSetOverridePermissionsTypeDef(TypedDict):
    DataSetIds: Sequence[str]
    Permissions: AssetBundleResourcePermissionsUnionTypeDef


class AssetBundleImportJobDataSourceOverridePermissionsTypeDef(TypedDict):
    DataSourceIds: Sequence[str]
    Permissions: AssetBundleResourcePermissionsUnionTypeDef


class AssetBundleImportJobFolderOverridePermissionsTypeDef(TypedDict):
    FolderIds: Sequence[str]
    Permissions: NotRequired[AssetBundleResourcePermissionsUnionTypeDef]


class AssetBundleImportJobThemeOverridePermissionsTypeDef(TypedDict):
    ThemeIds: Sequence[str]
    Permissions: AssetBundleResourcePermissionsUnionTypeDef


class AssetBundleResourceLinkSharingConfigurationTypeDef(TypedDict):
    Permissions: NotRequired[AssetBundleResourcePermissionsUnionTypeDef]


AxisDisplayRangeUnionTypeDef = Union[AxisDisplayRangeTypeDef, AxisDisplayRangeOutputTypeDef]


class NumericAxisOptionsOutputTypeDef(TypedDict):
    Scale: NotRequired[AxisScaleTypeDef]
    Range: NotRequired[AxisDisplayRangeOutputTypeDef]


class BrandElementStyleTypeDef(TypedDict):
    NavbarStyle: NotRequired[NavbarStyleTypeDef]


CreateColumnsOperationUnionTypeDef = Union[
    CreateColumnsOperationTypeDef, CreateColumnsOperationOutputTypeDef
]


class DescribeCustomPermissionsResponseTypeDef(TypedDict):
    Status: int
    CustomPermissions: CustomPermissionsTypeDef
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListCustomPermissionsResponseTypeDef(TypedDict):
    Status: int
    CustomPermissionsList: List[CustomPermissionsTypeDef]
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ClusterMarkerConfigurationTypeDef(TypedDict):
    ClusterMarker: NotRequired[ClusterMarkerTypeDef]


TopicConstantValueUnionTypeDef = Union[TopicConstantValueTypeDef, TopicConstantValueOutputTypeDef]


class TopicCategoryFilterOutputTypeDef(TypedDict):
    CategoryFilterFunction: NotRequired[CategoryFilterFunctionType]
    CategoryFilterType: NotRequired[CategoryFilterTypeType]
    Constant: NotRequired[TopicCategoryFilterConstantOutputTypeDef]
    Inverse: NotRequired[bool]


class TopicCategoryFilterConstantTypeDef(TypedDict):
    ConstantType: NotRequired[ConstantTypeType]
    SingularConstant: NotRequired[str]
    CollectiveConstant: NotRequired[CollectiveConstantUnionTypeDef]


ColorScaleUnionTypeDef = Union[ColorScaleTypeDef, ColorScaleOutputTypeDef]
ColorsConfigurationUnionTypeDef = Union[
    ColorsConfigurationTypeDef, ColorsConfigurationOutputTypeDef
]


class TagColumnOperationOutputTypeDef(TypedDict):
    ColumnName: str
    Tags: List[ColumnTagTypeDef]


class TagColumnOperationTypeDef(TypedDict):
    ColumnName: str
    Tags: Sequence[ColumnTagTypeDef]


ColumnGroupSchemaUnionTypeDef = Union[ColumnGroupSchemaTypeDef, ColumnGroupSchemaOutputTypeDef]


class DataSetConfigurationOutputTypeDef(TypedDict):
    Placeholder: NotRequired[str]
    DataSetSchema: NotRequired[DataSetSchemaOutputTypeDef]
    ColumnGroupSchemaList: NotRequired[List[ColumnGroupSchemaOutputTypeDef]]


DataSetSchemaUnionTypeDef = Union[DataSetSchemaTypeDef, DataSetSchemaOutputTypeDef]


class ConditionalFormattingIconTypeDef(TypedDict):
    IconSet: NotRequired[ConditionalFormattingIconSetTypeDef]
    CustomCondition: NotRequired[ConditionalFormattingCustomIconConditionTypeDef]


class ListDataSetsResponseTypeDef(TypedDict):
    DataSetSummaries: List[DataSetSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SearchDataSetsResponseTypeDef(TypedDict):
    DataSetSummaries: List[DataSetSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DestinationParameterValueConfigurationOutputTypeDef(TypedDict):
    CustomValuesConfiguration: NotRequired[CustomValuesConfigurationOutputTypeDef]
    SelectAllValueOptions: NotRequired[Literal["ALL_VALUES"]]
    SourceParameterName: NotRequired[str]
    SourceField: NotRequired[str]
    SourceColumn: NotRequired[ColumnIdentifierTypeDef]


CustomSqlUnionTypeDef = Union[CustomSqlTypeDef, CustomSqlOutputTypeDef]
RelationalTableUnionTypeDef = Union[RelationalTableTypeDef, RelationalTableOutputTypeDef]


class CustomContentConfigurationTypeDef(TypedDict):
    ContentUrl: NotRequired[str]
    ContentType: NotRequired[CustomContentTypeType]
    ImageScaling: NotRequired[CustomContentImageScalingConfigurationType]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class DashboardPublishOptionsTypeDef(TypedDict):
    AdHocFilteringOption: NotRequired[AdHocFilteringOptionTypeDef]
    ExportToCSVOption: NotRequired[ExportToCSVOptionTypeDef]
    SheetControlsOption: NotRequired[SheetControlsOptionTypeDef]
    VisualPublishOptions: NotRequired[DashboardVisualPublishOptionsTypeDef]
    SheetLayoutElementMaximizationOption: NotRequired[SheetLayoutElementMaximizationOptionTypeDef]
    VisualMenuOption: NotRequired[VisualMenuOptionTypeDef]
    VisualAxisSortOption: NotRequired[VisualAxisSortOptionTypeDef]
    ExportWithHiddenFieldsOption: NotRequired[ExportWithHiddenFieldsOptionTypeDef]
    DataPointDrillUpDownOption: NotRequired[DataPointDrillUpDownOptionTypeDef]
    DataPointMenuLabelOption: NotRequired[DataPointMenuLabelOptionTypeDef]
    DataPointTooltipOption: NotRequired[DataPointTooltipOptionTypeDef]


class DataPathColorTypeDef(TypedDict):
    Element: DataPathValueTypeDef
    Color: str
    TimeGranularity: NotRequired[TimeGranularityType]


class DataPathSortOutputTypeDef(TypedDict):
    Direction: SortDirectionType
    SortPaths: List[DataPathValueTypeDef]


class DataPathSortTypeDef(TypedDict):
    Direction: SortDirectionType
    SortPaths: Sequence[DataPathValueTypeDef]


class PivotTableDataPathOptionOutputTypeDef(TypedDict):
    DataPathList: List[DataPathValueTypeDef]
    Width: NotRequired[str]


class PivotTableDataPathOptionTypeDef(TypedDict):
    DataPathList: Sequence[DataPathValueTypeDef]
    Width: NotRequired[str]


class PivotTableFieldCollapseStateTargetOutputTypeDef(TypedDict):
    FieldId: NotRequired[str]
    FieldDataPathValues: NotRequired[List[DataPathValueTypeDef]]


class PivotTableFieldCollapseStateTargetTypeDef(TypedDict):
    FieldId: NotRequired[str]
    FieldDataPathValues: NotRequired[Sequence[DataPathValueTypeDef]]


TimeRangeFilterValueUnionTypeDef = Union[
    TimeRangeFilterValueTypeDef, TimeRangeFilterValueOutputTypeDef
]


class DecimalDatasetParameterTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[DecimalDatasetParameterDefaultValuesUnionTypeDef]


class DescribeDashboardPermissionsResponseTypeDef(TypedDict):
    DashboardId: str
    DashboardArn: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    Status: int
    RequestId: str
    LinkSharingConfiguration: LinkSharingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDashboardPermissionsResponseTypeDef(TypedDict):
    DashboardArn: str
    DashboardId: str
    Permissions: List[ResourcePermissionOutputTypeDef]
    RequestId: str
    Status: int
    LinkSharingConfiguration: LinkSharingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class LinkSharingConfigurationTypeDef(TypedDict):
    Permissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]


class ListTopicRefreshSchedulesResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    RefreshSchedules: List[TopicRefreshScheduleSummaryTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DefaultFormattingTypeDef(TypedDict):
    DisplayFormat: NotRequired[DisplayFormatType]
    DisplayFormatOptions: NotRequired[DisplayFormatOptionsTypeDef]


class TopicIRMetricOutputTypeDef(TypedDict):
    MetricId: NotRequired[IdentifierTypeDef]
    Function: NotRequired[AggFunctionOutputTypeDef]
    Operands: NotRequired[List[IdentifierTypeDef]]
    ComparisonMethod: NotRequired[TopicIRComparisonMethodTypeDef]
    Expression: NotRequired[str]
    CalculatedFieldReferences: NotRequired[List[IdentifierTypeDef]]
    DisplayFormat: NotRequired[DisplayFormatType]
    DisplayFormatOptions: NotRequired[DisplayFormatOptionsTypeDef]
    NamedEntity: NotRequired[NamedEntityRefTypeDef]


class TopicIRMetricTypeDef(TypedDict):
    MetricId: NotRequired[IdentifierTypeDef]
    Function: NotRequired[AggFunctionUnionTypeDef]
    Operands: NotRequired[Sequence[IdentifierTypeDef]]
    ComparisonMethod: NotRequired[TopicIRComparisonMethodTypeDef]
    Expression: NotRequired[str]
    CalculatedFieldReferences: NotRequired[Sequence[IdentifierTypeDef]]
    DisplayFormat: NotRequired[DisplayFormatType]
    DisplayFormatOptions: NotRequired[DisplayFormatOptionsTypeDef]
    NamedEntity: NotRequired[NamedEntityRefTypeDef]


class TopicIRFilterOptionOutputTypeDef(TypedDict):
    FilterType: NotRequired[TopicIRFilterTypeType]
    FilterClass: NotRequired[FilterClassType]
    OperandField: NotRequired[IdentifierTypeDef]
    Function: NotRequired[TopicIRFilterFunctionType]
    Constant: NotRequired[TopicConstantValueOutputTypeDef]
    Inverse: NotRequired[bool]
    NullFilter: NotRequired[NullFilterOptionType]
    Aggregation: NotRequired[AggTypeType]
    AggregationFunctionParameters: NotRequired[Dict[str, str]]
    AggregationPartitionBy: NotRequired[List[AggregationPartitionByTypeDef]]
    Range: NotRequired[TopicConstantValueOutputTypeDef]
    Inclusive: NotRequired[bool]
    TimeGranularity: NotRequired[TimeGranularityType]
    LastNextOffset: NotRequired[TopicConstantValueOutputTypeDef]
    AggMetrics: NotRequired[List[FilterAggMetricsTypeDef]]
    TopBottomLimit: NotRequired[TopicConstantValueOutputTypeDef]
    SortDirection: NotRequired[TopicSortDirectionType]
    Anchor: NotRequired[AnchorTypeDef]


class TopicIRGroupByTypeDef(TypedDict):
    FieldName: NotRequired[IdentifierTypeDef]
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    Sort: NotRequired[TopicSortClauseTypeDef]
    DisplayFormat: NotRequired[DisplayFormatType]
    DisplayFormatOptions: NotRequired[DisplayFormatOptionsTypeDef]
    NamedEntity: NotRequired[NamedEntityRefTypeDef]


class CategoryFilterConfigurationTypeDef(TypedDict):
    FilterListConfiguration: NotRequired[FilterListConfigurationUnionTypeDef]
    CustomFilterListConfiguration: NotRequired[CustomFilterListConfigurationUnionTypeDef]
    CustomFilterConfiguration: NotRequired[CustomFilterConfigurationTypeDef]


class CustomActionFilterOperationOutputTypeDef(TypedDict):
    SelectedFieldsConfiguration: FilterOperationSelectedFieldsConfigurationOutputTypeDef
    TargetVisualsConfiguration: FilterOperationTargetVisualsConfigurationOutputTypeDef


class AxisLabelOptionsTypeDef(TypedDict):
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    CustomLabel: NotRequired[str]
    ApplyTo: NotRequired[AxisLabelReferenceOptionsTypeDef]


class DataLabelOptionsOutputTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    CategoryLabelVisibility: NotRequired[VisibilityType]
    MeasureLabelVisibility: NotRequired[VisibilityType]
    DataLabelTypes: NotRequired[List[DataLabelTypeTypeDef]]
    Position: NotRequired[DataLabelPositionType]
    LabelContent: NotRequired[DataLabelContentType]
    LabelFontConfiguration: NotRequired[FontConfigurationTypeDef]
    LabelColor: NotRequired[str]
    Overlap: NotRequired[DataLabelOverlapType]
    TotalsVisibility: NotRequired[VisibilityType]


class DataLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    CategoryLabelVisibility: NotRequired[VisibilityType]
    MeasureLabelVisibility: NotRequired[VisibilityType]
    DataLabelTypes: NotRequired[Sequence[DataLabelTypeTypeDef]]
    Position: NotRequired[DataLabelPositionType]
    LabelContent: NotRequired[DataLabelContentType]
    LabelFontConfiguration: NotRequired[FontConfigurationTypeDef]
    LabelColor: NotRequired[str]
    Overlap: NotRequired[DataLabelOverlapType]
    TotalsVisibility: NotRequired[VisibilityType]


class FunnelChartDataLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    CategoryLabelVisibility: NotRequired[VisibilityType]
    MeasureLabelVisibility: NotRequired[VisibilityType]
    Position: NotRequired[DataLabelPositionType]
    LabelFontConfiguration: NotRequired[FontConfigurationTypeDef]
    LabelColor: NotRequired[str]
    MeasureDataLabelStyle: NotRequired[FunnelChartMeasureDataLabelStyleType]


class LabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    CustomLabel: NotRequired[str]


class PanelTitleOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    HorizontalTextAlignment: NotRequired[HorizontalTextAlignmentType]


class TableFieldCustomTextContentTypeDef(TypedDict):
    FontConfiguration: FontConfigurationTypeDef
    Value: NotRequired[str]


TypographyUnionTypeDef = Union[TypographyTypeDef, TypographyOutputTypeDef]


class ForecastConfigurationOutputTypeDef(TypedDict):
    ForecastProperties: NotRequired[TimeBasedForecastPropertiesTypeDef]
    Scenario: NotRequired[ForecastScenarioOutputTypeDef]


class DefaultFreeFormLayoutConfigurationTypeDef(TypedDict):
    CanvasSizeOptions: FreeFormLayoutCanvasSizeOptionsTypeDef


class SnapshotUserConfigurationTypeDef(TypedDict):
    AnonymousUsers: NotRequired[Sequence[SnapshotAnonymousUserTypeDef]]


class PredictQAResultsResponseTypeDef(TypedDict):
    PrimaryResult: QAResultTypeDef
    AdditionalResults: List[QAResultTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ColumnGroupTypeDef(TypedDict):
    GeoSpatialColumnGroup: NotRequired[GeoSpatialColumnGroupUnionTypeDef]


class GeospatialHeatmapConfigurationOutputTypeDef(TypedDict):
    HeatmapColor: NotRequired[GeospatialHeatmapColorScaleOutputTypeDef]


GeospatialHeatmapColorScaleUnionTypeDef = Union[
    GeospatialHeatmapColorScaleTypeDef, GeospatialHeatmapColorScaleOutputTypeDef
]


class GeospatialCategoricalColorOutputTypeDef(TypedDict):
    CategoryDataColors: List[GeospatialCategoricalDataColorTypeDef]
    NullDataVisibility: NotRequired[VisibilityType]
    NullDataSettings: NotRequired[GeospatialNullDataSettingsTypeDef]
    DefaultOpacity: NotRequired[float]


class GeospatialCategoricalColorTypeDef(TypedDict):
    CategoryDataColors: Sequence[GeospatialCategoricalDataColorTypeDef]
    NullDataVisibility: NotRequired[VisibilityType]
    NullDataSettings: NotRequired[GeospatialNullDataSettingsTypeDef]
    DefaultOpacity: NotRequired[float]


class GeospatialGradientColorOutputTypeDef(TypedDict):
    StepColors: List[GeospatialGradientStepColorTypeDef]
    NullDataVisibility: NotRequired[VisibilityType]
    NullDataSettings: NotRequired[GeospatialNullDataSettingsTypeDef]
    DefaultOpacity: NotRequired[float]


class GeospatialGradientColorTypeDef(TypedDict):
    StepColors: Sequence[GeospatialGradientStepColorTypeDef]
    NullDataVisibility: NotRequired[VisibilityType]
    NullDataSettings: NotRequired[GeospatialNullDataSettingsTypeDef]
    DefaultOpacity: NotRequired[float]


class GlobalTableBorderOptionsTypeDef(TypedDict):
    UniformBorder: NotRequired[TableBorderOptionsTypeDef]
    SideSpecificBorder: NotRequired[TableSideBorderOptionsTypeDef]


class ConditionalFormattingGradientColorOutputTypeDef(TypedDict):
    Expression: str
    Color: GradientColorOutputTypeDef


GradientColorUnionTypeDef = Union[GradientColorTypeDef, GradientColorOutputTypeDef]


class DefaultGridLayoutConfigurationTypeDef(TypedDict):
    CanvasSizeOptions: GridLayoutCanvasSizeOptionsTypeDef


class GridLayoutConfigurationOutputTypeDef(TypedDict):
    Elements: List[GridLayoutElementTypeDef]
    CanvasSizeOptions: NotRequired[GridLayoutCanvasSizeOptionsTypeDef]


class GridLayoutConfigurationTypeDef(TypedDict):
    Elements: Sequence[GridLayoutElementTypeDef]
    CanvasSizeOptions: NotRequired[GridLayoutCanvasSizeOptionsTypeDef]


class ImageSetConfigurationTypeDef(TypedDict):
    Original: ImageConfigurationTypeDef


class ImageSetTypeDef(TypedDict):
    Original: ImageTypeDef
    Height64: NotRequired[ImageTypeDef]
    Height32: NotRequired[ImageTypeDef]


class RefreshConfigurationTypeDef(TypedDict):
    IncrementalRefresh: IncrementalRefreshTypeDef


class DescribeIngestionResponseTypeDef(TypedDict):
    Ingestion: IngestionTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListIngestionsResponseTypeDef(TypedDict):
    Ingestions: List[IngestionTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class IntegerDatasetParameterTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[IntegerDatasetParameterDefaultValuesUnionTypeDef]


class LogicalTableSourceTypeDef(TypedDict):
    JoinInstruction: NotRequired[JoinInstructionTypeDef]
    PhysicalTableId: NotRequired[str]
    DataSetArn: NotRequired[str]


class DataFieldSeriesItemTypeDef(TypedDict):
    FieldId: str
    AxisBinding: AxisBindingType
    FieldValue: NotRequired[str]
    Settings: NotRequired[LineChartSeriesSettingsTypeDef]


class FieldSeriesItemTypeDef(TypedDict):
    FieldId: str
    AxisBinding: AxisBindingType
    Settings: NotRequired[LineChartSeriesSettingsTypeDef]


class SheetStyleTypeDef(TypedDict):
    Tile: NotRequired[TileStyleTypeDef]
    TileLayout: NotRequired[TileLayoutStyleTypeDef]


class TopicNamedEntityOutputTypeDef(TypedDict):
    EntityName: str
    EntityDescription: NotRequired[str]
    EntitySynonyms: NotRequired[List[str]]
    SemanticEntityType: NotRequired[SemanticEntityTypeOutputTypeDef]
    Definition: NotRequired[List[NamedEntityDefinitionOutputTypeDef]]


class NamedEntityDefinitionTypeDef(TypedDict):
    FieldName: NotRequired[str]
    PropertyName: NotRequired[str]
    PropertyRole: NotRequired[PropertyRoleType]
    PropertyUsage: NotRequired[PropertyUsageType]
    Metric: NotRequired[NamedEntityDefinitionMetricUnionTypeDef]


class DescribeNamespaceResponseTypeDef(TypedDict):
    Namespace: NamespaceInfoV2TypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListNamespacesResponseTypeDef(TypedDict):
    Namespaces: List[NamespaceInfoV2TypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListVPCConnectionsResponseTypeDef(TypedDict):
    VPCConnectionSummaries: List[VPCConnectionSummaryTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeVPCConnectionResponseTypeDef(TypedDict):
    VPCConnection: VPCConnectionTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class CurrencyDisplayFormatConfigurationTypeDef(TypedDict):
    Prefix: NotRequired[str]
    Suffix: NotRequired[str]
    SeparatorConfiguration: NotRequired[NumericSeparatorConfigurationTypeDef]
    Symbol: NotRequired[str]
    DecimalPlacesConfiguration: NotRequired[DecimalPlacesConfigurationTypeDef]
    NumberScale: NotRequired[NumberScaleType]
    NegativeValueConfiguration: NotRequired[NegativeValueConfigurationTypeDef]
    NullValueFormatConfiguration: NotRequired[NullValueFormatConfigurationTypeDef]


class NumberDisplayFormatConfigurationTypeDef(TypedDict):
    Prefix: NotRequired[str]
    Suffix: NotRequired[str]
    SeparatorConfiguration: NotRequired[NumericSeparatorConfigurationTypeDef]
    DecimalPlacesConfiguration: NotRequired[DecimalPlacesConfigurationTypeDef]
    NumberScale: NotRequired[NumberScaleType]
    NegativeValueConfiguration: NotRequired[NegativeValueConfigurationTypeDef]
    NullValueFormatConfiguration: NotRequired[NullValueFormatConfigurationTypeDef]


class PercentageDisplayFormatConfigurationTypeDef(TypedDict):
    Prefix: NotRequired[str]
    Suffix: NotRequired[str]
    SeparatorConfiguration: NotRequired[NumericSeparatorConfigurationTypeDef]
    DecimalPlacesConfiguration: NotRequired[DecimalPlacesConfigurationTypeDef]
    NegativeValueConfiguration: NotRequired[NegativeValueConfigurationTypeDef]
    NullValueFormatConfiguration: NotRequired[NullValueFormatConfigurationTypeDef]


class AggregationFunctionTypeDef(TypedDict):
    NumericalAggregationFunction: NotRequired[NumericalAggregationFunctionTypeDef]
    CategoricalAggregationFunction: NotRequired[CategoricalAggregationFunctionType]
    DateAggregationFunction: NotRequired[DateAggregationFunctionType]
    AttributeAggregationFunction: NotRequired[AttributeAggregationFunctionTypeDef]


class ScrollBarOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    VisibleRange: NotRequired[VisibleRangeOptionsTypeDef]


PluginVisualOptionsUnionTypeDef = Union[
    PluginVisualOptionsTypeDef, PluginVisualOptionsOutputTypeDef
]


class TopicDateRangeFilterTypeDef(TypedDict):
    Inclusive: NotRequired[bool]
    Constant: NotRequired[TopicRangeFilterConstantTypeDef]


class TopicNumericRangeFilterTypeDef(TypedDict):
    Inclusive: NotRequired[bool]
    Constant: NotRequired[TopicRangeFilterConstantTypeDef]
    Aggregation: NotRequired[NamedFilterAggTypeType]


class RedshiftParametersTypeDef(TypedDict):
    Database: str
    Host: NotRequired[str]
    Port: NotRequired[int]
    ClusterId: NotRequired[str]
    IAMParameters: NotRequired[RedshiftIAMParametersUnionTypeDef]
    IdentityCenterConfiguration: NotRequired[IdentityCenterConfigurationTypeDef]


class RefreshScheduleOutputTypeDef(TypedDict):
    ScheduleId: str
    ScheduleFrequency: RefreshFrequencyTypeDef
    RefreshType: IngestionTypeType
    StartAfterDateTime: NotRequired[datetime]
    Arn: NotRequired[str]


class RefreshScheduleTypeDef(TypedDict):
    ScheduleId: str
    ScheduleFrequency: RefreshFrequencyTypeDef
    RefreshType: IngestionTypeType
    StartAfterDateTime: NotRequired[TimestampTypeDef]
    Arn: NotRequired[str]


class RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef(TypedDict):
    InitialPath: NotRequired[str]
    FeatureConfigurations: NotRequired[RegisteredUserConsoleFeatureConfigurationsTypeDef]


class RegisteredUserDashboardEmbeddingConfigurationTypeDef(TypedDict):
    InitialDashboardId: str
    FeatureConfigurations: NotRequired[RegisteredUserDashboardFeatureConfigurationsTypeDef]


class SnapshotDestinationConfigurationOutputTypeDef(TypedDict):
    S3Destinations: NotRequired[List[SnapshotS3DestinationConfigurationTypeDef]]


class SnapshotDestinationConfigurationTypeDef(TypedDict):
    S3Destinations: NotRequired[Sequence[SnapshotS3DestinationConfigurationTypeDef]]


class SnapshotJobS3ResultTypeDef(TypedDict):
    S3DestinationConfiguration: NotRequired[SnapshotS3DestinationConfigurationTypeDef]
    S3Uri: NotRequired[str]
    ErrorInfo: NotRequired[List[SnapshotJobResultErrorInfoTypeDef]]


class PhysicalTableOutputTypeDef(TypedDict):
    RelationalTable: NotRequired[RelationalTableOutputTypeDef]
    CustomSql: NotRequired[CustomSqlOutputTypeDef]
    S3Source: NotRequired[S3SourceOutputTypeDef]


S3SourceUnionTypeDef = Union[S3SourceTypeDef, S3SourceOutputTypeDef]


class FilterOperationTargetVisualsConfigurationTypeDef(TypedDict):
    SameSheetTargetVisualConfiguration: NotRequired[SameSheetTargetVisualConfigurationUnionTypeDef]


class SectionBasedLayoutCanvasSizeOptionsTypeDef(TypedDict):
    PaperCanvasSizeOptions: NotRequired[SectionBasedLayoutPaperCanvasSizeOptionsTypeDef]


class FilterScopeConfigurationOutputTypeDef(TypedDict):
    SelectedSheets: NotRequired[SelectedSheetsFilterScopeConfigurationOutputTypeDef]
    AllSheets: NotRequired[Dict[str, Any]]


class FreeFormLayoutElementOutputTypeDef(TypedDict):
    ElementId: str
    ElementType: LayoutElementTypeType
    XAxisLocation: str
    YAxisLocation: str
    Width: str
    Height: str
    Visibility: NotRequired[VisibilityType]
    RenderingRules: NotRequired[List[SheetElementRenderingRuleTypeDef]]
    BorderStyle: NotRequired[FreeFormLayoutElementBorderStyleTypeDef]
    SelectedBorderStyle: NotRequired[FreeFormLayoutElementBorderStyleTypeDef]
    BackgroundStyle: NotRequired[FreeFormLayoutElementBackgroundStyleTypeDef]
    LoadingAnimation: NotRequired[LoadingAnimationTypeDef]


class FreeFormLayoutElementTypeDef(TypedDict):
    ElementId: str
    ElementType: LayoutElementTypeType
    XAxisLocation: str
    YAxisLocation: str
    Width: str
    Height: str
    Visibility: NotRequired[VisibilityType]
    RenderingRules: NotRequired[Sequence[SheetElementRenderingRuleTypeDef]]
    BorderStyle: NotRequired[FreeFormLayoutElementBorderStyleTypeDef]
    SelectedBorderStyle: NotRequired[FreeFormLayoutElementBorderStyleTypeDef]
    BackgroundStyle: NotRequired[FreeFormLayoutElementBackgroundStyleTypeDef]
    LoadingAnimation: NotRequired[LoadingAnimationTypeDef]


class SelectedSheetsFilterScopeConfigurationTypeDef(TypedDict):
    SheetVisualScopingConfigurations: NotRequired[
        Sequence[SheetVisualScopingConfigurationUnionTypeDef]
    ]


TopicTemplateUnionTypeDef = Union[TopicTemplateTypeDef, TopicTemplateOutputTypeDef]


class SnapshotFileGroupOutputTypeDef(TypedDict):
    Files: NotRequired[List[SnapshotFileOutputTypeDef]]


class SnapshotFileTypeDef(TypedDict):
    SheetSelections: Sequence[SnapshotFileSheetSelectionUnionTypeDef]
    FormatType: SnapshotFileFormatTypeType


class ImageStaticFileTypeDef(TypedDict):
    StaticFileId: str
    Source: NotRequired[StaticFileSourceTypeDef]


class SpatialStaticFileTypeDef(TypedDict):
    StaticFileId: str
    Source: NotRequired[StaticFileSourceTypeDef]


class DatasetParameterOutputTypeDef(TypedDict):
    StringDatasetParameter: NotRequired[StringDatasetParameterOutputTypeDef]
    DecimalDatasetParameter: NotRequired[DecimalDatasetParameterOutputTypeDef]
    IntegerDatasetParameter: NotRequired[IntegerDatasetParameterOutputTypeDef]
    DateTimeDatasetParameter: NotRequired[DateTimeDatasetParameterOutputTypeDef]


class StringDatasetParameterTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    DefaultValues: NotRequired[StringDatasetParameterDefaultValuesUnionTypeDef]


class FilterCrossSheetControlOutputTypeDef(TypedDict):
    FilterControlId: str
    SourceFilterId: str
    CascadingControlConfiguration: NotRequired[CascadingControlConfigurationOutputTypeDef]


CascadingControlConfigurationUnionTypeDef = Union[
    CascadingControlConfigurationTypeDef, CascadingControlConfigurationOutputTypeDef
]


class DateTimeParameterDeclarationOutputTypeDef(TypedDict):
    Name: str
    DefaultValues: NotRequired[DateTimeDefaultValuesOutputTypeDef]
    TimeGranularity: NotRequired[TimeGranularityType]
    ValueWhenUnset: NotRequired[DateTimeValueWhenUnsetConfigurationOutputTypeDef]
    MappedDataSetParameters: NotRequired[List[MappedDataSetParameterTypeDef]]


DateTimeDefaultValuesUnionTypeDef = Union[
    DateTimeDefaultValuesTypeDef, DateTimeDefaultValuesOutputTypeDef
]


class DecimalParameterDeclarationOutputTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[DecimalDefaultValuesOutputTypeDef]
    ValueWhenUnset: NotRequired[DecimalValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[List[MappedDataSetParameterTypeDef]]


DecimalDefaultValuesUnionTypeDef = Union[
    DecimalDefaultValuesTypeDef, DecimalDefaultValuesOutputTypeDef
]


class IntegerParameterDeclarationOutputTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[IntegerDefaultValuesOutputTypeDef]
    ValueWhenUnset: NotRequired[IntegerValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[List[MappedDataSetParameterTypeDef]]


IntegerDefaultValuesUnionTypeDef = Union[
    IntegerDefaultValuesTypeDef, IntegerDefaultValuesOutputTypeDef
]


class StringParameterDeclarationOutputTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[StringDefaultValuesOutputTypeDef]
    ValueWhenUnset: NotRequired[StringValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[List[MappedDataSetParameterTypeDef]]


StringDefaultValuesUnionTypeDef = Union[
    StringDefaultValuesTypeDef, StringDefaultValuesOutputTypeDef
]


class DateTimeHierarchyOutputTypeDef(TypedDict):
    HierarchyId: str
    DrillDownFilters: NotRequired[List[DrillDownFilterOutputTypeDef]]


class ExplicitHierarchyOutputTypeDef(TypedDict):
    HierarchyId: str
    Columns: List[ColumnIdentifierTypeDef]
    DrillDownFilters: NotRequired[List[DrillDownFilterOutputTypeDef]]


class PredefinedHierarchyOutputTypeDef(TypedDict):
    HierarchyId: str
    Columns: List[ColumnIdentifierTypeDef]
    DrillDownFilters: NotRequired[List[DrillDownFilterOutputTypeDef]]


class AnonymousUserEmbeddingExperienceConfigurationTypeDef(TypedDict):
    Dashboard: NotRequired[AnonymousUserDashboardEmbeddingConfigurationTypeDef]
    DashboardVisual: NotRequired[AnonymousUserDashboardVisualEmbeddingConfigurationTypeDef]
    QSearchBar: NotRequired[AnonymousUserQSearchBarEmbeddingConfigurationTypeDef]
    GenerativeQnA: NotRequired[AnonymousUserGenerativeQnAEmbeddingConfigurationTypeDef]


class StartAssetBundleExportJobRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssetBundleExportJobId: str
    ResourceArns: Sequence[str]
    ExportFormat: AssetBundleExportFormatType
    IncludeAllDependencies: NotRequired[bool]
    CloudFormationOverridePropertyConfiguration: NotRequired[
        AssetBundleCloudFormationOverridePropertyConfigurationTypeDef
    ]
    IncludePermissions: NotRequired[bool]
    IncludeTags: NotRequired[bool]
    ValidationStrategy: NotRequired[AssetBundleExportJobValidationStrategyTypeDef]
    IncludeFolderMemberships: NotRequired[bool]
    IncludeFolderMembers: NotRequired[IncludeFolderMembersType]


class AssetBundleImportJobOverridePermissionsOutputTypeDef(TypedDict):
    DataSources: NotRequired[List[AssetBundleImportJobDataSourceOverridePermissionsOutputTypeDef]]
    DataSets: NotRequired[List[AssetBundleImportJobDataSetOverridePermissionsOutputTypeDef]]
    Themes: NotRequired[List[AssetBundleImportJobThemeOverridePermissionsOutputTypeDef]]
    Analyses: NotRequired[List[AssetBundleImportJobAnalysisOverridePermissionsOutputTypeDef]]
    Dashboards: NotRequired[List[AssetBundleImportJobDashboardOverridePermissionsOutputTypeDef]]
    Folders: NotRequired[List[AssetBundleImportJobFolderOverridePermissionsOutputTypeDef]]


class AssetBundleImportJobOverrideTagsTypeDef(TypedDict):
    VPCConnections: NotRequired[Sequence[AssetBundleImportJobVPCConnectionOverrideTagsUnionTypeDef]]
    DataSources: NotRequired[Sequence[AssetBundleImportJobDataSourceOverrideTagsUnionTypeDef]]
    DataSets: NotRequired[Sequence[AssetBundleImportJobDataSetOverrideTagsUnionTypeDef]]
    Themes: NotRequired[Sequence[AssetBundleImportJobThemeOverrideTagsUnionTypeDef]]
    Analyses: NotRequired[Sequence[AssetBundleImportJobAnalysisOverrideTagsUnionTypeDef]]
    Dashboards: NotRequired[Sequence[AssetBundleImportJobDashboardOverrideTagsUnionTypeDef]]
    Folders: NotRequired[Sequence[AssetBundleImportJobFolderOverrideTagsUnionTypeDef]]


class DataSourceParametersOutputTypeDef(TypedDict):
    AmazonElasticsearchParameters: NotRequired[AmazonElasticsearchParametersTypeDef]
    AthenaParameters: NotRequired[AthenaParametersTypeDef]
    AuroraParameters: NotRequired[AuroraParametersTypeDef]
    AuroraPostgreSqlParameters: NotRequired[AuroraPostgreSqlParametersTypeDef]
    AwsIotAnalyticsParameters: NotRequired[AwsIotAnalyticsParametersTypeDef]
    JiraParameters: NotRequired[JiraParametersTypeDef]
    MariaDbParameters: NotRequired[MariaDbParametersTypeDef]
    MySqlParameters: NotRequired[MySqlParametersTypeDef]
    OracleParameters: NotRequired[OracleParametersTypeDef]
    PostgreSqlParameters: NotRequired[PostgreSqlParametersTypeDef]
    PrestoParameters: NotRequired[PrestoParametersTypeDef]
    RdsParameters: NotRequired[RdsParametersTypeDef]
    RedshiftParameters: NotRequired[RedshiftParametersOutputTypeDef]
    S3Parameters: NotRequired[S3ParametersTypeDef]
    ServiceNowParameters: NotRequired[ServiceNowParametersTypeDef]
    SnowflakeParameters: NotRequired[SnowflakeParametersTypeDef]
    SparkParameters: NotRequired[SparkParametersTypeDef]
    SqlServerParameters: NotRequired[SqlServerParametersTypeDef]
    TeradataParameters: NotRequired[TeradataParametersTypeDef]
    TwitterParameters: NotRequired[TwitterParametersTypeDef]
    AmazonOpenSearchParameters: NotRequired[AmazonOpenSearchParametersTypeDef]
    ExasolParameters: NotRequired[ExasolParametersTypeDef]
    DatabricksParameters: NotRequired[DatabricksParametersTypeDef]
    StarburstParameters: NotRequired[StarburstParametersTypeDef]
    TrinoParameters: NotRequired[TrinoParametersTypeDef]
    BigQueryParameters: NotRequired[BigQueryParametersTypeDef]


class CustomValuesConfigurationTypeDef(TypedDict):
    CustomValues: CustomParameterValuesUnionTypeDef
    IncludeNullValue: NotRequired[bool]


class DateTimeDatasetParameterTypeDef(TypedDict):
    Id: str
    Name: str
    ValueType: DatasetParameterValueTypeType
    TimeGranularity: NotRequired[TimeGranularityType]
    DefaultValues: NotRequired[DateTimeDatasetParameterDefaultValuesUnionTypeDef]


class ParametersTypeDef(TypedDict):
    StringParameters: NotRequired[Sequence[StringParameterUnionTypeDef]]
    IntegerParameters: NotRequired[Sequence[IntegerParameterUnionTypeDef]]
    DecimalParameters: NotRequired[Sequence[DecimalParameterUnionTypeDef]]
    DateTimeParameters: NotRequired[Sequence[DateTimeParameterUnionTypeDef]]


class OverrideDatasetParameterOperationTypeDef(TypedDict):
    ParameterName: str
    NewParameterName: NotRequired[str]
    NewDefaultValues: NotRequired[NewDefaultValuesUnionTypeDef]


class DrillDownFilterTypeDef(TypedDict):
    NumericEqualityFilter: NotRequired[NumericEqualityDrillDownFilterTypeDef]
    CategoryFilter: NotRequired[CategoryDrillDownFilterUnionTypeDef]
    TimeRangeFilter: NotRequired[TimeRangeDrillDownFilterUnionTypeDef]


class ForecastScenarioTypeDef(TypedDict):
    WhatIfPointScenario: NotRequired[WhatIfPointScenarioUnionTypeDef]
    WhatIfRangeScenario: NotRequired[WhatIfRangeScenarioUnionTypeDef]


AssetBundleImportJobAnalysisOverridePermissionsUnionTypeDef = Union[
    AssetBundleImportJobAnalysisOverridePermissionsTypeDef,
    AssetBundleImportJobAnalysisOverridePermissionsOutputTypeDef,
]
AssetBundleImportJobDataSetOverridePermissionsUnionTypeDef = Union[
    AssetBundleImportJobDataSetOverridePermissionsTypeDef,
    AssetBundleImportJobDataSetOverridePermissionsOutputTypeDef,
]
AssetBundleImportJobDataSourceOverridePermissionsUnionTypeDef = Union[
    AssetBundleImportJobDataSourceOverridePermissionsTypeDef,
    AssetBundleImportJobDataSourceOverridePermissionsOutputTypeDef,
]
AssetBundleImportJobFolderOverridePermissionsUnionTypeDef = Union[
    AssetBundleImportJobFolderOverridePermissionsTypeDef,
    AssetBundleImportJobFolderOverridePermissionsOutputTypeDef,
]
AssetBundleImportJobThemeOverridePermissionsUnionTypeDef = Union[
    AssetBundleImportJobThemeOverridePermissionsTypeDef,
    AssetBundleImportJobThemeOverridePermissionsOutputTypeDef,
]
AssetBundleResourceLinkSharingConfigurationUnionTypeDef = Union[
    AssetBundleResourceLinkSharingConfigurationTypeDef,
    AssetBundleResourceLinkSharingConfigurationOutputTypeDef,
]


class NumericAxisOptionsTypeDef(TypedDict):
    Scale: NotRequired[AxisScaleTypeDef]
    Range: NotRequired[AxisDisplayRangeUnionTypeDef]


class AxisDataOptionsOutputTypeDef(TypedDict):
    NumericAxisOptions: NotRequired[NumericAxisOptionsOutputTypeDef]
    DateAxisOptions: NotRequired[DateAxisOptionsTypeDef]


class ApplicationThemeTypeDef(TypedDict):
    BrandColorPalette: NotRequired[BrandColorPaletteTypeDef]
    BrandElementStyle: NotRequired[BrandElementStyleTypeDef]


class TopicIRFilterOptionTypeDef(TypedDict):
    FilterType: NotRequired[TopicIRFilterTypeType]
    FilterClass: NotRequired[FilterClassType]
    OperandField: NotRequired[IdentifierTypeDef]
    Function: NotRequired[TopicIRFilterFunctionType]
    Constant: NotRequired[TopicConstantValueUnionTypeDef]
    Inverse: NotRequired[bool]
    NullFilter: NotRequired[NullFilterOptionType]
    Aggregation: NotRequired[AggTypeType]
    AggregationFunctionParameters: NotRequired[Mapping[str, str]]
    AggregationPartitionBy: NotRequired[Sequence[AggregationPartitionByTypeDef]]
    Range: NotRequired[TopicConstantValueUnionTypeDef]
    Inclusive: NotRequired[bool]
    TimeGranularity: NotRequired[TimeGranularityType]
    LastNextOffset: NotRequired[TopicConstantValueUnionTypeDef]
    AggMetrics: NotRequired[Sequence[FilterAggMetricsTypeDef]]
    TopBottomLimit: NotRequired[TopicConstantValueUnionTypeDef]
    SortDirection: NotRequired[TopicSortDirectionType]
    Anchor: NotRequired[AnchorTypeDef]


TopicCategoryFilterConstantUnionTypeDef = Union[
    TopicCategoryFilterConstantTypeDef, TopicCategoryFilterConstantOutputTypeDef
]


class TransformOperationOutputTypeDef(TypedDict):
    ProjectOperation: NotRequired[ProjectOperationOutputTypeDef]
    FilterOperation: NotRequired[FilterOperationTypeDef]
    CreateColumnsOperation: NotRequired[CreateColumnsOperationOutputTypeDef]
    RenameColumnOperation: NotRequired[RenameColumnOperationTypeDef]
    CastColumnTypeOperation: NotRequired[CastColumnTypeOperationTypeDef]
    TagColumnOperation: NotRequired[TagColumnOperationOutputTypeDef]
    UntagColumnOperation: NotRequired[UntagColumnOperationOutputTypeDef]
    OverrideDatasetParameterOperation: NotRequired[OverrideDatasetParameterOperationOutputTypeDef]


TagColumnOperationUnionTypeDef = Union[TagColumnOperationTypeDef, TagColumnOperationOutputTypeDef]


class DataSetConfigurationTypeDef(TypedDict):
    Placeholder: NotRequired[str]
    DataSetSchema: NotRequired[DataSetSchemaUnionTypeDef]
    ColumnGroupSchemaList: NotRequired[Sequence[ColumnGroupSchemaUnionTypeDef]]


class SetParameterValueConfigurationOutputTypeDef(TypedDict):
    DestinationParameterName: str
    Value: DestinationParameterValueConfigurationOutputTypeDef


class VisualPaletteOutputTypeDef(TypedDict):
    ChartColor: NotRequired[str]
    ColorMap: NotRequired[List[DataPathColorTypeDef]]


class VisualPaletteTypeDef(TypedDict):
    ChartColor: NotRequired[str]
    ColorMap: NotRequired[Sequence[DataPathColorTypeDef]]


DataPathSortUnionTypeDef = Union[DataPathSortTypeDef, DataPathSortOutputTypeDef]
PivotTableDataPathOptionUnionTypeDef = Union[
    PivotTableDataPathOptionTypeDef, PivotTableDataPathOptionOutputTypeDef
]


class PivotTableFieldCollapseStateOptionOutputTypeDef(TypedDict):
    Target: PivotTableFieldCollapseStateTargetOutputTypeDef
    State: NotRequired[PivotTableFieldCollapseStateType]


PivotTableFieldCollapseStateTargetUnionTypeDef = Union[
    PivotTableFieldCollapseStateTargetTypeDef, PivotTableFieldCollapseStateTargetOutputTypeDef
]
DecimalDatasetParameterUnionTypeDef = Union[
    DecimalDatasetParameterTypeDef, DecimalDatasetParameterOutputTypeDef
]


class TopicCalculatedFieldOutputTypeDef(TypedDict):
    CalculatedFieldName: str
    Expression: str
    CalculatedFieldDescription: NotRequired[str]
    CalculatedFieldSynonyms: NotRequired[List[str]]
    IsIncludedInTopic: NotRequired[bool]
    DisableIndexing: NotRequired[bool]
    ColumnDataRole: NotRequired[ColumnDataRoleType]
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    DefaultFormatting: NotRequired[DefaultFormattingTypeDef]
    Aggregation: NotRequired[DefaultAggregationType]
    ComparativeOrder: NotRequired[ComparativeOrderOutputTypeDef]
    SemanticType: NotRequired[SemanticTypeOutputTypeDef]
    AllowedAggregations: NotRequired[List[AuthorSpecifiedAggregationType]]
    NotAllowedAggregations: NotRequired[List[AuthorSpecifiedAggregationType]]
    NeverAggregateInFilter: NotRequired[bool]
    CellValueSynonyms: NotRequired[List[CellValueSynonymOutputTypeDef]]
    NonAdditive: NotRequired[bool]


class TopicCalculatedFieldTypeDef(TypedDict):
    CalculatedFieldName: str
    Expression: str
    CalculatedFieldDescription: NotRequired[str]
    CalculatedFieldSynonyms: NotRequired[Sequence[str]]
    IsIncludedInTopic: NotRequired[bool]
    DisableIndexing: NotRequired[bool]
    ColumnDataRole: NotRequired[ColumnDataRoleType]
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    DefaultFormatting: NotRequired[DefaultFormattingTypeDef]
    Aggregation: NotRequired[DefaultAggregationType]
    ComparativeOrder: NotRequired[ComparativeOrderUnionTypeDef]
    SemanticType: NotRequired[SemanticTypeUnionTypeDef]
    AllowedAggregations: NotRequired[Sequence[AuthorSpecifiedAggregationType]]
    NotAllowedAggregations: NotRequired[Sequence[AuthorSpecifiedAggregationType]]
    NeverAggregateInFilter: NotRequired[bool]
    CellValueSynonyms: NotRequired[Sequence[CellValueSynonymTypeDef]]
    NonAdditive: NotRequired[bool]


class TopicColumnOutputTypeDef(TypedDict):
    ColumnName: str
    ColumnFriendlyName: NotRequired[str]
    ColumnDescription: NotRequired[str]
    ColumnSynonyms: NotRequired[List[str]]
    ColumnDataRole: NotRequired[ColumnDataRoleType]
    Aggregation: NotRequired[DefaultAggregationType]
    IsIncludedInTopic: NotRequired[bool]
    DisableIndexing: NotRequired[bool]
    ComparativeOrder: NotRequired[ComparativeOrderOutputTypeDef]
    SemanticType: NotRequired[SemanticTypeOutputTypeDef]
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    AllowedAggregations: NotRequired[List[AuthorSpecifiedAggregationType]]
    NotAllowedAggregations: NotRequired[List[AuthorSpecifiedAggregationType]]
    DefaultFormatting: NotRequired[DefaultFormattingTypeDef]
    NeverAggregateInFilter: NotRequired[bool]
    CellValueSynonyms: NotRequired[List[CellValueSynonymOutputTypeDef]]
    NonAdditive: NotRequired[bool]


class TopicColumnTypeDef(TypedDict):
    ColumnName: str
    ColumnFriendlyName: NotRequired[str]
    ColumnDescription: NotRequired[str]
    ColumnSynonyms: NotRequired[Sequence[str]]
    ColumnDataRole: NotRequired[ColumnDataRoleType]
    Aggregation: NotRequired[DefaultAggregationType]
    IsIncludedInTopic: NotRequired[bool]
    DisableIndexing: NotRequired[bool]
    ComparativeOrder: NotRequired[ComparativeOrderUnionTypeDef]
    SemanticType: NotRequired[SemanticTypeUnionTypeDef]
    TimeGranularity: NotRequired[TopicTimeGranularityType]
    AllowedAggregations: NotRequired[Sequence[AuthorSpecifiedAggregationType]]
    NotAllowedAggregations: NotRequired[Sequence[AuthorSpecifiedAggregationType]]
    DefaultFormatting: NotRequired[DefaultFormattingTypeDef]
    NeverAggregateInFilter: NotRequired[bool]
    CellValueSynonyms: NotRequired[Sequence[CellValueSynonymUnionTypeDef]]
    NonAdditive: NotRequired[bool]


TopicIRMetricUnionTypeDef = Union[TopicIRMetricTypeDef, TopicIRMetricOutputTypeDef]


class ContributionAnalysisTimeRangesOutputTypeDef(TypedDict):
    StartRange: NotRequired[TopicIRFilterOptionOutputTypeDef]
    EndRange: NotRequired[TopicIRFilterOptionOutputTypeDef]


CategoryFilterConfigurationUnionTypeDef = Union[
    CategoryFilterConfigurationTypeDef, CategoryFilterConfigurationOutputTypeDef
]


class ChartAxisLabelOptionsOutputTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    SortIconVisibility: NotRequired[VisibilityType]
    AxisLabelOptions: NotRequired[List[AxisLabelOptionsTypeDef]]


class ChartAxisLabelOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    SortIconVisibility: NotRequired[VisibilityType]
    AxisLabelOptions: NotRequired[Sequence[AxisLabelOptionsTypeDef]]


DataLabelOptionsUnionTypeDef = Union[DataLabelOptionsTypeDef, DataLabelOptionsOutputTypeDef]


class AxisTickLabelOptionsTypeDef(TypedDict):
    LabelOptions: NotRequired[LabelOptionsTypeDef]
    RotationAngle: NotRequired[float]


class DateTimePickerControlDisplayOptionsTypeDef(TypedDict):
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    DateTimeFormat: NotRequired[str]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]
    HelperTextVisibility: NotRequired[VisibilityType]
    DateIconVisibility: NotRequired[VisibilityType]


class DropDownControlDisplayOptionsTypeDef(TypedDict):
    SelectAllOptions: NotRequired[ListControlSelectAllOptionsTypeDef]
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class LegendOptionsTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    Title: NotRequired[LabelOptionsTypeDef]
    Position: NotRequired[LegendPositionType]
    Width: NotRequired[str]
    Height: NotRequired[str]
    ValueFontConfiguration: NotRequired[FontConfigurationTypeDef]


class ListControlDisplayOptionsTypeDef(TypedDict):
    SearchOptions: NotRequired[ListControlSearchOptionsTypeDef]
    SelectAllOptions: NotRequired[ListControlSelectAllOptionsTypeDef]
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class RelativeDateTimeControlDisplayOptionsTypeDef(TypedDict):
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    DateTimeFormat: NotRequired[str]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class SliderControlDisplayOptionsTypeDef(TypedDict):
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class TextAreaControlDisplayOptionsTypeDef(TypedDict):
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    PlaceholderOptions: NotRequired[TextControlPlaceholderOptionsTypeDef]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class TextFieldControlDisplayOptionsTypeDef(TypedDict):
    TitleOptions: NotRequired[LabelOptionsTypeDef]
    PlaceholderOptions: NotRequired[TextControlPlaceholderOptionsTypeDef]
    InfoIconLabelOptions: NotRequired[SheetControlInfoIconLabelOptionsTypeDef]


class PanelConfigurationTypeDef(TypedDict):
    Title: NotRequired[PanelTitleOptionsTypeDef]
    BorderVisibility: NotRequired[VisibilityType]
    BorderThickness: NotRequired[str]
    BorderStyle: NotRequired[PanelBorderStyleType]
    BorderColor: NotRequired[str]
    GutterVisibility: NotRequired[VisibilityType]
    GutterSpacing: NotRequired[str]
    BackgroundVisibility: NotRequired[VisibilityType]
    BackgroundColor: NotRequired[str]


class TableFieldLinkContentConfigurationTypeDef(TypedDict):
    CustomTextContent: NotRequired[TableFieldCustomTextContentTypeDef]
    CustomIconContent: NotRequired[TableFieldCustomIconContentTypeDef]


ColumnGroupUnionTypeDef = Union[ColumnGroupTypeDef, ColumnGroupOutputTypeDef]


class GeospatialPointStyleOptionsOutputTypeDef(TypedDict):
    SelectedPointStyle: NotRequired[GeospatialSelectedPointStyleType]
    ClusterMarkerConfiguration: NotRequired[ClusterMarkerConfigurationTypeDef]
    HeatmapConfiguration: NotRequired[GeospatialHeatmapConfigurationOutputTypeDef]


class GeospatialHeatmapConfigurationTypeDef(TypedDict):
    HeatmapColor: NotRequired[GeospatialHeatmapColorScaleUnionTypeDef]


GeospatialCategoricalColorUnionTypeDef = Union[
    GeospatialCategoricalColorTypeDef, GeospatialCategoricalColorOutputTypeDef
]


class GeospatialColorOutputTypeDef(TypedDict):
    Solid: NotRequired[GeospatialSolidColorTypeDef]
    Gradient: NotRequired[GeospatialGradientColorOutputTypeDef]
    Categorical: NotRequired[GeospatialCategoricalColorOutputTypeDef]


GeospatialGradientColorUnionTypeDef = Union[
    GeospatialGradientColorTypeDef, GeospatialGradientColorOutputTypeDef
]


class TableCellStyleTypeDef(TypedDict):
    Visibility: NotRequired[VisibilityType]
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    TextWrap: NotRequired[TextWrapType]
    HorizontalTextAlignment: NotRequired[HorizontalTextAlignmentType]
    VerticalTextAlignment: NotRequired[VerticalTextAlignmentType]
    BackgroundColor: NotRequired[str]
    Height: NotRequired[int]
    Border: NotRequired[GlobalTableBorderOptionsTypeDef]


class ConditionalFormattingColorOutputTypeDef(TypedDict):
    Solid: NotRequired[ConditionalFormattingSolidColorTypeDef]
    Gradient: NotRequired[ConditionalFormattingGradientColorOutputTypeDef]


class ConditionalFormattingGradientColorTypeDef(TypedDict):
    Expression: str
    Color: GradientColorUnionTypeDef


class DefaultInteractiveLayoutConfigurationTypeDef(TypedDict):
    Grid: NotRequired[DefaultGridLayoutConfigurationTypeDef]
    FreeForm: NotRequired[DefaultFreeFormLayoutConfigurationTypeDef]


class SheetControlLayoutConfigurationOutputTypeDef(TypedDict):
    GridLayout: NotRequired[GridLayoutConfigurationOutputTypeDef]


GridLayoutConfigurationUnionTypeDef = Union[
    GridLayoutConfigurationTypeDef, GridLayoutConfigurationOutputTypeDef
]


class LogoSetConfigurationTypeDef(TypedDict):
    Primary: ImageSetConfigurationTypeDef
    Favicon: NotRequired[ImageSetConfigurationTypeDef]


class LogoSetTypeDef(TypedDict):
    Primary: ImageSetTypeDef
    Favicon: NotRequired[ImageSetTypeDef]


class DataSetRefreshPropertiesTypeDef(TypedDict):
    RefreshConfiguration: RefreshConfigurationTypeDef


IntegerDatasetParameterUnionTypeDef = Union[
    IntegerDatasetParameterTypeDef, IntegerDatasetParameterOutputTypeDef
]


class SeriesItemTypeDef(TypedDict):
    FieldSeriesItem: NotRequired[FieldSeriesItemTypeDef]
    DataFieldSeriesItem: NotRequired[DataFieldSeriesItemTypeDef]


class ThemeConfigurationOutputTypeDef(TypedDict):
    DataColorPalette: NotRequired[DataColorPaletteOutputTypeDef]
    UIColorPalette: NotRequired[UIColorPaletteTypeDef]
    Sheet: NotRequired[SheetStyleTypeDef]
    Typography: NotRequired[TypographyOutputTypeDef]


class ThemeConfigurationTypeDef(TypedDict):
    DataColorPalette: NotRequired[DataColorPaletteUnionTypeDef]
    UIColorPalette: NotRequired[UIColorPaletteTypeDef]
    Sheet: NotRequired[SheetStyleTypeDef]
    Typography: NotRequired[TypographyUnionTypeDef]


NamedEntityDefinitionUnionTypeDef = Union[
    NamedEntityDefinitionTypeDef, NamedEntityDefinitionOutputTypeDef
]


class ComparisonFormatConfigurationTypeDef(TypedDict):
    NumberDisplayFormatConfiguration: NotRequired[NumberDisplayFormatConfigurationTypeDef]
    PercentageDisplayFormatConfiguration: NotRequired[PercentageDisplayFormatConfigurationTypeDef]


class NumericFormatConfigurationTypeDef(TypedDict):
    NumberDisplayFormatConfiguration: NotRequired[NumberDisplayFormatConfigurationTypeDef]
    CurrencyDisplayFormatConfiguration: NotRequired[CurrencyDisplayFormatConfigurationTypeDef]
    PercentageDisplayFormatConfiguration: NotRequired[PercentageDisplayFormatConfigurationTypeDef]


class AggregationSortConfigurationTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    SortDirection: SortDirectionType
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]


class ColumnSortTypeDef(TypedDict):
    SortBy: ColumnIdentifierTypeDef
    Direction: SortDirectionType
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]


class ColumnTooltipItemTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Label: NotRequired[str]
    Visibility: NotRequired[VisibilityType]
    Aggregation: NotRequired[AggregationFunctionTypeDef]
    TooltipTarget: NotRequired[TooltipTargetType]


class ReferenceLineDynamicDataConfigurationTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Calculation: NumericalAggregationFunctionTypeDef
    MeasureAggregationFunction: NotRequired[AggregationFunctionTypeDef]


class TopicFilterOutputTypeDef(TypedDict):
    FilterName: str
    OperandFieldName: str
    FilterDescription: NotRequired[str]
    FilterClass: NotRequired[FilterClassType]
    FilterSynonyms: NotRequired[List[str]]
    FilterType: NotRequired[NamedFilterTypeType]
    CategoryFilter: NotRequired[TopicCategoryFilterOutputTypeDef]
    NumericEqualityFilter: NotRequired[TopicNumericEqualityFilterTypeDef]
    NumericRangeFilter: NotRequired[TopicNumericRangeFilterTypeDef]
    DateRangeFilter: NotRequired[TopicDateRangeFilterTypeDef]
    RelativeDateFilter: NotRequired[TopicRelativeDateFilterTypeDef]


RedshiftParametersUnionTypeDef = Union[RedshiftParametersTypeDef, RedshiftParametersOutputTypeDef]


class DescribeRefreshScheduleResponseTypeDef(TypedDict):
    RefreshSchedule: RefreshScheduleOutputTypeDef
    Status: int
    RequestId: str
    Arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListRefreshSchedulesResponseTypeDef(TypedDict):
    RefreshSchedules: List[RefreshScheduleOutputTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRefreshScheduleRequestRequestTypeDef(TypedDict):
    DataSetId: str
    AwsAccountId: str
    Schedule: RefreshScheduleTypeDef


class UpdateRefreshScheduleRequestRequestTypeDef(TypedDict):
    DataSetId: str
    AwsAccountId: str
    Schedule: RefreshScheduleTypeDef


class RegisteredUserEmbeddingExperienceConfigurationTypeDef(TypedDict):
    Dashboard: NotRequired[RegisteredUserDashboardEmbeddingConfigurationTypeDef]
    QuickSightConsole: NotRequired[RegisteredUserQuickSightConsoleEmbeddingConfigurationTypeDef]
    QSearchBar: NotRequired[RegisteredUserQSearchBarEmbeddingConfigurationTypeDef]
    DashboardVisual: NotRequired[RegisteredUserDashboardVisualEmbeddingConfigurationTypeDef]
    GenerativeQnA: NotRequired[RegisteredUserGenerativeQnAEmbeddingConfigurationTypeDef]


SnapshotDestinationConfigurationUnionTypeDef = Union[
    SnapshotDestinationConfigurationTypeDef, SnapshotDestinationConfigurationOutputTypeDef
]


class SnapshotJobResultFileGroupTypeDef(TypedDict):
    Files: NotRequired[List[SnapshotFileOutputTypeDef]]
    S3Results: NotRequired[List[SnapshotJobS3ResultTypeDef]]


class PhysicalTableTypeDef(TypedDict):
    RelationalTable: NotRequired[RelationalTableUnionTypeDef]
    CustomSql: NotRequired[CustomSqlUnionTypeDef]
    S3Source: NotRequired[S3SourceUnionTypeDef]


FilterOperationTargetVisualsConfigurationUnionTypeDef = Union[
    FilterOperationTargetVisualsConfigurationTypeDef,
    FilterOperationTargetVisualsConfigurationOutputTypeDef,
]


class DefaultSectionBasedLayoutConfigurationTypeDef(TypedDict):
    CanvasSizeOptions: SectionBasedLayoutCanvasSizeOptionsTypeDef


class FreeFormLayoutConfigurationOutputTypeDef(TypedDict):
    Elements: List[FreeFormLayoutElementOutputTypeDef]
    CanvasSizeOptions: NotRequired[FreeFormLayoutCanvasSizeOptionsTypeDef]


class FreeFormSectionLayoutConfigurationOutputTypeDef(TypedDict):
    Elements: List[FreeFormLayoutElementOutputTypeDef]


FreeFormLayoutElementUnionTypeDef = Union[
    FreeFormLayoutElementTypeDef, FreeFormLayoutElementOutputTypeDef
]
SelectedSheetsFilterScopeConfigurationUnionTypeDef = Union[
    SelectedSheetsFilterScopeConfigurationTypeDef,
    SelectedSheetsFilterScopeConfigurationOutputTypeDef,
]


class SnapshotConfigurationOutputTypeDef(TypedDict):
    FileGroups: List[SnapshotFileGroupOutputTypeDef]
    DestinationConfiguration: NotRequired[SnapshotDestinationConfigurationOutputTypeDef]
    Parameters: NotRequired[ParametersOutputTypeDef]


SnapshotFileUnionTypeDef = Union[SnapshotFileTypeDef, SnapshotFileOutputTypeDef]


class StaticFileTypeDef(TypedDict):
    ImageStaticFile: NotRequired[ImageStaticFileTypeDef]
    SpatialStaticFile: NotRequired[SpatialStaticFileTypeDef]


StringDatasetParameterUnionTypeDef = Union[
    StringDatasetParameterTypeDef, StringDatasetParameterOutputTypeDef
]


class FilterCrossSheetControlTypeDef(TypedDict):
    FilterControlId: str
    SourceFilterId: str
    CascadingControlConfiguration: NotRequired[CascadingControlConfigurationUnionTypeDef]


class DateTimeParameterDeclarationTypeDef(TypedDict):
    Name: str
    DefaultValues: NotRequired[DateTimeDefaultValuesUnionTypeDef]
    TimeGranularity: NotRequired[TimeGranularityType]
    ValueWhenUnset: NotRequired[DateTimeValueWhenUnsetConfigurationUnionTypeDef]
    MappedDataSetParameters: NotRequired[Sequence[MappedDataSetParameterTypeDef]]


class DecimalParameterDeclarationTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[DecimalDefaultValuesUnionTypeDef]
    ValueWhenUnset: NotRequired[DecimalValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[Sequence[MappedDataSetParameterTypeDef]]


class IntegerParameterDeclarationTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[IntegerDefaultValuesUnionTypeDef]
    ValueWhenUnset: NotRequired[IntegerValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[Sequence[MappedDataSetParameterTypeDef]]


class ParameterDeclarationOutputTypeDef(TypedDict):
    StringParameterDeclaration: NotRequired[StringParameterDeclarationOutputTypeDef]
    DecimalParameterDeclaration: NotRequired[DecimalParameterDeclarationOutputTypeDef]
    IntegerParameterDeclaration: NotRequired[IntegerParameterDeclarationOutputTypeDef]
    DateTimeParameterDeclaration: NotRequired[DateTimeParameterDeclarationOutputTypeDef]


class StringParameterDeclarationTypeDef(TypedDict):
    ParameterValueType: ParameterValueTypeType
    Name: str
    DefaultValues: NotRequired[StringDefaultValuesUnionTypeDef]
    ValueWhenUnset: NotRequired[StringValueWhenUnsetConfigurationTypeDef]
    MappedDataSetParameters: NotRequired[Sequence[MappedDataSetParameterTypeDef]]


class ColumnHierarchyOutputTypeDef(TypedDict):
    ExplicitHierarchy: NotRequired[ExplicitHierarchyOutputTypeDef]
    DateTimeHierarchy: NotRequired[DateTimeHierarchyOutputTypeDef]
    PredefinedHierarchy: NotRequired[PredefinedHierarchyOutputTypeDef]


class GenerateEmbedUrlForAnonymousUserRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    Namespace: str
    AuthorizedResourceArns: Sequence[str]
    ExperienceConfiguration: AnonymousUserEmbeddingExperienceConfigurationTypeDef
    SessionLifetimeInMinutes: NotRequired[int]
    SessionTags: NotRequired[Sequence[SessionTagTypeDef]]
    AllowedDomains: NotRequired[Sequence[str]]


class AssetBundleImportJobDataSourceOverrideParametersOutputTypeDef(TypedDict):
    DataSourceId: str
    Name: NotRequired[str]
    DataSourceParameters: NotRequired[DataSourceParametersOutputTypeDef]
    VpcConnectionProperties: NotRequired[VpcConnectionPropertiesTypeDef]
    SslProperties: NotRequired[SslPropertiesTypeDef]
    Credentials: NotRequired[AssetBundleImportJobDataSourceCredentialsTypeDef]


DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "Arn": NotRequired[str],
        "DataSourceId": NotRequired[str],
        "Name": NotRequired[str],
        "Type": NotRequired[DataSourceTypeType],
        "Status": NotRequired[ResourceStatusType],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "DataSourceParameters": NotRequired[DataSourceParametersOutputTypeDef],
        "AlternateDataSourceParameters": NotRequired[List[DataSourceParametersOutputTypeDef]],
        "VpcConnectionProperties": NotRequired[VpcConnectionPropertiesTypeDef],
        "SslProperties": NotRequired[SslPropertiesTypeDef],
        "ErrorInfo": NotRequired[DataSourceErrorInfoTypeDef],
        "SecretArn": NotRequired[str],
    },
)
CustomValuesConfigurationUnionTypeDef = Union[
    CustomValuesConfigurationTypeDef, CustomValuesConfigurationOutputTypeDef
]
DateTimeDatasetParameterUnionTypeDef = Union[
    DateTimeDatasetParameterTypeDef, DateTimeDatasetParameterOutputTypeDef
]
ParametersUnionTypeDef = Union[ParametersTypeDef, ParametersOutputTypeDef]
OverrideDatasetParameterOperationUnionTypeDef = Union[
    OverrideDatasetParameterOperationTypeDef, OverrideDatasetParameterOperationOutputTypeDef
]
DrillDownFilterUnionTypeDef = Union[DrillDownFilterTypeDef, DrillDownFilterOutputTypeDef]
ForecastScenarioUnionTypeDef = Union[ForecastScenarioTypeDef, ForecastScenarioOutputTypeDef]


class AssetBundleImportJobDashboardOverridePermissionsTypeDef(TypedDict):
    DashboardIds: Sequence[str]
    Permissions: NotRequired[AssetBundleResourcePermissionsUnionTypeDef]
    LinkSharingConfiguration: NotRequired[AssetBundleResourceLinkSharingConfigurationUnionTypeDef]


NumericAxisOptionsUnionTypeDef = Union[NumericAxisOptionsTypeDef, NumericAxisOptionsOutputTypeDef]
TopicIRFilterOptionUnionTypeDef = Union[
    TopicIRFilterOptionTypeDef, TopicIRFilterOptionOutputTypeDef
]


class TopicCategoryFilterTypeDef(TypedDict):
    CategoryFilterFunction: NotRequired[CategoryFilterFunctionType]
    CategoryFilterType: NotRequired[CategoryFilterTypeType]
    Constant: NotRequired[TopicCategoryFilterConstantUnionTypeDef]
    Inverse: NotRequired[bool]


class LogicalTableOutputTypeDef(TypedDict):
    Alias: str
    Source: LogicalTableSourceTypeDef
    DataTransforms: NotRequired[List[TransformOperationOutputTypeDef]]


DataSetConfigurationUnionTypeDef = Union[
    DataSetConfigurationTypeDef, DataSetConfigurationOutputTypeDef
]


class CustomActionSetParametersOperationOutputTypeDef(TypedDict):
    ParameterValueConfigurations: List[SetParameterValueConfigurationOutputTypeDef]


VisualPaletteUnionTypeDef = Union[VisualPaletteTypeDef, VisualPaletteOutputTypeDef]


class PivotTableFieldOptionsOutputTypeDef(TypedDict):
    SelectedFieldOptions: NotRequired[List[PivotTableFieldOptionTypeDef]]
    DataPathOptions: NotRequired[List[PivotTableDataPathOptionOutputTypeDef]]
    CollapseStateOptions: NotRequired[List[PivotTableFieldCollapseStateOptionOutputTypeDef]]


class PivotTableFieldCollapseStateOptionTypeDef(TypedDict):
    Target: PivotTableFieldCollapseStateTargetUnionTypeDef
    State: NotRequired[PivotTableFieldCollapseStateType]


TopicCalculatedFieldUnionTypeDef = Union[
    TopicCalculatedFieldTypeDef, TopicCalculatedFieldOutputTypeDef
]
TopicColumnUnionTypeDef = Union[TopicColumnTypeDef, TopicColumnOutputTypeDef]


class TopicIRContributionAnalysisOutputTypeDef(TypedDict):
    Factors: NotRequired[List[ContributionAnalysisFactorTypeDef]]
    TimeRanges: NotRequired[ContributionAnalysisTimeRangesOutputTypeDef]
    Direction: NotRequired[ContributionAnalysisDirectionType]
    SortType: NotRequired[ContributionAnalysisSortTypeType]


ChartAxisLabelOptionsUnionTypeDef = Union[
    ChartAxisLabelOptionsTypeDef, ChartAxisLabelOptionsOutputTypeDef
]


class AxisDisplayOptionsOutputTypeDef(TypedDict):
    TickLabelOptions: NotRequired[AxisTickLabelOptionsTypeDef]
    AxisLineVisibility: NotRequired[VisibilityType]
    GridLineVisibility: NotRequired[VisibilityType]
    DataOptions: NotRequired[AxisDataOptionsOutputTypeDef]
    ScrollbarOptions: NotRequired[ScrollBarOptionsTypeDef]
    AxisOffset: NotRequired[str]


DefaultDateTimePickerControlOptionsTypeDef = TypedDict(
    "DefaultDateTimePickerControlOptionsTypeDef",
    {
        "Type": NotRequired[SheetControlDateTimePickerTypeType],
        "DisplayOptions": NotRequired[DateTimePickerControlDisplayOptionsTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
FilterDateTimePickerControlTypeDef = TypedDict(
    "FilterDateTimePickerControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[DateTimePickerControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlDateTimePickerTypeType],
        "CommitMode": NotRequired[CommitModeType],
    },
)


class ParameterDateTimePickerControlTypeDef(TypedDict):
    ParameterControlId: str
    Title: str
    SourceParameterName: str
    DisplayOptions: NotRequired[DateTimePickerControlDisplayOptionsTypeDef]


DefaultFilterDropDownControlOptionsOutputTypeDef = TypedDict(
    "DefaultFilterDropDownControlOptionsOutputTypeDef",
    {
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesOutputTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
DefaultFilterDropDownControlOptionsTypeDef = TypedDict(
    "DefaultFilterDropDownControlOptionsTypeDef",
    {
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesUnionTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
FilterDropDownControlOutputTypeDef = TypedDict(
    "FilterDropDownControlOutputTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesOutputTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationOutputTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
FilterDropDownControlTypeDef = TypedDict(
    "FilterDropDownControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesUnionTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationUnionTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
ParameterDropDownControlOutputTypeDef = TypedDict(
    "ParameterDropDownControlOutputTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[ParameterSelectableValuesOutputTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationOutputTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
ParameterDropDownControlTypeDef = TypedDict(
    "ParameterDropDownControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[DropDownControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[ParameterSelectableValuesUnionTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationUnionTypeDef],
        "CommitMode": NotRequired[CommitModeType],
    },
)
DefaultFilterListControlOptionsOutputTypeDef = TypedDict(
    "DefaultFilterListControlOptionsOutputTypeDef",
    {
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesOutputTypeDef],
    },
)
DefaultFilterListControlOptionsTypeDef = TypedDict(
    "DefaultFilterListControlOptionsTypeDef",
    {
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesUnionTypeDef],
    },
)
FilterListControlOutputTypeDef = TypedDict(
    "FilterListControlOutputTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesOutputTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationOutputTypeDef],
    },
)
FilterListControlTypeDef = TypedDict(
    "FilterListControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[FilterSelectableValuesUnionTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationUnionTypeDef],
    },
)
ParameterListControlOutputTypeDef = TypedDict(
    "ParameterListControlOutputTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[ParameterSelectableValuesOutputTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationOutputTypeDef],
    },
)
ParameterListControlTypeDef = TypedDict(
    "ParameterListControlTypeDef",
    {
        "ParameterControlId": str,
        "Title": str,
        "SourceParameterName": str,
        "DisplayOptions": NotRequired[ListControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlListTypeType],
        "SelectableValues": NotRequired[ParameterSelectableValuesUnionTypeDef],
        "CascadingControlConfiguration": NotRequired[CascadingControlConfigurationUnionTypeDef],
    },
)


class DefaultRelativeDateTimeControlOptionsTypeDef(TypedDict):
    DisplayOptions: NotRequired[RelativeDateTimeControlDisplayOptionsTypeDef]
    CommitMode: NotRequired[CommitModeType]


class FilterRelativeDateTimeControlTypeDef(TypedDict):
    FilterControlId: str
    Title: str
    SourceFilterId: str
    DisplayOptions: NotRequired[RelativeDateTimeControlDisplayOptionsTypeDef]
    CommitMode: NotRequired[CommitModeType]


DefaultSliderControlOptionsTypeDef = TypedDict(
    "DefaultSliderControlOptionsTypeDef",
    {
        "MaximumValue": float,
        "MinimumValue": float,
        "StepSize": float,
        "DisplayOptions": NotRequired[SliderControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlSliderTypeType],
    },
)
FilterSliderControlTypeDef = TypedDict(
    "FilterSliderControlTypeDef",
    {
        "FilterControlId": str,
        "Title": str,
        "SourceFilterId": str,
        "MaximumValue": float,
        "MinimumValue": float,
        "StepSize": float,
        "DisplayOptions": NotRequired[SliderControlDisplayOptionsTypeDef],
        "Type": NotRequired[SheetControlSliderTypeType],
    },
)


class ParameterSliderControlTypeDef(TypedDict):
    ParameterControlId: str
    Title: str
    SourceParameterName: str
    MaximumValue: float
    MinimumValue: float
    StepSize: float
    DisplayOptions: NotRequired[SliderControlDisplayOptionsTypeDef]


class DefaultTextAreaControlOptionsTypeDef(TypedDict):
    Delimiter: NotRequired[str]
    DisplayOptions: NotRequired[TextAreaControlDisplayOptionsTypeDef]


class FilterTextAreaControlTypeDef(TypedDict):
    FilterControlId: str
    Title: str
    SourceFilterId: str
    Delimiter: NotRequired[str]
    DisplayOptions: NotRequired[TextAreaControlDisplayOptionsTypeDef]


class ParameterTextAreaControlTypeDef(TypedDict):
    ParameterControlId: str
    Title: str
    SourceParameterName: str
    Delimiter: NotRequired[str]
    DisplayOptions: NotRequired[TextAreaControlDisplayOptionsTypeDef]


class DefaultTextFieldControlOptionsTypeDef(TypedDict):
    DisplayOptions: NotRequired[TextFieldControlDisplayOptionsTypeDef]


class FilterTextFieldControlTypeDef(TypedDict):
    FilterControlId: str
    Title: str
    SourceFilterId: str
    DisplayOptions: NotRequired[TextFieldControlDisplayOptionsTypeDef]


class ParameterTextFieldControlTypeDef(TypedDict):
    ParameterControlId: str
    Title: str
    SourceParameterName: str
    DisplayOptions: NotRequired[TextFieldControlDisplayOptionsTypeDef]


class SmallMultiplesOptionsTypeDef(TypedDict):
    MaxVisibleRows: NotRequired[int]
    MaxVisibleColumns: NotRequired[int]
    PanelConfiguration: NotRequired[PanelConfigurationTypeDef]
    XAxis: NotRequired[SmallMultiplesAxisPropertiesTypeDef]
    YAxis: NotRequired[SmallMultiplesAxisPropertiesTypeDef]


class TableFieldLinkConfigurationTypeDef(TypedDict):
    Target: URLTargetConfigurationType
    Content: TableFieldLinkContentConfigurationTypeDef


GeospatialHeatmapConfigurationUnionTypeDef = Union[
    GeospatialHeatmapConfigurationTypeDef, GeospatialHeatmapConfigurationOutputTypeDef
]


class GeospatialCircleSymbolStyleOutputTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorOutputTypeDef]
    StrokeColor: NotRequired[GeospatialColorOutputTypeDef]
    StrokeWidth: NotRequired[GeospatialLineWidthTypeDef]
    CircleRadius: NotRequired[GeospatialCircleRadiusTypeDef]


class GeospatialLineSymbolStyleOutputTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorOutputTypeDef]
    LineWidth: NotRequired[GeospatialLineWidthTypeDef]


class GeospatialPolygonSymbolStyleOutputTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorOutputTypeDef]
    StrokeColor: NotRequired[GeospatialColorOutputTypeDef]
    StrokeWidth: NotRequired[GeospatialLineWidthTypeDef]


class GeospatialColorTypeDef(TypedDict):
    Solid: NotRequired[GeospatialSolidColorTypeDef]
    Gradient: NotRequired[GeospatialGradientColorUnionTypeDef]
    Categorical: NotRequired[GeospatialCategoricalColorUnionTypeDef]


class PivotTableOptionsOutputTypeDef(TypedDict):
    MetricPlacement: NotRequired[PivotTableMetricPlacementType]
    SingleMetricVisibility: NotRequired[VisibilityType]
    ColumnNamesVisibility: NotRequired[VisibilityType]
    ToggleButtonsVisibility: NotRequired[VisibilityType]
    ColumnHeaderStyle: NotRequired[TableCellStyleTypeDef]
    RowHeaderStyle: NotRequired[TableCellStyleTypeDef]
    CellStyle: NotRequired[TableCellStyleTypeDef]
    RowFieldNamesStyle: NotRequired[TableCellStyleTypeDef]
    RowAlternateColorOptions: NotRequired[RowAlternateColorOptionsOutputTypeDef]
    CollapsedRowDimensionsVisibility: NotRequired[VisibilityType]
    RowsLayout: NotRequired[PivotTableRowsLayoutType]
    RowsLabelOptions: NotRequired[PivotTableRowsLabelOptionsTypeDef]
    DefaultCellWidth: NotRequired[str]


class PivotTableOptionsTypeDef(TypedDict):
    MetricPlacement: NotRequired[PivotTableMetricPlacementType]
    SingleMetricVisibility: NotRequired[VisibilityType]
    ColumnNamesVisibility: NotRequired[VisibilityType]
    ToggleButtonsVisibility: NotRequired[VisibilityType]
    ColumnHeaderStyle: NotRequired[TableCellStyleTypeDef]
    RowHeaderStyle: NotRequired[TableCellStyleTypeDef]
    CellStyle: NotRequired[TableCellStyleTypeDef]
    RowFieldNamesStyle: NotRequired[TableCellStyleTypeDef]
    RowAlternateColorOptions: NotRequired[RowAlternateColorOptionsUnionTypeDef]
    CollapsedRowDimensionsVisibility: NotRequired[VisibilityType]
    RowsLayout: NotRequired[PivotTableRowsLayoutType]
    RowsLabelOptions: NotRequired[PivotTableRowsLabelOptionsTypeDef]
    DefaultCellWidth: NotRequired[str]


class PivotTotalOptionsOutputTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    Placement: NotRequired[TableTotalsPlacementType]
    ScrollStatus: NotRequired[TableTotalsScrollStatusType]
    CustomLabel: NotRequired[str]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    ValueCellStyle: NotRequired[TableCellStyleTypeDef]
    MetricHeaderCellStyle: NotRequired[TableCellStyleTypeDef]
    TotalAggregationOptions: NotRequired[List[TotalAggregationOptionTypeDef]]


class PivotTotalOptionsTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    Placement: NotRequired[TableTotalsPlacementType]
    ScrollStatus: NotRequired[TableTotalsScrollStatusType]
    CustomLabel: NotRequired[str]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    ValueCellStyle: NotRequired[TableCellStyleTypeDef]
    MetricHeaderCellStyle: NotRequired[TableCellStyleTypeDef]
    TotalAggregationOptions: NotRequired[Sequence[TotalAggregationOptionTypeDef]]


class SubtotalOptionsOutputTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    CustomLabel: NotRequired[str]
    FieldLevel: NotRequired[PivotTableSubtotalLevelType]
    FieldLevelOptions: NotRequired[List[PivotTableFieldSubtotalOptionsTypeDef]]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    ValueCellStyle: NotRequired[TableCellStyleTypeDef]
    MetricHeaderCellStyle: NotRequired[TableCellStyleTypeDef]
    StyleTargets: NotRequired[List[TableStyleTargetTypeDef]]


class SubtotalOptionsTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    CustomLabel: NotRequired[str]
    FieldLevel: NotRequired[PivotTableSubtotalLevelType]
    FieldLevelOptions: NotRequired[Sequence[PivotTableFieldSubtotalOptionsTypeDef]]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    ValueCellStyle: NotRequired[TableCellStyleTypeDef]
    MetricHeaderCellStyle: NotRequired[TableCellStyleTypeDef]
    StyleTargets: NotRequired[Sequence[TableStyleTargetTypeDef]]


class TableOptionsOutputTypeDef(TypedDict):
    Orientation: NotRequired[TableOrientationType]
    HeaderStyle: NotRequired[TableCellStyleTypeDef]
    CellStyle: NotRequired[TableCellStyleTypeDef]
    RowAlternateColorOptions: NotRequired[RowAlternateColorOptionsOutputTypeDef]


class TableOptionsTypeDef(TypedDict):
    Orientation: NotRequired[TableOrientationType]
    HeaderStyle: NotRequired[TableCellStyleTypeDef]
    CellStyle: NotRequired[TableCellStyleTypeDef]
    RowAlternateColorOptions: NotRequired[RowAlternateColorOptionsUnionTypeDef]


class TotalOptionsOutputTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    Placement: NotRequired[TableTotalsPlacementType]
    ScrollStatus: NotRequired[TableTotalsScrollStatusType]
    CustomLabel: NotRequired[str]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    TotalAggregationOptions: NotRequired[List[TotalAggregationOptionTypeDef]]


class TotalOptionsTypeDef(TypedDict):
    TotalsVisibility: NotRequired[VisibilityType]
    Placement: NotRequired[TableTotalsPlacementType]
    ScrollStatus: NotRequired[TableTotalsScrollStatusType]
    CustomLabel: NotRequired[str]
    TotalCellStyle: NotRequired[TableCellStyleTypeDef]
    TotalAggregationOptions: NotRequired[Sequence[TotalAggregationOptionTypeDef]]


class GaugeChartArcConditionalFormattingOutputTypeDef(TypedDict):
    ForegroundColor: NotRequired[ConditionalFormattingColorOutputTypeDef]


class GaugeChartPrimaryValueConditionalFormattingOutputTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIActualValueConditionalFormattingOutputTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIComparisonValueConditionalFormattingOutputTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIPrimaryValueConditionalFormattingOutputTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIProgressBarConditionalFormattingOutputTypeDef(TypedDict):
    ForegroundColor: NotRequired[ConditionalFormattingColorOutputTypeDef]


class ShapeConditionalFormatOutputTypeDef(TypedDict):
    BackgroundColor: ConditionalFormattingColorOutputTypeDef


class TableRowConditionalFormattingOutputTypeDef(TypedDict):
    BackgroundColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]


class TextConditionalFormatOutputTypeDef(TypedDict):
    BackgroundColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    TextColor: NotRequired[ConditionalFormattingColorOutputTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


ConditionalFormattingGradientColorUnionTypeDef = Union[
    ConditionalFormattingGradientColorTypeDef, ConditionalFormattingGradientColorOutputTypeDef
]


class SheetControlLayoutOutputTypeDef(TypedDict):
    Configuration: SheetControlLayoutConfigurationOutputTypeDef


class SheetControlLayoutConfigurationTypeDef(TypedDict):
    GridLayout: NotRequired[GridLayoutConfigurationUnionTypeDef]


class LogoConfigurationTypeDef(TypedDict):
    AltText: str
    LogoSet: LogoSetConfigurationTypeDef


class LogoTypeDef(TypedDict):
    AltText: str
    LogoSet: LogoSetTypeDef


class DescribeDataSetRefreshPropertiesResponseTypeDef(TypedDict):
    RequestId: str
    Status: int
    DataSetRefreshProperties: DataSetRefreshPropertiesTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PutDataSetRefreshPropertiesRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    DataSetRefreshProperties: DataSetRefreshPropertiesTypeDef


class ThemeVersionTypeDef(TypedDict):
    VersionNumber: NotRequired[int]
    Arn: NotRequired[str]
    Description: NotRequired[str]
    BaseThemeId: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    Configuration: NotRequired[ThemeConfigurationOutputTypeDef]
    Errors: NotRequired[List[ThemeErrorTypeDef]]
    Status: NotRequired[ResourceStatusType]


class CreateThemeRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    Name: str
    BaseThemeId: str
    Configuration: ThemeConfigurationTypeDef
    VersionDescription: NotRequired[str]
    Permissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateThemeRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ThemeId: str
    BaseThemeId: str
    Name: NotRequired[str]
    VersionDescription: NotRequired[str]
    Configuration: NotRequired[ThemeConfigurationTypeDef]


class TopicNamedEntityTypeDef(TypedDict):
    EntityName: str
    EntityDescription: NotRequired[str]
    EntitySynonyms: NotRequired[Sequence[str]]
    SemanticEntityType: NotRequired[SemanticEntityTypeUnionTypeDef]
    Definition: NotRequired[Sequence[NamedEntityDefinitionUnionTypeDef]]


class ComparisonConfigurationTypeDef(TypedDict):
    ComparisonMethod: NotRequired[ComparisonMethodType]
    ComparisonFormat: NotRequired[ComparisonFormatConfigurationTypeDef]


class DateTimeFormatConfigurationTypeDef(TypedDict):
    DateTimeFormat: NotRequired[str]
    NullValueFormatConfiguration: NotRequired[NullValueFormatConfigurationTypeDef]
    NumericFormatConfiguration: NotRequired[NumericFormatConfigurationTypeDef]


class NumberFormatConfigurationTypeDef(TypedDict):
    FormatConfiguration: NotRequired[NumericFormatConfigurationTypeDef]


class ReferenceLineValueLabelConfigurationTypeDef(TypedDict):
    RelativePosition: NotRequired[ReferenceLineValueLabelRelativePositionType]
    FormatConfiguration: NotRequired[NumericFormatConfigurationTypeDef]


class StringFormatConfigurationTypeDef(TypedDict):
    NullValueFormatConfiguration: NotRequired[NullValueFormatConfigurationTypeDef]
    NumericFormatConfiguration: NotRequired[NumericFormatConfigurationTypeDef]


class BodySectionDynamicCategoryDimensionConfigurationOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Limit: NotRequired[int]
    SortByMetrics: NotRequired[List[ColumnSortTypeDef]]


class BodySectionDynamicCategoryDimensionConfigurationTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Limit: NotRequired[int]
    SortByMetrics: NotRequired[Sequence[ColumnSortTypeDef]]


class BodySectionDynamicNumericDimensionConfigurationOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Limit: NotRequired[int]
    SortByMetrics: NotRequired[List[ColumnSortTypeDef]]


class BodySectionDynamicNumericDimensionConfigurationTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Limit: NotRequired[int]
    SortByMetrics: NotRequired[Sequence[ColumnSortTypeDef]]


class FieldSortOptionsTypeDef(TypedDict):
    FieldSort: NotRequired[FieldSortTypeDef]
    ColumnSort: NotRequired[ColumnSortTypeDef]


class PivotTableSortByOutputTypeDef(TypedDict):
    Field: NotRequired[FieldSortTypeDef]
    Column: NotRequired[ColumnSortTypeDef]
    DataPath: NotRequired[DataPathSortOutputTypeDef]


class PivotTableSortByTypeDef(TypedDict):
    Field: NotRequired[FieldSortTypeDef]
    Column: NotRequired[ColumnSortTypeDef]
    DataPath: NotRequired[DataPathSortUnionTypeDef]


class TooltipItemTypeDef(TypedDict):
    FieldTooltipItem: NotRequired[FieldTooltipItemTypeDef]
    ColumnTooltipItem: NotRequired[ColumnTooltipItemTypeDef]


class ReferenceLineDataConfigurationTypeDef(TypedDict):
    StaticConfiguration: NotRequired[ReferenceLineStaticDataConfigurationTypeDef]
    DynamicConfiguration: NotRequired[ReferenceLineDynamicDataConfigurationTypeDef]
    AxisBinding: NotRequired[AxisBindingType]
    SeriesType: NotRequired[ReferenceLineSeriesTypeType]


class DatasetMetadataOutputTypeDef(TypedDict):
    DatasetArn: str
    DatasetName: NotRequired[str]
    DatasetDescription: NotRequired[str]
    DataAggregation: NotRequired[DataAggregationTypeDef]
    Filters: NotRequired[List[TopicFilterOutputTypeDef]]
    Columns: NotRequired[List[TopicColumnOutputTypeDef]]
    CalculatedFields: NotRequired[List[TopicCalculatedFieldOutputTypeDef]]
    NamedEntities: NotRequired[List[TopicNamedEntityOutputTypeDef]]


class DataSourceParametersTypeDef(TypedDict):
    AmazonElasticsearchParameters: NotRequired[AmazonElasticsearchParametersTypeDef]
    AthenaParameters: NotRequired[AthenaParametersTypeDef]
    AuroraParameters: NotRequired[AuroraParametersTypeDef]
    AuroraPostgreSqlParameters: NotRequired[AuroraPostgreSqlParametersTypeDef]
    AwsIotAnalyticsParameters: NotRequired[AwsIotAnalyticsParametersTypeDef]
    JiraParameters: NotRequired[JiraParametersTypeDef]
    MariaDbParameters: NotRequired[MariaDbParametersTypeDef]
    MySqlParameters: NotRequired[MySqlParametersTypeDef]
    OracleParameters: NotRequired[OracleParametersTypeDef]
    PostgreSqlParameters: NotRequired[PostgreSqlParametersTypeDef]
    PrestoParameters: NotRequired[PrestoParametersTypeDef]
    RdsParameters: NotRequired[RdsParametersTypeDef]
    RedshiftParameters: NotRequired[RedshiftParametersUnionTypeDef]
    S3Parameters: NotRequired[S3ParametersTypeDef]
    ServiceNowParameters: NotRequired[ServiceNowParametersTypeDef]
    SnowflakeParameters: NotRequired[SnowflakeParametersTypeDef]
    SparkParameters: NotRequired[SparkParametersTypeDef]
    SqlServerParameters: NotRequired[SqlServerParametersTypeDef]
    TeradataParameters: NotRequired[TeradataParametersTypeDef]
    TwitterParameters: NotRequired[TwitterParametersTypeDef]
    AmazonOpenSearchParameters: NotRequired[AmazonOpenSearchParametersTypeDef]
    ExasolParameters: NotRequired[ExasolParametersTypeDef]
    DatabricksParameters: NotRequired[DatabricksParametersTypeDef]
    StarburstParameters: NotRequired[StarburstParametersTypeDef]
    TrinoParameters: NotRequired[TrinoParametersTypeDef]
    BigQueryParameters: NotRequired[BigQueryParametersTypeDef]


class GenerateEmbedUrlForRegisteredUserRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    UserArn: str
    ExperienceConfiguration: RegisteredUserEmbeddingExperienceConfigurationTypeDef
    SessionLifetimeInMinutes: NotRequired[int]
    AllowedDomains: NotRequired[Sequence[str]]


class GenerateEmbedUrlForRegisteredUserWithIdentityRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    ExperienceConfiguration: RegisteredUserEmbeddingExperienceConfigurationTypeDef
    SessionLifetimeInMinutes: NotRequired[int]
    AllowedDomains: NotRequired[Sequence[str]]


class AnonymousUserSnapshotJobResultTypeDef(TypedDict):
    FileGroups: NotRequired[List[SnapshotJobResultFileGroupTypeDef]]


PhysicalTableUnionTypeDef = Union[PhysicalTableTypeDef, PhysicalTableOutputTypeDef]


class CustomActionFilterOperationTypeDef(TypedDict):
    SelectedFieldsConfiguration: FilterOperationSelectedFieldsConfigurationUnionTypeDef
    TargetVisualsConfiguration: FilterOperationTargetVisualsConfigurationUnionTypeDef


class DefaultPaginatedLayoutConfigurationTypeDef(TypedDict):
    SectionBased: NotRequired[DefaultSectionBasedLayoutConfigurationTypeDef]


class SectionLayoutConfigurationOutputTypeDef(TypedDict):
    FreeFormLayout: FreeFormSectionLayoutConfigurationOutputTypeDef


class FreeFormLayoutConfigurationTypeDef(TypedDict):
    Elements: Sequence[FreeFormLayoutElementUnionTypeDef]
    CanvasSizeOptions: NotRequired[FreeFormLayoutCanvasSizeOptionsTypeDef]


class FreeFormSectionLayoutConfigurationTypeDef(TypedDict):
    Elements: Sequence[FreeFormLayoutElementUnionTypeDef]


class FilterScopeConfigurationTypeDef(TypedDict):
    SelectedSheets: NotRequired[SelectedSheetsFilterScopeConfigurationUnionTypeDef]
    AllSheets: NotRequired[Mapping[str, Any]]


class DescribeDashboardSnapshotJobResponseTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    SnapshotJobId: str
    UserConfiguration: SnapshotUserConfigurationRedactedTypeDef
    SnapshotConfiguration: SnapshotConfigurationOutputTypeDef
    Arn: str
    JobStatus: SnapshotJobStatusType
    CreatedTime: datetime
    LastUpdatedTime: datetime
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class SnapshotFileGroupTypeDef(TypedDict):
    Files: NotRequired[Sequence[SnapshotFileUnionTypeDef]]


FilterCrossSheetControlUnionTypeDef = Union[
    FilterCrossSheetControlTypeDef, FilterCrossSheetControlOutputTypeDef
]
DateTimeParameterDeclarationUnionTypeDef = Union[
    DateTimeParameterDeclarationTypeDef, DateTimeParameterDeclarationOutputTypeDef
]
DecimalParameterDeclarationUnionTypeDef = Union[
    DecimalParameterDeclarationTypeDef, DecimalParameterDeclarationOutputTypeDef
]
IntegerParameterDeclarationUnionTypeDef = Union[
    IntegerParameterDeclarationTypeDef, IntegerParameterDeclarationOutputTypeDef
]
StringParameterDeclarationUnionTypeDef = Union[
    StringParameterDeclarationTypeDef, StringParameterDeclarationOutputTypeDef
]


class AssetBundleImportJobOverrideParametersOutputTypeDef(TypedDict):
    ResourceIdOverrideConfiguration: NotRequired[
        AssetBundleImportJobResourceIdOverrideConfigurationTypeDef
    ]
    VPCConnections: NotRequired[
        List[AssetBundleImportJobVPCConnectionOverrideParametersOutputTypeDef]
    ]
    RefreshSchedules: NotRequired[
        List[AssetBundleImportJobRefreshScheduleOverrideParametersOutputTypeDef]
    ]
    DataSources: NotRequired[List[AssetBundleImportJobDataSourceOverrideParametersOutputTypeDef]]
    DataSets: NotRequired[List[AssetBundleImportJobDataSetOverrideParametersTypeDef]]
    Themes: NotRequired[List[AssetBundleImportJobThemeOverrideParametersTypeDef]]
    Analyses: NotRequired[List[AssetBundleImportJobAnalysisOverrideParametersTypeDef]]
    Dashboards: NotRequired[List[AssetBundleImportJobDashboardOverrideParametersTypeDef]]
    Folders: NotRequired[List[AssetBundleImportJobFolderOverrideParametersTypeDef]]


class DescribeDataSourceResponseTypeDef(TypedDict):
    DataSource: DataSourceTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ListDataSourcesResponseTypeDef(TypedDict):
    DataSources: List[DataSourceTypeDef]
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DestinationParameterValueConfigurationTypeDef(TypedDict):
    CustomValuesConfiguration: NotRequired[CustomValuesConfigurationUnionTypeDef]
    SelectAllValueOptions: NotRequired[Literal["ALL_VALUES"]]
    SourceParameterName: NotRequired[str]
    SourceField: NotRequired[str]
    SourceColumn: NotRequired[ColumnIdentifierTypeDef]


class DatasetParameterTypeDef(TypedDict):
    StringDatasetParameter: NotRequired[StringDatasetParameterUnionTypeDef]
    DecimalDatasetParameter: NotRequired[DecimalDatasetParameterUnionTypeDef]
    IntegerDatasetParameter: NotRequired[IntegerDatasetParameterUnionTypeDef]
    DateTimeDatasetParameter: NotRequired[DateTimeDatasetParameterUnionTypeDef]


class TransformOperationTypeDef(TypedDict):
    ProjectOperation: NotRequired[ProjectOperationUnionTypeDef]
    FilterOperation: NotRequired[FilterOperationTypeDef]
    CreateColumnsOperation: NotRequired[CreateColumnsOperationUnionTypeDef]
    RenameColumnOperation: NotRequired[RenameColumnOperationTypeDef]
    CastColumnTypeOperation: NotRequired[CastColumnTypeOperationTypeDef]
    TagColumnOperation: NotRequired[TagColumnOperationUnionTypeDef]
    UntagColumnOperation: NotRequired[UntagColumnOperationUnionTypeDef]
    OverrideDatasetParameterOperation: NotRequired[OverrideDatasetParameterOperationUnionTypeDef]


class DateTimeHierarchyTypeDef(TypedDict):
    HierarchyId: str
    DrillDownFilters: NotRequired[Sequence[DrillDownFilterUnionTypeDef]]


class ExplicitHierarchyTypeDef(TypedDict):
    HierarchyId: str
    Columns: Sequence[ColumnIdentifierTypeDef]
    DrillDownFilters: NotRequired[Sequence[DrillDownFilterUnionTypeDef]]


class PredefinedHierarchyTypeDef(TypedDict):
    HierarchyId: str
    Columns: Sequence[ColumnIdentifierTypeDef]
    DrillDownFilters: NotRequired[Sequence[DrillDownFilterUnionTypeDef]]


class ForecastConfigurationTypeDef(TypedDict):
    ForecastProperties: NotRequired[TimeBasedForecastPropertiesTypeDef]
    Scenario: NotRequired[ForecastScenarioUnionTypeDef]


AssetBundleImportJobDashboardOverridePermissionsUnionTypeDef = Union[
    AssetBundleImportJobDashboardOverridePermissionsTypeDef,
    AssetBundleImportJobDashboardOverridePermissionsOutputTypeDef,
]


class AxisDataOptionsTypeDef(TypedDict):
    NumericAxisOptions: NotRequired[NumericAxisOptionsUnionTypeDef]
    DateAxisOptions: NotRequired[DateAxisOptionsTypeDef]


class ContributionAnalysisTimeRangesTypeDef(TypedDict):
    StartRange: NotRequired[TopicIRFilterOptionUnionTypeDef]
    EndRange: NotRequired[TopicIRFilterOptionUnionTypeDef]


TopicCategoryFilterUnionTypeDef = Union[
    TopicCategoryFilterTypeDef, TopicCategoryFilterOutputTypeDef
]


class DataSetTypeDef(TypedDict):
    Arn: NotRequired[str]
    DataSetId: NotRequired[str]
    Name: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    PhysicalTableMap: NotRequired[Dict[str, PhysicalTableOutputTypeDef]]
    LogicalTableMap: NotRequired[Dict[str, LogicalTableOutputTypeDef]]
    OutputColumns: NotRequired[List[OutputColumnTypeDef]]
    ImportMode: NotRequired[DataSetImportModeType]
    ConsumedSpiceCapacityInBytes: NotRequired[int]
    ColumnGroups: NotRequired[List[ColumnGroupOutputTypeDef]]
    FieldFolders: NotRequired[Dict[str, FieldFolderOutputTypeDef]]
    RowLevelPermissionDataSet: NotRequired[RowLevelPermissionDataSetTypeDef]
    RowLevelPermissionTagConfiguration: NotRequired[RowLevelPermissionTagConfigurationOutputTypeDef]
    ColumnLevelPermissionRules: NotRequired[List[ColumnLevelPermissionRuleOutputTypeDef]]
    DataSetUsageConfiguration: NotRequired[DataSetUsageConfigurationTypeDef]
    DatasetParameters: NotRequired[List[DatasetParameterOutputTypeDef]]


class ImageCustomActionOperationOutputTypeDef(TypedDict):
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationOutputTypeDef]


class LayerCustomActionOperationOutputTypeDef(TypedDict):
    FilterOperation: NotRequired[CustomActionFilterOperationOutputTypeDef]
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationOutputTypeDef]


class VisualCustomActionOperationOutputTypeDef(TypedDict):
    FilterOperation: NotRequired[CustomActionFilterOperationOutputTypeDef]
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationOutputTypeDef]


PivotTableFieldCollapseStateOptionUnionTypeDef = Union[
    PivotTableFieldCollapseStateOptionTypeDef, PivotTableFieldCollapseStateOptionOutputTypeDef
]


class TopicIROutputTypeDef(TypedDict):
    Metrics: NotRequired[List[TopicIRMetricOutputTypeDef]]
    GroupByList: NotRequired[List[TopicIRGroupByTypeDef]]
    Filters: NotRequired[List[List[TopicIRFilterOptionOutputTypeDef]]]
    Sort: NotRequired[TopicSortClauseTypeDef]
    ContributionAnalysis: NotRequired[TopicIRContributionAnalysisOutputTypeDef]
    Visual: NotRequired[VisualOptionsTypeDef]


class LineSeriesAxisDisplayOptionsOutputTypeDef(TypedDict):
    AxisOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    MissingDataConfigurations: NotRequired[List[MissingDataConfigurationTypeDef]]


DefaultFilterDropDownControlOptionsUnionTypeDef = Union[
    DefaultFilterDropDownControlOptionsTypeDef, DefaultFilterDropDownControlOptionsOutputTypeDef
]
FilterDropDownControlUnionTypeDef = Union[
    FilterDropDownControlTypeDef, FilterDropDownControlOutputTypeDef
]
ParameterDropDownControlUnionTypeDef = Union[
    ParameterDropDownControlTypeDef, ParameterDropDownControlOutputTypeDef
]
DefaultFilterListControlOptionsUnionTypeDef = Union[
    DefaultFilterListControlOptionsTypeDef, DefaultFilterListControlOptionsOutputTypeDef
]
FilterListControlUnionTypeDef = Union[FilterListControlTypeDef, FilterListControlOutputTypeDef]
ParameterListControlUnionTypeDef = Union[
    ParameterListControlTypeDef, ParameterListControlOutputTypeDef
]


class DefaultFilterControlOptionsOutputTypeDef(TypedDict):
    DefaultDateTimePickerOptions: NotRequired[DefaultDateTimePickerControlOptionsTypeDef]
    DefaultListOptions: NotRequired[DefaultFilterListControlOptionsOutputTypeDef]
    DefaultDropdownOptions: NotRequired[DefaultFilterDropDownControlOptionsOutputTypeDef]
    DefaultTextFieldOptions: NotRequired[DefaultTextFieldControlOptionsTypeDef]
    DefaultTextAreaOptions: NotRequired[DefaultTextAreaControlOptionsTypeDef]
    DefaultSliderOptions: NotRequired[DefaultSliderControlOptionsTypeDef]
    DefaultRelativeDateTimeOptions: NotRequired[DefaultRelativeDateTimeControlOptionsTypeDef]


FilterControlOutputTypeDef = TypedDict(
    "FilterControlOutputTypeDef",
    {
        "DateTimePicker": NotRequired[FilterDateTimePickerControlTypeDef],
        "List": NotRequired[FilterListControlOutputTypeDef],
        "Dropdown": NotRequired[FilterDropDownControlOutputTypeDef],
        "TextField": NotRequired[FilterTextFieldControlTypeDef],
        "TextArea": NotRequired[FilterTextAreaControlTypeDef],
        "Slider": NotRequired[FilterSliderControlTypeDef],
        "RelativeDateTime": NotRequired[FilterRelativeDateTimeControlTypeDef],
        "CrossSheet": NotRequired[FilterCrossSheetControlOutputTypeDef],
    },
)
ParameterControlOutputTypeDef = TypedDict(
    "ParameterControlOutputTypeDef",
    {
        "DateTimePicker": NotRequired[ParameterDateTimePickerControlTypeDef],
        "List": NotRequired[ParameterListControlOutputTypeDef],
        "Dropdown": NotRequired[ParameterDropDownControlOutputTypeDef],
        "TextField": NotRequired[ParameterTextFieldControlTypeDef],
        "TextArea": NotRequired[ParameterTextAreaControlTypeDef],
        "Slider": NotRequired[ParameterSliderControlTypeDef],
    },
)


class TableFieldURLConfigurationTypeDef(TypedDict):
    LinkConfiguration: NotRequired[TableFieldLinkConfigurationTypeDef]
    ImageConfiguration: NotRequired[TableFieldImageConfigurationTypeDef]


class GeospatialPointStyleOptionsTypeDef(TypedDict):
    SelectedPointStyle: NotRequired[GeospatialSelectedPointStyleType]
    ClusterMarkerConfiguration: NotRequired[ClusterMarkerConfigurationTypeDef]
    HeatmapConfiguration: NotRequired[GeospatialHeatmapConfigurationUnionTypeDef]


class GeospatialPointStyleOutputTypeDef(TypedDict):
    CircleSymbolStyle: NotRequired[GeospatialCircleSymbolStyleOutputTypeDef]


class GeospatialLineStyleOutputTypeDef(TypedDict):
    LineSymbolStyle: NotRequired[GeospatialLineSymbolStyleOutputTypeDef]


class GeospatialPolygonStyleOutputTypeDef(TypedDict):
    PolygonSymbolStyle: NotRequired[GeospatialPolygonSymbolStyleOutputTypeDef]


GeospatialColorUnionTypeDef = Union[GeospatialColorTypeDef, GeospatialColorOutputTypeDef]
PivotTableOptionsUnionTypeDef = Union[PivotTableOptionsTypeDef, PivotTableOptionsOutputTypeDef]
PivotTotalOptionsUnionTypeDef = Union[PivotTotalOptionsTypeDef, PivotTotalOptionsOutputTypeDef]


class PivotTableTotalOptionsOutputTypeDef(TypedDict):
    RowSubtotalOptions: NotRequired[SubtotalOptionsOutputTypeDef]
    ColumnSubtotalOptions: NotRequired[SubtotalOptionsOutputTypeDef]
    RowTotalOptions: NotRequired[PivotTotalOptionsOutputTypeDef]
    ColumnTotalOptions: NotRequired[PivotTotalOptionsOutputTypeDef]


SubtotalOptionsUnionTypeDef = Union[SubtotalOptionsTypeDef, SubtotalOptionsOutputTypeDef]
TableOptionsUnionTypeDef = Union[TableOptionsTypeDef, TableOptionsOutputTypeDef]
TotalOptionsUnionTypeDef = Union[TotalOptionsTypeDef, TotalOptionsOutputTypeDef]


class GaugeChartConditionalFormattingOptionOutputTypeDef(TypedDict):
    PrimaryValue: NotRequired[GaugeChartPrimaryValueConditionalFormattingOutputTypeDef]
    Arc: NotRequired[GaugeChartArcConditionalFormattingOutputTypeDef]


class KPIConditionalFormattingOptionOutputTypeDef(TypedDict):
    PrimaryValue: NotRequired[KPIPrimaryValueConditionalFormattingOutputTypeDef]
    ProgressBar: NotRequired[KPIProgressBarConditionalFormattingOutputTypeDef]
    ActualValue: NotRequired[KPIActualValueConditionalFormattingOutputTypeDef]
    ComparisonValue: NotRequired[KPIComparisonValueConditionalFormattingOutputTypeDef]


class FilledMapShapeConditionalFormattingOutputTypeDef(TypedDict):
    FieldId: str
    Format: NotRequired[ShapeConditionalFormatOutputTypeDef]


class PivotTableCellConditionalFormattingOutputTypeDef(TypedDict):
    FieldId: str
    TextFormat: NotRequired[TextConditionalFormatOutputTypeDef]
    Scope: NotRequired[PivotTableConditionalFormattingScopeTypeDef]
    Scopes: NotRequired[List[PivotTableConditionalFormattingScopeTypeDef]]


class TableCellConditionalFormattingOutputTypeDef(TypedDict):
    FieldId: str
    TextFormat: NotRequired[TextConditionalFormatOutputTypeDef]


class ConditionalFormattingColorTypeDef(TypedDict):
    Solid: NotRequired[ConditionalFormattingSolidColorTypeDef]
    Gradient: NotRequired[ConditionalFormattingGradientColorUnionTypeDef]


SheetControlLayoutConfigurationUnionTypeDef = Union[
    SheetControlLayoutConfigurationTypeDef, SheetControlLayoutConfigurationOutputTypeDef
]


class BrandDefinitionTypeDef(TypedDict):
    BrandName: str
    Description: NotRequired[str]
    ApplicationTheme: NotRequired[ApplicationThemeTypeDef]
    LogoConfiguration: NotRequired[LogoConfigurationTypeDef]


class BrandDetailTypeDef(TypedDict):
    BrandId: str
    Arn: NotRequired[str]
    BrandStatus: NotRequired[BrandStatusType]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    VersionId: NotRequired[str]
    VersionStatus: NotRequired[BrandVersionStatusType]
    Errors: NotRequired[List[str]]
    Logo: NotRequired[LogoTypeDef]


ThemeTypeDef = TypedDict(
    "ThemeTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
        "ThemeId": NotRequired[str],
        "Version": NotRequired[ThemeVersionTypeDef],
        "CreatedTime": NotRequired[datetime],
        "LastUpdatedTime": NotRequired[datetime],
        "Type": NotRequired[ThemeTypeType],
    },
)
TopicNamedEntityUnionTypeDef = Union[TopicNamedEntityTypeDef, TopicNamedEntityOutputTypeDef]


class GaugeChartOptionsTypeDef(TypedDict):
    PrimaryValueDisplayType: NotRequired[PrimaryValueDisplayTypeType]
    Comparison: NotRequired[ComparisonConfigurationTypeDef]
    ArcAxis: NotRequired[ArcAxisConfigurationTypeDef]
    Arc: NotRequired[ArcConfigurationTypeDef]
    PrimaryValueFontConfiguration: NotRequired[FontConfigurationTypeDef]


class KPIOptionsTypeDef(TypedDict):
    ProgressBar: NotRequired[ProgressBarOptionsTypeDef]
    TrendArrows: NotRequired[TrendArrowOptionsTypeDef]
    SecondaryValue: NotRequired[SecondaryValueOptionsTypeDef]
    Comparison: NotRequired[ComparisonConfigurationTypeDef]
    PrimaryValueDisplayType: NotRequired[PrimaryValueDisplayTypeType]
    PrimaryValueFontConfiguration: NotRequired[FontConfigurationTypeDef]
    SecondaryValueFontConfiguration: NotRequired[FontConfigurationTypeDef]
    Sparkline: NotRequired[KPISparklineOptionsTypeDef]
    VisualLayoutOptions: NotRequired[KPIVisualLayoutOptionsTypeDef]


class DateDimensionFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    DateGranularity: NotRequired[TimeGranularityType]
    HierarchyId: NotRequired[str]
    FormatConfiguration: NotRequired[DateTimeFormatConfigurationTypeDef]


class DateMeasureFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    AggregationFunction: NotRequired[DateAggregationFunctionType]
    FormatConfiguration: NotRequired[DateTimeFormatConfigurationTypeDef]


class NumericalDimensionFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    HierarchyId: NotRequired[str]
    FormatConfiguration: NotRequired[NumberFormatConfigurationTypeDef]


class NumericalMeasureFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    AggregationFunction: NotRequired[NumericalAggregationFunctionTypeDef]
    FormatConfiguration: NotRequired[NumberFormatConfigurationTypeDef]


class ReferenceLineLabelConfigurationTypeDef(TypedDict):
    ValueLabelConfiguration: NotRequired[ReferenceLineValueLabelConfigurationTypeDef]
    CustomLabelConfiguration: NotRequired[ReferenceLineCustomLabelConfigurationTypeDef]
    FontConfiguration: NotRequired[FontConfigurationTypeDef]
    FontColor: NotRequired[str]
    HorizontalPosition: NotRequired[ReferenceLineLabelHorizontalPositionType]
    VerticalPosition: NotRequired[ReferenceLineLabelVerticalPositionType]


class CategoricalDimensionFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    HierarchyId: NotRequired[str]
    FormatConfiguration: NotRequired[StringFormatConfigurationTypeDef]


class CategoricalMeasureFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    AggregationFunction: NotRequired[CategoricalAggregationFunctionType]
    FormatConfiguration: NotRequired[StringFormatConfigurationTypeDef]


class FormatConfigurationTypeDef(TypedDict):
    StringFormatConfiguration: NotRequired[StringFormatConfigurationTypeDef]
    NumberFormatConfiguration: NotRequired[NumberFormatConfigurationTypeDef]
    DateTimeFormatConfiguration: NotRequired[DateTimeFormatConfigurationTypeDef]


BodySectionDynamicCategoryDimensionConfigurationUnionTypeDef = Union[
    BodySectionDynamicCategoryDimensionConfigurationTypeDef,
    BodySectionDynamicCategoryDimensionConfigurationOutputTypeDef,
]


class BodySectionRepeatDimensionConfigurationOutputTypeDef(TypedDict):
    DynamicCategoryDimensionConfiguration: NotRequired[
        BodySectionDynamicCategoryDimensionConfigurationOutputTypeDef
    ]
    DynamicNumericDimensionConfiguration: NotRequired[
        BodySectionDynamicNumericDimensionConfigurationOutputTypeDef
    ]


BodySectionDynamicNumericDimensionConfigurationUnionTypeDef = Union[
    BodySectionDynamicNumericDimensionConfigurationTypeDef,
    BodySectionDynamicNumericDimensionConfigurationOutputTypeDef,
]


class BarChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[List[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[List[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[List[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class BarChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class BoxPlotSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[List[FieldSortOptionsTypeDef]]
    PaginationConfiguration: NotRequired[PaginationConfigurationTypeDef]


class BoxPlotSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    PaginationConfiguration: NotRequired[PaginationConfigurationTypeDef]


class ComboChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[List[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[List[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class ComboChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class FilledMapSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[List[FieldSortOptionsTypeDef]]


class FilledMapSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]


class FunnelChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[List[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class FunnelChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class HeatMapSortConfigurationOutputTypeDef(TypedDict):
    HeatMapRowSort: NotRequired[List[FieldSortOptionsTypeDef]]
    HeatMapColumnSort: NotRequired[List[FieldSortOptionsTypeDef]]
    HeatMapRowItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    HeatMapColumnItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class HeatMapSortConfigurationTypeDef(TypedDict):
    HeatMapRowSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    HeatMapColumnSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    HeatMapRowItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    HeatMapColumnItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class KPISortConfigurationOutputTypeDef(TypedDict):
    TrendGroupSort: NotRequired[List[FieldSortOptionsTypeDef]]


class KPISortConfigurationTypeDef(TypedDict):
    TrendGroupSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]


class LineChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[List[FieldSortOptionsTypeDef]]
    CategoryItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[List[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class LineChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class PieChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[List[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[List[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class PieChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    SmallMultiplesSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    SmallMultiplesLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class PluginVisualTableQuerySortOutputTypeDef(TypedDict):
    RowSort: NotRequired[List[FieldSortOptionsTypeDef]]
    ItemsLimitConfiguration: NotRequired[PluginVisualItemsLimitConfigurationTypeDef]


class PluginVisualTableQuerySortTypeDef(TypedDict):
    RowSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    ItemsLimitConfiguration: NotRequired[PluginVisualItemsLimitConfigurationTypeDef]


class RadarChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[List[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[List[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class RadarChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    ColorSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    ColorItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class SankeyDiagramSortConfigurationOutputTypeDef(TypedDict):
    WeightSort: NotRequired[List[FieldSortOptionsTypeDef]]
    SourceItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    DestinationItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class SankeyDiagramSortConfigurationTypeDef(TypedDict):
    WeightSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    SourceItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    DestinationItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class TableSortConfigurationOutputTypeDef(TypedDict):
    RowSort: NotRequired[List[FieldSortOptionsTypeDef]]
    PaginationConfiguration: NotRequired[PaginationConfigurationTypeDef]


class TableSortConfigurationTypeDef(TypedDict):
    RowSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    PaginationConfiguration: NotRequired[PaginationConfigurationTypeDef]


class TreeMapSortConfigurationOutputTypeDef(TypedDict):
    TreeMapSort: NotRequired[List[FieldSortOptionsTypeDef]]
    TreeMapGroupItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class TreeMapSortConfigurationTypeDef(TypedDict):
    TreeMapSort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    TreeMapGroupItemsLimitConfiguration: NotRequired[ItemsLimitConfigurationTypeDef]


class WaterfallChartSortConfigurationOutputTypeDef(TypedDict):
    CategorySort: NotRequired[List[FieldSortOptionsTypeDef]]
    BreakdownItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class WaterfallChartSortConfigurationTypeDef(TypedDict):
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]
    BreakdownItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]


class WordCloudSortConfigurationOutputTypeDef(TypedDict):
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    CategorySort: NotRequired[List[FieldSortOptionsTypeDef]]


class WordCloudSortConfigurationTypeDef(TypedDict):
    CategoryItemsLimit: NotRequired[ItemsLimitConfigurationTypeDef]
    CategorySort: NotRequired[Sequence[FieldSortOptionsTypeDef]]


class PivotFieldSortOptionsOutputTypeDef(TypedDict):
    FieldId: str
    SortBy: PivotTableSortByOutputTypeDef


PivotTableSortByUnionTypeDef = Union[PivotTableSortByTypeDef, PivotTableSortByOutputTypeDef]


class FieldBasedTooltipOutputTypeDef(TypedDict):
    AggregationVisibility: NotRequired[VisibilityType]
    TooltipTitleType: NotRequired[TooltipTitleTypeType]
    TooltipFields: NotRequired[List[TooltipItemTypeDef]]


class FieldBasedTooltipTypeDef(TypedDict):
    AggregationVisibility: NotRequired[VisibilityType]
    TooltipTitleType: NotRequired[TooltipTitleTypeType]
    TooltipFields: NotRequired[Sequence[TooltipItemTypeDef]]


class TopicDetailsOutputTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    UserExperienceVersion: NotRequired[TopicUserExperienceVersionType]
    DataSets: NotRequired[List[DatasetMetadataOutputTypeDef]]
    ConfigOptions: NotRequired[TopicConfigOptionsTypeDef]


DataSourceParametersUnionTypeDef = Union[
    DataSourceParametersTypeDef, DataSourceParametersOutputTypeDef
]


class SnapshotJobResultTypeDef(TypedDict):
    AnonymousUsers: NotRequired[List[AnonymousUserSnapshotJobResultTypeDef]]


CustomActionFilterOperationUnionTypeDef = Union[
    CustomActionFilterOperationTypeDef, CustomActionFilterOperationOutputTypeDef
]


class DefaultNewSheetConfigurationTypeDef(TypedDict):
    InteractiveLayoutConfiguration: NotRequired[DefaultInteractiveLayoutConfigurationTypeDef]
    PaginatedLayoutConfiguration: NotRequired[DefaultPaginatedLayoutConfigurationTypeDef]
    SheetContentType: NotRequired[SheetContentTypeType]


class BodySectionContentOutputTypeDef(TypedDict):
    Layout: NotRequired[SectionLayoutConfigurationOutputTypeDef]


class HeaderFooterSectionConfigurationOutputTypeDef(TypedDict):
    SectionId: str
    Layout: SectionLayoutConfigurationOutputTypeDef
    Style: NotRequired[SectionStyleTypeDef]


FreeFormLayoutConfigurationUnionTypeDef = Union[
    FreeFormLayoutConfigurationTypeDef, FreeFormLayoutConfigurationOutputTypeDef
]
FreeFormSectionLayoutConfigurationUnionTypeDef = Union[
    FreeFormSectionLayoutConfigurationTypeDef, FreeFormSectionLayoutConfigurationOutputTypeDef
]
FilterScopeConfigurationUnionTypeDef = Union[
    FilterScopeConfigurationTypeDef, FilterScopeConfigurationOutputTypeDef
]
SnapshotFileGroupUnionTypeDef = Union[SnapshotFileGroupTypeDef, SnapshotFileGroupOutputTypeDef]


class ParameterDeclarationTypeDef(TypedDict):
    StringParameterDeclaration: NotRequired[StringParameterDeclarationUnionTypeDef]
    DecimalParameterDeclaration: NotRequired[DecimalParameterDeclarationUnionTypeDef]
    IntegerParameterDeclaration: NotRequired[IntegerParameterDeclarationUnionTypeDef]
    DateTimeParameterDeclaration: NotRequired[DateTimeParameterDeclarationUnionTypeDef]


class DescribeAssetBundleImportJobResponseTypeDef(TypedDict):
    JobStatus: AssetBundleImportJobStatusType
    Errors: List[AssetBundleImportJobErrorTypeDef]
    RollbackErrors: List[AssetBundleImportJobErrorTypeDef]
    Arn: str
    CreatedTime: datetime
    AssetBundleImportJobId: str
    AwsAccountId: str
    AssetBundleImportSource: AssetBundleImportSourceDescriptionTypeDef
    OverrideParameters: AssetBundleImportJobOverrideParametersOutputTypeDef
    FailureAction: AssetBundleImportFailureActionType
    RequestId: str
    Status: int
    OverridePermissions: AssetBundleImportJobOverridePermissionsOutputTypeDef
    OverrideTags: AssetBundleImportJobOverrideTagsOutputTypeDef
    OverrideValidationStrategy: AssetBundleImportJobOverrideValidationStrategyTypeDef
    Warnings: List[AssetBundleImportJobWarningTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


DestinationParameterValueConfigurationUnionTypeDef = Union[
    DestinationParameterValueConfigurationTypeDef,
    DestinationParameterValueConfigurationOutputTypeDef,
]
DatasetParameterUnionTypeDef = Union[DatasetParameterTypeDef, DatasetParameterOutputTypeDef]
TransformOperationUnionTypeDef = Union[TransformOperationTypeDef, TransformOperationOutputTypeDef]
DateTimeHierarchyUnionTypeDef = Union[DateTimeHierarchyTypeDef, DateTimeHierarchyOutputTypeDef]
ExplicitHierarchyUnionTypeDef = Union[ExplicitHierarchyTypeDef, ExplicitHierarchyOutputTypeDef]
PredefinedHierarchyUnionTypeDef = Union[
    PredefinedHierarchyTypeDef, PredefinedHierarchyOutputTypeDef
]
ForecastConfigurationUnionTypeDef = Union[
    ForecastConfigurationTypeDef, ForecastConfigurationOutputTypeDef
]


class AssetBundleImportJobOverridePermissionsTypeDef(TypedDict):
    DataSources: NotRequired[
        Sequence[AssetBundleImportJobDataSourceOverridePermissionsUnionTypeDef]
    ]
    DataSets: NotRequired[Sequence[AssetBundleImportJobDataSetOverridePermissionsUnionTypeDef]]
    Themes: NotRequired[Sequence[AssetBundleImportJobThemeOverridePermissionsUnionTypeDef]]
    Analyses: NotRequired[Sequence[AssetBundleImportJobAnalysisOverridePermissionsUnionTypeDef]]
    Dashboards: NotRequired[Sequence[AssetBundleImportJobDashboardOverridePermissionsUnionTypeDef]]
    Folders: NotRequired[Sequence[AssetBundleImportJobFolderOverridePermissionsUnionTypeDef]]


AxisDataOptionsUnionTypeDef = Union[AxisDataOptionsTypeDef, AxisDataOptionsOutputTypeDef]
ContributionAnalysisTimeRangesUnionTypeDef = Union[
    ContributionAnalysisTimeRangesTypeDef, ContributionAnalysisTimeRangesOutputTypeDef
]


class TopicFilterTypeDef(TypedDict):
    FilterName: str
    OperandFieldName: str
    FilterDescription: NotRequired[str]
    FilterClass: NotRequired[FilterClassType]
    FilterSynonyms: NotRequired[Sequence[str]]
    FilterType: NotRequired[NamedFilterTypeType]
    CategoryFilter: NotRequired[TopicCategoryFilterUnionTypeDef]
    NumericEqualityFilter: NotRequired[TopicNumericEqualityFilterTypeDef]
    NumericRangeFilter: NotRequired[TopicNumericRangeFilterTypeDef]
    DateRangeFilter: NotRequired[TopicDateRangeFilterTypeDef]
    RelativeDateFilter: NotRequired[TopicRelativeDateFilterTypeDef]


class DescribeDataSetResponseTypeDef(TypedDict):
    DataSet: DataSetTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class ImageCustomActionOutputTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: ImageCustomActionTriggerType
    ActionOperations: List[ImageCustomActionOperationOutputTypeDef]
    Status: NotRequired[WidgetStatusType]


class LayerCustomActionOutputTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: LayerCustomActionTriggerType
    ActionOperations: List[LayerCustomActionOperationOutputTypeDef]
    Status: NotRequired[WidgetStatusType]


class VisualCustomActionOutputTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: VisualCustomActionTriggerType
    ActionOperations: List[VisualCustomActionOperationOutputTypeDef]
    Status: NotRequired[WidgetStatusType]


class PivotTableFieldOptionsTypeDef(TypedDict):
    SelectedFieldOptions: NotRequired[Sequence[PivotTableFieldOptionTypeDef]]
    DataPathOptions: NotRequired[Sequence[PivotTableDataPathOptionUnionTypeDef]]
    CollapseStateOptions: NotRequired[Sequence[PivotTableFieldCollapseStateOptionUnionTypeDef]]


class TopicVisualOutputTypeDef(TypedDict):
    VisualId: NotRequired[str]
    Role: NotRequired[VisualRoleType]
    Ir: NotRequired[TopicIROutputTypeDef]
    SupportingVisuals: NotRequired[List[Dict[str, Any]]]


class DefaultFilterControlOptionsTypeDef(TypedDict):
    DefaultDateTimePickerOptions: NotRequired[DefaultDateTimePickerControlOptionsTypeDef]
    DefaultListOptions: NotRequired[DefaultFilterListControlOptionsUnionTypeDef]
    DefaultDropdownOptions: NotRequired[DefaultFilterDropDownControlOptionsUnionTypeDef]
    DefaultTextFieldOptions: NotRequired[DefaultTextFieldControlOptionsTypeDef]
    DefaultTextAreaOptions: NotRequired[DefaultTextAreaControlOptionsTypeDef]
    DefaultSliderOptions: NotRequired[DefaultSliderControlOptionsTypeDef]
    DefaultRelativeDateTimeOptions: NotRequired[DefaultRelativeDateTimeControlOptionsTypeDef]


FilterControlTypeDef = TypedDict(
    "FilterControlTypeDef",
    {
        "DateTimePicker": NotRequired[FilterDateTimePickerControlTypeDef],
        "List": NotRequired[FilterListControlUnionTypeDef],
        "Dropdown": NotRequired[FilterDropDownControlUnionTypeDef],
        "TextField": NotRequired[FilterTextFieldControlTypeDef],
        "TextArea": NotRequired[FilterTextAreaControlTypeDef],
        "Slider": NotRequired[FilterSliderControlTypeDef],
        "RelativeDateTime": NotRequired[FilterRelativeDateTimeControlTypeDef],
        "CrossSheet": NotRequired[FilterCrossSheetControlUnionTypeDef],
    },
)
ParameterControlTypeDef = TypedDict(
    "ParameterControlTypeDef",
    {
        "DateTimePicker": NotRequired[ParameterDateTimePickerControlTypeDef],
        "List": NotRequired[ParameterListControlUnionTypeDef],
        "Dropdown": NotRequired[ParameterDropDownControlUnionTypeDef],
        "TextField": NotRequired[ParameterTextFieldControlTypeDef],
        "TextArea": NotRequired[ParameterTextAreaControlTypeDef],
        "Slider": NotRequired[ParameterSliderControlTypeDef],
    },
)


class DefaultFilterControlConfigurationOutputTypeDef(TypedDict):
    Title: str
    ControlOptions: DefaultFilterControlOptionsOutputTypeDef


class TableFieldOptionTypeDef(TypedDict):
    FieldId: str
    Width: NotRequired[str]
    CustomLabel: NotRequired[str]
    Visibility: NotRequired[VisibilityType]
    URLStyling: NotRequired[TableFieldURLConfigurationTypeDef]


GeospatialPointStyleOptionsUnionTypeDef = Union[
    GeospatialPointStyleOptionsTypeDef, GeospatialPointStyleOptionsOutputTypeDef
]


class GeospatialPointLayerOutputTypeDef(TypedDict):
    Style: GeospatialPointStyleOutputTypeDef


class GeospatialLineLayerOutputTypeDef(TypedDict):
    Style: GeospatialLineStyleOutputTypeDef


class GeospatialPolygonLayerOutputTypeDef(TypedDict):
    Style: GeospatialPolygonStyleOutputTypeDef


class GeospatialCircleSymbolStyleTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorUnionTypeDef]
    StrokeColor: NotRequired[GeospatialColorUnionTypeDef]
    StrokeWidth: NotRequired[GeospatialLineWidthTypeDef]
    CircleRadius: NotRequired[GeospatialCircleRadiusTypeDef]


class GeospatialLineSymbolStyleTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorUnionTypeDef]
    LineWidth: NotRequired[GeospatialLineWidthTypeDef]


class GeospatialPolygonSymbolStyleTypeDef(TypedDict):
    FillColor: NotRequired[GeospatialColorUnionTypeDef]
    StrokeColor: NotRequired[GeospatialColorUnionTypeDef]
    StrokeWidth: NotRequired[GeospatialLineWidthTypeDef]


class PivotTableTotalOptionsTypeDef(TypedDict):
    RowSubtotalOptions: NotRequired[SubtotalOptionsUnionTypeDef]
    ColumnSubtotalOptions: NotRequired[SubtotalOptionsUnionTypeDef]
    RowTotalOptions: NotRequired[PivotTotalOptionsUnionTypeDef]
    ColumnTotalOptions: NotRequired[PivotTotalOptionsUnionTypeDef]


class GaugeChartConditionalFormattingOutputTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[
        List[GaugeChartConditionalFormattingOptionOutputTypeDef]
    ]


class KPIConditionalFormattingOutputTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[List[KPIConditionalFormattingOptionOutputTypeDef]]


class FilledMapConditionalFormattingOptionOutputTypeDef(TypedDict):
    Shape: FilledMapShapeConditionalFormattingOutputTypeDef


class PivotTableConditionalFormattingOptionOutputTypeDef(TypedDict):
    Cell: NotRequired[PivotTableCellConditionalFormattingOutputTypeDef]


class TableConditionalFormattingOptionOutputTypeDef(TypedDict):
    Cell: NotRequired[TableCellConditionalFormattingOutputTypeDef]
    Row: NotRequired[TableRowConditionalFormattingOutputTypeDef]


ConditionalFormattingColorUnionTypeDef = Union[
    ConditionalFormattingColorTypeDef, ConditionalFormattingColorOutputTypeDef
]


class SheetControlLayoutTypeDef(TypedDict):
    Configuration: SheetControlLayoutConfigurationUnionTypeDef


class CreateBrandRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str
    BrandDefinition: NotRequired[BrandDefinitionTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class UpdateBrandRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    BrandId: str
    BrandDefinition: NotRequired[BrandDefinitionTypeDef]


class CreateBrandResponseTypeDef(TypedDict):
    RequestId: str
    BrandDetail: BrandDetailTypeDef
    BrandDefinition: BrandDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBrandPublishedVersionResponseTypeDef(TypedDict):
    RequestId: str
    BrandDetail: BrandDetailTypeDef
    BrandDefinition: BrandDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeBrandResponseTypeDef(TypedDict):
    RequestId: str
    BrandDetail: BrandDetailTypeDef
    BrandDefinition: BrandDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrandResponseTypeDef(TypedDict):
    RequestId: str
    BrandDetail: BrandDetailTypeDef
    BrandDefinition: BrandDefinitionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeThemeResponseTypeDef(TypedDict):
    Theme: ThemeTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReferenceLineTypeDef(TypedDict):
    DataConfiguration: ReferenceLineDataConfigurationTypeDef
    Status: NotRequired[WidgetStatusType]
    StyleConfiguration: NotRequired[ReferenceLineStyleConfigurationTypeDef]
    LabelConfiguration: NotRequired[ReferenceLineLabelConfigurationTypeDef]


class DimensionFieldTypeDef(TypedDict):
    NumericalDimensionField: NotRequired[NumericalDimensionFieldTypeDef]
    CategoricalDimensionField: NotRequired[CategoricalDimensionFieldTypeDef]
    DateDimensionField: NotRequired[DateDimensionFieldTypeDef]


class MeasureFieldTypeDef(TypedDict):
    NumericalMeasureField: NotRequired[NumericalMeasureFieldTypeDef]
    CategoricalMeasureField: NotRequired[CategoricalMeasureFieldTypeDef]
    DateMeasureField: NotRequired[DateMeasureFieldTypeDef]
    CalculatedMeasureField: NotRequired[CalculatedMeasureFieldTypeDef]


class ColumnConfigurationOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    FormatConfiguration: NotRequired[FormatConfigurationTypeDef]
    Role: NotRequired[ColumnRoleType]
    ColorsConfiguration: NotRequired[ColorsConfigurationOutputTypeDef]


class ColumnConfigurationTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    FormatConfiguration: NotRequired[FormatConfigurationTypeDef]
    Role: NotRequired[ColumnRoleType]
    ColorsConfiguration: NotRequired[ColorsConfigurationUnionTypeDef]


class UnaggregatedFieldTypeDef(TypedDict):
    FieldId: str
    Column: ColumnIdentifierTypeDef
    FormatConfiguration: NotRequired[FormatConfigurationTypeDef]


class BodySectionRepeatConfigurationOutputTypeDef(TypedDict):
    DimensionConfigurations: NotRequired[List[BodySectionRepeatDimensionConfigurationOutputTypeDef]]
    PageBreakConfiguration: NotRequired[BodySectionRepeatPageBreakConfigurationTypeDef]
    NonRepeatingVisuals: NotRequired[List[str]]


class BodySectionRepeatDimensionConfigurationTypeDef(TypedDict):
    DynamicCategoryDimensionConfiguration: NotRequired[
        BodySectionDynamicCategoryDimensionConfigurationUnionTypeDef
    ]
    DynamicNumericDimensionConfiguration: NotRequired[
        BodySectionDynamicNumericDimensionConfigurationUnionTypeDef
    ]


BarChartSortConfigurationUnionTypeDef = Union[
    BarChartSortConfigurationTypeDef, BarChartSortConfigurationOutputTypeDef
]
BoxPlotSortConfigurationUnionTypeDef = Union[
    BoxPlotSortConfigurationTypeDef, BoxPlotSortConfigurationOutputTypeDef
]
ComboChartSortConfigurationUnionTypeDef = Union[
    ComboChartSortConfigurationTypeDef, ComboChartSortConfigurationOutputTypeDef
]
FilledMapSortConfigurationUnionTypeDef = Union[
    FilledMapSortConfigurationTypeDef, FilledMapSortConfigurationOutputTypeDef
]
FunnelChartSortConfigurationUnionTypeDef = Union[
    FunnelChartSortConfigurationTypeDef, FunnelChartSortConfigurationOutputTypeDef
]
HeatMapSortConfigurationUnionTypeDef = Union[
    HeatMapSortConfigurationTypeDef, HeatMapSortConfigurationOutputTypeDef
]
KPISortConfigurationUnionTypeDef = Union[
    KPISortConfigurationTypeDef, KPISortConfigurationOutputTypeDef
]
LineChartSortConfigurationUnionTypeDef = Union[
    LineChartSortConfigurationTypeDef, LineChartSortConfigurationOutputTypeDef
]
PieChartSortConfigurationUnionTypeDef = Union[
    PieChartSortConfigurationTypeDef, PieChartSortConfigurationOutputTypeDef
]


class PluginVisualSortConfigurationOutputTypeDef(TypedDict):
    PluginVisualTableQuerySort: NotRequired[PluginVisualTableQuerySortOutputTypeDef]


PluginVisualTableQuerySortUnionTypeDef = Union[
    PluginVisualTableQuerySortTypeDef, PluginVisualTableQuerySortOutputTypeDef
]
RadarChartSortConfigurationUnionTypeDef = Union[
    RadarChartSortConfigurationTypeDef, RadarChartSortConfigurationOutputTypeDef
]
SankeyDiagramSortConfigurationUnionTypeDef = Union[
    SankeyDiagramSortConfigurationTypeDef, SankeyDiagramSortConfigurationOutputTypeDef
]
TableSortConfigurationUnionTypeDef = Union[
    TableSortConfigurationTypeDef, TableSortConfigurationOutputTypeDef
]
TreeMapSortConfigurationUnionTypeDef = Union[
    TreeMapSortConfigurationTypeDef, TreeMapSortConfigurationOutputTypeDef
]
WaterfallChartSortConfigurationUnionTypeDef = Union[
    WaterfallChartSortConfigurationTypeDef, WaterfallChartSortConfigurationOutputTypeDef
]
WordCloudSortConfigurationUnionTypeDef = Union[
    WordCloudSortConfigurationTypeDef, WordCloudSortConfigurationOutputTypeDef
]


class PivotTableSortConfigurationOutputTypeDef(TypedDict):
    FieldSortOptions: NotRequired[List[PivotFieldSortOptionsOutputTypeDef]]


class PivotFieldSortOptionsTypeDef(TypedDict):
    FieldId: str
    SortBy: PivotTableSortByUnionTypeDef


class TooltipOptionsOutputTypeDef(TypedDict):
    TooltipVisibility: NotRequired[VisibilityType]
    SelectedTooltipType: NotRequired[SelectedTooltipTypeType]
    FieldBasedTooltip: NotRequired[FieldBasedTooltipOutputTypeDef]


FieldBasedTooltipUnionTypeDef = Union[FieldBasedTooltipTypeDef, FieldBasedTooltipOutputTypeDef]


class DescribeTopicResponseTypeDef(TypedDict):
    Arn: str
    TopicId: str
    Topic: TopicDetailsOutputTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class AssetBundleImportJobDataSourceOverrideParametersTypeDef(TypedDict):
    DataSourceId: str
    Name: NotRequired[str]
    DataSourceParameters: NotRequired[DataSourceParametersUnionTypeDef]
    VpcConnectionProperties: NotRequired[VpcConnectionPropertiesTypeDef]
    SslProperties: NotRequired[SslPropertiesTypeDef]
    Credentials: NotRequired[AssetBundleImportJobDataSourceCredentialsTypeDef]


class CredentialPairTypeDef(TypedDict):
    Username: str
    Password: str
    AlternateDataSourceParameters: NotRequired[Sequence[DataSourceParametersUnionTypeDef]]


class DescribeDashboardSnapshotJobResultResponseTypeDef(TypedDict):
    Arn: str
    JobStatus: SnapshotJobStatusType
    CreatedTime: datetime
    LastUpdatedTime: datetime
    Result: SnapshotJobResultTypeDef
    ErrorInfo: SnapshotJobErrorInfoTypeDef
    RequestId: str
    Status: int
    ResponseMetadata: ResponseMetadataTypeDef


class AnalysisDefaultsTypeDef(TypedDict):
    DefaultNewSheetConfiguration: DefaultNewSheetConfigurationTypeDef


class SectionLayoutConfigurationTypeDef(TypedDict):
    FreeFormLayout: FreeFormSectionLayoutConfigurationUnionTypeDef


class SnapshotConfigurationTypeDef(TypedDict):
    FileGroups: Sequence[SnapshotFileGroupUnionTypeDef]
    DestinationConfiguration: NotRequired[SnapshotDestinationConfigurationUnionTypeDef]
    Parameters: NotRequired[ParametersUnionTypeDef]


ParameterDeclarationUnionTypeDef = Union[
    ParameterDeclarationTypeDef, ParameterDeclarationOutputTypeDef
]


class SetParameterValueConfigurationTypeDef(TypedDict):
    DestinationParameterName: str
    Value: DestinationParameterValueConfigurationUnionTypeDef


class LogicalTableTypeDef(TypedDict):
    Alias: str
    Source: LogicalTableSourceTypeDef
    DataTransforms: NotRequired[Sequence[TransformOperationUnionTypeDef]]


class ColumnHierarchyTypeDef(TypedDict):
    ExplicitHierarchy: NotRequired[ExplicitHierarchyUnionTypeDef]
    DateTimeHierarchy: NotRequired[DateTimeHierarchyUnionTypeDef]
    PredefinedHierarchy: NotRequired[PredefinedHierarchyUnionTypeDef]


class AxisDisplayOptionsTypeDef(TypedDict):
    TickLabelOptions: NotRequired[AxisTickLabelOptionsTypeDef]
    AxisLineVisibility: NotRequired[VisibilityType]
    GridLineVisibility: NotRequired[VisibilityType]
    DataOptions: NotRequired[AxisDataOptionsUnionTypeDef]
    ScrollbarOptions: NotRequired[ScrollBarOptionsTypeDef]
    AxisOffset: NotRequired[str]


class TopicIRContributionAnalysisTypeDef(TypedDict):
    Factors: NotRequired[Sequence[ContributionAnalysisFactorTypeDef]]
    TimeRanges: NotRequired[ContributionAnalysisTimeRangesUnionTypeDef]
    Direction: NotRequired[ContributionAnalysisDirectionType]
    SortType: NotRequired[ContributionAnalysisSortTypeType]


TopicFilterUnionTypeDef = Union[TopicFilterTypeDef, TopicFilterOutputTypeDef]


class SheetImageOutputTypeDef(TypedDict):
    SheetImageId: str
    Source: SheetImageSourceTypeDef
    Scaling: NotRequired[SheetImageScalingConfigurationTypeDef]
    Tooltip: NotRequired[SheetImageTooltipConfigurationTypeDef]
    ImageContentAltText: NotRequired[str]
    Interactions: NotRequired[ImageInteractionOptionsTypeDef]
    Actions: NotRequired[List[ImageCustomActionOutputTypeDef]]


class CustomContentVisualOutputTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[CustomContentConfigurationTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class EmptyVisualOutputTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]


PivotTableFieldOptionsUnionTypeDef = Union[
    PivotTableFieldOptionsTypeDef, PivotTableFieldOptionsOutputTypeDef
]


class TopicReviewedAnswerTypeDef(TypedDict):
    AnswerId: str
    DatasetArn: str
    Question: str
    Arn: NotRequired[str]
    Mir: NotRequired[TopicIROutputTypeDef]
    PrimaryVisual: NotRequired[TopicVisualOutputTypeDef]
    Template: NotRequired[TopicTemplateOutputTypeDef]


DefaultFilterControlOptionsUnionTypeDef = Union[
    DefaultFilterControlOptionsTypeDef, DefaultFilterControlOptionsOutputTypeDef
]
FilterControlUnionTypeDef = Union[FilterControlTypeDef, FilterControlOutputTypeDef]
ParameterControlUnionTypeDef = Union[ParameterControlTypeDef, ParameterControlOutputTypeDef]


class CategoryFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    Configuration: CategoryFilterConfigurationOutputTypeDef
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class CategoryInnerFilterOutputTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Configuration: CategoryFilterConfigurationOutputTypeDef
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class NumericEqualityFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    MatchOperator: NumericEqualityMatchOperatorType
    NullOption: FilterNullOptionType
    Value: NotRequired[float]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]
    ParameterName: NotRequired[str]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class NumericRangeFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    NullOption: FilterNullOptionType
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]
    RangeMinimum: NotRequired[NumericRangeFilterValueTypeDef]
    RangeMaximum: NotRequired[NumericRangeFilterValueTypeDef]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class RelativeDatesFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    AnchorDateConfiguration: AnchorDateConfigurationTypeDef
    TimeGranularity: TimeGranularityType
    RelativeDateType: RelativeDateTypeType
    NullOption: FilterNullOptionType
    MinimumGranularity: NotRequired[TimeGranularityType]
    RelativeDateValue: NotRequired[int]
    ParameterName: NotRequired[str]
    ExcludePeriodConfiguration: NotRequired[ExcludePeriodConfigurationTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class TimeEqualityFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    Value: NotRequired[datetime]
    ParameterName: NotRequired[str]
    TimeGranularity: NotRequired[TimeGranularityType]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class TimeRangeFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    NullOption: FilterNullOptionType
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]
    RangeMinimumValue: NotRequired[TimeRangeFilterValueOutputTypeDef]
    RangeMaximumValue: NotRequired[TimeRangeFilterValueOutputTypeDef]
    ExcludePeriodConfiguration: NotRequired[ExcludePeriodConfigurationTypeDef]
    TimeGranularity: NotRequired[TimeGranularityType]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class TopBottomFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    AggregationSortConfigurations: List[AggregationSortConfigurationTypeDef]
    Limit: NotRequired[int]
    TimeGranularity: NotRequired[TimeGranularityType]
    ParameterName: NotRequired[str]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationOutputTypeDef]


class TableFieldOptionsOutputTypeDef(TypedDict):
    SelectedFieldOptions: NotRequired[List[TableFieldOptionTypeDef]]
    Order: NotRequired[List[str]]
    PinnedFieldOptions: NotRequired[TablePinnedFieldOptionsOutputTypeDef]


class TableFieldOptionsTypeDef(TypedDict):
    SelectedFieldOptions: NotRequired[Sequence[TableFieldOptionTypeDef]]
    Order: NotRequired[Sequence[str]]
    PinnedFieldOptions: NotRequired[TablePinnedFieldOptionsUnionTypeDef]


class GeospatialLayerDefinitionOutputTypeDef(TypedDict):
    PointLayer: NotRequired[GeospatialPointLayerOutputTypeDef]
    LineLayer: NotRequired[GeospatialLineLayerOutputTypeDef]
    PolygonLayer: NotRequired[GeospatialPolygonLayerOutputTypeDef]


GeospatialCircleSymbolStyleUnionTypeDef = Union[
    GeospatialCircleSymbolStyleTypeDef, GeospatialCircleSymbolStyleOutputTypeDef
]
GeospatialLineSymbolStyleUnionTypeDef = Union[
    GeospatialLineSymbolStyleTypeDef, GeospatialLineSymbolStyleOutputTypeDef
]
GeospatialPolygonSymbolStyleUnionTypeDef = Union[
    GeospatialPolygonSymbolStyleTypeDef, GeospatialPolygonSymbolStyleOutputTypeDef
]
PivotTableTotalOptionsUnionTypeDef = Union[
    PivotTableTotalOptionsTypeDef, PivotTableTotalOptionsOutputTypeDef
]


class FilledMapConditionalFormattingOutputTypeDef(TypedDict):
    ConditionalFormattingOptions: List[FilledMapConditionalFormattingOptionOutputTypeDef]


class PivotTableConditionalFormattingOutputTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[
        List[PivotTableConditionalFormattingOptionOutputTypeDef]
    ]


class TableConditionalFormattingOutputTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[List[TableConditionalFormattingOptionOutputTypeDef]]


class GaugeChartArcConditionalFormattingTypeDef(TypedDict):
    ForegroundColor: NotRequired[ConditionalFormattingColorUnionTypeDef]


class GaugeChartPrimaryValueConditionalFormattingTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorUnionTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIActualValueConditionalFormattingTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorUnionTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIComparisonValueConditionalFormattingTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorUnionTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIPrimaryValueConditionalFormattingTypeDef(TypedDict):
    TextColor: NotRequired[ConditionalFormattingColorUnionTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


class KPIProgressBarConditionalFormattingTypeDef(TypedDict):
    ForegroundColor: NotRequired[ConditionalFormattingColorUnionTypeDef]


class ShapeConditionalFormatTypeDef(TypedDict):
    BackgroundColor: ConditionalFormattingColorUnionTypeDef


class TableRowConditionalFormattingTypeDef(TypedDict):
    BackgroundColor: NotRequired[ConditionalFormattingColorUnionTypeDef]
    TextColor: NotRequired[ConditionalFormattingColorUnionTypeDef]


class TextConditionalFormatTypeDef(TypedDict):
    BackgroundColor: NotRequired[ConditionalFormattingColorUnionTypeDef]
    TextColor: NotRequired[ConditionalFormattingColorUnionTypeDef]
    Icon: NotRequired[ConditionalFormattingIconTypeDef]


SheetControlLayoutUnionTypeDef = Union[SheetControlLayoutTypeDef, SheetControlLayoutOutputTypeDef]


class UniqueValuesComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Category: NotRequired[DimensionFieldTypeDef]


class BarChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]
    Colors: NotRequired[List[DimensionFieldTypeDef]]
    SmallMultiples: NotRequired[List[DimensionFieldTypeDef]]


class BarChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    Colors: NotRequired[Sequence[DimensionFieldTypeDef]]
    SmallMultiples: NotRequired[Sequence[DimensionFieldTypeDef]]


class BoxPlotAggregatedFieldWellsOutputTypeDef(TypedDict):
    GroupBy: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]


class BoxPlotAggregatedFieldWellsTypeDef(TypedDict):
    GroupBy: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class ComboChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[List[DimensionFieldTypeDef]]
    BarValues: NotRequired[List[MeasureFieldTypeDef]]
    Colors: NotRequired[List[DimensionFieldTypeDef]]
    LineValues: NotRequired[List[MeasureFieldTypeDef]]


class ComboChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    BarValues: NotRequired[Sequence[MeasureFieldTypeDef]]
    Colors: NotRequired[Sequence[DimensionFieldTypeDef]]
    LineValues: NotRequired[Sequence[MeasureFieldTypeDef]]


class FilledMapAggregatedFieldWellsOutputTypeDef(TypedDict):
    Geospatial: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]


class FilledMapAggregatedFieldWellsTypeDef(TypedDict):
    Geospatial: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class ForecastComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Time: NotRequired[DimensionFieldTypeDef]
    Value: NotRequired[MeasureFieldTypeDef]
    PeriodsForward: NotRequired[int]
    PeriodsBackward: NotRequired[int]
    UpperBoundary: NotRequired[float]
    LowerBoundary: NotRequired[float]
    PredictionInterval: NotRequired[int]
    Seasonality: NotRequired[ForecastComputationSeasonalityType]
    CustomSeasonalityValue: NotRequired[int]


class FunnelChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]


class FunnelChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class GaugeChartFieldWellsOutputTypeDef(TypedDict):
    Values: NotRequired[List[MeasureFieldTypeDef]]
    TargetValues: NotRequired[List[MeasureFieldTypeDef]]


class GaugeChartFieldWellsTypeDef(TypedDict):
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    TargetValues: NotRequired[Sequence[MeasureFieldTypeDef]]


class GeospatialLayerColorFieldOutputTypeDef(TypedDict):
    ColorDimensionsFields: NotRequired[List[DimensionFieldTypeDef]]
    ColorValuesFields: NotRequired[List[MeasureFieldTypeDef]]


class GeospatialLayerColorFieldTypeDef(TypedDict):
    ColorDimensionsFields: NotRequired[Sequence[DimensionFieldTypeDef]]
    ColorValuesFields: NotRequired[Sequence[MeasureFieldTypeDef]]


class GeospatialMapAggregatedFieldWellsOutputTypeDef(TypedDict):
    Geospatial: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]
    Colors: NotRequired[List[DimensionFieldTypeDef]]


class GeospatialMapAggregatedFieldWellsTypeDef(TypedDict):
    Geospatial: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    Colors: NotRequired[Sequence[DimensionFieldTypeDef]]


class GrowthRateComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Time: NotRequired[DimensionFieldTypeDef]
    Value: NotRequired[MeasureFieldTypeDef]
    PeriodSize: NotRequired[int]


class HeatMapAggregatedFieldWellsOutputTypeDef(TypedDict):
    Rows: NotRequired[List[DimensionFieldTypeDef]]
    Columns: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]


class HeatMapAggregatedFieldWellsTypeDef(TypedDict):
    Rows: NotRequired[Sequence[DimensionFieldTypeDef]]
    Columns: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class HistogramAggregatedFieldWellsOutputTypeDef(TypedDict):
    Values: NotRequired[List[MeasureFieldTypeDef]]


class HistogramAggregatedFieldWellsTypeDef(TypedDict):
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class KPIFieldWellsOutputTypeDef(TypedDict):
    Values: NotRequired[List[MeasureFieldTypeDef]]
    TargetValues: NotRequired[List[MeasureFieldTypeDef]]
    TrendGroups: NotRequired[List[DimensionFieldTypeDef]]


class KPIFieldWellsTypeDef(TypedDict):
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    TargetValues: NotRequired[Sequence[MeasureFieldTypeDef]]
    TrendGroups: NotRequired[Sequence[DimensionFieldTypeDef]]


class LineChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]
    Colors: NotRequired[List[DimensionFieldTypeDef]]
    SmallMultiples: NotRequired[List[DimensionFieldTypeDef]]


class LineChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    Colors: NotRequired[Sequence[DimensionFieldTypeDef]]
    SmallMultiples: NotRequired[Sequence[DimensionFieldTypeDef]]


MaximumMinimumComputationTypeDef = TypedDict(
    "MaximumMinimumComputationTypeDef",
    {
        "ComputationId": str,
        "Type": MaximumMinimumComputationTypeType,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
    },
)


class MetricComparisonComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Time: NotRequired[DimensionFieldTypeDef]
    FromValue: NotRequired[MeasureFieldTypeDef]
    TargetValue: NotRequired[MeasureFieldTypeDef]


class PeriodOverPeriodComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Time: NotRequired[DimensionFieldTypeDef]
    Value: NotRequired[MeasureFieldTypeDef]


class PeriodToDateComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Time: NotRequired[DimensionFieldTypeDef]
    Value: NotRequired[MeasureFieldTypeDef]
    PeriodTimeGranularity: NotRequired[TimeGranularityType]


class PieChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]
    SmallMultiples: NotRequired[List[DimensionFieldTypeDef]]


class PieChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    SmallMultiples: NotRequired[Sequence[DimensionFieldTypeDef]]


class PivotTableAggregatedFieldWellsOutputTypeDef(TypedDict):
    Rows: NotRequired[List[DimensionFieldTypeDef]]
    Columns: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]


class PivotTableAggregatedFieldWellsTypeDef(TypedDict):
    Rows: NotRequired[Sequence[DimensionFieldTypeDef]]
    Columns: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class RadarChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Category: NotRequired[List[DimensionFieldTypeDef]]
    Color: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]


class RadarChartAggregatedFieldWellsTypeDef(TypedDict):
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Color: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


class SankeyDiagramAggregatedFieldWellsOutputTypeDef(TypedDict):
    Source: NotRequired[List[DimensionFieldTypeDef]]
    Destination: NotRequired[List[DimensionFieldTypeDef]]
    Weight: NotRequired[List[MeasureFieldTypeDef]]


class SankeyDiagramAggregatedFieldWellsTypeDef(TypedDict):
    Source: NotRequired[Sequence[DimensionFieldTypeDef]]
    Destination: NotRequired[Sequence[DimensionFieldTypeDef]]
    Weight: NotRequired[Sequence[MeasureFieldTypeDef]]


class ScatterPlotCategoricallyAggregatedFieldWellsOutputTypeDef(TypedDict):
    XAxis: NotRequired[List[MeasureFieldTypeDef]]
    YAxis: NotRequired[List[MeasureFieldTypeDef]]
    Category: NotRequired[List[DimensionFieldTypeDef]]
    Size: NotRequired[List[MeasureFieldTypeDef]]
    Label: NotRequired[List[DimensionFieldTypeDef]]


class ScatterPlotCategoricallyAggregatedFieldWellsTypeDef(TypedDict):
    XAxis: NotRequired[Sequence[MeasureFieldTypeDef]]
    YAxis: NotRequired[Sequence[MeasureFieldTypeDef]]
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Size: NotRequired[Sequence[MeasureFieldTypeDef]]
    Label: NotRequired[Sequence[DimensionFieldTypeDef]]


class ScatterPlotUnaggregatedFieldWellsOutputTypeDef(TypedDict):
    XAxis: NotRequired[List[DimensionFieldTypeDef]]
    YAxis: NotRequired[List[DimensionFieldTypeDef]]
    Size: NotRequired[List[MeasureFieldTypeDef]]
    Category: NotRequired[List[DimensionFieldTypeDef]]
    Label: NotRequired[List[DimensionFieldTypeDef]]


class ScatterPlotUnaggregatedFieldWellsTypeDef(TypedDict):
    XAxis: NotRequired[Sequence[DimensionFieldTypeDef]]
    YAxis: NotRequired[Sequence[DimensionFieldTypeDef]]
    Size: NotRequired[Sequence[MeasureFieldTypeDef]]
    Category: NotRequired[Sequence[DimensionFieldTypeDef]]
    Label: NotRequired[Sequence[DimensionFieldTypeDef]]


class TableAggregatedFieldWellsOutputTypeDef(TypedDict):
    GroupBy: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]


class TableAggregatedFieldWellsTypeDef(TypedDict):
    GroupBy: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]


TopBottomMoversComputationTypeDef = TypedDict(
    "TopBottomMoversComputationTypeDef",
    {
        "ComputationId": str,
        "Type": TopBottomComputationTypeType,
        "Name": NotRequired[str],
        "Time": NotRequired[DimensionFieldTypeDef],
        "Category": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
        "MoverSize": NotRequired[int],
        "SortOrder": NotRequired[TopBottomSortOrderType],
    },
)
TopBottomRankedComputationTypeDef = TypedDict(
    "TopBottomRankedComputationTypeDef",
    {
        "ComputationId": str,
        "Type": TopBottomComputationTypeType,
        "Name": NotRequired[str],
        "Category": NotRequired[DimensionFieldTypeDef],
        "Value": NotRequired[MeasureFieldTypeDef],
        "ResultSize": NotRequired[int],
    },
)


class TotalAggregationComputationTypeDef(TypedDict):
    ComputationId: str
    Name: NotRequired[str]
    Value: NotRequired[MeasureFieldTypeDef]


class TreeMapAggregatedFieldWellsOutputTypeDef(TypedDict):
    Groups: NotRequired[List[DimensionFieldTypeDef]]
    Sizes: NotRequired[List[MeasureFieldTypeDef]]
    Colors: NotRequired[List[MeasureFieldTypeDef]]


class TreeMapAggregatedFieldWellsTypeDef(TypedDict):
    Groups: NotRequired[Sequence[DimensionFieldTypeDef]]
    Sizes: NotRequired[Sequence[MeasureFieldTypeDef]]
    Colors: NotRequired[Sequence[MeasureFieldTypeDef]]


class WaterfallChartAggregatedFieldWellsOutputTypeDef(TypedDict):
    Categories: NotRequired[List[DimensionFieldTypeDef]]
    Values: NotRequired[List[MeasureFieldTypeDef]]
    Breakdowns: NotRequired[List[DimensionFieldTypeDef]]


class WaterfallChartAggregatedFieldWellsTypeDef(TypedDict):
    Categories: NotRequired[Sequence[DimensionFieldTypeDef]]
    Values: NotRequired[Sequence[MeasureFieldTypeDef]]
    Breakdowns: NotRequired[Sequence[DimensionFieldTypeDef]]


class WordCloudAggregatedFieldWellsOutputTypeDef(TypedDict):
    GroupBy: NotRequired[List[DimensionFieldTypeDef]]
    Size: NotRequired[List[MeasureFieldTypeDef]]


class WordCloudAggregatedFieldWellsTypeDef(TypedDict):
    GroupBy: NotRequired[Sequence[DimensionFieldTypeDef]]
    Size: NotRequired[Sequence[MeasureFieldTypeDef]]


ColumnConfigurationUnionTypeDef = Union[
    ColumnConfigurationTypeDef, ColumnConfigurationOutputTypeDef
]


class PluginVisualFieldWellOutputTypeDef(TypedDict):
    AxisName: NotRequired[PluginVisualAxisNameType]
    Dimensions: NotRequired[List[DimensionFieldTypeDef]]
    Measures: NotRequired[List[MeasureFieldTypeDef]]
    Unaggregated: NotRequired[List[UnaggregatedFieldTypeDef]]


class PluginVisualFieldWellTypeDef(TypedDict):
    AxisName: NotRequired[PluginVisualAxisNameType]
    Dimensions: NotRequired[Sequence[DimensionFieldTypeDef]]
    Measures: NotRequired[Sequence[MeasureFieldTypeDef]]
    Unaggregated: NotRequired[Sequence[UnaggregatedFieldTypeDef]]


class TableUnaggregatedFieldWellsOutputTypeDef(TypedDict):
    Values: NotRequired[List[UnaggregatedFieldTypeDef]]


class TableUnaggregatedFieldWellsTypeDef(TypedDict):
    Values: NotRequired[Sequence[UnaggregatedFieldTypeDef]]


class BodySectionConfigurationOutputTypeDef(TypedDict):
    SectionId: str
    Content: BodySectionContentOutputTypeDef
    Style: NotRequired[SectionStyleTypeDef]
    PageBreakConfiguration: NotRequired[SectionPageBreakConfigurationTypeDef]
    RepeatConfiguration: NotRequired[BodySectionRepeatConfigurationOutputTypeDef]


BodySectionRepeatDimensionConfigurationUnionTypeDef = Union[
    BodySectionRepeatDimensionConfigurationTypeDef,
    BodySectionRepeatDimensionConfigurationOutputTypeDef,
]


class PluginVisualSortConfigurationTypeDef(TypedDict):
    PluginVisualTableQuerySort: NotRequired[PluginVisualTableQuerySortUnionTypeDef]


PivotFieldSortOptionsUnionTypeDef = Union[
    PivotFieldSortOptionsTypeDef, PivotFieldSortOptionsOutputTypeDef
]


class TooltipOptionsTypeDef(TypedDict):
    TooltipVisibility: NotRequired[VisibilityType]
    SelectedTooltipType: NotRequired[SelectedTooltipTypeType]
    FieldBasedTooltip: NotRequired[FieldBasedTooltipUnionTypeDef]


AssetBundleImportJobDataSourceOverrideParametersUnionTypeDef = Union[
    AssetBundleImportJobDataSourceOverrideParametersTypeDef,
    AssetBundleImportJobDataSourceOverrideParametersOutputTypeDef,
]


class DataSourceCredentialsTypeDef(TypedDict):
    CredentialPair: NotRequired[CredentialPairTypeDef]
    CopySourceArn: NotRequired[str]
    SecretArn: NotRequired[str]


SectionLayoutConfigurationUnionTypeDef = Union[
    SectionLayoutConfigurationTypeDef, SectionLayoutConfigurationOutputTypeDef
]


class StartDashboardSnapshotJobRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    SnapshotJobId: str
    UserConfiguration: SnapshotUserConfigurationTypeDef
    SnapshotConfiguration: SnapshotConfigurationTypeDef


SetParameterValueConfigurationUnionTypeDef = Union[
    SetParameterValueConfigurationTypeDef, SetParameterValueConfigurationOutputTypeDef
]
LogicalTableUnionTypeDef = Union[LogicalTableTypeDef, LogicalTableOutputTypeDef]


class UpdateDataSetRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    Name: str
    PhysicalTableMap: Mapping[str, PhysicalTableTypeDef]
    ImportMode: DataSetImportModeType
    LogicalTableMap: NotRequired[Mapping[str, LogicalTableTypeDef]]
    ColumnGroups: NotRequired[Sequence[ColumnGroupTypeDef]]
    FieldFolders: NotRequired[Mapping[str, FieldFolderTypeDef]]
    RowLevelPermissionDataSet: NotRequired[RowLevelPermissionDataSetTypeDef]
    RowLevelPermissionTagConfiguration: NotRequired[RowLevelPermissionTagConfigurationTypeDef]
    ColumnLevelPermissionRules: NotRequired[Sequence[ColumnLevelPermissionRuleTypeDef]]
    DataSetUsageConfiguration: NotRequired[DataSetUsageConfigurationTypeDef]
    DatasetParameters: NotRequired[Sequence[DatasetParameterTypeDef]]


ColumnHierarchyUnionTypeDef = Union[ColumnHierarchyTypeDef, ColumnHierarchyOutputTypeDef]
AxisDisplayOptionsUnionTypeDef = Union[AxisDisplayOptionsTypeDef, AxisDisplayOptionsOutputTypeDef]
TopicIRContributionAnalysisUnionTypeDef = Union[
    TopicIRContributionAnalysisTypeDef, TopicIRContributionAnalysisOutputTypeDef
]


class DatasetMetadataTypeDef(TypedDict):
    DatasetArn: str
    DatasetName: NotRequired[str]
    DatasetDescription: NotRequired[str]
    DataAggregation: NotRequired[DataAggregationTypeDef]
    Filters: NotRequired[Sequence[TopicFilterUnionTypeDef]]
    Columns: NotRequired[Sequence[TopicColumnUnionTypeDef]]
    CalculatedFields: NotRequired[Sequence[TopicCalculatedFieldUnionTypeDef]]
    NamedEntities: NotRequired[Sequence[TopicNamedEntityUnionTypeDef]]


class SheetTypeDef(TypedDict):
    SheetId: NotRequired[str]
    Name: NotRequired[str]
    Images: NotRequired[List[SheetImageOutputTypeDef]]


class ListTopicReviewedAnswersResponseTypeDef(TypedDict):
    TopicId: str
    TopicArn: str
    Answers: List[TopicReviewedAnswerTypeDef]
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DefaultFilterControlConfigurationTypeDef(TypedDict):
    Title: str
    ControlOptions: DefaultFilterControlOptionsUnionTypeDef


class InnerFilterOutputTypeDef(TypedDict):
    CategoryInnerFilter: NotRequired[CategoryInnerFilterOutputTypeDef]


TableFieldOptionsUnionTypeDef = Union[TableFieldOptionsTypeDef, TableFieldOptionsOutputTypeDef]


class GeospatialPointStyleTypeDef(TypedDict):
    CircleSymbolStyle: NotRequired[GeospatialCircleSymbolStyleUnionTypeDef]


class GeospatialLineStyleTypeDef(TypedDict):
    LineSymbolStyle: NotRequired[GeospatialLineSymbolStyleUnionTypeDef]


class GeospatialPolygonStyleTypeDef(TypedDict):
    PolygonSymbolStyle: NotRequired[GeospatialPolygonSymbolStyleUnionTypeDef]


GaugeChartArcConditionalFormattingUnionTypeDef = Union[
    GaugeChartArcConditionalFormattingTypeDef, GaugeChartArcConditionalFormattingOutputTypeDef
]
GaugeChartPrimaryValueConditionalFormattingUnionTypeDef = Union[
    GaugeChartPrimaryValueConditionalFormattingTypeDef,
    GaugeChartPrimaryValueConditionalFormattingOutputTypeDef,
]
KPIActualValueConditionalFormattingUnionTypeDef = Union[
    KPIActualValueConditionalFormattingTypeDef, KPIActualValueConditionalFormattingOutputTypeDef
]
KPIComparisonValueConditionalFormattingUnionTypeDef = Union[
    KPIComparisonValueConditionalFormattingTypeDef,
    KPIComparisonValueConditionalFormattingOutputTypeDef,
]
KPIPrimaryValueConditionalFormattingUnionTypeDef = Union[
    KPIPrimaryValueConditionalFormattingTypeDef, KPIPrimaryValueConditionalFormattingOutputTypeDef
]
KPIProgressBarConditionalFormattingUnionTypeDef = Union[
    KPIProgressBarConditionalFormattingTypeDef, KPIProgressBarConditionalFormattingOutputTypeDef
]
ShapeConditionalFormatUnionTypeDef = Union[
    ShapeConditionalFormatTypeDef, ShapeConditionalFormatOutputTypeDef
]
TableRowConditionalFormattingUnionTypeDef = Union[
    TableRowConditionalFormattingTypeDef, TableRowConditionalFormattingOutputTypeDef
]
TextConditionalFormatUnionTypeDef = Union[
    TextConditionalFormatTypeDef, TextConditionalFormatOutputTypeDef
]


class BarChartFieldWellsOutputTypeDef(TypedDict):
    BarChartAggregatedFieldWells: NotRequired[BarChartAggregatedFieldWellsOutputTypeDef]


BarChartAggregatedFieldWellsUnionTypeDef = Union[
    BarChartAggregatedFieldWellsTypeDef, BarChartAggregatedFieldWellsOutputTypeDef
]


class BoxPlotFieldWellsOutputTypeDef(TypedDict):
    BoxPlotAggregatedFieldWells: NotRequired[BoxPlotAggregatedFieldWellsOutputTypeDef]


BoxPlotAggregatedFieldWellsUnionTypeDef = Union[
    BoxPlotAggregatedFieldWellsTypeDef, BoxPlotAggregatedFieldWellsOutputTypeDef
]


class ComboChartFieldWellsOutputTypeDef(TypedDict):
    ComboChartAggregatedFieldWells: NotRequired[ComboChartAggregatedFieldWellsOutputTypeDef]


ComboChartAggregatedFieldWellsUnionTypeDef = Union[
    ComboChartAggregatedFieldWellsTypeDef, ComboChartAggregatedFieldWellsOutputTypeDef
]


class FilledMapFieldWellsOutputTypeDef(TypedDict):
    FilledMapAggregatedFieldWells: NotRequired[FilledMapAggregatedFieldWellsOutputTypeDef]


FilledMapAggregatedFieldWellsUnionTypeDef = Union[
    FilledMapAggregatedFieldWellsTypeDef, FilledMapAggregatedFieldWellsOutputTypeDef
]


class FunnelChartFieldWellsOutputTypeDef(TypedDict):
    FunnelChartAggregatedFieldWells: NotRequired[FunnelChartAggregatedFieldWellsOutputTypeDef]


FunnelChartAggregatedFieldWellsUnionTypeDef = Union[
    FunnelChartAggregatedFieldWellsTypeDef, FunnelChartAggregatedFieldWellsOutputTypeDef
]


class GaugeChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[GaugeChartFieldWellsOutputTypeDef]
    GaugeChartOptions: NotRequired[GaugeChartOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    TooltipOptions: NotRequired[TooltipOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    ColorConfiguration: NotRequired[GaugeChartColorConfigurationTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


GaugeChartFieldWellsUnionTypeDef = Union[
    GaugeChartFieldWellsTypeDef, GaugeChartFieldWellsOutputTypeDef
]


class GeospatialLayerJoinDefinitionOutputTypeDef(TypedDict):
    ShapeKeyField: NotRequired[str]
    DatasetKeyField: NotRequired[UnaggregatedFieldTypeDef]
    ColorField: NotRequired[GeospatialLayerColorFieldOutputTypeDef]


GeospatialLayerColorFieldUnionTypeDef = Union[
    GeospatialLayerColorFieldTypeDef, GeospatialLayerColorFieldOutputTypeDef
]


class GeospatialMapFieldWellsOutputTypeDef(TypedDict):
    GeospatialMapAggregatedFieldWells: NotRequired[GeospatialMapAggregatedFieldWellsOutputTypeDef]


GeospatialMapAggregatedFieldWellsUnionTypeDef = Union[
    GeospatialMapAggregatedFieldWellsTypeDef, GeospatialMapAggregatedFieldWellsOutputTypeDef
]


class HeatMapFieldWellsOutputTypeDef(TypedDict):
    HeatMapAggregatedFieldWells: NotRequired[HeatMapAggregatedFieldWellsOutputTypeDef]


HeatMapAggregatedFieldWellsUnionTypeDef = Union[
    HeatMapAggregatedFieldWellsTypeDef, HeatMapAggregatedFieldWellsOutputTypeDef
]


class HistogramFieldWellsOutputTypeDef(TypedDict):
    HistogramAggregatedFieldWells: NotRequired[HistogramAggregatedFieldWellsOutputTypeDef]


HistogramAggregatedFieldWellsUnionTypeDef = Union[
    HistogramAggregatedFieldWellsTypeDef, HistogramAggregatedFieldWellsOutputTypeDef
]


class KPIConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[KPIFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[KPISortConfigurationOutputTypeDef]
    KPIOptions: NotRequired[KPIOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


KPIFieldWellsUnionTypeDef = Union[KPIFieldWellsTypeDef, KPIFieldWellsOutputTypeDef]


class LineChartFieldWellsOutputTypeDef(TypedDict):
    LineChartAggregatedFieldWells: NotRequired[LineChartAggregatedFieldWellsOutputTypeDef]


LineChartAggregatedFieldWellsUnionTypeDef = Union[
    LineChartAggregatedFieldWellsTypeDef, LineChartAggregatedFieldWellsOutputTypeDef
]


class PieChartFieldWellsOutputTypeDef(TypedDict):
    PieChartAggregatedFieldWells: NotRequired[PieChartAggregatedFieldWellsOutputTypeDef]


PieChartAggregatedFieldWellsUnionTypeDef = Union[
    PieChartAggregatedFieldWellsTypeDef, PieChartAggregatedFieldWellsOutputTypeDef
]


class PivotTableFieldWellsOutputTypeDef(TypedDict):
    PivotTableAggregatedFieldWells: NotRequired[PivotTableAggregatedFieldWellsOutputTypeDef]


PivotTableAggregatedFieldWellsUnionTypeDef = Union[
    PivotTableAggregatedFieldWellsTypeDef, PivotTableAggregatedFieldWellsOutputTypeDef
]


class RadarChartFieldWellsOutputTypeDef(TypedDict):
    RadarChartAggregatedFieldWells: NotRequired[RadarChartAggregatedFieldWellsOutputTypeDef]


RadarChartAggregatedFieldWellsUnionTypeDef = Union[
    RadarChartAggregatedFieldWellsTypeDef, RadarChartAggregatedFieldWellsOutputTypeDef
]


class SankeyDiagramFieldWellsOutputTypeDef(TypedDict):
    SankeyDiagramAggregatedFieldWells: NotRequired[SankeyDiagramAggregatedFieldWellsOutputTypeDef]


SankeyDiagramAggregatedFieldWellsUnionTypeDef = Union[
    SankeyDiagramAggregatedFieldWellsTypeDef, SankeyDiagramAggregatedFieldWellsOutputTypeDef
]
ScatterPlotCategoricallyAggregatedFieldWellsUnionTypeDef = Union[
    ScatterPlotCategoricallyAggregatedFieldWellsTypeDef,
    ScatterPlotCategoricallyAggregatedFieldWellsOutputTypeDef,
]


class ScatterPlotFieldWellsOutputTypeDef(TypedDict):
    ScatterPlotCategoricallyAggregatedFieldWells: NotRequired[
        ScatterPlotCategoricallyAggregatedFieldWellsOutputTypeDef
    ]
    ScatterPlotUnaggregatedFieldWells: NotRequired[ScatterPlotUnaggregatedFieldWellsOutputTypeDef]


ScatterPlotUnaggregatedFieldWellsUnionTypeDef = Union[
    ScatterPlotUnaggregatedFieldWellsTypeDef, ScatterPlotUnaggregatedFieldWellsOutputTypeDef
]
TableAggregatedFieldWellsUnionTypeDef = Union[
    TableAggregatedFieldWellsTypeDef, TableAggregatedFieldWellsOutputTypeDef
]


class ComputationTypeDef(TypedDict):
    TopBottomRanked: NotRequired[TopBottomRankedComputationTypeDef]
    TopBottomMovers: NotRequired[TopBottomMoversComputationTypeDef]
    TotalAggregation: NotRequired[TotalAggregationComputationTypeDef]
    MaximumMinimum: NotRequired[MaximumMinimumComputationTypeDef]
    MetricComparison: NotRequired[MetricComparisonComputationTypeDef]
    PeriodOverPeriod: NotRequired[PeriodOverPeriodComputationTypeDef]
    PeriodToDate: NotRequired[PeriodToDateComputationTypeDef]
    GrowthRate: NotRequired[GrowthRateComputationTypeDef]
    UniqueValues: NotRequired[UniqueValuesComputationTypeDef]
    Forecast: NotRequired[ForecastComputationTypeDef]


class TreeMapFieldWellsOutputTypeDef(TypedDict):
    TreeMapAggregatedFieldWells: NotRequired[TreeMapAggregatedFieldWellsOutputTypeDef]


TreeMapAggregatedFieldWellsUnionTypeDef = Union[
    TreeMapAggregatedFieldWellsTypeDef, TreeMapAggregatedFieldWellsOutputTypeDef
]


class WaterfallChartFieldWellsOutputTypeDef(TypedDict):
    WaterfallChartAggregatedFieldWells: NotRequired[WaterfallChartAggregatedFieldWellsOutputTypeDef]


WaterfallChartAggregatedFieldWellsUnionTypeDef = Union[
    WaterfallChartAggregatedFieldWellsTypeDef, WaterfallChartAggregatedFieldWellsOutputTypeDef
]


class WordCloudFieldWellsOutputTypeDef(TypedDict):
    WordCloudAggregatedFieldWells: NotRequired[WordCloudAggregatedFieldWellsOutputTypeDef]


WordCloudAggregatedFieldWellsUnionTypeDef = Union[
    WordCloudAggregatedFieldWellsTypeDef, WordCloudAggregatedFieldWellsOutputTypeDef
]


class PluginVisualConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[List[PluginVisualFieldWellOutputTypeDef]]
    VisualOptions: NotRequired[PluginVisualOptionsOutputTypeDef]
    SortConfiguration: NotRequired[PluginVisualSortConfigurationOutputTypeDef]


PluginVisualFieldWellUnionTypeDef = Union[
    PluginVisualFieldWellTypeDef, PluginVisualFieldWellOutputTypeDef
]


class TableFieldWellsOutputTypeDef(TypedDict):
    TableAggregatedFieldWells: NotRequired[TableAggregatedFieldWellsOutputTypeDef]
    TableUnaggregatedFieldWells: NotRequired[TableUnaggregatedFieldWellsOutputTypeDef]


TableUnaggregatedFieldWellsUnionTypeDef = Union[
    TableUnaggregatedFieldWellsTypeDef, TableUnaggregatedFieldWellsOutputTypeDef
]


class SectionBasedLayoutConfigurationOutputTypeDef(TypedDict):
    HeaderSections: List[HeaderFooterSectionConfigurationOutputTypeDef]
    BodySections: List[BodySectionConfigurationOutputTypeDef]
    FooterSections: List[HeaderFooterSectionConfigurationOutputTypeDef]
    CanvasSizeOptions: SectionBasedLayoutCanvasSizeOptionsTypeDef


class BodySectionRepeatConfigurationTypeDef(TypedDict):
    DimensionConfigurations: NotRequired[
        Sequence[BodySectionRepeatDimensionConfigurationUnionTypeDef]
    ]
    PageBreakConfiguration: NotRequired[BodySectionRepeatPageBreakConfigurationTypeDef]
    NonRepeatingVisuals: NotRequired[Sequence[str]]


PluginVisualSortConfigurationUnionTypeDef = Union[
    PluginVisualSortConfigurationTypeDef, PluginVisualSortConfigurationOutputTypeDef
]


class PivotTableSortConfigurationTypeDef(TypedDict):
    FieldSortOptions: NotRequired[Sequence[PivotFieldSortOptionsUnionTypeDef]]


TooltipOptionsUnionTypeDef = Union[TooltipOptionsTypeDef, TooltipOptionsOutputTypeDef]


class AssetBundleImportJobOverrideParametersTypeDef(TypedDict):
    ResourceIdOverrideConfiguration: NotRequired[
        AssetBundleImportJobResourceIdOverrideConfigurationTypeDef
    ]
    VPCConnections: NotRequired[
        Sequence[AssetBundleImportJobVPCConnectionOverrideParametersUnionTypeDef]
    ]
    RefreshSchedules: NotRequired[
        Sequence[AssetBundleImportJobRefreshScheduleOverrideParametersUnionTypeDef]
    ]
    DataSources: NotRequired[Sequence[AssetBundleImportJobDataSourceOverrideParametersUnionTypeDef]]
    DataSets: NotRequired[Sequence[AssetBundleImportJobDataSetOverrideParametersTypeDef]]
    Themes: NotRequired[Sequence[AssetBundleImportJobThemeOverrideParametersTypeDef]]
    Analyses: NotRequired[Sequence[AssetBundleImportJobAnalysisOverrideParametersTypeDef]]
    Dashboards: NotRequired[Sequence[AssetBundleImportJobDashboardOverrideParametersTypeDef]]
    Folders: NotRequired[Sequence[AssetBundleImportJobFolderOverrideParametersTypeDef]]


CreateDataSourceRequestRequestTypeDef = TypedDict(
    "CreateDataSourceRequestRequestTypeDef",
    {
        "AwsAccountId": str,
        "DataSourceId": str,
        "Name": str,
        "Type": DataSourceTypeType,
        "DataSourceParameters": NotRequired[DataSourceParametersTypeDef],
        "Credentials": NotRequired[DataSourceCredentialsTypeDef],
        "Permissions": NotRequired[Sequence[ResourcePermissionTypeDef]],
        "VpcConnectionProperties": NotRequired[VpcConnectionPropertiesTypeDef],
        "SslProperties": NotRequired[SslPropertiesTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "FolderArns": NotRequired[Sequence[str]],
    },
)


class UpdateDataSourceRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSourceId: str
    Name: str
    DataSourceParameters: NotRequired[DataSourceParametersTypeDef]
    Credentials: NotRequired[DataSourceCredentialsTypeDef]
    VpcConnectionProperties: NotRequired[VpcConnectionPropertiesTypeDef]
    SslProperties: NotRequired[SslPropertiesTypeDef]


class BodySectionContentTypeDef(TypedDict):
    Layout: NotRequired[SectionLayoutConfigurationUnionTypeDef]


class HeaderFooterSectionConfigurationTypeDef(TypedDict):
    SectionId: str
    Layout: SectionLayoutConfigurationUnionTypeDef
    Style: NotRequired[SectionStyleTypeDef]


class CustomActionSetParametersOperationTypeDef(TypedDict):
    ParameterValueConfigurations: Sequence[SetParameterValueConfigurationUnionTypeDef]


class CreateDataSetRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DataSetId: str
    Name: str
    PhysicalTableMap: Mapping[str, PhysicalTableUnionTypeDef]
    ImportMode: DataSetImportModeType
    LogicalTableMap: NotRequired[Mapping[str, LogicalTableUnionTypeDef]]
    ColumnGroups: NotRequired[Sequence[ColumnGroupUnionTypeDef]]
    FieldFolders: NotRequired[Mapping[str, FieldFolderUnionTypeDef]]
    Permissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    RowLevelPermissionDataSet: NotRequired[RowLevelPermissionDataSetTypeDef]
    RowLevelPermissionTagConfiguration: NotRequired[RowLevelPermissionTagConfigurationTypeDef]
    ColumnLevelPermissionRules: NotRequired[Sequence[ColumnLevelPermissionRuleUnionTypeDef]]
    Tags: NotRequired[Sequence[TagTypeDef]]
    DataSetUsageConfiguration: NotRequired[DataSetUsageConfigurationTypeDef]
    DatasetParameters: NotRequired[Sequence[DatasetParameterUnionTypeDef]]
    FolderArns: NotRequired[Sequence[str]]


class LineSeriesAxisDisplayOptionsTypeDef(TypedDict):
    AxisOptions: NotRequired[AxisDisplayOptionsUnionTypeDef]
    MissingDataConfigurations: NotRequired[Sequence[MissingDataConfigurationTypeDef]]


class TopicIRTypeDef(TypedDict):
    Metrics: NotRequired[Sequence[TopicIRMetricUnionTypeDef]]
    GroupByList: NotRequired[Sequence[TopicIRGroupByTypeDef]]
    Filters: NotRequired[Sequence[Sequence[TopicIRFilterOptionUnionTypeDef]]]
    Sort: NotRequired[TopicSortClauseTypeDef]
    ContributionAnalysis: NotRequired[TopicIRContributionAnalysisUnionTypeDef]
    Visual: NotRequired[VisualOptionsTypeDef]


DatasetMetadataUnionTypeDef = Union[DatasetMetadataTypeDef, DatasetMetadataOutputTypeDef]


class AnalysisTypeDef(TypedDict):
    AnalysisId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Status: NotRequired[ResourceStatusType]
    Errors: NotRequired[List[AnalysisErrorTypeDef]]
    DataSetArns: NotRequired[List[str]]
    ThemeArn: NotRequired[str]
    CreatedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    Sheets: NotRequired[List[SheetTypeDef]]


class DashboardVersionTypeDef(TypedDict):
    CreatedTime: NotRequired[datetime]
    Errors: NotRequired[List[DashboardErrorTypeDef]]
    VersionNumber: NotRequired[int]
    Status: NotRequired[ResourceStatusType]
    Arn: NotRequired[str]
    SourceEntityArn: NotRequired[str]
    DataSetArns: NotRequired[List[str]]
    Description: NotRequired[str]
    ThemeArn: NotRequired[str]
    Sheets: NotRequired[List[SheetTypeDef]]


class TemplateVersionTypeDef(TypedDict):
    CreatedTime: NotRequired[datetime]
    Errors: NotRequired[List[TemplateErrorTypeDef]]
    VersionNumber: NotRequired[int]
    Status: NotRequired[ResourceStatusType]
    DataSetConfigurations: NotRequired[List[DataSetConfigurationOutputTypeDef]]
    Description: NotRequired[str]
    SourceEntityArn: NotRequired[str]
    ThemeArn: NotRequired[str]
    Sheets: NotRequired[List[SheetTypeDef]]


DefaultFilterControlConfigurationUnionTypeDef = Union[
    DefaultFilterControlConfigurationTypeDef, DefaultFilterControlConfigurationOutputTypeDef
]


class NestedFilterOutputTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    IncludeInnerSet: bool
    InnerFilter: InnerFilterOutputTypeDef


GeospatialPointStyleUnionTypeDef = Union[
    GeospatialPointStyleTypeDef, GeospatialPointStyleOutputTypeDef
]
GeospatialLineStyleUnionTypeDef = Union[
    GeospatialLineStyleTypeDef, GeospatialLineStyleOutputTypeDef
]
GeospatialPolygonStyleUnionTypeDef = Union[
    GeospatialPolygonStyleTypeDef, GeospatialPolygonStyleOutputTypeDef
]


class GaugeChartConditionalFormattingOptionTypeDef(TypedDict):
    PrimaryValue: NotRequired[GaugeChartPrimaryValueConditionalFormattingUnionTypeDef]
    Arc: NotRequired[GaugeChartArcConditionalFormattingUnionTypeDef]


class KPIConditionalFormattingOptionTypeDef(TypedDict):
    PrimaryValue: NotRequired[KPIPrimaryValueConditionalFormattingUnionTypeDef]
    ProgressBar: NotRequired[KPIProgressBarConditionalFormattingUnionTypeDef]
    ActualValue: NotRequired[KPIActualValueConditionalFormattingUnionTypeDef]
    ComparisonValue: NotRequired[KPIComparisonValueConditionalFormattingUnionTypeDef]


class FilledMapShapeConditionalFormattingTypeDef(TypedDict):
    FieldId: str
    Format: NotRequired[ShapeConditionalFormatUnionTypeDef]


class PivotTableCellConditionalFormattingTypeDef(TypedDict):
    FieldId: str
    TextFormat: NotRequired[TextConditionalFormatUnionTypeDef]
    Scope: NotRequired[PivotTableConditionalFormattingScopeTypeDef]
    Scopes: NotRequired[Sequence[PivotTableConditionalFormattingScopeTypeDef]]


class TableCellConditionalFormattingTypeDef(TypedDict):
    FieldId: str
    TextFormat: NotRequired[TextConditionalFormatUnionTypeDef]


class BarChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[BarChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[BarChartSortConfigurationOutputTypeDef]
    Orientation: NotRequired[BarChartOrientationType]
    BarsArrangement: NotRequired[BarsArrangementType]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    SmallMultiplesOptions: NotRequired[SmallMultiplesOptionsTypeDef]
    CategoryAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ValueAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    ReferenceLines: NotRequired[List[ReferenceLineTypeDef]]
    ContributionAnalysisDefaults: NotRequired[List[ContributionAnalysisDefaultOutputTypeDef]]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class BarChartFieldWellsTypeDef(TypedDict):
    BarChartAggregatedFieldWells: NotRequired[BarChartAggregatedFieldWellsUnionTypeDef]


class BoxPlotChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[BoxPlotFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[BoxPlotSortConfigurationOutputTypeDef]
    BoxPlotOptions: NotRequired[BoxPlotOptionsTypeDef]
    CategoryAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    ReferenceLines: NotRequired[List[ReferenceLineTypeDef]]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class BoxPlotFieldWellsTypeDef(TypedDict):
    BoxPlotAggregatedFieldWells: NotRequired[BoxPlotAggregatedFieldWellsUnionTypeDef]


class ComboChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[ComboChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[ComboChartSortConfigurationOutputTypeDef]
    BarsArrangement: NotRequired[BarsArrangementType]
    CategoryAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    SecondaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    SecondaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    SingleAxisOptions: NotRequired[SingleAxisOptionsTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    BarDataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    LineDataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    ReferenceLines: NotRequired[List[ReferenceLineTypeDef]]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class ComboChartFieldWellsTypeDef(TypedDict):
    ComboChartAggregatedFieldWells: NotRequired[ComboChartAggregatedFieldWellsUnionTypeDef]


class FilledMapConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[FilledMapFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[FilledMapSortConfigurationOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    WindowOptions: NotRequired[GeospatialWindowOptionsTypeDef]
    MapStyleOptions: NotRequired[GeospatialMapStyleOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class FilledMapFieldWellsTypeDef(TypedDict):
    FilledMapAggregatedFieldWells: NotRequired[FilledMapAggregatedFieldWellsUnionTypeDef]


class FunnelChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[FunnelChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[FunnelChartSortConfigurationOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    DataLabelOptions: NotRequired[FunnelChartDataLabelOptionsTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class FunnelChartFieldWellsTypeDef(TypedDict):
    FunnelChartAggregatedFieldWells: NotRequired[FunnelChartAggregatedFieldWellsUnionTypeDef]


class GaugeChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GaugeChartConfigurationOutputTypeDef]
    ConditionalFormatting: NotRequired[GaugeChartConditionalFormattingOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class GeospatialLayerItemOutputTypeDef(TypedDict):
    LayerId: str
    LayerType: NotRequired[GeospatialLayerTypeType]
    DataSource: NotRequired[GeospatialDataSourceItemTypeDef]
    Label: NotRequired[str]
    Visibility: NotRequired[VisibilityType]
    LayerDefinition: NotRequired[GeospatialLayerDefinitionOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    JoinDefinition: NotRequired[GeospatialLayerJoinDefinitionOutputTypeDef]
    Actions: NotRequired[List[LayerCustomActionOutputTypeDef]]


class GeospatialLayerJoinDefinitionTypeDef(TypedDict):
    ShapeKeyField: NotRequired[str]
    DatasetKeyField: NotRequired[UnaggregatedFieldTypeDef]
    ColorField: NotRequired[GeospatialLayerColorFieldUnionTypeDef]


class GeospatialMapConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[GeospatialMapFieldWellsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    WindowOptions: NotRequired[GeospatialWindowOptionsTypeDef]
    MapStyleOptions: NotRequired[GeospatialMapStyleOptionsTypeDef]
    PointStyleOptions: NotRequired[GeospatialPointStyleOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class GeospatialMapFieldWellsTypeDef(TypedDict):
    GeospatialMapAggregatedFieldWells: NotRequired[GeospatialMapAggregatedFieldWellsUnionTypeDef]


class HeatMapConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[HeatMapFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[HeatMapSortConfigurationOutputTypeDef]
    RowLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColumnLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColorScale: NotRequired[ColorScaleOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class HeatMapFieldWellsTypeDef(TypedDict):
    HeatMapAggregatedFieldWells: NotRequired[HeatMapAggregatedFieldWellsUnionTypeDef]


class HistogramConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[HistogramFieldWellsOutputTypeDef]
    XAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    XAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    YAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    BinOptions: NotRequired[HistogramBinOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class HistogramFieldWellsTypeDef(TypedDict):
    HistogramAggregatedFieldWells: NotRequired[HistogramAggregatedFieldWellsUnionTypeDef]


class KPIVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[KPIConfigurationOutputTypeDef]
    ConditionalFormatting: NotRequired[KPIConditionalFormattingOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


class KPIConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[KPIFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[KPISortConfigurationUnionTypeDef]
    KPIOptions: NotRequired[KPIOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


LineChartConfigurationOutputTypeDef = TypedDict(
    "LineChartConfigurationOutputTypeDef",
    {
        "FieldWells": NotRequired[LineChartFieldWellsOutputTypeDef],
        "SortConfiguration": NotRequired[LineChartSortConfigurationOutputTypeDef],
        "ForecastConfigurations": NotRequired[List[ForecastConfigurationOutputTypeDef]],
        "Type": NotRequired[LineChartTypeType],
        "SmallMultiplesOptions": NotRequired[SmallMultiplesOptionsTypeDef],
        "XAxisDisplayOptions": NotRequired[AxisDisplayOptionsOutputTypeDef],
        "XAxisLabelOptions": NotRequired[ChartAxisLabelOptionsOutputTypeDef],
        "PrimaryYAxisDisplayOptions": NotRequired[LineSeriesAxisDisplayOptionsOutputTypeDef],
        "PrimaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsOutputTypeDef],
        "SecondaryYAxisDisplayOptions": NotRequired[LineSeriesAxisDisplayOptionsOutputTypeDef],
        "SecondaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsOutputTypeDef],
        "SingleAxisOptions": NotRequired[SingleAxisOptionsTypeDef],
        "DefaultSeriesSettings": NotRequired[LineChartDefaultSeriesSettingsTypeDef],
        "Series": NotRequired[List[SeriesItemTypeDef]],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsOutputTypeDef],
        "ReferenceLines": NotRequired[List[ReferenceLineTypeDef]],
        "Tooltip": NotRequired[TooltipOptionsOutputTypeDef],
        "ContributionAnalysisDefaults": NotRequired[List[ContributionAnalysisDefaultOutputTypeDef]],
        "VisualPalette": NotRequired[VisualPaletteOutputTypeDef],
        "Interactions": NotRequired[VisualInteractionOptionsTypeDef],
    },
)


class LineChartFieldWellsTypeDef(TypedDict):
    LineChartAggregatedFieldWells: NotRequired[LineChartAggregatedFieldWellsUnionTypeDef]


class PieChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[PieChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[PieChartSortConfigurationOutputTypeDef]
    DonutOptions: NotRequired[DonutOptionsTypeDef]
    SmallMultiplesOptions: NotRequired[SmallMultiplesOptionsTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    ContributionAnalysisDefaults: NotRequired[List[ContributionAnalysisDefaultOutputTypeDef]]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class PieChartFieldWellsTypeDef(TypedDict):
    PieChartAggregatedFieldWells: NotRequired[PieChartAggregatedFieldWellsUnionTypeDef]


class PivotTableConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[PivotTableFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[PivotTableSortConfigurationOutputTypeDef]
    TableOptions: NotRequired[PivotTableOptionsOutputTypeDef]
    TotalOptions: NotRequired[PivotTableTotalOptionsOutputTypeDef]
    FieldOptions: NotRequired[PivotTableFieldOptionsOutputTypeDef]
    PaginatedReportOptions: NotRequired[PivotTablePaginatedReportOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class PivotTableFieldWellsTypeDef(TypedDict):
    PivotTableAggregatedFieldWells: NotRequired[PivotTableAggregatedFieldWellsUnionTypeDef]


class RadarChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[RadarChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[RadarChartSortConfigurationOutputTypeDef]
    Shape: NotRequired[RadarChartShapeType]
    BaseSeriesSettings: NotRequired[RadarChartSeriesSettingsTypeDef]
    StartAngle: NotRequired[float]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    AlternateBandColorsVisibility: NotRequired[VisibilityType]
    AlternateBandEvenColor: NotRequired[str]
    AlternateBandOddColor: NotRequired[str]
    CategoryAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColorAxis: NotRequired[AxisDisplayOptionsOutputTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    AxesRangeScale: NotRequired[RadarChartAxesRangeScaleType]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class RadarChartFieldWellsTypeDef(TypedDict):
    RadarChartAggregatedFieldWells: NotRequired[RadarChartAggregatedFieldWellsUnionTypeDef]


class SankeyDiagramChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[SankeyDiagramFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[SankeyDiagramSortConfigurationOutputTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class SankeyDiagramFieldWellsTypeDef(TypedDict):
    SankeyDiagramAggregatedFieldWells: NotRequired[SankeyDiagramAggregatedFieldWellsUnionTypeDef]


class ScatterPlotConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[ScatterPlotFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[ScatterPlotSortConfigurationTypeDef]
    XAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    XAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    YAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    YAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class ScatterPlotFieldWellsTypeDef(TypedDict):
    ScatterPlotCategoricallyAggregatedFieldWells: NotRequired[
        ScatterPlotCategoricallyAggregatedFieldWellsUnionTypeDef
    ]
    ScatterPlotUnaggregatedFieldWells: NotRequired[ScatterPlotUnaggregatedFieldWellsUnionTypeDef]


class InsightConfigurationOutputTypeDef(TypedDict):
    Computations: NotRequired[List[ComputationTypeDef]]
    CustomNarrative: NotRequired[CustomNarrativeOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class InsightConfigurationTypeDef(TypedDict):
    Computations: NotRequired[Sequence[ComputationTypeDef]]
    CustomNarrative: NotRequired[CustomNarrativeOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class TreeMapConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[TreeMapFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[TreeMapSortConfigurationOutputTypeDef]
    GroupLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    SizeLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    ColorScale: NotRequired[ColorScaleOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    Tooltip: NotRequired[TooltipOptionsOutputTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class TreeMapFieldWellsTypeDef(TypedDict):
    TreeMapAggregatedFieldWells: NotRequired[TreeMapAggregatedFieldWellsUnionTypeDef]


class WaterfallChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[WaterfallChartFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[WaterfallChartSortConfigurationOutputTypeDef]
    WaterfallChartOptions: NotRequired[WaterfallChartOptionsTypeDef]
    CategoryAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    CategoryAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsOutputTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsOutputTypeDef]
    VisualPalette: NotRequired[VisualPaletteOutputTypeDef]
    ColorConfiguration: NotRequired[WaterfallChartColorConfigurationTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class WaterfallChartFieldWellsTypeDef(TypedDict):
    WaterfallChartAggregatedFieldWells: NotRequired[WaterfallChartAggregatedFieldWellsUnionTypeDef]


class WordCloudChartConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[WordCloudFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[WordCloudSortConfigurationOutputTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsOutputTypeDef]
    WordCloudOptions: NotRequired[WordCloudOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class WordCloudFieldWellsTypeDef(TypedDict):
    WordCloudAggregatedFieldWells: NotRequired[WordCloudAggregatedFieldWellsUnionTypeDef]


class PluginVisualOutputTypeDef(TypedDict):
    VisualId: str
    PluginArn: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PluginVisualConfigurationOutputTypeDef]
    VisualContentAltText: NotRequired[str]


class TableConfigurationOutputTypeDef(TypedDict):
    FieldWells: NotRequired[TableFieldWellsOutputTypeDef]
    SortConfiguration: NotRequired[TableSortConfigurationOutputTypeDef]
    TableOptions: NotRequired[TableOptionsOutputTypeDef]
    TotalOptions: NotRequired[TotalOptionsOutputTypeDef]
    FieldOptions: NotRequired[TableFieldOptionsOutputTypeDef]
    PaginatedReportOptions: NotRequired[TablePaginatedReportOptionsTypeDef]
    TableInlineVisualizations: NotRequired[List[TableInlineVisualizationTypeDef]]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class TableFieldWellsTypeDef(TypedDict):
    TableAggregatedFieldWells: NotRequired[TableAggregatedFieldWellsUnionTypeDef]
    TableUnaggregatedFieldWells: NotRequired[TableUnaggregatedFieldWellsUnionTypeDef]


class LayoutConfigurationOutputTypeDef(TypedDict):
    GridLayout: NotRequired[GridLayoutConfigurationOutputTypeDef]
    FreeFormLayout: NotRequired[FreeFormLayoutConfigurationOutputTypeDef]
    SectionBasedLayout: NotRequired[SectionBasedLayoutConfigurationOutputTypeDef]


BodySectionRepeatConfigurationUnionTypeDef = Union[
    BodySectionRepeatConfigurationTypeDef, BodySectionRepeatConfigurationOutputTypeDef
]


class PluginVisualConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[Sequence[PluginVisualFieldWellUnionTypeDef]]
    VisualOptions: NotRequired[PluginVisualOptionsUnionTypeDef]
    SortConfiguration: NotRequired[PluginVisualSortConfigurationUnionTypeDef]


PivotTableSortConfigurationUnionTypeDef = Union[
    PivotTableSortConfigurationTypeDef, PivotTableSortConfigurationOutputTypeDef
]


class GaugeChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[GaugeChartFieldWellsUnionTypeDef]
    GaugeChartOptions: NotRequired[GaugeChartOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    TooltipOptions: NotRequired[TooltipOptionsUnionTypeDef]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    ColorConfiguration: NotRequired[GaugeChartColorConfigurationTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class StartAssetBundleImportJobRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AssetBundleImportJobId: str
    AssetBundleImportSource: AssetBundleImportSourceTypeDef
    OverrideParameters: NotRequired[AssetBundleImportJobOverrideParametersTypeDef]
    FailureAction: NotRequired[AssetBundleImportFailureActionType]
    OverridePermissions: NotRequired[AssetBundleImportJobOverridePermissionsTypeDef]
    OverrideTags: NotRequired[AssetBundleImportJobOverrideTagsTypeDef]
    OverrideValidationStrategy: NotRequired[AssetBundleImportJobOverrideValidationStrategyTypeDef]


BodySectionContentUnionTypeDef = Union[BodySectionContentTypeDef, BodySectionContentOutputTypeDef]
HeaderFooterSectionConfigurationUnionTypeDef = Union[
    HeaderFooterSectionConfigurationTypeDef, HeaderFooterSectionConfigurationOutputTypeDef
]
CustomActionSetParametersOperationUnionTypeDef = Union[
    CustomActionSetParametersOperationTypeDef, CustomActionSetParametersOperationOutputTypeDef
]
LineSeriesAxisDisplayOptionsUnionTypeDef = Union[
    LineSeriesAxisDisplayOptionsTypeDef, LineSeriesAxisDisplayOptionsOutputTypeDef
]
TopicIRUnionTypeDef = Union[TopicIRTypeDef, TopicIROutputTypeDef]


class TopicDetailsTypeDef(TypedDict):
    Name: NotRequired[str]
    Description: NotRequired[str]
    UserExperienceVersion: NotRequired[TopicUserExperienceVersionType]
    DataSets: NotRequired[Sequence[DatasetMetadataUnionTypeDef]]
    ConfigOptions: NotRequired[TopicConfigOptionsTypeDef]


class DescribeAnalysisResponseTypeDef(TypedDict):
    Analysis: AnalysisTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DashboardTypeDef(TypedDict):
    DashboardId: NotRequired[str]
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[DashboardVersionTypeDef]
    CreatedTime: NotRequired[datetime]
    LastPublishedTime: NotRequired[datetime]
    LastUpdatedTime: NotRequired[datetime]
    LinkEntities: NotRequired[List[str]]


class TemplateTypeDef(TypedDict):
    Arn: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[TemplateVersionTypeDef]
    TemplateId: NotRequired[str]
    LastUpdatedTime: NotRequired[datetime]
    CreatedTime: NotRequired[datetime]


class CategoryFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    Configuration: CategoryFilterConfigurationUnionTypeDef
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationUnionTypeDef]


class CategoryInnerFilterTypeDef(TypedDict):
    Column: ColumnIdentifierTypeDef
    Configuration: CategoryFilterConfigurationUnionTypeDef
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationUnionTypeDef]


class NumericEqualityFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    MatchOperator: NumericEqualityMatchOperatorType
    NullOption: FilterNullOptionType
    Value: NotRequired[float]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]
    ParameterName: NotRequired[str]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationUnionTypeDef]


class NumericRangeFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    NullOption: FilterNullOptionType
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]
    RangeMinimum: NotRequired[NumericRangeFilterValueTypeDef]
    RangeMaximum: NotRequired[NumericRangeFilterValueTypeDef]
    SelectAllOptions: NotRequired[Literal["FILTER_ALL_VALUES"]]
    AggregationFunction: NotRequired[AggregationFunctionTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationUnionTypeDef]


class RelativeDatesFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    AnchorDateConfiguration: AnchorDateConfigurationTypeDef
    TimeGranularity: TimeGranularityType
    RelativeDateType: RelativeDateTypeType
    NullOption: FilterNullOptionType
    MinimumGranularity: NotRequired[TimeGranularityType]
    RelativeDateValue: NotRequired[int]
    ParameterName: NotRequired[str]
    ExcludePeriodConfiguration: NotRequired[ExcludePeriodConfigurationTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationUnionTypeDef]


class TimeEqualityFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    Value: NotRequired[TimestampTypeDef]
    ParameterName: NotRequired[str]
    TimeGranularity: NotRequired[TimeGranularityType]
    RollingDate: NotRequired[RollingDateConfigurationTypeDef]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationUnionTypeDef]


class TimeRangeFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    NullOption: FilterNullOptionType
    IncludeMinimum: NotRequired[bool]
    IncludeMaximum: NotRequired[bool]
    RangeMinimumValue: NotRequired[TimeRangeFilterValueUnionTypeDef]
    RangeMaximumValue: NotRequired[TimeRangeFilterValueUnionTypeDef]
    ExcludePeriodConfiguration: NotRequired[ExcludePeriodConfigurationTypeDef]
    TimeGranularity: NotRequired[TimeGranularityType]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationUnionTypeDef]


class TopBottomFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    AggregationSortConfigurations: Sequence[AggregationSortConfigurationTypeDef]
    Limit: NotRequired[int]
    TimeGranularity: NotRequired[TimeGranularityType]
    ParameterName: NotRequired[str]
    DefaultFilterControlConfiguration: NotRequired[DefaultFilterControlConfigurationUnionTypeDef]


class FilterOutputTypeDef(TypedDict):
    CategoryFilter: NotRequired[CategoryFilterOutputTypeDef]
    NumericRangeFilter: NotRequired[NumericRangeFilterOutputTypeDef]
    NumericEqualityFilter: NotRequired[NumericEqualityFilterOutputTypeDef]
    TimeEqualityFilter: NotRequired[TimeEqualityFilterOutputTypeDef]
    TimeRangeFilter: NotRequired[TimeRangeFilterOutputTypeDef]
    RelativeDatesFilter: NotRequired[RelativeDatesFilterOutputTypeDef]
    TopBottomFilter: NotRequired[TopBottomFilterOutputTypeDef]
    NestedFilter: NotRequired[NestedFilterOutputTypeDef]


class GeospatialPointLayerTypeDef(TypedDict):
    Style: GeospatialPointStyleUnionTypeDef


class GeospatialLineLayerTypeDef(TypedDict):
    Style: GeospatialLineStyleUnionTypeDef


class GeospatialPolygonLayerTypeDef(TypedDict):
    Style: GeospatialPolygonStyleUnionTypeDef


GaugeChartConditionalFormattingOptionUnionTypeDef = Union[
    GaugeChartConditionalFormattingOptionTypeDef, GaugeChartConditionalFormattingOptionOutputTypeDef
]
KPIConditionalFormattingOptionUnionTypeDef = Union[
    KPIConditionalFormattingOptionTypeDef, KPIConditionalFormattingOptionOutputTypeDef
]
FilledMapShapeConditionalFormattingUnionTypeDef = Union[
    FilledMapShapeConditionalFormattingTypeDef, FilledMapShapeConditionalFormattingOutputTypeDef
]
PivotTableCellConditionalFormattingUnionTypeDef = Union[
    PivotTableCellConditionalFormattingTypeDef, PivotTableCellConditionalFormattingOutputTypeDef
]
TableCellConditionalFormattingUnionTypeDef = Union[
    TableCellConditionalFormattingTypeDef, TableCellConditionalFormattingOutputTypeDef
]


class BarChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[BarChartConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


BarChartFieldWellsUnionTypeDef = Union[BarChartFieldWellsTypeDef, BarChartFieldWellsOutputTypeDef]


class BoxPlotVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[BoxPlotChartConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


BoxPlotFieldWellsUnionTypeDef = Union[BoxPlotFieldWellsTypeDef, BoxPlotFieldWellsOutputTypeDef]


class ComboChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[ComboChartConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


ComboChartFieldWellsUnionTypeDef = Union[
    ComboChartFieldWellsTypeDef, ComboChartFieldWellsOutputTypeDef
]


class FilledMapVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[FilledMapConfigurationOutputTypeDef]
    ConditionalFormatting: NotRequired[FilledMapConditionalFormattingOutputTypeDef]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


FilledMapFieldWellsUnionTypeDef = Union[
    FilledMapFieldWellsTypeDef, FilledMapFieldWellsOutputTypeDef
]


class FunnelChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[FunnelChartConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


FunnelChartFieldWellsUnionTypeDef = Union[
    FunnelChartFieldWellsTypeDef, FunnelChartFieldWellsOutputTypeDef
]


class GeospatialLayerMapConfigurationOutputTypeDef(TypedDict):
    Legend: NotRequired[LegendOptionsTypeDef]
    MapLayers: NotRequired[List[GeospatialLayerItemOutputTypeDef]]
    MapState: NotRequired[GeospatialMapStateTypeDef]
    MapStyle: NotRequired[GeospatialMapStyleTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


GeospatialLayerJoinDefinitionUnionTypeDef = Union[
    GeospatialLayerJoinDefinitionTypeDef, GeospatialLayerJoinDefinitionOutputTypeDef
]


class GeospatialMapVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GeospatialMapConfigurationOutputTypeDef]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


GeospatialMapFieldWellsUnionTypeDef = Union[
    GeospatialMapFieldWellsTypeDef, GeospatialMapFieldWellsOutputTypeDef
]


class HeatMapVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[HeatMapConfigurationOutputTypeDef]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


HeatMapFieldWellsUnionTypeDef = Union[HeatMapFieldWellsTypeDef, HeatMapFieldWellsOutputTypeDef]


class HistogramVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[HistogramConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


HistogramFieldWellsUnionTypeDef = Union[
    HistogramFieldWellsTypeDef, HistogramFieldWellsOutputTypeDef
]
KPIConfigurationUnionTypeDef = Union[KPIConfigurationTypeDef, KPIConfigurationOutputTypeDef]


class LineChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[LineChartConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


LineChartFieldWellsUnionTypeDef = Union[
    LineChartFieldWellsTypeDef, LineChartFieldWellsOutputTypeDef
]


class PieChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PieChartConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


PieChartFieldWellsUnionTypeDef = Union[PieChartFieldWellsTypeDef, PieChartFieldWellsOutputTypeDef]


class PivotTableVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PivotTableConfigurationOutputTypeDef]
    ConditionalFormatting: NotRequired[PivotTableConditionalFormattingOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


PivotTableFieldWellsUnionTypeDef = Union[
    PivotTableFieldWellsTypeDef, PivotTableFieldWellsOutputTypeDef
]


class RadarChartVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[RadarChartConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


RadarChartFieldWellsUnionTypeDef = Union[
    RadarChartFieldWellsTypeDef, RadarChartFieldWellsOutputTypeDef
]


class SankeyDiagramVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[SankeyDiagramChartConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


SankeyDiagramFieldWellsUnionTypeDef = Union[
    SankeyDiagramFieldWellsTypeDef, SankeyDiagramFieldWellsOutputTypeDef
]


class ScatterPlotVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[ScatterPlotConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


ScatterPlotFieldWellsUnionTypeDef = Union[
    ScatterPlotFieldWellsTypeDef, ScatterPlotFieldWellsOutputTypeDef
]


class InsightVisualOutputTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    InsightConfiguration: NotRequired[InsightConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


InsightConfigurationUnionTypeDef = Union[
    InsightConfigurationTypeDef, InsightConfigurationOutputTypeDef
]


class TreeMapVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[TreeMapConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


TreeMapFieldWellsUnionTypeDef = Union[TreeMapFieldWellsTypeDef, TreeMapFieldWellsOutputTypeDef]


class WaterfallVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[WaterfallChartConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


WaterfallChartFieldWellsUnionTypeDef = Union[
    WaterfallChartFieldWellsTypeDef, WaterfallChartFieldWellsOutputTypeDef
]


class WordCloudVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[WordCloudChartConfigurationOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    ColumnHierarchies: NotRequired[List[ColumnHierarchyOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


WordCloudFieldWellsUnionTypeDef = Union[
    WordCloudFieldWellsTypeDef, WordCloudFieldWellsOutputTypeDef
]


class TableVisualOutputTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[TableConfigurationOutputTypeDef]
    ConditionalFormatting: NotRequired[TableConditionalFormattingOutputTypeDef]
    Actions: NotRequired[List[VisualCustomActionOutputTypeDef]]
    VisualContentAltText: NotRequired[str]


TableFieldWellsUnionTypeDef = Union[TableFieldWellsTypeDef, TableFieldWellsOutputTypeDef]


class LayoutOutputTypeDef(TypedDict):
    Configuration: LayoutConfigurationOutputTypeDef


PluginVisualConfigurationUnionTypeDef = Union[
    PluginVisualConfigurationTypeDef, PluginVisualConfigurationOutputTypeDef
]
GaugeChartConfigurationUnionTypeDef = Union[
    GaugeChartConfigurationTypeDef, GaugeChartConfigurationOutputTypeDef
]


class BodySectionConfigurationTypeDef(TypedDict):
    SectionId: str
    Content: BodySectionContentUnionTypeDef
    Style: NotRequired[SectionStyleTypeDef]
    PageBreakConfiguration: NotRequired[SectionPageBreakConfigurationTypeDef]
    RepeatConfiguration: NotRequired[BodySectionRepeatConfigurationUnionTypeDef]


class ImageCustomActionOperationTypeDef(TypedDict):
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationUnionTypeDef]


class LayerCustomActionOperationTypeDef(TypedDict):
    FilterOperation: NotRequired[CustomActionFilterOperationUnionTypeDef]
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationUnionTypeDef]


class VisualCustomActionOperationTypeDef(TypedDict):
    FilterOperation: NotRequired[CustomActionFilterOperationUnionTypeDef]
    NavigationOperation: NotRequired[CustomActionNavigationOperationTypeDef]
    URLOperation: NotRequired[CustomActionURLOperationTypeDef]
    SetParametersOperation: NotRequired[CustomActionSetParametersOperationUnionTypeDef]


class TopicVisualTypeDef(TypedDict):
    VisualId: NotRequired[str]
    Role: NotRequired[VisualRoleType]
    Ir: NotRequired[TopicIRUnionTypeDef]
    SupportingVisuals: NotRequired[Sequence[Mapping[str, Any]]]


class CreateTopicRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    Topic: TopicDetailsTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]
    FolderArns: NotRequired[Sequence[str]]


class UpdateTopicRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    Topic: TopicDetailsTypeDef


class DescribeDashboardResponseTypeDef(TypedDict):
    Dashboard: DashboardTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTemplateResponseTypeDef(TypedDict):
    Template: TemplateTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


CategoryFilterUnionTypeDef = Union[CategoryFilterTypeDef, CategoryFilterOutputTypeDef]
CategoryInnerFilterUnionTypeDef = Union[
    CategoryInnerFilterTypeDef, CategoryInnerFilterOutputTypeDef
]
NumericEqualityFilterUnionTypeDef = Union[
    NumericEqualityFilterTypeDef, NumericEqualityFilterOutputTypeDef
]
NumericRangeFilterUnionTypeDef = Union[NumericRangeFilterTypeDef, NumericRangeFilterOutputTypeDef]
RelativeDatesFilterUnionTypeDef = Union[
    RelativeDatesFilterTypeDef, RelativeDatesFilterOutputTypeDef
]
TimeEqualityFilterUnionTypeDef = Union[TimeEqualityFilterTypeDef, TimeEqualityFilterOutputTypeDef]
TimeRangeFilterUnionTypeDef = Union[TimeRangeFilterTypeDef, TimeRangeFilterOutputTypeDef]
TopBottomFilterUnionTypeDef = Union[TopBottomFilterTypeDef, TopBottomFilterOutputTypeDef]


class FilterGroupOutputTypeDef(TypedDict):
    FilterGroupId: str
    Filters: List[FilterOutputTypeDef]
    ScopeConfiguration: FilterScopeConfigurationOutputTypeDef
    CrossDataset: CrossDatasetTypesType
    Status: NotRequired[WidgetStatusType]


GeospatialPointLayerUnionTypeDef = Union[
    GeospatialPointLayerTypeDef, GeospatialPointLayerOutputTypeDef
]
GeospatialLineLayerUnionTypeDef = Union[
    GeospatialLineLayerTypeDef, GeospatialLineLayerOutputTypeDef
]
GeospatialPolygonLayerUnionTypeDef = Union[
    GeospatialPolygonLayerTypeDef, GeospatialPolygonLayerOutputTypeDef
]


class GaugeChartConditionalFormattingTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[
        Sequence[GaugeChartConditionalFormattingOptionUnionTypeDef]
    ]


class KPIConditionalFormattingTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[Sequence[KPIConditionalFormattingOptionUnionTypeDef]]


class FilledMapConditionalFormattingOptionTypeDef(TypedDict):
    Shape: FilledMapShapeConditionalFormattingUnionTypeDef


class PivotTableConditionalFormattingOptionTypeDef(TypedDict):
    Cell: NotRequired[PivotTableCellConditionalFormattingUnionTypeDef]


class TableConditionalFormattingOptionTypeDef(TypedDict):
    Cell: NotRequired[TableCellConditionalFormattingUnionTypeDef]
    Row: NotRequired[TableRowConditionalFormattingUnionTypeDef]


class BarChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[BarChartFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[BarChartSortConfigurationUnionTypeDef]
    Orientation: NotRequired[BarChartOrientationType]
    BarsArrangement: NotRequired[BarsArrangementType]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    SmallMultiplesOptions: NotRequired[SmallMultiplesOptionsTypeDef]
    CategoryAxis: NotRequired[AxisDisplayOptionsUnionTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    ValueAxis: NotRequired[AxisDisplayOptionsUnionTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    ReferenceLines: NotRequired[Sequence[ReferenceLineTypeDef]]
    ContributionAnalysisDefaults: NotRequired[Sequence[ContributionAnalysisDefaultUnionTypeDef]]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class BoxPlotChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[BoxPlotFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[BoxPlotSortConfigurationUnionTypeDef]
    BoxPlotOptions: NotRequired[BoxPlotOptionsTypeDef]
    CategoryAxis: NotRequired[AxisDisplayOptionsUnionTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsUnionTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    ReferenceLines: NotRequired[Sequence[ReferenceLineTypeDef]]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class ComboChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[ComboChartFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[ComboChartSortConfigurationUnionTypeDef]
    BarsArrangement: NotRequired[BarsArrangementType]
    CategoryAxis: NotRequired[AxisDisplayOptionsUnionTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsUnionTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    SecondaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsUnionTypeDef]
    SecondaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    SingleAxisOptions: NotRequired[SingleAxisOptionsTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    BarDataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    LineDataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    ReferenceLines: NotRequired[Sequence[ReferenceLineTypeDef]]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class FilledMapConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[FilledMapFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[FilledMapSortConfigurationUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    WindowOptions: NotRequired[GeospatialWindowOptionsTypeDef]
    MapStyleOptions: NotRequired[GeospatialMapStyleOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class FunnelChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[FunnelChartFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[FunnelChartSortConfigurationUnionTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    DataLabelOptions: NotRequired[FunnelChartDataLabelOptionsTypeDef]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class LayerMapVisualOutputTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GeospatialLayerMapConfigurationOutputTypeDef]
    VisualContentAltText: NotRequired[str]


class GeospatialMapConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[GeospatialMapFieldWellsUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    WindowOptions: NotRequired[GeospatialWindowOptionsTypeDef]
    MapStyleOptions: NotRequired[GeospatialMapStyleOptionsTypeDef]
    PointStyleOptions: NotRequired[GeospatialPointStyleOptionsUnionTypeDef]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class HeatMapConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[HeatMapFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[HeatMapSortConfigurationUnionTypeDef]
    RowLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    ColumnLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    ColorScale: NotRequired[ColorScaleUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class HistogramConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[HistogramFieldWellsUnionTypeDef]
    XAxisDisplayOptions: NotRequired[AxisDisplayOptionsUnionTypeDef]
    XAxisLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    YAxisDisplayOptions: NotRequired[AxisDisplayOptionsUnionTypeDef]
    BinOptions: NotRequired[HistogramBinOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


LineChartConfigurationTypeDef = TypedDict(
    "LineChartConfigurationTypeDef",
    {
        "FieldWells": NotRequired[LineChartFieldWellsUnionTypeDef],
        "SortConfiguration": NotRequired[LineChartSortConfigurationUnionTypeDef],
        "ForecastConfigurations": NotRequired[Sequence[ForecastConfigurationUnionTypeDef]],
        "Type": NotRequired[LineChartTypeType],
        "SmallMultiplesOptions": NotRequired[SmallMultiplesOptionsTypeDef],
        "XAxisDisplayOptions": NotRequired[AxisDisplayOptionsUnionTypeDef],
        "XAxisLabelOptions": NotRequired[ChartAxisLabelOptionsUnionTypeDef],
        "PrimaryYAxisDisplayOptions": NotRequired[LineSeriesAxisDisplayOptionsUnionTypeDef],
        "PrimaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsUnionTypeDef],
        "SecondaryYAxisDisplayOptions": NotRequired[LineSeriesAxisDisplayOptionsUnionTypeDef],
        "SecondaryYAxisLabelOptions": NotRequired[ChartAxisLabelOptionsUnionTypeDef],
        "SingleAxisOptions": NotRequired[SingleAxisOptionsTypeDef],
        "DefaultSeriesSettings": NotRequired[LineChartDefaultSeriesSettingsTypeDef],
        "Series": NotRequired[Sequence[SeriesItemTypeDef]],
        "Legend": NotRequired[LegendOptionsTypeDef],
        "DataLabels": NotRequired[DataLabelOptionsUnionTypeDef],
        "ReferenceLines": NotRequired[Sequence[ReferenceLineTypeDef]],
        "Tooltip": NotRequired[TooltipOptionsUnionTypeDef],
        "ContributionAnalysisDefaults": NotRequired[
            Sequence[ContributionAnalysisDefaultUnionTypeDef]
        ],
        "VisualPalette": NotRequired[VisualPaletteUnionTypeDef],
        "Interactions": NotRequired[VisualInteractionOptionsTypeDef],
    },
)


class PieChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[PieChartFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[PieChartSortConfigurationUnionTypeDef]
    DonutOptions: NotRequired[DonutOptionsTypeDef]
    SmallMultiplesOptions: NotRequired[SmallMultiplesOptionsTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    ValueLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    ContributionAnalysisDefaults: NotRequired[Sequence[ContributionAnalysisDefaultUnionTypeDef]]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class PivotTableConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[PivotTableFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[PivotTableSortConfigurationUnionTypeDef]
    TableOptions: NotRequired[PivotTableOptionsUnionTypeDef]
    TotalOptions: NotRequired[PivotTableTotalOptionsUnionTypeDef]
    FieldOptions: NotRequired[PivotTableFieldOptionsUnionTypeDef]
    PaginatedReportOptions: NotRequired[PivotTablePaginatedReportOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class RadarChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[RadarChartFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[RadarChartSortConfigurationUnionTypeDef]
    Shape: NotRequired[RadarChartShapeType]
    BaseSeriesSettings: NotRequired[RadarChartSeriesSettingsTypeDef]
    StartAngle: NotRequired[float]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    AlternateBandColorsVisibility: NotRequired[VisibilityType]
    AlternateBandEvenColor: NotRequired[str]
    AlternateBandOddColor: NotRequired[str]
    CategoryAxis: NotRequired[AxisDisplayOptionsUnionTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    ColorAxis: NotRequired[AxisDisplayOptionsUnionTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    AxesRangeScale: NotRequired[RadarChartAxesRangeScaleType]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class SankeyDiagramChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[SankeyDiagramFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[SankeyDiagramSortConfigurationUnionTypeDef]
    DataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class ScatterPlotConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[ScatterPlotFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[ScatterPlotSortConfigurationTypeDef]
    XAxisLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    XAxisDisplayOptions: NotRequired[AxisDisplayOptionsUnionTypeDef]
    YAxisLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    YAxisDisplayOptions: NotRequired[AxisDisplayOptionsUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class TreeMapConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[TreeMapFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[TreeMapSortConfigurationUnionTypeDef]
    GroupLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    SizeLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    ColorLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    ColorScale: NotRequired[ColorScaleUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class WaterfallChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[WaterfallChartFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[WaterfallChartSortConfigurationUnionTypeDef]
    WaterfallChartOptions: NotRequired[WaterfallChartOptionsTypeDef]
    CategoryAxisLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    CategoryAxisDisplayOptions: NotRequired[AxisDisplayOptionsUnionTypeDef]
    PrimaryYAxisLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    PrimaryYAxisDisplayOptions: NotRequired[AxisDisplayOptionsUnionTypeDef]
    Legend: NotRequired[LegendOptionsTypeDef]
    DataLabels: NotRequired[DataLabelOptionsUnionTypeDef]
    VisualPalette: NotRequired[VisualPaletteUnionTypeDef]
    ColorConfiguration: NotRequired[WaterfallChartColorConfigurationTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class WordCloudChartConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[WordCloudFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[WordCloudSortConfigurationUnionTypeDef]
    CategoryLabelOptions: NotRequired[ChartAxisLabelOptionsUnionTypeDef]
    WordCloudOptions: NotRequired[WordCloudOptionsTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class TableConfigurationTypeDef(TypedDict):
    FieldWells: NotRequired[TableFieldWellsUnionTypeDef]
    SortConfiguration: NotRequired[TableSortConfigurationUnionTypeDef]
    TableOptions: NotRequired[TableOptionsUnionTypeDef]
    TotalOptions: NotRequired[TotalOptionsUnionTypeDef]
    FieldOptions: NotRequired[TableFieldOptionsUnionTypeDef]
    PaginatedReportOptions: NotRequired[TablePaginatedReportOptionsTypeDef]
    TableInlineVisualizations: NotRequired[Sequence[TableInlineVisualizationTypeDef]]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


class PluginVisualTypeDef(TypedDict):
    VisualId: str
    PluginArn: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PluginVisualConfigurationUnionTypeDef]
    VisualContentAltText: NotRequired[str]


BodySectionConfigurationUnionTypeDef = Union[
    BodySectionConfigurationTypeDef, BodySectionConfigurationOutputTypeDef
]
ImageCustomActionOperationUnionTypeDef = Union[
    ImageCustomActionOperationTypeDef, ImageCustomActionOperationOutputTypeDef
]
LayerCustomActionOperationUnionTypeDef = Union[
    LayerCustomActionOperationTypeDef, LayerCustomActionOperationOutputTypeDef
]
VisualCustomActionOperationUnionTypeDef = Union[
    VisualCustomActionOperationTypeDef, VisualCustomActionOperationOutputTypeDef
]
TopicVisualUnionTypeDef = Union[TopicVisualTypeDef, TopicVisualOutputTypeDef]


class InnerFilterTypeDef(TypedDict):
    CategoryInnerFilter: NotRequired[CategoryInnerFilterUnionTypeDef]


class GeospatialLayerDefinitionTypeDef(TypedDict):
    PointLayer: NotRequired[GeospatialPointLayerUnionTypeDef]
    LineLayer: NotRequired[GeospatialLineLayerUnionTypeDef]
    PolygonLayer: NotRequired[GeospatialPolygonLayerUnionTypeDef]


GaugeChartConditionalFormattingUnionTypeDef = Union[
    GaugeChartConditionalFormattingTypeDef, GaugeChartConditionalFormattingOutputTypeDef
]
KPIConditionalFormattingUnionTypeDef = Union[
    KPIConditionalFormattingTypeDef, KPIConditionalFormattingOutputTypeDef
]
FilledMapConditionalFormattingOptionUnionTypeDef = Union[
    FilledMapConditionalFormattingOptionTypeDef, FilledMapConditionalFormattingOptionOutputTypeDef
]
PivotTableConditionalFormattingOptionUnionTypeDef = Union[
    PivotTableConditionalFormattingOptionTypeDef, PivotTableConditionalFormattingOptionOutputTypeDef
]
TableConditionalFormattingOptionUnionTypeDef = Union[
    TableConditionalFormattingOptionTypeDef, TableConditionalFormattingOptionOutputTypeDef
]
BarChartConfigurationUnionTypeDef = Union[
    BarChartConfigurationTypeDef, BarChartConfigurationOutputTypeDef
]
BoxPlotChartConfigurationUnionTypeDef = Union[
    BoxPlotChartConfigurationTypeDef, BoxPlotChartConfigurationOutputTypeDef
]
ComboChartConfigurationUnionTypeDef = Union[
    ComboChartConfigurationTypeDef, ComboChartConfigurationOutputTypeDef
]
FilledMapConfigurationUnionTypeDef = Union[
    FilledMapConfigurationTypeDef, FilledMapConfigurationOutputTypeDef
]
FunnelChartConfigurationUnionTypeDef = Union[
    FunnelChartConfigurationTypeDef, FunnelChartConfigurationOutputTypeDef
]


class VisualOutputTypeDef(TypedDict):
    TableVisual: NotRequired[TableVisualOutputTypeDef]
    PivotTableVisual: NotRequired[PivotTableVisualOutputTypeDef]
    BarChartVisual: NotRequired[BarChartVisualOutputTypeDef]
    KPIVisual: NotRequired[KPIVisualOutputTypeDef]
    PieChartVisual: NotRequired[PieChartVisualOutputTypeDef]
    GaugeChartVisual: NotRequired[GaugeChartVisualOutputTypeDef]
    LineChartVisual: NotRequired[LineChartVisualOutputTypeDef]
    HeatMapVisual: NotRequired[HeatMapVisualOutputTypeDef]
    TreeMapVisual: NotRequired[TreeMapVisualOutputTypeDef]
    GeospatialMapVisual: NotRequired[GeospatialMapVisualOutputTypeDef]
    FilledMapVisual: NotRequired[FilledMapVisualOutputTypeDef]
    LayerMapVisual: NotRequired[LayerMapVisualOutputTypeDef]
    FunnelChartVisual: NotRequired[FunnelChartVisualOutputTypeDef]
    ScatterPlotVisual: NotRequired[ScatterPlotVisualOutputTypeDef]
    ComboChartVisual: NotRequired[ComboChartVisualOutputTypeDef]
    BoxPlotVisual: NotRequired[BoxPlotVisualOutputTypeDef]
    WaterfallVisual: NotRequired[WaterfallVisualOutputTypeDef]
    HistogramVisual: NotRequired[HistogramVisualOutputTypeDef]
    WordCloudVisual: NotRequired[WordCloudVisualOutputTypeDef]
    InsightVisual: NotRequired[InsightVisualOutputTypeDef]
    SankeyDiagramVisual: NotRequired[SankeyDiagramVisualOutputTypeDef]
    CustomContentVisual: NotRequired[CustomContentVisualOutputTypeDef]
    EmptyVisual: NotRequired[EmptyVisualOutputTypeDef]
    RadarChartVisual: NotRequired[RadarChartVisualOutputTypeDef]
    PluginVisual: NotRequired[PluginVisualOutputTypeDef]


GeospatialMapConfigurationUnionTypeDef = Union[
    GeospatialMapConfigurationTypeDef, GeospatialMapConfigurationOutputTypeDef
]
HeatMapConfigurationUnionTypeDef = Union[
    HeatMapConfigurationTypeDef, HeatMapConfigurationOutputTypeDef
]
HistogramConfigurationUnionTypeDef = Union[
    HistogramConfigurationTypeDef, HistogramConfigurationOutputTypeDef
]
LineChartConfigurationUnionTypeDef = Union[
    LineChartConfigurationTypeDef, LineChartConfigurationOutputTypeDef
]
PieChartConfigurationUnionTypeDef = Union[
    PieChartConfigurationTypeDef, PieChartConfigurationOutputTypeDef
]
PivotTableConfigurationUnionTypeDef = Union[
    PivotTableConfigurationTypeDef, PivotTableConfigurationOutputTypeDef
]
RadarChartConfigurationUnionTypeDef = Union[
    RadarChartConfigurationTypeDef, RadarChartConfigurationOutputTypeDef
]
SankeyDiagramChartConfigurationUnionTypeDef = Union[
    SankeyDiagramChartConfigurationTypeDef, SankeyDiagramChartConfigurationOutputTypeDef
]
ScatterPlotConfigurationUnionTypeDef = Union[
    ScatterPlotConfigurationTypeDef, ScatterPlotConfigurationOutputTypeDef
]
TreeMapConfigurationUnionTypeDef = Union[
    TreeMapConfigurationTypeDef, TreeMapConfigurationOutputTypeDef
]
WaterfallChartConfigurationUnionTypeDef = Union[
    WaterfallChartConfigurationTypeDef, WaterfallChartConfigurationOutputTypeDef
]
WordCloudChartConfigurationUnionTypeDef = Union[
    WordCloudChartConfigurationTypeDef, WordCloudChartConfigurationOutputTypeDef
]
TableConfigurationUnionTypeDef = Union[TableConfigurationTypeDef, TableConfigurationOutputTypeDef]
PluginVisualUnionTypeDef = Union[PluginVisualTypeDef, PluginVisualOutputTypeDef]


class SectionBasedLayoutConfigurationTypeDef(TypedDict):
    HeaderSections: Sequence[HeaderFooterSectionConfigurationUnionTypeDef]
    BodySections: Sequence[BodySectionConfigurationUnionTypeDef]
    FooterSections: Sequence[HeaderFooterSectionConfigurationUnionTypeDef]
    CanvasSizeOptions: SectionBasedLayoutCanvasSizeOptionsTypeDef


class ImageCustomActionTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: ImageCustomActionTriggerType
    ActionOperations: Sequence[ImageCustomActionOperationUnionTypeDef]
    Status: NotRequired[WidgetStatusType]


class LayerCustomActionTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: LayerCustomActionTriggerType
    ActionOperations: Sequence[LayerCustomActionOperationUnionTypeDef]
    Status: NotRequired[WidgetStatusType]


class VisualCustomActionTypeDef(TypedDict):
    CustomActionId: str
    Name: str
    Trigger: VisualCustomActionTriggerType
    ActionOperations: Sequence[VisualCustomActionOperationUnionTypeDef]
    Status: NotRequired[WidgetStatusType]


class CreateTopicReviewedAnswerTypeDef(TypedDict):
    AnswerId: str
    DatasetArn: str
    Question: str
    Mir: NotRequired[TopicIRUnionTypeDef]
    PrimaryVisual: NotRequired[TopicVisualUnionTypeDef]
    Template: NotRequired[TopicTemplateUnionTypeDef]


InnerFilterUnionTypeDef = Union[InnerFilterTypeDef, InnerFilterOutputTypeDef]
GeospatialLayerDefinitionUnionTypeDef = Union[
    GeospatialLayerDefinitionTypeDef, GeospatialLayerDefinitionOutputTypeDef
]


class FilledMapConditionalFormattingTypeDef(TypedDict):
    ConditionalFormattingOptions: Sequence[FilledMapConditionalFormattingOptionUnionTypeDef]


class PivotTableConditionalFormattingTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[
        Sequence[PivotTableConditionalFormattingOptionUnionTypeDef]
    ]


class TableConditionalFormattingTypeDef(TypedDict):
    ConditionalFormattingOptions: NotRequired[
        Sequence[TableConditionalFormattingOptionUnionTypeDef]
    ]


class SheetDefinitionOutputTypeDef(TypedDict):
    SheetId: str
    Title: NotRequired[str]
    Description: NotRequired[str]
    Name: NotRequired[str]
    ParameterControls: NotRequired[List[ParameterControlOutputTypeDef]]
    FilterControls: NotRequired[List[FilterControlOutputTypeDef]]
    Visuals: NotRequired[List[VisualOutputTypeDef]]
    TextBoxes: NotRequired[List[SheetTextBoxTypeDef]]
    Images: NotRequired[List[SheetImageOutputTypeDef]]
    Layouts: NotRequired[List[LayoutOutputTypeDef]]
    SheetControlLayouts: NotRequired[List[SheetControlLayoutOutputTypeDef]]
    ContentType: NotRequired[SheetContentTypeType]


SectionBasedLayoutConfigurationUnionTypeDef = Union[
    SectionBasedLayoutConfigurationTypeDef, SectionBasedLayoutConfigurationOutputTypeDef
]
ImageCustomActionUnionTypeDef = Union[ImageCustomActionTypeDef, ImageCustomActionOutputTypeDef]
LayerCustomActionUnionTypeDef = Union[LayerCustomActionTypeDef, LayerCustomActionOutputTypeDef]


class BoxPlotVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[BoxPlotChartConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class ComboChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[ComboChartConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class CustomContentVisualTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[CustomContentConfigurationTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class EmptyVisualTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]


class FunnelChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[FunnelChartConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class GaugeChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GaugeChartConfigurationUnionTypeDef]
    ConditionalFormatting: NotRequired[GaugeChartConditionalFormattingUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class GeospatialMapVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GeospatialMapConfigurationUnionTypeDef]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class HeatMapVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[HeatMapConfigurationUnionTypeDef]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class HistogramVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[HistogramConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class InsightVisualTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    InsightConfiguration: NotRequired[InsightConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class KPIVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[KPIConfigurationUnionTypeDef]
    ConditionalFormatting: NotRequired[KPIConditionalFormattingUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyUnionTypeDef]]
    VisualContentAltText: NotRequired[str]


class LineChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[LineChartConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class PieChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PieChartConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyUnionTypeDef]]
    VisualContentAltText: NotRequired[str]


class RadarChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[RadarChartConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class SankeyDiagramVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[SankeyDiagramChartConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class ScatterPlotVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[ScatterPlotConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class TreeMapVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[TreeMapConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


VisualCustomActionUnionTypeDef = Union[VisualCustomActionTypeDef, VisualCustomActionOutputTypeDef]


class WaterfallVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[WaterfallChartConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class WordCloudVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[WordCloudChartConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    VisualContentAltText: NotRequired[str]


class BatchCreateTopicReviewedAnswerRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TopicId: str
    Answers: Sequence[CreateTopicReviewedAnswerTypeDef]


class NestedFilterTypeDef(TypedDict):
    FilterId: str
    Column: ColumnIdentifierTypeDef
    IncludeInnerSet: bool
    InnerFilter: InnerFilterUnionTypeDef


FilledMapConditionalFormattingUnionTypeDef = Union[
    FilledMapConditionalFormattingTypeDef, FilledMapConditionalFormattingOutputTypeDef
]
PivotTableConditionalFormattingUnionTypeDef = Union[
    PivotTableConditionalFormattingTypeDef, PivotTableConditionalFormattingOutputTypeDef
]
TableConditionalFormattingUnionTypeDef = Union[
    TableConditionalFormattingTypeDef, TableConditionalFormattingOutputTypeDef
]


class AnalysisDefinitionOutputTypeDef(TypedDict):
    DataSetIdentifierDeclarations: List[DataSetIdentifierDeclarationTypeDef]
    Sheets: NotRequired[List[SheetDefinitionOutputTypeDef]]
    CalculatedFields: NotRequired[List[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[List[ParameterDeclarationOutputTypeDef]]
    FilterGroups: NotRequired[List[FilterGroupOutputTypeDef]]
    ColumnConfigurations: NotRequired[List[ColumnConfigurationOutputTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsTypeDef]
    QueryExecutionOptions: NotRequired[QueryExecutionOptionsTypeDef]
    StaticFiles: NotRequired[List[StaticFileTypeDef]]


class DashboardVersionDefinitionOutputTypeDef(TypedDict):
    DataSetIdentifierDeclarations: List[DataSetIdentifierDeclarationTypeDef]
    Sheets: NotRequired[List[SheetDefinitionOutputTypeDef]]
    CalculatedFields: NotRequired[List[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[List[ParameterDeclarationOutputTypeDef]]
    FilterGroups: NotRequired[List[FilterGroupOutputTypeDef]]
    ColumnConfigurations: NotRequired[List[ColumnConfigurationOutputTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsTypeDef]
    StaticFiles: NotRequired[List[StaticFileTypeDef]]


class TemplateVersionDefinitionOutputTypeDef(TypedDict):
    DataSetConfigurations: List[DataSetConfigurationOutputTypeDef]
    Sheets: NotRequired[List[SheetDefinitionOutputTypeDef]]
    CalculatedFields: NotRequired[List[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[List[ParameterDeclarationOutputTypeDef]]
    FilterGroups: NotRequired[List[FilterGroupOutputTypeDef]]
    ColumnConfigurations: NotRequired[List[ColumnConfigurationOutputTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsTypeDef]
    QueryExecutionOptions: NotRequired[QueryExecutionOptionsTypeDef]
    StaticFiles: NotRequired[List[StaticFileTypeDef]]


class LayoutConfigurationTypeDef(TypedDict):
    GridLayout: NotRequired[GridLayoutConfigurationUnionTypeDef]
    FreeFormLayout: NotRequired[FreeFormLayoutConfigurationUnionTypeDef]
    SectionBasedLayout: NotRequired[SectionBasedLayoutConfigurationUnionTypeDef]


class SheetImageTypeDef(TypedDict):
    SheetImageId: str
    Source: SheetImageSourceTypeDef
    Scaling: NotRequired[SheetImageScalingConfigurationTypeDef]
    Tooltip: NotRequired[SheetImageTooltipConfigurationTypeDef]
    ImageContentAltText: NotRequired[str]
    Interactions: NotRequired[ImageInteractionOptionsTypeDef]
    Actions: NotRequired[Sequence[ImageCustomActionUnionTypeDef]]


class GeospatialLayerItemTypeDef(TypedDict):
    LayerId: str
    LayerType: NotRequired[GeospatialLayerTypeType]
    DataSource: NotRequired[GeospatialDataSourceItemTypeDef]
    Label: NotRequired[str]
    Visibility: NotRequired[VisibilityType]
    LayerDefinition: NotRequired[GeospatialLayerDefinitionUnionTypeDef]
    Tooltip: NotRequired[TooltipOptionsUnionTypeDef]
    JoinDefinition: NotRequired[GeospatialLayerJoinDefinitionUnionTypeDef]
    Actions: NotRequired[Sequence[LayerCustomActionUnionTypeDef]]


BoxPlotVisualUnionTypeDef = Union[BoxPlotVisualTypeDef, BoxPlotVisualOutputTypeDef]
ComboChartVisualUnionTypeDef = Union[ComboChartVisualTypeDef, ComboChartVisualOutputTypeDef]
CustomContentVisualUnionTypeDef = Union[
    CustomContentVisualTypeDef, CustomContentVisualOutputTypeDef
]
EmptyVisualUnionTypeDef = Union[EmptyVisualTypeDef, EmptyVisualOutputTypeDef]
FunnelChartVisualUnionTypeDef = Union[FunnelChartVisualTypeDef, FunnelChartVisualOutputTypeDef]
GaugeChartVisualUnionTypeDef = Union[GaugeChartVisualTypeDef, GaugeChartVisualOutputTypeDef]
GeospatialMapVisualUnionTypeDef = Union[
    GeospatialMapVisualTypeDef, GeospatialMapVisualOutputTypeDef
]
HeatMapVisualUnionTypeDef = Union[HeatMapVisualTypeDef, HeatMapVisualOutputTypeDef]
HistogramVisualUnionTypeDef = Union[HistogramVisualTypeDef, HistogramVisualOutputTypeDef]
InsightVisualUnionTypeDef = Union[InsightVisualTypeDef, InsightVisualOutputTypeDef]
KPIVisualUnionTypeDef = Union[KPIVisualTypeDef, KPIVisualOutputTypeDef]
LineChartVisualUnionTypeDef = Union[LineChartVisualTypeDef, LineChartVisualOutputTypeDef]
PieChartVisualUnionTypeDef = Union[PieChartVisualTypeDef, PieChartVisualOutputTypeDef]
RadarChartVisualUnionTypeDef = Union[RadarChartVisualTypeDef, RadarChartVisualOutputTypeDef]
SankeyDiagramVisualUnionTypeDef = Union[
    SankeyDiagramVisualTypeDef, SankeyDiagramVisualOutputTypeDef
]
ScatterPlotVisualUnionTypeDef = Union[ScatterPlotVisualTypeDef, ScatterPlotVisualOutputTypeDef]
TreeMapVisualUnionTypeDef = Union[TreeMapVisualTypeDef, TreeMapVisualOutputTypeDef]


class BarChartVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[BarChartConfigurationUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionUnionTypeDef]]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyUnionTypeDef]]
    VisualContentAltText: NotRequired[str]


WaterfallVisualUnionTypeDef = Union[WaterfallVisualTypeDef, WaterfallVisualOutputTypeDef]
WordCloudVisualUnionTypeDef = Union[WordCloudVisualTypeDef, WordCloudVisualOutputTypeDef]
NestedFilterUnionTypeDef = Union[NestedFilterTypeDef, NestedFilterOutputTypeDef]


class FilledMapVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[FilledMapConfigurationUnionTypeDef]
    ConditionalFormatting: NotRequired[FilledMapConditionalFormattingUnionTypeDef]
    ColumnHierarchies: NotRequired[Sequence[ColumnHierarchyTypeDef]]
    Actions: NotRequired[Sequence[VisualCustomActionTypeDef]]
    VisualContentAltText: NotRequired[str]


class PivotTableVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[PivotTableConfigurationUnionTypeDef]
    ConditionalFormatting: NotRequired[PivotTableConditionalFormattingUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionUnionTypeDef]]
    VisualContentAltText: NotRequired[str]


class TableVisualTypeDef(TypedDict):
    VisualId: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[TableConfigurationUnionTypeDef]
    ConditionalFormatting: NotRequired[TableConditionalFormattingUnionTypeDef]
    Actions: NotRequired[Sequence[VisualCustomActionUnionTypeDef]]
    VisualContentAltText: NotRequired[str]


class DescribeAnalysisDefinitionResponseTypeDef(TypedDict):
    AnalysisId: str
    Name: str
    Errors: List[AnalysisErrorTypeDef]
    ResourceStatus: ResourceStatusType
    ThemeArn: str
    Definition: AnalysisDefinitionOutputTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDashboardDefinitionResponseTypeDef(TypedDict):
    DashboardId: str
    Errors: List[DashboardErrorTypeDef]
    Name: str
    ResourceStatus: ResourceStatusType
    ThemeArn: str
    Definition: DashboardVersionDefinitionOutputTypeDef
    Status: int
    RequestId: str
    DashboardPublishOptions: DashboardPublishOptionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTemplateDefinitionResponseTypeDef(TypedDict):
    Name: str
    TemplateId: str
    Errors: List[TemplateErrorTypeDef]
    ResourceStatus: ResourceStatusType
    ThemeArn: str
    Definition: TemplateVersionDefinitionOutputTypeDef
    Status: int
    RequestId: str
    ResponseMetadata: ResponseMetadataTypeDef


LayoutConfigurationUnionTypeDef = Union[
    LayoutConfigurationTypeDef, LayoutConfigurationOutputTypeDef
]
SheetImageUnionTypeDef = Union[SheetImageTypeDef, SheetImageOutputTypeDef]
GeospatialLayerItemUnionTypeDef = Union[
    GeospatialLayerItemTypeDef, GeospatialLayerItemOutputTypeDef
]
BarChartVisualUnionTypeDef = Union[BarChartVisualTypeDef, BarChartVisualOutputTypeDef]


class FilterTypeDef(TypedDict):
    CategoryFilter: NotRequired[CategoryFilterUnionTypeDef]
    NumericRangeFilter: NotRequired[NumericRangeFilterUnionTypeDef]
    NumericEqualityFilter: NotRequired[NumericEqualityFilterUnionTypeDef]
    TimeEqualityFilter: NotRequired[TimeEqualityFilterUnionTypeDef]
    TimeRangeFilter: NotRequired[TimeRangeFilterUnionTypeDef]
    RelativeDatesFilter: NotRequired[RelativeDatesFilterUnionTypeDef]
    TopBottomFilter: NotRequired[TopBottomFilterUnionTypeDef]
    NestedFilter: NotRequired[NestedFilterUnionTypeDef]


FilledMapVisualUnionTypeDef = Union[FilledMapVisualTypeDef, FilledMapVisualOutputTypeDef]
PivotTableVisualUnionTypeDef = Union[PivotTableVisualTypeDef, PivotTableVisualOutputTypeDef]
TableVisualUnionTypeDef = Union[TableVisualTypeDef, TableVisualOutputTypeDef]


class LayoutTypeDef(TypedDict):
    Configuration: LayoutConfigurationUnionTypeDef


class GeospatialLayerMapConfigurationTypeDef(TypedDict):
    Legend: NotRequired[LegendOptionsTypeDef]
    MapLayers: NotRequired[Sequence[GeospatialLayerItemUnionTypeDef]]
    MapState: NotRequired[GeospatialMapStateTypeDef]
    MapStyle: NotRequired[GeospatialMapStyleTypeDef]
    Interactions: NotRequired[VisualInteractionOptionsTypeDef]


FilterUnionTypeDef = Union[FilterTypeDef, FilterOutputTypeDef]
LayoutUnionTypeDef = Union[LayoutTypeDef, LayoutOutputTypeDef]
GeospatialLayerMapConfigurationUnionTypeDef = Union[
    GeospatialLayerMapConfigurationTypeDef, GeospatialLayerMapConfigurationOutputTypeDef
]


class FilterGroupTypeDef(TypedDict):
    FilterGroupId: str
    Filters: Sequence[FilterUnionTypeDef]
    ScopeConfiguration: FilterScopeConfigurationUnionTypeDef
    CrossDataset: CrossDatasetTypesType
    Status: NotRequired[WidgetStatusType]


class LayerMapVisualTypeDef(TypedDict):
    VisualId: str
    DataSetIdentifier: str
    Title: NotRequired[VisualTitleLabelOptionsTypeDef]
    Subtitle: NotRequired[VisualSubtitleLabelOptionsTypeDef]
    ChartConfiguration: NotRequired[GeospatialLayerMapConfigurationUnionTypeDef]
    VisualContentAltText: NotRequired[str]


FilterGroupUnionTypeDef = Union[FilterGroupTypeDef, FilterGroupOutputTypeDef]
LayerMapVisualUnionTypeDef = Union[LayerMapVisualTypeDef, LayerMapVisualOutputTypeDef]


class VisualTypeDef(TypedDict):
    TableVisual: NotRequired[TableVisualUnionTypeDef]
    PivotTableVisual: NotRequired[PivotTableVisualUnionTypeDef]
    BarChartVisual: NotRequired[BarChartVisualUnionTypeDef]
    KPIVisual: NotRequired[KPIVisualUnionTypeDef]
    PieChartVisual: NotRequired[PieChartVisualUnionTypeDef]
    GaugeChartVisual: NotRequired[GaugeChartVisualUnionTypeDef]
    LineChartVisual: NotRequired[LineChartVisualUnionTypeDef]
    HeatMapVisual: NotRequired[HeatMapVisualUnionTypeDef]
    TreeMapVisual: NotRequired[TreeMapVisualUnionTypeDef]
    GeospatialMapVisual: NotRequired[GeospatialMapVisualUnionTypeDef]
    FilledMapVisual: NotRequired[FilledMapVisualUnionTypeDef]
    LayerMapVisual: NotRequired[LayerMapVisualUnionTypeDef]
    FunnelChartVisual: NotRequired[FunnelChartVisualUnionTypeDef]
    ScatterPlotVisual: NotRequired[ScatterPlotVisualUnionTypeDef]
    ComboChartVisual: NotRequired[ComboChartVisualUnionTypeDef]
    BoxPlotVisual: NotRequired[BoxPlotVisualUnionTypeDef]
    WaterfallVisual: NotRequired[WaterfallVisualUnionTypeDef]
    HistogramVisual: NotRequired[HistogramVisualUnionTypeDef]
    WordCloudVisual: NotRequired[WordCloudVisualUnionTypeDef]
    InsightVisual: NotRequired[InsightVisualUnionTypeDef]
    SankeyDiagramVisual: NotRequired[SankeyDiagramVisualUnionTypeDef]
    CustomContentVisual: NotRequired[CustomContentVisualUnionTypeDef]
    EmptyVisual: NotRequired[EmptyVisualUnionTypeDef]
    RadarChartVisual: NotRequired[RadarChartVisualUnionTypeDef]
    PluginVisual: NotRequired[PluginVisualUnionTypeDef]


VisualUnionTypeDef = Union[VisualTypeDef, VisualOutputTypeDef]


class SheetDefinitionTypeDef(TypedDict):
    SheetId: str
    Title: NotRequired[str]
    Description: NotRequired[str]
    Name: NotRequired[str]
    ParameterControls: NotRequired[Sequence[ParameterControlUnionTypeDef]]
    FilterControls: NotRequired[Sequence[FilterControlUnionTypeDef]]
    Visuals: NotRequired[Sequence[VisualUnionTypeDef]]
    TextBoxes: NotRequired[Sequence[SheetTextBoxTypeDef]]
    Images: NotRequired[Sequence[SheetImageUnionTypeDef]]
    Layouts: NotRequired[Sequence[LayoutUnionTypeDef]]
    SheetControlLayouts: NotRequired[Sequence[SheetControlLayoutUnionTypeDef]]
    ContentType: NotRequired[SheetContentTypeType]


SheetDefinitionUnionTypeDef = Union[SheetDefinitionTypeDef, SheetDefinitionOutputTypeDef]


class AnalysisDefinitionTypeDef(TypedDict):
    DataSetIdentifierDeclarations: Sequence[DataSetIdentifierDeclarationTypeDef]
    Sheets: NotRequired[Sequence[SheetDefinitionUnionTypeDef]]
    CalculatedFields: NotRequired[Sequence[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[Sequence[ParameterDeclarationUnionTypeDef]]
    FilterGroups: NotRequired[Sequence[FilterGroupUnionTypeDef]]
    ColumnConfigurations: NotRequired[Sequence[ColumnConfigurationUnionTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsTypeDef]
    QueryExecutionOptions: NotRequired[QueryExecutionOptionsTypeDef]
    StaticFiles: NotRequired[Sequence[StaticFileTypeDef]]


class DashboardVersionDefinitionTypeDef(TypedDict):
    DataSetIdentifierDeclarations: Sequence[DataSetIdentifierDeclarationTypeDef]
    Sheets: NotRequired[Sequence[SheetDefinitionUnionTypeDef]]
    CalculatedFields: NotRequired[Sequence[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[Sequence[ParameterDeclarationUnionTypeDef]]
    FilterGroups: NotRequired[Sequence[FilterGroupUnionTypeDef]]
    ColumnConfigurations: NotRequired[Sequence[ColumnConfigurationUnionTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsTypeDef]
    StaticFiles: NotRequired[Sequence[StaticFileTypeDef]]


class TemplateVersionDefinitionTypeDef(TypedDict):
    DataSetConfigurations: Sequence[DataSetConfigurationUnionTypeDef]
    Sheets: NotRequired[Sequence[SheetDefinitionUnionTypeDef]]
    CalculatedFields: NotRequired[Sequence[CalculatedFieldTypeDef]]
    ParameterDeclarations: NotRequired[Sequence[ParameterDeclarationUnionTypeDef]]
    FilterGroups: NotRequired[Sequence[FilterGroupUnionTypeDef]]
    ColumnConfigurations: NotRequired[Sequence[ColumnConfigurationUnionTypeDef]]
    AnalysisDefaults: NotRequired[AnalysisDefaultsTypeDef]
    Options: NotRequired[AssetOptionsTypeDef]
    QueryExecutionOptions: NotRequired[QueryExecutionOptionsTypeDef]
    StaticFiles: NotRequired[Sequence[StaticFileTypeDef]]


class CreateAnalysisRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str
    Name: str
    Parameters: NotRequired[ParametersTypeDef]
    Permissions: NotRequired[Sequence[ResourcePermissionUnionTypeDef]]
    SourceEntity: NotRequired[AnalysisSourceEntityTypeDef]
    ThemeArn: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    Definition: NotRequired[AnalysisDefinitionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]
    FolderArns: NotRequired[Sequence[str]]


class UpdateAnalysisRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    AnalysisId: str
    Name: str
    Parameters: NotRequired[ParametersTypeDef]
    SourceEntity: NotRequired[AnalysisSourceEntityTypeDef]
    ThemeArn: NotRequired[str]
    Definition: NotRequired[AnalysisDefinitionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]


class CreateDashboardRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    Name: str
    Parameters: NotRequired[ParametersTypeDef]
    Permissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    SourceEntity: NotRequired[DashboardSourceEntityTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    VersionDescription: NotRequired[str]
    DashboardPublishOptions: NotRequired[DashboardPublishOptionsTypeDef]
    ThemeArn: NotRequired[str]
    Definition: NotRequired[DashboardVersionDefinitionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]
    FolderArns: NotRequired[Sequence[str]]
    LinkSharingConfiguration: NotRequired[LinkSharingConfigurationTypeDef]
    LinkEntities: NotRequired[Sequence[str]]


class UpdateDashboardRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    DashboardId: str
    Name: str
    SourceEntity: NotRequired[DashboardSourceEntityTypeDef]
    Parameters: NotRequired[ParametersTypeDef]
    VersionDescription: NotRequired[str]
    DashboardPublishOptions: NotRequired[DashboardPublishOptionsTypeDef]
    ThemeArn: NotRequired[str]
    Definition: NotRequired[DashboardVersionDefinitionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]


class CreateTemplateRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    Name: NotRequired[str]
    Permissions: NotRequired[Sequence[ResourcePermissionTypeDef]]
    SourceEntity: NotRequired[TemplateSourceEntityTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]
    VersionDescription: NotRequired[str]
    Definition: NotRequired[TemplateVersionDefinitionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]


class UpdateTemplateRequestRequestTypeDef(TypedDict):
    AwsAccountId: str
    TemplateId: str
    SourceEntity: NotRequired[TemplateSourceEntityTypeDef]
    VersionDescription: NotRequired[str]
    Name: NotRequired[str]
    Definition: NotRequired[TemplateVersionDefinitionTypeDef]
    ValidationStrategy: NotRequired[ValidationStrategyTypeDef]
