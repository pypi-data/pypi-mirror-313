import click
from humanfriendly.tables import format_pretty_table

from tinybird.user import UserAccount, UserAccountDoesNotExist

from ... import common
from ..cli_base import cli


@cli.command()
@click.argument("email_needle")
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def accounts(email_needle, config):
    """List accounts matching an email needle"""
    common.setup_redis_client(config)
    all_accounts = UserAccount.get_all()

    matching_accounts = []
    for account in all_accounts:
        if email_needle.lower() in account.email.lower():
            matching_accounts.append([account.email, account.id])

    column_names = ["email", "id"]
    click.echo(format_pretty_table(matching_accounts, column_names=column_names))


@cli.command()
@click.argument("old_domain")
@click.argument("new_domain")
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def migrate_accounts(old_domain, new_domain, dry_run, config):
    """Migrate accounts between email domains"""
    common.setup_redis_client(config)

    if "@" in old_domain or "@" in new_domain:
        click.secho("[ERROR] Please, don't include the at-sign in the domains.", fg="red")
        return

    matching = 0
    migrated = 0

    for user in UserAccount.get_all():
        parts = user.email.split("@", maxsplit=1)
        if len(parts) == 1 or parts[1].lower() != old_domain:
            continue

        matching = matching + 1
        new_email = f"{parts[0]}@{new_domain.lower()}"

        if _try_change_account_email(user, new_email, dry_run=dry_run):
            migrated = migrated + 1

    click.echo("")
    if matching == 0:
        click.secho(f"No accounts found for domain '{old_domain}'", fg="yellow")
    else:
        msg = "Dry run results:" if dry_run else "Migration results:"
        click.secho(msg, fg="green")
        click.echo(f"- {matching} matching accounts")
        click.echo(f"- {migrated} migrated accounts")


@cli.command()
@click.argument("old_email")
@click.argument("new_email")
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--config", type=click.Path(exists=True), help=common.CONFIG_HELP)
def migrate_account(old_email, new_email, dry_run, config):
    """Change an account's email address"""
    common.setup_redis_client(config)

    user = None
    try:
        user = UserAccount.get_by_email(old_email)

        # Can happen if the user had this email previously (it remains in the index)
        if user.email != old_email:
            user = None
    except UserAccountDoesNotExist:
        pass

    if user is None:
        click.secho(f"> Account '{old_email}' does not exist.", fg="yellow")
        return

    if old_email == new_email:
        click.secho(f"> Nothing to do for '{old_email}'.", fg="cyan")
        return

    _try_change_account_email(user, new_email, dry_run=dry_run)


def _try_change_account_email(user: UserAccount, new_email: str, dry_run: bool = False) -> bool:
    """Change an account's email address"""

    try:
        usr = UserAccount.get_by_email(new_email)
        # No exception --> user exists
        # Also, the returned user must be *different* to be considered an error
        if usr.id != user.id:
            click.secho(f"> [ERROR] Destination address ({usr.email}) already in use.", fg="red")
            return False
    except UserAccountDoesNotExist:
        pass

    if user.email == new_email:
        click.secho(f"> Nothing to do for '{new_email}'.", fg="cyan")
        return False

    try:
        if not dry_run:
            with UserAccount.transaction(user.id) as u:
                u._clean_index("email")
                u.email = new_email
    except Exception as e:
        click.secho(f"> ERROR migrating '{user.email}' to '{new_email}': {e}", fg="red")
        return False

    msg = (
        f"> '{user.email}' will be migrated to '{new_email}'"
        if dry_run
        else f"> '{user.email}' migrated to '{new_email}'"
    )
    click.secho(msg, fg="cyan")

    return True
