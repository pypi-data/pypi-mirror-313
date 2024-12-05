import glob
import os
from collections.abc import Sequence
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from dify_plugin.core.utils.yaml_loader import load_yaml_file
from dify_plugin.entities import I18nObject
from dify_plugin.entities.model import AIModelEntity, ModelType


class ConfigurateMethod(Enum):
    """
    Enum class for configurate method of provider model.
    """

    PREDEFINED_MODEL = "predefined-model"
    CUSTOMIZABLE_MODEL = "customizable-model"


class FormType(Enum):
    """
    Enum class for form type.
    """

    TEXT_INPUT = "text-input"
    SECRET_INPUT = "secret-input"
    SELECT = "select"
    RADIO = "radio"
    SWITCH = "switch"


class FormShowOnObject(BaseModel):
    """
    Model class for form show on.
    """

    variable: str
    value: str


class FormOption(BaseModel):
    """
    Model class for form option.
    """

    label: I18nObject
    value: str
    show_on: list[FormShowOnObject] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.label:
            self.label = I18nObject(en_US=self.value)


class CredentialFormSchema(BaseModel):
    """
    Model class for credential form schema.
    """

    variable: str
    label: I18nObject
    type: FormType
    required: bool = True
    default: Optional[str] = None
    options: Optional[list[FormOption]] = None
    placeholder: Optional[I18nObject] = None
    max_length: int = 0
    show_on: list[FormShowOnObject] = Field(default_factory=list)


class ProviderCredentialSchema(BaseModel):
    """
    Model class for provider credential schema.
    """

    credential_form_schemas: list[CredentialFormSchema]


class FieldModelSchema(BaseModel):
    label: I18nObject
    placeholder: Optional[I18nObject] = None


class ModelCredentialSchema(BaseModel):
    """
    Model class for model credential schema.
    """

    model: FieldModelSchema
    credential_form_schemas: list[CredentialFormSchema]


class SimpleProviderEntity(BaseModel):
    """
    Simple model class for provider.
    """

    provider: str
    label: I18nObject
    icon_small: Optional[I18nObject] = None
    icon_large: Optional[I18nObject] = None
    supported_model_types: Sequence[ModelType]
    models: list[AIModelEntity] = []


class ProviderHelpEntity(BaseModel):
    """
    Model class for provider help.
    """

    title: I18nObject
    url: I18nObject


class ModelPosition(BaseModel):
    """
    Model class for ai models
    """

    llm: Optional[list[str]] = Field(default_factory=list)
    text_embedding: Optional[list[str]] = Field(default_factory=list)
    rerank: Optional[list[str]] = Field(default_factory=list)
    tts: Optional[list[str]] = Field(default_factory=list)
    speech2text: Optional[list[str]] = Field(default_factory=list)
    moderation: Optional[list[str]] = Field(default_factory=list)


class ProviderEntity(BaseModel):
    """
    Model class for provider.
    """

    provider: str
    label: I18nObject
    description: Optional[I18nObject] = None
    icon_small: Optional[I18nObject] = None
    icon_large: Optional[I18nObject] = None
    background: Optional[str] = None
    help: Optional[ProviderHelpEntity] = None
    supported_model_types: Sequence[ModelType]
    configurate_methods: list[ConfigurateMethod]
    models: list[AIModelEntity] = Field(default_factory=list)
    provider_credential_schema: Optional[ProviderCredentialSchema] = None
    model_credential_schema: Optional[ModelCredentialSchema] = None
    position: Optional[ModelPosition] = None

    # pydantic configs
    model_config = ConfigDict(protected_namespaces=())

    def to_simple_provider(self) -> SimpleProviderEntity:
        """
        Convert to simple provider.

        :return: simple provider
        """
        return SimpleProviderEntity(
            provider=self.provider,
            label=self.label,
            icon_small=self.icon_small,
            icon_large=self.icon_large,
            supported_model_types=self.supported_model_types,
            models=self.models,
        )

    @model_validator(mode="before")
    @classmethod
    def validate_models(cls, values) -> dict:
        value = values.get("models", {})
        if not isinstance(value, dict):
            raise ValueError("models should be a glob path list")

        cwd = os.getcwd()

        model_entities = []

        def load_models(model_type: str):
            if model_type not in value:
                return

            for path in value[model_type].get("predefined", []):
                yaml_paths = glob.glob(os.path.join(cwd, path))
                for yaml_path in yaml_paths:
                    if yaml_path.endswith("_position.yaml"):
                        if "position" not in values:
                            values["position"] = {}

                        position = load_yaml_file(yaml_path)
                        values["position"][model_type] = position
                    else:
                        model_entity = load_yaml_file(yaml_path)
                        if not model_entity:
                            raise ValueError(f"Error loading model entity: {yaml_path}")

                        provider_model = AIModelEntity(**model_entity)
                        model_entities.append(provider_model)

        load_models("llm")
        load_models("text_embedding")
        load_models("rerank")
        load_models("tts")
        load_models("speech2text")
        load_models("moderation")

        values["models"] = model_entities

        return values


class ModelProviderConfigurationExtra(BaseModel):
    class Python(BaseModel):
        provider_source: str
        model_sources: list[str] = Field(default_factory=list)

        model_config = ConfigDict(protected_namespaces=())

    python: Python


class ModelProviderConfiguration(ProviderEntity):
    extra: ModelProviderConfigurationExtra


# class ProviderConfig(BaseModel):
#     """
#     Model class for provider config.
#     """

#     provider: str
#     credentials: dict
