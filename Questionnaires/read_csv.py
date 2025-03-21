import pandas as pd

# Perform reversion of the items according to the test
def reverse(rev_set, df, type):
    for trait, items in rev_set.items():
        for item in items:
        # Subtract 1 to adjust for 0-based indexing in Python
            if type == 'big5':
                df.iloc[:, item - 1 ] = df.iloc[:, item - 1 ]*(-1)
            if type == 'iri':
                df.iloc[:, item - 1] = df.iloc[:, item - 1 ]*(-1)+4

# Perform score sum for each trait
def eval_score(set, df, score_df):
    for trait, items in set.items():
        # Somma i punteggi per gli items regolari
        try:
            score_df[trait] = df.iloc[:, [item - 1 for item in items]].sum(axis=1, skipna=True)
        except IndexError as e:
            print(f"Error with trait {trait}: {e}")

# BIG-5 Items 1-44
big5_items = {
    'Extraversion': [1, 11, 16, 26, 36, 6, 21, 31],
    'Agreeableness': [7, 17, 22, 32, 42, 2, 12, 27, 37 ],
    'Conscientiousness': [3, 13, 28, 33, 38, 8, 18, 23, 43],
    'Neuroticism': [4, 14, 19, 29, 39, 9, 24, 34],
    'Openness': [5, 10, 15, 20, 25, 30, 40, 44, 35, 41]
}
big5_reversed_items = {
    'Extraversion': [6, 21, 31],
    'Agreeableness': [2, 12, 27, 37],
    'Conscientiousness': [8, 18, 23, 43],
    'Neuroticism': [9, 24, 34],
    'Openness': [35, 41]
}

# IRI Items 1-28
iri_items = {
    'Perspective-Taking' : [3, 8, 11, 15, 21, 25, 28],
    'Fantasy' : [1, 5, 7, 12, 16, 23, 26],
    'Emphatic Concern' : [2, 4, 9, 14, 18, 20, 22],
    'Personal Distress' : [6, 10, 13, 17, 19, 24, 27]
}
iri_reversed_items = {
    'Perspective-Taking' : [3],
    'Fantasy' : [7, 12],
    'Emphatic Concern' : [4, 14, 18],
    'Personal Distress' : [13, 15, 19]
}

# Load csv as DataFrame. Replace "dummy.csv" with your results sheet
df = pd.read_csv('dummy.csv')

# Partitioning
df_big5 = df.iloc[:, 1:45]
df_iri = df.iloc[:, 45:]

# Columns name matching
df_big5.columns = range(1, 45)
df_iri.columns = range(1, 29)

scores_big5 = {}
scores_iri = {}

# Eval on 0-4 scale instead of 1-5
df_iri = df_iri.map(lambda x: x - 1 if isinstance(x, (int, float)) else x)

# Accounting reverse values
reverse(big5_reversed_items, df_big5, 'big5')
reverse(iri_reversed_items, df_iri, 'iri')

# Score sum
eval_score(big5_items, df_big5, scores_big5)
eval_score(iri_items, df_iri, scores_iri)

# Combine the results into a DataFrame
big5_scores = pd.DataFrame(scores_big5)
iri_scores = pd.DataFrame(scores_iri)

# Print the calculated scores for each Big 5 trait
print(big5_scores)
print(iri_scores)
