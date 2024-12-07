#  Copyright 2024 Exactpro (Exactpro Systems Limited)
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

from dataclasses import dataclass


@dataclass
class IterStatus:
    taskID: str = None
    createdAt: str = None
    completedAt: str = None
    status: str = None
    errors: str = None


class StatusUpdateManager:
    def __init__(self, data):
        """Initialize the StatusUpdateManager.

        Args:
            data: The data object to manage status updates for.
        """
        self.__data = data

    def update(self, status):
        self.__data.update_metadata({"Iter statuses": IterStatus(**status)})
