from . import request_error


class WorkspacesClientErrorBadRequest:
    invalid_operation = request_error(400, 'Invalid operation "{operation}", valid operations are {valid_operations}')
    failed_operation = request_error(400, "Failed to {operation} user: {error}")
    invalid_workspace_name = request_error(400, "Workspace name must be provided (name=my_workspace)")
    max_owned_workspaces = request_error(400, "User {email} already has {workspaces} workspaces")
    no_users = request_error(400, "The 'users' parameter must be provided")
    failed_emails = request_error(400, "There was a problem with the given emails")
    name_is_not_valid = request_error(400, "Workspace name is not valid, reason: {validation_error}")
    name_already_taken = request_error(
        400,
        "The name '{name}' is already being used, please select another name as Workspace " "names should be unique.",
    )
    no_branch_name = request_error(400, "The 'branch_name' parameter must be provided")
    confirmation_is_not_valid = request_error(400, "The 'confirmation' parameter does not match the Workspace name")
    no_branch_rename = request_error(400, "Branches can not be renamed")
    no_workspace_with_branches_rename = request_error(400, "You can not rename a Workspace with Branches")
    invalid_read_only_value = request_error(400, "Invalid value for 'is_read_only' parameter")
    invalid_role = request_error(
        400, "Invalid value {value} for the '{parameter}' parameter. Valid values are: {valid_values}"
    )


class WorkspacesClientErrorNotFound:
    no_workspace = request_error(404, "Workspace not found")


class WorkspacesClientErrorForbidden:
    no_workspace_creation_allowed = request_error(403, "You can not create another workspace from a workspace")
    no_workspace_deletion_allowed = request_error(403, "Workspace could not be deleted: {error}")
    no_workspace_rename_allowed = request_error(403, "You can not rename this workspace")
    not_allowed = request_error(403, "Not allowed")
    user_is_read_only = request_error(
        403,
        "You have the Viewer role in this workspace, you can not perform this action. Please contact an admin to grant you write permissions.",
    )
    delete_remote_forbidden = request_error(
        403, "Workspace {name} has associated releases or branches. Please, remove them and try again."
    )


class WorkspacesServerErrorInternal:
    failed_operation = request_error(500, 'Failed to {operation} user: "{error}"')
    failed_register = request_error(500, 'Failed to register {name} workspace: "{error}"')
    failed_register_user = request_error(500, "Failed to register user: '{name}': \"{error}\"")
    failed_delete = request_error(500, 'Failed to delete {name} workspace: "{error}"')
    failed_invite = request_error(500, 'Error: "{error}"')
    failed_unlink = request_error(500, 'Failed to unlink {name} workspace: "{error}"')


class WorkspacesClientRemoteError:
    invalid_provider = request_error(400, "Invalid remote provider")
    not_connected = request_error(400, "Workspace not connected to a remote")
    already_connected = request_error(
        400, "Workspace already connected to a remote. Please disconnect from remote first"
    )
    failed_push = request_error(400, "Failed to push to remote: {error}")
    no_message = request_error(400, "Invalid 'message', it can't be empty")
    pull_request_from_main_not_allowed = request_error(
        400, "Pull requests from main workspace should have a target branch"
    )
    main_has_no_branch = request_error(400, "Origin workspace has no default branch defined")
