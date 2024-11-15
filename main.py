from fastcore.meta import method
from fasthtml import common as fh


def render_person(person):
    pid = f"person-{person.pid}"
    delete_button = fh.A(
        "Delete", hx_delete=f"/delete/{person.pid}", hx_swap="outerHTML", target_id=pid
    )

    return fh.Li(
        delete_button,
        f"[{person.pid}] {person.name} ({person.age}) - {person.job}",
        id=pid,
    )


app, rt, people, Person = fh.fast_app(
    live=True,
    db_file="data/people.db",
    pid=int,
    name=str,
    age=int,
    job=str,
    pk="pid",
    render=render_person,
)


@rt("/")
def index():
    return fh.Titled(
        "My Title",
        fh.Div(fh.P("Hello World")),
        fh.A("NeuralNine", href="https://neuralnine.com"),
        fh.A("Hello", href="/hello"),
    )


@rt("/hello")
def hello():
    return fh.Div(
        fh.P("Hello World!"),
        fh.A("Back", href="/"),
    )


@rt("/fibonacci/{n}")
def fibonacci(n: int):
    numbers = []

    a, b = 0, 1
    for _ in range(n):
        numbers.append(a)
        b, a = a + b, b

    return fh.Titled("Fibonacci Numbers", fh.Ul(*[fh.Li(num) for num in numbers]))


@rt("/people", methods=["get"])
def list_people():
    create_form = fh.Form(
        fh.Group(
            fh.Label("Name", fh.Input(name="name")),
            fh.Label("Age", fh.Input(name="age", type="number")),
            fh.Label("Job", fh.Input(name="job")),
            fh.Button("Create", type="submit"),
        ),
        hx_post="/people",
        hx_swap="beforeend",
        target_id="people_list",
    )
    return fh.Div(fh.Card(fh.Ul(*people(), id="people_list"), header=create_form))


@rt("/people", methods=["post"])
def create_person(person: Person):
    people.insert(person)


@rt("/delete/{pid}", methods=["delete"])
def delete_person(pid: int):
    people.delete(pid)


fh.serve()
