from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_formatted"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_formatted"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")
cds = ColumnDataSource(df)

fig = figure(x_axis_type='datetime', height=500, width=800,
             title="Motion detector graph", align='center')
fig.yaxis.minor_tick_line_color = None
fig.ygrid[0].ticker.desired_num_ticks = 1
hover = HoverTool(tooltips=[("Start ", "@Start_formatted"),
                            ("End ", "@End_formatted")])
fig.add_tools(hover)
q = fig.quad(left="Start", right="End", bottom=0, top=1, color="cyan",
             source=cds)
output_file("graph.html")
show(fig)
