import streamlit as st
from streamlit_option_menu import option_menu
from googleapiclient.discovery import build
import requests
import time
from annotated_text import annotated_text
import re
import pandas as pd
import seaborn as sns
import numpy as np
# from selenium import webdriver
# from selenium.webdriver.common.by import By




api_key = 'AIzaSyAmikuiuKlm6th6U2-0wKhHDI1VK9ZeZYY'
youtube = build('youtube', 'v3', developerKey=api_key)
st.set_page_config(page_title="TubeStack ", page_icon=":zap:", layout="wide")
hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("TUBESTACK TOOLS")


seleted = option_menu(
    menu_title="Best Tools For Content Creators",
    options=["Competitor Analysis", "Top Rated Keywords", "Top Description Tags",
             "Video Engagement Checker"],
    default_index=0,
    orientation="horizontal",
)



#############################   Tool Number 1   ##################################

if seleted == "Competitor Analysis":
    st.title("Find Top Competitors For Any Topic On YouTube 🔥")
    st.write("\n")
    st.text("➡️ This tool provides the complete analysis of the searched topic on youtube which helps you to identify your competitors and their strategies.")
    st.text("    So, you can determine your strengths and weaknesses in optimizing your video content!")

    url = 'http://suggestqueries.google.com/complete/search?client=youtube&ds=yt&client=chrome'
    query = \
        st.text_input('Enter Keyword to check top competitors of top Keywords ⬇️'
                      )
    r = requests.get(url, params={"q": query})
    top_keywords = r.json()[1]
    

    def youtubeSearch(youtube, top_keywords, order="relevance"):

        for i in range(len(top_keywords)):
            search_request = youtube.search().list(
                q=top_keywords[i],
                type="video",
                order=order,
                part="id,snippet",
                maxResults=10,
            )
            search_response = search_request.execute()

            video_ids = []
            for items in search_response['items']:
                video_ids.append(items['id']['videoId'])

            vid_request = youtube.videos().list(
                part='statistics, snippet',
                id=','.join(video_ids)
            )

            vid_response = vid_request.execute()

            all_video_stats = []
            for items in vid_response['items']:
                video_title = items['snippet']['title']
                channel_title = items['snippet']['channelTitle']
                view_count = items['statistics']['viewCount']

                try:
                    like_count = items['statistics']['likeCount']
                except:
                    # Good to be aware of Channels that turn off their Likes
                    # print("Video titled {0}, on Channel {1} Likes Count is not available".format(items['snippet']['title'],
                    #                                                                 items['snippet']['channelTitle']))
                    like_count = '0'

                if 'commentCount' in items['statistics'].keys():
                    comment_count = items['statistics']['commentCount']
                else:
                    comment_count = '0'

                if 'tags' in items['snippet'].keys():
                    video_tags = items['snippet']['tags']
                else:
                    video_tags = []

                all_video_stats.append(
                    {
                        'VideoTitle': video_title,
                        'ChannelName': channel_title,
                        'Views': view_count,
                        'Likes': like_count,
                        'Comments': comment_count,
                        'Tags': video_tags,
                    }
                )

            video_data = pd.DataFrame(all_video_stats)
            video_data.index = np.arange(1, len(video_data)+1)

            st.write("\n")
            left_column, right_column = st.columns(2)
            with left_column:
                st.write('🌟 Top dominated Videos On This Keyword')
                key = str(top_keywords[i])
                st.subheader(f"({i+1}) {key.upper()}")
                st.write("\n")
                st.dataframe(video_data, height=1300, width=22222)
                csv = video_data.to_csv().encode('utf-8')
                st.download_button(
                    "Download CSV",
                    csv,
                    "file.csv",
                    "text/csv",
                    key='download csv'
                )

            video_data['Views'] = pd.to_numeric(video_data['Views'])
            video_data['Comments'] = pd.to_numeric(video_data['Comments'])
            video_data['Likes'] = pd.to_numeric(video_data['Likes'])
            with right_column:
                st.write('🌟 Top Dominated Channels On This Keyword')
                key = str(top_keywords[i])
                st.subheader(f"({i+1}) {key.upper()}")
                st.write("\n")
                sns.set(rc={'figure.figsize': (10, 4)})
                ax = sns.barplot(x='Views', y='ChannelName', data=video_data)
                st.pyplot(ax.get_figure())
                st.write("\n")
            st.write("\n")
            
    if(len(query) != 0):
        time.sleep(3)
        st.text("Here is the complete Competitor analysis of videos and channels on this Topic ⬇️")
        st.write("\n")
        st.write("\n")
        left_des, right_des = st.columns(2)
        with left_des:
            st.write("✔️ Following are the detailed information of top rated videos on most dominated keywords of your searched topic ")
        with right_des:
            st.write("✔️ Following are the detailed information of top rated channels on most dominated keywords of your searched topics ")
            
        response = youtubeSearch(youtube, top_keywords)
        print(response)

