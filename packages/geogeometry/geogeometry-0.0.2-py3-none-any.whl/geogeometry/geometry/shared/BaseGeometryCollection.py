from typing import List, TypeVar, Iterator, Optional, Union

T = TypeVar('T')


class BaseGeometryCollection(object):

    def __init__(self, name: Optional[str] = None):
        self.name: Optional[str] = name
        self.elements: List[T] = []

    def __len__(self) -> int:
        return len(self.elements)

    def __iter__(self) -> Iterator[T]:
        for e in self.elements:
            yield e

    def __getitem__(self, identifier: Union[int, str]) -> T:
        if isinstance(identifier, int):
            return self.elements[identifier]
        else:
            for e in self.elements:
                if e.getName() == identifier:
                    return e
            else:
                raise ValueError(f"Element '{identifier}' not found in collection.")

    def addElement(self, element: T) -> None:
        self.elements += [element]

    def deleteElement(self, identifier: Union[int, str]):
        for e in self.elements:
            if e.getName() == identifier:
                self.elements.remove(e)
                break
        else:
            raise ValueError(f"Element '{identifier}' not found in collection.")
