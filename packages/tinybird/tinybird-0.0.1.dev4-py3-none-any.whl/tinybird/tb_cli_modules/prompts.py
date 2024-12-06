create_project_prompt = """
You are a Tinybird expert. You will be given a prompt describing a data project and you will generate all the associated datasources and pipes.
<datasource>
    name: The name of the datasource.
    content: The content of the datasource datafile in the following format:

    ```
DESCRIPTION >
    Some meaningful description of the datasource

SCHEMA >
    `<column_name_1>` <clickhouse_tinybird_compatible_data_type> `json:$.<column_name_1>`,
    `<column_name_2>` <clickhouse_tinybird_compatible_data_type> `json:$.<column_name_2>`,
    ...
    `<column_name_n>` <clickhouse_tinybird_compatible_data_type> `json:$.<column_name_n>`

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "<partition_key>"
ENGINE_SORTING_KEY "<sorting_key_1, sorting_key_2, ...>"
    ```
</datasource>
<pipe>
    name: The name of the pipe.
    content: The content of the pipe datafile in the following format:
    ```
DESCRIPTION >
    Some meaningful description of the pipe

NODE node_1
SQL >
    <sql_query_using_clickhouse_syntax_and_tinybird_templating_syntax>

...

NODE node_n
SQL >
    <sql_query_using_clickhouse_syntax_and_tinybird_templating_syntax>
    ```
</pipe>
<instructions>
    - The datasource name must be unique.
    - The pipe name must be unique.
    - The datasource will be the landing table for the data.
    - Create multiple pipes to show different use cases over the same datasource.
    - The SQL query must be a valid ClickHouse SQL query that mixes ClickHouse syntax and Tinybird templating syntax.
    - If you need to use dynamic parameters you must start the whole sql query ALWAYS with "%" symbol on top. e.g: SQL >\n    %\n SELECT * FROM <table> WHERE <condition> LIMIT 10
    - The Parameter functions like this one {{String(<my_param_name>,<default_value>)}} can be one of the following: String, DateTime, Date, Float32, Float64, Int, Integer, UInt8, UInt16, UInt32, UInt64, UInt128, UInt256, Int8, Int16, Int32, Int64, Int128, Int256
    - Parameter names must be different from column names. Pass always the param name and a default value to the function.
    - Nodes can't have the same exact name as the Pipe they belong to.
</instructions>
"""

sample_data_prompt = """Your role is to generate sample data for a given data source. A data source is a table in Tinybird. You will be given a schema for the data source, and you will need to generate a set of rows that fit that schema.

The schema will be provided to you at the end of this prompt in the following format:

```
SCHEMA >
    `span_id` String `json:$.span_id`,
    `operation_id` String `json:$.operation_name`,
    `duration` Nullable(Float32) `json:$.duration`,
```

In the example above, `span_id` are column names, String and Float32 are column types, and `json:$.duration` is a JSON path expression that points to the duration value in the JSON data. Use this information to generate valid data.

You will generate {row_count} rows of data in JSON format, newlines separated. Your reponse will only contain the {row_count} rows of data, without any other text. Do not format the data in any way, and do not place it inside any markers for a code block of any kind. Most importantly, do not use backticks on the first or last line or anywhere else in the response. This is extremely important, ensure that your response doesn't include any backticks.

Remember that for a JSON to be valid, there can't be a trailing comma after the last value in an object.

Make sure to include all columns in the schema, and use valid JSON. You may leave some columns empty only if the column type allows it (e.g. Nullable(String)). Use realistic values for the data, and make sure to include a variety of values in each column.

For columns that represent timestamps, use values that are close to the current date and time. The current date and time is {current_datetime}"""

sample_data_with_errors_prompt = """Your role is to generate incorrect sample data for a given data source. A data source is a table in Tinybird. You will be given a schema for the data source, and you will need to generate a set of rows that mostly fit that schema, but with some errors.

The schema will be provided to you at the end of this prompt in the following format:

```
SCHEMA >
    `span_id` String `json:$.span_id`,
    `operation_id` String `json:$.operation_name`,
    `duration` Nullable(Float32) `json:$.duration`,
```

In the example above, `span_id` are column names, String and Float32 are column types, and `json:$.duration` is a JSON path expression that points to the duration value in the JSON data. Use this information to generate valid data.

You will generate {row_count} rows of data in JSON format, newlines separated. Your reponse will be a single string containing all {row_count} rows, without any other text. Make sure to include all columns in the schema, and use valid JSON. Use realistic values for the data, and make sure to include a variety of values in each column. In every set of {row_count} rows, there should be at least one row that has an error. The error could be in any column, and it could be a type error (e.g. a string where a number is expected), or it could be an error in the structure of the JSON (e.g. a value in the wrong place in the document).

For columns that represent timestamps, use values that are close to the current date and time. The current date and time is {current_datetime}"""


sample_data_sql_prompt = """
Given the schema for a Tinybird datasource, return a can you create a clickhouse sql query to generate some random data that matches that schema.

Response format MUST be just a valid clickhouse sql query.

# Example input:

SCHEMA >
    experience_gained Int16 `json:$.experience_gained`,
    level Int16 `json:$.level`,
    monster_kills Int16 `json:$.monster_kills`,
    player_id String `json:$.player_id`,
    pvp_kills Int16 `json:$.pvp_kills`,
    quest_completions Int16 `json:$.quest_completions`,
    timestamp DateTime `json:$.timestamp`


# Example output:

SELECT
    rand() % 1000 AS experience_gained, -- Random experience gained between 0 and 999
    1 + rand() % 100 AS level,          -- Random level between 1 and 100
    rand() % 500 AS monster_kills,      -- Random monster kills between 0 and 499
    concat('player_', toString(rand() % 10000)) AS player_id, -- Random player IDs like "player_1234"
    rand() % 50 AS pvp_kills,           -- Random PvP kills between 0 and 49
    rand() % 200 AS quest_completions,  -- Random quest completions between 0 and 199
    now() - rand() % 86400 AS timestamp -- Random timestamp within the last day
FROM numbers({row_count})

# Instructions:

- The query MUST return a random sample of data that matches the schema.
- The query MUST return a valid clickhouse sql query.
- The query MUST return a sample of {row_count} rows.
- The query MUST be valid for clickhouse and Tinybird.
- Return JUST the sql query, without any other text or symbols. 
- Do NOT include ```clickhouse or ```sql or any other wrapping text.
- Do NOT use any of these functions: elementAt
- Do NOT add a semicolon at the end of the query
- Do NOT add any FORMAT at the end of the query, because it will be added later by Tinybird.

"""
