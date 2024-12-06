from burr.visibility.tracing import trace

if __name__ == "__main__":
    from burr.core import State, action

    @trace()
    def bar():
        return 1

    @trace()
    def baz(a: int, b: int) -> int:
        return a + b

    @trace()
    def foo(a: int, b: int, recursion_count=3) -> int:
        if recursion_count == 0:
            return a + b + baz(a, b)
        return foo(a + 1, b + 1, recursion_count - 1)

    @action(reads=["num"], writes=["num"])
    def act(state: State) -> State:
        num = state["num"]
        return state.update(num=foo(baz(num, num + bar()), num))

    from burr.core.application import Application, ApplicationBuilder

    app: Application = (
        ApplicationBuilder()
        .with_actions(act)
        .with_transitions(("act", "act"))
        .with_tracker(project="test_tracing_decorator")
        .with_state(num=0)
        .with_entrypoint("act")
    ).build()

    i = 0
    for item in app.iterate():
        i += 1
        if i > 10:
            break
        print(item)
