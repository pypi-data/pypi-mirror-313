import dataclasses
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence, Sized
from typing import Any, Generic, Optional, TypeVar, cast

import colt
from mpire import WorkerPool

from harbory.common.iterutils import SizedIterator, batched
from harbory.types import BaseModel, IDataclass, INamedTuple, T_DataContainer

# inputs/outputs
S = TypeVar("S")
T = TypeVar("T")
U = TypeVar("U")
# fixtures
E = TypeVar("E")
F = TypeVar("F")
# runtime params
P = TypeVar("P")
Q = TypeVar("Q")


class Processor(Generic[S, T, F, P], colt.Registrable):
    """
    A base class for processors.

    To define a processor, inherit this class and implement the `apply` method, which
    applies the processor to a single input. The `apply_batch` method is implemented
    in terms of `apply`, and can be overridden for efficiency.

    Here is an example of processor that tokenizes a string by splitting on spaces:

    Example:
        >>> class MyProcessor(Processor[str, list[str], None, None]):
        >>>     fixtures = None
        >>>
        >>>     def apply_batch(self, inputs: list[str], fixtures: None, params: None) -> list[str]:
        >>>         return [x.split() for x in inputs]

    To apply the processor to a sequence of inputs, call the processor object as a
    function. The `batch_size` argument controls the number of inputs to process
    at a time. The `max_workers` argument controls the number of threads to use
    for multi-thread processing. For example, to apply the processor to a sequence
    of inputs, 100 at a time, using 4 threads, do the following:

    Example:
        >>> processor = MyProcessor()
        >>> inputs = ["This is a test.", "This is another test.", ...]
        >>> outputs = processor(inputs, batch_size=100, max_workers=4)

    Chaining processors together is done using the `|` operator. For example, to
    create a processor consisting of three steps, `first_step`, `second_step`, and
    `third_step`, do the following:

    Example:
        >>> first_step = FirstProcessor()
        >>> second_step = SecondProcessor()
        >>> third_step = ThirdProcessor()
        >>> processor = first_step | second_step | third_step

    Args:
        batch_size: The batch size. Defaults to `1`.
        max_workers: The maximum number of workers to use for multi-thread
            processing. Defaults to `1`.
    """

    def __init__(
        self,
        *,
        batch_size: int = 1,
        max_workers: int = 1,
    ) -> None:
        if batch_size < 1:
            raise ValueError("batch_size must be at least 1")
        if max_workers < 1:
            raise ValueError("max_workers must be at least 1")

        self._batch_size = batch_size
        self._max_workers = max_workers

    @property
    def fixtures(self) -> F:
        raise NotImplementedError

    def apply_batch(
        self,
        batch: Sequence[S],
        fixtures: F,
        params: Optional[P] = None,
    ) -> list[T]:
        """
        Apply the processor to a batch of inputs.

        Args:
            batch: The batch of inputs.
            fixtures: The fixtures to use.
            params: The runtime parameters.

        Returns:
            The batch of outputs.
        """

        raise NotImplementedError

    def apply(
        self,
        x: S,
        params: Optional[P] = None,
    ) -> T:
        """
        Apply the processor to a single input.

        Args:
            x: The input.
            params: The runtime parameters.

        Returns:
            The output.
        """

        return self.apply_batch([x], self.fixtures, params)[0]

    def __call__(
        self,
        inputs: Iterable[S],
        params: Optional[P] = None,
        *,
        batch_size: Optional[int] = None,
        max_workers: Optional[int] = None,
    ) -> Iterator[T]:
        """
        Apply the processor to a sequence of inputs.

        Args:
            inputs: The sequence of inputs.
            params: The runtime parameters.
            batch_size: The batch size. Defaults to `1`.
            max_workers: The maximum number of workers to use for multi-thread
                processing. Defaults to `1`.

        Returns:
            An iterator over the outputs.
        """

        batch_size = batch_size or self._batch_size or 1
        max_workers = max_workers or self._max_workers or 1

        assert batch_size is not None
        assert max_workers is not None

        if batch_size < 1:
            raise ValueError("batch_size must be at least 1")
        if max_workers < 1:
            raise ValueError("max_workers must be at least 1")

        def iterator() -> Iterator[T]:
            assert batch_size is not None
            assert max_workers is not None

            if max_workers < 2:
                fixtures = self.fixtures
                for batch in batched(inputs, batch_size):
                    yield from self.apply_batch(batch, fixtures, params)
            else:

                def apply_batch(shared_objects: tuple[F, Optional[P]], *batch: S) -> list[T]:
                    fixtures, params = shared_objects
                    return self.apply_batch(batch, fixtures, params)

                with WorkerPool(
                    n_jobs=max_workers,
                    shared_objects=(self.fixtures, params),
                ) as pool:
                    for results in pool.imap(
                        apply_batch,
                        batched(inputs, batch_size),
                    ):
                        yield from results

        if isinstance(inputs, Sized):
            return SizedIterator(iterator(), len(inputs))

        return iterator()

    def __or__(self, other: "Processor[T, U, E, Q]") -> "Processor[S, U, tuple[F, E], tuple[P, Q]]":
        return ComposeProcessor(self, other)

    @classmethod
    def from_callable(
        cls,
        func: Callable[[Sequence[S], F, Optional[Q]], list[T]],
        fixtures: F,
        **kwargs: Any,
    ) -> "Processor[S, T, F, Q]":
        """
        Create a processor from a callable.

        Args:
            func: The callable.
            fixtures: The fixtures to use.

        Returns:
            The processor.
        """

        return CallableProcessor(func, fixtures, **kwargs)


