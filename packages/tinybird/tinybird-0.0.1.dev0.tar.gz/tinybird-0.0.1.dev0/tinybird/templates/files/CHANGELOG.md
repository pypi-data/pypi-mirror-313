# Tinybird

We believe that Real-time data has the potential to change entire industries. For that, data engineers and developers need to be able to work with huge amounts of data just like they do with small amounts of data.

Tinybird is a platform for data engineers to expose huge amounts of data through low-latency, secure and linearly scalable APIs. This enables developers within and across organizations to quickly build Real-time Analytics Data products over any amount of data.

All notable changes to this project will be documented in this file.

Types of changes:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Fixed` for any bug fixes.
- `Released` for public releases (CLI, Tinybird.js, etc.).
- `Removed` for now removed features.
- `Security` in case of vulnerabilities.
- `Fixed` Improve error feedback when Explain feature fails

## Changelog

(2024W14) 2024-04-08 - 2024-04-12

- `Added` support for S3IAM roles for the ingest (!11716)
- `Changed` AWS access policy to write and read (!11952)

(2024W13) 2024-03-18 - 2024-03-25

---

- `Removed` DATA_SINKS feature flag from the API (!11576)

(2024W12) 2024-03-11 - 2024-03-17

---

- `Fixed` Avoid logging legitimate timeout errors in Copy Jobs in Sentry (!11404)
- `Changed` Workflow file names and secrets generated from the UI on GH include the workflow name (!11492)

(2024W11) 2024-03-04 - 2024-03-10

---

- `Added` Use job ID as `backend_hint` for Copy Jobs to enable multi-writer support (!11303)

(2024W10) 2024-02-26 - 2024-03-03

---

- `Added` Enable disabling the `max_result_rows` limit in Copy operations, by setting it to 0. (!11168)

(2024W09) 2024-02-19 - 2024-02-25

---

- `Fixed` Pipe with multiple tokens (!11087)
- `Added` Docs: better explanation about Org Service Data Sources (!11166)

(2024W08) 2024-02-12 - 2024-02-18

---

- `Added` Cancel datasource jobs when datasource is deleted (!11086)

(2024W07) 2024-02-12 - 2024-02-18

---

- `Fixed` Delete Sinks when soft-deleting Workspaces (!10901)

(2024W07) 2024-02-05 - 2024-02-11

---

- `Added` billing origin and destination region and provider to `log_comment`` for sink jobs (!10829)

(2024W06) 2024-02-05 - 2024-02-11

---

- `Fixed` Scrollbar chrome 121 support (!10843)
- `Fixed` Hide required field in OpenAPI spec when it's not required (!10862)
- `Fixed` Undoing changes in Data Source preview now shows the correct type (!10808)
- `Added` File observability for Sinks based on metadata (!10710)
- `Fixed` Allow set default values in NDSJON datasources that already have any (!10770)
- `Added` `dry_run` parameter when creating a sink pipe to validate user inputs (!11034)

(2024W05) 2024-01-22 - 2024-01-28

---

- `Changed` Allow using Playgrounds and Time Series in Releases (!10720)
- `Changed` OpenAPI formats for `UInt64` and `UInt32` to `int64` and `int32` respectively (!10742)
- `Fixed` Hide 0.0.0 release if workspace is git connected (!10637)
- `Added` Validation for dataconnector unique names (!10572)
- `Changed` Description for the Others option in Connect to Git UI (!10424)

(2024W04) 2024-01-15 - 2024-01-21

---

- `Removed` Wrong placeholder in Upgrade email field (!10329)
- `Removed` Killing the TableOptimizer (!10228)
- `Added` Maximum number of sink jobs per workspace quota (!9954)
- `Changed` Default Version feature flags for @tinybird.co (!9960)
- `Removed` Killing the TableOptimizer (!10228)
- `Added` API Endpoint to get the differences of a Release compared to the Live Release (!10991)
- `Added` Use gatherer configuration ingesting by kafka (!10311)
- `Changed` Group initial files on the first sync in a single commit (!10301)
- `Fixed` Always create the secret TB_ADMIN_TOKEN at the beginning (!10301)
- `Fixed` Commit hashes are rendered as text if there is no Git provider to kink (!10349)
- `Fixed` Populate with SQL condition feature sends wrong params (!10352)

(2024W03) 2024-01-08 - 2024-01-14

---

- `Added` Versions documentation
- `Removed` Do not OPTIMIZE every partition before moving it to S3 on populate's revamp (!10294)

(2024W02) 2024-01-08 - 2024-01-14

---

- `Added` Mock S3 integration endpoint (!10066)
- `Fixed` Avoid redirection when deleting a timeseries (!10172)
- `Added` Opening a Pipe or a Data Source scrolls the sidebar to that element (!10058)
- `Added` Make sinks recursively search for connectors (!10147)
- `Fixed` Explain shows sensitive information (!10091)
- `Added` IAM Role authentication implementation with boto3 for Sinks (!10040)
- `Added` Maximum frequency between scheduled sink jobs quota (!10058)
- `Added` Change mock values in S3 integration endpoint to actual ones (!10197)
- `Added` Maximum frequency between scheduled sink jobs quota (!10085)
- `Added` Maximum frequency between scheduled sink jobs quota (!10058)
- `Added` Sink queries included in the billable queries (!10164)

(2024W01) 2024-01-01 - 2024-01-07

---

- `Added` Maximum execution time per Sink job quota (!9954)
- `Added` Service Data Source sinks_ops_log available in the editor UI under FF (!10020)
- `Fixed` Cmd+K keeps its scrolls to the top when searching (!10051)
- `Fixed` 500 code returned if sink job template validation times out (!10775)
- `Fixed` Changed all LIMIT 0 clauses in the UI to get metadata for DESCRIBE (!10041)

(2023W52) 2023-12-25 - 2023-12-31

---

- `Added` Maximum number of sink jobs per workspace quota (!9954)
- `Changed` Default Version feature flags for @tinybird.co (!9960)
- `Added` Support SharedDataSources on GitHub API integration (!9938)
- `Added` Maximum number of sink jobs per workspace quota (!9954)
- `Changed` `request_id` in Service Data Sources is now a `ULID` string instead of a `UUID`. Note this change is incremental, that means for some time both formats UUID and ULID will coexist, at least until TTLs apply for each Service Data Source. Take it into account if you plan tou use ULIDs right away.
- `Added` New endpoint `/remote/access` to generate the GitHub secret for the admin token (!9983)
- `Changed` Use new /remote/access endpoint in the UI (!9983)
- `Changed` Support bump tinyenv version on push (!9983)
- `Added` Add 'method' column to pipe_stats_rt and update Internal to version 0.0.10

(2023W51) 2023-12-18 - 2023-12-24

---

- `Added` Compression info in Data Source schema tab (!9949)
- `Added` App skeleton before loading app (!9939)
- `Added` Allow GitHub connection for all regions (!9798)
- `Added` Make `sinks_ops_log` available to users (!9806)
- `Added` Kafka schema registry is now entered using URL, username and password (!9872)
- `Added` Maximum number of sink pipes per workspace quota (!9919)
- `Added` Send data to `sinks_ops_log`: logging errors and processed data (!9371)

(2023W50) 2023-12-11 - 2023-12-17

- `Fixed` Enum field in OpenApi schema when param type is Array (!9792)
- `Added` AWS eu-central to Region selector (!9774)

---

- `Added` APIWorkspaceRemotePullRequestHandler to get the pull request of an environment branch (!9651)
- `Added` APIWorkspaceRemoteBranchHandler to manage Git branch creation from an environment branch (!9651)
- `Fixed` When an environment is created from a workspace that is connected to a Git provider, it inherits the needed settings (!9651)
- `Added` GET endpoint on APIWorkspaceRemoteHandler to list the owners that a GitHub connection has access to (!9724)
- `Changed` Add 'parameters' column to pipe_stats_rt and update Internal to version 0.0.8 (!9265)
- `Fixed` Missing service parameter when creating a connector (!10570)

(2023W49) 2023-12-04 - 2023-12-10

---

- `Added` APIWorkspaceRemoteCheckHandler to get the list of files for the last commit (!9537)
- `Changed` APIWorkspaceRemoteChangesHandler to actually compare the current changed files against GitHub files (!9537)
- `Changed` APIWorkspaceRemoteChangesHandler to actually compare the current changed files against GitHub files (!9537)
- `Changed` Mark as 'changed' when Data Sources and Pipe have changed to be able to compare them against GitHub files (!9537)
- `Added` List Sinks Output files in /v0/jobs when JobID is part of the path (9624)

(2023W48) 2023-11-27 - 2023-12-03

---

- `Fixed` Let select again current region in select step (!9614)
- `Changed` Smarter redirection to the last Workspace or Environment used (!9486)
- `Fixed` Avoid regression tests on new created pipe endpoints (!9526)
- `Fixed` Removed unnecessary params from POST request to Explain API (!9538)
- `Added` Allow adding Job ID in file template (!9415)
- `Added` Allow adding Job ID in file template (!9415)
- `Added` Explain endpoint to the Pipes API (!9464)
- `Added` New parameters in `date_diff_*` functions. It provides a backup date format and return None instead of erroring the whole endpoint (!9588)

(2023W47) 2023-11-20 - 2023-11-26

---

- `Fixed` Engine settings were ignored creating S3 data sources from the API (!9963)

- `Fixed` Allow creation of Data Sources with S3 connection (ignoring the connection) on environments (!9458)
- `Added` AWS `us-east-1` to the list of available regions (!9494)
- `Fixed` Concatenate properly Data Source links in ProTip banner (!9472)
- `Added` Explain Node view in the UI (!9433)
- `Fixed` Avoid duplicated node names in Playground when deleting a Node (!9436)
- `Fixed` Materialized pipes coming from old endpoints showing wrong components in the UI (!9437)
- `Fixed` Timeseries tooltip cut (!9394)
- `Added` When consulting the Jobs API for Sinks Job the response will now include: `file_template`, `file_compression`, `file_format`, `token_name` and `service` (!9403).
- `Changed` ProTip visibility for Full Scan use cases (!9275)
- `Fixed` Tokens list not refreshed after bulk delete (!9394)
- `Added` Tokens list page (!9352)

(2023W46) 2023-11-13 - 2023-11-19

---

- `Added` Implement HTTP query parameter substitution in file_template for Sinks (!9331)
- `Changed` CI/CD workflow template creation to use the workspace token and `Fixed` knowing the release information when using the workspace token (!9382)
- `Added` Implement format and compression override for files when triggering Sink (!9362)
- `Changed` Add `max_bytes_before_external_sort` configuration for Sinks (!9376)
- `Changed` Set Sinks query as Read-Only with `ch_guarded_query` (!9376)
- `Added` Explain feature in Query statistics open for everybody (!9392)
- `Added` Added internal endpoint (`APIWorkspaceRemotePushHandler`) to commit and push changes (!9274)

(2023W46) 2023-11-13 - 2023-11-19

---

- `Fixed` Group properly empty strings in Time Series table (!9368)
- `Fixed` Group properly falsy values in Time Series graph (!9359)
- `Added` Materialized View output page (!9262)
- `Added` Content type application/json to OpenAPI definition (!9345)
- `Added` Add new Service Data Source `sinks_ops_log` and update Internal to version 0.0.7 (!9262)
- `Changed` Redirect ui.tinybird.co/changelog (Analytics changelog) to tinybird/changelog (our release notes) (!9301)

(2023W45) 2023-11-06 - 2023-11-12

---

- `Added` Support to Map type in the UI (!9282)
- `Fixed` Long names break the UI in several places (!9318)
- `Added` Organizations and Integrations title to browser tab (!9319)
- `Added` Optional fields to OpenApi spec (!9299)
- `Changed` Disable data operations (Truncate and Populate) in the UI for read only main environments (!9243)
- `Fixed` Redirect always to main environment when deleting another (!9252)
- `Changed` Analyze API not suggesting `-SimpleState` aggregations (!9179)
- `Changed` Update clickhouse-toolset to 0.28.dev0 (!9179)
- `Fixed` Always delete scheduled copies on copy node removal and improve logs in case of errors (!9206)
- `Fixed` Always delete scheduled copies on copy node removal and improve logs in case of errors (!9206)
- `Added` Better observability on parameters used on both Endpoints API and SQL API. (!9173)
- `Changed` Copy and Sink on-demand jobs now return the job URL in the CLI. (!9285)

(2023W44) 2023-10-30 - 2023-11-05

---

- `Added` Token actions to sidebar (!9177)
- `Fixed` `tinybird_tool` not using `pro.py` path as default onf `--config` parameters (!9164)
- `Changed` Sidebar now shows more area with long names (!9170)
- `Fixed` Workspace menu breaking the layout for long names (!9125)
- `Changed` Not track full story setting when url is localhost (!9145)
- `Fixed` Data Source loading state unsynced in Playgrounds (!9149)
- `Fixed` Environment creation failure better cleaup (!9125)
- `Fixed` Fixed bug branching environments (!4065)
- `Added` New Feature Flag at user level `ALL_NEW_WORKSPACES_WITH_VERSIONS` to make all new workspaces work with versions by default.

---

(2023W43) 2023-10-23 - 2023-10-29

---

- `Fixed` Current nodes used to in node options to calculate disable materialization (!9081)
- `Fixed` Data Source list shows the correct type when is materialized (!9050)
- `Fixed` Drop partitions as they're fetched on populate's revamp (!8960)
- `Fixed` README.md instructing the user to use the same http_port on both clickhouse servers for a local analytics install
- `Changed` Improve HFI API performance handling long periods of Rate Limit Errors (!9052)

---

(2023W44) 2023-10-30 - 2023-11-05

---

- `Fixed` Create non-replicated tables properly in populate setup (!9112)

(2023W43) 2023-10-23 - 2023-10-29

---

- `Fixed` Used trackEvent function in last position to avoid blocking the success action (!9098)
- `Added` `rows_before_limit_at_least` field on OpenAPI spec (!8983)
- `Fixed` Duplicate Pipe in Playground open the Playground section properly (!9050)
- `Added` BigQuery and drop resources sections in the Versions [common use cases guide](https://www.tinybird.co/docs/guides/how-to-iterate-use-cases.html) (!9032)
- `Fixed` Current nodes used to in node options to calculate disable materialization (!9081)
- `Fixed` Drop partitions as they're fetched on populate's revamp (!8960)
  (2023W40) 2023-10-02 - 2023-10-08

---

- `Fixed` Add pipe_id and pipe_name in datasource_ops_log for materializations in replaces (!7904)

(2023W39) 2023-09-25 - 2023-10-01
(2023W40) 2023-09-25 - 2023-10-01
(2023W41) 2023-10-16 - 2023-10-21

---

- `Fixed` Include GCP service account from main on Environment creation (!8875)
- `Fixed` `datasources_ops_log.result` generated by materialization not using anymore propagated `result` from landing log (!8910)

(2023W42) 2023-10-16 - 2023-10-22

---

- `Added` Node full screen mode (!9031)
- `Changed` Region selection flow to make easier to switch between regions (!8982)
- `Fixed` Sortable nodes in sidebar (!8986)
- `Added` Exchange API to swap Data Sources CH table names (https://clickhouse.com/docs/en/sql-reference/statements/exchange) (!9540)
- `Changed` Progress bar color in Settings modal (!8970)
- `Changed` Query quarantine rows by id instead of name (!8978)
- `Added` New UI navigation (!8864)
- `Fixed` Populate banners alignment (!8945)
- `Added` Node autocompletion in Playground UI (!8906)
- `Changed` Pass token in every API call to avoid errors when working in multiple sessions (!8905)
- `Fixed` Include GCP service account from main on Environment creation (!8875)
- `Fixed` Upgrade page redirects to workspace settings if Stripe user is not created (!8901)
- `Fixed` Support an array as default value for the `Array` data type on templates (!8874)
- `Added` Log the `node_id` when a variable fails in a template to make it easier to debug it (!8874)
- `Changed` Change the orphan materialized views monitoring (!8933)
- `Chore` Changed `_query_table_partitions_with_condition_fallback_sync` http user agent to Internal Query (!9534)

(2023W41) 2023-10-09 - 2023-10-15

---

(2023W39) 2023-10-02 - 2023-10-08

- `Fixed` Exact matchings in command menu search (!8778)
- `Changed` `DROP TABLE` to not using `SYNC` by default (!8832)
- `Fixed` Move `tinybird/copy` to `tinybird/copy_pipes` to prevent clashes with Python's `copy` standard (!8837)
- `Changed` Set `max_concurrent_queries_per_user` to 1GB and `max_result_bytes` to 50 on us_east_2 to prevent the BI connector raising an OOM error (!8842)
- `Fixed` Include GCP service account from main on Environment creation (!8875)
- `Fixed` `datasources_ops_log.result` generated by materialization not using anymore propagated `result` from landing log (!8910)

(2023W40) 2023-10-02 - 2023-10-08

---

- `Fixed` Bad alignment in materialization banner (!8778)
- `Fixed` Description not aligned in Time Series selector (!9500)
- `Fixed` Select starter kit by default when creating a new workspace with deploy button (!8778)
- `Fixed` Default column modifier not allowed when there's json paths (!9499)
- `Changed` Add search by id in cmdk (!8771)
- `Added` Recent section to cmdk component (!8697)
- `Changed` Show enterprise label in not available regions (!8791)
- `Fixed` Check if not main when creating an Environment (!8778)
- `Fixed` Hide starter kits banners and confetti when is not main environment (!8777)
- `Changed` Add search by id in cmdk (!8771)
- `Fixed` Allow to create worker from another origin when ingesting demo data (!8762)
- `Added` Request new regions from the UI (!8755)
- `Changed` Workspace creation modal for new users (!8751)
- `Added` Pipes' API POST endpoint is not available in OpenAPI specification (!8715)
- `Changed` Only using one record for the HFI snippet (!8797)
- `Added` Show pipe and node name on SQL template error message (!7313)

(2023W39) 2023-09-25 - 2023-10-01

---

- `Fixed` Don't count Environments in Workspace limits (!8629)
- `Changed` Improved error messages when importing Data Files in the UI (!8660)
- `Added` Recent section to cmdk component (!8697)
- `Fixed` Long names in Command Menu options (!8686)
- `Added` Shortcuts for Playground toolbar (!8716)
- `Fixed` Show notification when Pipe creation fails (!8629)
- `Added` New Datafile reference documentation page https://www.tinybird.co/docs/cli/datafile.html (!8660)
- `Changed` Extract redis client to a separate package (!8656)
- `Changed` Improved response message when the server raises an error due to too simultaneous queries (!8695)

(2023W38) 2023-09-18 - 2023-09-24

---

- `Changed` Toasts are rendered now in the bottom right corner (!8670)
- `Added` Playground member selection modal (!8658)
- `Fixed` Shared playgrounds checking wrong permissions (!8629)
- `Fixed` Playground nodes when there is some error in one of the queries (!8629)
- `Changed` Better error handling when creating a new Time Series (!8629)
- `Fixed` Column type selection when creating a new Data Source (!8629)
- `Fixed` Fix tb pull with Data Sink pipes that do not include compression (!8558)
- `Fixed` Renaming `Main` to `main` everywhere in the UI & docs (!8558)
- `Fixed` Renaming `environment` to `Environment` everywhere in the UI & docs (!8558)
- `Fixed` Do not require EXTERNAL_DATASOURCE parameter creating bigquery datasources (!8568)
- `Fixed` Fix exception when POST request body is empty in /v0/sql endpoint (!8615)
- `Fixed` Fix MVs not currently calculated with null columns and simple aggregation functions (!8601)
- `Fixed` Patch type inference of Simple Agregation type when column is nullable (!8306)
- `Removed` Remove support for Endpoint Pipes in Copy (!8640)

- `Added` support for NDJSON to create the quarantine tables on demand if they do not exist(!8570)

(2023W37) 2023-09-11 - 2023-09-17

---

- `Fixed` Fix tb pull with Data Sink pipes that do not include compression (!8558)
- `Changed` Use Cloudfront for serving static assets in Production (!8562)
- `Fixed` Playground requests when queries have more than 2048 characters (!8549)
- `Added` Duplicate Pipe on Playground option (!8541)
- `Fixed` Endpoint graph width on resize (!8530)
- `Changed` Redirect to dashboard when deleting a resource (!8520)
- `Fixed` a bug when `tb diff` Kafka Data Sources in an Environment (!8607)
- `Fixed` Return 503 error if all Materialized Views have failed and landing DS has Null engine (!8306)
- `Fixed` Reduce data_guess ingested items to avoid timeouts (!8507)
- `Added` warning message when SQL queries used for Materialized Views are going to be automatically rewritten. See [docs](https://www.tinybird.co/docs/concepts/materialized-views.html#what-should-i-use-materialized-views-for) (!8481)
- `Fixed` Return 503 error if all Materialized Views have failed and landing DS has Null engine (!8306)
- `Added` support for parameters in the request body for the POST `v0/sql` endpoint (!8427)
- `Changed` behaviour of the delete jobs created in `/v0/datasources/(.+)/delete` to skip running the delete operation if there is no row that will be affected by the `delete_condition` (!8524)
- `Added` support for parameters in the request body for the POST `v0/sql` endpoint (!8427)
- `Released` version 1.0.0b415 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8538)

(2023W36) 2023-09-04 - 2023-09-10

---

- `Fixed` Duplicate Pipes in read-only Workspaces (!8373)
- `Changed` Rate limit checking is now asynchronous and will make queries with rate limits faster. (!8398)
- `Deprecated` Hide and deprecate warning for the `--prefix` flag in all CLI commands. The prefix feature is superseded by Workspaces, use `tb workspace create` instead.
- `Released` version 1.0.0b409 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8470)
- `Added` New public explain mode for queries. (!8469)

(2023W35) 2023-08-28 - 2023-09-03

---

- `Added` Last 15 minutes in Dashboard filtering interval (!8382)
- `Released` version 1.0.0b401 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8368)
- `Fixed` UI representing nan and inf as null. Added output_format_json_quote_denormals tag to the API calls (!8384)
- `Fixed` Next run date on snowflake connector on UTC (!8373 !8405)
- `Fixed` Next run date on snowflake conector on UTC (!8373 !8405)
- `Changed` environment creation behaviour. Now, the quarantine tables will not be cloned in the environment (!8381)

