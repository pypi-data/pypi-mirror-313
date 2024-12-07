import io
from typing import Any

from sapiopylib.rest.ClientCallbackService import ClientCallback
from sapiopylib.rest.DataMgmtService import DataMgmtServer
from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.CustomReport import CustomReport, CustomReportCriteria
from sapiopylib.rest.pojo.DataRecord import DataRecord
from sapiopylib.rest.pojo.datatype.DataType import DataTypeDefinition
from sapiopylib.rest.pojo.datatype.DataTypeLayout import DataTypeLayout
from sapiopylib.rest.pojo.datatype.FieldDefinition import AbstractVeloxFieldDefinition, VeloxStringFieldDefinition, \
    VeloxIntegerFieldDefinition, VeloxDoubleFieldDefinition
from sapiopylib.rest.pojo.webhook.ClientCallbackRequest import OptionDialogRequest, ListDialogRequest, \
    FormEntryDialogRequest, InputDialogCriteria, TableEntryDialogRequest, ESigningRequestPojo, \
    DataRecordSelectionRequest, DataRecordDialogRequest, InputSelectionRequest, FilePromptRequest, \
    MultiFilePromptRequest
from sapiopylib.rest.pojo.webhook.ClientCallbackResult import ESigningResponsePojo
from sapiopylib.rest.pojo.webhook.WebhookContext import SapioWebhookContext
from sapiopylib.rest.pojo.webhook.WebhookEnums import FormAccessLevel, ScanToSelectCriteria, SearchType
from sapiopylib.rest.utils.DataTypeCacheManager import DataTypeCacheManager
from sapiopylib.rest.utils.FormBuilder import FormBuilder
from sapiopylib.rest.utils.recorddatasinks import InMemoryRecordDataSink
from sapiopylib.rest.utils.recordmodel.RecordModelWrapper import WrappedType

from sapiopycommons.general.aliases import FieldMap, SapioRecord, AliasUtil, RecordIdentifier
from sapiopycommons.general.custom_report_util import CustomReportUtil
from sapiopycommons.general.exceptions import SapioUserCancelledException, SapioException, SapioUserErrorException
from sapiopycommons.recordmodel.record_handler import RecordHandler


