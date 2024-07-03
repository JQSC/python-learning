from pathlib import Path
import re


# js 替换
# 将类名转换为小驼峰形式
def to_upperCase(match):
    return match.group(1).capitalize()


def camelCaseClassName(str):
    return re.sub(r"[-_]([a-z1-9]*)", to_upperCase, str)


def replace_class_name(match):
    class_name = match.group(1)
    return f"className={{styles.{camelCaseClassName(class_name)}}}"


def replace_import(match):
    return 'import styles from "./index.module.less"'


# 转换 less 样式文件
def replace_less(match):
    groups = match.groups()

    return groups[0] + camelCaseClassName(groups[1])


js_patterns_and_replacements = {
    r'className=[\"\']([^"\']*)[\"\']': replace_class_name,
    r"import [\"\']\./index\.less[\"\']": replace_import,
}

less_patterns_and_replacements = {r"([.#])([\w-]+)": replace_less}


# 读取文件
def readFileSync(file_path: Path):
    return file_path.read_text()


# 转换react文件
def transformReact(file_path: Path):
    file_content = readFileSync(file_path)
    if not file_content:
        return

    transformed_content = file_content
    for pattern, replacement in js_patterns_and_replacements.items():
        transformed_content = re.sub(pattern, replacement, transformed_content)

    print(transformed_content)


# 转换less文件
def transformLess(file_path: Path):
    file_content = readFileSync(file_path)
    if not file_content:
        return

    transformed_content = file_content
    for pattern, replacement in less_patterns_and_replacements.items():
        transformed_content = re.sub(pattern, replacement, transformed_content)

    print(transformed_content)


# 处理文件
def processFile(file_path: Path):
    if file_path.suffix == ".tsx":
        transformReact(file_path.resolve())
    elif file_path.suffix == ".less":
        transformLess(file_path)


# 主函数
def main(file_path):
    if not file_path:
        print("Please provide a file path.")
        return
    processFile(Path(file_path))


file_path = Path().cwd() / "文件格式化/test/index.less"

main(file_path)
