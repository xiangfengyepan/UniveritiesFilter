# my_custom_function.py

def process(df):
    """
    Example process function that performs custom data manipulation on a DataFrame.

    This function filters rows where the value in the "Població" column is 'Barcelona',
    and then sorts the rows by the "Preu orientatiu" column in descending order.
    """
    # Filter rows where the "Població" column is 'Barcelona'
    filtered_df = df[df['Població'] == 'Barcelona']
    
    # Sort the filtered DataFrame by the "Preu orientatiu" column in descending order
    sorted_df = filtered_df.sort_values(by='Preu orientatiu', ascending=False)
    
    return sorted_df
