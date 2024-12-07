from typing import Any, List, Optional

import httpx

from ..config import maiconfig
from .maimaidx_error import *


class MaimaiAPI:
    
    MaiAPI = 'https://www.diving-fish.com/api/maimaidxprober'
    MaiAliasAPI = 'https://api.yuzuai.xyz/maimaidx'
    
    def __init__(self) -> None:
        """封装Api"""
    
    
    def load_token(self) -> str:
        self.token = maiconfig.maimaidxtoken
        self.headers = {'developer-token': self.token}
    
    
    async def _request(self, method: str, url: str, **kwargs) -> Any:
        
        session = httpx.AsyncClient(timeout=30)
        res = await session.request(method, url, **kwargs)

        data = None
        
        if self.MaiAPI in url:
            if res.status_code == 200:
                data = res.json()
            elif res.status_code == 400:
                raise UserNotFoundError
            elif res.status_code == 403:
                raise UserDisabledQueryError
            else:
                raise UnknownError
        elif self.MaiAliasAPI in url:
            if res.status_code == 200:
                data = res.json()
                if 'error' in data:
                    raise ValueError(f'发生错误：{data["error"]}')
            elif res.status_code == 400:
                raise EnterError
            elif res.status_code == 500:
                raise ServerError
            else:
                raise UnknownError
        await session.aclose()
        return data
    
    
    async def music_data(self):
        """获取曲目数据"""
        return await self._request('GET', self.MaiAPI + '/music_data')
    
    
    async def chart_stats(self):
        """获取单曲数据"""
        return await self._request('GET', self.MaiAPI + '/chart_stats')
    
    
    async def query_user(self, project: str, *, qqid: Optional[int] = None, username: Optional[str] = None, version: Optional[List[str]] = None):
        """
        请求用户数据
        
        - `project`: 查询的功能
            - `player`: 查询用户b50
            - `plate`: 按版本查询用户游玩成绩
        - `qqid`: 用户QQ
        - `username`: 查分器用户名
        """
        json = {}
        if qqid:
            json['qq'] = qqid
        if username:
            json['username'] = username
        if version:
            json['version'] = version
        if project == 'player':
            json['b50'] = True
        return await self._request('POST', self.MaiAPI + f'/query/{project}', json=json)
    
    
    async def query_user_dev(self, *, qqid: Optional[int] = None, username: Optional[str] = None):
        """
        使用开发者接口获取用户数据，请确保拥有和输入了开发者 `token`
        
        - `qqid`: 用户QQ
        - `username`: 查分器用户名
        """
        params = {}
        if qqid:
            params['qq'] = qqid
        if username:
            params['username'] = username
        return await self._request('GET', self.MaiAPI + f'/dev/player/records', headers=self.headers, params=params)
    
    
    async def rating_ranking(self):
        """获取查分器排行榜"""
        return await self._request('GET', self.MaiAPI + f'/rating_ranking')
        
    
    async def get_alias(self):
        """获取所有别名"""
        return await self._request('GET', self.MaiAliasAPI + '/maimaidxalias')
    
    
    async def get_songs(self, id: int):
        """使用曲目 `id` 查询别名"""
        return await self._request('GET', self.MaiAliasAPI + '/getsongsalias', params={'id': id})
    
    
    async def get_alias_status(self):
        """获取当前正在进行的别名投票"""
        return await self._request('GET', self.MaiAliasAPI + '/getaliasstatus')
    
    
    async def get_alias_end(self):
        """获取五分钟内结束的别名投票"""
        return await self._request('GET', self.MaiAliasAPI + '/getaliasend')
    
    
    async def transfer_music(self):
        """中转查分器曲目数据"""
        return await self._request('GET', self.MaiAliasAPI + '/getmaimaidxmusic')
    
    
    async def transfer_chart(self):
        """中转查分器单曲数据"""
        return await self._request('GET', self.MaiAliasAPI + '/getmaimaidxchartstats')
    
    
    async def post_alias(self, id: int, aliasname: str, tag: str, user_id: int):
        """
        提交别名申请
        
        - `id`: 曲目 `id`
        - `aliasname`: 别名
        - `tag`: 标签
        - `user_id`: 提交的用户
        """
        params = {
            'id': id,
            'aliasname': aliasname,
            'tag': tag,
            'uid': user_id
        }
        return await self._request('POST', self.MaiAliasAPI + '/applyalias', params=params)
    
    
    async def post_agree_user(self, tag: str, user_id: int):
        """
        提交同意投票
        
        - `tag`: 标签
        - `user_id`: 同意投票的用户
        """
        params = {
            'tag': tag,
            'uid': user_id
        }
        return await self._request('POST', self.MaiAliasAPI + '/agreeuser', params=params)
    

maiApi = MaimaiAPI()