(2023W34) 2023-08-21 - 2023-08-27

---

- `Added` Error handling for at different stages when running a copy job (!8299)
- `Added` Support for parameters for the `v0/sql` endpoint (!8335)
- `Added` support for ClickHouse syntax: SETTINGS (!8744), EXISTS and GROUPING (!8743).
- `Added` `result_rows` to `tinybird.pipe_stats_rt`
- `Fixed` `.datasource` file no longer include commas between workspaces listed in the `SHARED_WITH` section (!8954)
- `Fixed` Error not updated in editor (!8337)
- `Fixed` Time Series crash when too low granularity selected for too high time range (!8287)
- `Fixed` Time Series crash when too low granularity selected for too hight time range (!8287)

(2023W33) 2023-08-14 - 2023-08-20

---

- `Changed` Member list in Workspace creation modal (!8288)
- `Added` Validation of cron expression when step values are provided without a preceding range for the time slot (!8249)
- `Fixed` `Table Already Exists` error when creating aux_copy tables (!8285)
- `Fixed` Allow using custom integration names in Snowflake connector (!8284)
- `Changed` Table component to accept controlled filtering, sorting and pagination (!8303)

(2023W32) 2023-08-07 - 2023-08-13

---

- `Released` version 1.0.0b395 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8277)
- `Changed` Save changes banner in Token Page is now the same across the app (!8276)
- `Fixed` Sending correct error message when an SQL error is encountered when creating a copy pipe via CLI or API (!8203)
- `Added` Allow token duplication from UI (!8232)
- `Added` Description field to Tokens UI (!8208)
- `Added` Materialized banner to Pipe page (!8235)
- `Added` Creation of a sink pipe from the POST `/v0/pipes` API endpoint (!8000)
- `Fixed` OpenAPI Endpoint Parameter detection when using `defined(variable)` and parameter definition is later in the node (!8213)

(2023W31) 2023-07-31 - 2023-08-06

---

- `Changed` OpenAPI examples return fake data by default. Use examples=show to return real data, examples=hide to avoid including examples (!8108)
- `Released` version 1.0.0b387 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8026)
- `Changed` Google Cloud Storage connector service name from `'gcs' to 'gcs_hmac'` (!8026)
- `Fixed` Remove limit when requesting total members in the server (!8211)
- `Fixed` Workspace settings add members error when there are no spots left (!8145)
- `Fixed` Add column icon color contrast (!8200)
- `Fixed` Workspace settings totals when incoming data is empty (!8116)
- `Changed` OpenAPI examples return fake data by default. Use examples=show to return real data, examples=hide to avoid including examples (!8108)
- `Changed` Login and Singup app instrumented and deployed in auth0 authomatically (!7963)
- `Released` version 1.0.0b388 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8132)
- `Added` Login app favicon and minify without comments (!8141)
- `Fixed` Set snowflake datasource sync paused even the last run failed (!8170)
- `Fixed` Update sql node placeholder on changing prev node (!8159)
- `Fixed` badge styles component on @tinybird/ui package (!8159)
- `Added` Deletion of sink pipes from the `DELETE /v0/pipes` endpoint (!8073)
- `Released` version 1.0.0b387 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8026)
- `Changed` Google Cloud Storage connector service name from `'gcs' to 'gcs_hmac'` (!8026)
- `Changed` OpenAPI examples return fake data by default. Use examples=show to return real data, examples=hide to avoid including examples (!8108)
- `Released` version 1.0.0b387 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8026)
- `Changed` Google Cloud Storage connector service name from `'gcs' to 'gcs_hmac'` (!8026)
- `Fixed` validation of node copy queries to use the overridden `copy_max_execution_time` when describing the node's sql query (!8114)
- `Added` Limit to 50 GB the parts that can be attached to Environments (!8096)

(2023W30) 2023-07-24 - 2023-07-30

---

- `Added` New `host` attribute to tokens payload to know which region the token belongs to (!8045)
- `Released` version 1.0.0b381 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8060)
- `Released` version 1.0.0b383 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8062)
- `Added` Workspace settings redesign (!8093)
- `Released` version 1.0.0b384 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!8060)
- `Added` New `host` attribute to tokens payload to know which region the token belongs to (!8045)
- `Fixed` Support clickhouse compression type none (!8028)
- `Added` Tooltip at the Node Editor informing that materialized pipes are not editable (!8068)
- `Added` Added CTA to create a Data Source on empty Data Flow (!8071)
- `Changed` Disable attach all data option in Environments (!8686)
- `Fixed` updating of `source_copy_pipes` when overriding a copy pipe (!8091)
- `Changed` Do not retrieve indexes in EXPLAIN queries by default (!8095)

(2023W29) 2023-07-17 - 2023-07-23

---

- `Changed` Icons are rendered from svg instead of Javascript code. (!7925)
- `Fixed` Remove dependencies from compatible Data Source check in Copy Pipes UI (!8027)
- `Changed` Copy, Endpoint and Sink icons (!8023)
- `Added` Limit number of datasources per workspace to 100 by default (!7977)
- `Fixed` Detach Copy notification (!7866)
- `Released` version 1.0.0b374 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!7946)
- `Fixed` Overriding of pipes (!7866)
- `Added` Add partition capabilities with dynamic properties to file_template property (!7892)
- `Added` `resource_id` from Data Sinks is now included in the Data Connector's list (!7972)
- `Added` Compression parameter when creating a sink node (!7935)
- `Changed` click package version from 8.1.3 to 8.1.6 (!7904)
- `Added` Support of `SHARED_WITH` in `tb pull` and `tb diff` (!7918)
- `Fixed` Authorization check correctly sends 503 in case of internal error (!7985)
- `Added` S3 support for Sinks. Service URL translation from gcs:// and s3:// protocols. (!8039)

(2023W28) 2023-07-10 - 2023-07-16

---

