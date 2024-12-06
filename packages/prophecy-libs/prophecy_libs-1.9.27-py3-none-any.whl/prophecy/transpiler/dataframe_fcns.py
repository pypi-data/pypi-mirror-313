from pyspark.sql import column, DataFrame
from prophecy.transpiler.abi_base import ScalaUtil
from prophecy.utils import ProphecyDataFrame
from prophecy.libs.utils import createScalaOption


def readFixedFile(schema, path):
    spark = ScalaUtil.getAbiLib().spark
    df = spark.sparkContext._jvm.io.prophecy.libs.FixedFileFormatImplicits.readFixedFile(spark._jsparkSession, schema,
                                                                                         path)
    return DataFrame(df, ScalaUtil.getAbiLib().sqlContext)


def writeFixedFile(df, schema, path, mode="overwrite"):
    spark = ScalaUtil.getAbiLib().spark
    spark.sparkContext._jvm.io.prophecy.libs.FixedFileFormatImplicits.writeFixedFile(df._jdf, schema, path,
                                                                                     createScalaOption(spark, None),
                                                                                     createScalaOption(spark, None),
                                                                                     createScalaOption(spark, None),
                                                                                     _getSaveMode(spark, mode))


def _getSaveMode(spark, mode):
    if mode == "ignore":
        return spark.sparkContext._jvm.org.apache.spark.sql.SaveMode.Ignore
    elif mode == "append":
        return spark.sparkContext._jvm.org.apache.spark.sql.SaveMode.Append
    elif mode == "overwrite":
        return spark.sparkContext._jvm.org.apache.spark.sql.SaveMode.Overwrite

    return spark.sparkContext._jvm.org.apache.spark.sql.SaveMode.ErrorIfExists


def getMTimeDataframe(filepath, format, spark) -> DataFrame:
    df = ScalaUtil.getAbiLib().libs.getMTimeDataframe(filepath, format, spark._jsparkSession)
    return DataFrame(df, ScalaUtil.getAbiLib().sqlContext)


def getEmptyLogDataFrame(spark) -> DataFrame:
    df = ScalaUtil.getAbiLib().libs.getEmptyLogDataFrame(spark._jsparkSession)
    return DataFrame(df, ScalaUtil.getAbiLib().sqlContext)


def collectDataFrameColumnsToApplyFilter(
        df,
        spark,
        columnList,
        filterSourceDataFrame
) -> DataFrame:
    return ProphecyDataFrame(df, spark).collectDataFrameColumnsToApplyFilter(
        columnList,
        filterSourceDataFrame
    )


def normalize(
        df,
        spark,
        lengthExpression,
        finishedExpression,
        finishedCondition,
        alias,
        colsToSelect,
        tempWindowExpr,
        lengthRelatedGlobalExpressions={}
) -> DataFrame:
    return ProphecyDataFrame(df, spark).normalize(
        lengthExpression,
        finishedExpression,
        finishedCondition,
        alias,
        colsToSelect,
        tempWindowExpr,
        lengthRelatedGlobalExpressions
    )


def denormalizeSorted(
        df,
        spark,
        groupByColumns,
        orderByColumns,
        denormalizeRecordExpression,
        finalizeExpressionMap,
        inputFilter,
        outputFilter,
        denormColumnName,
        countColumnName="count") -> DataFrame:
    return ProphecyDataFrame(df, spark).denormalizeSorted(
        groupByColumns,
        orderByColumns,
        denormalizeRecordExpression,
        finalizeExpressionMap,
        inputFilter,
        outputFilter,
        denormColumnName,
        countColumnName)


def readSeparatedValues(
        df,
        spark,
        inputColumn,
        outputSchemaColumns,
        recordSeparator,
        fieldSeparator
) -> DataFrame:
    return ProphecyDataFrame(df, spark).readSeparatedValues(
        inputColumn,
        outputSchemaColumns,
        recordSeparator,
        fieldSeparator
    )


def syncDataFrameColumnsWithSchema(df, spark, columnNames) -> DataFrame:
    return ProphecyDataFrame(df, spark).syncDataFrameColumnsWithSchema(columnNames)


def zipWithIndex(
        df,
        startValue,
        incrementBy,
        indexColName,
        sparkSession
) -> DataFrame:
    return ProphecyDataFrame(df, sparkSession).zipWithIndex(
        startValue,
        incrementBy,
        indexColName,
        sparkSession
    )


def metaPivot(
        df,
        pivotColumns,
        nameField,
        valueField,
        sparkSession
) -> DataFrame:
    return ProphecyDataFrame(df, sparkSession).metaPivot(
        pivotColumns,
        nameField,
        valueField,
        sparkSession
    )


def compareRecords(df, otherDataFrame, componentName, limit, sparkSession) -> DataFrame:
    return ProphecyDataFrame(df, sparkSession).compareRecords(otherDataFrame, componentName, limit, sparkSession)


def generateSurrogateKeys(
        df,
        keyDF,
        naturalKeys,
        surrogateKey,
        overrideSurrogateKeys,
        computeOldPortOutput,
        spark
) -> (DataFrame, DataFrame, DataFrame):
    return ProphecyDataFrame(df, spark).generateSurrogateKeys(
        keyDF,
        naturalKeys,
        surrogateKey,
        overrideSurrogateKeys,
        computeOldPortOutput,
        spark
    )


def generateLogOutput(
        df,
        sparkSession,
        componentName,
        subComponentName="",
        perRowEventTypes=None,
        perRowEventTexts=None,
        inputRowCount=0,
        outputRowCount=0,
        finalLogEventType=None,
        finalLogEventText=None,
        finalEventExtraColumnMap={}
) -> DataFrame:
    return ProphecyDataFrame(df, sparkSession).generateLogOutput(
        componentName,
        subComponentName,
        perRowEventTypes,
        perRowEventTexts,
        inputRowCount,
        outputRowCount,
        finalLogEventType,
        finalLogEventText,
        finalEventExtraColumnMap,
        sparkSession
    )


def mergeMultipleFileContentInDataFrame(
        df,
        fileNameDF,
        spark,
        delimiter,
        readFormat,
        joinWithInputDataframe,
        outputSchema=None,
        ffSchema=None,
        abinitioSchema=None
) -> DataFrame:
    return ProphecyDataFrame(df, spark).mergeMultipleFileContentInDataFrame(
        fileNameDF,
        spark,
        delimiter,
        readFormat,
        joinWithInputDataframe,
        outputSchema,
        ffSchema,
        abinitioSchema
    )


def breakAndWriteDataFrameForOutputFile(
        df,
        spark,
        outputColumns,
        fileColumnName,
        format,
        delimiter
) -> DataFrame:
    return ProphecyDataFrame(df, spark).breakAndWriteDataFrameForOutputFile(
        outputColumns,
        fileColumnName,
        format,
        delimiter
    )
