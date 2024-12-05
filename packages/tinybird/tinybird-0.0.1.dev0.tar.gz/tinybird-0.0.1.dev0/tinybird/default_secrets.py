import os

from tinybird_shared.redis_client.redis_client import DEFAULT_REDIS_CONFIG

SECRETS_KEY = "T67++TQ85w+bJH5jHKkdenvQyloztdipgP8F1q+w4CY="
DEFAULT_SECRET = "abcd"
DEFAULT_DOMAIN = "tinybird.co"
DEFAULT_PORT = "8000"
HFI_PORT = "8004"


def conf(env):
    DOMAIN = DEFAULT_DOMAIN
    port = env.get("port", DEFAULT_PORT)
    return dict(
        title="tinybird.co",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        login_url="/login",
        jwt_secret=DEFAULT_SECRET,
        secrets_key=SECRETS_KEY,
        debug=True,
        domain=DOMAIN,
        cdn_host="http://localhost:%s" % port,
        api_host="http://localhost:%s" % port,
        hfi_host="http://localhost:%s" % HFI_PORT,
        docs_host="http://localhost:8000",
        commercial_host="https://tinybird.webflow.io",
        host="http://localhost:%s" % port,
        tinybird_js_version="v1",
        billing_provider="aws",
        billing_region="us-east-1",
        microsoft_oauth={"id": "e2ebc98d-ad0f-4d1d-83eb-9de1aba5718f", "secret": "s9tmgn1rERqBbJk~18_i.9t._mJ4hl3OX3"},
        github_oauth={"id": "de6669588b3a3199b561", "secret": "4be7a25a3eeaaf25da0a231d500b62fb8709abbb"},
        auth0_oauth={
            "domain": "dev-w5qrzecn.us.auth0.com",
            "client_id": "62a9R0IrNUPqq7QGxVjBUlkT0m0aKsgo",
            "client_secret": "7qdXnDx63JQt3TxDGgS9J8Y5DIw9FVTJKJdTlbQpRYZb8DMUKZ-ZKbMrcC3Pju7A",
        },
        auth0_api={
            "domain": "dev-w5qrzecn.us.auth0.com",
            "client_id": "nFOOfxUWDHEl0QwdzA0ApGWIeRHd86c2",
            "client_secret": "1JD7_yX112m7I_u1vfi68rQyN1YbsKp5DNMiLjzFvR5eAlPfKP8xH3YCAtCFyv0Y",
        },
        github_api={
            # For starter kit downloads
            # Unauthenticated requests have a limit of 50reqs per hour.
            # You can use your own PAT is you need more requests.
            "sk_read_token": ""
        },
        github_user="tinybirdco",
        mailgun={
            "api_key": "31e0641590dfe5c04a49564a0812436d-523596d9-2974e903",
            "domain": "https://api.eu.mailgun.net/v3/mg.speedwins.tech",
            "email": "services@speedwins.tech",
        },
        stripe={
            # The following settings are using the sandbox account of the Spanish account of Stripe
            "api_key": "sk_test_pV9yB5moG9mwdQepzZ9mhAEQ00PCVbPKa0",
            "public_api_key": "pk_test_AOsb9qIGnY7DLbTZCIxFNXsy00fwfdvMmZ",
            "webhook_endpoint_secret": "whsec_mUFSStF74EPQiU8ZJKKssq9E8uGIGgrt",
            "default_products": {"pro": "prod_KzcRM1yeYmaKKA"},
            # The following settings are using the sandbox account of the US account of Stripe.
            # For the shared infra plan, we are going to use this account to create the subscription.
            "us_api_key": "sk_test_51QHjf9KB0Rr6jQleyGvaBJkLCLzQijAPf6PcI48NenYa3cRLAgqsiWVVMMB2ZZRnP5kCuHmPqR0s6SNMjUAfe8mb00Eb83kr6Q",
            "us_public_api_key": "pk_test_51QHjf9KB0Rr6jQleuBxTSjByVpqLqWlEySziY4HQnD6Rvl5K56A6q9EQGzNo0N4Q5ULEEoBkPO7Ie5xAMlhgk1aL00r6DvUP6V",
            # In local, we don't need the webhook secret as the webhook will not reach the server
            "us_webhook_endpoint_secret": "",
        },
        orb={
            "api_key": "b5bd948e0a987bd18e6945578e0a3a3753cde3ba4ad8b3dbf076aaf546d24780",
            "webhook_secret": "",
        },
        vercel_integration={
            "redirect_uri": "http://localhost:8001/integrations/vercel/new",
            "client_secret": "vWyCCA5ymLngu12260raOC1h",
            "client_id": "oac_zaRuLdoYRMdxpTlUIJ58nHWO",
        },
        openai={
            "api_key": "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",
        },
        github_integration={
            "client_id": "d7b70bf28e252dd8dd5a",
            "client_secret": "c4be8a3f5cdfb0190268bb4148ce61f30fdfc59c",
        },
        sentry={},
        redis=DEFAULT_REDIS_CONFIG,
        import_workers=1,
        max_seconds_before_timeout_on_application_shutdown=120,
        idle_connection_timeout=30,
        disable_rate_limits=False,
        available_regions={},
        all_regions={},
        confirmed_account=True,
        hubspot_integration=False,
        marketing_integration_token="",
        enabled_campaigns=["welcome-form"],
        default_cluster="tinybird",
        default_database_server="ci_ch:6081",
        internal_database_server="ci_ch_internal:6081",
        metrics_cluster="internal",
        metrics_database_server="ci_ch_internal:6081",  # needed for local metrics initialization
        clickhouse_clusters={"tinybird": "ci_ch:6081"},
        cdk_project_id="development-353413",
        cdk_webserver_url="https://213c2c9ad9df49c58a07e42f0e429047-dot-europe-west3.composer.googleusercontent.com",
        cdk_service_account_key_location="local",
        cdk_gcs_export_bucket="dev-cdk-data",
        cdk_gcs_composer_bucket="europe-west3-tinybird-compo-cee9fdc8-bucket",
        cdk_group_email="cdk-service-accounts-dev@tinybird.co",
        yepcode_environment="tinybird-staging",
        yepcode_token="dGlueWJpcmQtaW5nZXN0aW9uOlQkeDd6WGkycDdANnkyQTE=",
        gcscheduler_project_id="stddevco",
        gcscheduler_service_account_key_location="local",
        gcscheduler_region="southamerica-east1",
        max_datasources=100,
        kafka_server_groups={},
        whitelist_local_networks=[],
        rudderstack_write_key=None,
        tb_region="local",
        # Controls whether to start the QueryLogTracker thread or not.
        track_query_log=False,
        # How many log entries read at once (only for track_query_log==True)
        track_query_log_batch_limit=1000,
        telemetry_token="p.eyJ1IjogIjFmMzY4MDE4LWI1MjctNGM3Ny1iM2ZiLWJiYjBjOTQ5NThkYyIsICJpZCI6ICIwNTE1NWMzYy1iZDY1LTQ3NDUtOGY1Ny04MmNiZjNmMzRhYmEifQ.nKn9kRffLUy6d70Ev4Er9Jo749rtQn1fRKoFmbT_92g",
    )


def running_in_testing_environment() -> bool:
    return os.environ.get("RUNNING_IN_TESTING_ENVIRONMENT", "").lower() == "true"
