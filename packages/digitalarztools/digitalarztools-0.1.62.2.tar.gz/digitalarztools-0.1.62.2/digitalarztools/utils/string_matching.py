from fuzzywuzzy import process


def get_closest_match(x, choices, scorer, cutoff=70):
    """
    usage:
    # Apply fuzzy matching for unmatched rows (example logic)
    choices = df['Name_standardized'].unique()
    gdf['tehsil_matched'] = gdf['tehsil_standardized'].apply(lambda x: get_closest_match(x, choices, scorer=fuzzywuzzy.fuzz.token_sort_ratio, cutoff=70))

    """
    match = process.extractOne(x, choices, scorer=scorer, score_cutoff=cutoff)
    if match:
        return match[0]
    return None
