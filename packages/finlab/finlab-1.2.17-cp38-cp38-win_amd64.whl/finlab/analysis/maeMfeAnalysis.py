import numpy as np
import pandas as pd
from finlab.analysis import Analysis


class MaeMfeAnalysis(Analysis):

    def __init__(self, violinmode='group', mfe_scatter_x='mae', **kwargs):
        self.violinmode = violinmode
        self.mfe_scatter_x = mfe_scatter_x
        self.kwargs = kwargs

    @staticmethod
    def calc_edge_ratio(report):
        mae_mfe = report.mae_mfe
        mae_mfe_window_col = [i for i in list(set(mae_mfe.columns.get_level_values(0))) if
                              ('exit' not in str(i)) and (i != 0)]

        if len(mae_mfe_window_col) == 0:
            edge_ratio = pd.DataFrame({'time_scale': [1], 'mean_edge_ratio': [1]})

        else:
            edge_ratio = pd.DataFrame(
                [{'time_scale': m, 
                  'mean_edge_ratio': (
                      (mae_mfe[m]['gmfe']).sum()) / (abs(mae_mfe[m]['mae']).sum())} 
                        for m in mae_mfe_window_col])
        return edge_ratio

    def analyze(self, report):
        self.report = report

        ret_dist = {}
        for col in ['return', 'mae', 'bmfe', 'gmfe', 'mdd', 'pdays']:

            # profit and loss
            sp = report.trades[col].loc[report.trades['return'] > 0].dropna()
            hist_p = pd.DataFrame(np.histogram(sp, bins=20)).T.set_index(1).squeeze().fillna(0)

            sl = report.trades[col].loc[report.trades['return'] < 0].dropna()
            hist_l = pd.DataFrame(np.histogram(sl, bins=20)).T.set_index(1).squeeze().fillna(0)

            ret_dist[col] = {
                'p_values': hist_p.values.tolist(),
                'p_index': hist_p.index.values.tolist(),
                'p_stats': sp.describe().to_dict(),
                'l_values': hist_l.values.tolist(),
                'l_index': hist_l.index.values.tolist(),
                'l_stats': sl.describe().to_dict()
                }

        ret = {
            'stats': ret_dist,
            'edge_ratio': self.calc_edge_ratio(report).to_dict(orient='list')
        }

        return ret

    def display(self):
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        import plotly.figure_factory as ff

        violinmode = self.violinmode
        mfe_scatter_x = self.mfe_scatter_x
        kwargs = self.kwargs
        report = self.report
        stats = report.get_stats()
        trade_record = report.get_trades().copy().dropna(
                subset=['mae', 'mdd', 'bmfe', 'gmfe', 'pdays', 'return'])
        trade_record['entry_date'] = trade_record['entry_date'].dt.strftime('%Y-%m-%d')
        trade_record.loc[:, ['return']] = round(trade_record[['return']] * 100, 2)
        trade_record.loc[:, ['pdays_ratio']] = trade_record['pdays'] / trade_record['period']
        trade_record.loc[:, ['mae', 'mdd', 'bmfe', 'gmfe', 'pdays_ratio'], ] = round(
            abs(trade_record[['mae', 'mdd', 'bmfe', 'gmfe', 'pdays_ratio']] * 100), 2)
        trade_record.loc[:, ['profit_loss']] = trade_record['return'].apply(lambda s: 'profit' if s > 0 else 'loss')
        trade_record.loc[:, ['size']] = abs(trade_record['return'])
        win_ratio = round(stats['win_ratio']*100, 1)
        stats = {g[0]: g[1].describe().to_dict() for g in trade_record.groupby('profit_loss')}

        # calculate edge_ratio
        mae_mfe = report.mae_mfe
        mae_mfe_window_col = [i for i in list(set(mae_mfe.columns.get_level_values(0))) if
                              ('exit' not in str(i)) and (i != 0)]
        if len(mae_mfe_window_col) == 0:
            edge_ratio = pd.DataFrame({'time_scale': [1], 'mean_edge_ratio': [1]})
        else:
            edge_ratio = pd.DataFrame(
                [{'time_scale': m, 
                  'mean_edge_ratio': (
                      (mae_mfe[m]['gmfe']).sum()) / (abs(mae_mfe[m]['mae']).sum())} 
                        for m in mae_mfe_window_col]).sort_values(['time_scale'])

        # mdd_gmfe:use for trailing stop
        mdd_gmfe = trade_record[(trade_record['mdd'] > trade_record['gmfe'])]
        pl_count = trade_record.groupby(['profit_loss'])['mdd'].count()
        breakeven_safe_pct = abs(round((len(mdd_gmfe) / len(trade_record) - 1) * 100))
        missed_profits_pct = round(len(mdd_gmfe[mdd_gmfe['profit_loss'] == 'profit']) / pl_count['profit'] * 100)

        # plot
        fig = make_subplots(rows=4, cols=6,
                            specs=[[{"colspan": 2}, None, {"colspan": 2}, None, {"colspan": 2}, None],
                                   [{"colspan": 2}, None, {"colspan": 2}, None, {"colspan": 2}, None],
                                   [{"colspan": 2}, None, {"colspan": 2}, None, {"colspan": 2}, None],
                                   [{"colspan": 6}, None, None, None, None, None], ],
                            vertical_spacing=0.1,
                            horizontal_spacing=0.1,
                            subplot_titles=[f"Win Ratio:{win_ratio}%", "Edge Ratio", "MAE/Return",
                                            f"GMFE/{mfe_scatter_x.capitalize()}", f"BMFE/{mfe_scatter_x.capitalize()}",
                                            f"Missed Win-profits PCT:{missed_profits_pct}%<br>Breakeven Safe PCT:{breakeven_safe_pct}%",
                                            "MAE Distribution", "BMFE Distribution", "GMFE Distribution",
                                            "Indices Stats"])

        colors = {'profit': '#69b0ea', 'loss': '#F66095'}

        def set_fig_data_color(fig_data, color_set=colors):
            fig_data['marker']['color'] = color_set.get(fig_data['legendgroup'], colors['loss'])
            return fig_data

        # Return histogram
        fig_return_hist = px.histogram(trade_record, x="return", color="profit_loss")
        for f_data in fig_return_hist.data:
            fig.add_trace(set_fig_data_color(f_data), row=1, col=1)

        return_mean = round(trade_record['return'].mean(), 2)
        fig.add_vline(x=return_mean, line_width=2, line_dash="dash", line_color="green",
                      annotation_position="top right",
                      annotation_text=f'  avg:{return_mean}%',
                      row=1, col=1)

        # "Edge Ratio"
        fig_edge_ratio = px.line(edge_ratio, x='time_scale', y='mean_edge_ratio')
        for f_data in fig_edge_ratio.data:
            fig.add_trace(set_fig_data_color(f_data), row=1, col=3)

        # MAE/Return
        px_fig = px.scatter(trade_record, x="return", y="mae", color="profit_loss",
                            size='size', hover_data=['stock_id', 'entry_date'])
        for f_data in px_fig.data:
            fig.add_trace(set_fig_data_color(f_data), row=1, col=5)
        for pl, color in colors.items():
            y = stats[pl]['mae']['75%']
            fig.add_hline(y=y, line_width=2, line_dash="dash", annotation_text=f' Q3:{round(y, 2)}%', line_color=color,
                          row=1, col=5)

        # GMFE/MAE,BMFE/MAE
        for name, col in zip(['gmfe', 'bmfe'], [1, 3]):
            px_fig = px.scatter(trade_record, x=mfe_scatter_x, y=name, color="profit_loss",
                                size='size', hover_data=['stock_id', 'entry_date'])
            for f_data in px_fig.data:
                fig.add_trace(set_fig_data_color(f_data), row=2, col=col)
            for pl, color in colors.items():
                y = stats[pl][name]['75%']
                fig.add_hline(y=y, line_width=2, line_dash="dash", annotation_text=f' Q3:{round(y, 2)}%', line_color=color,
                              row=2, col=col)

        # MDD/GMFE
        px_fig = px.scatter(trade_record, x="gmfe", y="mdd", color="profit_loss",
                            size='size', hover_data=['stock_id', 'entry_date'])
        for f_data in px_fig.data:
            fig.add_trace(set_fig_data_color(f_data), row=2, col=5)

        # MDD/GMFE benchmark
        max_gmfe = trade_record['gmfe'].max()
        fig.add_trace(go.Scatter(x=[0, max_gmfe * 1.1], y=[0, max_gmfe * 1.01],
                                 mode='lines', name='mdd/mfe_benchmark', line_color="orange", line_width=3), row=2, col=5)
        # distributions
        group_labels = list(colors.keys())

        def create_distplot_data(index='mae'):
            hist_data = [trade_record[(trade_record['profit_loss'] == g)][index].values for g in
                         group_labels]
            distplot = ff.create_distplot(hist_data, group_labels, bin_size=1)
            return distplot['data']

        for name, col in zip(['mae', 'bmfe', 'gmfe'], [1, 3, 5]):
            plot = create_distplot_data(name)
            for data_num in range(0, 2):
                fig.add_trace(go.Histogram(plot[data_num],
                                           marker_color=colors[group_labels[data_num % 2]]
                                           ), row=3, col=col)
                fig.add_trace(go.Scatter(plot[data_num + 2],
                                         line=dict(color=colors[group_labels[data_num % 2]], width=3)
                                         ), row=3, col=col)
            for pl, color in colors.items():
                x = stats[pl][name]['75%']
                fig.add_vline(x=x, annotation=dict(text=f' Q3:{round(x, 2)}%', textangle=-90), line_width=2,
                              line_dash="dash",
                              line_color=color, row=3, col=col)

        violin_columns = ['return', 'mae', 'bmfe', 'gmfe', 'mdd', 'pdays_ratio']
        tr_melt_df = pd.melt(trade_record, id_vars=['entry_sig_date', 'exit_sig_date', 'stock_id', 'profit_loss'],
                             value_vars=violin_columns)

        if violinmode == 'overlay':
            for v in violin_columns:
                fig.add_trace(go.Violin(x=tr_melt_df['variable'][tr_melt_df['variable'] == v],
                                        y=tr_melt_df['value'][tr_melt_df['variable'] == v],
                                        name=v, box_visible=True, meanline_visible=True), row=4, col=1)
        elif violinmode == 'group':
            for group, color in colors.items():
                fig.add_trace(go.Violin(x=tr_melt_df['variable'][tr_melt_df['profit_loss'] == group],
                                        y=tr_melt_df['value'][tr_melt_df['profit_loss'] == group], line_color=color,
                                        legendgroup=group, scalegroup=group, name=group, box_visible=False,
                                        meanline_visible=True,
                                        opacity=0.6), row=4, col=1
                              )

        fig.update_layout(
            height=1200, width=1200,
            title={
                'text': "MAE/MFE Analysis",
                'x': 0.46,
                'y': 0.98,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            violinmode=violinmode,
            yaxis=dict(
                title='count',
            ),
            yaxis2=dict(
                title='edge ratio',
                showgrid=False,
            ),
            yaxis3=dict(
                title='mae(%)',
            ),
            yaxis4=dict(
                title='gmfe(%)',
            ),
            yaxis5=dict(
                title='bmfe(%)',
            ),
            yaxis6=dict(
                title='mdd(%)',
            ),
            xaxis=dict(
                title='return(%)',
            ),
            xaxis2=dict(
                title='time_scale',
            ),
            xaxis3=dict(
                title='return(%)',
            ),
            xaxis4=dict(
                title=f'{mfe_scatter_x}(%)',
            ),
            xaxis5=dict(
                title=f'{mfe_scatter_x}(%)',
            ),
            xaxis6=dict(
                title='gmfe(%)',
            ),
            xaxis7=dict(
                title='mae(%)',
            ),
            xaxis8=dict(
                title='bmfe(%)',
            ),
            xaxis9=dict(
                title='gmfe(%)',
            ),
            **kwargs
        )
        return fig

