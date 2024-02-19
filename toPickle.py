import pandas as pd
import plotly.express as px
import streamlit as st
import pickle

out = {}

# Chart 1
f = pd.read_excel('K5.qmatrix.xlsx',skiprows=[0],header=None,index_col=0)
f.columns = [f"Value{n}" for n in range(len(f.columns))]
clusters = list(f.columns)
f = f.sort_values(by=clusters, ascending=False)
f['Sample'] = f.index
df = pd.wide_to_long(f, ['Value'], i='Sample', j='Cluster')
df = df.reset_index()
chart = px.area(
        df,
        x='Sample',
        y='Value',
        color='Cluster',
        line_shape='spline',
        template='simple_white',
        hover_data = ['Cluster', 'Value']
        )
out['chart1'] = chart

# Chart 2
pattern = pd.read_table('g_shape_color.xls', names=['group', 'sample', 'pattern', 'color'])
vector = pd.read_excel('pca.eigenvector.xlsx')
merge = pd.merge(vector, pattern, on='sample', how='left')
merge['Group'] = merge['group'].fillna('Unknown')

info = pd.read_excel('pca.eigenvalue.xlsx')
dic = dict(zip(info['PCs'], info['variance_explained']))

chart2 = px.scatter(
        merge,
        x='PC1',
        y='PC2',
        color='Group',
    )
out['chart2'] = chart2

# output
with open('test.pkl', 'wb') as f:
    f.write(pickle.dumps(out))
