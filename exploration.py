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

# calculons le nompre des pris négatifs et nul dans notre jeu de données 
print("\nPrix nuls: ", (df['UnitPrice']==0).sum())
print("\nPrix négatifs: ", (df['UnitPrice']<0).sum())

print("\nLinges avec des prix négatifs :")

print(
    df.loc[df['UnitPrice']<0, ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'UnitPrice']].to_string(index=False)
)

print("\nDescription des prix nuls : ")
print(
    df.loc[df["UnitPrice"] == 0, "Description"]
    .value_counts(dropna=False)
    .head(10)
)

#voir combien on de doublons sur notre jeu de donée : 
print("\nNombre de doublons:", df.duplicated().sum())

print("\nExemple de doublons exact: ")
doublons = df[df.duplicated(keep=False)] 

print(
    doublons.sort_values(['InvoiceNo', 'StockCode'])
    .head(10)
    .to_string(index=False)
)

dates = pd.to_datetime(
    df["InvoiceDate"],
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce"
)

print("\nDates non convertibles:", dates.isna().sum()) 
print("\nPremières date :", dates.min())
print("\nDernière date :", dates.max())

df["InvoiceDate"] = dates

#première analyse : quantité de produits positifs avec prix positifs en éxluant les factures commancant par c 
# c désigne les annulations de commandes 'cancelled' 

ventes = df.loc[
    (df['Quantity'] > 0) 
    & (df['UnitPrice'] > 0) 
    & (~df['InvoiceNo'].str.startswith('C'))
].copy() 

print("\nNombre de lignes de ventes valides: ", len(ventes))

ventes["Montant"] = ventes["Quantity"] * ventes["UnitPrice"]
total_ventes = ventes["Montant"].sum()

print("\nTotal des ventes valides: ", total_ventes)

nombre_commandes = ventes["InvoiceNo"].nunique()

print("Nombre de commandes :", nombre_commandes) #une factures contenant plusieurs produits est considérée comme une seule commande


ventes_sans_doublons = ventes.drop_duplicates()
total_sans_doublons = ventes_sans_doublons["Montant"].sum() 
ecart = total_ventes - total_sans_doublons

print("\nLinges en moins après suppression des doublons: ", len(ventes) - len(ventes_sans_doublons))
print("\nTotal des ventes sans doublons: ", total_sans_doublons)
print(f"\nÉcart: {ecart:,.2f}")