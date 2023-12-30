"""Helper functions that use spotipy APIs."""

from dataclasses import dataclass
from time import sleep
from typing import Callable, Iterator, Optional

from spotipy.exceptions import SpotifyException
from tqdm import tqdm


@dataclass
class InvalidPaginationResponse(Exception):
    """Error when a spotipy paginated function doesn't contain `items`."""


def unpaginate(
    f: Callable,
    item_limit: Optional[int] = None,
    limit: Optional[int] = None,
    starting_offset: int = 0,
    *args,
    **kwargs,
) -> Iterator[dict]:
    """Wraps a spotipy function that returns a paginated response from spotify."""

    current_offset = starting_offset
    yielded_items = 0
    total = None

    metadata_response = f(*args, limit=1, **kwargs)
    total = metadata_response["total"]
    pbar = tqdm(total=total)

    while yielded_items < total:
        limit_offset_kwargs = dict()
        if limit is not None:
            limit_offset_kwargs["limit"] = limit

        limit_offset_kwargs["offset"] = current_offset

        try:
            sleep(0.05)
            response = f(*args, **limit_offset_kwargs, **kwargs)
        except SpotifyException as e:
            if e.http_status == 429:
                print("should sleep")
            print(e)

        if "items" not in response:
            raise InvalidPaginationResponse(response)

        new_items = response["items"]

        current_offset += len(new_items)

        for item in new_items:
            if item_limit is not None and yielded_items >= item_limit:
                pbar.close()
                return

            yield item
            pbar.update(1)
            yielded_items += 1

    pbar.close()
