import re
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import seaborn as sns

user_dict = {
    '@34669080231', 'Juan'
    '@24669851384', 'Alberto'
    '@34616651144', 'Ana'
    '@34633431579', 'Andrea'
    '@34655464779', 'Belen'
    '@34611147490', 'Dani'
    '@34647159195', 'Elena'
    '@34653422425', 'Ivan'
    '@34636075391', 'Juanan'
    '@34626681263', 'Nuria'
    '@34685344040', 'Paloma'
    '@34636613461', 'Lorena'
    '@34655964667', 'Monica'
    '@34674474322', 'Pilar'
    '@34678498054', 'Sergio'
    '@34638039395', 'Mari'
}

# Define a regular expression pattern to match the user, date, time, and message
pattern = r'\[(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2}:\d{2})] (.*?): (.*)'

# Define an empty list to store the messages
messages = []

# Open the file in read mode with UTF-8 encoding
with open('febrero.txt', 'r', encoding='utf-8') as file:
    # Read the contents of the file line by line
    for line in file:
        # Use the regular expression pattern to match the user, date, time, and message
        match = re.match(pattern, line)
        if match:
            # Extract the user, date, time, and message from the match object
            user = match.group(3)
            if user != 'EL GRUPO DE LAS CACAS':
                date = match.group(1)
                time = match.group(2)
                message = match.group(4)
                # Append the message to the list of messages
                messages.append({'user': user, 'date': date, 'time': time, 'message': message})

# Create a DataFrame from the list of messages
df = pd.DataFrame(messages)

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y')

# Convert the 'time' column to time format
df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time

# Convert the 'user' column to string format
df['user'] = df['user'].astype(str)
df['cagada'] = df['message'].str.contains('💩')
df['rojos'] = df['message'].str.contains('🔴')
df['verdes'] = df['message'].str.contains('🟢')
df['user'] = df['user'].str.split(' ').str[0].str.replace('~', '').str.replace(' ', '')

# Cuenta las veces que aparece cada usuario
value_counts = df['user'].value_counts()

# Filtrar los valores que aparecen menos de 5 veces
values_to_remove = value_counts[value_counts < 5].index

# Filtrar el DataFrame para eliminar las entradas con esos valores
df = df[~df['user'].isin(values_to_remove)]

# Group the DataFrame by month and user, and sum the messages
messages_by_month_user = df.groupby([df['date'].dt.month, 'user'])['cagada'].sum().sort_values(ascending=False)
reds_by_month_user = df.groupby([df['date'].dt.month, 'user'])['rojos'].sum()
greens_by_month_user = df.groupby([df['date'].dt.month, 'user'])['verdes'].sum()

# Get the unique months in the DataFrame, sorted in descending order
months = df['date'].dt.month.unique()
## DIC ##
#months[-1] = months[-1] + 12
#months.sort()

# Get the last 4 months
last_4_months = months[-5:-1]

# Get the unique users in the DataFrame
users = df['user'].unique()

# Define a custom color palette for the bars
colors = sns.color_palette("tab20", n_colors=len(users))

# Create a dictionary to map users to colors
user_colors = dict(zip(users, colors))

# Create a figure with a 3x2 grid layout
fig = plt.figure(figsize=(12, 7))
gs = GridSpec(3, 2)

# Loop through each of the last 4 months and create a bar graph for that month
for i, month in enumerate(last_4_months):
    # Get the messages for this month
    messages_this_month = messages_by_month_user.loc[month]

    # Create a subplot for this month
    ax = fig.add_subplot(gs[i // 2, i % 2])

    # Create a bar graph for this month, with the same color for each user
    bars = ax.bar(messages_this_month.index, messages_this_month, color=[user_colors[user] for user in messages_this_month.index])
    ax.set_title(f'Month {month}º')
    ax.set_ylabel('Total shits')
    ax.set_ylim(0, messages_by_month_user.max() * 1.1)
    ax.set_xticklabels(messages_this_month.index, rotation=45, ha='right')

    # Remove the grid
    ax.grid(False)

    # Add the number that each bar is representing to the bar graph
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')


## Get the last 6 months
#last_6_months = months[-7:-1]
#
## Create a subplot that spans the bottom two subplots
#ax = fig.add_subplot(gs[2:, :])
#
## Create a line graph for each user, with the same color for each user
#for user in users:
#    messages_this_user = messages_by_month_user.loc[:, user]
#    messages_this_user = messages_this_user.reindex(last_6_months, fill_value=0)
#    ax.plot(last_6_months, messages_this_user[last_6_months], label=user, color=user_colors[user], linestyle='--', marker='*', linewidth=1)
#
## Set the title and labels for the line graph
#ax.set_title('User shits for the last 6 months')
#ax.set_xlabel('Month')
#ax.set_ylabel('Shits by month')
#ax.set_ylim(0, messages_by_month_user.max() * 1.1)
#
## Set the x-ticks to the specific months you want
##ax.set_xticks(range(len(last_6_months)))
##ax.set_xticklabels(last_6_months)
#
## Add a legend to the line graph, outside of the graph
#ax.legend(title='Shitter', loc='upper left', bbox_to_anchor=(1, 1.5))


fig.subplots_adjust(hspace=0.5, wspace=0.3)

# Show the plot
plt.show()

print(df)

