"""
This module contains the Record dataclass, which is used to store the data and additional
"""

import dataclasses
from datetime import datetime
from typing import Any, Callable, Dict, List, Literal, Optional, Self, Union
from uuid import uuid4

from loguru import logger as log

EventHandler = Callable[[Self], None]
EventType = Literal["on_done", "on_error", "on_start"]
RecordState = Literal["done", "error", "start", "rejected"]


@dataclasses.dataclass
class Record:
    """This dataclass represents a single record in a data set.
    It is used to store the data and additional information about the record and helps to keep
    the data organized.

    The use cases where this class is used are:
    - help reshuffling the data, i.e. based on the source directory name.
    - create audit logs, i.e. to keep track of the data source
      and the time the data was processed.

    Attributes
    ----------
    payload : Any
        The data of the record.
    source : Optional[Record]
        The source of the record.
    uuid : Optional[str]
        The unique identifier of the record.
    processed_at : datetime
        The time the record was processed.
    children : List["Record"]
        The list of child records of the record.

    Examples
    --------
    >>> record = Record({"key": "value"}, Path())
    >>> record.uuid
    '...'
    >>> record.processed_at
    '...'
    >>> record.payload
    {"key": "value"}
    >>> record.source
    Path()
    >>> record.children
    []

    """

    payload: Optional[Any] = None
    source: Optional[Self] = None
    uuid: Optional[str] = uuid4().hex
    processed_at: datetime = datetime.now()
    children: List[Self] = dataclasses.field(default_factory=list)
    event_handlers: Dict[EventType, List[EventHandler]] = dataclasses.field(
        default_factory=dict
    )
    state: RecordState = "start"

    def split(
        self,
        key: Optional[str] = None,
        id_key: Optional[str] = None,
        func: Optional[Callable[[Self, ...], List[Self]]] = None,
        **kwargs,
    ) -> List[Self]:
        """Splits the record bases on either a keyword or a function. If a function is provided,
        it will be used to split the payload, even if you provide a key. If a key is provided, it
        will split the payload.
        All further kwargs will be passed to the function.


        Parameters:
            key (Optional[str], optional): The key to split the record on.
            id_key (Optional[str], optional): The key to use as the unique identifier for
                the child records. Defaults to None.
            func (Optional[Callable], optional): A function to split to the payload before.

        Returns:
            List[Record]: A list of records, if the key is not found or the
                          addressed field is not a list, it will return an empty list.

        Examples:
            >>> record = Record({"key": [{"name": "Elsbeth"}, {"name": "Eliza"}]}, Path())
            >>> record.split("key")
            [Record(payload={"name": "Elsbeth"}), Record(payload={"name": "Eliza"})]
            >>> record.split("key", id_key="name")
            [
                Record(
                    id="Elsbeth",
                    payload={"name": "Elsbeth"}
                ),
                Record(
                    id="Eliza",
                    payload={"name": "Eliza"}
                )
            ]
        """
        if func is not None:
            return func(self, **kwargs)
        return self._handle_key_split_(id_key, key)

    def _handle_key_split_(self, id_key, key):
        if key not in self.payload:
            return []
        if not isinstance(self.payload[key], list):
            return []
        split_payload = [
            Record(
                **{
                    "payload": value,
                    "uuid": value.get(id_key) if id_key else uuid4().hex,
                    "source": self,
                }
            )
            for value in self.payload[key]
        ]
        self.children.extend(split_payload)
        return split_payload

    def to_log(self) -> Dict[str, Union[str, List[Dict[str, Any]]]]:
        """Return a loggable representation of the record."""
        log.debug(f"Logging record {self.uuid}.")

        return {
            "uuid": str(self.uuid),
            "processed_at": self.processed_at.isoformat(),
            # We cannot allow the source to be a Record, as it would create a circular reference
            # while serializing the dataclass to JSON.
            "source": (
                self.source if not isinstance(self.source, Record) else self.source.uuid
            ),
            "children": [child.to_log() for child in self.children],
        }

    def walk_tree(self, only_leafs=True) -> List[Self]:
        """Walk the record tree and return a list of all records.

        Parameters:
            only_leafs (bool, optional): If True, only the leaf nodes will be returned.
                Defaults to True.
        """
        records = []
        if self.__is_leaf__() and only_leafs:
            return [self]
        if not only_leafs:
            records.append(self)
        for child in self.children:
            records.extend(child.walk_tree(only_leafs=only_leafs))
        return records

    def done(self):
        """Call the on_done event handler."""
        # Signal parent that this record is done
        self.state = "done"
        log.debug(f"Record {self.uuid} is set as done.")
        if self.source:
            self.source.signal_done()
            log.debug(f"Signaled parent {self.source.uuid} of record {self.uuid}.")
        self.__dispatch_event__("on_done")

    def signal_done(self):
        """Signal that a child record is done."""
        # If all children are done, so is the parent.
        _children_status_ = [child.state == "done" for child in self.children]
        log.debug(f"Signaled that children of {self.uuid} is done.")
        if all(_children_status_):
            self.done()
            log.debug(f"Record {self.uuid} is done.")

    def destroy(self):
        """Destroy the record and all its children."""
        for child in self.children:
            child.destroy()

        del self

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Record):
            raise ValueError(
                "Cannot compare Record with non-Record type"
                f" Comparison was Record == {type(other)}"
            )
        # if self.payload or other.payload:
        #    return self.payload == other.payload
        return self.uuid == other.uuid

    def __dispatch_event__(self, event: EventType):
        """Dispatch an event to the event handlers."""
        log.debug(f"Dispatching event '{event}' for '{self.uuid}'.")
        for handler in self.event_handlers.get(event, []):
            handler(self)

    def __is_leaf__(self):
        return not self.children

    def __repr__(self):
        return f"Record(uuid={self.uuid}, children={len(self.children)})"
