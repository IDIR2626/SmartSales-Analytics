import pandas as pd

#df = pd.read_excel('data/Online Retail.xlsx', sheet_name='Online Retail')
#df.to_csv('data/Online Retail.csv', index=False)
df = pd.read_csv('data/Online Retail.csv')
print(df.head())

print("Dimension de jeu de données: ", df.shape)
print("Colonnes: ", df.columns)
print("\nTypes de données: ", df.dtypes)
#vérifications s'il manques des données
print("\nNombre de valeurs manquantes par colonne:", df.isna().sum()) 
#nombre de lignes avec des quantités negatives
print("\nNombre de lignes avec des quantités négatives:", (df['Quantity']<0).sum())
#exemple des quantités négatives 
print(df.loc[df['Quantity'] < 0, ['InvoiceNo', 'Description', 'Quantity']].head()) # .loc permet de sélectionner des lignes et des colonnes spécifiques

negative_quantity_df = df[df['Quantity'] < 0]
print(
    "Quantités négatives sans c au début de la facture: ",
    (~negative_quantity_df['InvoiceNo'].str.startswith('C')).sum()
)

negative_quantity_sans_c_df = negative_quantity_df[~negative_quantity_df['InvoiceNo'].str.startswith('C')]
print("\nQuantités négatives sans c au début de la facture:")
print(negative_quantity_sans_c_df[['InvoiceNo', 'Description', 'Quantity']].head(10))
print("\nNombre de lignes avec des quantités négatives sans c au début de la facture avec une description null:", negative_quantity_sans_c_df['Description'].isna().sum())
print("\nQuantités négatives sans c au début de la facture avec une description :")
print(
    negative_quantity_sans_c_df[negative_quantity_sans_c_df['Description'].notna()][
        ['InvoiceNo', 'Description', 'Quantity']
    ].head(10)
)

print(
    "Répartition des prix des quantités négatives sans C :\n",
    negative_quantity_sans_c_df["UnitPrice"].value_counts(dropna=False)
)