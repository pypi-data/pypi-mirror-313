from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Generator

import ipywidgets
from IPython.display import display

from ..api.chat.interfaces import StreamingChatCompletionChunk


def StreamingMultiplexer(
    streaming_generators: list[Generator[StreamingChatCompletionChunk, Any, Any]],
    boxes_per_row: int = 2,
):
    """Display multiple streaming outputs simultaneously in a grid layout.

    Uses ThreadPoolExecutor to concurrently process multiple streaming generators
    and display their outputs in a grid of text areas. Each stream gets its own
    text area that updates in real-time.

    Args:
        streaming_generators: List of generators yielding StreamingChatCompletionChunks
        boxes_per_row: Number of text areas to display per row. Defaults to 2.

    Example:
        >>> generators = [chat.stream() for chat in chats]
        >>> StreamingMultiplexer(generators, boxes_per_row=3)
    """

    def _stream_output(
        generator: Generator[StreamingChatCompletionChunk, Any, Any],
        output_widget: ipywidgets.Textarea,
    ):
        for chunk in generator:
            output_widget.value += chunk.choices[0].delta.content

    textareas = [
        ipywidgets.Textarea(
            value="",
            placeholder=f"{index}",
            disabled=False,
            layout=ipywidgets.Layout(width="45%", height="200px"),
        )
        for index in range(len(streaming_generators))
    ]

    for textarea in range(0, len(textareas), boxes_per_row):
        hbox = ipywidgets.HBox(textareas[textarea : textarea + boxes_per_row])
        display(hbox)

    with ThreadPoolExecutor(max_workers=len(streaming_generators)) as executor:
        futures = []
        for index, generator in enumerate(streaming_generators):
            future = executor.submit(_stream_output, generator, textareas[index])
            futures.append(future)

        for future in as_completed(futures):
            pass
