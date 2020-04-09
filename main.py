import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from helper import ax_points, custom_axes, plot_inset, imscatter
from matplotlib.projections import get_projection_class
from collections import Counter

plt.style.use("custom_style.mplstyle") ##mplstylesheet for background color, and font family
fig, ax, ax1, aux_ax1 = custom_axes()

"""
fig - figure
ax - the polar axis ax
ax1 - is the floating cartesian axis
aux_ax1 - auxilaary floating cartesian axis - this is the one we'll use to plot the 'table' and the legend
"""



##Dictionaries to replace and map values on the dataframe and during plotting
situations_dict = {'OpenPlay':'o',
                   'DirectFreekick':'x',
                   'Penalty':'s'}

results_dict = {'MissedShots':'#fe0000',
                'Goal':'#24b5d6',
                'SavedShot': '#ed9600'}

new_results_dict ={"Scored":"#24b5d6",
                   "Missed":"#fe0000",
                   "Saved":"#ed9600"}

col_dict = {"situation": "Situation",
            "Goal":"Scored",
            "MissedShots":"Missed",
            "SavedShot":"Saved"}

ind_dict = {"DirectFreekick": "Freekick",
            "OpenPlay":"Open Play",
            "Penalty":"Penalty"}



player = "Lionel Messi"
your_name = "Abhishek Sharma"

ax.set_ylim([-5, 35]) 
ax.set_yticklabels(labels = ["", "", 5, 10, 15, 20, 25, 30])
ax.tick_params(axis='y', which='both', labelsize=8)

ax.xaxis.grid(True, color='white', linestyle='-.')
ax.yaxis.grid(True)
ax.spines["polar"].set_alpha(0.0)
ax1.patch.set(visible=False)
####
##----Data-wrangling----
####
df = pd.read_csv("https://raw.githubusercontent.com/sharmaabhishekk/undershot_backup/master/understat_all_shots.csv",
                 usecols=["X", "player", "season", "result", "situation"])
results = ['MissedShots', 'Goal', 'SavedShot']
situations = ['OpenPlay', 'DirectFreekick', 'Penalty']
df = df.query("(player == @player) & (situation in @situations) & (result in @results) ")
df["x_metres"] = (1-df.X)*109.7 ## the X is in range(0, 1) and we'll transform to metres on a 109.7 x 73.15 dimension pitch
df["x_metres"] = df["x_metres"].round() ##round to one decimal place

grouped_player_df = df.groupby(["result", "situation"]).size().reset_index()
b = grouped_player_df.pivot(index='situation', columns='result', values=0).reset_index()
b.index = b.situation
b = b.rename(columns = col_dict, index=ind_dict)
b = b[["Scored", "Missed", "Saved"]]
    
n_seasons, = df.season.unique().shape ##Get number of seasons
y_ticks = np.linspace(25, 295, n_seasons+1)
ax.set_thetagrids(angles=y_ticks, labels=[""]*len(y_ticks))

####
##----Plotting----
####

for num, season in enumerate(sorted(df.season.unique())):
    pdf = df.query("season == @season")
    x_dict = Counter(pdf["x_metres"])

    mean = np.radians( (y_ticks[num] + y_ticks[num+1])/2 )
    ax.text(x=mean, y=31.5, s=f"{season}", rotation= np.degrees(mean)-90, va="center", ha="center", fontweight="bold", size=12, alpha=0.4, zorder=2) ##plot season
    for key, value in x_dict.items():
        xs = ax_points(N=value, mean=mean, step=0.1)
        queried = pdf.query("x_metres == @key")
        grouped = queried.groupby(['result','situation']).size().reset_index().rename(columns={0:'counts'})
        x_index = 0

        for i in grouped.index:
            for j in range(grouped.loc[i, "counts"]):
                ax.scatter(x = xs[x_index],
                           y=key,
                           marker = situations_dict[grouped.loc[i, "situation"]],
                           color=results_dict[grouped.loc[i, "result"]],
                           s=12,
                           alpha=0.9)
                x_index+=1
        assert grouped.counts.sum() == value == x_index ##check for any missed values

##### Get data in a proper format for plotting 'table'
        
col = b.columns.to_list()
col.insert(0, " ")
vals = []
for ind, row in zip(b.index, b.values.tolist()):
    row.insert(0, ind)
    vals.append(row)
vals.insert(0, col)

"""
Plotting tables in floating axes is surprisingly difficult. Pyplot table doesn't respect the rotation of the floating axis.
To work around that, I used ax.text in a nested loop. 
"""

for i, row in enumerate(vals[::-1]):
    for j, cell in enumerate(row):
        aux_ax1.text(x=j,
                     y=(i+4)/2,
                     s=cell,
                     rotation=25,
                     size=10,
                     color = "white" if cell not in ["Scored", "Missed", "Saved"] else new_results_dict[cell],
                     fontweight = "bold" if type(cell) == str else None
                     )

##Adding figure information and plotting the logo, and key grid and 
fig.text(0.86, 0.601, "metres\nfrom goal", size=8, rotation=25, color="white", va="bottom")
imscatter(0, 4, "images/messi_cropped.png", aux_ax1, zoom=0.3) ##plot image
fig.text(0.05, 0.9, "Profiling players\nacross Europe's top 5 leagues", ha="left", color="white", size=20, va="top", fontweight="bold")
fig.text(0.97, 0.9, f"\n{player} |2014-2018", ha="right", color="white", size=16, fontweight="bold", va="top")
fig.text(0.05, 0.12, f"By {your_name} |Inspired by Peter McKeever", va="center", color="white", size=10)


aux_ax1.text(2, 1.6, "Key", fontweight="bold", size=12, ha="center", va="center")
ax_sub = plot_inset(2, 0.6, aux_ax1, 1.4, color="white") ##plot key plot

for axis in ax1.axis.values():
    axis.line.set(visible=False)
    axis.major_ticks.set(visible=False)
    axis.major_ticklabels.set(visible=False)
aux_ax1.plot([.6, 3.6], [3.3, 3.3], linestyle="dotted", color="white") ##line between column headers and values

fig.savefig(f"images/{player}_shots.png", dpi=350)
plt.show()