- `Fixed` `tb pull` return copy node params once (#7955)
- `Fixed` Workspace errors when user is not logged (#7951)
- `Fixed` Error handling in new Kafka connections (#7940)
- `Changed` `PLAIN` as default `kafka_sasl_mechanism` in connectors API (#7912)
- `Fixed` Fix template syntax highlighting when code is commented (#7912)
- `Fixed` Notifications wrong method (#7867)
- `Released` version 1.0.0b365 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!7141)
- `Fixed` Compatible Data Sources proposed when creating a Copy Pipe in the UI (#7867)
- `Added` Confluent title to Confluent import flow (#7852)
- `Fixed` Token deletion can use both the token id or the token value (#7822)
- `Changed` the status code to 204 when dropping a copy node (!7875)
- `Added` Tokens now supports adding a free text description (#5714)

(2023W27) 2023-07-03 - 2023-07-09

---

- `Added` Pipe API errors to Datasource Ops Log when a copy job is run and an error occurs (!7784)
- `Changed` billing to not charge for queries using service datasources (!7820)
- `Changed` billing to not charge for queries using service datasources (!7820 )
- `Released` version 1.0.0b363 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!7141)
- `Fixed` Bigquery chart for scheduled Data Sources (!7849)
- `Fixed` Clean error when Group ID is duplicated (!7829)
- `Fixed` Compatible Data Sources in Copy Pipes require only to have `MergeTree` included in the engine (!7831)
- `Fixed` Show an error when a duplicated name is used in a pipe (!7826)
- `Fixed` Fix error handling of workspace tokens request in the UI (!7827)
- `Added` Pipe API errors to Datasource Ops Log when a copy job is run and an error occurs (!7784)
- `Changed` to use the recommended library for google.cloud.scheduler to create, update, pause, resume and delete scheduled jobs (!7744)
- `Added` Limits for Data Sink Job (!7783)

(2023W26) 2023-06-26 - 2023-07-02

---

- `Added` DOCS: S3 Connector docs (!7764)
- `Changed` Browse Pipes modal now let you navigate through different pipes easily (!7737)
- `Fixed` Drag and drop override not working as expected (!8341)
- `Fixed` Unpublish a pipe now updates the checked options in the output menu properly (!7717)
- `Fixed` Loading step of file and url imports has proper styles again (!7738)
- `Added` Copy Url when endpoint is created (!7705)
- `Added` Data Sinks API endpoints (!7398)
- `Changed` Kafka errors are parsed and provided to the user in the UI, finally (!7681)
- `Fixed` Add missing params to Data Source creation in Copy (!7698)
- `Fixed` Time Series when there is no pipelines yet (!7657)
- `Fixed` Support Copy Pipes with multiple materialized views (backwards compatibility) (!7664)
- `Added` .csv.gz support (!7650)
- `Added` Make configurable max message size in kafka ingestion (!7703)
- `Added` Amazon S3 connector (7532)
- `Fixed` OpenAPI spec now returns "format" on API endpoint parameters (!7710)
- `Added` Data Sinks API endpoints (!7398)
- `Added` Scheduling for Sink Pipes (!7620)
- `Changed` Increased the height of the import modal (!7727)

(2023W25) 2023-06-19 - 2023-06-25

---

- `Added` Datafiles import on dragging (!7544)
- `Fixed` Wrong error message when datasource preview fails (!7652)
- `Fixed` Parquet import error bad formatting (!7619)
- `Fixed` Missing markdown input styles (!7604)
- `Fixed` Pipe MV icon in sidebar showing properly (!7607)
- `Fixed` Icons color in editor (!7607)
- `Fixed` Data Source link is available again in Data Sources last events (!8153)
- `Added` Filtering of jobs based on params e.g `kind, status, pipe_id, pipe_name, created_before and created_after` (!7464)
- `Added` DOCS: Copy Pipes best practices (!7601)
- `Added` New Data Sink job for GCS (!7363)
- `Fixed` Drilldown in Time Series (!7598)
- `Added` Time Series with API Endpoints (!7070)

(2023W24) 2023-06-12 - 2023-06-18

---

- `Added` Support for sending datafiles directly through the API (!7552)
- `Released` version 1.0.0b348 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!7141)
- `Added` Support for ingestion of Map column (!7416)
- `Added` DOCS: Copy Pipes docs (!7482)
- `Fixed` Member list modal was crashing in case the user was not available yet (!7578)
- `Added` DOCS: Copy Pipes docs (!7482)
- `Fixed` Confetti not being displayed properly (!7541)
- `Fixed` Change duplicated pipe suffix to \_dup (!7542)
- `Fixed` HTML injection in markdown input (!7522)
- `Fixed` Broken styles in new users Workspace form (!7514)
- `Added` Copy Pipes UI (!7503)
- `Added` DOCS: Copy Pipes docs (!7482)
- `Added` `dry_run` parameter when creating a copy pipe to validate user inputs (!7368)
- `Released` version 1.0.0b344 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Added` endpoint to cancel scheduled copy jobs attached to a copy pipe(!7336)
- `Added` Allow get kafka preview when app has no connection to broker (!7465)
- `Changed` Updated Output icons (!7460)
- `Fixed` Data Source Icons that were not showing the right entity in the Browse modal nor the time series selector (!7460)
- `Added` an Icons story with all our existing icons (!7460)
- `Changed` status code to 403 from 429 when copy business limits are reached (!7396)
- `Removed` the copy feature flags for workspaces i.e. export jobs and scheduling of copy jobs (!7475)
- `Changed` Using `pipe_stats` instead of `pipe_stats_rt` when 7 days is selected in the dashboard stats (!7468)
- `Changed` Rounding the total_price for the reaching your limits emails (!7470)
- `Added` Deleting of scheduled jobs from Google Cloud Scheduler for scheduled pipes that were in a deleted workspace (!7224)
- `Added` Kafka \_\_headers support in the UI (!7425)
- `Added` Support for ingestion of Map column (!7416)
- `Added` Kafka headers ingestion capabilities (!7362)
- `Fixed` Do not check Copy Pipes limit if pipe is not a Copy pipe in /v0/pipes (!7535)

(2023W23) 2023-06-05 - 2023-06-11

---

- `Fixed` Snowflake once ingestion when using @on-demand param (!7449)
- `Fixed` Kafka confirmation dialog now uses new Accessible Modal component (!7419)
- `Added` `data-sr-redact` attribute to hide sensitive data in the Datatables (!7362)
- `Added` DOCS: MV Concepts page (!7194)
- `Changed` Use same clickhouse for local and server (22.8.11.15) (!7305)
- `Fixed` node default names when a new node is added (!7382)
- `Fixed` Missing quantity_gb_processed prop in mailgun payload (!7383)
- `Fixed` Stop displaying "No visualizations yet" in the collapsed event (!7399)
- `Fixed` Shared Data Sources long names are cut off in the Data Flow (!7399)
- `Removed` Code related to `js_errors` Data Source, currently unused (!7399)
- `Removed` JavaScript code related to `idle_events` Data Source, currently unused (!7399)
- `Changed` Use same clickhouse for local and server (22.8.11.15) (!7305)
- `Added` New Google Cloud Storage Connector (!7314)

(2023W22) 2023-05-29 - 2023-06-04

---

- `Fixed` Time Series XSS vulnerabilities (!7354)
- `Fixed` Materialized view outpug graph missing events (!7341)
- `Added` Materialized view output page (!7317)
- `Fixed` Adjust topic list height to maximum modal height (!7284)
- `Added` DOCS: added Grafbase API Gateway docs (!7289)
- `Fixed` schedule validation now not conside `@once` (!7284)
- `Changed` `@once` schedule in External Data Sources is now `@on-demand` (!7250)
- `Fixed` Error with function `toFixedString` when defining `FixedString` fields (!7237)
- `Fixed` Jobs list response to use the `to_public_json` function which will include the pipe details for a job if provided (!7225)
- `Fixed` Exception querying ds details if DS is shared and based in distributed table (!7239)
- `Fixed` Codemirror behaviour in Endpoint Page and in Dashboard (!7273)
- `Changed` Enable Atomic Copy mode by default (!7159)
- `Fixed` Next button misaligned in Snowflake form (!7308)
- `Fixed` DOCS: fix API reference for pipes
- `Fixed` Dashboard table overflow (!7318)

(2023W21) 2023-05-29 - 2023-06-02

---

- `Fixed` Stop inserting data into datasources from dependent materialized nodes in Copy flow (!7306)
- `Fixed` Make datasource shared workspaces number consistent (!7300)
- `Fixed` Jobs list response to use the `to_public_json` function which will include the pipe details for a job if provided (!7225)
- `Fixed` Exception querying ds details if DS is shared and based in distributed table (!7239)
- `Changed` Cron expression validater to croniter and propagate invalid cron expression errors from Google Cloud Scheduler (!7161)
- `Added` New `copy` analysis mode for `/v0/pipes/(.+)/nodes/(.+)/analysis`
- `Fixed` Jobs list response to use the `to_public_json` function which will include the pipe details for a job if provided (!7225)
- `Fixed` Exception querying ds details if DS is shared and based in distributed table (!7239)
- `Changed` Cron expression validater to croniter and propagate invalid cron expression errors from Google Cloud Scheduler (!7161)
- `Changed` billing for queries and calls to endpoints using only service datasources. From now on, this calls won't be charged (!7283)

(2023W21) 2023-05-22 - 2023-05-28

---

- `Change` Sidebar collapsing is only forced now when split screen is active and screen is less than 1200px (!7231)
- `Released` version 1.0.0b332 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!7141)
- `Fixed` Typo in `external_data_source` field in BigQuery Preview (!7222)
- `Added` Limit for maximum number of delete jobs per workspace (!7169)
- `Fixed` Order workspace organization table in UI by billable column (!7229)

(2023W20) 2023-05-15 - 2023-05-21

---

- `Added` Custom stage and integration to Snowflake connector configuration (!7097)
- `Added` Logs for each step in a copy job (!7053)
- `Added` Fill written bytes and rows in `datasources_ops_log` in `replace` mode (!7092)
- `Added` SQL API accepts preview parameter values (!7148)
- `Added` Limit for maximum number of copy pipes per workspace (!7126)
- `Fixed` Wrong colors in Code editor search bar (!7157)
- `Fixed` Data Source options in the sidebar now create a pipe properly (!7130)
- `Fixed` Layout behaviors when resizing the browser in Safari (!7130)
- `Fixed` PUT /v0/pipes/{pipe}/nodes/{node}/copy now supports receiving current mode and schedule cron without failure
- `Fixed` Fixed a typo in the Organizations UI
- `Fixed` Provide correct filters in the workspaces commitment page in the Organization section (!7172)
- `Released` version 1.0.0b329 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!7114)
- `Added` Fill written bytes and rows in `datasources_ops_log` in `replace` mode (!7092)
- `Added` SQL API accepts preview parameter values (!7148)
- `Fixed` Query error returned during high load scenarios

(2023W19) 2023-05-08 - 2023-05-14

---

- `Released` version 1.0.0b328 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!7114)
- `Added` Custom integration and stage names to Snowflake connector (!7081)
- `Added` Unified design tokens colors across the whole ui (!7050)
- `Changed` Improve primary color contrast (!7108)
- `Fixed` Error handling in Import file previews (!7112)
- `Fixed` Warning limit Banner icon size (!7101)
- `Fixed` Race condition when loading Data Source data in split screen (!7118)
- `Fixed` Broken links in Data Source modal (!7051)
- `Fixed` Code editor auto close bracket option works now properly (!7062)
- `Fixed` Table styles in public endpoint page (!7056)
- `Fixed` Kafka column value dialog now renders properly (!7044)
- `Added` Maximum Execution Time limit for Copy Jobs (!7012)
- `Changed` `v0/tokens` now supports data in the body (!7083)
- `Changed` `/v0/pipes/(.+)\.(json|csv|ndjson|parquet)` now supports parameters in the body (!7089)
- `Added` Return a response schema in the OpenAPI spec of Pipes published an endpoint that matches the attributes and types of the default response of the Pipe.
- `Added` Return a response schema in the OpenAPI spec of Pipes published as an API endpoint that matches the attributes and types of the default response of the Pipe.
- `Added` Allow advanced users of BigQuery/Snowflake to specify their own queries without automatic addition of columns (!7470)
- `Released` version 1.0.0b326 of the CLI with support for single line comments in schema definitions. See [changelog](https://pypi.org/project/tinybird-cli/) (!6957)

- `Changed` Improve parquet imports by using jobs and increase parquet file size limit to 1GB (!5978)
- `Changed` Improve parquet imports by using jobs and increase parquet file size limit to 1GB (!6922)
- `Changed` billing for queries using internal datasources (!7028)

(2023W18) 2023-05-01 - 2023-05-07

---

- `Fixed` Accesibility issues in modal component (!7019)

- `Fixed` Accessibility issues in Data Source page (!7011)
- `Fixed` Parsing of cron expressions when creating a scheduled copy pipe (!6976)
- `Added` Allow promoting an existing Data Source to a BigQuery or a Snowflake one (!6964)
- `Added` Searchbar to the Table ui component of the design system lib (!6996)
- `Added` Fill `elapsed_time` in `datasources_ops_log` for HFI (!7505)
- `Released` version 1.0.0b320 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6957)
- `Fixed` Accessibility issues in DataTable component (!7499)
- `Fixed` Accessibility issues in Pipe Options (!6982)
- `Added` Dark version of checkbox and radio inputs (!6924)
- `Fixed` Unpublish endpoint modal now closes the dialog when action is successful (!6992)
- `Removed` `schedule_timezone` parameter when creating or updating copy pipes or nodes and instead use default timezone as UTC (!7016)
- `Fixed` Allow updating of a schedule_cron when updating copy pipes or nodes even if datasource provided is the same (!7016)

(2023W17) 2023-04-24 - 2023-04-30

---

- `Released` version 1.0.0b316 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6780)
- `Fixed` Typo in Data Source shared modal (!6963)
- `Added` DOCS: Billing docs (!6783)
- `Changed` Clarified commitments and usage copy on organizations page to avoid confusion between how Processed Data and Storage are accounted for (!7465)
- `Changed` Branch commands visible in the CLI (!6894)
- `Fixed` Sorting by `used_by` in Browse Data Source modal (!6921)
- `Added` the ability to set the type of node when creating a pipe via API (!6837)
- `Changed` the error message given to the user when re-creating a copy node via API (!6926)
- `Fixed` Handling of raised SQLTemplateException and handle unexpected Exceptions in the Copy API (!6916)
- `Fixed` bug that was impeding some users to push BigQuery-connected datasources. (!6917)
- `Fixed` Show pulse chart for one-off snowflake datasources and the history chart for the scheduled ones. (!6931)
- `Changed` Import File copies (!6914)
- `Added` the ability to set the type of node when creating a pipe via API (!6837)
- `Added` Storybook accesibility testing (!6931)
- `Added` Maximum Active Copy Jobs limit depends on workspace's plan now (!6919)
- `Fixed` Use only the copied block on copy operation in cascade (!6932)
- `Fixed` `node_type` attribute not found in PipeNode (!6949)
- `Added` Maximum Copy Job Frequency limit (!6935)
- `Released` version 1.0.0b316 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6780)
- `Changed` Limits emails to encourage upgrade when hitting the limits (!6980)
- `Changed` Branch commands visible in the CLI (!6894)
- `Fixed` Typo in Data Source shared modal (!6963)
- `Added` DOCS: Billing docs (!6783)

(2023W16) 2023-04-17 - 2023-04-23

---

- `Released` version 1.0.0b300 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6822)
- `Changed` Revert CDK GCP service account key location for Wadus environment (!6817)
- `Changed` Return the Pipe name in the `operationId` attribute of the OpenAPI Spec of the pipe (!7327)
- `Fixed` Close delete modal if a pipe is not removable and not block the UI (!6831)
- `Released` version 1.0.0b303 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6664)
- `Changed` DOCS: removed mention to timezone in Copy API reference (!6830)
- `Added` Snowflake connector UI (!6859)
- `Added` DOCS: API Gateway docs
- `Released` version 1.0.0b307 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6780)
- `Released` version 1.0.0b306 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6780)
- `Released` version 1.0.0b303 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6780)
- `Released` version 1.0.0b303 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6844)
- `Released` version 1.0.0b308 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6866)
- `Released` version 1.0.0b311 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6866)
- `Added` Make it clearer how to interpret the GB / rows stats under a pipe node (!6895)

(2023W15) 2023-04-10 - 2023-04-16

---

- `Fix` Engine guessing for Materialized nodes querying another node or endpoint (!5117)
- `Changed` DOCS: updated Data Source modal screenshots (!6723)
- `Released` version 1.0.0b289 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6664)
- `Fix` Reference to start_datetime changed to start_date in the Organizations tip (!6738)\
- `Released` version 1.0.0b294 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6735)
- `Added` Support to schema evolution (adding new columns) in imports using the CDK. (!6260)
- `Fixed` Reference to start_datetime changed to start_date in the Organizations tip (!6738)
- `Fixed` Prevent naming Pipes using hyphens (!6703)
- `Released` version 1.0.0b298 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6765)
- `Released` version 1.0.0b297 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6653)
- `Released` version 1.0.0b299 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6780)
- `Released` version 1.0.0b300 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6782)
- `Released` version 1.0.0b300 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6776)
- `Fixed` Error 500 on /tokens page (!6761)
- `Fixed` Error when deleting Node from Copy Pipe (!6768)
- `Fixed` Error when deleting a Copy Pipe where the Copy Node is not in the latest position (!6768)
- `Fixed` Reference to start_datetime changed to start_date in the Organizations tip (!6738)
- `Fixed` Reference to start_datetime changed to start_date in the Organizations tip (!6738)
- `Fixed` Prevent naming Pipes using hyphens (!6703)
- `Fixed` Error 500 on /tokens page (!6761)
- `Released` version 1.0.0b289, 1.0.0b294, 1.0.0b297, 1.0.0b298 and 1.0.0b299 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)

(2023W14) 2023-04-03 - 2023-04-09

---

- `Released` version 1.0.0b284 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6653)
- `Fixed` results preview for queries in pipes that return infinity and not a number as null
- `Added` Confirmation modal when performing destructive actions in the UI (!6707)
- `Changed` Token actions are always visible in header (!6670)
- `Fixed` Token selection in browse modal fixed to work by url (!6711)
- `Fixed` Sidebar items reorder when selected item is recently used (!6702)
- `Fixed` Time Series table totals were not updating properly when selecting time range in the graph (!7182)
- `Changed` Make datasource shared workspaces number consistent even if user doesn't have access to some of them (!6689)
- `Fixed` Return pipe name instead of endpoint name in the `summary` attribute of the OpenAPI spec of a pipe endpoint (!7167)
- `Changed` Enforce limits importing big files by url, depending on plan. Limit configurable internally (!6868)
- `Fixed` Double quotes will not be removed from endpoint parameter values used in expressions (!6572)
- `Released` version 1.0.0b284 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6653)
- `Released` version 1.0.0b285 of the CLI with internal improvements. (!6685)

(2023W13) 2023-03-27 - 2023-04-02

---

- `Released` version 1.0.0b286 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6625)
- `Released` version 1.0.0b280 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6616)
- `Released` version 1.0.0b283 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6595)
- `Fixed` Time Series date filter change when visualization is public (!6627)
- `Fixed` Duplicating a Copy Pipe through POST `/v0/pipes/?`. (!6557)
- `Fixed` workspace cluster selection for Enterprise customers (!6556).
- `Fixed` Default values in negative `Float` and `Int` query parameters were null on the Pipe info. (!6558)
- `Fixed` Kafka Schema registry credentials correctly parsed (!6537).
- `Changed` Block some modals to be closed clicking outside (!6639)
- `Fixed` Some fixes for openapi.json for a pipe endpoint to pass the OpenAPI validator (!6642).
- `Released` version 1.0.0b280 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6616)
- `Fixed` Error on Snapshots page when trying to get pipe's mode (!6626)
- `Fixed` Default values in negative `Float` and `Int` query parameters were null on the Pipe info. (!6558)

(2023W13) 2023-03-27 - 2023-04-02

---

- `Added` Allowed to specify ENGINE for Kafka datasources at API level. (!6591)
- `Fixed` Default values in negative `Float` and `Int` query parameters were null on the Pipe info. (!6558)
- `Fixed` workspace cluster selection for Enterprise customers (!6556).
- `Fixed` Enforce limits when import files using url (!6868)
- `Fixed` Fix kinesis ingestion by returning proper body and HTTP code. (!6889)
- `Added` pricing section to Copy API reference. (!6600)

(2023W13) 2023-03-27 - 2023-04-02

---

- `Fixed` workspace cluster selection for Enterprise customers (!6556).

(2023W13) 2023-03-27 - 2023-04-02

---

- `Fixed` workspace cluster selection for Enterprise customers (!6556).

(2023W12) 2023-03-20 - 2023-03-26

---

- `Added` Advanced settings (engine, ttl, partition key and sorting key) to datasource creation in the UI (!6500)
- `Released` version 1.0.0b272 of the CLI with telemetry reporting. Telemetry data helps out team understand how the commands are used so we can improve your experience. For more information and how to opt-out for this feature, please refer to our [CLI docs](https://www.tinybird.co/docs/cli.html#cli-telemetry). (!6409)
- `Changed` Token refresh confirmation is displayed as a destructive action now (!6483)
- `Added` `copy_timestamp` default parameter that matches the `timestamp` column on `datasource_ops_log` Data Source entry for the generated job. (!6327)
- `Added` support `output_format_parquet_string_as_string` to `v0/sql` when exporting with `FORMAT Parquet` and `v0/pipes/:pipe.parquet`. (!6506)
- `Released` version 1.0.0b274 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6514)
- `Changed` Block some modals to be closed clicking outside (!6519)
- `Fix` Fix kinesis ingestion by returning proper body and HTTP code. (!6889)
  (2023W12) 2023-03-20 - 2023-03-17

---

- `Fixed` Enforce limits when import files using url (!6868)
- `Added` `copy_timestamp` default parameter that matches the `timestamp` column on `datasource_ops_log` Data Source entry for the generated job. (!6327)
- `Released` version 1.0.0b272 of the CLI with telemetry reporting. Telemetry data helps out team understand how the commands are used so we can improve your experience. For more information and how to opt-out for this feature, please refer to our [CLI docs](https://www.tinybird.co/docs/cli.html#cli-telemetry). (!6409)

(2023W11) 2023-03-13 - 2023-03-19

---

- `Added` PUT endpoint for Scheduled Copy nodes. This allows modifying the Target Data Source of a Copy Pipe, as well as adding or modifying a Schedule. Read [docs](<https://www.tinybird.co/docs/api-reference/pipe-api.html#put--v0-pipes-(.+)-nodes-(.+)-copy>) for more details. (!6257)
- `Changed` Removed Recently viewed and fill the space in the sidebar with entities (!6049)
- `Changed` the datasource settings validation to give proper errors (!6405)
- `Fixed` Sidebar not refreshing when navigating from TimeSeries to Tokens (!6474)
- `Fixed` Date format in Populate progress query (!6453)
- `Fix` Date format in Populate progress query (!6453)
- `Fix` Fixed Time Series date filters (!6420)
- `Fix` Fixed internal bugs in the CLI (!6428)
- `Fix` cURL snippet in Organizations Monitoring sample usage (!6443)
- `Fix` endpoint curl snippet in the sample usage created correctly (!6443)
- `Fix` Storage metrics in the UI are correct from now on (!6443)
- `Fix` UTC labels included in the pulse metrics and BigQuery synchronization (!6443)
- `Released` version 1.0.0b268 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6384)
- `Changed` DOCS: Improve Replaces docs, including examples (!6438)

- `Released` version 1.0.0b270 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6013)
- `Fix` Remove copy dependencies on pipe copy and node copy deletes (!6860)

(2023W10) 2023-03-06 - 2023-03-12

---

- `Fixed` Some Data Sources and Endpoints were not accessible using the BI Connector. We have fixed problems related to some column types not being supported: `Bool`, `Ìnt128`, `UInt128`, `Int256` and `UInt256`. (!5990)
- `Added` PUT endpoint for Scheduled Copy nodes. This allows modifying the Target Data Source of a Copy Pipe, as well as adding or modifying a Schedule. Read [docs](<https://www.tinybird.co/docs/api-reference/pipe-api.html#put--v0-pipes-(.+)-nodes-(.+)-copy>) for more details. (!6257)
- `Fixed` DOCS: Correct Copy API endpoints scopes information (!6371)
- `Fixed` If a Copy execution fails during an API call, including failures that occur before the Copy Job is created, log the error on `datasource_ops_log`. (!6391)
- `Changed` Change return http codes for some errors to improve error handling (!5490)
- `Fixed` Add complex types (UUID, datetimes) to avro decoding in kafka ingestion (!6801)
- `Added` More than 300 ClickHouse functions to our autocomplete reference that can be used in a template as described in our [docs](https://www.tinybird.co/docs/cli/advanced-templates.html) (!6297)
- `Changed` Link in materialized nodes now opens the target Data Source in split screen. (!6342)
- `Fixed` Layout width calculations when split screen is not active and sidebar is collapsed (!6322)
- `Changed` Node editor in full screen now fills the whole screen (!6328)
- `Fixed` Styles in DataTable checkbox are now properly applied (!6396)
- `Fixed` UI: Guided step issues when a workspace is shared (!6686)
- `Fixed` Fix time series filtering by URL (!6303)
- `Fixed` A bug that didn't unlink correctly materialized views when there was two materialized nodes with the same name and the target data source was deleted (!6336)
- `Fixed` A bug that made possible to publish a materialized node and an endpoint in the same pipe (!6320)
- `Fixed` A bug that made possible to change the published node of an endpoint used in a materialized node (!6357)
- `Fixed` A bug that made possible to force push a pipe used in a materialized node (!6357)
- `Fixed` An issue when parsing the IMPORT_QUERY parameter (!6762)
- `Fixed` Issue editing a node name on last version of Firefox (!6355)
- `Fixed` Invite users actions fixed (!6308)
- `Fixed` Prevent modal to close when the click starts in the modal and ends outside (!6382)
- `Released` version 1.0.0b265 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5952)
- `Changed` the guide about testing to include more information about CI and regression test (!6312)
- `Fixed` Override billing configs in Cheriff does not update "billing and members" UI (!6385)
- `Fixed` Removed TTL for `bi_stats` Data Source schema (!6395)

(2023W09) 2023-02-27 - 2023-03-05

---

- `Added` BigQuery guide link to Import modal in the UI (!6281)
- `Added` DOCS: Add the concurrency limit to the BigQuery Connector docs (!6239)
- `Added` Organizations docs
- `Added` DOCS: BigQuery docs (!6199)
- `Changed` DOCS: Re-organization of docs (!5855)
- `Released` version 1.0.0b253 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5952)
- `Released` versions 1.0.0b257, 1.0.0b258, and 1.0.0b259 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (#6590, !6152, !6182)
- `Changed` Prevent users from changing the schema when Data Source import is BigQuery (!6211)
- `Fixed` Avoid looking for integration projects when selected token is null (!6299)
- `Fixed` Change Big Query Data Source runs order from left to right (!6277)
- `Fixed` Javascript error that was causing snippets in shared endpoints to not work (!6282)
- `Fixed` Confetti was not displaying properly when publishing a new endpoint (#6285)
- `Fixed` UI: Fix import modal scroll (#6620)
- `Released` version 1.0.0b258 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (#6590)
- `Released` versions 1.0.0b257, 1.0.0b258, 1.0.0b259, and 1.0.0b260 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (#6590, !6152, !6182, #6625)
- `Added` Scheduled Copy API reference (!6217)
- `Released` version 1.0.0b261 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (#6295)
- `Fixed`: Bug with remove endpoint via API (!6242)
- `Fixed`: Not grouping by datetime in usage metrics timeseries link (!6629)
- `Fix`: Bug with remove endpoint via API (!6242)
- `Fix`: Not grouping by datetime in usage metrics timeseries link (!6629)
- `Added` Check dependent Copy Pipes when removing a target Data Source (!6259)

(2023W08) 2023-02-20 - 2023-02-26

---

- `Released` versions 1.0.0b253, 1.0.0b254, 1.0.0b255, and 1.0.0b256 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5952)

(2023W07) 2023-02-13 - 2023-02-19

---

- `Fixed` Send TTL when creating a new BigQuery Data Source (!6064)
- `Added` `type` property on Pipes (!6037)
- `Added` API endpoint to create pipes of type `copy` (!6037)
- `Fixed` Improve applying TTL performance and increase alter timeout (!4139)
- `Fixed` `pipe_name` field in `pipe_stats_rt` correct even when querying endpoints using the Pipe ID instead of the Pipe name (!5894)
- `Changed` Unify BigQuery icon in code editor, data graph and datasource list modal (!6051)
- `Changed` Avoid guest users from unsharing Data Sources in workspaces where they are not admin (!6054)
- `Changed` Improve placement of Guided Tour in the sidebar to be able to browse Data Sources with the tour active (!5988)
- `Changed` Avoid guest users from sharing Data Sources in workspaces where they are not admin (!5967)
- `Released` version 1.0.0b244 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5533)
- `Fixed` We've added more precission on the Dashboard processed stats for more than 1 day ago data (!5892)
- `Changed` UI: In the pipeline page, when clicking on a node name in the editor, opens the results on split screen instead of a modal (!5999)
- `Released` version 1.0.0b249 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5972)
- `Changed` UI: In the pipeline page, when clicking on an endpoint in the editor, opens the results on split screen instead of a modal (!6409)
- `Released` version 1.0.0b251 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6024)

(2023W06) 2023-02-06 - 2023-02-12

---

- `Added` DOCS: Add docs for error handling & retries for Events API
- `Fixed` Restore focus in add members dialog when is open from workspace settings (!5869)
- `Changed` Change CI test to run through varnish (!5943)
- `Fixed` Table cached sorting in dashboard is applied properly (!5940)
- `Fixed` API Endpoint stats create a TimeSeries visualization instead redirecting to Karman (!5915)
- `Fixed` Fixed the table top border in the Data Source log tab (!5912)
- `Fixed` Fixed the table top border in the Data Source log tab (!5912)
- `Fixed` Tooltip for Data Source operations in consumption graph (!5933)
- `Fixed` Added Pulse component to missing screens (!5929)
- `Fixed` Fixed the table top border in the Data Source log tab (!5912)
- `Changed` Improved compatibility with ClickHouse syntax
- `Released` version 1.0.0b242 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6186)
- `Fixed` Possibility to materalize a node which gave a timeout (!5914)
- `Released` version 1.0.0b241 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6186)
- `Released` version 1.0.0b244 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5533)
- `Fixed` Allow to refresh the user token (!5931)
- `Fixed` Fixed the table top border in the Data Source log tab (!5912)
- `Changed` Improved compatibility with ClickHouse syntax
- `Released` version 1.0.0b242 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!6186)
- `Fixed` Not loose the changes if you edit a query while it's been executed (!5926)

(2023W05) 2023-01-30 - 2023-02-05

---

- `Added` Usage metrics available for any workspace member (!5777)
- `Changed` Estimation and next invoice amounts appear with only 2 decimals (!5777)
- `Changed` Log analytics banner steps. (!5777)
- `Changed` New label for storage metrics graph (!5794)
- `Fixed` Time series not found error when no visualizations are created yet. (!5843)
- `Fixed` Add confirmation step to Data Source TTL modal (!5856)
- `Changed` Add lock focus to empty dialogs (!5826)
- `Fixed` Data Source relationships are not removed if a Data Source is deleted. (!5815)
- `Added` Allow set partition key and sorting key in kafka datasources. (!5140)

(2023W04) 2023-01-23 - 2023-01-29

---

- `Added` Adapted the remaining tests to run always on cluster. (!4768)
- `Fixed` Labels in token scope forms are now visible over light backgrounds. (!5746)
- `Fixed` Data Flow graph shows correctly Shared Data Sources after data is refreshed (!5702)
- `Added` New `date_diff_in_seconds` —and its variants in minutes, hours, and days— function added to templating language (!5351)
- `Fixed` Import Data Sources via url now updates the schema properly (!5682)
- `Fixed` Adding a new scope from the UI displays the labels correctly (!5688)
- `Fixed` Don't block the clean up button when dependencies are loading in the Browse Data Sources modal (!5741)
- `Changed` Better explained what "Read and write" means in the processing graph (!5763)
- `Fixed` User emails in Tinybird aren't case sensitive (!5742)
- `Released` version 1.0.0b234 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5657)
- `Changed` Update file size limits (!5686)

(2023W03) 2023-01-16 - 2023-01-22

---

- `Added` New Data Source import modal. (!5799)
- `Added` New Confluent import option added (!5677)

(2023W02) 2023-01-09 - 2023-01-15

---

- `Fixed` Safari rendering issues: blurry image and wrapping text (!5603) (!5476)
- `Added` Adapted test to run always on cluster. (!4768)
- `Changed` DOCS: Update API reference page & moved Build plan pricing to API Concepts
- `Released` version 1.0.0b225 of the CLI including a new `tb diff` command to compare local with remote files. See [changelog](https://pypi.org/project/tinybird-cli/) (!5536)
- `Released` version 1.0.0b232 of the CLI including a new `tb prompt` command. See [changelog](https://pypi.org/project/tinybird-cli/) (!5566)
- `Removed` Old BigQuery Connector Guide
- `Added` Adapted some tests that escaped the first modification to run always on cluster. (!4768)
- `Changed` DOCS: Update Query API reference to take into account the data encoding.
- `Changed` DOCS: Update Query API reference to take into account the data encoding.
- `Fixed` Allow copying of text in Firefox browsers (!5626)
- `Fixed` Allow copying of the Data Source schema (!5626)
- `Changed` Improve Parquet ingestion performance
- `Changed` DOCS: Update Query API reference to take into account the data encoding.
- `Fixed` Improve memory consumption importing csv (!5698)
- `Added DOCS: Adds Iterating Data Sources guide`
- `Added` UI: Added a check icon to the node when it's materialized.
- `Changed` DOCS: Added Quarantine explanation at Main Concepts > Data Sources and edited Quarantine guide (!5541)
- `Changed` When a populate job fails for the first time, the related Materialized View is unlinked. See [docs](<https://www.tinybird.co/docs/api-reference/pipe-api.html#post--v0-pipes-(.+)-nodes-(.+)-population>) for more details (!5015)
- `Changed` UI: Renders the error returned by the API on the Kafka import modal when credential don't have enough permissions (!5595)
- `Released` version 1.0.0b220 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5252)
- `Fixed` Data Source rename message doesn't warn anymore about errors in dependant entities (!5511)
- `Fixed` Materialized View icon size in Pipe page (!5531)
- `Fixed` Style in populate error (!5547)
- `Fixed` Billing metrics for custom and tinybird plans (!5535)
- `Fixed` Data Source log editor works as expected (!5552)
- `Changed` Guess type of HH:MM:SS is String instead of DateTime (!5513)
- `Fixed` Upgrade plan button (!5562)
- `Fixed` When filtering by dragging and dropping in the exploration chart, it doesn't lose all filters and settings (!5556)
- `Fixed` Limit tokens with TOKENS scope for guests users in the UI (!5491)
- `Released` version 1.0.0b222 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5515)
- `Added` `dry_run` parameter to POST /v0/datasources/(.+)/delete API to enable checking `delete_condition` matched rows (!5497)
- `Released` version 1.0.0b223 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5520)
- `Released` version 1.0.0b228 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5125)

(2023W01) 2023-01-02 - 2023-01-08

---

- `Changed` DOCS: Clarified that only JSONPaths can be altered for existing Data Sources (!5421)
- `Fixed` Add missing `root-directory=dashboard` param to Vercel link in Log Analytics Starter Kit onboarding (!5442)
- `Fixed` Hide layout resizer on hover when some modal or dialog is active (!5462)
- `Fixed` Delete datasource operation now is atomic by passing force=true as param (!5469)
- `Fixed` Add missing scroll to Analytics Banner component (!5487)
- `Added` Support arbitrary binary buffers on Kafka keys while using Schema Registry
- `Added` API support for Avro with Schema Registry Kafka deserialization of keys (!5464)
- `Changed` UI: Add a 30 days value in granularity dropdown Time series (!4520)
- `Changed` DOCS: Clarified that only JSONPaths can be altered for existing Data Sources (!5421)
- `Fixed` Add missing `root-directory=dashboard` param to Vercel link in Log Analytics Starter Kit onboarding (!5442)
- `Changed` Added the possibility of ingest data using different kafka clusters.
- `Changed` DOCS: Update API reference page & moved Build plan pricing to API Concepts
- `Changed` Usage metrics graph UI at the billing modal (!5461)

(2022W52) 2022-12-26 - 2023-01-01

---

- `Released` version 1.0.0b218 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5252)
- `Released` version 1.0.0b219 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5252)
- `Changed` UI: Reorder the elements in the Node dropdown menu, gives feedback when the endpoint or the MV can not be created (!4812)
- `Changed` DOCS: Clarified that only JSONPaths can be altered for existing Data Sources (!5421)

(2022W52) 2022-12-26 - 2023-01-01

---

- `Added` Service Data Sources in split screen mode. (!5391)
- `Added` When you create a workspace from a Log Analytics Starter kit, a new onboarding process appears (!5407)
- `Changed` `tinybird.datasources_ops_log`. `populateview` records are now being registered for populateview jobs lasting up to 8 hours (!4960)
- `Fixed` Add new columns in the UI now displays a loading state until the operation is completed and a notification error in case of error. (!5395)
- `Added` Enable the pulse graph for materializations from Kafka Data Sources (!5348)
- `Added` Allow defining jsonpaths to existing CSV datasources. (!5137)
- `Added` Service Data Sources in split screen mode. (!5391)
- `Changed` Schema and engine data now appears in Service Data Sources. (!5412)
- `Changed` DOCS: Update API reference page & moved Build plan pricing to API Concepts
- `Changed` `tinybird.datasources_ops_log`. `populateview` records are now being registered for populateview jobs lasting up to 8 hours (!4960)
- `Fixed` Hide shared datasources in browse datasource modal. (!5410)
- `Fixed` Add new columns in the UI now displays a loading state until the operation is completed and a notification error in case of error. (!5395)
- `Released` version 1.0.0b214 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5409)

(2022W51) 2022-12-19 - 2022-12-25

---

- `Changed` DOCS: Split GCS & S3 guides into separate pages
- `Fixed` Updating a Pipe with an existing endpoint through the API is now atomic: the endpoint node is maintained when overwriting a Pipe if the node maintains its name. (!5361)
- `Added` DOCS: Added Query API vs API EP question to FAQ
- `Fixed` Allow unlinking of self-referencing -same origin and target Data Source- Materialized Pipe (!5297)
- `Added` New Import File/Url flow under `external_datasources` FF (!5213)
- `Added` Starter kits: New `Log Analytics` starter kit added (!5350)
- `Added` UUID column type available in the UI (!5352)
- `Changed` Quarantine rows number formatted in the UI (!5352)
- `Fixed` Adding a new column works when a column has a DEFAULT value (!5352)
- `Fixed` Hide split view resizer when it shouldn't be enabled (!5465)
- `Released` version 1.0.0b213 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5392)
- `Changed` DOCS: Update API reference page & moved Build plan pricing to API Concepts

(2022W50) 2022-12-12 - 2022-12-18

---

- `Added` DOCS: How to set the TTL of a new Data Source in UI/CLI
- `Changed` DOCS: Update name substitution to always call the product 'Tinybird' instead of 'Tinybird Analytics'
- `Changed` DOCS: Concepts pages meta descriptions
- `Added` DOCS: Guide for [consuming API Endpoints in Grafana](https://www.tinybird.co/docs/guides/consume-api-endpoints-in-grafana.html) (!5337)
- `Added` DOCS: Documents the API parameter `dialect_new_line`, which allows users to explictly set a record delimiter in CSV imports.
- `Added` DOCS: Guide for [ingesting data from AWS Kinesis](https://www.tinybird.co/docs/guides/ingest-from-aws-kinesis.html) (!5289)
- `Changed` The pipes API now have a new restriction that forbids updating or deleting a node that's being used in a Materialized Node. Materialized Nodes are "immutable" you have to fully overwrite the pipe with `--force` or `force=true` or delete and create again the Materialized Node to make a change. (!4702)
- `Added` a safety check when creating Materialized Views to avoid issues with bad-picked partition keys. (!5307)
- `Released` version 1.0.0b212 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5334)

(2022W49) 2022-12-05 - 2022-12-11

---

- `Added` DOCS: Guide for deleting Workspaces
- `Changed` DOCS: Update Karman refs to Time Series
- `Changed` DOCS: [API limits](https://www.tinybird.co/docs/api-reference/api-reference.html#id8) Response limits from 10MB to 100MB (!5251)
- `Changed` DOCS: Re-structure Guides
- `Changed` DOCS: Updates Main Concepts section to simplify content for new users
- `Added` DOCS: Guide for deleting Workspaces
- `Changed` DOCS: Update Karman refs to Time Series
- `Fixed` show labels in empty state for DS logs graph (!5283)
- `Changed` DOCS: [API limits](https://www.tinybird.co/docs/api-reference/api-reference.html#id8) Response limits from 10MB to 100MB (!5251)
- `Fixed` Improve metrics queries that were being filtered incorrectly (!5325)
- `Fixed` forbid access to API endpoints after workspace deletion. (!5266)
- `Fixed` reduce number of fetch to /metrics endpoint in DS screen. (!5279)
- `Fixed` forbid access to API endpoints after workspace deletion. (!5266)
- `Fixed` The description font-size of the Tip sections is fixed (!5275)
- `Fixed` Properly limit the max file size for Parquet files to 50MB (!5269)

(2022W48) 2022-11-28 - 2022-12-04

---

- `Added` DOCS: Adds Concepts section
- `Changed` DOCS: Add FAQ for changing Kafka DS sorting key
- `Changed` DOCS: Remove (beta) from Tips & CLI docs titles
- `Added` DOCS: Adds FAQ section
- `Changed` DOCS: Updated BI Connector best practices
- `Added` DOCS: Added best practices to work with the BI connector (postgres interface to Tinybird)
- `Fixed` Type range checks in unsigned integers. (!5251)
- `Changed` DOCS: updated example JSON response for GET v0/datasources API https://gitlab.com/tinybird/tinybird-docs/-/issues/8
- `Changed` DOCS: updated GET /pipes API response example (docs#11)
- `Changed` Introduction page with new content / videos / links
- `Added` brand new Quick Start guides for CLI & UI
- `Fixed` Remove or rename datasources with some specific pattern name. (!5162)
- `Fixed` a crash when choosing full populate materializing a very recently created Data Source. (!5183)
- `Fixed` an unwanted CH Exception by temporarily allowing it, until the upstream PR is merged. (!5223)
- `Added` Partial replaces now report the condition used in the Job view. (!5205)
- `Fixed` 500s returned in some cases when a user tries to update a Token using the PUT method over `/v0/tokens/`. (!5207)
- `Released` version 1.0.0b211 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5191)
- `Fixed` pipes UI when they had their endpoints published through the `tb publish` CLI command. The UI didn't reflect that the pipes had a published API (!5236)
- `Fixed` added scheck to verify that the previous state is not null before adding the new pipe to the list on the ADD_PIPELINE reducer (!5244)
- `Added` Documentation for two new service datasources `bi_stats_rt` and `bi_stats`. (!5237)
- `Fixed` Key shortcuts for the query editor working properly now (!5234)
- `Fixed` Bring back the Cmd/Ctrl + Enter shortcut to run a Node (!5258)
- `Added` new ingestion modal UI under `external_datasources` FF (!5211)

(2022W47) 2022-11-21 - 2022-11-27

---

- `Changed` New changelog page for help
- `Fixed` Analyze parquet files bigger than 32Mb. (!4357)
- `Added` BI Connector and Query API stats on Dashboard screen. (!5203)
- `Added` documentation for the supported ClickHouse data types when [creating a Data Source from a schema](https://www.tinybird.co/docs/api-reference/datasource-api.html#create-from-schema). (!4949)
- `Added` created a guide where explains how to integrate google cloud pubsub push subscription delivery type with tinybird MV. [google-cloud-pubsub-integration](https://www.tinybird.co/docs/guides/google-cloud-pubsub-integration.html) (!5200)
- `Fixed` Layout rerenders on split screen route change. (!5208)
- `Added` created a guide where explains how to integrate google cloud pubsub push subscription delivery type with tinybird MV. [google-cloud-pubsub-integration](https://www.tinybird.co/docs/guides/google-cloud-pubsub-integration.html) (!5200)
- `Added` created a guide where explains how to integrate google cloud pubsub push subscription delivery type with tinybird MV. [google-cloud-pubsub-integration](https://www.tinybird.co/docs/guides/google-cloud-pubsub-integration.html) (!5200)

(2022W46) 2022-11-14 - 2022-11-20

---

- `Changed` default behavior regarding the truncation of the target Data Source when populating a Materialized View. API and CLI will both default to not truncating. UI will be explicitly truncating. See [Pipes API - POST /v0/pipes/(.+)/nodes/(.+)/population](<https://www.tinybird.co/docs/api-reference/pipe-api.html#post--v0-pipes-(.+)-nodes-(.+)-population>) (!5131)
- `Fixed` Data Source sharing from sidebar. It was not displaying properly when option was selected. (!5157)
- `Added` Data Source split screen resizing (!4909)
- `Fixed` issue when truncate a quarantine table and the related datasource was created with Null Engine (!4588)
- `Fixed` Improve error messages when a number conversion fails due the value is out of range. Standardize messages with same error in dates. (!3996)
- `Fixed` issue with NDJSON/Parquet files containing many columns (!5009)
- `Changed` Scrollbar design to show only when the section is hovered or focused. (!5167)
- `Changed` Improved two details at Rudderstack guide: regex to skip dots and url of the events API. See [Streaming via Rudderstack](https://www.tinybird.co/docs/guides/streaming-via-rudderstack.html#create-a-rudderstack-destination)(!5110)
- `Added` documentation about how to interpret timestamps in query results (!5103).
- `Fixed` `tinybird.datasources_ops_log`. `populateview` records were not being properly registered when pusing a pipe with `force=true` (!5092)
- `Added` Kafka support for raw (non UTF-8) keys (!5120).
- `Fixed` UI crash when refreshing a token in different tabs (!5137)

---

- `Fixed` Date Picker in Time Series screen for firefox (!5154)
- `Fixed` the logic that shows warnings and Pro Tips. Now any new Pro Tips or warning coming from the API will show, without having to add custom logic in the UI. (!5054)
- `Added` Full append and materializations logs in [`tinybird.datasources_ops_log`](https://www.tinybird.co/docs/monitoring/service-datasources.html#tinybird-datasources-ops-log).
- `Added` documentation about how to interpret timestamps in query results (!5103).
- `Added` Kafka support for raw (non UTF-8) keys (!5120).
- `Changed` Improved two details at Rudderstack guide: regex to skip dots and url of the events API. See [Streaming via Rudderstack](https://www.tinybird.co/docs/guides/streaming-via-rudderstack.html#create-a-rudderstack-destination)(!5110)
- `Fixed` `tinybird.datasources_ops_log`. `populateview` records were not being properly registered when pusing a pipe with `force=true` (!5092)
- `Fixed` issue when truncate a quarantine table and the related datasource was created with Null Engine (!4588)
- `Fixed` Improve error messages when a number conversion fails due the value is out of range. Standardize messages with same error in dates. (!3996)
- `Fixed` issue with NDJSON/Parquet files containing many columns (!5009)
- `Fixed` Fixed issue related to a referrer used to track login origins causing the login to fail sometimes. (!5156)
- `Released` version 1.0.0b209 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4910)
- `Fixed` Skip checking queries with `ARRAY JOIN`s in materialized view `GROUP BY` restrictions.
- `Fixed` Import simple csv with header and a row. Also use escape char if exists to guess separator. (!3676)
- `Added` support to Parquet files containing 'bytes' type (!5102)
- `Fixed` update HFI frequency after configuration (!3970)
- `Changed` Data Source data is requested when import job is successful (!5097)
- `Fixed` copy button position in Data Source Events log (!5096)

(2022W45) 2022-11-07 - 2022-11-13

---

- `Fixed` `GROUP BY` restrictions on Materialized Views creation now allow for statements in between the left table and a `GROUP BY` clause with multiple columns (!5079)
- `Added` Enabled Data Source Pulse graph for Materialized Views coming from Kafka appends (!5057)
- `Changed` Events API docs link in new Data Source modal (!5073)
- `Changed` Improve v0/events with concurrency-based rate limits with best-effort service. See [API docs](https://www.tinybird.co/docs/events-api)
- `Fixed` Report 100% progress at most and 0 estimated remaining time at least in populate queries (!4760)
- `Fixed` Some Data Sources and Endpoints weren't being accessible from the BI Connector. We have fixed problems related to some column types not being supported. For example, types Like `Array(Tuple(String, Float32))` and `Array(DateTime64(3))` are now correctly supported. (!5035)
- `Fixed` New datepicker range component for Time Series filters without bugs (!5061)
- `Changed` Improve v0/events with concurrency-based rate limits with best-effort service. See [API docs](https://www.tinybird.co/docs/events-api).
- `Fixed` typo in import snippet modal (!5056)
- `Fixed` Broken internal links in guides (!4887)
- `Fixed` Notification banner styles in Data Source page for screens small screens (!5091)
- `Fixed` performance of Data Source Page when update schema actions are active (!5038)
- `Fixed` Wrong extra value at Time series tooltip graph when there is a Group By value (!5090)
- `Fixed` Padding on Time Series tooltip graph (!5090)
- `Released` version 1.0.0b208 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!5078)

(2022W44) 2022-10-31 - 2022-11-06

---

- `Released` version 1.0.0b208 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4977)
- `Released` version 1.0.0b207 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4917)
- `Added` Data Source page UI in both full and split screen mode. This page shows the data source details, the schema, and the data preview. (!5023)
- `Added` Drill down on the time series graph (!4968)
- `Added` /timeseries url to redirect to redirect to the first visualization by defaoult or the onboarding page if there is any (!4997)
- `Added` `tinybird.datasources_ops_log` now contains two additional entries for populate jobs. When the populate job is created a `populateview-queued` entry is added to the target Data Source of the Materialized View, when the job is finished a `populateview` entry is added. Dependent Materialized Views triggered due to the populate job will also have `populateview` entries. These entries are handy for observability and tracing purposes. See [example query](<https://www.tinybird.co/docs/api-reference/pipe-api.html#post--v0-pipes-(.+)-nodes-(.+)-population>) (!4881)
- `Changed` Import modal tabs to improve accesibility and be easier to test (!4966)
- `Changed` message displayed in Import modal when file size exceeds the limit (!4957)
- `Changed` focus state of Button and IconButton components (!4957)
- `Fixed` Errors inserting DateTime64 should be stored in quarantine if the type is composed by precision or timezone. Also applies to DateTime. (!1621)
- `Changed` body sent in Event API requests to a more complete object (!4998)
- `Changed` Help icon (!5005)
- `Fixed` rounded big integers in the Data Source table (!5058)
- `Fixed` ingested rows message in Data Source pulse when count is one (!5037)
- `Fixed` Token input min width to prevent copy button from disappearing (!5025)
- `Fixed` missing parameters in Close button for Data Source not found page (!5006)
- `Fixed` closing split screen if some input is focused and Escape key is pressed (!4972)
- `Fixed` missing close button in Data Source page if it isn't found (!4972)
- `Fixed` Cancel old populates on push pipe force correctly (!4971)
- `Fixed` GROUP BY restrictions on Materialized Views creation (!4967)
- `Fixed` Default type for new columns created using UI is Nullable(String) instead of String (!3840)
- `Fixed` Usage graph tooltip (!5005)

(2022W43) 2022-10-24 - 2022-10-30

---

- `Fixed` Full support for '+' signs in email addresses (!4903)
- `Added` CSV preview custom delimiter option (!4930)
- `Added` Data Source pulse graph for materialized datasources (!4890)
- `Added` support for showing warnings when creating a Materialized View (!4535)
- `Fixed` Copy button position in add Data Source modal (!4903)
- `Fixed` the dialog shown when clicking in value column of Kafka Data Sources. Now, the dialog is not partially hidden if there are other banners at the bottom, like the quarantine warning or the new columns banner. (!4946)
- `Fixed` styles of scope token modal to match new global design updates (!4937)
- `Fixed` racy values of rows & rows_quarantine in datasources ops logs for LFI appends (!4908)
- `Fixed` the minimun width of Delimiter select in CSV previews to prevent cut texts (!4898)
- `Fixed` an issue that would prevent timestamp column to appear in Data Source table when ingestion comes from Kafka (!4904)
- `Fixed` requests to Time Series data when no Data Source or Date Column is selected yet to avoid error responses from the server (!4648)
- `Fixed` Data Source showing null as description when coming from a Materialization (!4919)
- `Fixed` appending a new node to a Pipe via CLI (!4924)
- `Fixed` query editor autocomplete hints to be case insensitive (!4931)
- `Fixed` Improved how we check if a login session is active (!4951)
- `Changed` data displayed in Data Source pulse graph tooltips adding the date of the selected ingestion (!4897)
- `Changed` Data Source description default visibility hiding it only when it has three lines or more (!4882)
- `Changed` check session behaviour by adding 3 retrys when the request to the server fails due to Network problems (!4906)
- `Changed` the names of Kafka metadata fields from `timestamp`, `value`, `topic`, `offset`, `key`, `partition` to `__timestamp`, `__value`, `__topic`, `__offset`, `__key`, `__partition` to prevent conflicts in case same keys are provided in the ingested data (!4645)
- `Released` version 1.0.0b202 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4859)
- `Released` version 1.0.0b205 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4945)
- `Released` version 1.0.0b206 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4928)

(2022W42) 2022-10-17 - 2022-10-23

---

- `Added` Show/hide to datasource description (!4874)
- `Fixed` Run Button loading state (!4872)
- `Added` Browse Tokens modal (!4860)
- `Fixed` Return empty pipeline list in case datasource is not found when requesting delete (!4855)
- `Changed` Limit Datasource API calls to improve performance (!4832)
- `Added` Filter partitions before running a populate.
- `Fixed` Refresh pipelines instead of requesting all dependencies (!4834)
- `Released` version 1.0.0b200 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4580)
- `Released` version 1.0.0b198 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4817)

(2022W41) 2022-10-10 - 2022-10-16

---

- `Changed` Updated tooltip styles and added missing shortcuts (!4579)
- `Changed` Only display one day of datasources_ops_log in the Data Source log tab (!4808)
- `Released` version 1.0.0b197 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4801)

(2022W40) 2022-10-03 - 2022-10-09

---

- `Added` Actions button on top right corner of the Time Series page. (!4728)
- `Added` Be able to hide other results on time series graph. (!4742)
- `Added` Advanced and simple mode on timeseries query editor. (!4758)
- `Fixed` Tooltip in entities menu. (!4756)
- `Fixed` Datasource OpsLog copy button background color. (!4732)
- `Fixed` Null values in DataSourceMetrics Graph. (!4730)
- `Fixed` DataLog width when is displayed in modal view. (!4727)
- `Fixed` Added @tinybird/ui styles to timeseries entrypoint. (!4719)
- `Added` Disable node edition in materialized pipes (!4737)

(2022W39) 2022-09-26 - 2022-10-02

---

- `Changed` Improve delete Data Source CLI prompt message when they are the target of materialized views. (!4661)
- `Added` New Analytics Starter Kit Banner (!4705)
- `Added` Support for role management from the CLI using the subcommand `tb workspace members set-role` (!4626).
- `Added` Shared page UI component (!4649)
- `Added` Allow to hide token values in the output using the `--hide-tokens` flag (!4631)
- `Added` Time Series opened for everybody (!4708)
- `Changed` Manage Pro Tips at pipe level (!4566)
- `Changed` Change query format icon (!4683)
- `Fixed` Update missing buttons in UI (!4657)
- `Fixed` Check null property when deleting a pipeline (!4664)
- `Fixed` Polling in Kafka datasources (!4704)

(2022W38) 2022-09-19 - 2022-09-25

---

- `Added` Fixed node styles in full screen view (!4632)
- `Added` Button UI component (!4552)
- `Fixed` Add collapsed state to Token and Time Series lists. (!4623)
- `Changed` Updated Sidebar and Icons in UI. (!4617)
- `Fixed` Force update of DataSource Event Log when new rows are imported via UI (!4609)
- `Fixed` Data Source deletion when multiple nodes have the same name (!4598)
- `Released` version 1.0.0b190 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4519)

(2022W37) 2022-09-12 - 2022-09-18

---

- `Fixed` Tree view in datasource creation (!4591)
- `Added` Dependencies information returned when executing a Data Source deletion dry run (!4508)
- `Fixed` Disable query formating when editor is disabled (!4577)
- `Added` Time Series public tool (!4274)
- `Added` Datasource clickable tag in Time Series selection (!4538)
- `Added` Improved token management for a pipe. When the pipe is unpublished or deleted we delete its token associated. But only if the token doesn't have more scopes thane the READ:Pipe Scope (!4503)
- `Released` version 1.0.0b184 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4519)
- `Added` `dry_run` parameter to DELETE /v0/datasources/(.+) API endpoint to enable testing the deletion of datasources (!4441)
- `Added` support for `DateTime64` as query parameter (!4514)

(2022W36) 2022-09-05 - 2022-09-11

---

- `Added` Add UTC formatting to Data Source Metrics labels (!4510)
- `Changed` Add more languages to Events API snippet (!4502)
- `Changed` Update DataSource metrics graph when no data available (!4500)
- `Fixed` Focus combobox on click in Safari (!4501)
- `Added` Improved node selection on dataflow (!4477)
- `Fixed` Fixed DateColumn combobox description in Time Series (!4483)
- `Added` Add name and description input fields on create materialized view step 2 (!4413)
- `Added` Show dependencies graph when deleting pipelines (!4465)
- `Added` DataSource metrics graph (!4450)
- `Added` `force` parameter to DELETE /v0/datasources/(.+) API endpoint to enable deletion of datasources being used as a target of materialized views (!4343)
- `Removed` After deprecation a couple of months ago, three APIs are now removed: `/v0/pipes/(.+)/nodes/(.+)/analyze`, `/v0/pipes/(.+)/materialized/(.+)` and `/v0/pipes/(.+)/population/(.+)`, use instead: `/v0/pipes/(.+)/nodes/(.+)/analysis`, `/v0/pipes/(.+)/nodes/(.+)/materialization` and `/v0/pipes/(.+)/nodes/(.+)/population`. In the case of error in the CLI, make sure you are using the latest version.
- `Changed` Added starter kits link to workspace creation modal (!4451)
- `Changed` The Exploration is dead, long live the Time Series (!4468)
- `Changed` Iconography changes (!4470)
- `Fixed` Copy button default fill color (!4452)
- `Fixed` Improve Materialized View creation when there's a GROUP BY query with a plain JOIN (!4489)
- `Released` version 1.0.0b182 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4490)
- `Released` version 1.0.0b183 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4487)

(2022W35) 2022-08-29 - 2022-09-04

---

- `Changed` Added UTC to quarantine observability events. (!4394)
- `Added` Improvements on populate flow UI (!4405)
- `Added` Option to create a new Workspace from a template (!4350)
- `Added` Kafka SASL mechanism selector in connection form. (!4387)
- `Changed` new Data Sources created without specifying an `engine_partition_key` are created without partition if there's no Date column (!4378)
- `Added` enhancements of explorations (!4203)
- `Changed` internal handling of non `latin-1` inputs. (!4411)
- `Changed` more actionable error when a query needs a `-Merge` combinator (!4385)
- `Added` a new endpoint at `/v0/templates` to get all available starter kits
- `Fixed` Checkbox component styles in Safari browser. (!4390)

(2022W34) 2022-08-22 - 2022-08-28

---

- `Added` Improved long textes on sortable multiselect component (!4393)
- `Fixed` Fixed a bug that didn't allow to truncate or populate Data Sources bigger than 50GB.
- `Changed` token label to show the description of the actual scope of the token instead of a generic one (!4242)
- `Added` Possibility of using `join_algorithm=auto` as a feature flag. (!4276)
- `Released` version 1.0.0b175 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4199)
- `Released` version 1.0.0b176 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4356)

(2022W33) 2022-08-15 - 2022-08-21

---

- `Fixed` Some fixes when materializing timeout queries (!4334)
- `Released` version 1.0.0b174 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4326)

(2022W32) 2022-08-08 - 2022-08-14

---

- `Fixed` Show loading state on create materialized view button (!4322)
- `Fixed` Fixed and issue that made errors persistant (!4312)
- `Added` Improved interaction when hiding protips (!4304)
- `Changed` Added way to select destination datasource when creating materialized views (!4301)
- `Changed` Limit available formats on Import when mode is append or replace. (!4267)
- `Added` Added RadioGroup component. (!4246)

(2022W31) 2022-08-01 - 2022-08-07

---

- `Changed` Add consistency on error reporting when saving node (!3639)
- `Changed` Make error on node edit more consistent (!4196)
- `Added` Added TTL edition with custom SQL. (!4167)
- `Changed` Improved visual experience for mv populate (!4254)
- `Fixed` Several issues with the populate section of MV creation modal (!4262)
- `Changed` Added language and formats to import snippets. (!4191)
- `Released` version 1.0.0b170 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4190)
- `Released` version 1.0.0b171 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) P(!4199)
- `Changed` Limited maximum columns to 500. (!3811)

(2022W30) 2022-07-25 - 2022-07-31

---

- `Fixed` Issue with missing dependencies on datasource advanced tab dependency graph (!4212)
- `Changed` Improved quarantine banner behavior by detecting new rows in quarantine. (!4148)
- `Fixed` Fixed a bug when trying to delete an MV on the UI (!4187)
- `Fixed` Added error handling of reserved words to Kafka Preview. (!4157)
- `Added` Added python snippet to local files tab in import modal. (!3944)
- `Added` Show/Hide ProTip button on pipeline node (!3116)
- `Fixed` Removed JSON option from import snippets. (!4113)
- `Fixed` Updated datasource icons. (!4106)
- `Fixed` Added quarantine banner only where it is needed. (!4085)

(2022W29) 2022-07-18 - 2022-07-24

---

- `Added` Explicit populate options on materialized view creation (!3028)
- `Added` Added gzip support from UI (!4101)
- `Added` Documentation for the new parameters supported in the ALTER endpoint: description, kafka_store_raw_value and ttl (!4110)
- `Released` version 1.0.0b168 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!4119)

(2022W28) 2022-07-11 - 2022-07-17

---

- `Added` Set an on/off switch so the user can opt in/out of ingestion error and quarantined data notifications (!3223)
- `Changed` Validate the `populate_condition` before appending a node to avoid creating orphan materialized views (!4002)
- `Changed` Pipes, Data Sources and Node names are now validated against a list of forbidden words. See [docs](https://docs.tinybird.co/api-reference/api-reference.html#forbidden-names) (!4010)
- `Changed` Column aliases cannot match a Pipe, Data Source or Node name. See [docs](https://docs.tinybird.co/api-reference/api-reference.html#forbidden-names) (!4023)

(2022W27) 2022-07-04 - 2022-07-10

---

- `Fixed` a bug that made possible to drop a Data Source being used in a materialized view when there was another node in another pipe with the same name (!3941)
- `Fixed` Selects the first admin token for your User once you arrived to the tokens page (!3975)
- `Fixed` Removed "JOIN THE BETA" CTA from Public API Enpoint pages (!3975)
- `Fixed` The replace bottom in a Data Source takes you to the File option (!3975)
- `Fixed` improve error reporting on template syntax errors (!3970)

(2022W26) 2022-06-27 - 2022-07-03

---

- `Fixed` Refresh dataflow names when changing datasource name. (!3904)
- `Added` Support for commenting in the query editor using cmd + / or ctrl + / (!3908)
- `Added` Support for parquet files when exporting from the UI (!3905)
- `Released` version 1.0.0b159 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3425)
- `Fixed` Exporting Data Source schemas have updated TTL values (!3471)

(2022W25) 2022-06-20 - 2022-06-26

---

- `Added` Detect new datasources that are created via events showing a notification and updating the guided tour. (!3846)
- `Added` Show errors when column names are reserved words preventing the user from creating a new datasource. (!3842)
- `Fixed` Hiding the pipeline options tooltip when options are open (!3371)
- `Fixed` Improved cancellation policy for populate jobs, now they are cancelled faster ([API](<https://docs.tinybird.co/api-reference/jobs-api.html#post--v0-jobs-(.+)-cancel>)) (!3838)
- `Fixed` Automatically cancel population jobs when the related materialized node is deleted. (!3841)
- `Changed` Increased TTL for populate jobs, now it's 72 hours. (!3838)
- `Fixed` Fix service and shared datasource hints on typing a dot. (!3853)
- `Fixed` Improved cancellation policy for populate jobs, now they are cancelled faster ([API](<https://docs.tinybird.co/api-reference/jobs-api.html#post--v0-jobs-(.+)-cancel>)) (!3838)
- `Fixed` Automatically cancel population jobs when the related materialized node is deleted. (!3841)
- `Fixed` Fixes a bug that made a shared materialized Data Source to be dropped when the materialized node was dropped leaving the Data Source broken (!3836)
- `Released` version 1.0.0b155 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3808)

(2022W24) 2022-06-13 - 2022-06-19

---

- `Released` version 1.0.0b149 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3778)
- `Released` version 1.0.0b150 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3757)
- `Released` version 1.0.0b151 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3803)
- `Released` version 1.0.0b154 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3816)
- `Fixed` Return all `engine_*` params when downloading a Data Source datafile (!3807)
- `Fixed` Hide guests admin tokens in the UI, but keep the possibility to refresh them (!3788)
- `Deprecated` Dropped Data Source's `__engine_full` param for APIs . You must use `ENGINE` plus [the rest of the options](https://docs.tinybird.co/api-reference/datasource-api.html#engines-parameters-and-options). (!3802)
- `Added` More intervals in the dashboard. (!3796)
- `Changed` It's now possible to rename Data Sources with dependent Pipes. Pipes using the Data Source are updated as well. (!3822)

(2022W23) 2022-05-06 - 2022-06-12

---

- `Added` Added dependency graph on delete datasource modal
- `Changed` Show data for the whole previous month in usage graph (!3709)
- `Added` Add `populate_condition` param to send an arbitrary SQL condition to be applied when populating a materialized node. See [docs](https://docs.tinybird.co/api-reference/pipe-api.html#id20) (!3706)
- `Released` version 1.0.0b145 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3706)
- `Changed` the scope of the Microsoft Auth as personal accounts was causing issues (!3718)
- `Released` version 1.0.0b147 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3729)
- `Added` Added "Events" tab to the ingestion modal in the UI (!3600)

(2022W22) 2022-05-30 - 2022-06-05

---

- `Changed` Don't quarantine empty trailing NDJSON lines (!3690)
- `Fixed` a bug that allowed to remove or stop sharing Data Sources being used in Materialized Views (!3699)
- `Fixed` pushing a kafka datasource without custom columns or with TTL using the CLI (!3668)

(2022W21) 2022-05-23 - 2022-05-29

---

- `Released` version 1.0.0b142 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3511)
- `Changed` \_ch_cancel_query_async_operation to async (!3451)
- `Added` Added Processed data and Avg. Processed data to Pipe List UI (!3589)
- `Fixed` Fixed Operational logs Editor of the Data Source modal (!3653)
- `Released` version 1.0.0b139 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3658)
- `Added` Added Date32 as type supported in NDJSON schema (!3665)
- `Fixed` Report duplicated column errors when creating a Data Source (!3678)
- `Released` version 1.0.0b144 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3678)

(2022W20) 2022-05-16 - 2022-05-22

---

- `Added` support ndjson as the output format of an endpoint (!3618)
- `Changed` Enhancements on Pipe Stats Usage Metrics graphs (!3547)
- `Changed` Better query validation (#3084) (#3070) (#3084) (#2577) (#3020)
- `Changed` Improved materialized views validation, including performance (!3599) (#3015)
- `Fixed` Added more checks when trying to remove a Data Source that was used by a Materialized View (!3554)
- `Fixed` populateview jobs were not reporting the `queries` progress (!3605)
- `Released` version 1.0.0b135 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3448)
- `Deprecated` skip_table_checks (!3623)

(2022W19) 2022-05-09 - 2022-05-15

---

- `Added` Added Avg. Processed data to the Pipe Stats Usage Metrics graphs (!3552)
- `Released` version 1.0.0b132 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3532)
- `Released` version 1.0.0b131 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3437)
- `Added` Added new tb test command, to allow testing in data projects (!3437).
- `Released` version 1.0.0b130 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` version 1.0.0b129 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3519)
- `Added` Added new metrics about endpoint response times (max,min,mean,median an p90) on `pipe` command `regression-test` (!3515)
- `Added` Autocomplete for tinybird service datasources in code editor (!3234)
- `Released` version 1.0.0b128 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3334)
- `Fixed` Table view sometimes rejecting the column resizing (!3514)
- `Fixed` Prevent triggering the shortcuts when the dashboard is empty and the user is at the first workspace creation modal. (!3514)
- `Fixed` support NDJSON with dots in the properties names (!3517)

(2022W18) 2022-05-02 - 2022-05-08

---

- `Added` Detailed Pipe Stats Usage Metrics graphs (!3300)
  ![Pipe Stats Usage Metrics](https://gitlab.com/tinybird/analytics/uploads/2d2eee97e32e56719c4905d21bc10b25/Captura_de_pantalla_2022-05-06_a_las_12.17.47.png)
- `Added` Billing enabled for all users (!3300)
- `Changed` Forbid appends to Join Data Sources or to data flows with a depending Join Data Source in new data flows. For more details, please read the [documentation about replacing data](https://docs.tinybird.co/api-reference/datasource-api.html?#replacing-data) (!2847)
- `Fixed` `Nullable` types checks when creating a Materialized View (!3460)
- `Fixed` Kafka group id text input back to work as usual (!3479)
- `Released` version 1.0.0b124 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3448)

(2022W17) 2022-04-25 - 2022-05-01

---

- `Added` Help and support menu (!3450)
  <img src="https://gitlab.com/tinybird/analytics/uploads/6ec7baa951557503a9feec9158fe277f/Screenshot_2022-04-28_at_17.13.05.png" style="width: 300px"/>
- `Released` version 1.0.0b123 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3441)
- `Released` version 1.0.0b121 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3422)

(2022W16) 2022-04-18 - 2022-04-24

---

- `Added` User token is visible in the tokens section (!3300)
- `Released` version 1.0.0b118 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3343)
- `Released` version 1.0.0b119 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3300)
- `Fixed` Improve syntax error reporting for the query and pipes APIs
- `Released` version 1.0.0b120 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3293)

(2022W14) 2022-04-04 - 2022-04-10

---

- `Released` version 1.0.0b115 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3170)
- `Released` version 1.0.0b116 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3241)
- `Fixed` Handle `day_diff` errors (!3281)
- `Fixed` Description of shared Data Sources (!3252)
- `Fixed` Dashboard interval filters (!3290)
- `Fixed` Added ellipsis to long pipe and node names in header (!3265)
- `Released` version 1.0.0b117 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3276)

