## Pandas
df.loc[0:1,"a":"b"] | inclusive of both
df.iloc[0:1,0:1] | exclusive of right
df.sort_values(by=...,ascending=False,key=...)
df.drop("abc",axis=1)
df.rename({"col1":"newname"})
df.sample(n,replace=True)
series.value_counts() | series.unique()
df.merge(temp,how="inner",left_on="key",left_index=True...)

## Plots
Bar - express categorical
>>sns.countplot(data = df, x = 'col');px.histogram(df, x = 'col')
Histogram - express proportion
>>sns.histplot(data = df, x = 'col');px.histogram(df, x = 'df')
left skew - tail on left - negative skew

box plot
>>>sns.boxplot(y = "col", data = df)
inner fence - whisker = Q1 - 1.5IQR
outer fence = Q1 - 3IQR
Near outlier - [outer,inner fence]
Far outlier - past outer fence

Scatter
>>>sns.lmplot(data=df, x='', y='', ci=False) | confidence interval
>>>sns.jointplot(data=births, x='', y='') - see distribution | kind="kde/hex"

KDE
- alpha - bandwidth - size of bin - large smoother
>>>sns.displot()

# Linear regression

## cross validation
Holdout method - simple CV - train,validation set
K-fold - k splits, each split becomes validation set, score = ave(sum(score_k))

## SQL
select * from * where * having * order by * limit 1
a inner join b on a.a=b.a
a cross join b where a.a=b.a
left outer join | full outer join
SELECT CAST(col as INT)
CASE WHEN ... THEN ... ELSE ... END
NOTE: use offset with order by (else not deterministic)

## Database
Fact table - joining table
Dimension table - information table