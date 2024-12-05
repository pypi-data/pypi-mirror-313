from typing import Optional, List, Dict, Any

from sapiopylib.rest.pojo.TableColumn import TableColumn
from sapiopylib.rest.pojo.datatype.FieldDefinition import AbstractVeloxFieldDefinition
from sapiopylib.rest.pojo.eln.ExperimentEntry import ExperimentEntry, EntryAttachment
from sapiopylib.rest.pojo.eln.SapioELNEnums import ElnEntryType, ExperimentEntryStatus


class ElnEntryCriteria:
    """
    Criteria to specify a new ELN entry.

    Attributes:
        entry_type: Experiment Entry Type (required)
        entry_name: Experiment Entry Name (required)
        data_type_name: Data type name of the experiment entry.
        order: The order of the entry in the tab. Cannot be before the title entry.
        is_shown_in_template: Whether the entry's template clone will be added to a new template.
        notebook_experiment_tab_id: Tab where the entry will be added.
        column_order: The column order of the entry (classic view only)
        column_span: The column span of the entry (classic view only)
        is_removable: Whether the entry can be removed by user.
        is_renamable: Whether the entry can be renamed by user.
        is_static_view: Whether the entry's attachment is static.
        enb_field_set_id: The field sets in the entry.
        related_entry_set: The entries this entry is implicitly dependent on.
        (if any of them are deleted this is also deleted)
        dependency_set: The entries this entry is dependent on. (requires them to be completed before enable)
        requires_grabber_plugin: Whether to run a grabber plugin in a new instance from template.
        entry_singleton_id: If the entry is singleton in ELN, the singleton ID to check.
        field_map_list: The default new data list of this entry. ELN types only.
        field_definition_list: The default new field list of this entry. ELN types only.
        csp_plugin_name: The CSP plugin name to render this entry with.
        using_template_data: Whether this entry will use the template data from previous template.
        provides_template_data: Whether this entry can provide template data to copy into template.
        source_entry_id: The source entry ID it created from.
        attachment_data_base64: The base 64 attachment payload to directly inject into the attachment entry.
        attachment_file_name: The file name of the attachment entry.
        temp_data_plugin_path: The temp data plugin path to run if this entry is temp data entry.
    """
    entry_type: ElnEntryType
    data_type_name: Optional[str]
    order: Optional[int]
    entry_name: Optional[str]
    is_shown_in_template: Optional[bool]
    notebook_experiment_tab_id: Optional[int]
    column_order: Optional[int]
    column_span: Optional[int]
    is_removable: Optional[bool]
    is_renamable: Optional[bool]
    is_static_view: Optional[bool]
    enb_field_set_id: Optional[int]
    related_entry_set: Optional[List[int]]
    dependency_set: Optional[List[int]]
    requires_grabber_plugin: bool
    entry_singleton_id: Optional[str]
    field_map_list: Optional[List[Dict[str, Any]]]
    field_definition_list: Optional[List[AbstractVeloxFieldDefinition]]
    csp_plugin_name: Optional[str]
    using_template_data: Optional[bool]
    provides_template_data: Optional[bool]
    source_entry_id: Optional[int]
    attachment_data_base64: Optional[str]
    attachment_file_name: Optional[str]
    temp_data_plugin_path: Optional[str]

    def __init__(self, entry_type: ElnEntryType, entry_name: Optional[str],
                 data_type_name: Optional[str], order: int, is_shown_in_template: Optional[
                bool] = None,
                 notebook_experiment_tab_id: Optional[int] = None, column_order: Optional[int] = None,
                 column_span: Optional[int] = None, is_removable: Optional[bool] = None, is_renamable: Optional[
                bool] = None,
                 is_static_view: Optional[bool] = None, enb_field_set_id: Optional[int] = None,
                 related_entry_set: Optional[List[int]] = None,
                 dependency_set: Optional[List[int]] = None,
                 requires_grabber_plugin: bool = False, entry_singleton_id: Optional[str] = None,
                 field_map_list: Optional[List[Dict[str, Any]]] = None,
                 field_definition_list: Optional[List[AbstractVeloxFieldDefinition]] = None,
                 csp_plugin_name: Optional[str] = None, using_template_data: Optional[bool] = None,
                 provides_template_data: Optional[bool] = None, source_entry_id: Optional[int] = None,
                 attachment_data_base64: Optional[str] = None, attachment_file_name: Optional[str] = None,
                 temp_data_plugin_path: Optional[str] = None):
        self.entry_type = entry_type
        self.entry_name = entry_name
        self.data_type_name = data_type_name
        self.order = order
        self.is_shown_in_template = is_shown_in_template
        self.notebook_experiment_tab_id = notebook_experiment_tab_id
        self.column_order = column_order
        self.column_span = column_span
        self.is_removable = is_removable
        self.is_renamable = is_renamable
        self.is_static_view = is_static_view
        self.enb_field_set_id = enb_field_set_id
        self.related_entry_set = related_entry_set
        self.dependency_set = dependency_set
        self.requires_grabber_plugin = requires_grabber_plugin
        self.entry_singleton_id = entry_singleton_id
        self.field_map_list = field_map_list
        self.field_definition_list = field_definition_list
        self.csp_plugin_name = csp_plugin_name
        self.using_template_data = using_template_data
        self.provides_template_data = provides_template_data
        self.source_entry_id = source_entry_id
        self.attachment_data_base64 = attachment_data_base64
        self.attachment_file_name = attachment_file_name
        self.temp_data_plugin_path = temp_data_plugin_path

    def to_json(self) -> Dict[str, Any]:
        field_def_list_pojo_list: Optional[List[Dict[str, Any]]] = None
        if self.field_definition_list is not None:
            field_def_list_pojo_list = [x.to_json() for x in self.field_definition_list]
        ret: Dict[str, Any] = {
            'entryType': self.entry_type.name,
            'dataTypeName': self.data_type_name,
            'order': self.order,
            'enbEntryName': self.entry_name,
            'isShownInTemplate': self.is_shown_in_template,
            'notebookExperimentTabId': self.notebook_experiment_tab_id,
            'columnOrder': self.column_order,
            'columnSpan': self.column_span,
            'isRemovable': self.is_removable,
            'isRenamable': self.is_renamable,
            'isStaticView': self.is_static_view,
            'enbFieldSetId': self.enb_field_set_id,
            'relatedEntryIdSet': self.related_entry_set,
            'dependencySet': self.dependency_set,
            'requiresGrabberPlugin': self.requires_grabber_plugin,
            'entrySingletonId': self.entry_singleton_id,
            'fieldMapList': self.field_map_list,
            'fieldDefinitionList': field_def_list_pojo_list,
            'pluginName': self.csp_plugin_name,
            'usingTemplateData': self.using_template_data,
            'providesTemplateData': self.provides_template_data,
            'sourceEntryId': self.source_entry_id,
            'attachmentData': self.attachment_data_base64,
            'attachmentFileName': self.attachment_file_name,
            'pluginPath': self.temp_data_plugin_path
        }
        return ret


