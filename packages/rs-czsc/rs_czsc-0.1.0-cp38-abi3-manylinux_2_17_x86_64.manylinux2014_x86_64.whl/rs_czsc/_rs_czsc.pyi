class PyWeightBacktest:
    @classmethod
    def __init__(cls, *args, **kwargs) -> None: ...
    @staticmethod
    def from_arrow(*args, **kwargs): ...
    @staticmethod
    def from_raw(*args, **kwargs): ...
    def stats(self, *args, **kwargs): ...
    def daily_return(self, *args, **kwargs): ...
    def dailys(self, *args, **kwargs): ...
    def alpha(self, *args, **kwargs): ...

def daily_performance(daily_returns: list[float], yearly_days: None | int = None):
    """采用单利计算日收益数据的各项指标

    函数计算逻辑：

    1. 首先，将传入的日收益率数据转换为NumPy数组，并指定数据类型为float64。
    2. 然后，进行一系列判断：如果日收益率数据为空或标准差为零或全部为零，则返回字典，其中所有指标的值都为零。
    3. 如果日收益率数据满足要求，则进行具体的指标计算：

        - 年化收益率 = 日收益率列表的和 / 日收益率列表的长度 * 252
        - 夏普比率 = 日收益率的均值 / 日收益率的标准差 * 标准差的根号252
        - 最大回撤 = 累计日收益率的最高累积值 - 累计日收益率
        - 卡玛比率 = 年化收益率 / 最大回撤（如果最大回撤不为零，则除以最大回撤；否则为10）
        - 日胜率 = 大于零的日收益率的个数 / 日收益率的总个数
        - 年化波动率 = 日收益率的标准差 * 标准差的根号252
        - 下行波动率 = 日收益率中小于零的日收益率的标准差 * 标准差的根号252
        - 非零覆盖 = 非零的日收益率个数 / 日收益率的总个数
        - 回撤风险 = 最大回撤 / 年化波动率；一般认为 1 以下为低风险，1-2 为中风险，2 以上为高风险

    4. 将所有指标的值存储在字典中，其中键为指标名称，值为相应的计算结果。

    :param daily_returns: 日收益率数据，样例：
        [0.01, 0.02, -0.01, 0.03, 0.02, -0.02, 0.01, -0.01, 0.02, 0.01]
    :param kwargs: 其他参数
        - yearly_days: int, 252, 一年的交易日数
    :return: dict
    """
    ...
