from typing import Optional

from pyspark.sql import *
from prophecy.libs.utils import *


class ProphecyDataFrame:
    def __init__(self, df: DataFrame, spark: SparkSession):
        self.jvm = spark.sparkContext._jvm
        self.spark = spark
        self.sqlContext = SQLContext(spark.sparkContext, sparkSession=spark)

        if type(df) == DataFrame:
            try:  # for backward compatibility
                self.extended_dataframe = (
                    self.jvm.org.apache.spark.sql.ProphecyDataFrame.extendedDataFrame(
                        df._jdf
                    )
                )
            except TypeError:
                self.extended_dataframe = (
                    self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
                )
            self.dataframe = df
        else:
            try:
                self.extended_dataframe = (
                    self.jvm.org.apache.spark.sql.ProphecyDataFrame.extendedDataFrame(
                        df._jdf
                    )
                )
            except TypeError:
                self.extended_dataframe = (
                    self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
                )
            self.dataframe = DataFrame(df, self.sqlContext)

    def interim(
            self,
            subgraph,
            component,
            port,
            subPath,
            numRows,
            interimOutput,
            detailedStats=False,
    ) -> DataFrame:
        result = self.extended_dataframe.interim(
            subgraph, component, port, subPath, numRows, interimOutput, detailedStats
        )
        return DataFrame(result, self.sqlContext)

    # Ab Initio extensions to Prophecy DataFrame
    def collectDataFrameColumnsToApplyFilter(
            self,
            columnList,
            filterSourceDataFrame
    ) -> DataFrame:
        result = self.extended_dataframe.collectDataFrameColumnsToApplyFilter(
            createScalaList(self.spark, columnList), filterSourceDataFrame._jdf
        )
        return DataFrame(result, self.sqlContext)

    def normalize(
            self,
            lengthExpression,
            finishedExpression,
            finishedCondition,
            alias,
            colsToSelect,
            tempWindowExpr,
            lengthRelatedGlobalExpressions={}
    ) -> DataFrame:
        result = self.extended_dataframe.normalize(
            createScalaColumnOption(self.spark, lengthExpression),
            createScalaColumnOption(self.spark, finishedExpression),
            createScalaColumnOption(self.spark, finishedCondition),
            alias,
            createScalaColumnList(self.spark, colsToSelect),
            createScalaColumnMap(self.spark, tempWindowExpr),
            createScalaColumnMap(self.spark, lengthRelatedGlobalExpressions)
        )
        return DataFrame(result, self.sqlContext)

    def denormalizeSorted(
            self,
            groupByColumns,
            orderByColumns,
            denormalizeRecordExpression,
            finalizeExpressionMap,
            inputFilter,
            outputFilter,
            denormColumnName,
            countColumnName="count") -> DataFrame:
        result = self.extended_dataframe.denormalizeSorted(
            self,
            createScalaColumnList(self.spark, groupByColumns),
            createScalaColumnList(self.spark, orderByColumns),
            denormalizeRecordExpression,
            createScalaColumnMap(self.spark, finalizeExpressionMap),
            createScalaColumnOption(self.spark, inputFilter),
            createScalaColumnOption(self.spark, outputFilter),
            denormColumnName,
            countColumnName)
        return DataFrame(result, self.sqlContext)

    def readSeparatedValues(
            self,
            inputColumn,
            outputSchemaColumns,
            recordSeparator,
            fieldSeparator
    ) -> DataFrame:
        result = self.extended_dataframe.readSeparatedValues(
            inputColumn._jc,
            createScalaList(self.spark, outputSchemaColumns),
            recordSeparator,
            fieldSeparator
        )
        return DataFrame(result, self.sqlContext)

    def syncDataFrameColumnsWithSchema(self, columnNames) -> DataFrame:
        result = self.extended_dataframe.syncDataFrameColumnsWithSchema(createScalaList(self.spark, columnNames))
        return DataFrame(result, self.sqlContext)

    def zipWithIndex(
            self,
            startValue,
            incrementBy,
            indexColName,
            sparkSession
    ) -> DataFrame:
        result = self.extended_dataframe.zipWithIndex(startValue,
                                                      incrementBy,
                                                      indexColName,
                                                      sparkSession._jsparkSession)
        return DataFrame(result, self.sqlContext)

    def metaPivot(
            self,
            pivotColumns,
            nameField,
            valueField,
            sparkSession
    ) -> DataFrame:
        result = self.extended_dataframe.metaPivot(pivotColumns,
                                                   nameField,
                                                   valueField,
                                                   sparkSession._jsparkSession)
        return DataFrame(result, self.sqlContext)

    def compareRecords(self, otherDataFrame, componentName, limit, sparkSession) -> DataFrame:
        result = self.extended_dataframe.compareRecords(otherDataFrame._jdf,
                                                        componentName,
                                                        limit,
                                                        sparkSession._jsparkSession)
        return DataFrame(result, self.sqlContext)

    def generateSurrogateKeys(
            self,
            keyDF,
            naturalKeys,
            surrogateKey,
            overrideSurrogateKeys,
            computeOldPortOutput,
            spark
    ) -> (DataFrame, DataFrame, DataFrame):
        result = self.extended_dataframe.generateSurrogateKeys(
            keyDF._jdf,
            createScalaList(self.spark, naturalKeys),
            surrogateKey,
            createScalaOption(self.spark, overrideSurrogateKeys),
            computeOldPortOutput,
            spark._jsparkSession)
        result.toString()
        return (DataFrame(result._1(), self.sqlContext), DataFrame(result._2(), self.sqlContext),
                DataFrame(result._3(), self.sqlContext))

    def generateLogOutput(
            self,
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
    ) -> DataFrame:
        result = self.extended_dataframe.generateLogOutput(
            componentName,
            subComponentName,
            createScalaColumnOption(self.spark, perRowEventTypes),
            createScalaColumnOption(self.spark, perRowEventTexts),
            inputRowCount,
            createScalaOption(self.spark, outputRowCount),
            createScalaColumnOption(self.spark, finalLogEventType),
            createScalaColumnOption(self.spark, finalLogEventText),
            createScalaColumnMap(self.spark, finalEventExtraColumnMap),
            sparkSession._jsparkSession
        )

        return DataFrame(result, self.sqlContext)

    def mergeMultipleFileContentInDataFrame(
            self,
            fileNameDF,
            spark,
            delimiter,
            readFormat,
            joinWithInputDataframe,
            outputSchema=None,
            ffSchema=None,
            abinitioSchema=None
    ) -> DataFrame:
        if outputSchema is not None:
            result = self.extended_dataframe.mergeMultipleFileContentInDataFrame(
                fileNameDF._jdf,
                spark._jsparkSession,
                outputSchema.json(),
                delimiter,
                readFormat,
                joinWithInputDataframe,
                createScalaOption(self.spark, ffSchema)
            )
        else:
            result = self.extended_dataframe.mergeMultipleFileContentInDataFrame(
                fileNameDF._jdf,
                spark._jsparkSession,
                abinitioSchema,
                delimiter,
                readFormat,
                joinWithInputDataframe
            )
        return DataFrame(result, self.sqlContext)

    def breakAndWriteDataFrameForOutputFile(
            self,
            outputColumns,
            fileColumnName,
            format,
            delimiter
    ) -> DataFrame:
        result = self.extended_dataframe.breakAndWriteDataFrameForOutputFile(
            createScalaList(self.spark, outputColumns),
            fileColumnName,
            format,
            self.createScalaOption(delimiter))
        return DataFrame(result, self.sqlContext)

    def __getattr__(self, item: str):
        if item == "interim":
            self.interim

        if hasattr(self.extended_dataframe, item):
            return getattr(self.extended_dataframe, item)
        else:
            return getattr(self.dataframe, item)


