from hcs_core.ctxp import CtxpException, recent


def parse_vm_path(vm_path: str):
    if not vm_path:
        template = recent.require(None, "template")
        vm = recent.require(None, "vm")
    else:
        parts = vm_path.split("/")
        # if len(parts) != 2:
        #    raise CtxpException("Invalid path. Valid path example: template1/vm1.")
        if len(parts) == 1:
            # treat as VM ID only
            template = recent.require(None, "template")
            vm = recent.require(parts[0], "vm")
        elif len(parts) == 2:
            template = recent.require(parts[0], "template")
            vm = recent.require(parts[1], "vm")
        else:
            raise CtxpException("Invalid path. Valid path example: template1/vm1")

    if not template:
        raise CtxpException("Invalid path (missing template):" + vm_path)
    if not vm:
        raise CtxpException("Invalid path (missing VM):" + vm_path)
    return template, vm


def parse_vm_params(template: str, vm: str, path: str):
    if template or vm:
        if path:
            raise CtxpException("Either --template/--vm or --path should be specified. Not together.")

        if not template:
            raise CtxpException("Missing parameter: --template")
        if not vm:
            raise CtxpException("Missing parameter: --vm")
        return template, vm

    if not path:
        raise CtxpException("Either --template/--vm or --path should be specified.")

    return parse_vm_path(path)
