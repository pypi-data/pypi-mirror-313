from pyspark.sql import Column
import inspect
def get_alias(column: Column):
    try:
        return column._jc.expr().name()
    except:
        return column._jc.expr().sql()

def execute_rule(rule_func):
    """
    Decorator to be used with rule definitions. This will do lazy evaluation of
    default values of rules param.
    """
    def get_value(argument):
        if isinstance(argument, Column):
            return argument
        if callable(argument):
            return argument()
        else:
            return argument
    def wrapper(*args, **kwargs):
        args_with_default = {}
        for (name, param) in inspect.signature(rule_func).parameters.items():
            if param.default is not param.empty:
                args_with_default[name] = param.default
            else:
                args_with_default[name] = None
        to_be_updated_keys = list(args_with_default.keys())[0:len(args)]
        for index in range(len(args)):
            args_with_default.update({to_be_updated_keys[index]: args[index]})
        updated_args = {**args_with_default, **kwargs}
        result = rule_func(**{key: get_value(value) for (key, value) in updated_args.items()})
        return result
    return wrapper