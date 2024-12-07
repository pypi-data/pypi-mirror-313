#  Copyright 2023-2024 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from typing import List, Optional


class Stream:
    """General interface for stream for lwdp ds.

    The class gives the opportunity to make stream with direction.
    """

    def __init__(self, alias: str, direction: Optional[int] = None):
        """Streams constructor.

        Args:
            alias: Stream name.
            direction: Direction of Stream (Only 1 or 2). If None then is both directions.
        """
        self._alias = alias
        if direction is not None:
            direction = str(direction)
            if direction not in ("1", "2"):
                raise ValueError("The direction must be '1' or '2'.")
        self._direction = direction

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(" f"alias={self._alias}, " f"direction={self._direction})"

    def url(self) -> str:
        """Generates the stream part of the HTTP protocol API.

        Returns:
            str: Generated streams.
        """
        if self._direction is None:
            return f"&stream={self._alias}"
        return f"&stream={self._alias}:{self._direction}"

    def convert_to_dict_format(self) -> dict:
        direction_mapper = {
            "1": ["IN"],
            "2": ["OUT"],
        }
        result = {"sessionAlias": self._alias}
        if self._direction:
            result["direction"] = direction_mapper[self._direction]
        return result


class Streams:
    """General interface for composite streams of lwdp ds.

    The class gives the opportunity to make list of streams with direction for each.
    """

    def __init__(self, aliases: List[str], direction: Optional[int] = None):
        """Streams constructor.

        Args:
            aliases: List of Streams.
            direction: Direction of Streams (Only 1 or 2). If None then is both directions.
        """
        self._aliases = aliases
        if direction is not None:
            direction = str(direction)
            if direction not in ("1", "2"):
                raise ValueError("The direction must be '1' or '2'.")
        self._direction = direction

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(" f"aliases={self._aliases}, " f"direction={self._direction})"

    def as_list(self):
        result = []
        if self._direction is None:
            for alias in self._aliases:
                result.append(alias)
        else:
            for alias in self._aliases:
                result.append(f"{alias}:{self._direction}")
        return result

    def url(self) -> str:
        """Generates the stream part of the HTTP protocol API.

        Returns:
            str: Generated streams.
        """
        if self._direction is None:
            return "&".join([f"stream={alias}" for alias in self._aliases])
        return "&".join([f"stream={stream}:{self._direction}" for stream in self._aliases])

    def convert_to_dict_format(self) -> List[dict]:
        return [
            Stream(stream, self._direction).convert_to_dict_format() for stream in self._aliases
        ]


def _convert_stream_to_dict_format(streams):
    def map_func(s):
        if isinstance(s, Stream):
            return [s.convert_to_dict_format()]

        if isinstance(s, Streams):
            return s.convert_to_dict_format()

        if isinstance(s, str):
            if ":" in s:
                stream_obj = Stream(*s.split(":"))
            else:
                stream_obj = Stream(s)
            return [stream_obj.convert_to_dict_format()]
        return [s]

    if isinstance(streams, List):
        return [item for sublist in map(map_func, streams) for item in sublist]
    return map_func(streams)
