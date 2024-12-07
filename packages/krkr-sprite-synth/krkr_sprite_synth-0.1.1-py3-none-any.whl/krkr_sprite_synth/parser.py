import csv
from collections import defaultdict
from typing import List, Dict, Tuple

from .models import Layer, ParseResult


class InfoParser:
    def __init__(self, a_info: str, b_info: str):
        """初始化 InfoParser 类，解析 a_info 和 b_info

        Args:
            a_info (str): a_info 的内容
            b_info (str): b_info 的内容
        """
        self.a_info = a_info
        self.b_info = b_info

        self.a_dress: Dict[Tuple[str, str], List[str]] = defaultdict(list)
        self.a_face: Dict[str, List[str]] = defaultdict(list)
        self.b_dress: Dict[Tuple[str, str], List[str]] = defaultdict(list)
        self.b_face: Dict[str, List[str]] = defaultdict(list)

        self._parse_info()

    def _parse_info(self):
        def parse_lines(
            info: str,
            dress_dict: Dict[Tuple[str, str], List[str]],
            face_dict: Dict[str, List[str]],
        ):
            for line in info.split("\n"):
                line = line.strip()
                if not line:
                    continue
                parts = line.split("\t")
                if parts[0] == "dress":
                    _, dress, _, diff, name = parts
                    dress_dict[(dress, diff)].append(name)
                elif parts[0] == "face":
                    _, face, _, name = parts
                    face_dict[face].append(name)

        parse_lines(self.a_info, self.a_dress, self.a_face)
        parse_lines(self.b_info, self.b_dress, self.b_face)

    def parse(self, dress: str, face: str, pose: str) -> ParseResult:
        """获取 dress, face 和 pose 对应的名称，用于绘制图片

        Args:
            dress (str): dress 名称
            face (str): face 名称
            pose (str): pose 名称

        Raises:
            ValueError: 如果找不到对应的名称
            ValueError: 如果在 a_info 和 b_info 中都找不到对应的 dress 名称

        Returns:
            ParseResult: 包含 dress, face 和 info_type 的 ParseResult 对象
        """
        # 私服-3-18 -> 刀服-表情（追加）/ベースb笑顔2eベースm
        dress_names = None
        info_type = None
        for (dress_, diff), names in self.a_dress.items():
            if dress_ == dress and diff == pose:
                dress_names = names
                info_type = "a"
                break

        if dress_names is None:
            for (dress_, diff), names in self.b_dress.items():
                if dress_ == dress and diff == pose:
                    dress_names = names
                    info_type = "b"
                    break

        if dress_names is None or info_type is None:
            raise ValueError(f"Cannot find dress name for {dress}-{pose}")

        try:
            face_names = self.a_face[face] if info_type == "a" else self.b_face[face]
            face_names = [name.split("/")[-1] for name in face_names]
        except KeyError:
            raise ValueError(f"Cannot find face name for {face} in {info_type} info")

        return ParseResult(dresses=dress_names, faces=face_names, info_type=info_type)


def parse_layers(layers_info: str) -> List[Layer]:
    """解析图层信息，用于绘制图片

    Args:
        layers_info (str): 图层信息

    Returns:
        List[Layer]: 图层列表
    """
    layers = []
    reader = csv.reader(layers_info.splitlines(), delimiter="\t")

    for row in reader:
        # Skip rows starting with '#'
        if row and row[0].startswith("#"):
            continue

        # Skip incomplete rows
        if len(row) < 12:
            continue

        # Parse row into Layer object
        layer = Layer(
            layer_type=int(row[0]) if row[0] else -1,
            name=row[1],
            left=int(row[2]) if row[2] else 0,
            top=int(row[3]) if row[3] else 0,
            width=int(row[4]) if row[4] else 0,
            height=int(row[5]) if row[5] else 0,
            type=int(row[6]) if row[6] else -1,
            opacity=int(row[7]) if row[7] else 0,
            visible=int(row[8]) if row[8] else 0,
            layer_id=int(row[9]) if row[9] else -1,
            group_layer_id=int(row[10]) if row[10] else -1,
            base=int(row[11]) if row[11] else -1,
            images=row[12] if len(row) > 12 else "",
        )
        layers.append(layer)
    return layers
