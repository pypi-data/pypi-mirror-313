# import SDK Version
from tikhub import version

# http_client
from tikhub.http_client.api_client import APIClient

# TikHub
from tikhub.api.v1.endpoints.tikhub.tikhub_user import TikHubUser

# Douyin
from tikhub.api.v1.endpoints.douyin.web.douyin_web import DouyinWeb
from tikhub.api.v1.endpoints.douyin.app.douyin_app_v1 import DouyinAppV1
from tikhub.api.v1.endpoints.douyin.app.douyin_app_v2 import DouyinAppV2
from tikhub.api.v1.endpoints.douyin.app.douyin_app_v3 import DouyinAppV3

# TikTok
from tikhub.api.v1.endpoints.tiktok.web.tiktok_web import TikTokWeb
from tikhub.api.v1.endpoints.tiktok.app.tiktok_app_v2 import TikTokAppV2
from tikhub.api.v1.endpoints.tiktok.app.tiktok_app_v3 import TikTokAppV3

# Instagram
from tikhub.api.v1.endpoints.instagram.web.instagram_web import InstagramWeb

# Weibo
from tikhub.api.v1.endpoints.weibo.web.weibo_web import WeiboWeb

# Captcha Solver
from tikhub.api.v1.endpoints.captcha.captcha_solver import CaptchaSolver

# Xigua Video APP V2
from tikhub.api.v1.endpoints.xigua.app.xigua_app_v2 import XiguaAppV2

# XiaoHongShu Web
from tikhub.api.v1.endpoints.xiaohongshu.web.xiaohongshu_web import XiaohongshuWeb

# KuaiShou Web
from tikhub.api.v1.endpoints.kuaishou.web.kuaishou_web import KuaishouWeb

# YouTube Web
from tikhub.api.v1.endpoints.youtube.web.youtube_web import YouTubeWeb

# Net Ease Cloud Music
from tikhub.api.v1.endpoints.net_ease_cloud_music.app.net_ease_cloud_music_app_v1 import NetEaseCloudMusicAppV1

# Hybrid Parsing
from tikhub.api.v1.endpoints.hybrid_parsing.hybrid_parsing import HybridParsing

# Twitter Web
from tikhub.api.v1.endpoints.twitter.web.twitter_web import TwitterWeb


class Client:
    def __init__(self,
                 base_url: str = 'https://api.tikhub.io',
                 api_key: str = None,
                 proxy: str = None,
                 max_retries: int = 3,
                 max_connections: int = 50,
                 timeout: int = 60,
                 max_tasks: int = 50,
                 custom_user_agent: str = None,
                 ):
        # Base URL
        self.base_url = base_url

        # API Key
        self.api_key = api_key
        if not self.api_key:
            raise RuntimeError("API Key is required to use the SDK. | 需要API Key才能使用SDK。")

        # Version
        self.version = str(version)

        # API Client
        self.client = APIClient(
            base_url=self.base_url,
            client_headers={
                "User-Agent": f"TikHub-API-SDK-Python/{self.version}" if not custom_user_agent else custom_user_agent,
                "X-SDK-Version": f"{self.version}",
                "Authorization": f"Bearer {self.api_key}"
            },
            proxy=proxy,
            max_retries=max_retries,
            max_connections=max_connections,
            timeout=timeout,
            max_tasks=max_tasks
        )

        # TikHub
        self.TikHubUser = TikHubUser(self.client)

        # Douyin
        self.DouyinWeb = DouyinWeb(self.client)
        self.DouyinAppV1 = DouyinAppV1(self.client)
        self.DouyinAppV2 = DouyinAppV2(self.client)
        self.DouyinAppV3 = DouyinAppV3(self.client)

        # TikTok
        self.TikTokWeb = TikTokWeb(self.client)
        self.TikTokAppV2 = TikTokAppV2(self.client)
        self.TikTokAppV3 = TikTokAppV3(self.client)

        # Instagram
        self.InstagramWeb = InstagramWeb(self.client)

        # Weibo
        self.WeiboWeb = WeiboWeb(self.client)

        # Captcha Solver
        self.CaptchaSolver = CaptchaSolver(self.client)

        # Xigua Video APP V2
        self.XiguaAppV2 = XiguaAppV2(self.client)

        # XiaoHongShu Web
        self.XiaohongshuWeb = XiaohongshuWeb(self.client)

        # KuaiShou Web
        self.KuaishouWeb = KuaishouWeb(self.client)

        # YouTube Web
        self.YouTubeWeb = YouTubeWeb(self.client)

        # Net Ease Cloud Music
        self.NetEaseCloudMusicAppV1 = NetEaseCloudMusicAppV1(self.client)

        # Twitter Web
        self.TwitterWeb = TwitterWeb(self.client)

        # Hybrid Parsing
        self.HybridParsing = HybridParsing(self.client)

    """
    [中文]
    
    这些代码用于实现异步上下文管理器，使得类的实例可以与 async with 语句一起使用，从而在进入和退出时自动处理资源的初始化和清理。
    
    例如：
    async with Client(api_key=api_key) as client:
        pass
        
    这样在退出时会自动调用 __aexit__ 方法，关闭 client。
    
    [English]
    
    This code is used to implement an asynchronous context manager, 
    which allows instances of a class to be used with the async with statement, 
    automatically handling the initialization and cleanup of resources when entering and exiting.
    
    For example:
    async with Client(api_key=api_key) as client:
        pass
        
    This way, the __aexit__ method is automatically called when exiting, closing the client.
    """

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()


if __name__ == '__main__':
    # Example
    api_key = "YOUR_API_KEY"
    client = Client(api_key=api_key)
