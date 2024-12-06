from pyspark.sql import DataFrame
from pyspark.sql.functions import lit

from prophecy.libs.utils import createScalaOption, createScalaList
from prophecy.utils import ProphecyDataFrame
from prophecy.utils.transpiler.abi_base import ScalaUtil


def readFixedFile(schema, path,
                  skipHeaderLines=0,
                  skipFooterLines=0,
                  parallelism=1,
                  tmpDir="temp",
                  bufferSize=4096):
    spark = ScalaUtil.getAbiLib().spark
    df = spark.sparkContext._jvm.io.prophecy.libs.FixedFileFormatImplicits.readFixedFile(spark._jsparkSession, schema,
                                                                                         path, skipHeaderLines,
                                                                                         skipFooterLines, parallelism,
                                                                                         tmpDir, bufferSize)
    return DataFrame(df, ScalaUtil.getAbiLib().sqlContext)


def writeFixedFile(df, schema, path, mode="overwrite"):
    spark = ScalaUtil.getAbiLib().spark
    spark.sparkContext._jvm.io.prophecy.libs.FixedFileFormatImplicits.writeFixedFile(df._jdf, schema, path,
                                                                                     createScalaOption(spark, None),
                                                                                     createScalaOption(spark, None),
                                                                                     createScalaOption(spark, None),
                                                                                     _getSaveMode(spark, mode))

def flattenSchema(df, jsonParsedColumnName, distributeColumnsOnType):
    spark = ScalaUtil.getAbiLib().spark
    result = spark.sparkContext._jvm.io.prophecy.alteryx.SparkFunctions.flattenSchema(df._jdf, jsonParsedColumnName, distributeColumnsOnType, spark._jsparkSession)
    return DataFrame(result, ScalaUtil.getAbiLib().sqlContext)

def parseXML(df, xmlStringColumnName, childName, attributeOrChildValues, spark):
    result = spark.sparkContext._jvm.io.prophecy.alteryx.SparkFunctions.parseXML(df._jdf, xmlStringColumnName, childName, createScalaList(spark, attributeOrChildValues), spark._jsparkSession)
    return DataFrame(result, ScalaUtil.getAbiLib().sqlContext)

def buildJson(df, groupByColumns, nameFieldColumn, valueFieldColumn, outputColumn, spark):
    result = spark.sparkContext._jvm.io.prophecy.alteryx.SparkFunctions.buildJson(df._jdf, createScalaList(spark, groupByColumns), nameFieldColumn, valueFieldColumn, outputColumn, spark._jsparkSession)
    return DataFrame(result, ScalaUtil.getAbiLib().sqlContext)

def buildJsonFromPrimitiveCols(df, groupByColumns, nameFieldColumn, stringFieldColumnName, intFieldColumnName, floatFieldColumnName, boolFieldColumnName, outputColumn, spark):
    result = spark.sparkContext._jvm.io.prophecy.alteryx.SparkFunctions.buildJsonFromPrimitiveCols(df._jdf, createScalaList(spark, groupByColumns), nameFieldColumn, stringFieldColumnName, intFieldColumnName, floatFieldColumnName, boolFieldColumnName, outputColumn, spark._jsparkSession)
    return DataFrame(result, ScalaUtil.getAbiLib().sqlContext)

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
        lengthRelatedGlobalExpressions={},
        normalizeRelatedGlobalExpressions={},
        sparkSession = None
) -> DataFrame:
    return ProphecyDataFrame(df, spark).normalize(
        lengthExpression,
        finishedExpression,
        finishedCondition,
        alias,
        colsToSelect,
        tempWindowExpr,
        lengthRelatedGlobalExpressions,
        normalizeRelatedGlobalExpressions,
        sparkSession
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


def fuzzyDedup(
        df, dedupColumnName, threshold, spark, algorithm
) -> DataFrame:
    return ProphecyDataFrame(df, spark).fuzzyDedup(
        dedupColumnName,
        threshold,
        spark,
        algorithm,
    )


def fuzzyPurgeMode(
        df, spark, recordId, threshold, matchFields, includeSimilarityScore=False
) -> DataFrame:
    return ProphecyDataFrame(df, spark).fuzzyPurgeMode(
        recordId=recordId,
        threshold=threshold,
        matchFields=matchFields,
        includeSimilarityScore=includeSimilarityScore
    )


def fuzzyMergeMode(
        df, spark, recordId, sourceId, threshold, matchFields, includeSimilarityScore=False
) -> DataFrame:
    return ProphecyDataFrame(df, spark).fuzzyMergeMode(
        recordId=recordId,
        sourceId=sourceId,
        threshold=threshold,
        matchFields=matchFields,
        includeSimilarityScore=includeSimilarityScore
    )


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


def dynamicReplaceExpr(df, rulesDf, rulesOrderBy, baseColName, replacementExpressionColumnName, replacementValueColumnName, sparkSession) -> DataFrame:
    return ProphecyDataFrame(df, sparkSession).dynamicReplaceExpr(rulesDf._jdf, rulesOrderBy, baseColName, replacementExpressionColumnName, replacementValueColumnName, sparkSession)

def dynamicReplace(df, rulesDf, rulesOrderBy, baseColName, replacementExpressionColumnName, replacementValueColumnName, sparkSession) -> DataFrame:
    return ProphecyDataFrame(df, sparkSession).dynamicReplace(rulesDf._jdf, rulesOrderBy, baseColName, replacementExpressionColumnName, replacementValueColumnName, sparkSession)

def evaluate_expression(df, userExpression, selectedColumnNames, sparkSession) -> DataFrame:
    return ProphecyDataFrame(df, sparkSession).evaluate_expression(userExpression, selectedColumnNames, sparkSession)


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
):
    ProphecyDataFrame(df, spark).breakAndWriteDataFrameForOutputFile(
        outputColumns,
        fileColumnName,
        format,
        delimiter
    )


def breakAndWriteDataFrameForOutputFileWithSchema(
        df,
        spark,
        outputSchema,
        fileColumnName,
        format,
        delimiter=None
):
    ProphecyDataFrame(df, spark).breakAndWriteDataFrameForOutputFileWithSchema(
        outputSchema,
        fileColumnName,
        format,
        delimiter
    )


def readInputFile(spark,
                  inputPath,
                  ffSchemaString,
                  formatType="fixedFormat",
                  delimiter=",",
                  sparkSchema="") -> DataFrame:
    df = ScalaUtil.getAbiLib().libs.readInputFile(spark._jsparkSession, inputPath, ffSchemaString, formatType,
                                                  delimiter, sparkSchema)
    return DataFrame(df, ScalaUtil.getAbiLib().sqlContext)


def writeToOutputFile(
        df,
        spark,
        outputPath,
        ffSchema,
        formatType="fixedFormat",
        delimiter=","
):
    ProphecyDataFrame(df, spark).writeToOutputFile(
        outputPath,
        ffSchema,
        formatType,
        delimiter
    )


def deduplicate(
        df,
        spark,
        typeToKeep,
        groupByColumns=None,
        orderByColumns=None
):
    if groupByColumns is None:
        groupByColumns = [lit(1)]
    if orderByColumns is None:
        orderByColumns = [lit(1)]
    ProphecyDataFrame(df, spark).deduplicate(
        typeToKeep, groupByColumns, orderByColumns
    )
