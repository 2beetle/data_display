import base64
import tempfile

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import pickle

params = st.query_params.to_dict()
presigned_url = params.get("pkl_url")
dic = None
if presigned_url:
    presigned_url = base64.b64decode(presigned_url).decode('utf-8')
    response = requests.get(presigned_url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(response.content)
            dic = pickle.load(open(fp.name, 'rb'))

def export(chart, fmt):
    return chart.to_image(format=fmt, scale=2)

if dic:
    st.set_page_config(layout='wide')
    # chart 1
    main_area, menu_area = st.columns([3, 1], gap='large')
    chart = dic['chart1']
    with menu_area:
        expo_tab, title_tab, legend_tab, axes_tab, color_tab = st.tabs(["导出", "标题", "图例", "坐标轴", "配色"])
        with expo_tab:
            export_format = st.selectbox('导出格式', ('svg', 'png', 'jpeg', 'pdf'))
            export_button = st.empty()
            st.divider()
        with title_tab:
            title_show = st.toggle('显示标题？', True)
            title_text = st.text_input('标题内容', 'Cluster')
            title_font = st.selectbox('标题字体', ('Source Han Sans CN', 'Source Han Serif SC'))
            title_size_col, title_color_col = st.columns([4, 1], gap='medium')
            with title_size_col:
                title_size = st.slider('标题大小', 10, 35, 20, 1, label_visibility='collapsed')
            with title_color_col:
                title_color = st.color_picker('标题颜色', label_visibility='collapsed')
            st.divider()
        with legend_tab:
            legend_show = st.toggle('显示图例？', True)
            legend_title_text = st.text_input('图例标题', 'Cluster')
            legend_font = st.selectbox('图例字体', ('Source Han Sans CN', 'Source Han Serif SC'))
            legend_size_col, legend_color_col = st.columns([5, 1], gap='medium')
            with legend_size_col:
                legend_size = st.slider('图例大小', 10, 20, 10, 1, label_visibility='collapsed')
            with legend_color_col:
                legend_color = st.color_picker('图例颜色', label_visibility='collapsed')
            st.divider()
        with axes_tab:
            xaxis_show = st.toggle('显示X轴标题？', True)
            xaxis_title = st.text_input('X轴标题', f'Sample')
            yaxis_show = st.toggle('显示Y轴标题？', True)
            yaxis_title = st.text_input('Y轴标题', f'Cluster proportion')
            axes_font = st.selectbox('坐标轴字体', ('Source Han Sans CN', 'Source Han Serif SC'))
            axes_size_col, axes_color_col = st.columns([5, 1], gap='medium')
            with axes_size_col:
                axes_size = st.slider('坐标轴大小', 10, 20, 13, 1, label_visibility='collapsed')
            with axes_color_col:
                axes_color = st.color_picker('坐标轴颜色', label_visibility='collapsed')
            axes_tickfont = st.selectbox('刻度字体', ('Source Han Sans CN', 'Source Han Serif SC'))
            axes_ticksize_col, axes_tickcolor_col = st.columns([5, 1], gap='medium')
            with axes_ticksize_col:
                axes_ticksize = st.slider('刻度大小', 10, 20, 10, 1, label_visibility='collapsed')
            with axes_tickcolor_col:
                axes_tickcolor = st.color_picker('刻度颜色', label_visibility='collapsed')
            st.divider()
        with color_tab:
            bg_color = st.color_picker('背景颜色', '#FFF')
            # theme = st.selectbox('配色模版', ('ggplot2', 'seaborn', 'simple_white', 'plotly',
            # 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
            # 'ygridoff', 'gridon', 'none'))
    with main_area:
        chart.update_layout(
            hovermode="x unified",
            selectdirection="h",
            barmode='stack',
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            title=dict(
                text=title_text,
                x=0.5,
                xanchor='auto',
                font=dict(family=title_font, size=title_size, color=title_color),
            ) if title_show else '',
            showlegend=legend_show,
            legend=dict(
                font=dict(family=legend_font, size=legend_size, color=legend_color),
                title=dict(text=legend_title_text, font=dict(family=legend_font, size=legend_size, color=legend_color)),
            ),
            # template=theme,
        )
        chart.update_xaxes(
            title=dict(
                text=xaxis_title,
                font=dict(family=axes_font, size=axes_size, color=axes_color),
            ) if xaxis_show else '',
            tickfont=dict(family=axes_tickfont, size=axes_ticksize, color=axes_tickcolor),
        )
        chart.update_yaxes(
            title=dict(
                text=yaxis_title,
                font=dict(family=axes_font, size=axes_size, color=axes_color),
            ) if yaxis_show else '',
            tickfont=dict(family=axes_tickfont, size=axes_ticksize, color=axes_tickcolor),
        )
        config = {
            'toImageButtonOptions': {'format': export_format, 'scale': 2},
            'displaylogo': False,
        }
        st.plotly_chart(chart, use_container_width=True, config=config)

    with export_button.container():
        st.download_button('导出', export(chart, export_format), f'export.{export_format}', type='primary',
                           use_container_width=True)
