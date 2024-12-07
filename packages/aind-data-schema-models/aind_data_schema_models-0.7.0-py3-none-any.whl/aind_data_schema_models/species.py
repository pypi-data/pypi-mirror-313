"""Species"""

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema_models.registries import Registry


class _SpeciesModel(BaseModel):
    """Base model for platform"""

    model_config = ConfigDict(frozen=True)
    name: str
    registry: Registry.ONE_OF
    registry_identifier: str


class _Callithrix_Jacchus(_SpeciesModel):
    """Model Callithrix jacchus"""

    name: Literal["Callithrix jacchus"] = "Callithrix jacchus"
    registry: Registry.ONE_OF = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9483"] = "NCBI:txid9483"


class _Homo_Sapiens(_SpeciesModel):
    """Model Homo sapiens"""

    name: Literal["Homo sapiens"] = "Homo sapiens"
    registry: Registry.ONE_OF = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9606"] = "NCBI:txid9606"


class _Macaca_Mulatta(_SpeciesModel):
    """Model Macaca mulatta"""

    name: Literal["Macaca mulatta"] = "Macaca mulatta"
    registry: Registry.ONE_OF = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9544"] = "NCBI:txid9544"


class _Mus_Musculus(_SpeciesModel):
    """Model Mus musculus"""

    name: Literal["Mus musculus"] = "Mus musculus"
    registry: Registry.ONE_OF = Registry.NCBI
    registry_identifier: Literal["NCBI:txid10090"] = "NCBI:txid10090"


class _Rattus_Norvegicus(_SpeciesModel):
    """Model Rattus norvegicus"""

    name: Literal["Rattus norvegicus"] = "Rattus norvegicus"
    registry: Registry.ONE_OF = Registry.NCBI
    registry_identifier: Literal["NCBI:txid10116"] = "NCBI:txid10116"


class Species:
    """Species"""

    CALLITHRIX_JACCHUS = _Callithrix_Jacchus()
    HOMO_SAPIENS = _Homo_Sapiens()
    MACACA_MULATTA = _Macaca_Mulatta()
    MUS_MUSCULUS = _Mus_Musculus()
    RATTUS_NORVEGICUS = _Rattus_Norvegicus()

    ALL = tuple(_SpeciesModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(_SpeciesModel.__subclasses__())], Field(discriminator="name")]