(2022W13) 2022-03-28 - 2022-04-03

---

- `Added` Allow to set the description of the Data source (!3223)
- `Added` Improve application logs to make a better use of loki (!3219)
- `Added` Build plan limits documented (!3263)
- `Changed` BI connector to run operations on cluster (!3184)
- `Changed` Updated limits text in the UI (!3263)
- `Fixed` Fixed problem with web requests on Windows (!2290)
- `Fixed` Handle invalid URL errors when importing CSV (!3236)
- `Released` version 1.0.0b112 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3209)
- `Released` version 1.0.0b113 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3225)

(2022W12) 2022-03-21 - 2022-03-27

---

- `Released` version 1.0.0b109 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3159)
- `Released` version 1.0.0b110 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3071)
- `Changed` From version 1.0.0b110 of the CLI there's a breaking change: if you had a pipe using the name of a materialized node, and the materialized node is not published as an endpoint the pipe won't work. To fix the issue you have to change your pipes so they depend on the Materialized Node target Data Source or `push --force` the pipes and they'll be automatically fixed.
- `Released` version 1.0.0b111 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3061)
- `Released` Build plan rate limits activated (!3204)

(2022W11) 2022-03-14 - 2022-03-20

---

- `Added` Build plan rate limit pre-release. Logging only (!2991)
- `Changed` Improved error response on a partial replace without partitions (!2946)
- `Added` option --skip-incompatible-partition-key when replacing a data source with condition and better error message (!2946)
- `Released` version 1.0.0b107 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2946)
- `Released` version 1.0.0b108 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!3071)
- `Added` Return the Data Source information in the job response (!3098)
- `Added` Return the Data Source information in the job list response (!3098)

