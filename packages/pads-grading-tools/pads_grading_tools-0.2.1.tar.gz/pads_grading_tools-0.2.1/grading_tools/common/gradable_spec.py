from __future__ import annotations

from collections.abc import Iterator, Iterable
from typing import Any, Self, Callable, TypeVar, Annotated

import pydantic
import yaml
from pydantic import ConfigDict

DEFAULT_QUESTION_DIVISION_LEVELS = ['Assignment', 'Question', 'Subquestion', 'Subsubquestion']


class GradableBase(pydantic.BaseModel):
    label: str


T = TypeVar('T')


class GradableNode(GradableBase):
    pts: float | None = pydantic.Field(default=None)
    info: dict[str, Any] | None = pydantic.Field(default=None)
    parent: GradableNode | None = pydantic.Field(default=None, repr=False)
    children: Annotated[list[GradableNode], pydantic.Field(default_factory=list), pydantic.SkipValidation]

    # @pydantic.computed_field(repr=False)
    @property
    def is_leaf(self) -> bool:
        return not self.children

    # @pydantic.computed_field(repr=False)

    @property
    def left_siblings(self) -> Iterator[Self]:
        if self.parent:
            for c in self.parent.children:
                if c == self: break
                yield c

    @property
    def right_siblings(self) -> Iterator[Self]:
        if self.parent:
            start_yielding = False
            for c in self.parent.children:
                if start_yielding:
                    yield c
                if c == self: start_yielding = True

    @property
    def siblings(self) -> Iterator[Self]:
        if self.parent:
            yield from (c for c in self.parent.children if c != self)

    # @pydantic.computed_field(repr=False)
    @property
    def ancestry(self) -> Iterator[Self]:
        if self.parent:
            yield from self.parent.ancestry
        yield self

    def get_info(self, k: str) -> Any:
        if self.info:
            return self.info.get(k, None)

    def select_children(self, selector: Callable[[GradableBase], bool]) -> list[Self]:
        return [c for c in self.children if selector(c)]

    @pydantic.computed_field(repr=False)
    @property
    def height(self) -> int:
        if not self.children:
            return 0
        return 1 + max(c.height for c in self.children)

    def iter_level(self, level: int) -> Iterable[GradableNode]:
        if level == 0:
            yield self
        elif level > 0:
            for c in self.children:
                yield from c.iter_level(level - 1)

    def preorder(self, mapper: Callable[[GradableBase], T] = lambda x: x) -> Iterator[T]:
        yield mapper(self) if mapper else self
        if self.children:
            for c in self.children:
                yield from c.preorder(mapper)
                # for c in s.preorder():
                #    yield c

    # depth of zero equals root (self) level
    def cutoff(self, depth: int) -> Self:
        children = [] if depth == 0 else [s.cutoff(depth - 1) for s in self.children]
        return self.__class__(label=self.label, pts=self.pts, info=self.info, subparts=children)

    def as_nested(self) -> dict[str, dict] | str:
        return {self.label: [c.as_nested() for c in self.children]} if self.children else self.label

    def paths(self) -> list[tuple[Self, ...]]:
        return [(self,) + v for c in self.children for v in c.paths()] if self.children else [(self,)]

    def paths_iter(self, mapper: Callable[[Self], T] | None = lambda x: x) -> Iterator[tuple[T, ...]]:
        res = (mapper(self),) if mapper else (self,)
        if not self.children:
            yield res
        else:
            for c in self.children:
                for p in c.paths_iter(mapper):
                    yield res + p

    def leaves(self) -> list[Self]:
        if not self.children:
            return [self]
        else:
            li = []
            for c in self.children:
                li.extend(c.leaves())
            return li

    def leaves_iter(self, mapper: Callable[[Self], T] = lambda x: x) -> Iterator[T]:
        if not self.children:
            yield mapper(self) if mapper else self
        else:
            for c in self.children:
                yield from c.leaves_iter(mapper)

    @pydantic.computed_field(repr=False)
    @property
    def leaf_count(self) -> int:
        return sum(1 for _ in self.leaves_iter())

    @pydantic.model_validator(mode='after')
    def leaf_or_list(self):
        if not (self.pts is not None or self.children):
            raise ValueError('Leaf nodes need to have points associated to them.')
        return self

    def bubble_up(self, func: Callable[[Self, Iterable[T]], T]) -> T:
        return func(self, (c.bubble_up(func) for c in self.children)) if self.children else func(self, ())

    def trickle_down(self, func: Callable[[Self, T | None], T], drip_depth: int = 0,
                     parent_value: T | None = None) -> None:
        if drip_depth < 0:
            return

        v = func(self, parent_value)
        if self.children:
            for c in self.children:
                c.trickle_down(func, drip_depth - 1, v)

    def complete(self, completion: Callable[[Self, Iterable[Self]], Self] | None = None) -> Self:
        if not completion:
            def completion(n: Self, children: Iterable[Self]) -> Self:
                s = 0
                for c in children:
                    c.parent = n
                    if not c.get_info('skip') and not c.get_info('skip_in_total'):
                        s += c.pts
                # assert n.pts is None or not had_children
                if n.children:
                    n.pts = s
                return n
        return self.bubble_up(completion)

    def make_self_summary(self) -> Self | None:
        return self.__class__(label=f'Total', pts=self.pts,
                              info={'skip': True, 'summary': True},
                              children=[], parent=self) if (self.children and not self.get_info('skip') and not self.get_info('skip_in_total')) else None

    def add_summaries(self, depth: int = 0) -> None:
        def summarize_children(n: Self, *args):
            if n.children:
                summary = n.make_self_summary()
                if summary:
                    n.children.append(summary)

        self.trickle_down(summarize_children, depth)

    # def collect_ranges(self, start: int = 0) -> Iterator[range]:
    #    if self.is_leaf and (r := self.get_info('summarizes')):
    #        yield range(start, start + r + 1)
    #    else:
    #        leaves_inbetween = 0
    #        for c in self.siblings:
    #            yield from c.collect_ranges(start + leaves_inbetween)
    #            leaves_inbetween += c.leaf_count


