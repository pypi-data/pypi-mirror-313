from hcs_core.ctxp import CtxpException
import hcs_core.ctxp.data_util as data_util


def calculate_patch(original_object: dict, allowed_fields: list, updates):
    patch = {}
    original_application_properties = original_object.get("applicationProperties", {})
    updated_application_properties = dict(original_application_properties)
    original_flags = original_object.get("flags", {})
    updated_flags = dict(original_flags)
    for u in updates:
        k, v = u.split("=")
        field_name = k.split(".")[0]
        if field_name not in allowed_fields:
            raise CtxpException("Not updatable: " + field_name)

        # special handling for applicationProperties
        if field_name == "applicationProperties":
            prop_name = k[k.index(".") + 1 :]
            updated_application_properties[prop_name] = v
        if field_name == "flags":
            prop_name = k[k.index(".") + 1 :]
            updated_flags[prop_name] = v
        else:
            current_value = data_util.deep_get_attr(original_object, k, raise_on_not_found=False)
            if str(current_value) == str(v):
                continue
            patch[field_name] = original_object.get(field_name)
            data_util.deep_set_attr(patch, k, v, raise_on_not_found=False)

    if updated_application_properties != original_application_properties:
        patch["applicationProperties"] = updated_application_properties

    if updated_flags != original_flags:
        patch["flags"] = updated_flags

    return patch