(2022W10) 2022-03-07 - 2022-03-13

---

- `Fixed` Usage graphs in other time zones (!3099)

(2022W10) 2022-03-07 - 2022-03-13

---

- `Fixed` Invitation handler to workspace dashboard from invitation email link (!3029)
- `Added` Added option to clear workspace via CLI (!2231)
- `Released` version 1.0.0b104 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2950)

(2022W09) 2022-02-28 - 2022-03-06

---

- `Released` version 1.0.0b100 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2950)
- `Added` Parquet support in API, CLI, and UI (!2650 & !2936)
- `Fixed` NDJSON import through URL for big files does not timeout anymore
- `Fixed` We've detected some workspaces might have orphan materialized views. We've improved how materialized views are deleted so the API will return an error if something went wrong. (!3023)

(2022W08) 2022-02-21 - 2022-02-27

---

- `Released` version 1.0.0b98 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)

(2022W07) 2022-02-14 - 2022-02-20

---

- `Added` Support for `Int128` and `Int256` with some limitations: `v0/analyze` does not detect those types and are not supported in NDJSON format files (!2651)
- `Changed` Added previous month value in usage graph tooltip (!2882)
- `Released` version 1.0.0b97 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2897)

(2022W06) 2022-02-07 - 2022-02-13

---

