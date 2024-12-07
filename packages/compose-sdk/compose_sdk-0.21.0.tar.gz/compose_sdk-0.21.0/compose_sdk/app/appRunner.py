import inspect
import io
from typing import Any, TypedDict, Callable, Union, Dict, Literal

from ..scheduler import Scheduler
from ..api import (
    ApiHandler,
    encode_string,
    encode_num_to_four_bytes,
    combine_buffers,
)
from ..core import (
    Utils,
    EventType,
    Render,
    ComponentInstance,
    INTERACTION_TYPE,
    TYPE,
    JSON,
    page_confirm,
    CONFIRM_APPEARANCE,
    CONFIRM_APPEARANCE_DEFAULT,
    RENDER_APPEARANCE,
    MODAL_WIDTH,
    RENDER_APPEARANCE_DEFAULT,
    MODAL_WIDTH_DEFAULT,
)

from .appDefinition import AppDefinition
from .state import State
from .page import Page, Config as PageConfig, Params as PageParams


class ConfirmationDialog(TypedDict):
    id: str
    is_active: bool
    resolve: Callable[[bool], None]
    cleanup: Callable[[], None]


class RenderObj(TypedDict):
    resolve: Callable[[Any], None]
    cleanup: Callable[[], None]
    layout: Any
    static_layout: Any
    appearance: RENDER_APPEARANCE
    modal_header: str
    modal_width: MODAL_WIDTH


DELETED_RENDER = "DELETED"
DeletedRender = Literal["DELETED"]


