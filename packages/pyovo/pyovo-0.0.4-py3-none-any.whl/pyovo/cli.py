import argparse

def main():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(
        description="pyovo: 一个示例 Python 包的命令行工具"
    )

    # 添加命令行参数
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="显示版本信息"
    )
    parser.add_argument(
        "-n", "--name",
        type=str,
        help="输入用户的名字"
    )

    # 解析参数
    args = parser.parse_args()

    # 根据参数执行不同逻辑
    if args.version:
        print("pyovo 版本 1.0.0")
    elif args.name:
        print(f"你好，{args.name}!")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
