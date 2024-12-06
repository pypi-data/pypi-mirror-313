'''
Statistics function
'''

from scipy import stats

def test_kruskal_wallis(*groups, variable, dataframe, alpha = 0.02, fill_na=0):
    """
    Statistical Kruskal-Wallis test.

    Parameters
    ----------

    groups : packaging argument, pd.Dataframe
        Dataframe with one of the target groups.
    dataframe : pd.Dataframe
        Dataframe with all target groups
    alpha : float, optional
        Statistical significance, by default 0.02
    fill_na : int, optional
        Fill empty rows, by default 0
    """
    krus_group = []
    for group in groups:
        group = group[variable].fillna(fill_na).to_list()
        krus_group.append(group)
    h_statistic, p_value = stats.kruskal(*krus_group)

    print("Wartość H-statystyki:", h_statistic)
    print("Wartość p-value:", p_value)

    if p_value < alpha:
        print("Odrzucamy hipotezę zerową - istnieje istotnie statystycznie różnice między przynajmniej jedną parą grup. Sprawdź poniższe mediany.")
        return dataframe.groupby('category')[variable].median()
    print("Nie ma podstaw do odrzucenia hipotezy zerowej - nie ma istotnych statystycznie różnic między grupami.")