#############################   Tool Number 2   ##################################


if seleted == "Top Rated Keywords":
    st.title("Find Top Keywords For Your Topic 🔥")
    url = 'http://suggestqueries.google.com/complete/search?client=youtube&ds=yt&client=chrome'
    query = \
        st.text_input('Enter your desired topic to check top competitors of top Keywords ⬇️'
                      )
    r = requests.get(url, params={"q": query})
    top_keywords = r.json()[1]
    time.sleep(6)
    # st.subheader("🌟 Top High Volume Search Keywords")
    # st.write("\n")
    # st.text("➡️ Following are the effective related keywords for your chosen topic. Get more views on YouTube by researching keywords people are searching for! ")
    for i in range(len(top_keywords)):
        if(i == 0):
            st.subheader("🌟 Top High Volume Search Keywords")
            st.write("\n")
            st.text("➡️ Following are the effective related keywords for your chosen topic. Get more views on YouTube by researching keywords people are searching for! ")
            st.write("\n")
            st.write("\n")
        keyword = str(top_keywords[i])
        annotated_text(("⭐ " + keyword.upper(), str(i+1), "#535dc5"))
        st.write("\n")


#############################   Tool Number 3   ##################################


if seleted == "Top Description Tags":
    st.title("Find Top Description Tags For Your Videos 🔥")
    st.write("\n")
    st.text("➡️ Description And Title Tags Are Really Important To Optimize Your Youtube Videos on Youtube Search Algorithm to make the Rank Higher")

    qr = \
        st.text_input('Enter your desired topic to check top competitors of top Keywords ⬇️'
                      )

    def getDescriptionTags(youtube):

        max_results = 20

        search_request = youtube.search().list(
            q=qr,
            part='id,snippet',
            maxResults=max_results).execute()

        videosDf = pd.DataFrame(columns=['videoId', 'title', 'description',
                                'descriptionTags', 'tags', 'viewCount', 'likeCount', 'dislikeCount'])
        videosDf = videosDf.astype(object)

        for search_result in search_request.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videosDf = videosDf.append(
                    {'videoId': search_result['id']['videoId']}, ignore_index=True)

        for (_, row) in videosDf.iterrows():
            video_request = youtube.videos().list(
                part="snippet",
                id=row['videoId'])

            response = video_request.execute()

            videosDf.loc[videosDf.videoId == row['videoId'], ['description', 'title']] = \
                response['items'][0]['snippet'].get('description'), \
                response['items'][0]['snippet'].get('title')

        return extract_desc_tags(videosDf).to_json(orient="records")

    def extract_desc_tags(df):
        for (_, row) in df.iterrows():
            tempArr = []
            for match in re.findall(r"#(\w+)", row['description']):
                tempArr.append(match)
            for i in range(len(tempArr) - 4):
                cols = st.columns(4)
                cols[0].write("✔️ "+str(tempArr[i]))
                cols[1].write("✔️ "+str(tempArr[i+1]))
                cols[2].write("✔️ "+str(tempArr[i+2]))
                cols[3].write("✔️ "+str(tempArr[i+3]))
                # cols[4].write(str(i+5)+" "+str(tempArr[i+4]))
        if len(tempArr) == 0:
                st.text("No Description Tags Founnd On This Topic, Try another one!")
            

        return df

    if(len(qr) != 0):
        time.sleep(3)
        st.text("These Are The Most Effective Description Tags For Your Youtube Video")
        st.write("\n")
        st.write("\n")
        getDescriptionTags(youtube)




#############################   Tool Number 4   ##################################