@Processor.register("compose")
class ComposeProcessor(Processor[S, U, tuple[E, F], tuple[P, Q]]):
    """
    A processor that is the composition of two processors.

    Args:
        first: The first processor.
        second: The second processor.
        batch_size: The batch size. Defaults to `1`.
        max_workers: The maximum number of workers to use for multi-thread
            processing. Defaults to `1`.
    """

    def __init__(
        self,
        first: Processor[S, T, E, P],
        second: Processor[T, U, F, Q],
        *,
        batch_size: int = 1,
        max_workers: int = 1,
    ):
        super().__init__(batch_size=batch_size, max_workers=max_workers)
        self.first = first
        self.second = second

    def apply_batch(
        self,
        batch: Sequence[S],
        fixtures: tuple[E, F],
        params: Optional[tuple[Optional[P], Optional[Q]]] = None,
    ) -> list[U]:
        params = params or (None, None)
        return self.second.apply_batch(self.first.apply_batch(batch, fixtures[0], params[0]), fixtures[1], params[1])

    def __call__(
        self,
        inputs: Iterable[S],
        params: Optional[tuple[Optional[P], Optional[Q]]] = None,
        *,
        batch_size: Optional[int] = None,
        max_workers: Optional[int] = None,
    ) -> Iterator[U]:
        params = params or (None, None)
        return self.second(
            self.first(
                inputs,
                params[0],
                batch_size=batch_size,
                max_workers=max_workers,
            ),
            params[1],
            batch_size=batch_size,
            max_workers=max_workers,
        )


@Processor.register("callable")
class CallableProcessor(Processor[S, T, F, P]):
    """
    A processor that can be created from a callable.

    Args:
        func: The callable.
        batch_size: The batch size. Defaults to `1`.
        max_workers: The maximum number of workers to use for multi-thread
            processing. Defaults to `1`.
    """

    def __init__(
        self,
        func: Callable[[Sequence[S], F, Optional[P]], list[T]],
        fixtures: F,
        *,
        batch_size: int = 1,
        max_workers: int = 1,
    ) -> None:
        super().__init__(batch_size=batch_size, max_workers=max_workers)
        self._func = func
        self._fixtures = fixtures

    @property
    def fixtures(self) -> F:
        return self._fixtures

    def apply_batch(
        self,
        batch: Sequence[S],
        fixtures: F,
        params: Optional[P] = None,
    ) -> list[T]:
        return self._func(batch, fixtures, params)


