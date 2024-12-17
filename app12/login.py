import reflex as rx
from .backend.backend import States


@rx.page(route='/login', title='login')
def login_default() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.form.root(
                rx.vstack(
                    rx.form.field(
                        rx.flex(
                            rx.form.label("Email"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Email",
                                    name="email",
                                    type="email",
                                    width="300px",  # Set desired width
                                    height="40px",  # Set desired height
                                ),
                                as_child=True,
                            ),
                            direction="column",
                            spacing="2",
                            aling='center',
                            justify='center'

                        ),
                        name="email",
                        align='center',
                        justify='center'
                    ),
                    rx.form.field(
                        rx.flex(
                            rx.form.label("Password"),
                            rx.form.control(
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    width="300px",  # Set desired width
                                    height="40px",
                                ),
                                as_child=True,
                            ),
                            direction="column",
                            spacing="2",
                            aling='center'
                        ),
                        name="password",
                        align='center'
                    ),
                    rx.form.submit(
                        rx.button("Login"),
                        as_child=True,
                    ),
                    rx.text(States.error_message, color="red"),
                    align='center',
                    justify='center',
                    max_width='400px',
                ),
                on_submit=States.handle_submit,
                justify='center',
                aling='center'
            ),
            border_width="2px",
            border_radius="1em",
            align='center',
            width='100vh',
            height="100vh",
            justify='center',
            max_width='400px',
            spacing="9",
            background_image="url('/drops-6392473_640.jpg')",
        ),
        justify='center'
    )


app = rx.App()