class InterimConfig:
    def __init__(self):
        self.isInitialized = False
        self.interimOutput = None

    def initialize(self, spark: SparkSession, sessionForInteractive: str = ""):
        self.isInitialized = True
        self.interimOutput = (
            spark.sparkContext._jvm.org.apache.spark.sql.InterimOutputHive2.apply(
                sessionForInteractive
            )
        )

    def maybeInitialize(self, spark: SparkSession, sessionForInteractive: str = ""):
        if not self.isInitialized:
            self.initialize(spark, sessionForInteractive)

    def clear(self):
        self.isInitialized = False
        self.interimOutput = None


interimConfig = InterimConfig()


class ProphecyDebugger:
    @classmethod
    def sparkSqlShow(cls, spark: SparkSession, query: str):
        spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.sparkSqlShow(spark._jsparkSession, query)

    @classmethod
    def sparkSql(cls, spark: SparkSession, query: str):
        jdf = spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.sparkSql(spark._jsparkSession, query)
        return DataFrame(jdf, spark)

    @classmethod
    def exception(cls, spark: SparkSession):
        spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.exception(spark._jsparkSession)

    @classmethod
    def class_details(cls, spark: SparkSession, name: str):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.classDetails(spark._jsparkSession, name)

    @classmethod
    def spark_conf(cls, spark: SparkSession):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.sparkConf(spark._jsparkSession)

    @classmethod
    def runtime_conf(cls, spark: SparkSession):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.runtimeConf(spark._jsparkSession)

    @classmethod
    def local_properties(cls, spark: SparkSession):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.localProperties(spark._jsparkSession)

    @classmethod
    def local_property(cls, spark: SparkSession, key: str):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.localProperty(spark._jsparkSession, key)

    @classmethod
    def local_property_async(cls, spark: SparkSession, key: str):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.localPropertyAsync(spark._jsparkSession,
                                                                                                key)

    @classmethod
    def get_scala_object(cls, spark: SparkSession, className: str):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.getScalaObject(spark._jsparkSession,
                                                                                            className)

    @classmethod
    def call_scala_object_method(cls, spark: SparkSession, className: str, methodName: str, args: list = []):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.callScalaObjectMethod(
            spark._jsparkSession, className, methodName, args)

    @classmethod
    def call_scala_object_method_async(cls, spark: SparkSession, className: str, methodName: str, args: list = []):
        return spark.sparkContext._jvm.org.apache.spark.sql.ProphecyDebugger.callScalaObjectMethodAsync(
            spark._jsparkSession, className, methodName, args)


