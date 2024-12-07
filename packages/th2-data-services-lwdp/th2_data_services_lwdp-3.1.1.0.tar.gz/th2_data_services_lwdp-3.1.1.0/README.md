# Lightweight Data Provider Data Source (major version 3)

## Introduction
This repository is an implementation of data-services data source for Lightweight Data Provider V3.

Most commands that this library provides can be seen in the example below.

## Example
<!-- start get_started_example.py -->
```python
from typing import List

from th2_data_services.event_tree import EventTreeCollection

from th2_data_services.data_source.lwdp.commands import http as commands
from th2_data_services.data_source.lwdp.data_source import DataSource
from th2_data_services.data_source.lwdp.event_tree import ETCDriver
from th2_data_services.data_source.lwdp.streams import Streams, Stream
from th2_data_services.data import Data
from datetime import datetime
from th2_data_services.data_source.lwdp import Page

# About this example
#   The following document shows common features of the library.
#   Read command's docstrings to know more about commands features.


# Initialize some variables that will be used in this example.
book_id = "demo_book_1"  # demo_book_1 is an example book from host namespace
page_name = "1"  # example page name from book demo_book_1
scopes = ["th2-scope"]  # Event scope - similar to stream for messages.

# [0] Streams
#   Stream is a string that looks like `alias:direction`
#   - You can provide only aliases as streams, in this way all directions
#   will be requested for stream.
#   - Stream objects to set up exact direction.
#   - Streams object to set up exact direction for all aliases.
#   - Mix of them.

# We can use a list of aliases.
streams = [
    "default-message-producer-alias",
    "fix-demo-server1",
    "fix-demo-server2",
    "fix-client2",
    "fix-client1",
]
# A list of Stream objects.
streams_list_with_stream_object = [
    Stream("default-message-producer-alias", direction=1),
    Stream("fix-demo-server1", direction=2),
    Stream("fix-demo-server2"),  # Both directions.
    Stream("fix-client1", direction=1),
    Stream("fix-client2", direction=1),
]
# Or a Streams object, which takes a list of aliases as argument.
streams_direction1 = Streams(streams, direction=1)


groups = streams  # In this namespace groups and streams have same name.

# Date has to be in utc timezone.
START_TIME = datetime(year=2023, month=1, day=5, hour=13, minute=57, second=5, microsecond=0)
END_TIME = datetime(year=2023, month=1, day=5, hour=13, minute=57, second=6, microsecond=0)

# [1] Create data source object to connect to lightweight data provider.
provider_url_link = "http://10.100.66.105:32681"
data_source = DataSource(provider_url_link)

# [2] Getting books, pages, scopes, groups and aliases.

# [2.1] Get books.
#   On database data is segregated with books, such as they never intersect.
#   To get the names of the books we have a command GetBooks which takes no argument.
books: List[str] = data_source.command(commands.GetBooks())

# [2.2] Get pages.
# This command returns objects of Page class
# GetPages with only book_id returns all pages.
pages_all: Data[Page] = data_source.command(commands.GetPages(book_id))

# GetPages with timestamps returns all pages within that time frame.
pages: Data[Page] = data_source.command(commands.GetPages(book_id, START_TIME, END_TIME))

# [2.3] Get scopes.
# Some events are grouped by scopes, which we can get using GetScopes command.
book_scopes: List[str] = data_source.command(commands.GetEventScopes(book_id))

# [2.4] Get message aliases.
aliases: List[str] = data_source.command(commands.GetMessageAliases(book_id))

# [2.5] Get message groups.
book_groups: List[str] = data_source.command(commands.GetMessageGroups(book_id))

# [3] Getting events and messages.

# [3.1] Get events/messages by ID.
#   These commands will raise Exception if the event/message is not found.
#   If you don't want to get Exception, use `use_stub=True` commands parameter.
#     In this way you will get event/message stub.

# [3.1.1] Get events by id.
single_event: dict = data_source.command(
    commands.GetEventById(
        "demo_book_1:th2-scope:20221226140719671764000:9c59694b-8526-11ed-8311-df33e1b504e4"
    )
)
multiple_events: List[dict] = data_source.command(
    commands.GetEventsById(
        [
            "demo_book_1:th2-scope:20221226140719671764000:9c59694b-8526-11ed-8311-df33e1b504e4",
            "demo_book_1:th2-scope:20221226140723967243000:9ee8edcc-8526-11ed-8311-df33e1b504e4",
            "demo_book_1:th2-scope:20221226140724065522000:9ef7e1ed-8526-11ed-8311-df33e1b504e4",
        ]
    )
)

# [3.1.2] Get messages by id.
single_message: dict = data_source.command(
    commands.GetMessageById("case3:arfq02fix30:2:20221111165012889502000:1668182272676097251")
)
multiple_messages: List[dict] = data_source.command(
    commands.GetMessagesById(
        [
            "case3:arfq02fix30:2:20221111165012889502000:1668182272676097251",
            "case3:arfq02fix30:2:20221111165252889876000:1668182272676097315",
        ]
    )
)

# [3.2] Get events/messages by BOOK.

# [3.2.1] Get events by BOOK, scopes and time interval.
events: Data[dict] = data_source.command(
    commands.GetEventsByBookByScopes(
        start_timestamp=START_TIME, end_timestamp=END_TIME, book_id=book_id, scopes=scopes
    )
)

# [3.2.2] Get messages by BOOK, streams and time interval.
#   streams: List of aliases to request. If direction is not specified all directions
#   will be requested for stream.
#   You can also use Stream and Streams classes to set up them (see streams section [0]).
messages_by_stream: Data[dict] = data_source.command(
    commands.GetMessagesByBookByStreams(
        start_timestamp=START_TIME,
        end_timestamp=END_TIME,
        streams=streams,
        book_id=book_id,
    )
)

# [3.2.3] Get messages by BOOK, groups and time interval.
messages_by_group: Data[dict] = data_source.command(
    commands.GetMessagesByBookByGroupsSse(
        start_timestamp=START_TIME, end_timestamp=END_TIME, groups=groups, book_id=book_id
    )
)

# [3.3] Get events/messages by PAGE.
#   This set of commands allows you to get data by specific page instead of datetime range.
#   GetByPage commands accept Page class objects as argument.
#   Alternatively they also accept page name with book id.

page: Page = list(pages)[0]

events_by_page_by_scopes: Data[dict] = data_source.command(
    commands.GetEventsByPageByScopes(page=page, scopes=["th2-scope"])
)
events_by_page_name_by_scopes: Data[dict] = data_source.command(
    commands.GetEventsByPageByScopes(page=page_name, book_id=book_id, scopes=["th2-scope"])
)

messages_by_page_by_streams: Data[dict] = data_source.command(
    commands.GetMessagesByPageByStreams(page=page, stream=streams)
)
messages_by_page_name_by_streams: Data[dict] = data_source.command(
    commands.GetMessagesByPageByStreams(page=page_name, book_id=book_id, stream=streams)
)

messages_by_page_by_groups: Data[dict] = data_source.command(
    commands.GetMessagesByPageByGroupsSse(page=page, groups=groups)
)
messages_by_page_name_by_groups: Data[dict] = data_source.command(
    commands.GetMessagesByPageByGroupsSse(page=page_name, book_id=book_id, groups=groups)
)

# [4] ETCDriver
#   To work with EventTreeCollection and its children we need to use special driver.
#   This driver contains lwdp-related methods that ETC required.

# [4.1] Init driver
etc_driver = ETCDriver(data_source=data_source, use_stub=False)
# [4.2] Init ETC object
etc = EventTreeCollection(etc_driver)

# [4.3] Build Event Trees inside ETC and recover unknown events if it has them.
etc.build(events)
etc.recover_unknown_events()
# See more info about how to use ETC in th2-data-services lib documentation.
```
<!-- end get_started_example.py -->

