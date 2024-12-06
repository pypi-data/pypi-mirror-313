import warnings


def deprecation_warning(message: str):
    warning_control_url = "https://docs.python.org/3/using/cmdline.html#cmdoption-W"
    documentation_url = "https://blockbax.com/docs/integrations/python-sdk/"
    default_warning_message_suffix = f", for more information please see visit our Blockbax SDK documentation: {documentation_url}, if you wish to suppress this warning please see: {warning_control_url}"
    warning_message = f"{message}{default_warning_message_suffix}"

    warnings.warn(warning_message, DeprecationWarning)
