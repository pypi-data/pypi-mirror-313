import io

import pyspark.sql.types
from pyspark.sql import Column, DataFrame, SQLContext, SparkSession

from prophecy.transpiler.abi_base import ScalaUtil
from prophecy.udfs.scala_udf_wrapper import call_udf


def castArgForScala(item):
    # TODO - this seems enough for now, but needs to be enhanced to handle more complex/nested types
    if isinstance(item, Column):
        return item._jc
    elif isinstance(item, SparkSession):
        return item._jsparkSession
    elif isinstance(item, pyspark.sql.types.StructType):
        return item.json()
    else:
        return item


def decorateColumnFunction(fn):
    spark = ScalaUtil.getAbiLib().spark
    sqlContext = SQLContext(spark.sparkContext, sparkSession=spark)

    def doit(*args):
        newArgs = [castArgForScala(item) for item in list(args)]
        result = fn(*newArgs)
        resultType = result.getClass().getName()
        if resultType == "org.apache.spark.sql.Dataset":
            return DataFrame(result, sqlContext)
        elif resultType == "org.apache.spark.sql.Column":
            return Column(result)
        else:
            return result

    return doit


# Wrapper to call column expression based functions implemented in the SparkFunction trait in scala
def call_spark_fcn(funcName, *args):
    libs = ScalaUtil.getAbiLib().libs
    try:
        func = libs.__getattr__(funcName)  # Check if this is a column function from the ScalaFunctions class
        f = decorateColumnFunction(func)
        return f(*args)
    except:
        return call_udf(funcName, *args)  # This must be a UDF