- `Added` Show Materialized View icons on Pipes/Nodes/Datasources (!2294)
- `Fixed` Closing menus when clicking on top of menu button (!2254)
- `Released` version 1.0.0b93 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2841)
- `Fixed` CLI failing when executing the command `tb workspace ls` with some tokens (!2861)

(2022W05) 2022-01-31 - 2022-02-06

---

- `Added` Allow ingesting/discarding the `value` column in Kafka connected Data Sources (!2778)
- `Added` Allows ingesting discarded columns in NDJSON Data Sources (!2807)
- `Fixed` The `Boolean()` function in SQL templates now always generates `1` or `0`, as ClickHouse [suggests](https://clickhouse.com/docs/en/sql-reference/data-types/boolean/). Our [API docs](https://tinybird.co/docs/query/query-parameters.html#available-data-types-for-dynamic-parameters) have been updated accordingly. (!2816)
- `Changed` Allow parallel JobProcessors execution without interfering with each other (!2772)

(2022W04) 2022-01-24 - 2022-01-30

---

- `Added` UI functionality to rearrange pipe nodes (!2769)
- `Released` version 1.0.0b84 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2755)
- `Added` HFI (v0/events) implicit Data Source creation (!2727)
- `Added` Partial replaces are now executed in cascade. You can find more information about this feature in our documentation: https://docs.tinybird.co/api-reference
- `Added` Set custom plan by default for new workspaces created in dedicated clusters (!2783)
- `Released` version 1.0.0b85 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` version 1.0.0b86 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` version 1.0.0b87 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2764)
- `Released` version 1.0.0b88 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Fixed` Include host in documentation link in API error responses (!2761)
- `Changed` Add validation to report as an error `UNION ALL` inside a materialized view. You need to explicitly use `skip_table_checks=true` to force its usage (!2796)

(2022W03) 2022-01-17 - 2022-01-23

---

- `Added` `KAFKA_STORE_RAW_VALUE` to docs (!2677)
- `Added` Hint to explai you can't share Data between Workspaces in different regions (!2754)
- `Added` Use Tree view to add new columns to NDJSON and Kafka Data sources (!2744)
- `Fixed` Preview all NDJSON content although it doesn't contain a \n at the end (!2730)
- `Fixed` Disallow dropping or stop sharing a shared Data Source if it has dependent materialized nodes in the destination workspace. You should remove or disconnect manually all dependent materialized nodes to be able to drop or stop sharing the Data Source (!2752)
- `Fixed` Provide Kafka errors in the Data Source modal (!2759)
- `Released` version 1.0.0b83 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2740)

(2022W02) 2022-01-10 - 2022-01-16

---

- `Fixed` UI sometimes shows Data Source engine details from other Data Sources (!2700)
- `Fixed` Transformation nodes disallow triggering empty queries (!2700)
- `Fixed` Correct icons for Data Sources in the Data flow graph search bar (!2700)
- `Fixed` Error view on the quarantine modal is sorted by desc (!2700)
- `Released` version 1.0.0b82 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2238)
- `Added` Support CSV files with different column order (!2701)
- `Changed` All API error responses now have a link to its corresponding [documentation](https://docs.tinybird.co) page. (!2706)

(2022W01) 2022-01-03 - 2022-01-09

---

- `Released` version 1.0.0b81 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2646)
- `Added` support for query params for sub pipes used in endpoints (!2575)

(2021W52) 2021-12-27 - 2022-01-02 (Happy new year!)

---

- `Added` Show new columns detected notification to the Dashboard (!2622)
- `Fixed` Improve error parser to detect when missing % in a node (!2574)

(2021W51) 2021-12-20 - 2021-12-26

---

- `Changed` successful create message to display the version when pushing a new resource (!2572)
- `Changed` Hide `value` column from Kafka connected datasources (!2537)
- `Fixed` Preview of CSV imports without trailing blank line (!2578)
- `Fixed` Support jsonpaths with hyphen (e.g. `{aria-hidden: "bla"}`) (!2521)

(2021W50) 2021-12-13 - 2021-12-19

---

- `Changed` Upgraded UI build to Webpack v5 (!2445)
- `Fixed` Error rate of pipes (!2552)
- `Fixed` Problem rendering public endpoint snippet (!2560)

(2021W49) 2021-12-06 - 2021-12-12

---

- `Added` Add resizing to the Tree view (!2505)
- `Added` Shows the Tree view by default (!2528)
- `Changed` Show Kafka meta columns at the end (!2517)
- `Fixed` Fatal crash when adding token (!2523)
- `Fixed` CLI new version not being displayed (!2501)
- `Released` version 1.0.0b75 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2513)
- `Released` version 1.0.0b76 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2432)
- `Added` Support ingesting the whole JSON object as a String in NDJSON files (see [docs](https://docs.tinybird.co/api-reference/datasource-api.html#jsonpaths))

(2021W48) 2021-11-29 - 2021-12-05

---

- `Added` New Tree view in NDJSON/Kafka previews (!2316)
- `Added` Show API Requests as usage metric and the Upgrade banner for DEV plans (!2438)
- `Added` Send params in the body when creating the data source from the UI (!2474)
- `Added` Send an email when a workspace is not available or when the user's role has changed (!2443)
- `Added` Show tooltip on usage graphs detail (!2472)
- `Added` NDJSON export (!2453)
- `Changed` Add '\_deleted' suffix to a workspace's name when it's deleted (!2440)
- `Changed` Improvments on mini usage metrics graphs (!2454)
- `Changed` Better explanation when you can't add columns manually for Kafka Data Sources (!2486)
- `Fixed` Operations Log updated when visits other Data Source (!2447)
- `Fixed` Don't navigate to other page when clicks over Advanced information (!2447)
- `Added` NDJSON ingestion open for everyone. See [API docs](https://docs.tinybird.co/api-reference/datasource-api.html#importing-ndjson) and related [guide](https://www.tinybird.co/guide/how-to-ingest-ndjson-data) (!2487)
- `Added` documentation for kafka_ops_log (!2434)
- `Removed` reference to dynamic tables templating (!2461)
- `Added` Shortcut to `tb auth --interactive` (!2456)
- `Changed` Now that there's quarantine support for Kafka Data Sources, `kafka_store_raw_value` defaults to `false` for new Kafka Data Sources (!2509)
- `Removed` explorations folder as it is not used and cause confusion (!2467)
- `Fixed` Hide usage metrics screen for non admin users (!2457)
- `Fixed` Replacement issue when selecting only some columns of a table (#1964)
- `Fixed` Correct Data Source icon when looking for an specific scope (!2465)
- `Fixed` Fix CORS problem when creating DS via body (!2494)
- `Fixed` TABLE macro to work with shared data sources (!2437)
- `Fixed` PipeNode cache for templated SQLs (!2451)
- `Fixed` Pipes with SQL errors can be duplicated and stored without issues (!2466)
- `Fixed` Pipes' SQL validation improved (!2480)
- `Fixed` Reduced the amount of errors related to concurrently editing a Workspace and adding/removing tokens (!2485)

(2021W47) 2021-11-22 - 2021-11-28

---

- `Added` Detailed Usage Metrics on Settings modal (!2369)
- `Changed` Migrate 'personal' plans to 'dev' (!2381)
- `Changed` Improve handling of table functions. Adds support for 'generateRandom', 'null', 'numbers_mt', 'values', 'zeros', 'zeros_mt' table functions ('numbers' was already supported) (#1881)
- `Fixed` Better handling of database errors and statistics (!2422)
- `Fixed` Reviewed usability problems in the modals after secondary actions (!2340)
- `Fixed` Render Pipes and Data Sources properly in the Recently used block (!2412)

(2021W46) 2021-11-15 - 2021-11-21

---

- `Changed` Display number columns with monospace font (!2397)
- `Changed` Workspace lists in user dropdown sorted by name (!2404)
- `Changed` NDJSON instead of (ND)JSON (!2404)
- `Changed` error_log modal background color changed (!2404)
- `Fixed` Adding support for DateTime64 type (!2380)
- `Fixed` Fixing user workspace dropdown alignment (!2380)
- `Fixed` Proper snippet when NDJSON file is too big (!2380)
- `Fixed` Don't submit the Spotlight form if there are no items (!2379)
- `Fixed` Update graph properly when dependencies change (!2371)
- `Fixed` Allow to refresh the admin token properly (!2395)
- `Removed` `skip_update_validation` in favor of `version_warning` (!2353)

(2021W45) 2021-11-08 - 2021-11-14

---

- `Added` Requesting less Pipes attributes in the first load (!2364)
- `Changed` Improved Materialized Views validation and error messages. (!2318)
- `Changed` Improve UI global error handling (!2178)
- `Fixed` Fix pipe node creation when passing asterisk plus existing columns (#1492)
- `Fixed` Don't rerender Data Source Preview modal when datasources redux collection changes (!2336)
- `Fixed` Don't lose title input focus in Data Source modal when any redux item changes (!2336)
- `Released` version 1.0.0b68 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2318)

(2021W44) 2021-11-01 - 2021-11-07

---

- `Added` Allows discarding columns directly in JSON preview (!2306)
- `Changed` Show region selector in new accounts that have been activated the first time the user logs in (!2282)
- `Changed` Improvements on workspace creation modal for empty dashboards (!2287)
- `Fixed` Snowflake connector was sending `\N` as null value and now it will send `,,` (!2315)
- `Released` version 1.0.0b65 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2021)
- `Released` version 1.0.0b66 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2144)

(2021W43) 2021-10-25 - 2021-10-31

---

- `Changed` Change import failure modal UI to avoid overflow (!2285)

(2021W42) 2021-10-18 - 2021-10-24

---

- `Added` Show workspace creation modal for empty dashboards (!2163)
- `Added` Adds UI version to error reports (!2224)
- `Added` Detect user idle time in the UI (!2227)
- `Added` retry in the CLI client when error 429 (!2228)
- `Added` Multi Region Selector UI (!2244)
- `Added` timeout option when tb push pipe (!2274)
- `Fixed` Fix duplicated rows in ingestion (!2240)
- `Fixed` Name validation at workspace creation modal (!2234)
- `Fixed` Workspace members order by email asc (!2262)
- `Fixed` Authentification error when removing datasources & pipes (!2278)

(2021W41) 2021-10-11 - 2021-10-17

---

- `Fixed` `updated_at` in `v0/datasources` returns the last date some data was saved for Kafka Data Sources.
- `Fixed` Improve CLI message when GCS compose does not have data because SQL query did not return any (!2201)
- `Released` version 1.0.0b60 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2198)
- `Fixed` Fix NDJSON path order in schema (!2210)

(2021W40) 2021-10-04 - 2021-10-10

---

- `Fixed` Send at least one object when importing a JSON file (!2164)
- `Fixed` Preview of the value column of a kafka connected DS shows also non-JSON values (!2140)
- `Fixed` Now connectors doing export with headers by default and can be customize by `-with-headers` (!2171)
- `Removed` URL selection should not provide the "Enable schema guessing" option (!2118)
- `Added` Detect new columns in NDJSON files and Kafka topics (!2082)
- `Added` Select the format of a remote file (!2118)
- `Added` Now the Kafka preview will return a more friendly message when using can not deserialize a message (!2180)
- `Fixed` [Selective replacements](https://www.tinybird.co/guide/replacing-and-deleting-data#replace-data-selectively) now work with shared Data Sources (!2184)
- `Added` Guided Tour component with logic (!2070)
- `Changed` New snippets for new Data Source import (!2118)
- `Changed` Import option input changes if the mode is "append" or "replace" (!2118)
- `Released` version 1.0.0b57 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2169)

(2021W39) 2021-09-27 - 2021-10-03

---

- `Fixed` Listing admin tokens first in tokens page
- `Fixed` Listing workspaces for both user and workspaces tokens
- `Changed` Documentation about `tb auth` and `tb workspace` command scopes
- `Added` workspaces to the [main concepts](https://docs.tinybird.co/core-concepts.html#workspaces) sections of the docs (!2123)
- `Released` version 1.0.0b55 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2021)
- `Changed` "Enable schema guessing" option moved to the preview step (!2104)
- `Added` New `attrs` and `node_attrs` params in the [Pipes API](https://docs.tinybird.co/api-reference/pipe-api.html#get--v0-pipes-?). Use it to get a lighter response object when requesting your list of pipes (!2119).
- `Changed` Support multiple admins per workspace internally (!1659)

(2021W38) 2021-09-20 - 2021-09-26

---

- `Fixed` Display a different button when Kafka connection is already created (!2051)
- `Added` API calls are now tagged with the build timestamp (!2049)
- `Fixed` Advanced Kafka information available again (!2052)
- `Added` Confetti effect when API is created with UI (!2053)
- `Changed` Use Go-like syntax to include JSONPaths on DS schemas (!1995)
- `Fixed` Alignment of the Kafka Data Source creation button fixed (!2051)
- `Added` support `IPv4` and `IPv6` in the BI connector (!2101)
- `Added` Ease Kafka's Schema Registry use (!2051)
- `Changed` Added more details about replace mode in datasource API documentation (!1964)
- `Added` new `v0/analyze` API, not publicly documented yet
- `Released` version 1.0.0b53 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2021)
- `Released` version 1.0.0b54 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2100)

(2021W37) 2021-09-13 - 2021-09-19

---

- `Added` Extract Kafka JSON directly to columns when creating a Data Source (!1978)
- `Added` Set On/Off the NDJSON feature flag via local storage (!2027)
- `Added` Added button on user dropdown to create a workspace for users without own workspaces (!2009)
- `Added` Apply new design to Kafka preview when there is no data (!2039)
- `Fixed` Support Datetime64 when importing CSV (!2005)
- `Fixed` Data flow initialization when Pipes dependencies are not ready (!2012)
- `Fixed` Update data flow diagram when Data Sources or Pipes change (!2031)
- `Changed` Added useOnlyOnUpdate hook. Runs effects when a dependency change its value, not with the initial one. (!1982)
- `Added` Allows to import JSON files from the UI (!2030)
- `Added` Added button on user dropdown to create a workspace for users without own workspaces (!2009)

- `Changed` Support `JSONEachRow` as output format for the [Query API](https://docs.tinybird.co/api-reference/query-api.html#id6)

(2021W36) 2021-09-06 - 2021-09-12

---

- `Added` Display tooltip for long Data Source and Pipe names in the Data Flow (!1945)
- `Released` version 1.0.0b50 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!2016)

(2021W35) 2021-08-30 - 2021-09-05

---

- `Changed` Refactor Data Sources modal. Entry points are file, URL or Kafka now. Under a feature flag. (!1945)
- `Fixed` Fixed query parameter in sample usage box (!1973)
- `Changed` Enabled cmd+k/ctrl+k for opening spotlight (!1974)

(2021W34) 2021-08-23 - 2021-08-29

---

- `Changed` Defer requesting pipeline dependencies (!1941)
- `Changed` Allowing to change column types and name for NDJSON imports (!1923)
- `Released` Tinybird.js v0.6.1. See [release](https://www.npmjs.com/package/tinybird.js/v/0.6.1)

(2021W33) 2021-08-16 - 2021-08-22

---

- `Changed` CSV import add support to DateTime64 (!1884)
- `Changed` Refresh dashboard styling (!1905)
- `Fixed` Apply new styling also to public endpoint pages (!1928)
- `Changed` Use `output_format_json_quote_64bit_integers` param from the UI to preview data from pipes and snapshots (!1870)
- `Changed` Column options changed (when adds new column {CSV} or edit one) (!1910)
- `Released` Tinybird.js v0.6.0. See [release](https://www.npmjs.com/package/tinybird.js/v/0.6.0)

(2021W32) 2021-08-09 - 2021-08-15

---

- `Changed` Upgrade CLI message (!1854)
- `Changed` Add workspace name to browser tab (!1892)
- `Fixed` Fixed styles when the file preview returns an error (!1883)
- `Added` First steps for NDJSON import in the UI (!1883)
- `Changed` Import tabs style changed (!1891)
- `Added` Importing NDJSON from the UI (without configuration) (!1891)

(2021W31) 2021-08-02 - 2021-08-08

---

- `Changed` Enable Kafka to all users (!1851)
- `Changed` Workspace and Shared Data Source emails updated (!1856)
- `Changed` Spotlight modal only shows data sources and pipes, even on Tokens page (!1867)
- `Fixed` Add warning message in the data source preview modal for Null engines (!1866)
- `Released` version 1.0.0b47 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Added` Return Int64 as String throught the API using `output_format_json_quote_64bit_integers=1` in a query (!1869)

