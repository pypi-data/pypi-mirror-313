import asyncio
import logging

import click
import stripe

from tinybird.app import get_config
from tinybird.plans import PlansService, configure_stripe

from ..cli_base import cli


@cli.group()
def plans():
    """Tinybird plans commands"""
    configure_stripe(get_config())
    logging.basicConfig(level=logging.INFO)


@plans.command(name="create_pro_plan")
@click.option("--plan-name-override", default=None, help="Pro plan name instead of the default one")
@click.option("--storage-price", default="0.34", help="Price per GB stored per month")
@click.option("--processed_price", default="0.07", help="Price per GB processed")
@click.option("--force", default=None, help="Skip checking if the pro plan is already configured")
def plans_create_pro_plan(plan_name_override, storage_price, processed_price, force):
    new_plan = PlansService.create_new_pro_plan(
        storage_price, processed_price, name_override=plan_name_override, force=force
    )
    click.echo(new_plan)


@plans.command(name="update_pro_prices")
@click.argument("stripe-product-id")
@click.argument("storage-price")
@click.argument("processed-price")
def plans_update_pro_prices(stripe_product_id, storage_price, processed_price):
    """
    Arguments:
        stripe-product-id: ID of the product in Stripe
        storage-price: Price per GB stored per month
        processed-price: Price per GB processed
    """
    asyncio.run(PlansService.update_product_prices(stripe_product_id, storage_price, processed_price))


@plans.command(name="list-subscriptions")
def plans_list_subscriptions() -> None:
    """
    Arguments:
        stripe-product-id: ID of the product in Stripe
        storage-price: Price per GB stored per month
        processed-price: Price per GB processed
    """
    subs = stripe.Subscription.list(limit=20)
    for sub in subs:
        print(sub)


@plans.command(name="add-sink-prices")
@click.option("--dry-run", default=True, help="Set to False to apply changes")
def plans_add_sink_prices(dry_run: bool) -> None:
    PlansService.add_sink_prices(dry_run=dry_run)