GradableNode.model_rebuild()


class WeirdGradableNode(GradableNode):
    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    def from_dict(cls: type[Self], dic) -> Self:
        k, v = next(iter(dic.items()))
        if isinstance(v, list):
            return cls(label=k, children=[cls.from_dict(s) for s in v])
        elif isinstance(v, dict):
            return cls(label=k, **{f: v.pop(f) for f in GradableNode.model_fields.keys() if f in v},
                       info=(v if v else None))
        else:
            return cls(label=k, pts=v)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls: Self, value: Any) -> Self:
        return cls.from_dict(value)

    @pydantic.model_serializer(mode='wrap')
    def serial(self, srlz: pydantic.SerializerFunctionWrapHandler) -> dict:
        if self.children:
            return {self.label: [srlz(sub) for sub in self.children]}
        elif self.info:
            return {self.label: srlz({'pts': self.pts}.update(self.info))}
        else:
            return {self.label: srlz(self.pts)}


class GradableSpec(pydantic.BaseModel):
    levels: list[str] = pydantic.Field(default=DEFAULT_QUESTION_DIVISION_LEVELS)
    tree: Annotated[WeirdGradableNode, pydantic.Field(default_factory=WeirdGradableNode), pydantic.BeforeValidator(
        WeirdGradableNode.from_dict)]

    def get_level(self, level_name: str, filter: Callable[[GradableNode], bool] = None) -> list[GradableNode]:
        return [n for n in self.tree.iter_level(self.levels.index(level_name)) if not filter or filter(n)]

    def cutoff(self, depth: int) -> GradableSpec:
        return GradableSpec(levels=self.levels[:depth + 1], tree=self.tree.cutoff(depth))


def load_spec(spec_path: str, custom_completion_func: Callable[[GradableNode, Iterable[
    GradableNode]], GradableNode] | None = None) -> GradableSpec:
    with open(spec_path, 'r') as spec_file:
        spec = yaml.load(spec_file, Loader=yaml.FullLoader)
        gradable_spec = GradableSpec.model_validate(spec)
        gradable_spec.tree.complete(custom_completion_func)
        return gradable_spec
