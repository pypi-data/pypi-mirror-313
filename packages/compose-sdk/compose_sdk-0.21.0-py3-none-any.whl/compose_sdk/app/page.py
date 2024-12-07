import io
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    TypedDict,
    Union,
    Callable,
    Literal,
    Union,
)
from ..core import (
    ComponentReturn,
    CONFIRM_APPEARANCE,
    CONFIRM_APPEARANCE_DEFAULT,
    MODAL_WIDTH,
    MODAL_WIDTH_DEFAULT,
)
from .state import State

if TYPE_CHECKING:
    from .appRunner import AppRunner


class Config(TypedDict, total=False):
    width: str
    padding_top: str
    padding_bottom: str
    padding_left: str
    padding_right: str
    padding_x: str
    padding_y: str
    spacing_y: str


TOAST_APPEARANCE = Literal["success", "error", "warning", "info"]
TOAST_DURATION = Literal["shortest", "short", "medium", "long", "longest", "infinite"]
DEFAULT_TOAST_APPEARANCE: TOAST_APPEARANCE = "info"
DEFAULT_TOAST_DURATION: TOAST_DURATION = "medium"


resolve = Callable[[Any], None]
staticLayout = Union[ComponentReturn, list[ComponentReturn]]

Params = dict[str, Union[str, int, bool]]

Layout = Union[
    staticLayout, Callable[[resolve], staticLayout], Callable[[], staticLayout]
]


class Page:
    def __init__(self, appRunner: "AppRunner", params: Params, state: State):
        self.__appRunner = appRunner
        self.__params = params if params is not None else {}
        self.__state = state

    @property
    def params(self) -> Params:
        return self.__params

    def add(
        self,
        layout: Layout,
    ) -> Union[Awaitable[Any], Any]:
        return self.__appRunner.scheduler.ensure_future(
            self.__appRunner.render_ui(layout)
        )

    def modal(
        self,
        layout: Layout,
        *,
        title: str = None,
        width: MODAL_WIDTH = MODAL_WIDTH_DEFAULT,
    ) -> Union[Awaitable[Any], Any]:
        return self.__appRunner.scheduler.ensure_future(
            self.__appRunner.render_ui(
                layout, appearance="modal", modal_header=title, modal_width=width
            )
        )

    def download(self, file: Union[bytes, io.BufferedIOBase], filename: str) -> None:
        self.__appRunner.scheduler.create_task(
            self.__appRunner.download(file, filename)
        )

    def set(self, config: Config) -> None:
        """
        Edit the root page configuration. The following properties are available:

        - `width`: The width of the page. Defaults to `"72rem"`.
        - `padding_top`: The padding at the top of the page. Supersedes `padding_y`. Defaults to `"4rem"`.
        - `padding_bottom`: The padding at the bottom of the page. Supersedes `padding_y`. Defaults to `"4rem"`.
        - `padding_left`: The padding at the left of the page. Supersedes `padding_x`. Defaults to `"1rem"`.
        - `padding_right`: The padding at the right of the page. Supersedes `padding_x`. Defaults to `"1rem"`.
        - `padding_x`: The padding at the left and right of the page. Defaults to `"1rem"`.
        - `padding_y`: The padding at the top and bottom of the page. Defaults to `"4rem"`.
        - `spacing_y`: vertical spacing between page.add() renders. Defaults to `"2rem"`.
        """

        # Convert snake_case keys to camelCase
        camel_case_config = {}
        for key, value in config.items():
            if "_" in key:
                words = key.split("_")
                camel_key = words[0] + "".join(word.capitalize() for word in words[1:])
                camel_case_config[camel_key] = value
            else:
                camel_case_config[key] = value

        # Use the converted camelCase config
        self.__appRunner.scheduler.create_task(
            self.__appRunner.set_config(camel_case_config)
        )

    def link(
        self, appRouteOrUrl: str, *, newTab: bool = False, params: Params = {}
    ) -> None:
        """
        Navigate to another Compose App, or link to an external URL.

        If linking to a Compose App, you should define a unique route for the app (`route` param in the App constructor), and then pass that route to this function.

        Furthermore, you can pass a dict of params to the app using the `params` keyword argument. These params will be accessible via `page.params` in the linked app.
        """
        self.__appRunner.scheduler.create_task(
            self.__appRunner.link(appRouteOrUrl, newTab, params)
        )

    def reload(self) -> None:
        """
        Reload the page, which restarts the app.
        """
        self.__appRunner.scheduler.create_task(self.__appRunner.reload())

    def confirm(
        self,
        *,
        title: str = None,
        message: str = None,
        type_to_confirm_text: str = None,
        confirm_button_label: str = None,
        cancel_button_label: str = None,
        appearance: CONFIRM_APPEARANCE = CONFIRM_APPEARANCE_DEFAULT,
    ) -> Awaitable[bool]:
        """
        Display a confirmation dialog to the user.

        Returns a boolean indicating the user's response.
        """
        return self.__appRunner.scheduler.ensure_future(
            self.__appRunner.confirm(
                title=title,
                message=message,
                type_to_confirm_text=type_to_confirm_text,
                confirm_button_label=confirm_button_label,
                cancel_button_label=cancel_button_label,
                appearance=appearance,
            )
        )

    def toast(
        self,
        message: str,
        *,
        title: str = None,
        appearance: TOAST_APPEARANCE = DEFAULT_TOAST_APPEARANCE,
        duration: TOAST_DURATION = DEFAULT_TOAST_DURATION,
    ):
        """
        Display a temporary toast notification to the user.

        Defaults to a `medium` duration and `info` appearance.
        """

        # Pass None if the default value is used so that we know not to send
        # that property over to the browser.
        _appearance = appearance if appearance is not DEFAULT_TOAST_APPEARANCE else None
        _duration = duration if duration is not DEFAULT_TOAST_DURATION else None

        self.__appRunner.scheduler.create_task(
            self.__appRunner.toast(message, title, _appearance, _duration)
        )

    def set_inputs(self, values: dict[str, Any]) -> None:
        """
        Set the values of one or more inputs. Pass in a dictionary with the input ID as the key and the new value as the value.
        """
        self.__appRunner.scheduler.create_task(self.__appRunner.set_inputs(values))

    def loading(
        self, value: bool, *, text: str = None, disable_interaction: bool = None
    ):
        """
        Display a loading indicator on the page. Call the method with a `True`
        value to show in the indicator, then again with a `False` value to
        hide the indicator.

        This method optionally accepts two named arguments:

        - `text`: Text to display next to the loading indicator. This method
        can be called multiple times with different texts to indicate steps
        take during a longer loading state.

        - `disable_interaction`: Disable all user interaction on the page while
        the indicator is active. This is helpful to prevent repeated form
        submissions or other unwanted inputs while loading.
        """
        self.__appRunner.scheduler.create_task(
            self.__appRunner.page_loading(value, text, disable_interaction)
        )

    def update(self):
        """
        Rerender the UI to reflect the latest data.
        """

        self.__state.merge({})
