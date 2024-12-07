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
from typing import List

from th2_data_services.interfaces.utils import resolver as resolver_core
from th2_data_services.data_source.lwdp.struct import event_struct, message_struct

from typing import Dict, Any


class EventFieldResolver(resolver_core.EventFieldResolver):
    @staticmethod
    def get_id(event) -> str:
        return event[event_struct.EVENT_ID]

    @staticmethod
    def get_parent_id(event) -> str:
        return event[event_struct.PARENT_EVENT_ID]

    @staticmethod
    def get_status(event) -> str:
        return event[event_struct.STATUS]

    @staticmethod
    def get_name(event) -> str:
        return event[event_struct.NAME]

    @staticmethod
    def get_batch_id(event) -> str:
        return event[event_struct.BATCH_ID]

    @staticmethod
    def get_is_batched(event) -> bool:
        return event[event_struct.IS_BATCHED]

    @staticmethod
    def get_type(event) -> str:
        return event[event_struct.EVENT_TYPE]

    @staticmethod
    def get_start_timestamp(event) -> Dict[str, int]:
        return event[event_struct.START_TIMESTAMP]

    @staticmethod
    def get_end_timestamp(event) -> Dict[str, int]:
        return event[event_struct.END_TIMESTAMP]

    @staticmethod
    def get_attached_messages_ids(event) -> List[str]:
        return event[event_struct.ATTACHED_MESSAGES_IDS]

    @staticmethod
    def get_body(event) -> Any:
        return event[event_struct.BODY]


class MessageFieldResolver(resolver_core.MessageFieldResolver):
    @staticmethod
    def get_direction(message) -> str:
        return message[message_struct.DIRECTION]

    @staticmethod
    def get_session_id(message) -> str:
        return message[message_struct.SESSION_ID]

    @staticmethod
    def get_type(message):
        """This field was removed since LwDP3."""
        raise NotImplementedError

    @staticmethod
    def get_sequence(message) -> str:
        # <book>:<group>:<alias>:<direction>:<timestamp>:<sequence>
        return message[message_struct.MESSAGE_ID].split(":")[5].split(".")[0]

    @staticmethod
    def get_timestamp(message) -> Dict[str, int]:
        return message[message_struct.TIMESTAMP]

    @staticmethod
    def get_body(message) -> List[Dict[str, Any]]:
        return message[message_struct.BODY]

    @staticmethod
    def get_body_base64(message) -> str:
        return message[message_struct.BODY_BASE64]

    @staticmethod
    def get_id(message) -> str:
        return message[message_struct.MESSAGE_ID]

    @staticmethod
    def get_attached_event_ids(message) -> List[str]:
        return message[message_struct.ATTACHED_EVENT_IDS]

    @staticmethod
    def expand_message(message) -> List[Dict[str, Any]]:
        """Extract compounded message into list of individual messages.

        2023.08.29 -- decided that this function should return the same structure of the message
            but with single body = {}.

        Args:
            message: Th2Message

        Returns:
            List[updated Th2Message]
        """
        if isinstance(message[message_struct.BODY], list):
            return [
                {
                    **message,
                    message_struct.BODY: msg_in_body,
                }
                for msg_in_body in message[message_struct.BODY]
            ]
        else:
            return [message]

    @staticmethod
    def get_group(message) -> str:
        """Non-interface method."""
        # <book>:<group>:<alias>:<direction>:<timestamp>:<sequence>
        return message[message_struct.MESSAGE_ID].split(":")[1]


class SubMessageFieldResolver(resolver_core.SubMessageFieldResolver):
    @staticmethod
    def get_metadata(sub_message) -> Dict[str, Any]:
        return sub_message["metadata"]

    @staticmethod
    def get_subsequence(sub_message) -> List[int]:
        return SubMessageFieldResolver.get_metadata(sub_message).get(
            message_struct.SUBSEQUENCE, [1]
        )

    @staticmethod
    def get_type(sub_message) -> str:
        return SubMessageFieldResolver.get_metadata(sub_message)[message_struct.MESSAGE_TYPE]

    @staticmethod
    def get_protocol(sub_message) -> str:
        """Returns None if no Protocol in the message."""
        return SubMessageFieldResolver.get_metadata(sub_message).get(message_struct.PROTOCOL)

    @staticmethod
    def get_fields(sub_message) -> Dict[str, Any]:
        return sub_message["fields"]


class ExpandedMessageFieldResolver(resolver_core.ExpandedMessageFieldResolver):
    @staticmethod
    def get_direction(message) -> str:
        return message[message_struct.DIRECTION]

    @staticmethod
    def get_session_id(message) -> str:
        return message[message_struct.SESSION_ID]

    @staticmethod
    def get_type(message) -> str:
        return ExpandedMessageFieldResolver.get_metadata(message)[message_struct.MESSAGE_TYPE]

    @staticmethod
    def get_sequence(message) -> str:
        # <book>:<group>:<alias>:<direction>:<timestamp>:<sequence>
        return message[message_struct.MESSAGE_ID].split(":")[5].split(".")[0]

    @staticmethod
    def get_timestamp(message) -> Dict[str, int]:
        return message[message_struct.TIMESTAMP]

    @staticmethod
    def get_body(message) -> Dict[str, Any]:
        return message[message_struct.BODY]

    @staticmethod
    def get_body_base64(message) -> str:
        return message[message_struct.BODY_BASE64]

    @staticmethod
    def get_id(message) -> str:
        return message[message_struct.MESSAGE_ID]

    @staticmethod
    def get_attached_event_ids(message) -> List[str]:
        return message[message_struct.ATTACHED_EVENT_IDS]

    @staticmethod
    def get_subsequence(message) -> List[int]:
        return ExpandedMessageFieldResolver.get_metadata(message).get(
            message_struct.SUBSEQUENCE, [1]
        )

    @staticmethod
    def get_fields(message) -> Dict[str, Any]:
        return ExpandedMessageFieldResolver.get_body(message)["fields"]

    @staticmethod
    def get_metadata(message) -> Dict[str, Any]:
        return ExpandedMessageFieldResolver.get_body(message)["metadata"]

    @staticmethod
    def get_protocol(message) -> str:
        return ExpandedMessageFieldResolver.get_metadata(message).get(message_struct.PROTOCOL)

    @staticmethod
    def get_group(message) -> str:
        """Non-interface method."""
        # <book>:<group>:<alias>:<direction>:<timestamp>:<sequence>
        return message[message_struct.MESSAGE_ID].split(":")[1]


# TODO - for backward compatibility. Should be removed some time.
LwdpEventFieldsResolver = EventFieldResolver
LwdpMessageFieldsResolver = MessageFieldResolver