class AbstractElnEntryUpdateCriteria:
    """
    Abstract criteria to specify supported update payload to an existing entry.

    This is an abstract class and serves as a base for the classes providing different
    types of entry updates. You should use a constructor from a subclass.

    Attributes:
        entry_type (ElnEntryType): The type of the entry.

        entry_name (str or None): The name of the entry.

        related_entry_set (List[int] or None): A set of implicit dependencies of this entry. i.e. removal of any of these entries will also remove the current entry.

        dependency_set (List[int] or None): A set of explict dependencies of this entry. i.e. the entries that must be submitted before this entry becomes available in client.

        entry_status (ExperimentEntryStatus or None): The status of the entry.

        order (int or None): The order of entry. The title entry must come before all other entries.

        description (str or None): The description of the entry.

        requires_grabber_plugin (bool or None): Flag indicating if the grabber plugin is required.

        is_initialization_required (bool or None): Flag indicating if initialization is required.

        notebook_experiment_tab_id (int or None): The ID of the notebook experiment tab.

        entry_height (int or None): The height of the entry.

        column_order (int or None): The column order of the entry.

        column_span (int or None): The column span of the entry.

        is_removable (bool or None): Flag indicating if the entry is removable.

        is_renamable (bool or None): Flag indicating if the entry is renamable.

        source_entry_id (int or None): The ID of the source entry.

        clear_source_entry_id (bool or None): Flag indicating if the ID of the source entry needs to be cleared.

        is_hidden (bool or None): Flag indicating if the entry is hidden.

        is_static_View (bool or None): Flag indicating if the view is static.

        is_shown_in_template (bool or None): Flag indicating if the entry is shown in template.

        template_item_fulfilled_timestamp (int or None): The timestamp of the fulfilled template item.

        clear_template_item_fulfilled_timestamp (bool or None): Flag indicating if the timestamp
            of the fulfilled template item needs to be cleared.

        entry_options_map (Dict[str, str] or None): Map of entry options.
    """
    entry_type: ElnEntryType
    entry_name: Optional[str]
    related_entry_set: Optional[List[int]]
    dependency_set: Optional[List[int]]
    entry_status: Optional[ExperimentEntryStatus]
    order: Optional[int]
    description: Optional[str]
    requires_grabber_plugin: Optional[bool]
    is_initialization_required: Optional[bool]
    notebook_experiment_tab_id: Optional[int]
    entry_height: Optional[int]
    column_order: Optional[int]
    column_span: Optional[int]
    is_removable: Optional[bool]
    is_renamable: Optional[bool]
    source_entry_id: Optional[int]
    clear_source_entry_id: Optional[bool]
    is_hidden: Optional[bool]
    is_static_View: Optional[bool]
    is_shown_in_template: Optional[bool]
    template_item_fulfilled_timestamp: Optional[int]
    clear_template_item_fulfilled_timestamp: Optional[bool]
    entry_options_map: Optional[Dict[str, str]]
    collapse_entry: bool | None

    def __init__(self, entry_type: ElnEntryType):
        """
        INTERNAL ONLY. USE a constructor from a subclass!
        """
        self.entry_type = entry_type
        self.entry_name = None
        self.related_entry_set = None
        self.dependency_set: Optional[List[int]] = None
        self.entry_status: Optional[ExperimentEntryStatus] = None
        self.order: Optional[int] = None
        self.description: Optional[str] = None
        self.requires_grabber_plugin: Optional[bool] = None
        self.is_initialization_required: Optional[bool] = None
        self.notebook_experiment_tab_id: Optional[int] = None
        self.entry_height: Optional[int] = None
        self.column_order: Optional[int] = None
        self.column_span: Optional[int] = None
        self.is_removable: Optional[bool] = None
        self.is_renamable: Optional[bool] = None
        self.source_entry_id: Optional[int] = None
        self.clear_source_entry_id: Optional[bool] = None
        self.is_hidden: Optional[bool] = None
        self.is_static_View: Optional[bool] = None
        self.is_shown_in_template: Optional[bool] = None
        self.template_item_fulfilled_timestamp: Optional[int] = None
        self.clear_template_item_fulfilled_timestamp: Optional[bool] = None
        self.entry_options_map: Optional[Dict[str, str]] = None
        self.collapse_entry = None

    def to_json(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = {
            'entryType': self.entry_type.name,
        }
        if self.entry_name is not None:
            ret['experimentEntryName'] = self.entry_name
        if self.dependency_set is not None:
            ret['dependencySet'] = self.dependency_set
        if self.related_entry_set is not None:
            ret['relatedEntrySet'] = self.related_entry_set
        if self.entry_status is not None:
            ret['entryStatus'] = self.entry_status.name
        if self.order is not None:
            ret['order'] = self.order
        if self.description is not None:
            ret['description'] = self.description
        if self.requires_grabber_plugin is not None:
            ret['requiresGrabberPlugin'] = self.requires_grabber_plugin
        if self.is_initialization_required is not None:
            ret['isInitializationRequired'] = self.is_initialization_required
        if self.notebook_experiment_tab_id is not None:
            ret['notebookExperimentTabId'] = self.notebook_experiment_tab_id
        if self.entry_height is not None:
            ret['entryHeight'] = self.entry_height
        if self.column_order is not None:
            ret['columnOrder'] = self.column_order
        if self.column_span is not None:
            ret['columnSpan'] = self.column_span
        if self.is_removable is not None:
            ret['isRemovable'] = self.is_removable
        if self.is_renamable is not None:
            ret['isRenamable'] = self.is_renamable
        if self.source_entry_id is not None:
            ret['sourceEntryId'] = self.source_entry_id
        if self.clear_source_entry_id is not None:
            ret['clearSourceEntryId'] = self.clear_source_entry_id
        if self.is_hidden is not None:
            ret['isHidden'] = self.is_hidden
        if self.is_static_View is not None:
            ret['isStaticView'] = self.is_static_View
        if self.is_shown_in_template is not None:
            ret['isShownInTemplate'] = self.is_shown_in_template
        if self.template_item_fulfilled_timestamp is not None:
            ret['templateItemFulfilledTimestamp'] = self.template_item_fulfilled_timestamp
        if self.clear_template_item_fulfilled_timestamp is not None:
            ret['clearTemplateItemFulfilledTimestamp'] = self.clear_template_item_fulfilled_timestamp
        if self.entry_options_map is not None:
            ret['entryOptionMap'] = self.entry_options_map
        if self.collapse_entry is not None:
            ret['collapseEntry'] = self.collapse_entry
        return ret


class ElnAttachmentEntryUpdateCriteria(AbstractElnEntryUpdateCriteria):
    """
    Update data payload for an attachment ELN entry.

    This class serves as a data holder for making attachment ELN entry updates.
    Create an instance of this class, set the attributes you want to update,
    and then use the instance to send the request.

    Attributes:
        attachment_name (str or None): The name of the attachment.

        record_id (int or None): The record ID.

        entry_attachment_list (List[EntryAttachment] or None): A list of entry attachments.
    """
    attachment_name: str | None
    record_id: int | None
    entry_attachment_list: List[EntryAttachment] | None

    def __init__(self):
        super().__init__(ElnEntryType.Attachment)
        self.attachment_name = None
        self.record_id = None
        self.entry_attachment_list = None

    def to_json(self) -> Dict[str, Any]:
        ret = super().to_json()
        if self.attachment_name is not None:
            ret['attachmentName'] = self.attachment_name
        if self.record_id is not None:
            ret['recordId'] = self.record_id
        if self.entry_attachment_list:
            ret['entryAttachmentList'] = [x.to_json() for x in self.entry_attachment_list]
        return ret


class ElnDashboardEntryUpdateCriteria(AbstractElnEntryUpdateCriteria):
    """
    Dashboard Entry Update Request Payload Data.
    This class serves as a data holder for making dashboard entry updates. Create an instance
    of this class, set the attributes you want to update, and then use the instance
    to send the request.

    Attributes:
        dashboard_guid (str or None): This attribute holds the unique identification for the dashboard.
            It can be set to None.

        dashboard_guid_list (list[str] or None): This attribute holds a list of dashboard GUIDs.
            It can be set to None.

        data_source_entry_id (int or None): This attribute holds the id of data source entry.
            It can be set to None.
    """
    dashboard_guid: str | None
    dashboard_guid_list: list[str] | None
    data_source_entry_id: int | None

    def __init__(self):
        super().__init__(ElnEntryType.Dashboard)
        self.dashboard_guid = None
        self.dashboard_guid_list = None
        self.data_source_entry_id = None

    def to_json(self) -> Dict[str, Any]:
        ret = super().to_json()
        if self.dashboard_guid is not None:
            ret['dashboardGuid'] = self.dashboard_guid
        if self.dashboard_guid_list:
            ret['dashboardGuidList'] = self.dashboard_guid_list
        if self.data_source_entry_id is not None:
            ret['dataSourceEntryId'] = self.data_source_entry_id
        return ret


class ElnFormEntryUpdateCriteria(AbstractElnEntryUpdateCriteria):
    """
    Form Entry Update Request payload data.

    This class serves as a data holder for making form entry updates. Create an instance
    of this class, set the attributes you want to update, and then use the instance to
    send the request.

    Attributes:
        form_name_list (Optional[List[str]]): A list of form names.

        data_type_layout_name (Optional[str]): The name of the data type layout.

        record_id (Optional[int]): The record ID.

        field_set_id_list (Optional[List[int]]): A list of field set IDs.

        extension_type_list (Optional[List[str]]): A list of extension types.

        data_field_name_list (Optional[List[str]]): A list of data field names.

        is_field_addable (Optional[bool]): A boolean flag indicating if a field is addable.

        is_existing_field_removable (Optional[bool]): A boolean flag indicating if an
            existing field is removable.

    """
    form_name_list: Optional[List[str]]
    data_type_layout_name: Optional[str]
    record_id: Optional[int]
    field_set_id_list: Optional[List[int]]
    extension_type_list: Optional[List[str]]
    data_field_name_list: Optional[List[str]]
    is_field_addable: Optional[bool]
    is_existing_field_removable: Optional[bool]

    def __init__(self):
        super().__init__(ElnEntryType.Form)
        self.form_name_list: Optional[List[str]] = None
        self.data_type_layout_name: Optional[str] = None
        self.record_id: Optional[int] = None
        self.field_set_id_list: Optional[List[int]] = None
        self.extension_type_list: Optional[List[str]] = None
        self.data_field_name_list: Optional[List[str]] = None
        self.is_field_addable: Optional[bool] = None
        self.is_existing_field_removable: Optional[bool] = None

    def to_json(self) -> Dict[str, Any]:
        ret = super().to_json()
        if self.form_name_list is not None:
            ret['formNameList'] = self.form_name_list
        if self.data_type_layout_name is not None:
            ret['dataTypeLayoutName'] = self.data_type_layout_name
        if self.record_id is not None:
            ret['recordId'] = self.record_id
        if self.field_set_id_list is not None:
            ret['fieldSetIdList'] = self.field_set_id_list
        if self.extension_type_list is not None:
            ret['extensionTypeList'] = self.extension_type_list
        if self.data_field_name_list is not None:
            ret['dataFieldNameList'] = self.data_field_name_list
        if self.is_field_addable is not None:
            ret['isFieldAddable'] = self.is_field_addable
        if self.is_existing_field_removable is not None:
            ret['isExistingFieldRemovable'] = self.is_existing_field_removable
        return ret


class ElnPluginEntryUpdateCriteria(AbstractElnEntryUpdateCriteria):
    """
    Plugin Entry Update Data Payload.

    This class serves as a data holder for making plugin entry updates.
    Create an instance of this class, set the attributes you want to update,
    and then use the instance to send the request.

    Attributes:
        plugin_name (Optional[str]): The name of the plugin.

        using_template_data (Optional[bool]): A flag indicating if template data is being used.

        provides_template_data (Optional[bool]): A flag indicating if the plugin provides template data.
    """
    plugin_name: Optional[str]
    using_template_data: Optional[bool]
    provides_template_data: Optional[bool]

    def __init__(self):
        super().__init__(ElnEntryType.Plugin)
        self.plugin_name = None
        self.using_template_data = None
        self.provides_template_data = None

    def to_json(self) -> Dict[str, Any]:
        ret = super().to_json()
        if self.plugin_name is not None:
            ret['pluginName'] = self.plugin_name
        if self.using_template_data is not None:
            ret['usingTemplateData'] = self.using_template_data
        if self.provides_template_data is not None:
            ret['provides_template_data'] = self.provides_template_data
        return ret


class ElnTableEntryUpdateCriteria(AbstractElnEntryUpdateCriteria):
    """
    Table Entry Update Criteria Payload.

    This class serves as a data holder for making table entry updates. Create an instance
    of this class, set the attributes you want to update, and then use the instance to
    send the request.

    Attributes:
        data_type_layout_name (str or None): The name of the data type layout.

        field_set_id_list (List[int] or None): A list of field set IDs used in table if ELN type.

        extension_type_list (List[str] or None): A list of extension types to show in the table.

        table_column_list (List[TableColumn] or None): A list of table columns explicitly defined to overwrite.

        show_key_fields (bool or None): A boolean flag indicating if key fields should be shown.

        is_field_addable (bool or None): A boolean flag indicating if a field is addable.

        is_existing_field_removable (bool or None): A boolean flag indicating if an
            existing field is removable.
    """
    data_type_layout_name: Optional[str]
    field_set_id_list: Optional[List[int]]
    extension_type_list: Optional[List[str]]
    table_column_list: Optional[List[TableColumn]]
    show_key_fields: Optional[bool]
    is_field_addable: Optional[bool]
    is_existing_field_removable: Optional[bool]

    def __init__(self):
        super().__init__(ElnEntryType.Table)
        self.data_type_layout_name: Optional[str] = None
        self.field_set_id_list: Optional[List[int]] = None
        self.extension_type_list: Optional[List[str]] = None
        self.table_column_list: Optional[List[TableColumn]] = None
        self.show_key_fields: Optional[bool] = None
        self.is_field_addable: Optional[bool] = None
        self.is_existing_field_removable: Optional[bool] = None

    def to_json(self) -> Dict[str, Any]:
        ret = super().to_json()
        if self.data_type_layout_name is not None:
            ret['dataTypeLayoutName'] = self.data_type_layout_name
        if self.field_set_id_list is not None:
            ret['fieldSetIdList'] = self.field_set_id_list
        if self.extension_type_list is not None:
            ret['extensionTypeList'] = self.extension_type_list
        if self.table_column_list is not None:
            ret['tableColumnList'] = [x.to_json() for x in self.table_column_list]
        if self.show_key_fields is not None:
            ret['showKeyFields'] = self.show_key_fields
        if self.is_field_addable is not None:
            ret['isFieldAddable'] = self.is_field_addable
        if self.is_existing_field_removable is not None:
            ret['isExistingFieldRemovable'] = self.is_existing_field_removable
        return ret


class ElnTempDataEntryUpdateCriteria(AbstractElnEntryUpdateCriteria):
    """
       Temporary Data Entry Update Data Payload.

       This class serves as a data holder for updating temporary data entry.
       Create an instance of this class, set the attributes you want to update,
       and then use the instance to send the request.

       Attributes:
           plugin_path (str or None): The path of the plugin.
       """
    plugin_path: Optional[str]

    def __init__(self):
        super().__init__(ElnEntryType.TempData)
        self.plugin_path = None

    def to_json(self) -> Dict[str, Any]:
        ret = super().to_json()
        if self.plugin_path is not None:
            ret['pluginPath'] = self.plugin_path
        return ret


class ElnTextEntryUpdateCriteria(AbstractElnEntryUpdateCriteria):
    """
    Text Entry Update Data Payload
    Create this payload object and set the attributes you want to update before sending the request.
    """

    def __init__(self):
        super().__init__(ElnEntryType.TempData)

    def to_json(self) -> Dict[str, Any]:
        ret = super().to_json()
        return ret


class ExperimentEntryCriteriaUtil:
    """
    Common utilities for ELN Experiment Entry Criteria
    """
    @staticmethod
    def create_empty_criteria(entry: ExperimentEntry) -> AbstractElnEntryUpdateCriteria:
        """
        Create an empty ELN entry criteria object based on the entry passed in.
        """
        entry_update_criteria: AbstractElnEntryUpdateCriteria
        if entry.entry_type == ElnEntryType.Attachment:
            entry_update_criteria = ElnAttachmentEntryUpdateCriteria()
        elif entry.entry_type == ElnEntryType.Dashboard:
            entry_update_criteria = ElnDashboardEntryUpdateCriteria()
        elif entry.entry_type == ElnEntryType.Form:
            entry_update_criteria = ElnFormEntryUpdateCriteria()
        elif entry.entry_type == ElnEntryType.Plugin:
            entry_update_criteria = ElnPluginEntryUpdateCriteria()
        elif entry.entry_type == ElnEntryType.Table:
            entry_update_criteria = ElnTableEntryUpdateCriteria()
        elif entry.entry_type == ElnEntryType.TempData:
            entry_update_criteria = ElnTempDataEntryUpdateCriteria()
        elif entry.entry_type == ElnEntryType.Text:
            entry_update_criteria = ElnTextEntryUpdateCriteria()
        else:
            raise ValueError("Unexpected entry type: " + entry.entry_type.name)
        return entry_update_criteria
