import re
from lesscpy.lessc import Less


def camel_case_class_name(class_name):
    return re.sub(r"-([a-z])", lambda x: x.group(1).upper(), class_name)


def transform_less(input_file_path):
    output_file_path = input_file_path.replace(".less", ".module.less")
    with open(input_file_path, "r") as f:
        less_code = f.read()
    less = Less()
    css_code = less.compile(less_code)
    replaced_css_code = re.sub(
        r"\.([^.\s]*)(?=\s*{)",
        lambda x: "." + camel_case_class_name(x.group(1)),
        css_code,
    )
    with open(output_file_path, "w") as f:
        f.write(replaced_css_code)
    print(f"Transformed LESS file: {input_file_path} -> {output_file_path}")


def transform_react(input_file_path):
    output_file_path = input_file_path.replace(".js", ".transformed.js")
    with open(input_file_path, "r") as f:
        react_code = f.read()
    transformed_code = re.sub(
        r'className="([^"]*)"',
        lambda x: f"className={{styles.{camel_case_class_name(x.group(1))}}}",
        react_code,
    )
    with open(output_file_path, "w") as f:
        f.write(transformed_code)
    print(f"Transformed React file: {input_file_path} -> {output_file_path}")


def process_file(file_path):
    if file_path.endswith(".less"):
        transform_less(file_path)
    elif file_path.endswith(".js"):
        transform_react(file_path)


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python transform.py <file_path>")
        return
    file_path = sys.argv[1]
    process_file(file_path)


if __name__ == "__main__":
    main()

print("name", __name__)
