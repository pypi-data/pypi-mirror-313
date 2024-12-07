"""This file is used to test static typing, it's analyzed with pyright and mypy."""

from collections.abc import Awaitable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable, Union, assert_type

from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.result import RunResult


@dataclass
class MyDeps:
    foo: int
    bar: int


typed_agent = Agent(deps_type=MyDeps, result_type=str)
assert_type(typed_agent, Agent[MyDeps, str])


@typed_agent.system_prompt
async def system_prompt_ok1(ctx: RunContext[MyDeps]) -> str:
    return f'{ctx.deps}'


@typed_agent.system_prompt
def system_prompt_ok2() -> str:
    return 'foobar'


# we have overloads for every possible signature of system_prompt, so the type of decorated functions is correct
assert_type(system_prompt_ok1, Callable[[RunContext[MyDeps]], Awaitable[str]])
assert_type(system_prompt_ok2, Callable[[], str])


@contextmanager
def expect_error(error_type: type[Exception]) -> Iterator[None]:
    try:
        yield None
    except Exception as e:
        assert isinstance(e, error_type), f'Expected {error_type}, got {type(e)}'
    else:
        raise AssertionError('Expected an error')


@typed_agent.tool
async def ok_tool(ctx: RunContext[MyDeps], x: str) -> str:
    assert_type(ctx.deps, MyDeps)
    total = ctx.deps.foo + ctx.deps.bar
    return f'{x} {total}'


# we can't add overloads for every possible signature of tool, so the type of ok_tool is obscured
assert_type(ok_tool, Callable[[RunContext[MyDeps], str], str])  # type: ignore[assert-type]


@typed_agent.tool_plain
def ok_tool_plain(x: str) -> dict[str, str]:
    return {'x': x}


@typed_agent.tool_plain
async def ok_json_list(x: str) -> list[Union[str, int]]:
    return [x, 1]


@typed_agent.tool
async def ok_ctx(ctx: RunContext[MyDeps], x: str) -> list[int | str]:
    return [ctx.deps.foo, ctx.deps.bar, x]


@typed_agent.tool
async def bad_tool1(ctx: RunContext[MyDeps], x: str) -> str:
    total = ctx.deps.foo + ctx.deps.spam  # type: ignore[attr-defined]
    return f'{x} {total}'


@typed_agent.tool  # type: ignore[arg-type]
async def bad_tool2(ctx: RunContext[int], x: str) -> str:
    return f'{x} {ctx.deps}'


with expect_error(ValueError):

    @typed_agent.tool  # type: ignore[arg-type]
    async def bad_tool3(x: str) -> str:
        return x


@typed_agent.result_validator
def ok_validator_simple(data: str) -> str:
    return data


@typed_agent.result_validator
async def ok_validator_ctx(ctx: RunContext[MyDeps], data: str) -> str:
    if ctx.deps.foo == 1:
        raise ModelRetry('foo is 1')
    return data


# we have overloads for every possible signature of result_validator, so the type of decorated functions is correct
assert_type(ok_validator_simple, Callable[[str], str])
assert_type(ok_validator_ctx, Callable[[RunContext[MyDeps], str], Awaitable[str]])


@typed_agent.result_validator  # type: ignore[arg-type]
async def result_validator_wrong(ctx: RunContext[int], result: str) -> str:
    return result


def run_sync() -> None:
    result = typed_agent.run_sync('testing', deps=MyDeps(foo=1, bar=2))
    assert_type(result, RunResult[str])
    assert_type(result.data, str)


async def run_stream() -> None:
    async with typed_agent.run_stream('testing', deps=MyDeps(foo=1, bar=2)) as streamed_result:
        result_items = [chunk async for chunk in streamed_result.stream()]
        assert_type(result_items, list[str])


def run_with_override() -> None:
    with typed_agent.override(deps=MyDeps(1, 2)):
        typed_agent.run_sync('testing', deps=MyDeps(3, 4))

    # invalid deps
    with typed_agent.override(deps=123):  # type: ignore[arg-type]
        typed_agent.run_sync('testing', deps=MyDeps(3, 4))


@dataclass
class Foo:
    a: int


@dataclass
class Bar:
    b: str


union_agent: Agent[None, Union[Foo, Bar]] = Agent(
    result_type=Union[Foo, Bar],  # type: ignore[arg-type]
)
assert_type(union_agent, Agent[None, Union[Foo, Bar]])


def run_sync3() -> None:
    result = union_agent.run_sync('testing')
    assert_type(result, RunResult[Union[Foo, Bar]])
    assert_type(result.data, Union[Foo, Bar])


def foobar_ctx(ctx: RunContext[int], x: str, y: int) -> str:
    return f'{x} {y}'


def foobar_plain(x: str, y: int) -> str:
    return f'{x} {y}'


Tool(foobar_ctx, True)
Tool(foobar_plain, False)

# unfortunately we can't type check these cases, since from a typing perspect `foobar_ctx` is valid as a plain tool
Tool(foobar_ctx, False)
Tool(foobar_plain, True)

Agent('test', tools=[foobar_ctx], deps_type=int)
Agent('test', tools=[foobar_plain], deps_type=int)
Agent('test', tools=[foobar_plain])
Agent('test', tools=[Tool(foobar_ctx, True)], deps_type=int)
Agent('test', tools=[Tool(foobar_plain, False)], deps_type=int)
Agent('test', tools=[Tool(foobar_ctx, True), foobar_ctx, foobar_plain], deps_type=int)

Agent('test', tools=[foobar_ctx], deps_type=str)  # pyright: ignore[reportArgumentType]
Agent('test', tools=[foobar_ctx])  # pyright: ignore[reportArgumentType]
Agent('test', tools=[Tool(foobar_ctx, True)])  # pyright: ignore[reportArgumentType]
