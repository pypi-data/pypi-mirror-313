from pydantic import ValidationError


def handle_pydantic_errors(e: ValidationError) -> str:
    msg = []
    for error in e.errors():
        if error["type"] == "missing":
            for field in error["loc"]:
                msg.append(f"{field} is mandatory")
        else:
            msg.append(f"'{error['loc']}': {error['msg']}")

    return ". ".join(msg)
