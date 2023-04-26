import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Video:
    """Реализация класса получение информации по id видео"""
    def __init__(self, video_id):
        """ метод  init, получает для класса id видео + определение переменных класса"""
        self.video_id = video_id
        api_key: str = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id
                                                    ).execute()
            self.title: str = video_response['items'][0]['snippet']['title']  # название видео
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']  # количество просмотров
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']  # количество лайков
            self.comment_count: int = video_response['items'][0]['statistics'][
                'commentCount']  # количество комментариев
            self.url_video = f"https://www.youtube.com/channel/{self.video_id}"  # адрес видео


        except (HttpError, IndexError):
            print(f'Error ID Video: ')
            self.title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None
            self.url_video = None

    def __str__(self):
        """реализация сетода str"""
        return f"{self.title}"


class PLVideo(Video):
    """Класс потомок от Video, принимает который принимает 'id видео' и 'id плейлиста"""
    def __init__(self, video_id, playlist_id: str):
        """метод  init, получает для класса id видео + id плейлиста + определение переменных класса, дополнение стандартного init родителя"""
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