## Changes in LwDP 3.* against LwDP 2.*

Changes mostly affect how messages are represented in LwDP V3.

In V3 message id will also get a group section, and the new format will look like:
`book:group:session_alias:direction:timestamp:sequence`

The Main changes are in the body field of a message:
* METADATA
  * the metadata does not contain duplicated information from the top message (direction, sequence, timestamp, sessionId). Only subsequence, messageType and protocol are left (inside metadata).
  * metadata block doesn’t have fixed structure. So if there is only 1 parsed was produced from raw message, metadata will not have this key.
  * ONLY messageType is required field in metadata.

* BODY
  * The body is a collection (list) now (if the raw message produced a single parsed message, it will have only 1 element. If raw messages produced more than 1 message, all of them will be in that collection in the order they were produced).

* subsequence
  * is always list.
  * may be missing in metadata. It means [1].

Here is a small example on how to use expander to expand single message into multiple ones:

```python
from th2_data_services.data import Data
from th2_data_services.data_source.lwdp.resolver import MessageFieldResolver
# message in this example have 2 items in its body
message = {
    "timestamp":{"epochSecond":1682680778,"nano":807953000},
    "direction":"IN",
    "sessionId":"ouch_1_1",
    "attachedEventIds":[],
    "body":[
        {
            "metadata":
            {
                "subsequence":[1],
                "messageType":"SequencedDataPacket",
                "protocol":"protocol"
            },
            "fields":
            {
                "MessageLength":55,
                "MessageType":83
            }
        },
        {
            "metadata":
            {   
                "subsequence":[2],
                "messageType":"OrderExecuted",
                "protocol":"protocol"
            },
            "fields":
            {
                "MessageType":69,
                "Timestamp":1682399803928773173,
                "OrderToken":"lzgjaynpgynbg1",
                "OrderBookID":110616,
                "TradedQuantity":50,
                "TradePrice":5000,
                "MatchID":"j\ufffdh\u0003\u0000\u0000\u0000\u0006\u0000\u0000\u0000",
                "DealSource":1,
                "MatchAttributes":5
            }
        }
    ],
    "messageId":"store_perf_test:ouch_1_1:1:20230428111938807953000:1682680778806000001"
}

message_data = Data([message])
mfr = MessageFieldResolver()
message_data = message_data.map(mfr.expand_message)
print(message_data) # we should now have 2 messages built from the body list of original message.
```

