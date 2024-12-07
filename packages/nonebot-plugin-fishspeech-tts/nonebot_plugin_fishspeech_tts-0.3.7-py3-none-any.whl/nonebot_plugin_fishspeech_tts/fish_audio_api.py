from pathlib import Path

import ormsgpack
from httpx import (
    AsyncClient,
    ConnectError,
    ConnectTimeout,
    HTTPStatusError,
    ReadTimeout,
)
from nonebot.log import logger

from .config import config
from .exception import (
    APIException,
    AuthorizationException,
    FileHandleException,
    HTTPException,
)
from .files import (
    extract_text_by_filename,
    get_path_speaker_list,
    get_speaker_audio_path,
)
from .request_params import ChunkLength, ServeReferenceAudio, ServeTTSRequest

is_reference_id_first = config.online_model_first
online_api_proxy = config.online_api_proxy


class FishAudioAPI:
    """
    FishAudioAPI类, 用于调用FishAudio的API接口
    """

    def __init__(self):
        self.url: str = "https://api.fish.audio/v1/tts"
        self.path_audio: Path = Path(config.tts_audio_path)
        self.proxy = online_api_proxy

        # 如果在线授权码为空, 且使用在线api, 则抛出异常
        if not config.online_authorization and config.tts_is_online:
            raise APIException("请先在配置文件中填写在线授权码或使用离线api")
        self.headers = {
            "Authorization": f"Bearer {config.online_authorization}",
        }

        # 如果音频文件夹不存在, 则创建音频文件夹
        if not self.path_audio.exists():
            self.path_audio.mkdir(parents=True)
            logger.warning(f"音频文件夹{self.path_audio.name}不存在, 已创建")
        elif not self.path_audio.is_dir():
            raise NotADirectoryError(f"{self.path_audio.name}不是一个文件夹")

    async def _get_reference_id_by_speaker(self, speaker: str) -> str:
        """
        通过说话人姓名获取说话人的reference_id

        Args:
            speaker: 说话人姓名

        Returns:
            reference_id: 说话人的reference_id

        exception:
            APIException: 获取语音角色列表为空
        """
        request_api = "https://api.fish.audio/model"
        sort_options = ["score", "task_count", "created_at"]
        async with AsyncClient(proxy=self.proxy) as client:
            for sort_by in sort_options:
                params = {"title": speaker, "sort_by": sort_by}
                response = await client.get(
                    request_api, params=params, headers=self.headers
                )
                resp_data = response.json()
                if resp_data["total"] == 0:
                    continue
                for item in resp_data["items"]:
                    if speaker in item["title"]:
                        return item["_id"]
        raise APIException("未找到对应的角色")

    async def generate_servettsrequest(
        self,
        text: str,
        speaker_name: str,
        chunk_length: ChunkLength = ChunkLength.NORMAL,
    ) -> ServeTTSRequest:
        """
        生成TTS请求

        Args:
            text: 待合成文本
            speaker_name: 说话人姓名
            chunk_length: 分片长度

        Returns:
            ServeTTSRequest: TTS请求
        """
        reference_id = None
        references = []
        try:
            if is_reference_id_first:
                reference_id = await self._get_reference_id_by_speaker(speaker_name)
            else:
                try:
                    speaker_audio_path = get_speaker_audio_path(
                        self.path_audio, speaker_name
                    )
                    for audio in speaker_audio_path:
                        audio_bytes = audio.read_bytes()
                        ref_text = extract_text_by_filename(audio.name)
                        references.append(
                            ServeReferenceAudio(audio=audio_bytes, text=ref_text)
                        )
                except FileHandleException:
                    logger.warning("音频文件夹不存在, 已转为在线模型优先模式")
                    reference_id = await self._get_reference_id_by_speaker(speaker_name)
        except APIException as e:
            raise e from e
        return ServeTTSRequest(
            text=text,
            reference_id=reference_id,
            format="wav",
            mp3_bitrate=64,
            latency="normal",
            opus_bitrate=24,
            normalize=True,
            chunk_length=chunk_length.value,
            references=references,
        )

    async def generate_tts(self, request: ServeTTSRequest) -> bytes:
        """
        获取TTS音频

        Args:
            request: TTS请求

        Returns:
            bytes: TTS音频二进制数据
        """
        if request.references:
            self.headers["content-type"] = "application/msgpack"
            try:
                async with (
                    AsyncClient(proxy=self.proxy) as client,
                    client.stream(
                        "POST",
                        self.url,
                        headers=self.headers,
                        content=ormsgpack.packb(
                            request.dict(),
                        ),
                        timeout=60,
                    ) as resp,
                ):
                    return await resp.aread()
            except (
                ConnectError,
                HTTPStatusError,
            ) as e:
                logger.error(f"获取TTS音频失败: {e}")
                if self.proxy:
                    raise HTTPException("代理地址错误, 请检查代理地址是否正确") from e
                raise HTTPException("网络错误, 请检查网络连接") from e
        else:
            self.headers["content-type"] = "application/json"
            try:
                async with AsyncClient(proxy=self.proxy) as client:
                    response = await client.post(
                        self.url,
                        headers=self.headers,
                        json=request.dict(),
                        timeout=60,
                    )
                    return response.content
            except (
                ReadTimeout,
                ConnectTimeout,
                ConnectError,
                HTTPStatusError,
            ) as e:
                logger.error(f"获取TTS音频失败: {e}")
                if self.proxy:
                    raise HTTPException("代理地址错误, 请检查代理地址是否正确") from e
                raise HTTPException("网络错误, 请检查网络连接") from e

    async def get_balance(self) -> float:
        """
        获取账户余额
        """
        balance_url = "https://api.fish.audio/wallet/self/api-credit"
        async with AsyncClient(proxy=self.proxy) as client:
            response = await client.get(balance_url, headers=self.headers)
            try:
                return response.json()["credit"]
            except KeyError:
                raise AuthorizationException("授权码错误或已失效") from KeyError

    def get_speaker_list(self) -> list[str]:
        """
        获取语音角色列表
        """
        return_list = ["请查看官网了解更多: https://fish.audio/zh-CN/"]
        if is_reference_id_first:
            try:
                return_list.extend(get_path_speaker_list(self.path_audio))
            except FileHandleException:
                logger.warning("音频文件夹不存在或无法读取")
        return return_list