if seleted == "Video Engagement Checker":
    st.title("Engagement Calculator For Tracking A Video's Performance 🔥")
    st.write("\n")
    st.text("➡️ No more tricky questions about how a YouTube video is performing. TubeStack Engagement Calculator is a practical tool to see how much your audience is")
    st.text("    engaged with a certain video. No sign up is required!")
    
    
    link = \
    st.text_input('YOUTUBE VIDEO LINK   (eg -> https://www.youtube.com/watch?******************* )'
                    )
    
    likesSuggest = ""
    commentsSuggest = ""
    
    def views_to_like_ratio(views, likes, likesSuggest):
        likes_score = 0
        ratio = (likes / views) * 100
        if ratio >= 5:
            likes_score += 48
            likesSuggest = "✔️ Your Video is Performing excellent on the basis of views to likes ratio!"
        elif ratio >= 4.6:
            likes_score += 43
            likesSuggest = "✔️ Your Video is Performing great on the basis of views to likes ratio!"
        elif ratio >= 4.1:
            likes_score += 39
            likesSuggest = "✔️ Your Video is Performing good on the basis of views to likes ratio!"
        elif ratio >= 3.7:
            likes_score += 33
            likesSuggest = "❎ On the basis of views to likes ratio, your Video is Performing just OK, can get better!"
        elif ratio >= 2.9:
            likes_score += 27
            likesSuggest = "❌ On the basis of views to likes ratio, your Video is Performing bad!"
        else:
            likes_score += 19
            likesSuggest = "❌ On the basis of views to likes ratio, your Video is Performing poor!"

        return likes_score, likesSuggest

    def views_to_comments_ratio(views, comments, commentsSuggest):
        comments_score = 0
        ratio = (comments / views) * 100
        if ratio >= 0.6:
            comments_score += 48
            commentsSuggest = "✔️ Your Video is Performing excellent on the basis of views to comment ratio!"
        elif ratio >= 0.55:
            comments_score += 43
            commentsSuggest = "✔️ Your Video is Performing great on the basis of views to comment ratio!"
        elif ratio >= 0.5:
            comments_score += 39
            commentsSuggest = "✔️ Your Video is Performing good on the basis of views to comment ratio!"
        elif ratio >= 0.45:
            comments_score += 33
            commentsSuggest = "❎ On the basis of views to comments ratio, your Video is Performing just OK, can get better!"
        elif ratio >= 0.4:
            comments_score += 27
            commentsSuggest = "❌ On the basis of views to comments ratio, your Video is Performing bad!"
        else:
            comments_score += 19
            commentsSuggest = "❌ On the basis of views to comments ratio, your Video is Performing poor!"

        return comments_score, commentsSuggest
    
    def engagementChecker(youtube):
        parsed = link.split("v=")
        Id = parsed[1]
        request = youtube.videos().list(part="snippet,contentDetails,statistics",id=Id)
        response = request.execute()

        title = response['items'][0]['snippet']['title']
        thumb = response['items'][0]['snippet']['thumbnails']['default']['url']
        views = int(response['items'][0]['statistics']['viewCount'])
        likes = int(response['items'][0]['statistics']['viewCount'])
        comments = int(response['items'][0]['statistics']['commentCount'])
        
        l_score, l_suggest = views_to_like_ratio(views, likes, likesSuggest)
        c_score, c_suggest = views_to_comments_ratio(views, comments, commentsSuggest)
        engagement_score = l_score + c_score
    
        st.title(f"Video Engagement score: {engagement_score} / 100")
        st.subheader(l_suggest)
        st.subheader(c_suggest)
    
    if(len(link) != 0):
        time.sleep(3)
        st.text("Here is the engagement score of your video ⬇️")
        st.write("\n")
        st.write("\n")
        response = engagementChecker(youtube)
        print(response)
        


#############################   Tool Number 5   ##################################

# if seleted == "Keyword Research":
#     options = webdriver.ChromeOptions()
#     options.headless = True
#     driver = webdriver.Chrome(options=options)


#     st.title("Keyword Research Tool") 
#     s_query = \
#         st.text_input('Enter keyword to find volume and difficulty level'
#                       )
#     search_url="https://h-supertools.com/youtube/youtube-keyword-tool?searchTerm={q}"

    
#     if len(s_query) != 0:
#         driver.get(search_url.format(q=s_query))
#         time.sleep(9)
#         table = driver.find_element(by=By.XPATH, value="//table[contains(@id,'keywordsTBL')]").get_attribute("outerHTML")
#         driver.execute_script("window.scrollTo(0,900)")
#         if table:
#             time.sleep(3)
#             df = pd.read_html(table)
#             merged = pd.concat(df)
#             merged.index = np.arange(1, len(merged)+1)
#             # merged = merged.iloc[: , :-1]
#             merged = pd.DataFrame(merged)
#             st.table(merged)
#             # print(merged)
#             driver.close()
    
