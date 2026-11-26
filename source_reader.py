"""读取值班侧保存的原始演练资料。"""

import argparse
import json
from pathlib import Path


def read_inventory(directory):
    result = json.loads((directory / "inventory.json").read_text("utf-8"))
    if not isinstance(result, dict) or not result:
        raise ValueError("清册应为非空对象")
    return result


def read_observations(path):
    previous = 0
    with path.open(encoding="utf-8") as file:
        for number, line in enumerate(file, 1):
            try:
                record = json.loads(line)
                if not isinstance(record, dict) or type(record.get("at")) is not int:
                    raise ValueError("记录应有整数接收时钟")
                if record["at"] < previous or not isinstance(record.get("kind"), str) or not record["kind"]:
                    raise ValueError("接收时钟倒退或缺少记录类别")
            except ValueError as error:
                raise ValueError(f"{path.name}:{number} {error}") from error
            previous = record["at"]
            yield record


def main():
    parser = argparse.ArgumentParser(description="浏览运维原始记录")
    parser.add_argument("records", type=Path)
    parser.add_argument("--kind", help="按记录类别查看")
    args = parser.parse_args()
    try:
        read_inventory(args.records.parent)
        for observation in read_observations(args.records):
            if args.kind is None or observation["kind"] == args.kind:
                print(json.dumps(observation, ensure_ascii=False))
    except (OSError, ValueError) as error:
        parser.exit(2, f"资料读取失败：{error}\n")


if __name__ == "__main__":
    main()
