import pandas as pd
import sys

testing_sales_df = pd.DataFrame({"SalesNumber" : [10001, 10002], "SalesDate": ["2026-01-05", "2026-01-09"], "GrossAmount":[5, 9]})

testing_arg = sys.argv[1]

output_df = testing_sales_df[testing_sales_df['SalesDate'] == testing_arg]
print(output_df)

output_df.to_parquet(f'Sales_Amount_on_{testing_arg}.parquet')