class MetricsCollector:

    # Called only for interactive execution and metrics mode.
    @classmethod
    def initializeMetrics(cls, spark: SparkSession):
        spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.initializeMetrics(
            spark._jsparkSession
        )

    @classmethod
    def start(
            cls, spark: SparkSession, sessionForInteractive: str = "", pipelineId: str = ""
    ):
        global interimConfig
        interimConfig.maybeInitialize(spark, sessionForInteractive)
        spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.start(
            spark._jsparkSession, pipelineId, sessionForInteractive
        )

    @classmethod
    def end(cls, spark: SparkSession):
        spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.end(
            spark._jsparkSession
        )
        global interimConfig
        interimConfig.clear()


def collectMetrics(
        spark: SparkSession,
        df: DataFrame,
        subgraph: str,
        component: str,
        port: str,
        numRows: int = 40,
) -> DataFrame:
    global interimConfig
    interimConfig.maybeInitialize(spark)
    pdf = ProphecyDataFrame(df, spark)
    return pdf.interim(
        subgraph, component, port, "dummy", numRows, interimConfig.interimOutput
    )


def createEventSendingListener(
        spark: SparkSession, execution_url: str, session: str, scheduled: bool
):
    spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.addSparkListener(
        spark._jsparkSession, execution_url, session, scheduled)


def postDataToSplunk(props: dict, payload):
    import gzip
    import requests
    from requests import HTTPError
    from requests.adapters import HTTPAdapter
    from urllib3 import Retry

    with requests.Session() as session:
        adapter = HTTPAdapter(
            max_retries=Retry(
                total=int(props.get("maxRetries", 4)),
                backoff_factor=float(props.get("backoffFactor", 1)),
                status_forcelist=[429, 500, 502, 503, 504],
            )
        )
        session.mount("http://", adapter)
        session.headers.update(
            {
                "Authorization": "Splunk " + props["token"],
                "Content-Encoding": "gzip",
                "BatchId": props.get("batchId", None),
            }
        )
        res = session.post(
            props["url"], gzip.compress(bytes(payload, encoding="utf8"))
        )
        print(f"IN SESSION URL={props['url']} res.status_code = {res.status_code} res={res.text}")
        if res.status_code != 200 and props.get("stopOnFailure", False):
            raise HTTPError(res.reason)


def splunkHECForEachWriter(props: dict):
    def wrapper(batchDF: DataFrame, batchId: int):
        max_load: Optional[int] = props.get("maxPayload")
        # Take 90% of the payload limit and convert KB into Bytes
        max_load = int(0.9 * 1024 * int(max_load)) if max_load else None
        props.update({"batchId": str(batchId)})

        def f(iterableDF):
            payload, prevsize = "", 0

            for row in iterableDF:
                if max_load and prevsize + len(row) >= max_load:
                    print(f"buffer hit at size {prevsize}")
                    postDataToSplunk(props, payload)
                    payload, prevsize = "", 0
                else:
                    payload += '{"event":' + row + '}'
                    prevsize += len(row) + 10  # 10 bytes is for padding

            if payload:
                print(f"last payload with size {prevsize}")
                postDataToSplunk(props, payload)

        batchDF.toJSON().foreachPartition(f)

    return wrapper
