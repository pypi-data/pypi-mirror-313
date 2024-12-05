# Flask-Failsafe v2

A failsafe for Flask reloader inspired by [Flask-Failsafe](https://github.com/mgood/flask-failsafe).

> [!NOTE]
> This repository made because [Flask-Failsafe](https://github.com/mgood/flask-failsafe) was discontinued.

As said in [Flask-Failsafe](https://github.com/mgood/flask-failsafe), the Flask reloader works great until you make a syntax error and it fails importing your app. This extension helps keep you working smoothly by catching errors during the initialization of your app, and provides a failsafe fallback app to display those startup errors instead.

### Why `flask-failsafe-v2` and why not `Flask-Failsafe`?

1. `flask-failsafe-v2` unlike `Flask-Failsafe` displays exceptions directly from *web browser*. e.g:

    ![Example - web browser showing exception](assets/example_webbrowser_showing_exception.jpg)

2. `flask-failsafe-v2` displays exceptions more *cleaner & prettier* than `Flask-Failsafe` in terminal! e.g:

    ![Example - terminal showing exception](assets/example_terminal_showing_exception.jpg)

3. and more importantly `flask-failsafe-v2` is *easier* and requires *lesser code* than `Flask-Failsafe` to be used! e.g:

    `flask-failsafe-v2`:

    ```py
    from flask_failsafe import failsafe

    failsafe_app = failsafe("example_module:example_app")
    ```

    `Flask-Failsafe`:

    ```py
    from flask_failsafe import failsafe

    @failsafe
    def create_app():
        from example_module import example_app
        return example_app

    failsafe_app = create_app()
    ```

## Installation

To start using this extension, you need to install it, by executing this command:

```bash
pip install flask-failsafe-v2
```

> [!WARNING]
> If the module/extension `Flask-Failsafe` is installed on your device, please uninstall it! this is because `Flask-Failsafe` and `flask-failsafe-v2` share same module name, which can lead to unexpected behavior in your application.

### Optional packages

* `coloredlogs` & `colorama`: Necessary for colored logs!

```bash
pip install coloredlogs colorama
```

## Usage

To start using this extension, you must create a separate module called `dev_app.py` (or whatever you like) from main module in the same folder as main module. After creating the module `dev_app.py`, you will have to write two lines of code which is shown below:

```py
from flask_failsafe import failsafe

failsafe_app = failsafe("example_module:example_app")
```

and then you can just run it from command line by typing:

```bash
flask --app dev_app:failsafe_app --debug run
```

or even, you can add these lines to the code, so you will be able to run it with command `python dev_app.py`:

```py
if __name__ == "__main__":
    failsafe_app.run()
```

and finally, this is the complete code:

```py
from flask_failsafe import failsafe

failsafe_app = failsafe("example_module:example_app")

if __name__ == "__main__":
    failsafe_app.run()
```

## License

Licensed under [MIT License](LICENSE).
