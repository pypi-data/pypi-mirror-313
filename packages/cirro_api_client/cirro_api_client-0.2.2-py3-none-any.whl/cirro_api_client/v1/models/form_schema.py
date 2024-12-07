from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.form_schema_form import FormSchemaForm
    from ..models.form_schema_ui import FormSchemaUi


T = TypeVar("T", bound="FormSchema")


@_attrs_define
class FormSchema:
    """
    Attributes:
        form (Union[Unset, FormSchemaForm]): JSONSchema representation of the parameters
        ui (Union[Unset, FormSchemaUi]): Describes how the form should be rendered, see rjsf
    """

    form: Union[Unset, "FormSchemaForm"] = UNSET
    ui: Union[Unset, "FormSchemaUi"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        form: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.form, Unset):
            form = self.form.to_dict()

        ui: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ui, Unset):
            ui = self.ui.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if form is not UNSET:
            field_dict["form"] = form
        if ui is not UNSET:
            field_dict["ui"] = ui

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.form_schema_form import FormSchemaForm
        from ..models.form_schema_ui import FormSchemaUi

        d = src_dict.copy()
        _form = d.pop("form", UNSET)
        form: Union[Unset, FormSchemaForm]
        if isinstance(_form, Unset):
            form = UNSET
        else:
            form = FormSchemaForm.from_dict(_form)

        _ui = d.pop("ui", UNSET)
        ui: Union[Unset, FormSchemaUi]
        if isinstance(_ui, Unset):
            ui = UNSET
        else:
            ui = FormSchemaUi.from_dict(_ui)

        form_schema = cls(
            form=form,
            ui=ui,
        )

        form_schema.additional_properties = d
        return form_schema

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())
