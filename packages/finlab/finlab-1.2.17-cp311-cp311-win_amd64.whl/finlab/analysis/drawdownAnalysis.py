import pandas as pd
from finlab.analysis import Analysis
from finlab.ffn_core import drawdown_details


class DrawdownAnalysis(Analysis):

    @staticmethod
    def drawdown(series):
        drawdown = series.to_drawdown_series()
        drawdown_obj = {
                'values': drawdown.values.tolist(),
                'index': drawdown.index.values.tolist()
                }

        drawdown_result = drawdown_details(drawdown)

        if drawdown_result is None:
            drawdown_result = pd.DataFrame(columns=("Start", "End", "Length", "drawdown"))
        
        details = (drawdown_result
            .assign(Start=lambda df: df.Start.astype(str).str.split(' ').str[0])
            .assign(End=lambda df: df.Start.astype(str).str.split(' ').str[0])
            .set_index('Start')
            )

        longest_drawdown_details = (details
            .sort_values('Length')
            .tail(5)
            .to_dict('index'))

        max_drawdown_details = (details
            .sort_values('drawdown')
            .head(5)
            .to_dict('index'))

        return {'drawdown': drawdown_obj, 'longest_drawdown': longest_drawdown_details, 
                'largest_drawdown':max_drawdown_details}

    def analyze(self, report):
        return {
            'strategy': self.drawdown(report.daily_creturn),
            'benchmark': self.drawdown(report.daily_benchmark)
        }
