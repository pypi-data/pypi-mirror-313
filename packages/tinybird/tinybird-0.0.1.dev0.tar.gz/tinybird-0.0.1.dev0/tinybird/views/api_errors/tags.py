from tinybird.views.api_errors import request_error


class TagClientErrorBadRequest:
    name_is_required = request_error(400, "Tag name is required")
    name_already_taken = request_error(
        400,
        "The name '{name}' is already being used, please select another name as Tag " "names should be unique.",
    )
    resources_must_be_list = request_error(400, "Tag resources must be a list")


class TagClientErrorNotFound:
    no_tag = request_error(404, "Tag '{name}' not found")
