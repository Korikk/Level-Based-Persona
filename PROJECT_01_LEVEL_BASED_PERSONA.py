import pandas as pd

# Reading csv files. Create the "df" dataframe by merging "users" and "purchases" on "uid".
users = pd.read_csv("Week_02/datasets/users.csv")
purchases = pd.read_csv("Week_02/datasets/purchases.csv")
df = purchases.merge(users, how='left', on='uid')

users.head()
purchases.head()
df.head()

# Generalize the dataframe by grouping some columns as index to see total prices.
agg_df = df.groupby(["country", "device", "gender", "age"]).agg({"price": "sum"}).sort_values("price", ascending=False)

agg_df = agg_df.reset_index()

# Add a new column as "age_cat" to define age ranges.
agg_df["age_cat"] = pd.cut(agg_df["age"], bins=[0, 18, 25, 35, 50, 70, 100],
                           labels=['0_18', '19_25', '26_35', '36_50', '51_70', '71_100'])

agg_df.drop("age", axis=1, inplace=True)

# Check the null values.
agg_df.isnull().sum()
agg_df.isna().sum()

# Combine the categorical columns as one.
agg_df["customers_level_based"] = [row[0]+"_"+row[1].upper()+"_"+row[2]+"_"+row[4] for row in agg_df.values]

agg_df = agg_df[["customers_level_based", "price"]]

# Create segments based on price ranges.
agg_df["groups"] = pd.qcut(agg_df["price"], 4, labels=["D", "C", "B", "A"])

# Calculate the mean of each segment to evaluate them.
agg_df.groupby(["groups"]).agg({"price": "mean"})

# Add a new user then specify his/her segment.
# In this case new user's segment is C because 1333(D) < 1596 < 3675(B).
#new_user = {"customers_level_based": "TUR_IOS_F_41_75", "price": 1596, "groups": "C"}
#agg_df = agg_df.append(new_user, ignore_index=True)

new_user = "TUR_IOS_F_41_75"
agg_df[agg_df["customers_level_based"] == new_user]
