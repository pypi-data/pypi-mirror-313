import pandas as pd
import numpy as np
from feature_engine.outliers import Winsorizer



def outl_iqr(df,columns):
    for i in columns:
        IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
        UL = df[i].quantile(0.75) + (1.5 * IQR)
        LL = df[i].quantile(0.25) - (1.5 * IQR)

        df[i] = np.where(df[i] > UL, UL, np.where(df[i] < LL , LL, df[i]))
    return df.sample(5)



def outl_winsor(df, column, capping_method='iqr'):
    winsor = Winsorizer(capping_method=capping_method,
                        tail='both',
                        fold=1.5,
                        variables=[column])
    
    df[column] = winsor.fit_transform(df[[column]])
    return df.sample(5)



def outl_clip(df,columns):
    for column in columns:
        df[column] = df[column].clip(lower=df[column].quantile(0.05), upper=df[column].quantile(0.95))
    


def miss_repl(df, columns, type='mean'):
    for i in columns:
        if type == 'mean':
            value = df[i].mean()
        elif type == 'median':
            value = df[i].median()
        elif type == 'mode':
            value = df[i].mode()[0]  
        
        df[i] = df[i].replace(np.nan, value)
    return df.sample(5)



def miss_all(df):
    num_cols = df.select_dtypes(include=['float', 'int']).columns
    for x in num_cols:
        df[x] = df[x].fillna(df[x].mean())

    cat_cols = df.select_dtypes(include=['object']).columns
    for y in cat_cols:
        df[y] = df[y].fillna(df[y].mode()[0])

    



def norm(i):
    x = (i - i.min())/(i.max() - i.min())
    return x



def outlierColumns(df):
    outl_cols = []
    for i in df.columns:
        if pd.api.types.is_numeric_dtype(df[i]):
            IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
            LLi = df[i].quantile(0.25) - (1.5 * IQR)
            ULi = df[i].quantile(0.75) + (1.5 * IQR)
            
            if ((df[i] < LLi) | (df[i] > ULi)).sum() > 0:
                outl_cols.append(i)
    return outl_cols