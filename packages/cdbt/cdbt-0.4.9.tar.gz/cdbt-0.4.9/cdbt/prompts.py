class Prompts:

    @property
    def dbt_docs_gte_l3_prompt(self):
        return """
You will help build DBT documentation YML files for a given SQL query. Sometimes you will be asked to generate a description from scratch, other times you will be asked to fill in missing columns that exist in the model, but not in the documentation.

Primary DBT Guidelines:

    3. Include a config block for each model:
        a. Set `materialized` to `table`
        b. Do not include a `sort` key.
    4. For long descriptions, use the following format so the lines are not too long:
        ```
        - name: replacement_plan_id
          description: >
            Identifier for the replacement plan if applicable. A replacement plan is defined as a plan that
            started within 5 days before, or up to 30 days after the end date of the prior plan and is not
            an add-on plan.
        ```
    5. If you find a column that is in the existing documentation, but not in the model, comment it out with a `#` at the start of each line.
    6. Only return the YML documentation file contents. Do not provide an explanation.
    7. Always place a new line between the end of the `description` line and the start of the next column name identified by `- name:`.
    8. If updating and existing file, do not replace or modify existing descriptions, data_tests:, or config blocks. Only add new ones, and comment out descriptions that don't exist in the SQL.
    9. Reorder or order the column descriptions in the YML file in the same order they appear in the SQL query. If you are modifying an existing YML file, still re-order the elements, don't comment out the old element location and put a new element in.
    10. If modifying an existing YML, leave the value of materialized as is. Do not change it to `table` if it is `view` or vice versa.
    11. The acronym PoP stands for "period over period". This will be some form of lookback or comparison to a prior period.
    12. The acronym MA stands for Moving Average. This will be some sort of moving average of days, or weeks.
    13. Lightdash portion details:

        We are using the lightdash system. This appends additional data to the columns of the YML file in a field called meta. For all fields, the following process should be followed. For all label values, title case should be used:
        1. If updating an existing YML and the meta parameter already exists, do not modify anything in the meta parameter. Modify other items as needed.

        2. Dimension fields. Dimensions are values that can be string, date, or number, but are not, and would not be aggregated via a sum or average type function. Some example of these fields would be anything that is boolean, a date, a string, or an ID field. Add the following structure to these fields:

        a. If the field is an ID, we want to hide it add:
        ```
        meta:
          hidden: true
        ```

        b. If the field is a date it will have _at either at the end or in the middle. For example, date_at, order_at_month, order_at_year. Add the following structure. For the label, split the name at the underscore and replace at with date. For example, if the field is order_date, the label would be "Order Date":
        ```
        - name: order_at
          description: "The date associated with the order."
           data_tests:
            - not_null
          meta:
            dimension:
              type: date
              label: "Order Date"
              time_intervals: [ "DAY", "WEEK", "MONTH", "QUARTER" ]
        ```
        If the name of the field contains "month", exclude "DAY", and "WEEK". If it contains "YEAR", exclude "DAY", "WEEK", and "MONTH".

        c. If the field is a boolean, replace the label with the name of the field, remove is_ from the prefix, and add "Flag". For example, is_active would become "Active Flag" and add the following structure:
        ```
        - name: is_active
          description: "Indicates if the record is active."
          meta:
            dimension:
              label: "Active Flag"
              type: boolean
        ```

        d. If the field is a string, structure as follows.
        ```
        - name: location_name
          description: "The name of the location where the order was placed."
          meta:
            dimension:
              label: "Location Name"
              type: string
        ```

        3. Metric fields. A metric field is any value that isn't an ID, and is numeric. We will define a dimension for these fields to hide them. For each of these fields, add a default sum and average metric. The sum label is just the name of the measure. Do not append "sum" to the end. For average, add the word "- Avg" to the end of the label.

        Each metric will need one or more groups assigned. Groups are assigned to a metric via the `groups: ["<group name>"]` key. These groups must be defined in the top level `config` block using the `group_details` attribute like this:

        ```
        group_details:
            example_top_level_grp:
              label: "Example Top Level Group"
            revenue:
              label: "Revenue"
            counts:
              label: "Counts"
        ```

        a. If the measure has "revenue" or "cost" in the name and the sample data shows values in the thousands or millions, add:
        ```
        format: "usd"
        round: 0
        compact: thousands
        groups: ["revenue"]
        ```
          if the sample data is typically in the hundreds, do not add `compact: thousands`. to the output.

        b. If the measure is a type of count, and the sample data shows values in the thousands or millions, add:
        ```
        round: 0
        compact: thousands
        groups: ["example_top_level_grp", "counts"]
        ```
            if the sample data is typically in the hundreds, do not add `compact: thousands`. to the output.

        c. If the measure is some other type of numeric value that is not an ID, take a best guess on the group field. Try to group similar measures together.
        ```
        round: 2
        groups: ["<best guess>"]
        ```

        Example:
        ```
        - name: medical_revenue
          description: "Total revenue from medical services."
          meta:
            dimension:
              hidden: true
            metrics:
              medical_revenue_sum:
                type: sum
                label: "Medical Revenue"
                description: "Total revenue from medical services."
                format: "usd"
                round: 0
                compact: thousands
                groups: ["revenue"]
        ```

        4. For grouping, try to cluster measures and dimensions based on commonalities. For these guidelines, when I say "measures or dimensions", I mean treat them seperatly. If there are 3 dimensions and 20 measures, you would only use a single grouping level for the dimensions, and up to three levels for metrics. Use the following guidelines:
            - If less than 6 measures or dimensions, only provide one grouping level.
            - If 6 or more measures or dimensions, provide two grouping levels if there is a logical division. For example, some metrics might apply to current period and could be added to the `current` group, with a sub group like `groups: ['current', 'revenue']`.
            - If there are more than 15 measures or dimensions, you can nest up to a third level of grouping.

        5. If there is an primary key ID column as the first field, then add a
           ```
           data_tests:
             - unique
             - not_null
           ```

          If the first column is not a primary key ID column, then use a "unique_combination_of_columns" test like this:
            ```
            data_tests:
              - dbt_utils.unique_combination_of_columns:
                  combination_of_columns:
                    - month_at
                    - network_name
            ```



Full example output:
```
version: 2

models:
  - name: appointment_revenue_mrpv_metrics
    description: >
      This model provides Medical Revenue Per Vist (MRPV) metrics. It includes filterable dimensions by first appt/rev
      veterinarian, location, and network.

    config:
      materialized: table
      group_details:
        appointments:
          label: "Appointments"
        financial:
          label: "Financial Metrics"
        revenue:
          label: "Revenue"
        counts:
          label: "Counts"

    columns:
      - name: order_at
        description: "The date associated with the order."
         data_tests:
          - not_null
        meta:
          dimension:
            type: date
            time_intervals: [ "DAY", "WEEK", "MONTH", "QUARTER" ]

      - name: location_id
        description: "The identifier for the location where the order was placed."
        meta:
          dimension:
            hidden: true

      - name: location_name
        description: "The name of the location where the order was placed."
        meta:
          dimension:
            label: "Location Name"
            type: string

      - name: network_name
        description: "The name of the network associated with the order."
        meta:
          dimension:
            label: "Network Name"
            type: string

      - name: medical_revenue
        description: "Total revenue from medical services."
        meta:
          dimension:
            hidden: true
          metrics:
            medical_revenue_sum:
              type: sum
              label: "Medical Revenue"
              description: "Total revenue from medical services."
              format: "usd"
              round: 0
              compact: thousands
              groups: ["financial", "revenue"]

      - name: medical_appointment_count
        description: "Count of medical appointments."
        meta:
          dimension:
            hidden: true
          metrics:
            medical_appointment_count_sum:
              type: sum
              label: "Medical Appointment Count"
              description: "Count of medical appointments."
              round: 0
              compact: thousands
              groups: ["appointments", "count"]

```

This is a CSV data sample from the model:
        """

    @property
    def dbt_docs_lte_l2_prompt(self):
        return """
        You will help build DBT documentation YML files for a given SQL query. Sometimes you will be asked to generate a description from scratch, other times you will be asked to fill in missing columns that exist in the model, but not in the documentation.


Primary DBT Guidelines:

    3. Include a config block for each model:
        a. Set `materialized` to `view`
        b. Do not include a `sort` key.
        c. If the model name ends in `_mat` set materialized to `table`.
    4. Add data_tests: `unique` and `not_null` to the primary key only. Do not add data_tests: to any other columns.
    5. For long descriptions, use the following format so the lines are not too long:
        ```
        - name: replacement_plan_id
          description: >
            Identifier for the replacement plan if applicable. A replacement plan is defined as a plan that
            started within 5 days before, or up to 30 days after the end date of the prior plan and is not
            an add-on plan.
        ```
    6. If you find a column that is in the existing documentation, but not in the model, comment it out with a `#` at the start of each line.
    7. Only return the YML documentation file contents. Do not provide an explanation.
    8. Always place a new line between the end of the `description` line and the start of the next column name identified by `- name:`.
    9. Do not replace or modify existing descriptions, data_tests:, or config blocks. Only add new ones, and comment out descriptions that don't exist in the SQL.
    10. Reorder or order the column descriptions in the YML file in the same order they appear in the SQL query. If you are modifying an existing YML file, still re-order the elements, don't comment out the old element location and put a new element in.
    11. If modifying an existing YML, leave the value of materialized as is. Do not change it to `table` if it is `view` or vice versa.
    12. Lightdash portion details:

        We are using the lightdash system. This appends additional data to the columns of the YML file. As this is a file in the L1 or L2 layer, we are just going to add a simple meta block to the top with the following code:
        ```
            meta:
              required_attributes:
                is_admin: "true"
        ```

Full example output:
```
version: 2

models:
  - name: stg_vs_example
    description: >
      This is an example description that is longer than one line. It is a good example of how to write a long
      description using the > character.

    config:
      materialized: table

    meta:
      required_attributes:
        is_admin: "true"

    columns:
      - name: order_at
        description: "The date associated with the order."

      - name: location_id
        description: "The identifier for the location where the order was placed."

      - name: location_name
        description: "The name of the location where the order was placed."

      - name: network_name
        description: "The name of the network associated with the order."

      - name: medical_revenue
        description: "Total revenue from medical services."

      - name: medical_appointment_count
        description: "Count of medical appointments."
```
This is a CSV data sample from the model:
        """

    @property
    def build_unit_test_prompt(self):

        return """
You will help build mockup input and expected output data for DBT unit data_tests: using the EqualExperts/dbt_unit_testing package. The input and expect data will be in a CSV type format using | as a seperator between fields.

The user will pass a SQL DBT model that looks like this as input:
```
select
    date(o.order_item_at)   as revenue_day_at
  , o.location_id
  , o.is_medical_revenue
  , o.is_plan_payment
  , o.location_name
  , o.product_type_name
  , sum(o.total_before_tax) as revenue_sum

from {{ dbt_unit_testing.ref('fct_order_items_mat') }} o
group by revenue_day_at
       , location_id
       , is_medical_revenue
       , is_plan_payment
       , location_name
       , product_type_name
```

You will return data that looks like this. Leave this line as is for the user to fill in `{% call dbt_unit_testing.test('model_name', 'Description of Test') %}` :

```
{{ config(tags=['unit-test']) }}

--depends-on: {{ ref('fct_appointments') }}

{% call dbt_unit_testing.test('model_name', 'Description of Test') %}

    {% call dbt_unit_testing.mock_ref('fct_order_items_mat', options={"input_format": "csv"}) %}

    ORDER_ITEM_AT                          |LOCATION_ID |IS_MEDICAL_REVENUE |IS_PLAN_PAYMENT |LOCATION_NAME | PRODUCT_TYPE_NAME    | TOTAL_BEFORE_TAX
    '2024-01-01 00:00:00.000000000 -08:00' |123         |TRUE               |TRUE            |'ABC123'      | 'Product 1'          | 25
    '2024-01-01 00:00:00.000000000 -08:00' |123         |TRUE               |FALSE           |'ABC123'      | 'Product 2'          | 25
    '2024-01-01 00:00:00.000000000 -08:00' |123         |FALSE              |FALSE           |'ABC123'      | 'Product 2'          | 25
    '2024-01-01 00:00:00.000000000 -08:00' |123         |TRUE               |TRUE            |'ABC123'      | 'Product 1'          | 25
    '2024-01-01 00:00:00.000000000 -08:00' |123         |TRUE               |FALSE           |'ABC123'      | 'Product 2'          | 25
    '2024-01-01 00:00:00.000000000 -08:00' |123         |FALSE              |FALSE           |'ABC123'      | 'Product 2'          | 25
    '2024-01-01 00:00:00.000000000 -08:00' |987         |TRUE               |TRUE            |'DEF123'      | 'Product 1'          | 25
    '2024-01-01 00:00:00.000000000 -08:00' |987         |TRUE               |FALSE           |'DEF123'      | 'Product 2'          | 25
    '2024-01-01 00:00:00.000000000 -08:00' |987         |FALSE              |FALSE           |'DEF123'      | 'Product 2'          | 25

    {% endcall %}

    {% call dbt_unit_testing.expect({"input_format": "csv"}) %}

    REVENUE_DAY_AT |LOCATION_ID |IS_MEDICAL_REVENUE |IS_PLAN_PAYMENT |LOCATION_NAME  |PRODUCT_TYPE_NAME |REVENUE_SUM
    '2024-01-01'   |123         |TRUE               |TRUE            |'ABC123'       |'Product 1'       |50
    '2024-01-01'   |123         |TRUE               |FALSE           |'ABC123'       |'Product 2'       |50
    '2024-01-01'   |123         |FALSE              |FALSE           |'ABC123'       |'Product 2'       |50
    '2024-01-01'   |987         |TRUE               |TRUE            |'DEF123'       |'Product 1'       |25
    '2024-01-01'   |987         |TRUE               |FALSE           |'DEF123'       |'Product 2'       |25
    '2024-01-01'   |987         |FALSE              |FALSE           |'DEF123'       |'Product 2'       |25

    {% endcall %}
{% endcall %}
```

Note how the model aggregates the expected REVENUE_SUM. Do your best to aggregate the expected data based on the SQL in the input. The goal is to create a model that is easy to read and hand validate.

When creating the mock data, follow these guidelines:

1. For boolean input columns, create enough rows that you can test both TRUE and FALSE values for all columns. For example, if there are 3 boolean columns, you would need six rows to test all combinations of TRUE and FALSE values.
2. For ID columns, use simple numbers. For example, 123, 456, 789, etc.
3. For name columns, try to identify when the name should be the same for a given ID. For example, if there are 3 rows with LOCATION_ID = 123, then the LOCATION_NAME should be the same for all three rows.
4. If a column ends in _at, it is either a date or a timestamp. If it is date, the column will end in _day_at. Timestamps will only end in _at. If the column is a date, use a date format like '2024-01-01'. If the column is a timestamp, use a timestamp format like '2024-01-01 00:00:00.000000000 -08:00'.
5. For numeric or dollar value columns, use simple numbers. For example, 10, 20.
6. Use a minimal number of rows needed to fully exercise the logic in the function. Try to sort dates and group by locations, names, or other similar common values.
7. You will need an `mock_ref` block for each DBT model in the input SQL. DBT models will be defined as either {{ ref('model_name') }} or {{ dbt_unit_testing.ref('model_name') }}.
8. Align the columns in the input and expected using tabs. You can use as many rows as needed.
9. Output the data in the same format as the example. Use as many `dbt_unit_testing.mock_ref` blocks as needed.
10. Use enough rows with variation that at least one aggregation can be created. For example, if the model groups by date and ID, you will need at least two rows with the same date and ID but different values for the columns being aggregated.
11. Location names are always three uppercase letters followed by three numbers. For example, "ABC123" or "DEF123". Network names are always the first three uppercase letters of the network name, like "ABC" or "DEF"
12. At the top of the file as in the example, add a --depends-on line for each moc_ref model used in the input SQL. Example, --depends-on: {{ ref('fct_appointments') }}
13. Encapsulate any string in single or date in single quotes. Even if the sample data has long strings, truncate to no more than 30 characters, preferably even less unless the logic requires something more.
14. Try to limit the date range in the input data to one or two days of time span, unless more is needed to fully test the logic of the model.
15. Do not include timezones in mockup data unless the sample data provided for that model includes timezones.
16. Do not include columns in the mock_ref blocks that are not used by the SQL model being tested.
Do not provide an explanation, only return the code for the test.
        """


# %%
