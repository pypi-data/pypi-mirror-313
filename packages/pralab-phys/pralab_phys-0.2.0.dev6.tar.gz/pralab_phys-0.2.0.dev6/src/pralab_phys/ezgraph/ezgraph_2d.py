import plotly.graph_objects as go

class EZGraph(go.Figure):

    def __init__(
        self, 
        dispname:str = "",
        xax_title:str = "",
        yax_title:str = "",
        width:int = 900, 
        height:int = 600,
        namedisplay:bool = True,
    ):
        super().__init__()

        # plotly側の設定により、最初にアンダーバーを入れないとエラーを吐く
        # 修正を要検討
        self._dispname = dispname

        if not namedisplay:
            self._dispname = ""

        self.update_layout(
            title = dict(text = "<b>" + self._dispname, font = dict(size=22, color='gray'), y = 0.95),
            legend=dict(xanchor='left', yanchor='bottom', x=0.02, y=0.82),
            width=width, 
            height=height,
            xaxis=dict(title = xax_title),
            yaxis=dict(title = yax_title),
            plot_bgcolor='white')

        self.update_xaxes(
            showline=True,
            linewidth=2, mirror= True, tickfont_size = 20, title_font=dict(size=24), color='black',
            linecolor='grey',
            ticks='inside',
            ticklen=5,
            tickwidth=2,
            tickcolor='grey'
            )

        self.update_yaxes(
            showline=True,
            linewidth=2, mirror= True, tickfont_size = 20, title_font=dict(size=24), color='black',
            linecolor='grey',
            ticks='inside',
            ticklen=5,
            tickwidth=2,
            tickcolor='grey'
            )
    
    def add_graph(self, xdata, ydata, name = "", mode = "lines+markers", color = None):
        self.add_trace(
            go.Scatter(x=xdata, y=ydata, mode=mode, name=name, 
                marker=dict(size=5, color=color), line=dict(width=3, color=color)
                )
            )

    def logx(self):
        self.update_xaxes(type="log")
    
    def logy(self): 
        self.update_yaxes(type="log")

    def legand_loc(self, x = 1.02, y = 1):
        self.update_layout(legend=dict(x=x, y=y))

    def title_loc(self, y:float = 0.95):
        self.update_layout(title = dict(y=y))
    
    def print_methods(self):
        print([method for method in dir(self) if callable(getattr(self, method)) and not method.startswith("__")])