class CallbackUtil:
    user: SapioUser
    callback: ClientCallback
    dt_cache: DataTypeCacheManager
    width_pixels: int | None
    width_percent: float | None

    def __init__(self, context: SapioWebhookContext | SapioUser):
        """
        :param context: The current webhook context or a user object to send requests from.
        """
        self.user = context if isinstance(context, SapioUser) else context.user
        self.callback = DataMgmtServer.get_client_callback(self.user)
        self.dt_cache = DataTypeCacheManager(self.user)
        self.width_pixels = None
        self.width_percent = None

    def set_dialog_width(self, width_pixels: int | None, width_percent: float | None):
        """
        Set the width that dialogs will appear as for those dialogs that support specifying their width.

        :param width_pixels: The number of pixels wide that dialogs will appear as.
        :param width_percent: The percentage of the client's screen width that dialogs will appear as.
        """
        self.width_pixels = width_pixels
        self.width_percent = width_percent
    
    def option_dialog(self, title: str, msg: str, options: list[str], default_option: int = 0,
                      user_can_cancel: bool = False) -> str:
        """
        Create an option dialog with the given options for the user to choose from.

        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        :param options: The button options that the user has to choose from.
        :param default_option: The index of the option in the options list that defaults as the first choice.
        :param user_can_cancel: True if the user is able to click the X to close the dialog. False if the user cannot
            close the dialog without selecting an option. If the user is able to cancel and does so, a
            SapioUserCancelledException is thrown.
        :return: The name of the button that the user selected.
        """
        request = OptionDialogRequest(title, msg, options, default_option, user_can_cancel)
        response: int | None = self.callback.show_option_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        return options[response]

    def ok_dialog(self, title: str, msg: str) -> None:
        """
        Create an option dialog where the only option is "OK". Doesn't allow the user to cancel the
        dialog using the X at the top right corner. Returns nothing.

        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        """
        self.option_dialog(title, msg, ["OK"], 0, False)

    def ok_cancel_dialog(self, title: str, msg: str, default_ok: bool = True) -> bool:
        """
        Create an option dialog where the only options are "OK" and "Cancel". Doesn't allow the user to cancel the
        dialog using the X at the top right corner.

        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        :param default_ok: If true, "OK" is the default choice. Otherwise, the default choice is "Cancel".
        :return: True if the user selected OK. False if the user selected Cancel.
        """
        return self.option_dialog(title, msg, ["OK", "Cancel"], 0 if default_ok else 1, False) == "OK"

    def yes_no_dialog(self, title: str, msg: str, default_yes: bool = True) -> bool:
        """
        Create an option dialog where the only options are "Yes" and "No". Doesn't allow the user to cancel the
        dialog using the X at the top right corner.

        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        :param default_yes: If true, "Yes" is the default choice. Otherwise, the default choice is "No".
        :return: True if the user selected Yes. False if the user selected No.
        """
        return self.option_dialog(title, msg, ["Yes", "No"], 0 if default_yes else 1, False) == "Yes"

    def list_dialog(self, title: str, options: list[str], multi_select: bool = False) -> list[str]:
        """
        Create a list dialog with the given options for the user to choose from.

        :param title: The title of the dialog.
        :param options: The list options that the user has to choose from.
        :param multi_select: Whether the user is able to select multiple options from the list.
        :return: The list of options that the user selected.
        """
        request = ListDialogRequest(title, multi_select, options)
        response: list[str] | None = self.callback.show_list_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        return response

    def form_dialog(self,
                    title: str,
                    msg: str,
                    fields: list[AbstractVeloxFieldDefinition],
                    values: FieldMap = None,
                    column_positions: dict[str, tuple[int, int]] = None,
                    *,
                    data_type: str = "Default",
                    display_name: str | None = None,
                    plural_display_name: str | None = None) -> FieldMap:
        """
        Create a form dialog where the user may input data into the fields of the form. Requires that the caller
        provide the definitions of every field in the form.

        :param title: The title of the dialog.
        :param msg: The message to display at the top of the form.
        :param fields: The definitions of the fields to display in the form. Fields will be displayed in the order they
            are provided in this list.
        :param values: Sets the default values of the fields.
        :param column_positions: If a tuple is provided for a field name, alters that field's column position and column
            span. (Field order is still determined by the fields list.)
        :param data_type: The data type name for the temporary data type that will be created for this form.
        :param display_name: The display name for the temporary data type. If not provided, defaults to the data type
            name.
        :param plural_display_name: The plural display name for the temporary data type. If not provided, defaults to
            the display name + "s".
        :return: A dictionary mapping the data field names of the given field definitions to the response value from
            the user for that field.
        """
        if display_name is None:
            display_name = data_type
        if plural_display_name is None:
            plural_display_name = display_name + "s"

        builder = FormBuilder(data_type, display_name, plural_display_name)
        for field_def in fields:
            field_name = field_def.data_field_name
            if values and hasattr(field_def, "default_value"):
                field_def.default_value = values.get(field_name)
            column: int = 0
            span: int = 4
            if column_positions and field_name in column_positions:
                position = column_positions.get(field_name)
                column = position[0]
                span = position[1]
            builder.add_field(field_def, column, span)

        request = FormEntryDialogRequest(title, msg, builder.get_temporary_data_type())
        response: FieldMap | None = self.callback.show_form_entry_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        return response

    def record_form_dialog(self,
                           title: str,
                           msg: str,
                           fields: list[str],
                           record: SapioRecord,
                           column_positions: dict[str, tuple[int, int]] = None,
                           editable: bool | None = True) -> FieldMap:
        """
        Create a form dialog where the user may input data into the fields of the form. The form is constructed from
        a given record. Provided field names must match fields on the definition of the data type of the given record.
        The fields that are displayed will have their default value be that of the fields on the given record.

        Makes webservice calls to get the data type definition and fields of the given record if they weren't
        previously cached.

        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        :param fields: The data field names of the fields from the record to display in the form. Fields will be
            displayed in the order they are provided in this list.
        :param record: The record to display the values of.
        :param column_positions: If a tuple is provided for a field name, alters that field's column position and column
            span. (Field order is still determined by the fields list.)
        :param editable: If true, all fields are displayed as editable. If false, all fields are displayed as
            uneditable. If none, only those fields that are defined as editable by the data designer will be editable.
        :return: A dictionary mapping the data field names of the given field definitions to the response value from
            the user for that field.
        """
        # Get the field definitions of the data type.
        data_type: str = record.data_type_name
        type_def: DataTypeDefinition = self.dt_cache.get_data_type(data_type)
        field_defs: dict[str, AbstractVeloxFieldDefinition] = self.dt_cache.get_fields_for_type(data_type)

        # Build the form using only those fields that are desired.
        builder = FormBuilder(data_type, type_def.display_name, type_def.plural_display_name)
        for field_name in fields:
            field_def = field_defs.get(field_name)
            if field_def is None:
                raise SapioException(f"No field of name \"{field_name}\" in field definitions of type \"{data_type}\"")
            if editable is not None:
                field_def.editable = editable
            field_def.visible = True
            if hasattr(field_def, "default_value"):
                field_def.default_value = record.get_field_value(field_name)
            column: int = 0
            span: int = 4
            if column_positions and field_name in column_positions:
                position = column_positions.get(field_name)
                column = position[0]
                span = position[1]
            builder.add_field(field_def, column, span)

        request = FormEntryDialogRequest(title, msg, builder.get_temporary_data_type())
        response: FieldMap | None = self.callback.show_form_entry_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        return response

    def input_dialog(self, title: str, msg: str, field: AbstractVeloxFieldDefinition) -> Any:
        """
        Create an input dialog where the user must input data for a singular field.

        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        :param field: The definition for a field that the user must provide input to.
        :return: The response value from the user for the given field.
        """
        request = InputDialogCriteria(title, msg, field, self.width_pixels, self.width_percent)
        response: Any | None = self.callback.show_input_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        return response

    def string_input_dialog(self, title: str, msg: str, field_name: str, default_value: str | None = None,
                            max_length: int | None = None, editable: bool = True, **kwargs) -> str:
        """
        Create an input dialog where the user must input data for a singular text field.

        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        :param field_name: The name and display name of the string field.
        :param default_value: The default value to place into the string field, if any.
        :param max_length: The max length of the string value. If not provided, uses the length of the default value.
            If neither this or a default value are not provided, defaults to 100 characters.
        :param editable: Whether the field is editable by the user.
        :param kwargs: Any additional keyword arguments to pass to the field definition.
        :return: The string that the user input into the dialog.
        """
        if max_length is None:
            max_length = len(default_value) if default_value else 100
        field = VeloxStringFieldDefinition("Input", field_name, field_name, default_value=default_value,
                                           max_length=max_length, editable=editable, **kwargs)
        return self.input_dialog(title, msg, field)

    def integer_input_dialog(self, title: str, msg: str, field_name: str, default_value: int = None,
                             min_value: int = -10000, max_value: int = 10000, editable: bool = True, **kwargs) -> int:
        """
        Create an input dialog where the user must input data for a singular integer field.

        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        :param field_name: The name and display name of the integer field.
        :param default_value: The default value to place into the integer field. If not provided, defaults to the 0 or
            the minimum value, whichever is higher.
        :param min_value: The minimum allowed value of the input.
        :param max_value: The maximum allowed value of the input.
        :param editable: Whether the field is editable by the user.
        :param kwargs: Any additional keyword arguments to pass to the field definition.
        :return: The integer that the user input into the dialog.
        """
        if default_value is None:
            default_value = max(0, min_value)
        field = VeloxIntegerFieldDefinition("Input", field_name, field_name, default_value=default_value,
                                            min_value=min_value, max_value=max_value, editable=editable, **kwargs)
        return self.input_dialog(title, msg, field)

    def double_input_dialog(self, title: str, msg: str, field_name: str, default_value: float = None,
                            min_value: float = -10000000, max_value: float = 100000000, editable: bool = True,
                            **kwargs) -> float:
        """
        Create an input dialog where the user must input data for a singular double field.

        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        :param field_name: The name and display name of the double field.
        :param default_value: The default value to place into the double field. If not provided, defaults to the 0 or
            the minimum value, whichever is higher.
        :param min_value: The minimum allowed value of the input.
        :param max_value: The maximum allowed value of the input.
        :param editable: Whether the field is editable by the user.
        :param kwargs: Any additional keyword arguments to pass to the field definition.
        :return: The float that the user input into the dialog.
        """
        if default_value is None:
            default_value = max(0., min_value)
        field = VeloxDoubleFieldDefinition("Input", field_name, field_name, default_value=default_value,
                                           min_value=min_value, max_value=max_value, editable=editable, **kwargs)
        return self.input_dialog(title, msg, field)

    def table_dialog(self,
                     title: str,
                     msg: str,
                     fields: list[AbstractVeloxFieldDefinition],
                     values: list[FieldMap],
                     *,
                     data_type: str = "Default",
                     display_name: str | None = None,
                     plural_display_name: str | None = None) -> list[FieldMap]:
        """
        Create a table dialog where the user may input data into the fields of the table. Requires that the caller
        provide the definitions of every field in the table.

        :param title: The title of the dialog.
        :param msg: The message to display at the top of the form.
        :param fields: The definitions of the fields to display as table columns. Fields will be displayed in the order
            they are provided in this list.
        :param values: The values to set for each row of the table.
        :param data_type: The data type name for the temporary data type that will be created for this table.
        :param display_name: The display name for the temporary data type. If not provided, defaults to the data type
            name.
        :param plural_display_name: The plural display name for the temporary data type. If not provided, defaults to
            the display name + "s".
        :return: A list of dictionaries mapping the data field names of the given field definitions to the response
            value from the user for that field for each row.
        """
        if display_name is None:
            display_name = data_type
        if plural_display_name is None:
            plural_display_name = display_name + "s"

        builder = FormBuilder(data_type, display_name, plural_display_name)
        for column in fields:
            builder.add_field(column)

        request = TableEntryDialogRequest(title, msg, builder.get_temporary_data_type(), values)
        response: list[FieldMap] | None = self.callback.show_table_entry_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        return response

    def record_table_dialog(self,
                            title: str,
                            msg: str,
                            fields: list[str],
                            records: list[SapioRecord],
                            editable: bool | None = True) -> list[FieldMap]:
        """
        Create a table dialog where the user may input data into the fields of the table. The table is constructed from
        a given list of records. Provided field names must match fields on the definition of the data type of the given
        records. The fields that are displayed will have their default value be that of the fields on the given records.

        Makes webservice calls to get the data type definition and fields of the given records if they weren't
        previously cached.

        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        :param records: The records to display as rows in the table.
        :param fields: The names of the fields to display as columns in the table. Fields will be displayed in the order
            they are provided in this list.
        :param editable: If true, all fields are displayed as editable. If false, all fields are displayed as
            uneditable. If none, only those fields that are defined as editable by the data designer will be editable.
        :return: A list of dictionaries mapping the data field names of the given field definitions to the response
            value from the user for that field for each row.
        """
        data_types: set[str] = {x.data_type_name for x in records}
        if len(data_types) > 1:
            raise SapioException("Multiple data type names encountered in records list for record table popup.")
        data_type: str = data_types.pop()
        # Get the field maps from the records.
        field_map_list: list[FieldMap] = AliasUtil.to_field_map_lists(records)
        # Get the field definitions of the data type.
        type_def: DataTypeDefinition = self.dt_cache.get_data_type(data_type)
        field_defs: dict[str, AbstractVeloxFieldDefinition] = self.dt_cache.get_fields_for_type(data_type)

        # Build the form using only those fields that are desired.
        builder = FormBuilder(data_type, type_def.display_name, type_def.plural_display_name)
        for field_name in fields:
            field_def = field_defs.get(field_name)
            if field_def is None:
                raise SapioException(f"No field of name \"{field_name}\" in field definitions of type \"{data_type}\"")
            if editable is not None:
                field_def.editable = editable
            field_def.visible = True
            # Key fields display their columns in order before all non-key fields.
            # Unmark key fields so that the column order is respected exactly as the caller provides it.
            field_def.key_field = False
            builder.add_field(field_def)

        request = TableEntryDialogRequest(title, msg, builder.get_temporary_data_type(), field_map_list)
        response: list[FieldMap] | None = self.callback.show_table_entry_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        return response
    
    def record_view_dialog(self,
                           title: str,
                           record: SapioRecord,
                           layout: str | DataTypeLayout | None = None,
                           minimized: bool = False,
                           access_level: FormAccessLevel | None = None,
                           plugin_path_list: list[str] | None = None) -> None:
        """
        Create an IDV dialog for the given record. This IDV may use an existing layout already defined in the system,
        and can be created to allow the user to edit the field in the IDV, or to be read-only for the user to review.
        This returns no value, but if the user cancels the dialog instead of clicking the "OK" button, then a
        SapioUserCancelledException will be thrown.

        :param title: The title of the dialog.
        :param record: The record to be displayed in the dialog.
        :param layout: The layout that will be used to display the record in the dialog. If this is not
            provided, then the layout assigned to the current user's group for this data type will be used. If this
            is provided as a string, then a webservice call will be made to retrieve the data type layout matching
            the name of that string for the given record's data type.
        :param minimized: If true, then the dialog will only show key fields and required fields initially
            until the expand button is clicked (similar to when using the built-in add buttons to create new records).
        :param access_level: The level of access that the user will have on this field entry dialog. This attribute
            determines whether the user will be able to edit the fields in the dialog, use core features, or use toolbar
            buttons. If no value is provided, then the form will be editable.
        :param plugin_path_list: A white list of plugins that should be displayed in the dialog. This white list
            includes plugins that would be displayed on sub-tables/components in the layout.
        """
        # Ensure that the given record is a DataRecord.
        record: DataRecord = AliasUtil.to_data_record(record)

        # Get the corresponding DataTypeLayout for the provided name.
        if isinstance(layout, str):
            # TODO: Replace with dt_cache if the DataTypeCacheManager ever starts caching layouts.
            dt_man = DataMgmtServer.get_data_type_manager(self.user)
            data_type: str = record.get_data_type_name()
            layouts: dict[str, DataTypeLayout] = {x.layout_name: x for x in dt_man.get_data_type_layout_list(data_type)}
            layout_name: str = layout
            layout: DataTypeLayout | None = layouts.get(layout_name)
            # If a name was provided then the caller expects that name to exist. Throw an exception if it doesn't.
            if not layout:
                raise SapioException(f"The data type \"{data_type}\" does not have a layout by the name "
                                     f"\"{layout_name}\" in the system.")

        request = DataRecordDialogRequest(title, record, layout, minimized, access_level, plugin_path_list)
        response: bool = self.callback.data_record_form_view_dialog(request)
        if not response:
            raise SapioUserCancelledException()
    
    def selection_dialog(self,
                         msg: str,
                         fields: list[AbstractVeloxFieldDefinition],
                         values: list[FieldMap],
                         multi_select: bool = True,
                         *,
                         display_name: str = "Default",
                         plural_display_name: str | None = None) -> list[FieldMap]:
        """
        Create a selection dialog for a list of field maps for the user to choose from. Requires that the caller
        provide the definitions of every field in the table.

        :param msg: The message to display in the dialog.
        :param fields: The definitions of the fields to display as table columns. Fields will be displayed in the order
            they are provided in this list.
        :param values: The values to set for each row of the table.
        :param multi_select: Whether the user is able to select multiple rows from the list.
        :param display_name: The display name for the temporary data type that will be created.
        :param plural_display_name: The plural display name for the temporary data type. If not provided, defaults to
            the display name + "s".
        :return: A list of field maps corresponding to the chosen input field maps.
        """
        if plural_display_name is None:
            plural_display_name = display_name + "s"

        # Build the form using only those fields that are desired.
        request = DataRecordSelectionRequest(display_name, plural_display_name,
                                             fields, values, msg, multi_select)
        response: list[FieldMap] | None = self.callback.show_data_record_selection_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        return response
    
    def record_selection_dialog(self, msg: str, fields: list[str], records: list[SapioRecord],
                                multi_select: bool = True) -> list[FieldMap]:
        """
        Create a record selection dialog for a list of records for the user to choose from. Provided field names must
        match fields on the definition of the data type of the given records.

        Makes webservice calls to get the data type definition and fields of the given records if they weren't
        previously cached.

        :param msg: The message to display in the dialog.
        :param fields: The names of the fields to display as columns in the table. Fields will be displayed in the order
            they are provided in this list.
        :param records: The records to display as rows in the table.
        :param multi_select: Whether the user is able to select multiple records from the list.
        :return: A list of field maps corresponding to the chosen input records.
        """
        data_types: set[str] = {x.data_type_name for x in records}
        if len(data_types) > 1:
            raise SapioException("Multiple data type names encountered in records list for record table popup.")
        data_type: str = data_types.pop()
        # Get the field maps from the records.
        field_map_list: list[FieldMap] = AliasUtil.to_field_map_lists(records)
        # Put the record ID of each record in its corresponding field map so that we can map the field maps back to
        # the records when we return them to the caller.
        for record, field_map in zip(records, field_map_list):
            field_map.update({"RecId": record.record_id})
        # Get the field definitions of the data type.
        type_def: DataTypeDefinition = self.dt_cache.get_data_type(data_type)
        field_defs: dict[str, AbstractVeloxFieldDefinition] = self.dt_cache.get_fields_for_type(data_type)

        # Build the form using only those fields that are desired.
        field_def_list: list = []
        for field_name in fields:
            field_def = field_defs.get(field_name)
            if field_def is None:
                raise SapioException(f"No field of name \"{field_name}\" in field definitions of type \"{data_type}\"")
            field_def.visible = True
            # Key fields display their columns in order before all non-key fields.
            # Unmark key fields so that the column order is respected exactly as the caller provides it.
            field_def.key_field = False
            field_def_list.append(field_def)

        request = DataRecordSelectionRequest(type_def.display_name, type_def.plural_display_name,
                                             field_def_list, field_map_list, msg, multi_select)
        response: list[FieldMap] | None = self.callback.show_data_record_selection_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        # Map the field maps in the response back to the record they come from, returning the chosen record instead of
        # the chosen field map.
        records_by_id: dict[int, SapioRecord] = RecordHandler.map_by_id(records)
        ret_list: list[SapioRecord] = []
        for field_map in response:
            ret_list.append(records_by_id.get(field_map.get("RecId")))
        return ret_list

    def input_selection_dialog(self,
                               wrapper_type: type[WrappedType],
                               msg: str,
                               multi_select: bool = True,
                               only_key_fields: bool = False,
                               search_types: list[SearchType] | None = None,
                               scan_criteria: ScanToSelectCriteria | None = None,
                               custom_search: CustomReport | CustomReportCriteria | str | None = None,
                               preselected_records: list[RecordIdentifier] | None = None,
                               record_blacklist: list[RecordIdentifier] | None = None,
                               record_whitelist: list[RecordIdentifier] | None = None) -> list[WrappedType]:
        """
        Display a table of records that exist in the system matching the given data type and filter criteria and have
        the user select one or more records from the table.

        :param wrapper_type: The record model wrapper for the records to display in the dialog.
        :param msg: The message to show near the top of the dialog, below the title. This can be used to
            instruct the user on what is desired from the dialog.
        :param multi_select: Whether the user may select multiple items at once in this dialog.
        :param only_key_fields: Whether only key fields of the selected data type should be displayed in the table
            of data in the dialog. If false, allows all possible fields to be displayed as columns in the table.
        :param search_types: The type of search that will be made available to the user through the dialog. This
            includes quick searching a list of records, allowing the user to create an advanced search, or allowing
            the user to browse the record tree.
        :param scan_criteria: If present, the dialog will show a scan-to-select editor in the quick search
            section that allows for picking a field to match on and scanning a value to more easily select records.
            If quick search is not an allowable search type from the search_types parameter, then this
            parameter will have no effect.
        :param custom_search: An alternate search to be used in the quick search section to pre-filter the displayed
            records. If not provided or if the search is cross data type or not a report of the type specified, all
            records of the type will be shown (which is the normal quick search results behavior).
            If quick search is not an allowable search type from the search_types parameter, then this
            parameter will have no effect.
            If the search is provided as a string, then a webservice call will be made to retrieve the custom report
            criteria for the system report/predefined search in the system matching that name.
        :param preselected_records: The records that should be selected in the dialog when it is initially
            displayed to the user. The user will be allowed to deselect these records if they so wish. If preselected
            record IDs are provided, the dialog will automatically allow multi-selection of records.
        :param record_blacklist: A list of records that should not be seen as possible options in the dialog.
        :param record_whitelist: A list of records that will be seen as possible options in the dialog. Records not in
            this whitelist will not be displayed if a whitelist is provided.
        :return: A list of the records selected by the user in the dialog, wrapped as record models using the provided
            wrapper.
        """
        data_type: str = wrapper_type.get_wrapper_data_type_name()

        # Reduce the provided lists of records down to lists of record IDs.
        if preselected_records:
            preselected_records: list[int] = AliasUtil.to_record_ids(preselected_records)
        if record_blacklist:
            record_blacklist: list[int] = AliasUtil.to_record_ids(record_blacklist)
        if record_whitelist:
            record_whitelist: list[int] = AliasUtil.to_record_ids(record_whitelist)

        # If CustomReportCriteria was provided, it must be wrapped as a CustomReport.
        if isinstance(custom_search, CustomReportCriteria):
            custom_search: CustomReport = CustomReport(False, None, custom_search)
        # If a string was provided, locate the report criteria for the predefined search in the system matching this
        # name.
        if isinstance(custom_search, str):
            custom_search: CustomReport = CustomReportUtil.get_system_report_criteria(self.user, custom_search)

        request = InputSelectionRequest(data_type, msg, search_types, only_key_fields, record_blacklist,
                                        record_whitelist, preselected_records, custom_search, scan_criteria,
                                        multi_select)
        response: list[DataRecord] | None = self.callback.show_input_selection_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        return RecordHandler(self.user).wrap_models(response, wrapper_type)
    
    def esign_dialog(self, title: str, msg: str, show_comment: bool = True,
                     additional_fields: list[AbstractVeloxFieldDefinition] = None) -> ESigningResponsePojo:
        """
        Create an e-sign dialog for the user to interact with.
        
        :param title: The title of the dialog.
        :param msg: The message to display in the dialog.
        :param show_comment: Whether the "Meaning of Action" field should appear in the e-sign dialog. If true, the
            user is required to provide an action.
        :param additional_fields: Field definitions for additional fields to display in the dialog, for if there is
            other information you wish to gather from the user alongside the e-sign.
        :return: An e-sign response object containing information about the e-sign attempt.
        """
        temp_dt = None
        if additional_fields:
            builder = FormBuilder()
            for field in additional_fields:
                builder.add_field(field)
            temp_dt = builder.get_temporary_data_type()
        request = ESigningRequestPojo(title, msg, show_comment, temp_dt)
        response: ESigningResponsePojo | None = self.callback.show_esign_dialog(request)
        if response is None:
            raise SapioUserCancelledException()
        return response

    def request_file(self, title: str, exts: list[str] | None = None,
                     show_image_editor: bool = False, show_camera_button: bool = False) -> (str, bytes):
        """
        Request a single file from the user.

        :param title: The title of the dialog.
        :param exts: The allowable file extensions of the uploaded file. If blank, any file can be uploaded. Throws an
            exception if an incorrect file extension is provided.
        :param show_image_editor: Whether the user will see an image editor when image is uploaded in this file prompt.
        :param show_camera_button: Whether the user will be able to use camera to take a picture as an upload request,
            rather than selecting an existing file.
        :return: The file name and bytes of the uploaded file.
        """
        # If no extensions were provided, use an empty list for the extensions instead.
        if exts is None:
            exts: list[str] = []

        # Use a data sink to consume the data. In order to get both the file name and the file data,
        # I've recreated a part of sink.upload_single_file_to_webhook_server() in this function, as
        # calling that sink function throws out the file name of the uploaded file.
        sink = InMemoryRecordDataSink(self.user)
        with sink as io_obj:
            def do_consume(chunk: bytes) -> None:
                return sink.consume_data(chunk, io_obj)

            request = FilePromptRequest(title, show_image_editor, ",".join(exts), show_camera_button)
            file_path: str | None = self.callback.show_file_dialog(request, do_consume)
        if file_path is None:
            raise SapioUserCancelledException()

        self.__verify_file(file_path, sink.data, exts)
        return file_path, sink.data

    def request_files(self, title: str, exts: list[str] | None = None,
                      show_image_editor: bool = False, show_camera_button: bool = False):
        """
        Request multiple files from the user.

        :param title: The title of the dialog.
        :param exts: The allowable file extensions of the uploaded files. If blank, any file can be uploaded. Throws an
            exception if an incorrect file extension is provided.
        :param show_image_editor: Whether the user will see an image editor when image is uploaded in this file prompt.
        :param show_camera_button: Whether the user will be able to use camera to take a picture as an upload request,
            rather than selecting an existing file.
        :return: A dictionary of file name to file bytes for each file the user uploaded.
        """
        # If no extensions were provided, use an empty list for the extensions instead.
        if exts is None:
            exts: list[str] = []

        request = MultiFilePromptRequest(title, show_image_editor, ",".join(exts), show_camera_button)
        file_paths: list[str] | None = self.callback.show_multi_file_dialog(request)
        if not file_paths:
            raise SapioUserCancelledException()

        ret_dict: dict[str, bytes] = {}
        for file_path in file_paths:
            sink = InMemoryRecordDataSink(self.user)
            sink.consume_client_callback_file_path_data(file_path)
            self.__verify_file(file_path, sink.data, exts)
            ret_dict.update({file_path: sink.data})

        return ret_dict

    @staticmethod
    def __verify_file(file_path: str, file_bytes: bytes, allowed_extensions: list[str]):
        """
        Verify that the provided file was read (i.e. the file path and file bytes aren't None or empty) and that it
        has the correct file extension. Raises a user error exception if something about the file is incorrect.

        :param file_path: The name of the file to verify.
        :param file_bytes: The bytes of the file to verify.
        :param allowed_extensions: The file extensions that the file path is allowed to have.
        """
        if file_path is None or len(file_path) == 0 or file_bytes is None or len(file_bytes) == 0:
            raise SapioUserErrorException("Empty file provided or file unable to be read.")
        if len(allowed_extensions) != 0:
            matches: bool = False
            for ext in allowed_extensions:
                if file_path.endswith("." + ext):
                    matches = True
                    break
            if matches is False:
                raise SapioUserErrorException("Unsupported file type. Expecting the following extension(s): "
                                              + (",".join(allowed_extensions)))

    def write_file(self, file_name: str, file_data: str | bytes) -> None:
        """
        Send a file to the user for them to download.

        :param file_name: The name of the file.
        :param file_data: The data of the file, provided as either a string or as a bytes array.
        """
        data = io.StringIO(file_data) if isinstance(file_data, str) else io.BytesIO(file_data)
        self.callback.send_file(file_name, False, data)
