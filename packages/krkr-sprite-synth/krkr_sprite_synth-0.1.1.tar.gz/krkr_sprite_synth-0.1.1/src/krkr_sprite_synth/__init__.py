from PIL import Image
from typing import List
from pathlib import Path

from .drawer import draw
from .models import Layer, ParseResult
from .parser import InfoParser, parse_layers


class SpriteSynth:
    def __init__(
        self,
        a_info_path: str,
        b_info_path: str,
        layers_info_path_template: str,
        assets_path: str,
    ):
        """初始化 SpriteSynth 类。

        Args:
            a_info_path (str): a_info 文件路径，一般位于 /fgimage/<character_name>a_info.txt
            b_info_path (str): b_info 文件路径，一般位于 /fgimage/<character_name>b_info.txt
            layers_info_path_template (str): 图层信息文件路径模板，一般是 /fgimage/<character_name>/<character_name>{info_type}.txt
            assets_path (str): 资源文件夹路径，一般是 /fgimage/<character_name>
        """
        self.a_info_path = a_info_path
        self.b_info_path = b_info_path
        self.layers_info_path_template = layers_info_path_template
        self.assets_path = Path(assets_path)

        self.a_info = self._read_file(self.a_info_path)
        self.b_info = self._read_file(self.b_info_path)

        self.info_parser = InfoParser(a_info=self.a_info, b_info=self.b_info)

    def _read_file(self, file_path: str, encoding: str = "utf-16 LE") -> str:
        """读取指定编码的文件内容。"""
        return Path(file_path).read_text(encoding=encoding).lstrip("\ufeff")

    def get_parse_result(self, dress: str, face: str, pose: str) -> ParseResult:
        """解析给定文件的信息并返回解析结果。"""
        return self.info_parser.parse(dress=dress, face=face, pose=pose)

    def get_layers(self, layers_info_path: str, names: List[str]) -> List[Layer]:
        """解析图层信息并返回相关图层。"""
        layers_info = self._read_file(layers_info_path)
        all_layers = parse_layers(layers_info=layers_info)

        layers = []

        for name in names:
            for layer in all_layers:
                if layer.name == name:
                    layers.append(layer)

        return layers

    def draw(self, dress: str, face: str, pose: str) -> Image.Image:
        """绘制立绘

        Args:
            dress (str): 服装名
            face (str): 表情序号
            pose (str): 姿势序号

        Raises:
            ValueError: 如果匹配到的服装数量不为 1 或 2

        Returns:
            Image.Image: 绘制好的立绘
        """
        parse_result = self.get_parse_result(dress=dress, face=face, pose=pose)
        layers_info_path = self.layers_info_path_template.format(
            info_type=parse_result.info_type
        )
        if len(parse_result.dresses) == 2:
            names = (
                [parse_result.dresses[0]]
                + parse_result.faces
                + [parse_result.dresses[1]]
            )
        elif len(parse_result.dresses) == 1:
            names = parse_result.dresses + parse_result.faces
        else:
            names = parse_result.dresses + parse_result.faces
            print(
                f"WARN: Invalid number of dresses: {parse_result.dresses}, can't ensure the correctness of the result."
            )

        layers = self.get_layers(layers_info_path, names)

        return draw(layers, parse_result.info_type, self.assets_path)


__all__ = ["SpriteSynth"]
