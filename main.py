import googleapiclient.discovery

class YouTubeAPI:
    def __init__(self,developer_key):
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.developer_key  = developer_key 
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, developerKey=self.developer_key
        )

    def combine_keywords(search_keys):
        # Combines search keywords with double quotes and OR operator.
        
        combined_query = '|'.join(f'"{keyword}"' for keyword in search_keys)
        return combined_query
    
    def search_videos(self, search_keys, pageToken=None):
        combined_query = self.combine_keywords(search_keys)
        request = self.youtube.search().list(
            part="id,snippet",
            type='video',
            q=combined_query,
            maxResults=10,
            regionCode="AZ",
            pageToken=pageToken,
            fields="nextPageToken,pageInfo,items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))"
        )
        response = request.execute()
        for item in response['items']:
            video_id = item['id']['videoId']
            item['statistics'] = self.get_video_statistics(video_id)
            item['keywords'] = self.find_keywords_in_description(search_keys, item)
        return response

    def get_video_statistics(self, video_id):
        request = self.youtube.videos().list(
            part="statistics,contentDetails",
            id=video_id,
            fields="items(statistics)"
        )
        response = request.execute()
        return response['items'][0]['statistics']

    def find_keywords_in_description(self, search_keys, item):
        keywords = list()
        for keyword in search_keys:
            if (
                keyword in item['snippet']['title']
                or keyword in item['snippet']['channelTitle']
                or keyword in item['snippet']['description']
            ):
                keywords.append(keyword)
        return keywords
    
if __name__ == "__main__":
    DEVELOPER_KEY = "YOUR_DEVELOPER_KEY"
    search_keys = ["keyword1", "keyword2"]

    youtube_api = YouTubeAPI(DEVELOPER_KEY)
    search_result = youtube_api.search_videos(search_keys)
    print(search_result)


