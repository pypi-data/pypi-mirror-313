def j2_snake_case_filter(value):
    return value.strip().replace(" ", "_").lower()


def j2_kebab_case_filter(value):
    return j2_snake_case_filter(value).replace("_", "-")


def j2_camel_case_filter(value):
    words = j2_snake_case_filter(value).replace("_", " ").split()
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


def j2_pascal_case_filter(value):
    words = j2_snake_case_filter(value).replace("_", " ").split()
    return "".join(word.capitalize() for word in words)
