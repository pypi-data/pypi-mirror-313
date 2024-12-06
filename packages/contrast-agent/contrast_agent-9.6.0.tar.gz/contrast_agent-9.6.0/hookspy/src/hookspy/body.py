from .signatures import fastcall_name


hook_macro_by_signature = {
    "unaryfunc": "HOOK_{}UNARYFUNC",
    "binaryfunc": "HOOK_{}BINARYFUNC",
    fastcall_name: "HOOK_{}FASTCALL",
}


def build_stream_hook_macro(name, hook_name, signature):
    hook_definition = hook_macro_by_signature[signature]
    hook_definition = hook_definition.format("STREAM_")
    hook_definition += '({}, "{}");'
    return hook_definition.format(hook_name, name)


def create_hook(strtype, name, signature, stream_type):
    hook_name = f"{strtype}_{name}"
    if stream_type:
        hook_definition = build_stream_hook_macro(name, hook_name, signature)
    else:
        raise ValueError(f"Unknown hook {hook_name}")

    return hook_definition, hook_name
