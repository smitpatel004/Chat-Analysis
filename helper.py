
from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def fetch_stats(selectd_user, df):
    # For "overall" case, calculate stats for all users
    if selectd_user == "overall":
        num_messages = df.shape[0]
        words = []
        for message in df['message']:
            words.extend(message.split())
        num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
        
        # Extracting all links from the messages
        links = []
        for message in df['message']:
            links.extend(extractor.find_urls(message))
        
        return num_messages, len(words), num_media_messages, len(links)
    
    else:
        # For specific user
        new_df = df[df['user'] == selectd_user]
        num_messages = new_df.shape[0]
        words = []
        for message in new_df['message']:
            words.extend(message.split())
        num_media_messages = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]
        
        # Extracting links for the specific user
        links = []
        for message in new_df['message']:
            links.extend(extractor.find_urls(message))
    
        
        return num_messages, len(words), num_media_messages, len(links)
    

def most_busy_user(df):
    if 'user' not in df.columns:
        raise ValueError("The DataFrame does not have a 'user' column.")
    
    # Get the top 5 most frequent users
    x = df['user'].value_counts().head()
    
    # Calculate the percentage of messages for each user
    percent_df = (df['user'].value_counts(normalize=True) * 100).round(2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'}
    )
    
    return x, percent_df


def create_wordcloud(selected_user,df):
    if selected_user != "overall":
        df = df[df['user']==selected_user]
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white') 
    df_wc =wc.generate(df['message'].str.cat(sep=" ")) 
    return df_wc  

def most_common_words(selected_user,df):
    f= open('stop_hinglish.txt','r')
    stop_words=f.read( )
    if selected_user != 'overall':
        df = df[df['user']==selected_user]
    temp = df[df['user']!='group_notification']
    temp=temp[temp['message']!='Media omitted\n']
    words =[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))            
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != "overall":
        df = df[df['user']==selected_user]
    emojis = []
    for message in df['message']:
     emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))) 
    return emoji_df
    
def monthly_timeline(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