(2021W30) 2021-07-26 - 2021-08-01

---

- `Added` Log kafka data sources creation (!1833)
- `Fixed` Connection graph should be rendered although there is an error (!1844)
- `Fixed` Improved kafka exceptions logs in kafka_ops_log (!1843)
- `Released` version 1.0.0b45 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` version 1.0.0b46 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)

(2021W29) 2021-07-19 - 2021-07-25

---

- `Released` version 1.0.0b44 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` Tinybird.js v0.5.8. See [release](https://www.npmjs.com/package/tinybird.js/v/0.5.8)
- `Changed` Reflect if a Data Source is being shared with other workspaces in the Data Flow view (!1820)
- `Fixed` Fixing JS error from JS tracker: "updated_at" is not defined (!1820)
- `Fixed` Block append and replace data from the options list if the Data Source is connected to Kafka (!1820)
- `Added` Providing the share option from the Data Source item list (!1820)
- `Fixed` Importing AccessList styles in the Workspace creation modal (!1820)
- `Changed` Add info about regions in CLI documentation
- `Added` Show Kafka errors in the UI (!1772)
- `Added` Show warning when reaching topic limit and block modal (!1248)
- `Fixed` Kafka Modal design issues (!1826)

(2021W28) 2021-07-12 - 2021-07-18

---

- `Fixed` Fix user invitation failing when the username part of the email contains not supported characters in a Workspace name (numbers, letters and underscores) ([#1341](https://gitlab.com/tinybird/analytics/-/issues/1341)).
- `Fixed` Don't throw a JS error if Data Source engine is not defined (!1791)
- `Fixed` Pipe preview modal working again (!1797)
- `Changed` Don't open autocomplete when the user types Ctrl, CMD, or Alt. Or if the pressed key was the backspace (!1797)
- `Changed` Owned workspaces and workspaces shared with you are differentiated in the User dropdown (!1799)
- `Changed` Improved Kafka Data Source creation (!1781)

(2021W27) 2021-07-05 - 2021-07-11

---

- `Changed` Better error reporting when signed URL expires during ingestion (!1770)
- `Added` Warn the user when a Workspace/Data Source is renamed if it is being shared (!1762)

(2021W26) 2021-06-28 - 2021-07-04

---

- `Added` Allowing to choose the name of your new Workspace (!1718)
- `Fixed` Fixed cli "auth use" message (!1752)

(2021W25) 2021-06-21 - 2021-06-27

---

- `Added` Share Data Sources with other Workspaces (!1651)
- `Changed` Use kafka-confluent library for the preview API ([!1688](https://gitlab.com/tinybird/analytics/-/merge_requests/1688)).
- `Fixed` Tear down properly and drop tables after a replace if necessary (!1699)
- `Fixed` Improved how the CLI handles host argument (!1694)

(2021W24) 2021-06-14 - 2021-06-20

---

- `Changed` Improved the type checking used when importing a new materialized view. It will now give better information about types not being compatible between Pipes and Data Sources, so you can catch errors early ([!1569](https://gitlab.com/tinybird/analytics/-/merge_requests/1599)).
- `Fixed` Updated the documentation.
- `Changed` Kafka graph changed (!1669)
- `Fixed` Fixed sql_and the documentation.

(2021W23) 2021-06-07 - 2021-06-13

---

- `Fixed` Increase GCS read timeouts for CLI connectors (!1642)
- `Changed` Don't let to create a Kafka Data Source if the preview failed (!1600)
  ![Kafka preview failing](https://gitlab.com/tinybird/analytics/uploads/090b6b68f395a6de4138b9684228d21e/Screen_Shot_2021-06-01_at_14.39.24.png)
- `Fixed` Data flow graph showing properly bidirectional Pipes (!1648)
- `Added` not_in filter in sql_and template function in dynamic parameters (!1650)

(2021W22) 2021-05-31 - 2021-06-06

---

- `Added` Display all the dependencies levels when a node is selected or viewed in the Data Source modal (!1602)
  ![Showing all dependencies of top_product_per_day pipe](https://gitlab.com/tinybird/analytics/uploads/edfd517d1054b07b0dc7137a082d4337/Screen_Shot_2021-05-31_at_16.34.47.png)
- `Changed` Data flow graph is rendered with Canvas instead of HTML (!1602)
- `Fixed` Better reporting of HTTP 405 method not allowed errors (!1621)
- `Fixed` Some errors in code snippets in https://docs.tinybird.co (!1623)
- `Fixed` Allow comments in dependent node's last lines (!1612)
- `Released` version 1.0.0b38 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)

(2021W21) 2021-05-24 - 2021-05-30

---

- `Changed` Options UI component used in a different way (!1569)
- `Fixed` Type options (in the preview, add-column,...) dropdown problem fixed (!1569)
- `Added` Import delimiter can be set when create a new import (!1569)
- `Released` version 1.0.0b35 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` version 1.0.0b36 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Fixed` Large file snippet provides the Data Source name when mode is not create (!1573)
- `Changed` Increased the size limit of the SQL used in the application to 8KB and improved the error messages where this limit is exceeded. ([!1559](https://gitlab.com/tinybird/analytics/-/merge_requests/1559))
- `Released` version 1.0.0b37 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)

(2021W20) 2021-05-17 - 2021-05-23

---

- `Released` version 1.0.0b33 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Fixed` `earliest` instead for `earlier` in any Kafka topic (!1557)
- `Changed` Allow to add new columns to any MergeTree engine (!1557)
- `Changed` Data lineage is not Data flow (!1560)
- `Fixed` Render data flow graph again when Data Sources or Pipes have changed (!1560)
- `Added` You can find a Data Source by id in the Browse dialog (& modal) (!1560)
- `Added` You can find a Token by id on its page (& modal) (!1560)
- `Changed` Don't make use of the Kafka credentials for previewing its data (!1565)
- `Released` version 1.0.0b34 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` version 1.0.0b35 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)

(2021W19) 2021-05-10 - 2021-05-16

---

- `Fixed` Fetching correct user workspaces from the beginning (!1512)
- `Added` New import modal for adding Kafka Data Sources, only for Tinybird members (!1508)
- `Fixed` Truncating a datasource with Null engine will not fail ([#1173](https://gitlab.com/tinybird/analytics/-/issues/1173)).
- `Fixed` Tokens now show the correct resource name when using the Token Management UI in other workspaces.

(2021W18) 2021-05-03 - 2021-05-09

---

- `Fixed` Use transactions when activating a user (!1093)
- `Added` Display Data Sources using a Kafka connection (!1491)
- `Fixed` Make test button work when there is a condition applied (!1160)
- `Fixed` Provide columns when querying another pipe (!1502)
- `Fixed` Public datasources should work in pipes (!1164)

(2021W17) 2021-04-26 - 2021-05-02

---

- `Released` version 1.0.0b32 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Fixed` `AggregatingMergeTree` and other engines of the Replacing family now support the `ENGINE_SETTINGS` tag in the .datasource file (!1465)
- `Fixed` Don't focus in the node name if you click close to it (!1473)

(2021W16) 2021-04-19 - 2021-04-25

---

- `Added` Documentation to create materialized views from API Rest (!1410)
- `Added` Possibility to add new columns to your MergeTree Data Sources (!1408)
  ![add-column](https://gitlab.com/tinybird/analytics/uploads/1779861035ce0dc4fc440c9c73e0aaff/Screen_Shot_2021-04-08_at_10.18.14.png)

(2021W15) 2021-04-12 - 2021-04-18

---

- `Fixed` Autocomplete provide the columns of the entities found in the SQL properly (!1431)
- `Changed` version 1.0.0b31 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/

(2021W14) 2021-04-05 - 2021-04-11

---

- `Fixed` Endpoint documentation now returns correctly all its parameters ([!1402](https://gitlab.com/tinybird/analytics/-/merge_requests/1402))
- `Released` version 1.0.0b30 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Fixed` Return error if present when creating a ReplicatedAggregatingMergeTree on cluster (!1409)
- `Fixed` CLI/API complains about wrong options when creating a data source (!1366)
- `Fixed` Update data source stats when replacing a data source (!1389)
- `Fixed` Update data source stats after a populate finishes successfully (!1389)
- `Fixed` Improve transactional management on User modifications ([!1394](https://gitlab.com/tinybird/analytics/-/merge_requests/1394))
- `Changed` Improve job processor shutdown (!1406)
- `Fixed` Fix replacing tables with Join engine (!1415)
- `Fixed` Default value is not displayed correctly in Endpoint documentation if value was 0 ([!1418](https://gitlab.com/tinybird/analytics/-/merge_requests/1418))

(2021W13) 2021-03-29 – 2021-04-04

---

- `Added` New service Data Source `endpoint_errors` available for reviewing any error (!1384)
  ![endpoint_errors](https://gitlab.com/tinybird/analytics/uploads/ca3f54b34b520d97b178b25246c693e1/Screen_Shot_2021-03-31_at_10.36.38.png)
- `Fixed` Error when there are problems while fetching data during an import (!1377)
- `Changed` Signup uppercase in docs header (!1395)
- `Changed` Data lineage graph uses the scroll for panning (!1395)
- `Added` Graph search results provide an icon for better discovery (!1395)
- `Fixed` Fixed problem with engine type info z-index (!1395)
- `Changed` All current ClickHouse functions are explained in the editor autocomplete (!1395)
  ![autocomplete-all](https://gitlab.com/tinybird/editor-languages/uploads/23139a8e330b95ca1eb9d37f9cf4820a/autocompleteall.gif)

(2021W12) 2021-03-22 – 2021-03-28

---

- `Released` version 1.0.0b26 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` version 1.0.0b27 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` version 1.0.0b28 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Added` New rows in quarantine table now have the import_id, so you can track which import tried to insert it.
- `Changed` If the node is materializing, take the data from the Data Source instead of the query itself (!1378)
- `Fixed` Long node names won't break the Pipeline header when scrolling (!1379)
- `Added` Express clearly when a token is only visible to you (!1379)
- `Changed` Check current job status if the cancellation failed (!1379)
- `Added` SQL case statement correctly highlighted (!1379)
- `Changed` Using cursor grab within the Graph (!1379)
- `Fixed` Disabled shift + drag behaviour within the Graph (!1379)
- `Added` Added endpoint_errors view so user can get info about why they have errors in their endpoints (!1384)
- `Fixed` Graph search will center the graph into the selected node (!1385)
- `Fixed` Node selection improved (!1385)

(2021W11) 2021-03-15 – 2021-03-21

---

- `Added` Dependencies graph being used under Data Source advanced information (!1350)
- `Fixed` Using reserved words as variables (!1330)
- `Added` Check dist data source columns: name of columns, order, data types of the data source must much the name of columns, order, data types in the pipe that materializes (!1312)
- `Added` Check aggregate functions are cast correctly (!1312)
- `Added` Check aggregate functions are using an aggregating engine (!1312)
- `Fixed` If a datasource used in a materialized view is renamed, the datasource can be deleted (!1312)
- `Added` Check order by and group by column match: columns in the ORDER BY should match columns in the GROUP BY in aggregating engines (!1312)
- `Added` Flag `skip_table_check` to skip materialized view and table checks (!1312)
- `Released` version 1.0.0b25 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Added` Added possibility to cancel a job in `waiting` status. Populates can be cancelled in `working` status too.

(2021W10) 2021-03-08 – 2021-03-14

---

- `Fixed` Snapshots table look and feel fixed (!1332)
- `Added` New Browse Data Sources and Pipes modals (!1301)
  [![](https://gitlab.com/tinybird/analytics/uploads/5417593a206c376cfdb1dd20919b2365/Screen_Shot_2021-03-08_at_23.41.38.png)](https://gitlab.com/tinybird/analytics/uploads/173a6ca798ff040bfaf4758ee128e78e/browse-entities.mp4 'Browse entities')
- `Fixed` Options dropdown with correct z-index (!1335)
- `Fixed` Better table bottom padding for BrowseEntities component (!1341)
- `Fixed` UsedBy headers were not properly positioned when scrolling (!1341)
- `Added` Added an arrow icon for Data Sources list link (!1341)
- `Changed` Making use of editor-languages repository (!1202)
- `Added` Check which Pipes are writing to a Data Source in the advanced section (!1343)
- `Released` version 1.0.0b24 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)

(2021W09) 2021-03-01 – 2021-03-07

---

- `Released` version 1.0.0b23 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Fixed` Edit code snippet buttons with same height (!1317)
- `Fixed` Number of nodes using the same parameter (!1317)
- `Added` New parameter snippet, how to paginate (!1317)
- `Fixed` Updating workspaces properly when there is change in the current one (!1319)
- `Changed` If a job didn't finish, and max pollings has been reached, the job will not be marked as errored (!1322)
- `Fixed` Improving the automatic encoding guessing for CSVs (!1315)

(2021W08) 2021-02-22 – 2021-02-28

---

- `Released` version 1.0.0b22 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Added` support `engine_settings` to set additional settings (such as `index_granularity` when creating a new Data Source). See [ClickHouse documentation](https://clickhouse.tech/docs/en/engines/table-engines/mergetree-family/mergetree/#mergetree-query-clauses). (!1238)
- `Fixed` support for `engine_ttl` when downloading the Data Source schema. (!1238)
- `Released` version 1.0.0b21 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` version 1.0.0b20 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Released` version 1.0.0b19 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Fixed` Curl snippets for datasources (!1292)
- `Fixed` Syntax SQL errors parsing (!1297)

(2021W07) 2021-02-15 – 2021-02-21

---

- `Fixed` Allow comments in node's last lines (!1261)
- `Fixed` Create an individual admin token for users in a workspace (!1259)
- `Fixed` CLI sql command (!1264)
- `Fixed` SQL errors with missing parentheses improved (!1266)
- `Fixed` Validate sorting key for ReplacingMergeTree, AggregatingMergeTree and CollapsingMergeTree engines (!1262)
- `Fixed` Give more details on populate error (!1269)

(2021W06) 2021-02-08 – 2021-02-14

---

- `Changed` New node look and feel (!1141)
  [![](https://gitlab.com/tinybird/analytics/uploads/939fd438d62003e3b94d2556d84ef5b1/Screenshot_2021-02-07_at_00.14.48.png)](https://gitlab.com/tinybird/analytics/uploads/d38dd9530b1de439c425fedbe23654ce/node-ui.mp4 'New Node UI')
- `Fixed` Revert changing between workspaces without reloading the whole application (!1242)
- `Fixed` Redirect correctly to the user's dashboard (!1242)
- `Changed` Added 'go back to dashboard' button from 404 page if user is loged in (!1242)
- `Fixed` Results paginator not displayed for Data Source opts log (!1250)
- `Changed` Front-end source files moved to its proper folder called `assets` (!1249)
- `Released` version 1.0.0b16 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Fixed` Searching types in the import preview process will not fail with non-word characters (!1255)
- `Released` version 1.0.0b17 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)
- `Added` Add new healthcheck entrypoint that checks Redis and Clickhouse connections (!1211)

(2021W05) 2021-02-01 – 2021-02-07

---

- `Added` Add/delete Workspace members (!1216|!1204)
- `Added` CLI: Added feedback about appended rows, total rows and errors to append command output (!1205)
- `Added` wait option to push command for waiting for the populate job to finish.
- `Fixed` appending large files (more than 2GB). Now, files are uploaded using multipart and without loading the whole file in memory.
- `Added` query explain info when making endpoint requests with _debug=query_ parameter.
- `Fixed` Displayed a warning when job has reached max polling times (!1234)
- `Added` Change between workspaces without reloading the whole application (!1220)
- `Added` Support for CSV and JSON output to "sql" CLI command (!1213)
- `Released` version 1.0.0b15 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/)

(2021W04) 2021-01-25 – 2021-01-31

---

- `Added` Log trace in Span for account activation/deactivation
- `Added` Create/edit/delete Workspaces (!1179|!1183)
- `Fixed` Workspaces login (!1196)
- `Performance` Improved performance on CSV files with space as separator
- `Added` Workspaces API endpoints (!1179)

(2021W03) 2021-01-18 – 2021-01-24

---

- `Added` Internal Workspaces (!1067)
- `Fixed` Docs search fixed (!1188)
- `Added` GitHub login available (!1188)

(2021W02) 2021-01-11 – 2021-01-17

---

- `Fixed` Wait for query to finish checking the query log on populate jobs (!1171)
- `Fixed` Catch StopIteration error when guessing columns reading a CSV (!1176)
- `Fixed` Column guessing in files with many blank lines (!1176)

(2021W01) 2021-01-04 – 2021-01-10

---

- `Fixed` Code snippets in documentation (!1172)
- `Fixed` [delete_condition](<https://docs.tinybird.co/api-reference/datasource-api.html#post--v0-datasources-(.+)-delete>) works on Data Sources created on cluster (!1174)

(2020W52) 2020-12-21 – 2020-12-27

---

- `Fixed` Remove temp tables on tear down (!1033)
- `Added` Last Jobs information in the Dashboard (!1157)
- `Fixed` Support TAB in dialect_delimiter param (!1164)
- `Added` Documentation for dialect_escapechar param (!1164)
- `Fixed` Parse null dates when appending data from csv (!1169)

(2020W51) 2020-12-14 – 2020-12-20

---

- `Added` Pipes and Data Sources will manage its loading state (!1156)
- `Fixed` Parameters properly computed after query changes (!1116)
- ``Fixed` Do not return parameters present nodes that aren't being used (!1054)
- `Changed` How to manage parameters in the UI has been changed (!1116)
  ![node-publish-changes](https://gitlab.com/tinybird/analytics/uploads/b8c9ddae4ad15e7044c9b5c29539630c/Screenshot_2020-12-04_at_14.58.52.png)
- `Fixed` Display correctly the number of rows deleted by condition (!1161)

(2020W50) 2020-12-07 – 2020-12-13

---

- `Fixed` Column names are available in the autocomplete for a recently renamed node (!1153)
- `Fixed` Query snippets uses parameter token if it is present (!1152)
- `Released` version 1.0.0b14 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!1145)
- `Added` The Data Sources Operations log will reflect the changes of Data Sources created and deleted via materialized nodes. (!1144)
- `Changed` Materialized nodes support DATASOURCE and ENGINE options. When using a DATASOURCE option, it will push the data to that Data Source if it exists. When using the ENGINE options, it will create a new Data Source with that engine and its parameters. This makes easier to prototype and test new materialized nodes as you don't have to do it in two steps. When deleting a materialized node, if the node created a Data Source via the ENGINE options, it will delete the Data Source if there are no other pipes using it. (!1144)
- `Changed` The .datasource and .pipe files include all the ENGINE metadata as defined in the API. This includes extra parameters that were missing for engines some engine, e.g. Join (!1144)
- `Deprecated` Data Source's `ENGINE_FULL` option will stop working after 2021-01-31. You must use `ENGINE` plus [the rest of the options](https://docs.tinybird.co/api-reference/datasource-api.html#engines-parameters-and-options). For upgrading existing projects to this new syntax, you can use `tb pull` to update your project files. (!1144)
- `Deprecated` Data Sources's `PARTITION_KEY`, `SORTING_KEY`, `PRIMARY_KEY`, `SAMPLING_KEY`, `TTL` parameters will stop working after 2021-01-31, you must use the same parameters prefixed by `ENGINE_`. For upgrading existing projects to this new syntax, you can use `tb pull` to update your project files. (!1144)
- `Released` version 1.0.0b13 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!1145)
- `Added` API endpoint to list user's Jobs (!1145)
- `Changed` API endpoints return pretty-printed JSON (!1145)
- `Fixed` White line doesn't appear anymore in the code snippets at public endpoint page (!1150)
- `Fixed` Rendering all user names properly (!1148)

(2020W49) 2020-11-30 – 2020-12-06

---

- `Security` Fix `used_by` to only list pipes accessible by the current token (!1147)
- `Changed` CORS headers are now included in all preflight requests (!1146)
- `Added` Data Source engine information in the UI (!1077)
- `Added` Pipe options under its name in the Pipe header (!1133)
- `Added` Create pipe possibility under Data Source options (!1133)

(2020W48) 2020-11-23 – 2020-11-29

---

- `Fixed` Bug when ingesting CSVs with columns with values like this `[ W ]`. It was trying to parse it as an array, crashing the ingestion. (!1134)

(2020W46) 2020-11-09 – 2020-11-15

---

- `Added` Instructions to use the CLI in a Docker image (!1107)

(2020W45) 2020-11-02 – 2020-11-08

---

- `Changed` New text when a token is refreshed (!1085)
- `Fixed` Changed the button loader when a token is renamed (!1085)
- `Fixed` Several bug-fixing for the docs (!1085)
- `Fixed` Wrong indentation for the selected Pipe on the sidebar (!1085)
- `Changed` Moved and renamed the download .datasource/.pipe options (!1085)
- `Added` Data Source and Pipe definitions can be downloaded from the UI (!1066)

(2020W44) 2020-10-26 – 2020-11-01

---

- `Added` Enforcing rate limits for `POST /v0/datasources` requests (!957)
- `Added` Rate limiting framework (!957)
- `Changed` Docs revamp (!1075)
- `Fixed` User was redirected to other token when it was refreshed (!1066)
- `Fixed` Parse data source datafiles for schemas with nullable types (!1706)

(2020W43) 2020-10-19 – 2020-10-25

---

- `Changed` Easy way to publish and unpublish a Pipe (!1061)
  ![node-publish-changes](https://gitlab.com/tinybird/analytics/uploads/0ac507af857dc941134fce064e80a136/node-publish-changes.png)
- `Removed` Not offering "Add node" under current Pipe (!1061)
- `Added` New section in the docs for [CLI common use cases](https://docs.tinybird.co/cli/common-use-cases.html) (!1056)
- `Changed` Removed output node element and moved to the Pipe options (!1047)
- `Fixed` Remove token scopes when updating a token sending no scope (!1062)

(2020W42) 2020-10-12 – 2020-10-18

---

- `Fixed` Pressing Tab when any selected SQL removes it (!1053)
- `Changed` Possibility to create a new Pipe empty (!1025)
- `Removed` We have removed the number of nodes in the Pipe information (!1025)

(2020W41) 2020-10-05 – 2020-10-11

---

- `Added` New way to resize the sidebar when it is not collapsed (!1019)
- `Changed` Output node selector for allowing display the whole node name when selected (!1019)
- `Changed` How to display the Pipe or the Data Source name when it is bigger than the space in the Spotlight modal (!1019)
- `Changed` Automatically load the pipe `token` in the OpenAPI page so you can test endpoints right away (!1002)
- `Changed` CLI [docs](https://docs.tinybird.co/cli.html). Added more cases, minor fixes and a ToC (!1016)
- `Changed` Keep data on data source replace if it fails (!1023)
- `Changed` Allow first parameter without default in `columns` template function (!1030)
- `Released` version 1.0.0b11 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!1020)

(2020W40) 2020-09-28 – 2020-10-04

---

- `Changed` Automatically load the pipe `token` in the OpenAPI page so you can test endpoints right away (!1002)
- `Fixed` populating from all sources after replacing a dependent view (!975)
- `Fixed` populate view from materialized node (!1010)
- `Fixed` problem with array params interaction (!1006)
- `Fixed` publish message from node options (!995)
- `Fixed` Parse error functions correctly in templates (!990)
- `Fixed` Getting only token resources in openapi endpoint (!990)
- `Fixed` Print custom error in the endpoint page instead of a generic error (!990)
- `Fixed` Use endpoint token when requesting open api data from the endpoint page (!990)
- `Fixed` 'q' parameter in openapi schema (!1000)
- `Fixed` display correctly array parameters in endpoint pages (!1000)
- `Fixed` Request endpoint params only when there's a read pipe token (!1003)
- `Fixed` Sorting params error when param name is None (!1003)
- `Fixed` Fix operations on vars (!1011)

(2020W39) 2020-09-21 – 2020-09-27

---

- `Added` more ClickHouse keywords for better syntax highlighting (!987)
- `Added` support for Microsoft login (!946)
- `Added` Improved performance for templated queries (!964)
- `Added` Do not allow Data Source deletion when it is involved in a materialized node (!958)
- `Changed` how to notify the user when a Pipe is published (!978)
- `Changed` the way to replace the SQL input when a suggestion is selected (!967)
- `Changed` Updated [available formats](https://docs.tinybird.co/api-reference/query-api.html#id6) in the Query API documentation (!971)
- `Changed` Better error messages when renaming nodes, pipes or datasources (!973)
- `Fixed` http snippet escaping the default query parameters (!988)
- `Fixed` scroll problem in output node dropdown (!985)
- `Fixed` Pipes API performance degradation (!962)
- `Fixed` when token filter is too long (!965)
- `Fixed` Validate and [document](https://docs.tinybird.co/api-reference/query-api.html#id5) the `pipeline` param in Query API (!972)
- `Fixed` Update datasource row count after a truncate operation (!976)
- `Fixed` type_guessing argument fixed and documented (!984)
- `Released` version 1.0.0b10 of the CLI. See [changelog](https://pypi.org/project/tinybird-cli/) (!966)

(2020W38) 2020-09-14 – 2020-09-20

---

- `Fixed` opening editor in full screen (!955)
- `Fixed` code selection when node is materialized (!955)
- `Changed` displaying query time in seconds when it is bigger than 999ms (!955)
- `Fixed` guessing when import mode is replace or append (!948)
  ![Guessing disabled for replace or append mode](https://gitlab.com/tinybird/analytics/uploads/d7e80470a2858b7b063f86f9f2db3576/948.png)
- `Fixed` error not being shown when pushing data to a Data Source with broken dependent views (!950)
- `Fixed` problem closing a Data Source modal in a new tab (!943)
- `Fixed` parsing schemas in datasource files when using aggregate function (!956)
- `Added` new custom_error on pipe templates (!961)

(2020W37) 2020-09-07 – 2020-09-13

---

- `Added` parameters in the code snippets (!927)
- `Added` edition for HTTP code snippet (!927)
  ![Code snippets changes](https://gitlab.com/tinybird/analytics/uploads/69bebcb0ec0189d577699f0643404068/Screenshot_2020-09-08_at_14.42.46.png)
- `Changed` Now, the `column` template function default value is an optional argument
- `Added` a way to remove all recently items (!890)
- `Fixed` problem displaying OpenApi button in private endpoing page (!933)
- `Fixed` Data Source schema parsing support for extra whitespace between parts (!928)
- `Fixed` bug not allowing to rename a node from its options (!920)
- `Added` the possibility to collapse the sidebar
  [![](https://gitlab.com/tinybird/analytics/uploads/a06a81720098684fcdd6235ad7fa16c2/Screenshot_2020-09-03_at_13.15.26.png)](https://gitlab.com/tinybird/analytics/uploads/acfbabbab442c97854449e31f805b8df/sidebar-collapse.mp4 'Collapse sidebar') (!864)
- `Fixed` adding repetitive errors (!929)
- `Changed` do not create a READ token when creating a pipe (!937)
- `Changed` add a READ token if there isn't any unique READ token for a pipe when publishing an endpoint from the UI (!937)
- `Fixed` creating a snapshot for a pipe without READ token (!937)
- `Fixed` CLI error when pushing fixtures (!938)

(2020W36) 2020-08-31 – 2020-09-06

---

- `Fixed` Creating a Data Source from a schema when it contains CODEC and DEFAULT|MATERIALIZED|ALIAS (!918)
- `Changed` Refresh dashboard data in different time intervals instead of all at once (!912)
  ![](https://gitlab.com/tinybird/analytics/uploads/fb74145f44f56529de24f53f8c8827f4/loading_requests.gif)
- `Fixed` [API documentation](<https://docs.tinybird.co/api-reference/datasource-api.html#post--v0-datasources-(.+)-truncate>) related to Data Source truncation (!913)
- `Added` truncate option under quarantine Data Sources (!913)
  ![](https://gitlab.com/tinybird/analytics/uploads/1024c428dbfa79aa1b234c093a21b487/Screenshot_2020-09-01_at_17.33.12.png)
- `Fixed` don't propagate key event to the Spotlight modal (!914)
- `Fixed` auto-complete keyboard navigation problem for parameters (!915)
  [![](https://gitlab.com/tinybird/analytics/uploads/4ff6a7d74a4b4416459c1004f92a44ec/Screenshot_2020-09-03_at_13.15.59.png)](https://gitlab.com/tinybird/analytics/uploads/5d4f15ec9a3efcda6c4c1108f6cf676e/bug-show-hint.mp4 'Bug')

- `Changed` do not display `format` and `q` in the parameter list (!910)
  ![](https://gitlab.com/tinybird/analytics/uploads/b6887ecf487757d5e067e333a7466acd/Screenshot_from_2020-08-28_12-17-18.png)
- `Security` do not allow using templates in `q` parameter when getting data from an endpoint pipe (!910)

(2020W35) 2020-08-24 – 2020-08-30

---

- `Added` CLI support for python 3.7 and 3.8 (!902)
- `Released` version 1.0.0b7 of the CLI. See [release notes](https://pypi.org/project/tinybird-cli/1.0.0b7/) for more info. (!905)
- `Fixed` a bug in the header detection of CSV files. Now the original header of the source CSV file is cached, so whenever new data is appended the importer discards any row which is exactly the same as the source header, no matter if it's at the beginning of the file or at any other position. (!837)
- `Fixed` Save pipe descriptions on push and pulls [CLI] (!904)
- `Fixed` a bug when pushing a datasource that included a `DEFAULT CAST(NULL, 'Nullable(String)')` (!908)
- `Released` version 1.0.0b6 of the CLI. See [release notes](https://pypi.org/project/tinybird-cli/1.0.0b6/) for more info.

- `Released` version 1.0.0b5 of the CLI. See [release notes](https://pypi.org/project/tinybird-cli/1.0.0b5/) for more info. (!905)

(2020W34) 2020-08-17 – 2020-08-23

---

- `Fixed` Do not add a variable from template if it is not casted or there is no data (!901)
- `Fixed` Share link only from the endpoint page (!900)
- `Fixed` Adjust label spacing in endpoint page (!900)
- `Fixed` Avoid sorting endpoint parameters alphabetically (!901)
- `Fixed` Replace with condition for replicated Join Data Sources (!898)
- `Fixed` Limit to a max number of rows the sample response in the endpoint page (!893)
- `Fixed` Fix stats query output in endpoint log view (!896)
- `Added` more information in stats endopoint log view (!896)

(2020W33) 2020-08-10 – 2020-08-16

---

- `Fixed` a bug in [delete with condition](<https://docs.tinybird.co/api-reference/datasource-api.html#post--v0-datasources-(.+)-delete>) when the `delete_condition` contains a single quoted string. (!881)
- `Added` Publish CHANGELOG page at [https://ui.tinybird.co/changelog](https://ui.tinybird.co/changelog)
- `Added` Add option to remove all recently used items from sidebar (!644)
- `Fixed` When user auto-completes in the editor, only add one cursor in first occurence after the completion text. (!537)
- `Released` version 1.0.0b4 of the CLI. See [release notes](https://pypi.org/project/tinybird-cli/1.0.0b4/) for more info. (!865)
- `Added` Python snippet in the API endpoint page and reorganized the rest of the snippets for more clarity. (!863)
- `Added` support for delete data from a datasource given a condition. See [API docs](<https://docs.tinybird.co/api-reference/datasource-api.html#post--v0-datasources-(.+)-delete>) for more info. (!836)
- `Added` a new parameter `type_guessing` in the Datasources API. When set to `false` all columns are created as `String` otherwise it tries to guess the column types based on the CSV contents. See [API docs](https://docs.tinybird.co/api-reference/datasource-api.html#id21) for more info. (!849)
  ![](https://gitlab.com/tinybird/analytics/uploads/91de67f1be3bf392f8ff5dce5af85f71/Screenshot_2020-08-06_at_18.13.46.png)

- `Fixed` a bug in the ingestion process. It now supports double quoted columns which contains new line breaks, this is a quite common case when ingesting data scraped from websites. (!851)
- `Fixed` a bug in the OpenAPI spec of API endpoints parameters. It now supports Arrays and deduplicate parameters. (!842)
- `Released` version 1.0.0b3 of the CLI. See [release notes](https://pypi.org/project/tinybird-cli/1.0.0b3/) for more info. (!867)
- `Added` support for node previews. When any user clicks over a node entity within a SQL, we scroll to the desired node. Instead of that, we show a modal with the node data. (!856)
  ![](https://gitlab.com/tinybird/analytics/uploads/be467033efec4fc8b931831189f62f6d/Screenshot_2020-08-07_at_16.05.55.png)

- `Fixed` a bug when populating materialized JOIN tables with more than one million records. (!860)

(2020W32) 2020-08-03 – 2020-08-09

---

- `Fixed` some errors in the API docs. (!828)
- `Changed` the way autocomplete hints are sorted in the query editor. It now sorts by length first and then alphabetically. (!848)
  ![](https://gitlab.com/tinybird/analytics/uploads/a53a5eb9756e9df3b8e318c4fbbe6ff5/mm.gif)
