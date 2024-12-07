import copy


def simplify_errors(errors: list) -> dict:
    prepared_errors = _prepare_errors(errors)
    simplified_errors = {"errors": prepared_errors["errors"]}
    if prepared_errors["attr_errors"]:
        simplified_errors["attr_errors"] = _simplify_errors(
            prepared_errors["attr_errors"]
        )
    if prepared_errors["list_errors"]:
        simplified_errors["list_errors"] = _simplify_errors(
            prepared_errors["list_errors"]
        )
    return simplified_errors


def _simplify_errors(attr_errors):
    simplified_errors = {}
    for attr, error in attr_errors.items():
        simplified_errors[attr] = {}
        if not attr.isdigit() and not error["attr_errors"] and not error["list_errors"]:
            simplified_errors[attr] = error["errors"][0]
            continue

        simplified_errors[attr] = {"errors": error["errors"]}

        if error["attr_errors"]:
            simplified_errors[attr]["attr_errors"] = _simplify_errors(
                error["attr_errors"]
            )
        if error["list_errors"]:
            simplified_errors[attr]["list_errors"] = _simplify_errors(
                error["list_errors"]
            )
    return simplified_errors


def _prepare_errors(errors: list) -> dict:
    loc_error: dict = {"errors": [], "attr_errors": {}, "list_errors": {}}
    prepared_errors = copy.deepcopy(loc_error)
    for error in errors:
        dest = prepared_errors
        attr = []
        loc = [f for f in error["loc"] if f != "body"]
        if not loc:
            # global error
            dest["errors"].append(error["msg"])
            continue

        for loc_attr in loc:
            if not isinstance(loc_attr, int):
                attr.append(loc_attr)
                continue

            # attr is a list
            loc_attr = str(loc_attr)
            flat_attr = ".".join(attr)
            if flat_attr:
                if flat_attr not in dest["attr_errors"]:
                    dest["attr_errors"][flat_attr] = copy.deepcopy(loc_error)
                if loc_attr not in dest["attr_errors"][flat_attr]["list_errors"]:
                    dest["attr_errors"][flat_attr]["list_errors"][
                        loc_attr
                    ] = copy.deepcopy(loc_error)
                dest = dest["attr_errors"][flat_attr]["list_errors"][loc_attr]
            else:
                if loc_attr not in dest["list_errors"]:
                    dest["list_errors"][loc_attr] = copy.deepcopy(loc_error)
                dest = dest["list_errors"][loc_attr]
            attr = []

        if attr:
            flat_attr = ".".join(attr)
            if flat_attr not in dest["attr_errors"]:
                dest["attr_errors"][flat_attr] = copy.deepcopy(loc_error)
            dest["attr_errors"][flat_attr]["errors"].append(error["msg"])
        else:
            dest["errors"].append(error["msg"])
    return prepared_errors
