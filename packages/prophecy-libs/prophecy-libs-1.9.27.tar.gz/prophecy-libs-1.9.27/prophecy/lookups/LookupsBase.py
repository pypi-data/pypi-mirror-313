# WARNING - Do not add import * in this module

from typing import List, Optional

from pyspark.sql import SparkSession
from pyspark.sql.column import Column
from pyspark.sql.functions import DataFrame


class LookupsBase:
    sparkSession = None
    UDFUtils = None

    def __init__(self, spark):
        self.UDFUtils = spark.sparkContext._jvm.io.prophecy.libs.python.UDFUtils
        self.sparkSession = spark


lookupConfig: Optional[LookupsBase] = None


class LookupCondition:
    lookupColumn = ""
    comparisonOp = ""
    inputParam = ""

    def __init__(self, lookupColumn, camparisonOp, inputParam):
        self.lookupColumn = lookupColumn
        self.comparisonOp = camparisonOp
        self.inputParam = inputParam


def initializeLookups(spark):
    global lookupConfig
    if lookupConfig is None:
        lookupConfig = LookupsBase(spark)
    return lookupConfig


def createScalaList(_list, spark):
    return spark.sparkContext._jvm.PythonUtils.toList(_list)


def createLookup(
    name: str,
    df: DataFrame,
    spark: SparkSession,
    keyCols: List[str],
    valueCols: List[str],
):
    initializeLookups(spark)
    keyColumns = createScalaList(keyCols, spark)
    valueColumns = createScalaList(valueCols, spark)
    lookupConfig.UDFUtils.createLookup(
        name, df._jdf, spark._jsparkSession, keyColumns, valueColumns
    )


def createRangeLookup(
    name: str,
    df: DataFrame,
    spark: SparkSession,
    minColumn: str,
    maxColumn: str,
    valueColumns: List[str],
):
    initializeLookups(spark)
    valueColumns = createScalaList(valueColumns, spark)
    lookupConfig.UDFUtils.createRangeLookup(
        name, df._jdf, spark._jsparkSession, minColumn, maxColumn, valueColumns
    )


def createScalaConditionsList(conditions: List[LookupCondition], spark):
    scalaConditions = []
    for condition in conditions:
        sConditions = lookupConfig.UDFUtils.LookupCondition(condition.lookupColumn, condition.comparisonOp, condition.inputParam)
        scalaConditions.append(sConditions)
    return spark.sparkContext._jvm.PythonUtils.toList(scalaConditions)


def createExtendedLookup(
        name: str,
        df: DataFrame,
        spark: SparkSession,
        conditions: List[LookupCondition],
        inputParams: List[str],
        valueColumns: List[str],
):
    initializeLookups(spark)
    conditions = createScalaConditionsList(conditions, spark)
    inputParams = createScalaList(inputParams, spark)
    valueColumns = createScalaList(valueColumns, spark)

    lookupConfig.UDFUtils.createExtendedLookup(
        name, df._jdf, spark._jsparkSession, conditions, inputParams, valueColumns
    )


def lookup(lookupName: str, *cols):
    if lookupConfig is None:
        raise Exception(f"Lookup: `{lookupName}` is being used but not initialised.")
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup(lookupName, _cols)
    return Column(lookupResult)

def extended_lookup(lookupName: str, *cols):
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.extended_lookup(lookupName, _cols)
    return Column(lookupResult)


def lookup_last(lookupName: str, *cols):
    if lookupConfig is None:
        raise Exception(f"Lookup: `{lookupName}` is being used but not initialised.")
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_last(lookupName, _cols)
    return Column(lookupResult)


def lookup_match(lookupName: str, *cols):
    if lookupConfig is None:
        raise Exception(f"Lookup: `{lookupName}` is being used but not initialised.")
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_match(lookupName, _cols)
    return Column(lookupResult)


def lookup_count(lookupName: str, *cols):
    if lookupConfig is None:
        raise Exception(f"Lookup: `{lookupName}` is being used but not initialised.")
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_count(lookupName, _cols)
    return Column(lookupResult)


def lookup_row(lookupName: str, *cols):
    if lookupConfig is None:
        raise Exception(f"Lookup: `{lookupName}` is being used but not initialised.")
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_row(lookupName, _cols)
    return Column(lookupResult)


def lookup_row_reverse(lookupName: str, *cols):
    if lookupConfig is None:
        raise Exception(f"Lookup: `{lookupName}` is being used but not initialised.")
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_row_reverse(lookupName, _cols)
    return Column(lookupResult)


def lookup_nth(lookupName: str, *cols):
    if lookupConfig is None:
        raise Exception(f"Lookup: `{lookupName}` is being used but not initialised.")
    _cols = createScalaList(
        [item._jc for item in list(cols)], lookupConfig.sparkSession
    )
    lookupResult = lookupConfig.UDFUtils.lookup_nth(lookupName, _cols)
    return Column(lookupResult)
