# 地区业务状态与事故客户公告的更正交付

这里的设备、合作方及业务记录均为合成资料。两份记录分别从同一清册开始，可独立读取。记录包含申请、通知及实际观察，申请可能未获准。

## 资料字段

`records/inventory.json` 是初始清册。两份 `.jsonl` 文件均以每行一个 JSON 对象保存观察。`at` 是记录进入值班侧的演练秒，同一秒按原文件顺序。`kind` 标识记录类别。另有字段时，业务发生时间由记录自身给出。

services 按 region/capability 标出实际依赖。supports 表示来源能为哪个范围提供直接证据，receipt 是具体客户接收或下游完成，不替代整体覆盖。audience 的订阅具有生效范围。notice_delivery 的 delivered 报实到，accepted 表示渠道已收到请求。

## 运行

在仓库根目录使用 Python 3.11 标准库。

```sh
python3 source_reader.py records/shift.jsonl
python3 source_reader.py records/comparison.jsonl
python3 -m unittest discover -s tests -v
```

读取工具按记录到达顺序显示原始资料，`--kind` 可按类别筛选。
