import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data 
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Create a draw_line_plot function that uses Matplotlib to draw a line chart similar to "examples/Figure_1.png".
    fig = plt.figure(figsize=(24, 8))
    plt.plot('date', 'value', data=df)
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")

    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Create a draw_bar_plot function that draws a bar chart similar to "examples/Figure_2.png".
    df_bar = df.copy()
    df_bar['year'] = df['date'].dt.year
    df_bar['month'] = df['date'].dt.month_name()
    df_bar = df_bar.groupby(['year', 'month']).agg('mean').reset_index()

    # Draw bar plot
    months_list = pd.date_range(start="2024-01-01", end="2024-12-01", freq="MS").strftime('%B').tolist()
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months_list, ordered=True)
    df_bar = df_bar.sort_values('month').reset_index(drop=True)
    df_bar.set_index(["year", "month"], inplace=True)
    fig = df_bar['value'].unstack(level=1).plot(kind ="bar", figsize=(9,6)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', loc='upper left')

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    months_list = pd.date_range(start="2024-01-01", end="2024-12-01", freq="MS").strftime('%b').tolist()

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(16, 4))
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0], palette='tab10')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], palette='husl',order=months_list)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig
    fig.tight_layout()
    fig.savefig('box_plot.png')
    return fig
    