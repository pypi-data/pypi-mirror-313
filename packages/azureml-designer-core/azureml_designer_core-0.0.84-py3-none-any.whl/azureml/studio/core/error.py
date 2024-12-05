# This is a standard user error message given by PM that hints customer to open support ticket.
_OPEN_SUPPORT_TICKET_HINT = "If the same error keeps occurring and blocks your experience, " \
                            "please open a support ticket of Designer in azure portal."


class UserError(Exception):
    """This is a base exception to indicate the errors that caused by unexpected user input.

    Once an exception inherited from UserError is raised,
    it could be displayed in Web UI to help the user adjust his input.
    """
    pass


class DataFrameSchemaValidationError(UserError):
    def __init__(self, detail=None):
        msg = "DataFrameSchema validation failed." \
            if not detail else f"DataFrameSchema validation failed, {detail}."
        super().__init__(msg)


class DirectoryNotExistError(UserError):
    def __init__(self, load_from_dir):
        super().__init__(f"Input path does not exist, please make sure your input is correct. Path='{load_from_dir}'.")


class DirectoryEmptyError(UserError):
    def __init__(self, load_from_dir):
        super().__init__(f"Input folder is empty, please make sure your input is correct. Path='{load_from_dir}'.")


class InvalidDirectoryError(UserError):
    def __init__(self, reason):
        super().__init__(f"Input folder is invalid, please make sure your input is correct."
                         f" Reason: {reason}")
        self.reason = reason


class PathExistsError(UserError):
    """Exception of user trying to save to an existing path"""
    def __init__(self, save_to_path):
        super().__init__(f"Save target path {save_to_path} already exists, set overwrite_if_exists=True "
                         f"if need to overwrite.")


class ModelSpecKeyError(UserError):
    """Exception of required key missing in model spec"""
    def __init__(self, load_from_path=None, detail=None, caused_ex=None):
        message = "Invalid model_spec because of KeyError."
        if load_from_path:
            message += f" load_from_path = {load_from_path}."
        if detail:
            message += f" Detail: {detail}."
        if caused_ex:
            message += f" Caused by exception: {caused_ex}."
        super().__init__(message)


class ModelSpecValueError(UserError):
    """Exception of value error in model spec"""
    def __init__(self, detail=None, caused_ex=None):
        message = "Invalid model_spec because of ValueError."
        if detail:
            message += f" Detail: {detail}."
        if caused_ex:
            message += f" Caused by exception: {caused_ex}."
        super().__init__(message)


class LocalDependencyValueError(UserError):
    """Exception of local_dependencies user provided is invalid"""
    def __init__(self, detail=None, caused_ex=None):
        message = "Invalid local_dependencies."
        if detail:
            message += f" Detail: {detail}."
        if caused_ex:
            message += f" Caused by exception: {caused_ex}."
        super().__init__(message)
