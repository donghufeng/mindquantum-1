.. py:class:: mindquantum.core.parameterresolver.PRGenerator(prefix: str = '', subfix: str = '', dtype=None)

    一个一个的生成参数。

    参数：
        - **prefix** (str) - 参数的前缀。默认值： ``''``。
        - **subfix** (str) - 参数的后缀。默认值： ``''``。
        - **dtype** (mindquantum.dtype) - 改参数解析器的数据类型。如果为 ``None``，则类型为 ``mindquantum.float64``。默认： ``None``。

    .. py:method:: reset()

        重置参数生成器到初态。

    .. py:method:: new()

        生成下一个新的参数。

    .. py:method:: size()

        返回已生成的参数的个数。
