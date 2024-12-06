import progressbar


def progress_bar_search_loop(target_name, item_type, key_to_search, data_to_loop):
    """Search for a specific item in a list of data using a progress bar.

    Args:
        target_name (string): The name of the item to search for.
        item_type (string): The type of item being searched.
        key_to_search (string): The key to use for searching in the data.
        data_to_loop (list[dicts]): The list of data to search through.

    Returns:
        dict: The data of the found item if it exists, otherwise None.
    """
    i = 0  # counter for progress bar
    with progressbar.ProgressBar(max_value=len(data_to_loop)) as bar:
        print(f'Searching for the {item_type} {target_name}...')
        for data in data_to_loop:
            # check if the data is nested
            if isinstance(data, dict):
                for item in data:
                    if item[key_to_search] == target_name:
                        return item  # target acquired
            # assuming not nested data
            else:
                if data[key_to_search] == target_name:
                    return data  # target acquired

            i += 1
            bar.update(i)

    print()  # cleanse the bar
    return None  # no results found


def progress_bar_eta(max_value):
    """Creates a progress bar with an estimated time of arrival.

    Args:
        max_value (int): The maximum value of the progress bar.

    Returns:
        progressbar.ProgressBar: The progress bar object.
    """
    return progressbar.ProgressBar(max_value=max_value, widgets=[
        progressbar.Percentage(),
        progressbar.Bar(),
        progressbar.ETA()
    ])
