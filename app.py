import streamlit as st
# import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from helper import helper
from preprocessor import preprocessor

st.sidebar.title("whatsapp chat Analyser")
upload_file = st.sidebar.file_uploader("choose a file")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    user_list=df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"overall")
    selectd_user=st.sidebar.selectbox("show analysis wrt",user_list)
    

    if st.sidebar.button("show Analysis"):
        num_messages,words,num_media_messages,num_links =helper.fetch_stats(selectd_user,df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)    
        with col3:
            st.header("media message")
            st.title(num_media_messages) 
        with col4:
            st.header("number links")
            st.title(num_links)   
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selectd_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selectd_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selectd_user,df)
            # busy_day = helper.week_activity_map(selectd_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selectd_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selectd_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        if selectd_user == "overall":
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_user(df)
            
            fig , ax =plt.subplots()
            
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index ,x.values)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)   

        df_wc =helper.create_wordcloud(selectd_user,df)  
        fig , ax =plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)     

        most_common_df=helper.most_common_words(selectd_user,df)   
        fig,ax =plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        st.dataframe(most_common_df)

        emoji_df= helper.emoji_helper(selectd_user,df)
        st.title("EMOJI ANALYSIS")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)

    