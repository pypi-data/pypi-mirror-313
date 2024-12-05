import math

def handle_single_argument(operator, a):
    match operator:
        case "+" : return a
        case "-" : return -a
        case "*" : return a * a
        case "/" : raise ValueError("Can't divide by zero")
        case "^"|"**"|"power"|"pow" : return math.e ** a
        case "sqrt"|"square_root" : return (a) ** (1/2)
        case "log" : return math.log(a)
        case "sin" : return math.sin(a)
        case "cos" : return math.cos(a)
        case "tan" : return math.tan(a)
        case _ : raise ValueError(f"Invalid operator for single argument: {operator}")

def calutions(a, operator="+", b=None):
    if b is None:
        return handle_single_argument(operator, a)

    match operator:
        case "+" : return a + b
        case "-" : return a - b
        case "*" : return a * b
        case "/" :
            if b == 0:
                raise ValueError("Can't divide by zero")
            return a / b
        case "^"|"**"|"power"|"pow" : return a ** b
        case "sqrt"|"square_root" : 
            if b == 0 :
                raise ValueError("Invalid argument for square root")
            return (a) ** (1/b)
        case "log" : return math.log(a, b)
        case "sin" | "cos" | "tan" : raise ValueError("Too many arguments")
        case ">" : return a > b
        case "<" : return a < b
        case "="|"==" : return a == b
        case "!=" : return a != b
        case ">=" : return a >= b
        case "<=" : return a <= b
        case _ : raise ValueError(f"Invalid operator: {operator}")

cal_info = {
    "type": "function",
    "function": {
        "name": "calutions",
        "description": """一个综合计算器，用于执行多种数学运算。函数接受三个参数：`a`、`b` 和 `operator`。\
            其中，`a` 是必填参数，`b` 和 `operator` 有默认值。""",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                     "type": "float",
                     "description": "运算中的第一个变量，例如计算`2+3`，2就是a，即第一个变量。"
                     },
                "b": {
                     "type": "float",
                     "description": "运算中的第二个数值，不是所有运算都需要第二个数值，例如例如比较是否相等的`=`运算就需要两个数值进行比较。在无需第二个数值的运算中，b需要等于None。"
                     },
                "operator": {
                    "type": "string",
                    "enum": ["+", "-", "*", "/", "^", "sqrt", "log", "sin", "cos", "tan", ">", "<", "=", "!=", ">=", "<="],
                    "description": "可以进行加减乘除、幂运算、开方运算、底数运算、三角函数、大于、小于、等于、不等于、大于等于、小于等于等运算，例如`^`为幂运算。"
                    }
            },
            "required": ["a", "b", "operator"]
        }
    }
}