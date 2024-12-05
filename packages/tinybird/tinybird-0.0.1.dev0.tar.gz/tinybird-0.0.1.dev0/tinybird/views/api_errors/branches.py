from . import request_error


class BranchesClientErrorBadRequest:
    branching_disabled = request_error(
        404,
        "This command depends on the Branch feature currently in beta. Contact us at support@tinybird.co to activate the feature in your Workspace. Branches are free of charge during beta.",
    )
    no_branch_name = request_error(400, "The 'name' parameter must be provided")
    branch_not_found = request_error(404, "Branch {name} not found")
    create_from_branch_not_allowed = request_error(
        400, "Branch can't be created from other Branch '{name}'. Use 'tb branch use main'"
    )
    delete_from_another_not_allowed = request_error(
        400, "Branch can't be deleted from other Branch '{name}'. Use 'tb branch use '{hint}'"
    )
    name_already_taken = request_error(
        400,
        "The name '{name}' is already being used in Workspace {main_name}, please select another name as Branch "
        "names should be unique.",
    )
    name_is_not_valid = request_error(400, "Branch name is not valid, reason: {validation_error}")
    max_number_of_branches = request_error(
        400, "Max number of Branches allowed for Workspace '{name}'. Please delete Branches."
    )
    remote_disabled = request_error(
        400,
        "Create Branch on remote depends on the Versions feature currently in beta. Contact us at support@tinybird.co to activate the feature in your Workspace.",
    )


class BranchesClientErrorForbidden:
    no_branch_deletion_allowed = request_error(403, "Branch could not be deleted: {error}")
    not_allowed = request_error(403, "Not allowed")
    not_a_branch = request_error(403, "Not a Branch")


class BranchesServerErrorInternal:
    failed_delete = request_error(422, 'Failed to delete {name} Branch: "{error}"')
