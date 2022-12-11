import os
import pandas as pd

# ==================== Initialize ====================
file_path = r'C:\Users\insert_template'
file_name = 'test1'
file_suffix = '.xlsx'
sheet_name = 'Sheet1'

# If select all the columns, selected_columns = None
# selected_columns = ['index', 'BOE Type', 'Date', 'Segment', 'Client ID', 'Client']
selected_columns = None

# If snowflake_table_name = None, table name is the same as file name
snowflake_table_name = 'test_excel'

# Recommended 50 - 100 (need to be confirmed)
bulk_insert_num = 10

# ==================== Read table ====================
file_df = pd.read_excel(os.path.join(file_path, file_name) + file_suffix, sheet_name = sheet_name)

if selected_columns:
    file_df = file_df[selected_columns]

row_num, column_num = file_df.shape
print('========== Read table FINISHED ==========')
print(f'row numbers: {row_num}, column numbers: {column_num}')

# ==================== Snowflake table name ====================
if not snowflake_table_name:
   snowflake_table_name = file_name

snowflake_table_name = snowflake_table_name.upper()

print('\n========== Get table name FINISHED ==========')
print(f'Excel table name: {file_name}')
print(f'Snowflake table name: {snowflake_table_name}')

# ==================== Generate DROP TABLE sql ====================
sql = 'USE SCHEMA "DEMO_DB"."PUBLIC";\n'
sql += f'DROP TABLE IF EXISTS {snowflake_table_name};\n'

# ==================== Generate CREATE TABLE sql ====================

dtypes = file_df.dtypes

# Column names
column_names = list(dtypes.index)
snowflake_column_names = [column_name.replace(' ', '_').upper() for column_name in column_names]

print(f'\n========== Covert column names FINISHED ==========')
print(f'Excel column names: {column_names}')
print(f'Snowflake column names: {snowflake_column_names}')

# Column types
snowflake_column_types = []
snowflake_column_quote_types = set()

# TO DO: handle other dtypes
# DONE: TEXT, TIMESTAMP_NTZ, NUMBER, BOOLEAN, FLOAT
# VARIANT, DATE, TIMESTAMP_LTZ

dtypes = list(dtypes.values)

for i in range(column_num):
    dtype = dtypes[i]

    if dtype == 'object':
        snowflake_column_type = 'TEXT'
        snowflake_column_quote_types.add(snowflake_column_type)

    elif dtype == 'datetime64[ns]':
        snowflake_column_type = 'TIMESTAMP_NTZ'
        snowflake_column_quote_types.add(snowflake_column_type)

    elif dtype == 'int64':
        snowflake_column_type = 'NUMBER'

    elif dtype == 'float64':
        snowflake_column_type = 'FLOAT'

    elif dtype == 'bool':
        snowflake_column_type = 'BOOLEAN'

    else:
        print(f'\n========== Covert column types Failed ==========')
        print(f'Add more conditions. column_name: {column_names[i]}, dtype: {dtype}')
        exit()

    snowflake_column_types.append(snowflake_column_type)

print(f'\n========== Covert column types FINISHED ==========')
print(f'Excel column types: {[str(dtype) for dtype in dtypes]}')
print(f'Snowflake column types: {snowflake_column_types}')
print(f'Snowflake column types with quote: {snowflake_column_quote_types}')

# Generate sql
column_names_types_sql = ', '.join([f'{snowflake_column_names[i]} {snowflake_column_types[i]}' for i in range(column_num)])
sql += f'CREATE TEMPORARY TABLE {snowflake_table_name} ({column_names_types_sql});\n'

# ==================== Generate INSERT TABLE sql ====================
column_names_sql = ', '.join(snowflake_column_names)
bulk_insert_count = 0
column_values_sqls = []

for i in range(row_num):
    values = file_df.iloc[i].values
    column_values = []

    for j in range(column_num):

        if pd.isnull(values[j]):
            column_value = 'NULL'

        else:
            if snowflake_column_types[j] in snowflake_column_quote_types:
                column_value = f'\'{values[j]}\''

            else:
                column_value = str(values[j])

        column_values.append(column_value)

    column_values_sql = ', '.join(column_values)

    bulk_insert_count += 1
    column_values_sqls.append(column_values_sql)

    if bulk_insert_count >= bulk_insert_num or i == row_num - 1:

        bulk_values_sql = ','.join([f'({column_values_sql})' for column_values_sql in column_values_sqls])
        sql += f'INSERT INTO {snowflake_table_name} ({column_names_sql}) VALUES {bulk_values_sql};\n'

        bulk_insert_count = 0
        column_values_sqls = []

# ==================== Save sql file ====================
sql_file_full_path = os.path.join(file_path, file_name) + '.sql'
with open(sql_file_full_path, 'w') as f:
    f.write(sql)

# ==================== Finish ====================
print('\n========== Convert excel to sql FINISHED ==========')
print(f'sql file path: {sql_file_full_path}')