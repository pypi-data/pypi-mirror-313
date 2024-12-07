from easy_spark.easy_con_opetator import EasyConOperator


class EasyConValue:
    def __init__(self, value: any, operator: EasyConOperator):
        self.value = value
        self.operator = operator