@Processor.register("chain")
class ChainProcessor(Processor[S, S, list[Any], list[Any]]):
    """
    A processor that is the composition of multiple processors.
    Note that each processor must have the same input and output types.

    Args:
        steps: The sequence of processors.
        batch_size: The batch size. Defaults to `1`.
        max_workers: The maximum number of workers to use for multi-thread
    """

    def __init__(
        self,
        steps: Sequence[Processor[S, S, Any, Any]],
        batch_size: int = 1,
        max_workers: int = 1,
    ) -> None:
        super().__init__(batch_size=batch_size, max_workers=max_workers)
        self._steps = steps or [PassThroughProcessor()]

    @property
    def fixtures(self) -> list[Any]:
        return [step.fixtures() for step in self._steps]

    def apply_batch(
        self,
        batch: Sequence[S],
        fixtures: list[Any],
        params: Optional[list[Any]] = None,
    ) -> list[S]:
        if params is not None and len(params) != len(self._steps):
            raise ValueError("params must have the same length as steps")
        params = params or [None] * len(self._steps)
        for s, f, p in zip(self._steps, fixtures, params):
            batch = s.apply_batch(batch, f, p)
        return list(batch)

    def __call__(
        self,
        inputs: Iterable[S],
        params: Optional[list[Any]] = None,
        *,
        batch_size: Optional[int] = None,
        max_workers: Optional[int] = None,
    ) -> Iterator[S]:
        if params is not None and len(params) != len(self._steps):
            raise ValueError("params must have the same length as steps")
        params = params or [None] * len(self._steps)
        output = self._steps[0](inputs, params[0], batch_size=batch_size, max_workers=max_workers)
        for step, param in zip(self._steps[1:], params[1:]):
            output = step(output, param, batch_size=batch_size, max_workers=max_workers)
        return output


@Processor.register("pass_through")
class PassThroughProcessor(Processor[S, S, None, None]):
    """
    A processor that does nothing.
    """

    fixtures = None

    def apply_batch(
        self,
        batch: Sequence[S],
        fixtures: None,
        params: None = None,
    ) -> list[S]:
        return list(batch)


@Processor.register("field")
class FieldProcessor(
    Processor[
        T_DataContainer,
        T_DataContainer,
        Mapping[str, Any],
        Mapping[str, Any],
    ]
):
    """
    A processor that applies a function to a field of a data container.
    """

    def __init__(
        self,
        processors: Mapping[str, Processor[Any, Any, Any, Any]],
        batch_size: int = 1,
        max_workers: int = 1,
    ) -> None:
        super().__init__(batch_size=batch_size, max_workers=max_workers)
        self._processors = processors

    @property
    def fixtures(self) -> Mapping[str, Any]:
        return {field: processor.fixtures for field, processor in self._processors.items()}

    def _get_field_value(self, item: T_DataContainer, field: str) -> Any:
        if isinstance(item, dict):
            return item[field]
        if isinstance(item, IDataclass):
            if field in item.__dataclass_fields__:
                return getattr(item, field)
            raise ValueError(f"Field '{field}' not found in data container")
        if isinstance(item, INamedTuple):
            if field in item._fields:
                return getattr(item, field)
            raise ValueError(f"Field '{field}' not found in data container")
        if isinstance(item, BaseModel):
            if field in item.model_fields:
                return getattr(item, field)
            raise ValueError(f"Field '{field}' not found in data container")
        raise ValueError("Data container must be a dict, a pydantic model or a dataclass")

    def _replace_field_value(self, item: T_DataContainer, field: str, value: Any) -> T_DataContainer:
        if isinstance(item, dict):
            return cast(T_DataContainer, {**item, field: value})
        if isinstance(item, IDataclass):
            return cast(T_DataContainer, dataclasses.replace(item, **{field: value}))
        if isinstance(item, INamedTuple):
            return cast(T_DataContainer, item._replace(**{field: value}))
        if isinstance(item, BaseModel):
            return cast(T_DataContainer, item.model_copy(update={field: value}))
        raise ValueError(f"Unsupported type: {type(item)}")

    def apply_batch(
        self,
        batch: Sequence[T_DataContainer],
        fixtures: Mapping[str, Any],
        params: Optional[Mapping[str, Any]] = None,
    ) -> list[T_DataContainer]:
        for key, processor in self._processors.items():
            field_fixtures = fixtures[key]
            field_params = params[key] if params is not None else None
            field_batch = [self._get_field_value(item, key) for item in batch]
            outputs = processor.apply_batch(field_batch, field_fixtures, field_params)
            batch = [self._replace_field_value(item, key, output) for item, output in zip(batch, outputs)]
        return list(batch)
