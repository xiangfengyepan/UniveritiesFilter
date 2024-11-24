class DataFrameProcessor:
    def __init__(self, df):
        self.df = df

    def clean_currency(self, column):
        """
        Cleans the currency column by removing the currency symbol and converting to float.
        It also handles the thousands separator (dot) and the euro symbol (€).
        """
        def parse_currency(value):
            if isinstance(value, str):
                # Remove the euro sign and spaces
                value = value.replace('€', '').replace(' ', '').strip()
                # Replace dot with empty for thousands separator and convert to float
                value = value.replace('.', '')
                try:
                    return float(value)
                except ValueError:
                    return None  # If the value cannot be converted, return None
            return value  # If not a string, return the value unchanged
            
        self.df[column] = self.df[column].apply(parse_currency)
        return self.df

    def compare_columns(self, col1, col2, operation):
        """
        Compare two columns based on the operation provided.
        Supports operations like '>', '<', '>=', '<=', '==', and '!='.
        """
        self.clean_currency(col1)
        self.clean_currency(col2)

        if operation == '>':
            return self.df[self.df[col1] > self.df[col2]]
        elif operation == '<':
            return self.df[self.df[col1] < self.df[col2]]
        elif operation == '>=':
            return self.df[self.df[col1] >= self.df[col2]]
        elif operation == '<=':
            return self.df[self.df[col1] <= self.df[col2]]
        elif operation == '==':
            return self.df[self.df[col1] == self.df[col2]]
        elif operation == '!=':
            return self.df[self.df[col1] != self.df[col2]]
        else:
            raise ValueError("Unsupported operation. Use one of: '>', '<', '>=', '<=', '==', '!='.")

    def clean_all_currency_columns(self, columns):
        """
        Automatically clean the specified currency columns.
        """
        for col in columns:
            self.clean_currency(col)
        return self.df

    def filter_lines(self, func_filter):
        """
        Filters the DataFrame by applying the func_filter to each row.
        If func_filter returns False, the row is removed.
        """
        # Apply func_filter to each row and keep the rows where func_filter is True
        self.df = self.df[self.df.apply(func_filter, axis=1)]
        return self.df

    def sort_lines(self, func_sort):
        """
        Sorts the DataFrame by applying the func_sort to each row.
        The function returns an integer value that determines the sort order.
        """
        # Create a new column with the sort values based on func_sort
        self.df['sort_order'] = self.df.apply(func_sort, axis=1)
        
        # Sort by the sort_order column, and then drop it as it's not needed anymore
        self.df = self.df.sort_values(by='sort_order', ascending=True).drop(columns=['sort_order'])
        return self.df