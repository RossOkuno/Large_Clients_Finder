def large_clients_finder(data, client_id_col_name, value_col_name, threshold_rate):
    """
    This function returns a list of large clients.
    Parameters
    ----------
    data : Pandas DataFrame consists of at least client name column
            and value (such as sales or consumption) column.
    client_id_col_name : String. The name of client name column.
                        E.g. "customer_id"
    value_col_name : String. The name of value column.
                        E.g. "power_usage"
    threshold_rate : Float. Percentage large clients account for.
        In 80/20 rule, register 0.8.
    """

    # prepare variables for calculation
    large_clients_consumption = 0
    large_clients = []
    total_consumption = data[value_col_name].sum()
    threshold = total_consumption * threshold_rate

    # sort clients by consumption in descending order
    df = data.groupby(client_id_col_name)[value_col_name].sum().reset_index()
    df = df.sort_values(by=value_col_name, ascending=False)

    # add top clients consumption until the sum of its consumption reaches the thereshold
    for i in range(len(df)):
        if large_clients_consumption <= threshold:
            large_clients_consumption += df.iloc[i][value_col_name]
            large_clients.append(df.iloc[i][client_id_col_name])
        else:
            break

    # print how many large clients account for the threshold and return a list of large clients
    print("Top %d (%.2f%%) clients account for %.2f%% of the total consumption or sales." %
          (len(large_clients), (len(large_clients) / len(df)) * 100,
           (large_clients_consumption / total_consumption) * 100))
    return large_clients