class AppRunner:
    def __init__(
        self,
        scheduler: Scheduler,
        api: ApiHandler,
        appDefinition: AppDefinition,
        executionId: str,
        browserSessionId: str,
    ):
        self.scheduler = scheduler
        self.api = api
        self.appDefinition = appDefinition
        self.executionId = executionId
        self.browserSessionId = browserSessionId

        self.renders: Dict[str, Union[RenderObj, DeletedRender]] = {}
        self.tempFiles = {}

        self.execution_task = None

        self.confirmationDialog: Union[ConfirmationDialog, None] = None

    async def render_ui(
        self,
        layout: Any,
        *,
        appearance: RENDER_APPEARANCE = RENDER_APPEARANCE_DEFAULT,
        modal_header: str = None,
        modal_width: MODAL_WIDTH = MODAL_WIDTH_DEFAULT,
    ) -> Any:
        try:
            future = self.scheduler.create_future()

            async def _resolve_render(data=None):
                if not future.done():
                    future.set_result(data)

                if appearance == "modal":
                    await self.api.send(
                        {
                            "type": EventType.SdkToServer.CLOSE_MODAL,
                            "executionId": self.executionId,
                            "renderId": renderId,
                        },
                        self.browserSessionId,
                    )

                    # After the modal is closed, we no longer need to track it.
                    self.renders[renderId] = DELETED_RENDER

            def resolve_render(data=None):
                self.scheduler.create_task(_resolve_render(data))

            def cleanup():
                if not future.done():
                    future.cancel()

            renderId = Utils.generate_id()

            static_layout = Render.generate_static_layout(layout, resolve_render)

            self.renders[renderId] = {
                "resolve": resolve_render,
                "layout": layout,
                "static_layout": static_layout,
                "cleanup": cleanup,
                "appearance": appearance,
                "modal_header": modal_header,
                "modal_width": modal_width,
            }

            optional_params = {
                "modalHeader": modal_header,
                "modalWidth": modal_width,
            }

            final_params = {
                "type": EventType.SdkToServer.RENDER_UI,
                "ui": static_layout,
                "executionId": self.executionId,
                "renderId": renderId,
                "appearance": appearance,
            }

            for key, value in optional_params.items():
                if value is not None:
                    final_params[key] = value

            await self.api.send(
                final_params,
                self.browserSessionId,
            )
        except Exception as error:
            await self.__send_error(
                f"An error occurred in the page.add fragment:\n\n{str(error)}"
            )

        return await future

    async def confirm(
        self,
        *,
        title: str = None,
        message: str = None,
        type_to_confirm_text: str = None,
        confirm_button_label: str = None,
        cancel_button_label: str = None,
        appearance: CONFIRM_APPEARANCE = CONFIRM_APPEARANCE_DEFAULT,
    ):
        if self.confirmationDialog is not None and self.confirmationDialog["is_active"]:
            await self.__send_error(
                "Trying to open a confirmation dialog while another one is already open"
            )

            return False

        future = self.scheduler.create_future()

        def resolve_confirm(response: bool):
            if not future.done():
                self.confirmationDialog["is_active"] = False
                future.set_result(response)

        def cleanup():
            if not future.done():
                self.confirmationDialog["is_active"] = False
                future.cancel()

        id = Utils.generate_id()

        self.confirmationDialog = {
            "id": id,
            "is_active": True,
            "resolve": resolve_confirm,
            "cleanup": cleanup,
        }

        component = page_confirm(
            id,
            resolve_confirm,
            title=title,
            message=message,
            type_to_confirm_text=type_to_confirm_text,
            confirm_button_label=confirm_button_label,
            cancel_button_label=cancel_button_label,
            appearance=appearance,
        )

        await self.api.send(
            {
                "type": EventType.SdkToServer.CONFIRM,
                "executionId": self.executionId,
                "component": component,
            },
            self.browserSessionId,
        )

        return await future

    async def toast(
        self,
        message: str,
        title: str = None,
        appearance: str = None,
        duration: str = None,
    ):
        def get_options():
            options = {}

            if title is not None:
                options["title"] = title
            if appearance is not None:
                options["appearance"] = appearance
            if duration is not None:
                options["duration"] = duration

            if len(options) == 0:
                return None

            return options

        options = get_options()

        await self.api.send(
            {
                "type": EventType.SdkToServer.TOAST,
                "message": message,
                "options": options,
                "executionId": self.executionId,
            },
            self.browserSessionId,
        )

    async def page_loading(
        self, value: bool = None, text: str = None, disable_interaction: bool = None
    ):
        def get_options():
            options = {}

            if text is not None:
                options["text"] = text
            if disable_interaction is not None:
                options["disableInteraction"] = disable_interaction

            if len(options) == 0:
                return None

            return options

        options = get_options()

        ws_message = {
            "type": EventType.SdkToServer.UPDATE_LOADING,
            "value": value,
            "executionId": self.executionId,
        }

        if options is not None:
            ws_message["properties"] = options

        await self.api.send(
            ws_message,
            self.browserSessionId,
        )

    async def set_config(self, config: PageConfig):
        await self.api.send(
            {
                "type": EventType.SdkToServer.PAGE_CONFIG,
                "config": config,
                "executionId": self.executionId,
            },
            self.browserSessionId,
        )

    async def on_state_update(self):
        updated_renders = {}

        for renderId in self.renders:
            if self.renders[renderId] == DELETED_RENDER:
                continue

            layout = self.renders[renderId]["layout"]

            # No need to check for changes for static layouts
            if not callable(layout):
                continue

            resolve_fn = self.renders[renderId]["resolve"]

            try:
                new_static_layout = Render.generate_static_layout(layout, resolve_fn)
            except Exception as error:
                return await self.__send_error(
                    f"An error occurred while re-rendering the UI:\n\n{str(error)}"
                )

            validation_error = Render.validate_static_layout(new_static_layout)

            if validation_error is not None:
                return await self.__send_error(
                    f"An error occurred while re-rendering the UI:\n\n{validation_error}"
                )

            diff = Render.diff_static_layouts(
                self.renders[renderId]["static_layout"], new_static_layout
            )

            # When we perform a diff, we don't update the IDs of existing
            # components (even if they're updated). Instead, in these cases,
            # we apply the old IDs onto the new layout so that the SDK layout
            # stays in sync with the client-side layout.
            #
            # For example, if we have an initial render, then a state update where
            # the render doesn't change, then a 2nd state update where we delete
            # a component, both state updates will produce a new static layout
            # with completely new IDs. But, after the first state update, we
            # don't send anything to the client, hence the client IDs will
            # still be the old IDs.
            #
            # By applying the old IDs onto the new layout, we ensure that
            # the render mappings between SDK and client stay in sync so
            # that when we finally do send a delete command to the client,
            # the ID is recognized.
            self.renders[renderId]["static_layout"] = diff[
                "new_layout_with_ids_applied"
            ]

            if not diff["did_change"]:
                continue

            updated_renders[renderId] = {
                "add": diff["add"],
                "delete": diff["delete"],
                "update": diff["update"],
                "rootId": diff["root_id"],
                "metadata": diff["metadata"],
            }

        if len(updated_renders) > 0:
            await self.api.send(
                {
                    "type": EventType.SdkToServer.RERENDER_UI_V2,
                    "executionId": self.executionId,
                    "diff": updated_renders,
                },
                self.browserSessionId,
            )

    async def set_inputs(self, values: Dict[str, Any]):
        if not isinstance(values, dict):
            await self.__send_error(
                f"An error occurred while trying to set input values:\n\nExpected a dictionary, but received {type(values).__name__}",
                "warning",
            )
            return

        for input_id in values:
            was_found = False

            for render_id in self.renders:
                if self.renders[render_id] == DELETED_RENDER:
                    continue

                static_layout = self.renders[render_id]["static_layout"]
                component = Render.find_component_by_id(static_layout, input_id)

                if component is not None:
                    if was_found is True:
                        await self.__send_error(
                            f"An error occurred while trying to set an input value:\n\nMultiple inputs were found with the same ID: {input_id}",
                            "warning",
                        )
                        return
                    elif component["type"] == TYPE.INPUT_FILE_DROP:
                        await self.__send_error(
                            f"Inputs of type {component['type']} cannot be set using the page.setInput method",
                            "warning",
                        )
                        return

                    was_found = True

            if was_found is False:
                await self.__send_error(
                    f"An error occurred while trying to set an input value:\n\nNo input was found with the ID: {input_id}",
                    "warning",
                )
                return

        await self.api.send(
            {
                "type": EventType.SdkToServer.SET_INPUTS,
                "executionId": self.executionId,
                "inputs": values,
            },
            self.browserSessionId,
        )

    async def download(self, file: Union[bytes, io.BufferedIOBase], filename: str):
        if isinstance(file, io.BufferedIOBase):
            file.seek(0)
            file_content = file.read()
        elif isinstance(file, bytes):
            file_content = file
        else:
            raise TypeError(
                "The 'file' argument must be of type 'bytes' or a bytes-like object that supports the read() method (e.g., BytesIO). "
                "Please provide the file content as bytes or a bytes-like object."
            )

        metadata = {
            "name": filename,
            "download": True,
            "executionId": self.executionId,
            "id": Utils.generate_id(),
        }

        metadata_str = JSON.stringify(metadata)

        header_binary = encode_string(
            EventType.SdkToServer.FILE_TRANSFER + self.browserSessionId
        )

        metadata_length_binary = encode_num_to_four_bytes(len(metadata_str))

        metadata_binary = encode_string(metadata_str)

        message = combine_buffers(
            header_binary, metadata_length_binary, metadata_binary, file_content
        )

        await self.api.send_raw(message)

    async def link(
        self, appRouteOrUrl: str, newTab: bool = True, params: PageParams = {}
    ):
        await self.api.send(
            {
                "type": EventType.SdkToServer.LINK,
                "appRouteOrUrl": appRouteOrUrl,
                "newTab": newTab,
                "executionId": self.executionId,
                "params": params,
            },
            self.browserSessionId,
        )

    async def reload(self):
        await self.api.send(
            {
                "type": EventType.SdkToServer.RELOAD_PAGE,
                "executionId": self.executionId,
            },
            self.browserSessionId,
        )

    async def __send_error(
        self, errorMsg: str, severity: Literal["error", "warning"] = "error"
    ):
        await self.api.send(
            {
                "type": EventType.SdkToServer.APP_ERROR,
                "errorMessage": errorMsg,
                "executionId": self.executionId,
                "severity": severity,
            },
            self.browserSessionId,
        )

    async def execute(self, params: PageParams):
        state = State(self, self.appDefinition.initial_state)
        page = Page(self, params, state)

        try:
            handler = self.appDefinition.handler
            handler_params = inspect.signature(handler).parameters
            kwargs = {}
            if "page" in handler_params:
                kwargs["page"] = page
            if "state" in handler_params:
                kwargs["state"] = state
            if "ui" in handler_params:
                kwargs["ui"] = ComponentInstance

            if inspect.iscoroutinefunction(self.appDefinition.handler):
                await self.appDefinition.handler(**kwargs)
            else:
                self.appDefinition.handler(**kwargs)
        except Exception as error:
            await self.__send_error(
                f"An error occurred while running the app:\n\n{str(error)}"
            )

    async def on_click_hook(self, component_id: str, render_id: str):
        if render_id not in self.renders:
            return

        if self.renders[render_id] == DELETED_RENDER:
            return

        static_layout = self.renders[render_id]["static_layout"]

        component = Render.find_component_by_id(static_layout, component_id)

        if (
            component is None
            or component["interactionType"] is not INTERACTION_TYPE.BUTTON
        ):
            return

        hookFunc = component["hooks"]["onClick"]

        if hookFunc is not None:
            try:
                if inspect.iscoroutinefunction(hookFunc):
                    await hookFunc()
                else:
                    hookFunc()
            except Exception as error:
                await self.__send_error(
                    f"An error occurred while executing a callback function:\n\n{str(error)}"
                )

    async def on_submit_form_hook(
        self, form_component_id: str, render_id: str, form_data: dict
    ):
        if render_id not in self.renders:
            return

        if self.renders[render_id] == DELETED_RENDER:
            return

        hydrated, temp_files_to_delete = Render.hydrate_form_data(
            form_data, self.tempFiles
        )

        for file_id in temp_files_to_delete:
            del self.tempFiles[file_id]

        static_layout = self.renders[render_id]["static_layout"]
        component = Render.find_component_by_id(static_layout, form_component_id)

        if component is None or component["type"] != TYPE.LAYOUT_FORM:
            return

        input_errors = await Render.get_form_input_errors(hydrated, static_layout)
        form_error = await Render.get_form_error(component, hydrated)

        if input_errors is not None or form_error is not None:
            await self.api.send(
                {
                    "type": EventType.SdkToServer.FORM_VALIDATION_ERROR,
                    "renderId": render_id,
                    "inputComponentErrors": input_errors,
                    "formError": form_error,
                    "executionId": self.executionId,
                    "formComponentId": form_component_id,
                },
                self.browserSessionId,
            )

            return

        hookFunc = component["hooks"]["onSubmit"]

        if hookFunc is not None:
            await self.api.send(
                {
                    "type": EventType.SdkToServer.FORM_SUBMISSION_SUCCESS,
                    "executionId": self.executionId,
                    "renderId": render_id,
                    "formComponentId": form_component_id,
                },
                self.browserSessionId,
            )

            try:
                if inspect.iscoroutinefunction(hookFunc):
                    await hookFunc(hydrated)
                else:
                    hookFunc(hydrated)
            except Exception as error:
                await self.__send_error(
                    f"An error occurred while executing a callback function:\n\n{str(error)}"
                )

    async def on_input_hook(
        self, event_type: str, component_id: str, render_id: str, value: any
    ):
        if render_id not in self.renders:
            return

        if self.renders[render_id] == DELETED_RENDER:
            return

        hydrated, temp_files_to_delete = Render.hydrate_form_data(
            {component_id: value}, self.tempFiles
        )

        for file_id in temp_files_to_delete:
            del self.tempFiles[file_id]

        static_layout = self.renders[render_id]["static_layout"]
        component = Render.find_component_by_id(static_layout, component_id)

        if component is None or component["interactionType"] != INTERACTION_TYPE.INPUT:
            return

        input_errors = await Render.get_form_input_errors(hydrated, static_layout)

        if input_errors is not None:
            error = input_errors[component_id]

            await self.api.send(
                {
                    "type": EventType.SdkToServer.INPUT_VALIDATION_ERROR,
                    "renderId": render_id,
                    "executionId": self.executionId,
                    "error": error,
                    "componentId": component_id,
                },
                self.browserSessionId,
            )

            return

        hookFunc = None
        if event_type == EventType.ServerToSdk.ON_ENTER_HOOK:
            hookFunc = component["hooks"]["onEnter"]
        elif event_type == EventType.ServerToSdk.ON_SELECT_HOOK:
            hookFunc = component["hooks"]["onSelect"]
        elif event_type == EventType.ServerToSdk.ON_FILE_CHANGE_HOOK:
            hookFunc = component["hooks"]["onFileChange"]

        if hookFunc is not None:
            try:
                if inspect.iscoroutinefunction(hookFunc):
                    await hookFunc(hydrated[component_id])
                else:
                    hookFunc(hydrated[component_id])
            except Exception as error:
                await self.__send_error(
                    f"An error occurred while executing a callback function:\n\n{str(error)}"
                )

    async def on_table_row_action_hook(
        self, component_id: str, render_id: str, action_idx: int, value: any
    ):
        if render_id not in self.renders:
            await self.__send_error(
                "An error occurred while trying to execute a table row action hook:\n\nThe render container was not found",
                "warning",
            )
            return

        if self.renders[render_id] == DELETED_RENDER:
            return

        static_layout = self.renders[render_id]["static_layout"]
        component = Render.find_component_by_id(static_layout, component_id)

        if component is None:
            await self.__send_error(
                "An error occurred while trying to execute a table row action hook:\n\nThe component was not found",
                "warning",
            )
            return

        if component["type"] != TYPE.INPUT_TABLE:
            await self.__send_error(
                "An error occurred while trying to execute a table row action hook:\n\nThe component is not a table",
                "warning",
            )
            return

        if (
            component["hooks"]["onRowActions"] is None
            or len(component["hooks"]["onRowActions"]) <= action_idx
        ):
            await self.__send_error(
                "An error occurred while trying to execute a table row action hook:\n\nThe row action was not found",
                "warning",
            )
            return

        hookFunc = component["hooks"]["onRowActions"][action_idx]

        try:
            if inspect.iscoroutinefunction(hookFunc):
                await hookFunc(value)
            else:
                hookFunc(value)
        except Exception as error:
            await self.__send_error(
                f"An error occurred while executing a callback function:\n\n{str(error)}"
            )

    async def on_confirm_response_hook(self, id: str, response: bool):
        if self.confirmationDialog is None or self.confirmationDialog["id"] != id:
            await self.__send_error(
                "An error occurred while trying to resolve a confirmation dialog:\n\nThe confirmation dialog was not found",
                "warning",
            )
            return

        self.confirmationDialog["resolve"](response)

    def on_close_modal(self, render_id: str):
        if render_id not in self.renders:
            return

        if self.renders[render_id] == DELETED_RENDER:
            return

        self.renders[render_id]["resolve"](None)

    def on_file_transfer(self, file_id: str, file_contents: bytes):
        self.tempFiles[file_id] = file_contents

    def cleanup(self):
        try:
            for render in self.renders.values():
                if render == DELETED_RENDER:
                    continue

                render["cleanup"]()

            if self.confirmationDialog is not None:
                self.confirmationDialog["cleanup"]()

            if self.execution_task is not None and not self.execution_task.done():
                self.execution_task.cancel()
        except Exception as error:
            print(f"Error cleaning up app runner: {error}")
