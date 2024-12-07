"""Platforms"""

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class _BrainStructureModel(BaseModel):
    """Base model for brain strutures"""

    model_config = ConfigDict(frozen=True)
    atlas: str
    name: str
    acronym: str
    id: str


class _Vi(_BrainStructureModel):
    """Model VI"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Abducens nucleus"] = "Abducens nucleus"
    acronym: Literal["VI"] = "VI"
    id: Literal["653"] = "653"


class _Acvii(_BrainStructureModel):
    """Model ACVII"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Accessory facial motor nucleus"] = "Accessory facial motor nucleus"
    acronym: Literal["ACVII"] = "ACVII"
    id: Literal["576"] = "576"


class _Aob(_BrainStructureModel):
    """Model AOB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Accessory olfactory bulb"] = "Accessory olfactory bulb"
    acronym: Literal["AOB"] = "AOB"
    id: Literal["151"] = "151"


class _Aobgl(_BrainStructureModel):
    """Model AOBgl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Accessory olfactory bulb, glomerular layer"] = "Accessory olfactory bulb, glomerular layer"
    acronym: Literal["AOBgl"] = "AOBgl"
    id: Literal["188"] = "188"


class _Aobgr(_BrainStructureModel):
    """Model AOBgr"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Accessory olfactory bulb, granular layer"] = "Accessory olfactory bulb, granular layer"
    acronym: Literal["AOBgr"] = "AOBgr"
    id: Literal["196"] = "196"


class _Aobmi(_BrainStructureModel):
    """Model AOBmi"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Accessory olfactory bulb, mitral layer"] = "Accessory olfactory bulb, mitral layer"
    acronym: Literal["AOBmi"] = "AOBmi"
    id: Literal["204"] = "204"


class _Aso(_BrainStructureModel):
    """Model ASO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Accessory supraoptic group"] = "Accessory supraoptic group"
    acronym: Literal["ASO"] = "ASO"
    id: Literal["332"] = "332"


class _Acs5(_BrainStructureModel):
    """Model Acs5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Accessory trigeminal nucleus"] = "Accessory trigeminal nucleus"
    acronym: Literal["Acs5"] = "Acs5"
    id: Literal["549009219"] = "549009219"


class _Ai(_BrainStructureModel):
    """Model AI"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area"] = "Agranular insular area"
    acronym: Literal["AI"] = "AI"
    id: Literal["95"] = "95"


class _Aid(_BrainStructureModel):
    """Model AId"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, dorsal part"] = "Agranular insular area, dorsal part"
    acronym: Literal["AId"] = "AId"
    id: Literal["104"] = "104"


class _Aid1(_BrainStructureModel):
    """Model AId1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, dorsal part, layer 1"] = "Agranular insular area, dorsal part, layer 1"
    acronym: Literal["AId1"] = "AId1"
    id: Literal["996"] = "996"


class _Aid2_3(_BrainStructureModel):
    """Model AId2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, dorsal part, layer 2/3"] = "Agranular insular area, dorsal part, layer 2/3"
    acronym: Literal["AId2/3"] = "AId2/3"
    id: Literal["328"] = "328"


class _Aid5(_BrainStructureModel):
    """Model AId5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, dorsal part, layer 5"] = "Agranular insular area, dorsal part, layer 5"
    acronym: Literal["AId5"] = "AId5"
    id: Literal["1101"] = "1101"


class _Aid6A(_BrainStructureModel):
    """Model AId6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, dorsal part, layer 6a"] = "Agranular insular area, dorsal part, layer 6a"
    acronym: Literal["AId6a"] = "AId6a"
    id: Literal["783"] = "783"


class _Aid6B(_BrainStructureModel):
    """Model AId6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, dorsal part, layer 6b"] = "Agranular insular area, dorsal part, layer 6b"
    acronym: Literal["AId6b"] = "AId6b"
    id: Literal["831"] = "831"


class _Aip(_BrainStructureModel):
    """Model AIp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, posterior part"] = "Agranular insular area, posterior part"
    acronym: Literal["AIp"] = "AIp"
    id: Literal["111"] = "111"


class _Aip1(_BrainStructureModel):
    """Model AIp1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, posterior part, layer 1"] = "Agranular insular area, posterior part, layer 1"
    acronym: Literal["AIp1"] = "AIp1"
    id: Literal["120"] = "120"


class _Aip2_3(_BrainStructureModel):
    """Model AIp2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, posterior part, layer 2/3"] = (
        "Agranular insular area, posterior part, layer 2/3"
    )
    acronym: Literal["AIp2/3"] = "AIp2/3"
    id: Literal["163"] = "163"


class _Aip5(_BrainStructureModel):
    """Model AIp5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, posterior part, layer 5"] = "Agranular insular area, posterior part, layer 5"
    acronym: Literal["AIp5"] = "AIp5"
    id: Literal["344"] = "344"


class _Aip6A(_BrainStructureModel):
    """Model AIp6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, posterior part, layer 6a"] = (
        "Agranular insular area, posterior part, layer 6a"
    )
    acronym: Literal["AIp6a"] = "AIp6a"
    id: Literal["314"] = "314"


class _Aip6B(_BrainStructureModel):
    """Model AIp6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, posterior part, layer 6b"] = (
        "Agranular insular area, posterior part, layer 6b"
    )
    acronym: Literal["AIp6b"] = "AIp6b"
    id: Literal["355"] = "355"


class _Aiv(_BrainStructureModel):
    """Model AIv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, ventral part"] = "Agranular insular area, ventral part"
    acronym: Literal["AIv"] = "AIv"
    id: Literal["119"] = "119"


class _Aiv1(_BrainStructureModel):
    """Model AIv1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, ventral part, layer 1"] = "Agranular insular area, ventral part, layer 1"
    acronym: Literal["AIv1"] = "AIv1"
    id: Literal["704"] = "704"


class _Aiv2_3(_BrainStructureModel):
    """Model AIv2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, ventral part, layer 2/3"] = "Agranular insular area, ventral part, layer 2/3"
    acronym: Literal["AIv2/3"] = "AIv2/3"
    id: Literal["694"] = "694"


class _Aiv5(_BrainStructureModel):
    """Model AIv5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, ventral part, layer 5"] = "Agranular insular area, ventral part, layer 5"
    acronym: Literal["AIv5"] = "AIv5"
    id: Literal["800"] = "800"


class _Aiv6A(_BrainStructureModel):
    """Model AIv6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, ventral part, layer 6a"] = "Agranular insular area, ventral part, layer 6a"
    acronym: Literal["AIv6a"] = "AIv6a"
    id: Literal["675"] = "675"


class _Aiv6B(_BrainStructureModel):
    """Model AIv6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Agranular insular area, ventral part, layer 6b"] = "Agranular insular area, ventral part, layer 6b"
    acronym: Literal["AIv6b"] = "AIv6b"
    id: Literal["699"] = "699"


class _Ca(_BrainStructureModel):
    """Model CA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ammon's horn"] = "Ammon's horn"
    acronym: Literal["CA"] = "CA"
    id: Literal["375"] = "375"


class _An(_BrainStructureModel):
    """Model AN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ansiform lobule"] = "Ansiform lobule"
    acronym: Literal["AN"] = "AN"
    id: Literal["1017"] = "1017"


class _Aaa(_BrainStructureModel):
    """Model AAA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior amygdalar area"] = "Anterior amygdalar area"
    acronym: Literal["AAA"] = "AAA"
    id: Literal["23"] = "23"


class _Visa(_BrainStructureModel):
    """Model VISa"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior area"] = "Anterior area"
    acronym: Literal["VISa"] = "VISa"
    id: Literal["312782546"] = "312782546"


class _Visa1(_BrainStructureModel):
    """Model VISa1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior area, layer 1"] = "Anterior area, layer 1"
    acronym: Literal["VISa1"] = "VISa1"
    id: Literal["312782550"] = "312782550"


class _Visa2_3(_BrainStructureModel):
    """Model VISa2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior area, layer 2/3"] = "Anterior area, layer 2/3"
    acronym: Literal["VISa2/3"] = "VISa2/3"
    id: Literal["312782554"] = "312782554"


class _Visa4(_BrainStructureModel):
    """Model VISa4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior area, layer 4"] = "Anterior area, layer 4"
    acronym: Literal["VISa4"] = "VISa4"
    id: Literal["312782558"] = "312782558"


class _Visa5(_BrainStructureModel):
    """Model VISa5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior area, layer 5"] = "Anterior area, layer 5"
    acronym: Literal["VISa5"] = "VISa5"
    id: Literal["312782562"] = "312782562"


class _Visa6A(_BrainStructureModel):
    """Model VISa6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior area, layer 6a"] = "Anterior area, layer 6a"
    acronym: Literal["VISa6a"] = "VISa6a"
    id: Literal["312782566"] = "312782566"


class _Visa6B(_BrainStructureModel):
    """Model VISa6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior area, layer 6b"] = "Anterior area, layer 6b"
    acronym: Literal["VISa6b"] = "VISa6b"
    id: Literal["312782570"] = "312782570"


class _Aca(_BrainStructureModel):
    """Model ACA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area"] = "Anterior cingulate area"
    acronym: Literal["ACA"] = "ACA"
    id: Literal["31"] = "31"


class _Acad(_BrainStructureModel):
    """Model ACAd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, dorsal part"] = "Anterior cingulate area, dorsal part"
    acronym: Literal["ACAd"] = "ACAd"
    id: Literal["39"] = "39"


class _Acad1(_BrainStructureModel):
    """Model ACAd1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, dorsal part, layer 1"] = "Anterior cingulate area, dorsal part, layer 1"
    acronym: Literal["ACAd1"] = "ACAd1"
    id: Literal["935"] = "935"


class _Acad2_3(_BrainStructureModel):
    """Model ACAd2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, dorsal part, layer 2/3"] = "Anterior cingulate area, dorsal part, layer 2/3"
    acronym: Literal["ACAd2/3"] = "ACAd2/3"
    id: Literal["211"] = "211"


class _Acad5(_BrainStructureModel):
    """Model ACAd5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, dorsal part, layer 5"] = "Anterior cingulate area, dorsal part, layer 5"
    acronym: Literal["ACAd5"] = "ACAd5"
    id: Literal["1015"] = "1015"


class _Acad6A(_BrainStructureModel):
    """Model ACAd6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, dorsal part, layer 6a"] = "Anterior cingulate area, dorsal part, layer 6a"
    acronym: Literal["ACAd6a"] = "ACAd6a"
    id: Literal["919"] = "919"


class _Acad6B(_BrainStructureModel):
    """Model ACAd6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, dorsal part, layer 6b"] = "Anterior cingulate area, dorsal part, layer 6b"
    acronym: Literal["ACAd6b"] = "ACAd6b"
    id: Literal["927"] = "927"


class _Acav(_BrainStructureModel):
    """Model ACAv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, ventral part"] = "Anterior cingulate area, ventral part"
    acronym: Literal["ACAv"] = "ACAv"
    id: Literal["48"] = "48"


class _Acav6A(_BrainStructureModel):
    """Model ACAv6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, ventral part, 6a"] = "Anterior cingulate area, ventral part, 6a"
    acronym: Literal["ACAv6a"] = "ACAv6a"
    id: Literal["810"] = "810"


class _Acav6B(_BrainStructureModel):
    """Model ACAv6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, ventral part, 6b"] = "Anterior cingulate area, ventral part, 6b"
    acronym: Literal["ACAv6b"] = "ACAv6b"
    id: Literal["819"] = "819"


class _Acav1(_BrainStructureModel):
    """Model ACAv1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, ventral part, layer 1"] = "Anterior cingulate area, ventral part, layer 1"
    acronym: Literal["ACAv1"] = "ACAv1"
    id: Literal["588"] = "588"


class _Acav2_3(_BrainStructureModel):
    """Model ACAv2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, ventral part, layer 2/3"] = (
        "Anterior cingulate area, ventral part, layer 2/3"
    )
    acronym: Literal["ACAv2/3"] = "ACAv2/3"
    id: Literal["296"] = "296"


class _Acav5(_BrainStructureModel):
    """Model ACAv5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior cingulate area, ventral part, layer 5"] = "Anterior cingulate area, ventral part, layer 5"
    acronym: Literal["ACAv5"] = "ACAv5"
    id: Literal["772"] = "772"


class _Atn(_BrainStructureModel):
    """Model ATN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior group of the dorsal thalamus"] = "Anterior group of the dorsal thalamus"
    acronym: Literal["ATN"] = "ATN"
    id: Literal["239"] = "239"


class _Ahn(_BrainStructureModel):
    """Model AHN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior hypothalamic nucleus"] = "Anterior hypothalamic nucleus"
    acronym: Literal["AHN"] = "AHN"
    id: Literal["88"] = "88"


class _Aon(_BrainStructureModel):
    """Model AON"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior olfactory nucleus"] = "Anterior olfactory nucleus"
    acronym: Literal["AON"] = "AON"
    id: Literal["159"] = "159"


class _Apn(_BrainStructureModel):
    """Model APN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior pretectal nucleus"] = "Anterior pretectal nucleus"
    acronym: Literal["APN"] = "APN"
    id: Literal["215"] = "215"


class _At(_BrainStructureModel):
    """Model AT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterior tegmental nucleus"] = "Anterior tegmental nucleus"
    acronym: Literal["AT"] = "AT"
    id: Literal["231"] = "231"


class _Ad(_BrainStructureModel):
    """Model AD"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterodorsal nucleus"] = "Anterodorsal nucleus"
    acronym: Literal["AD"] = "AD"
    id: Literal["64"] = "64"


class _Adp(_BrainStructureModel):
    """Model ADP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterodorsal preoptic nucleus"] = "Anterodorsal preoptic nucleus"
    acronym: Literal["ADP"] = "ADP"
    id: Literal["72"] = "72"


class _Visal(_BrainStructureModel):
    """Model VISal"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterolateral visual area"] = "Anterolateral visual area"
    acronym: Literal["VISal"] = "VISal"
    id: Literal["402"] = "402"


class _Visal1(_BrainStructureModel):
    """Model VISal1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterolateral visual area, layer 1"] = "Anterolateral visual area, layer 1"
    acronym: Literal["VISal1"] = "VISal1"
    id: Literal["1074"] = "1074"


class _Visal2_3(_BrainStructureModel):
    """Model VISal2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterolateral visual area, layer 2/3"] = "Anterolateral visual area, layer 2/3"
    acronym: Literal["VISal2/3"] = "VISal2/3"
    id: Literal["905"] = "905"


class _Visal4(_BrainStructureModel):
    """Model VISal4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterolateral visual area, layer 4"] = "Anterolateral visual area, layer 4"
    acronym: Literal["VISal4"] = "VISal4"
    id: Literal["1114"] = "1114"


class _Visal5(_BrainStructureModel):
    """Model VISal5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterolateral visual area, layer 5"] = "Anterolateral visual area, layer 5"
    acronym: Literal["VISal5"] = "VISal5"
    id: Literal["233"] = "233"


class _Visal6A(_BrainStructureModel):
    """Model VISal6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterolateral visual area, layer 6a"] = "Anterolateral visual area, layer 6a"
    acronym: Literal["VISal6a"] = "VISal6a"
    id: Literal["601"] = "601"


class _Visal6B(_BrainStructureModel):
    """Model VISal6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anterolateral visual area, layer 6b"] = "Anterolateral visual area, layer 6b"
    acronym: Literal["VISal6b"] = "VISal6b"
    id: Literal["649"] = "649"


class _Am(_BrainStructureModel):
    """Model AM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteromedial nucleus"] = "Anteromedial nucleus"
    acronym: Literal["AM"] = "AM"
    id: Literal["127"] = "127"


class _Amd(_BrainStructureModel):
    """Model AMd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteromedial nucleus, dorsal part"] = "Anteromedial nucleus, dorsal part"
    acronym: Literal["AMd"] = "AMd"
    id: Literal["1096"] = "1096"


class _Amv(_BrainStructureModel):
    """Model AMv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteromedial nucleus, ventral part"] = "Anteromedial nucleus, ventral part"
    acronym: Literal["AMv"] = "AMv"
    id: Literal["1104"] = "1104"


class _Visam(_BrainStructureModel):
    """Model VISam"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteromedial visual area"] = "Anteromedial visual area"
    acronym: Literal["VISam"] = "VISam"
    id: Literal["394"] = "394"


class _Visam1(_BrainStructureModel):
    """Model VISam1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteromedial visual area, layer 1"] = "Anteromedial visual area, layer 1"
    acronym: Literal["VISam1"] = "VISam1"
    id: Literal["281"] = "281"


class _Visam2_3(_BrainStructureModel):
    """Model VISam2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteromedial visual area, layer 2/3"] = "Anteromedial visual area, layer 2/3"
    acronym: Literal["VISam2/3"] = "VISam2/3"
    id: Literal["1066"] = "1066"


class _Visam4(_BrainStructureModel):
    """Model VISam4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteromedial visual area, layer 4"] = "Anteromedial visual area, layer 4"
    acronym: Literal["VISam4"] = "VISam4"
    id: Literal["401"] = "401"


class _Visam5(_BrainStructureModel):
    """Model VISam5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteromedial visual area, layer 5"] = "Anteromedial visual area, layer 5"
    acronym: Literal["VISam5"] = "VISam5"
    id: Literal["433"] = "433"


class _Visam6A(_BrainStructureModel):
    """Model VISam6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteromedial visual area, layer 6a"] = "Anteromedial visual area, layer 6a"
    acronym: Literal["VISam6a"] = "VISam6a"
    id: Literal["1046"] = "1046"


class _Visam6B(_BrainStructureModel):
    """Model VISam6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteromedial visual area, layer 6b"] = "Anteromedial visual area, layer 6b"
    acronym: Literal["VISam6b"] = "VISam6b"
    id: Literal["441"] = "441"


class _Av(_BrainStructureModel):
    """Model AV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteroventral nucleus of thalamus"] = "Anteroventral nucleus of thalamus"
    acronym: Literal["AV"] = "AV"
    id: Literal["255"] = "255"


class _Avpv(_BrainStructureModel):
    """Model AVPV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteroventral periventricular nucleus"] = "Anteroventral periventricular nucleus"
    acronym: Literal["AVPV"] = "AVPV"
    id: Literal["272"] = "272"


class _Avp(_BrainStructureModel):
    """Model AVP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Anteroventral preoptic nucleus"] = "Anteroventral preoptic nucleus"
    acronym: Literal["AVP"] = "AVP"
    id: Literal["263"] = "263"


class _Arh(_BrainStructureModel):
    """Model ARH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Arcuate hypothalamic nucleus"] = "Arcuate hypothalamic nucleus"
    acronym: Literal["ARH"] = "ARH"
    id: Literal["223"] = "223"


class _Ap(_BrainStructureModel):
    """Model AP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Area postrema"] = "Area postrema"
    acronym: Literal["AP"] = "AP"
    id: Literal["207"] = "207"


class _Apr(_BrainStructureModel):
    """Model APr"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Area prostriata"] = "Area prostriata"
    acronym: Literal["APr"] = "APr"
    id: Literal["484682508"] = "484682508"


class _Aud(_BrainStructureModel):
    """Model AUD"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Auditory areas"] = "Auditory areas"
    acronym: Literal["AUD"] = "AUD"
    id: Literal["247"] = "247"


class _B(_BrainStructureModel):
    """Model B"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Barrington's nucleus"] = "Barrington's nucleus"
    acronym: Literal["B"] = "B"
    id: Literal["280"] = "280"


class _Grey(_BrainStructureModel):
    """Model grey"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Basic cell groups and regions"] = "Basic cell groups and regions"
    acronym: Literal["grey"] = "grey"
    id: Literal["8"] = "8"


class _Bla(_BrainStructureModel):
    """Model BLA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Basolateral amygdalar nucleus"] = "Basolateral amygdalar nucleus"
    acronym: Literal["BLA"] = "BLA"
    id: Literal["295"] = "295"


class _Blaa(_BrainStructureModel):
    """Model BLAa"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Basolateral amygdalar nucleus, anterior part"] = "Basolateral amygdalar nucleus, anterior part"
    acronym: Literal["BLAa"] = "BLAa"
    id: Literal["303"] = "303"


class _Blap(_BrainStructureModel):
    """Model BLAp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Basolateral amygdalar nucleus, posterior part"] = "Basolateral amygdalar nucleus, posterior part"
    acronym: Literal["BLAp"] = "BLAp"
    id: Literal["311"] = "311"


class _Blav(_BrainStructureModel):
    """Model BLAv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Basolateral amygdalar nucleus, ventral part"] = "Basolateral amygdalar nucleus, ventral part"
    acronym: Literal["BLAv"] = "BLAv"
    id: Literal["451"] = "451"


class _Bma(_BrainStructureModel):
    """Model BMA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Basomedial amygdalar nucleus"] = "Basomedial amygdalar nucleus"
    acronym: Literal["BMA"] = "BMA"
    id: Literal["319"] = "319"


class _Bmaa(_BrainStructureModel):
    """Model BMAa"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Basomedial amygdalar nucleus, anterior part"] = "Basomedial amygdalar nucleus, anterior part"
    acronym: Literal["BMAa"] = "BMAa"
    id: Literal["327"] = "327"


class _Bmap(_BrainStructureModel):
    """Model BMAp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Basomedial amygdalar nucleus, posterior part"] = "Basomedial amygdalar nucleus, posterior part"
    acronym: Literal["BMAp"] = "BMAp"
    id: Literal["334"] = "334"


class _Bst(_BrainStructureModel):
    """Model BST"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Bed nuclei of the stria terminalis"] = "Bed nuclei of the stria terminalis"
    acronym: Literal["BST"] = "BST"
    id: Literal["351"] = "351"


class _Ba(_BrainStructureModel):
    """Model BA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Bed nucleus of the accessory olfactory tract"] = "Bed nucleus of the accessory olfactory tract"
    acronym: Literal["BA"] = "BA"
    id: Literal["292"] = "292"


class _Bac(_BrainStructureModel):
    """Model BAC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Bed nucleus of the anterior commissure"] = "Bed nucleus of the anterior commissure"
    acronym: Literal["BAC"] = "BAC"
    id: Literal["287"] = "287"


class _Bs(_BrainStructureModel):
    """Model BS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Brain stem"] = "Brain stem"
    acronym: Literal["BS"] = "BS"
    id: Literal["343"] = "343"


class _Cp(_BrainStructureModel):
    """Model CP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Caudoputamen"] = "Caudoputamen"
    acronym: Literal["CP"] = "CP"
    id: Literal["672"] = "672"


class _Cea(_BrainStructureModel):
    """Model CEA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Central amygdalar nucleus"] = "Central amygdalar nucleus"
    acronym: Literal["CEA"] = "CEA"
    id: Literal["536"] = "536"


class _Ceac(_BrainStructureModel):
    """Model CEAc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Central amygdalar nucleus, capsular part"] = "Central amygdalar nucleus, capsular part"
    acronym: Literal["CEAc"] = "CEAc"
    id: Literal["544"] = "544"


class _Ceal(_BrainStructureModel):
    """Model CEAl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Central amygdalar nucleus, lateral part"] = "Central amygdalar nucleus, lateral part"
    acronym: Literal["CEAl"] = "CEAl"
    id: Literal["551"] = "551"


class _Ceam(_BrainStructureModel):
    """Model CEAm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Central amygdalar nucleus, medial part"] = "Central amygdalar nucleus, medial part"
    acronym: Literal["CEAm"] = "CEAm"
    id: Literal["559"] = "559"


class _Cl(_BrainStructureModel):
    """Model CL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Central lateral nucleus of the thalamus"] = "Central lateral nucleus of the thalamus"
    acronym: Literal["CL"] = "CL"
    id: Literal["575"] = "575"


class _Cli(_BrainStructureModel):
    """Model CLI"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Central linear nucleus raphe"] = "Central linear nucleus raphe"
    acronym: Literal["CLI"] = "CLI"
    id: Literal["591"] = "591"


class _Cent(_BrainStructureModel):
    """Model CENT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Central lobule"] = "Central lobule"
    acronym: Literal["CENT"] = "CENT"
    id: Literal["920"] = "920"


class _Cm(_BrainStructureModel):
    """Model CM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Central medial nucleus of the thalamus"] = "Central medial nucleus of the thalamus"
    acronym: Literal["CM"] = "CM"
    id: Literal["599"] = "599"


class _Cbx(_BrainStructureModel):
    """Model CBX"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cerebellar cortex"] = "Cerebellar cortex"
    acronym: Literal["CBX"] = "CBX"
    id: Literal["528"] = "528"


class _Cbn(_BrainStructureModel):
    """Model CBN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cerebellar nuclei"] = "Cerebellar nuclei"
    acronym: Literal["CBN"] = "CBN"
    id: Literal["519"] = "519"


class _Cb(_BrainStructureModel):
    """Model CB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cerebellum"] = "Cerebellum"
    acronym: Literal["CB"] = "CB"
    id: Literal["512"] = "512"


class _Ctx(_BrainStructureModel):
    """Model CTX"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cerebral cortex"] = "Cerebral cortex"
    acronym: Literal["CTX"] = "CTX"
    id: Literal["688"] = "688"


class _Cnu(_BrainStructureModel):
    """Model CNU"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cerebral nuclei"] = "Cerebral nuclei"
    acronym: Literal["CNU"] = "CNU"
    id: Literal["623"] = "623"


class _Ch(_BrainStructureModel):
    """Model CH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cerebrum"] = "Cerebrum"
    acronym: Literal["CH"] = "CH"
    id: Literal["567"] = "567"


class _Cla(_BrainStructureModel):
    """Model CLA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Claustrum"] = "Claustrum"
    acronym: Literal["CLA"] = "CLA"
    id: Literal["583"] = "583"


class _Cn(_BrainStructureModel):
    """Model CN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cochlear nuclei"] = "Cochlear nuclei"
    acronym: Literal["CN"] = "CN"
    id: Literal["607"] = "607"


class _Copy(_BrainStructureModel):
    """Model COPY"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Copula pyramidis"] = "Copula pyramidis"
    acronym: Literal["COPY"] = "COPY"
    id: Literal["1033"] = "1033"


class _Coa(_BrainStructureModel):
    """Model COA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cortical amygdalar area"] = "Cortical amygdalar area"
    acronym: Literal["COA"] = "COA"
    id: Literal["631"] = "631"


class _Coaa(_BrainStructureModel):
    """Model COAa"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cortical amygdalar area, anterior part"] = "Cortical amygdalar area, anterior part"
    acronym: Literal["COAa"] = "COAa"
    id: Literal["639"] = "639"


class _Coap(_BrainStructureModel):
    """Model COAp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cortical amygdalar area, posterior part"] = "Cortical amygdalar area, posterior part"
    acronym: Literal["COAp"] = "COAp"
    id: Literal["647"] = "647"


class _Coapl(_BrainStructureModel):
    """Model COApl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cortical amygdalar area, posterior part, lateral zone"] = (
        "Cortical amygdalar area, posterior part, lateral zone"
    )
    acronym: Literal["COApl"] = "COApl"
    id: Literal["655"] = "655"


class _Coapm(_BrainStructureModel):
    """Model COApm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cortical amygdalar area, posterior part, medial zone"] = (
        "Cortical amygdalar area, posterior part, medial zone"
    )
    acronym: Literal["COApm"] = "COApm"
    id: Literal["663"] = "663"


class _Ctxpl(_BrainStructureModel):
    """Model CTXpl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cortical plate"] = "Cortical plate"
    acronym: Literal["CTXpl"] = "CTXpl"
    id: Literal["695"] = "695"


class _Ctxsp(_BrainStructureModel):
    """Model CTXsp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cortical subplate"] = "Cortical subplate"
    acronym: Literal["CTXsp"] = "CTXsp"
    id: Literal["703"] = "703"


class _Ancr1(_BrainStructureModel):
    """Model ANcr1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Crus 1"] = "Crus 1"
    acronym: Literal["ANcr1"] = "ANcr1"
    id: Literal["1056"] = "1056"


class _Ancr2(_BrainStructureModel):
    """Model ANcr2"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Crus 2"] = "Crus 2"
    acronym: Literal["ANcr2"] = "ANcr2"
    id: Literal["1064"] = "1064"


class _Cul(_BrainStructureModel):
    """Model CUL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Culmen"] = "Culmen"
    acronym: Literal["CUL"] = "CUL"
    id: Literal["928"] = "928"


class _Cu(_BrainStructureModel):
    """Model CU"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cuneate nucleus"] = "Cuneate nucleus"
    acronym: Literal["CU"] = "CU"
    id: Literal["711"] = "711"


class _Cun(_BrainStructureModel):
    """Model CUN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Cuneiform nucleus"] = "Cuneiform nucleus"
    acronym: Literal["CUN"] = "CUN"
    id: Literal["616"] = "616"


class _Dec(_BrainStructureModel):
    """Model DEC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Declive (VI)"] = "Declive (VI)"
    acronym: Literal["DEC"] = "DEC"
    id: Literal["936"] = "936"


class _Dg(_BrainStructureModel):
    """Model DG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dentate gyrus"] = "Dentate gyrus"
    acronym: Literal["DG"] = "DG"
    id: Literal["726"] = "726"


class _Dg_Sg(_BrainStructureModel):
    """Model DG-sg"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dentate gyrus, granule cell layer"] = "Dentate gyrus, granule cell layer"
    acronym: Literal["DG-sg"] = "DG-sg"
    id: Literal["632"] = "632"


class _Dg_Mo(_BrainStructureModel):
    """Model DG-mo"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dentate gyrus, molecular layer"] = "Dentate gyrus, molecular layer"
    acronym: Literal["DG-mo"] = "DG-mo"
    id: Literal["10703"] = "10703"


class _Dg_Po(_BrainStructureModel):
    """Model DG-po"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dentate gyrus, polymorph layer"] = "Dentate gyrus, polymorph layer"
    acronym: Literal["DG-po"] = "DG-po"
    id: Literal["10704"] = "10704"


class _Dn(_BrainStructureModel):
    """Model DN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dentate nucleus"] = "Dentate nucleus"
    acronym: Literal["DN"] = "DN"
    id: Literal["846"] = "846"


class _Ndb(_BrainStructureModel):
    """Model NDB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Diagonal band nucleus"] = "Diagonal band nucleus"
    acronym: Literal["NDB"] = "NDB"
    id: Literal["596"] = "596"


class _Audd(_BrainStructureModel):
    """Model AUDd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal auditory area"] = "Dorsal auditory area"
    acronym: Literal["AUDd"] = "AUDd"
    id: Literal["1011"] = "1011"


class _Audd1(_BrainStructureModel):
    """Model AUDd1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal auditory area, layer 1"] = "Dorsal auditory area, layer 1"
    acronym: Literal["AUDd1"] = "AUDd1"
    id: Literal["527"] = "527"


class _Audd2_3(_BrainStructureModel):
    """Model AUDd2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal auditory area, layer 2/3"] = "Dorsal auditory area, layer 2/3"
    acronym: Literal["AUDd2/3"] = "AUDd2/3"
    id: Literal["600"] = "600"


class _Audd4(_BrainStructureModel):
    """Model AUDd4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal auditory area, layer 4"] = "Dorsal auditory area, layer 4"
    acronym: Literal["AUDd4"] = "AUDd4"
    id: Literal["678"] = "678"


class _Audd5(_BrainStructureModel):
    """Model AUDd5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal auditory area, layer 5"] = "Dorsal auditory area, layer 5"
    acronym: Literal["AUDd5"] = "AUDd5"
    id: Literal["252"] = "252"


class _Audd6A(_BrainStructureModel):
    """Model AUDd6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal auditory area, layer 6a"] = "Dorsal auditory area, layer 6a"
    acronym: Literal["AUDd6a"] = "AUDd6a"
    id: Literal["156"] = "156"


class _Audd6B(_BrainStructureModel):
    """Model AUDd6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal auditory area, layer 6b"] = "Dorsal auditory area, layer 6b"
    acronym: Literal["AUDd6b"] = "AUDd6b"
    id: Literal["243"] = "243"


class _Dco(_BrainStructureModel):
    """Model DCO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal cochlear nucleus"] = "Dorsal cochlear nucleus"
    acronym: Literal["DCO"] = "DCO"
    id: Literal["96"] = "96"


class _Dcn(_BrainStructureModel):
    """Model DCN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal column nuclei"] = "Dorsal column nuclei"
    acronym: Literal["DCN"] = "DCN"
    id: Literal["720"] = "720"


class _Dmx(_BrainStructureModel):
    """Model DMX"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal motor nucleus of the vagus nerve"] = "Dorsal motor nucleus of the vagus nerve"
    acronym: Literal["DMX"] = "DMX"
    id: Literal["839"] = "839"


class _Dr(_BrainStructureModel):
    """Model DR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal nucleus raphe"] = "Dorsal nucleus raphe"
    acronym: Literal["DR"] = "DR"
    id: Literal["872"] = "872"


class _Lgd(_BrainStructureModel):
    """Model LGd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal part of the lateral geniculate complex"] = "Dorsal part of the lateral geniculate complex"
    acronym: Literal["LGd"] = "LGd"
    id: Literal["170"] = "170"


class _Lgd_Co(_BrainStructureModel):
    """Model LGd-co"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal part of the lateral geniculate complex, core"] = (
        "Dorsal part of the lateral geniculate complex, core"
    )
    acronym: Literal["LGd-co"] = "LGd-co"
    id: Literal["496345668"] = "496345668"


class _Lgd_Ip(_BrainStructureModel):
    """Model LGd-ip"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal part of the lateral geniculate complex, ipsilateral zone"] = (
        "Dorsal part of the lateral geniculate complex, ipsilateral zone"
    )
    acronym: Literal["LGd-ip"] = "LGd-ip"
    id: Literal["496345672"] = "496345672"


class _Lgd_Sh(_BrainStructureModel):
    """Model LGd-sh"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal part of the lateral geniculate complex, shell"] = (
        "Dorsal part of the lateral geniculate complex, shell"
    )
    acronym: Literal["LGd-sh"] = "LGd-sh"
    id: Literal["496345664"] = "496345664"


class _Dp(_BrainStructureModel):
    """Model DP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal peduncular area"] = "Dorsal peduncular area"
    acronym: Literal["DP"] = "DP"
    id: Literal["814"] = "814"


class _Pmd(_BrainStructureModel):
    """Model PMd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal premammillary nucleus"] = "Dorsal premammillary nucleus"
    acronym: Literal["PMd"] = "PMd"
    id: Literal["980"] = "980"


class _Dtn(_BrainStructureModel):
    """Model DTN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal tegmental nucleus"] = "Dorsal tegmental nucleus"
    acronym: Literal["DTN"] = "DTN"
    id: Literal["880"] = "880"


class _Dt(_BrainStructureModel):
    """Model DT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsal terminal nucleus of the accessory optic tract"] = (
        "Dorsal terminal nucleus of the accessory optic tract"
    )
    acronym: Literal["DT"] = "DT"
    id: Literal["75"] = "75"


class _Dmh(_BrainStructureModel):
    """Model DMH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Dorsomedial nucleus of the hypothalamus"] = "Dorsomedial nucleus of the hypothalamus"
    acronym: Literal["DMH"] = "DMH"
    id: Literal["830"] = "830"


class _Ect(_BrainStructureModel):
    """Model ECT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ectorhinal area"] = "Ectorhinal area"
    acronym: Literal["ECT"] = "ECT"
    id: Literal["895"] = "895"


class _Ect1(_BrainStructureModel):
    """Model ECT1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ectorhinal area/Layer 1"] = "Ectorhinal area/Layer 1"
    acronym: Literal["ECT1"] = "ECT1"
    id: Literal["836"] = "836"


class _Ect2_3(_BrainStructureModel):
    """Model ECT2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ectorhinal area/Layer 2/3"] = "Ectorhinal area/Layer 2/3"
    acronym: Literal["ECT2/3"] = "ECT2/3"
    id: Literal["427"] = "427"


class _Ect5(_BrainStructureModel):
    """Model ECT5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ectorhinal area/Layer 5"] = "Ectorhinal area/Layer 5"
    acronym: Literal["ECT5"] = "ECT5"
    id: Literal["988"] = "988"


class _Ect6A(_BrainStructureModel):
    """Model ECT6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ectorhinal area/Layer 6a"] = "Ectorhinal area/Layer 6a"
    acronym: Literal["ECT6a"] = "ECT6a"
    id: Literal["977"] = "977"


class _Ect6B(_BrainStructureModel):
    """Model ECT6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ectorhinal area/Layer 6b"] = "Ectorhinal area/Layer 6b"
    acronym: Literal["ECT6b"] = "ECT6b"
    id: Literal["1045"] = "1045"


class _Ew(_BrainStructureModel):
    """Model EW"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Edinger-Westphal nucleus"] = "Edinger-Westphal nucleus"
    acronym: Literal["EW"] = "EW"
    id: Literal["975"] = "975"


class _Ep(_BrainStructureModel):
    """Model EP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Endopiriform nucleus"] = "Endopiriform nucleus"
    acronym: Literal["EP"] = "EP"
    id: Literal["942"] = "942"


class _Epd(_BrainStructureModel):
    """Model EPd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Endopiriform nucleus, dorsal part"] = "Endopiriform nucleus, dorsal part"
    acronym: Literal["EPd"] = "EPd"
    id: Literal["952"] = "952"


class _Epv(_BrainStructureModel):
    """Model EPv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Endopiriform nucleus, ventral part"] = "Endopiriform nucleus, ventral part"
    acronym: Literal["EPv"] = "EPv"
    id: Literal["966"] = "966"


class _Ent(_BrainStructureModel):
    """Model ENT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area"] = "Entorhinal area"
    acronym: Literal["ENT"] = "ENT"
    id: Literal["909"] = "909"


class _Entl(_BrainStructureModel):
    """Model ENTl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, lateral part"] = "Entorhinal area, lateral part"
    acronym: Literal["ENTl"] = "ENTl"
    id: Literal["918"] = "918"


class _Entl1(_BrainStructureModel):
    """Model ENTl1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, lateral part, layer 1"] = "Entorhinal area, lateral part, layer 1"
    acronym: Literal["ENTl1"] = "ENTl1"
    id: Literal["1121"] = "1121"


class _Entl2(_BrainStructureModel):
    """Model ENTl2"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, lateral part, layer 2"] = "Entorhinal area, lateral part, layer 2"
    acronym: Literal["ENTl2"] = "ENTl2"
    id: Literal["20"] = "20"


class _Entl3(_BrainStructureModel):
    """Model ENTl3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, lateral part, layer 3"] = "Entorhinal area, lateral part, layer 3"
    acronym: Literal["ENTl3"] = "ENTl3"
    id: Literal["52"] = "52"


class _Entl5(_BrainStructureModel):
    """Model ENTl5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, lateral part, layer 5"] = "Entorhinal area, lateral part, layer 5"
    acronym: Literal["ENTl5"] = "ENTl5"
    id: Literal["139"] = "139"


class _Entl6A(_BrainStructureModel):
    """Model ENTl6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, lateral part, layer 6a"] = "Entorhinal area, lateral part, layer 6a"
    acronym: Literal["ENTl6a"] = "ENTl6a"
    id: Literal["28"] = "28"


class _Entm(_BrainStructureModel):
    """Model ENTm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, medial part, dorsal zone"] = "Entorhinal area, medial part, dorsal zone"
    acronym: Literal["ENTm"] = "ENTm"
    id: Literal["926"] = "926"


class _Entm1(_BrainStructureModel):
    """Model ENTm1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, medial part, dorsal zone, layer 1"] = (
        "Entorhinal area, medial part, dorsal zone, layer 1"
    )
    acronym: Literal["ENTm1"] = "ENTm1"
    id: Literal["526"] = "526"


class _Entm2(_BrainStructureModel):
    """Model ENTm2"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, medial part, dorsal zone, layer 2"] = (
        "Entorhinal area, medial part, dorsal zone, layer 2"
    )
    acronym: Literal["ENTm2"] = "ENTm2"
    id: Literal["543"] = "543"


class _Entm3(_BrainStructureModel):
    """Model ENTm3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, medial part, dorsal zone, layer 3"] = (
        "Entorhinal area, medial part, dorsal zone, layer 3"
    )
    acronym: Literal["ENTm3"] = "ENTm3"
    id: Literal["664"] = "664"


class _Entm5(_BrainStructureModel):
    """Model ENTm5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, medial part, dorsal zone, layer 5"] = (
        "Entorhinal area, medial part, dorsal zone, layer 5"
    )
    acronym: Literal["ENTm5"] = "ENTm5"
    id: Literal["727"] = "727"


class _Entm6(_BrainStructureModel):
    """Model ENTm6"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Entorhinal area, medial part, dorsal zone, layer 6"] = (
        "Entorhinal area, medial part, dorsal zone, layer 6"
    )
    acronym: Literal["ENTm6"] = "ENTm6"
    id: Literal["743"] = "743"


class _Epi(_BrainStructureModel):
    """Model EPI"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Epithalamus"] = "Epithalamus"
    acronym: Literal["EPI"] = "EPI"
    id: Literal["958"] = "958"


class _Eth(_BrainStructureModel):
    """Model Eth"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ethmoid nucleus of the thalamus"] = "Ethmoid nucleus of the thalamus"
    acronym: Literal["Eth"] = "Eth"
    id: Literal["560581551"] = "560581551"


class _Ecu(_BrainStructureModel):
    """Model ECU"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["External cuneate nucleus"] = "External cuneate nucleus"
    acronym: Literal["ECU"] = "ECU"
    id: Literal["903"] = "903"


class _Vii(_BrainStructureModel):
    """Model VII"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Facial motor nucleus"] = "Facial motor nucleus"
    acronym: Literal["VII"] = "VII"
    id: Literal["661"] = "661"


class _Fc(_BrainStructureModel):
    """Model FC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Fasciola cinerea"] = "Fasciola cinerea"
    acronym: Literal["FC"] = "FC"
    id: Literal["982"] = "982"


class _Fn(_BrainStructureModel):
    """Model FN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Fastigial nucleus"] = "Fastigial nucleus"
    acronym: Literal["FN"] = "FN"
    id: Literal["989"] = "989"


class _Ca1(_BrainStructureModel):
    """Model CA1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Field CA1"] = "Field CA1"
    acronym: Literal["CA1"] = "CA1"
    id: Literal["382"] = "382"


class _Ca2(_BrainStructureModel):
    """Model CA2"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Field CA2"] = "Field CA2"
    acronym: Literal["CA2"] = "CA2"
    id: Literal["423"] = "423"


class _Ca3(_BrainStructureModel):
    """Model CA3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Field CA3"] = "Field CA3"
    acronym: Literal["CA3"] = "CA3"
    id: Literal["463"] = "463"


class _Ff(_BrainStructureModel):
    """Model FF"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Fields of Forel"] = "Fields of Forel"
    acronym: Literal["FF"] = "FF"
    id: Literal["804"] = "804"


class _Fl(_BrainStructureModel):
    """Model FL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Flocculus"] = "Flocculus"
    acronym: Literal["FL"] = "FL"
    id: Literal["1049"] = "1049"


class _Fotu(_BrainStructureModel):
    """Model FOTU"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Folium-tuber vermis (VII)"] = "Folium-tuber vermis (VII)"
    acronym: Literal["FOTU"] = "FOTU"
    id: Literal["944"] = "944"


class _Frp(_BrainStructureModel):
    """Model FRP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Frontal pole, cerebral cortex"] = "Frontal pole, cerebral cortex"
    acronym: Literal["FRP"] = "FRP"
    id: Literal["184"] = "184"


class _Frp1(_BrainStructureModel):
    """Model FRP1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Frontal pole, layer 1"] = "Frontal pole, layer 1"
    acronym: Literal["FRP1"] = "FRP1"
    id: Literal["68"] = "68"


class _Frp2_3(_BrainStructureModel):
    """Model FRP2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Frontal pole, layer 2/3"] = "Frontal pole, layer 2/3"
    acronym: Literal["FRP2/3"] = "FRP2/3"
    id: Literal["667"] = "667"


class _Frp5(_BrainStructureModel):
    """Model FRP5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Frontal pole, layer 5"] = "Frontal pole, layer 5"
    acronym: Literal["FRP5"] = "FRP5"
    id: Literal["526157192"] = "526157192"


class _Frp6A(_BrainStructureModel):
    """Model FRP6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Frontal pole, layer 6a"] = "Frontal pole, layer 6a"
    acronym: Literal["FRP6a"] = "FRP6a"
    id: Literal["526157196"] = "526157196"


class _Frp6B(_BrainStructureModel):
    """Model FRP6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Frontal pole, layer 6b"] = "Frontal pole, layer 6b"
    acronym: Literal["FRP6b"] = "FRP6b"
    id: Literal["526322264"] = "526322264"


class _Fs(_BrainStructureModel):
    """Model FS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Fundus of striatum"] = "Fundus of striatum"
    acronym: Literal["FS"] = "FS"
    id: Literal["998"] = "998"


class _Gend(_BrainStructureModel):
    """Model GENd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Geniculate group, dorsal thalamus"] = "Geniculate group, dorsal thalamus"
    acronym: Literal["GENd"] = "GENd"
    id: Literal["1008"] = "1008"


class _Genv(_BrainStructureModel):
    """Model GENv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Geniculate group, ventral thalamus"] = "Geniculate group, ventral thalamus"
    acronym: Literal["GENv"] = "GENv"
    id: Literal["1014"] = "1014"


class _Grn(_BrainStructureModel):
    """Model GRN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Gigantocellular reticular nucleus"] = "Gigantocellular reticular nucleus"
    acronym: Literal["GRN"] = "GRN"
    id: Literal["1048"] = "1048"


class _Gpe(_BrainStructureModel):
    """Model GPe"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Globus pallidus, external segment"] = "Globus pallidus, external segment"
    acronym: Literal["GPe"] = "GPe"
    id: Literal["1022"] = "1022"


class _Gpi(_BrainStructureModel):
    """Model GPi"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Globus pallidus, internal segment"] = "Globus pallidus, internal segment"
    acronym: Literal["GPi"] = "GPi"
    id: Literal["1031"] = "1031"


class _Gr(_BrainStructureModel):
    """Model GR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Gracile nucleus"] = "Gracile nucleus"
    acronym: Literal["GR"] = "GR"
    id: Literal["1039"] = "1039"


class _Gu(_BrainStructureModel):
    """Model GU"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Gustatory areas"] = "Gustatory areas"
    acronym: Literal["GU"] = "GU"
    id: Literal["1057"] = "1057"


class _Gu1(_BrainStructureModel):
    """Model GU1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Gustatory areas, layer 1"] = "Gustatory areas, layer 1"
    acronym: Literal["GU1"] = "GU1"
    id: Literal["36"] = "36"


class _Gu2_3(_BrainStructureModel):
    """Model GU2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Gustatory areas, layer 2/3"] = "Gustatory areas, layer 2/3"
    acronym: Literal["GU2/3"] = "GU2/3"
    id: Literal["180"] = "180"


class _Gu4(_BrainStructureModel):
    """Model GU4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Gustatory areas, layer 4"] = "Gustatory areas, layer 4"
    acronym: Literal["GU4"] = "GU4"
    id: Literal["148"] = "148"


class _Gu5(_BrainStructureModel):
    """Model GU5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Gustatory areas, layer 5"] = "Gustatory areas, layer 5"
    acronym: Literal["GU5"] = "GU5"
    id: Literal["187"] = "187"


class _Gu6A(_BrainStructureModel):
    """Model GU6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Gustatory areas, layer 6a"] = "Gustatory areas, layer 6a"
    acronym: Literal["GU6a"] = "GU6a"
    id: Literal["638"] = "638"


class _Gu6B(_BrainStructureModel):
    """Model GU6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Gustatory areas, layer 6b"] = "Gustatory areas, layer 6b"
    acronym: Literal["GU6b"] = "GU6b"
    id: Literal["662"] = "662"


class _Hem(_BrainStructureModel):
    """Model HEM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Hemispheric regions"] = "Hemispheric regions"
    acronym: Literal["HEM"] = "HEM"
    id: Literal["1073"] = "1073"


class _Hb(_BrainStructureModel):
    """Model HB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Hindbrain"] = "Hindbrain"
    acronym: Literal["HB"] = "HB"
    id: Literal["1065"] = "1065"


class _Hpf(_BrainStructureModel):
    """Model HPF"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Hippocampal formation"] = "Hippocampal formation"
    acronym: Literal["HPF"] = "HPF"
    id: Literal["1089"] = "1089"


class _Hip(_BrainStructureModel):
    """Model HIP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Hippocampal region"] = "Hippocampal region"
    acronym: Literal["HIP"] = "HIP"
    id: Literal["1080"] = "1080"


class _Hata(_BrainStructureModel):
    """Model HATA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Hippocampo-amygdalar transition area"] = "Hippocampo-amygdalar transition area"
    acronym: Literal["HATA"] = "HATA"
    id: Literal["589508447"] = "589508447"


class _Xii(_BrainStructureModel):
    """Model XII"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Hypoglossal nucleus"] = "Hypoglossal nucleus"
    acronym: Literal["XII"] = "XII"
    id: Literal["773"] = "773"


class _Lz(_BrainStructureModel):
    """Model LZ"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Hypothalamic lateral zone"] = "Hypothalamic lateral zone"
    acronym: Literal["LZ"] = "LZ"
    id: Literal["290"] = "290"


class _Mez(_BrainStructureModel):
    """Model MEZ"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Hypothalamic medial zone"] = "Hypothalamic medial zone"
    acronym: Literal["MEZ"] = "MEZ"
    id: Literal["467"] = "467"


class _Hy(_BrainStructureModel):
    """Model HY"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Hypothalamus"] = "Hypothalamus"
    acronym: Literal["HY"] = "HY"
    id: Literal["1097"] = "1097"


class _Ig(_BrainStructureModel):
    """Model IG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Induseum griseum"] = "Induseum griseum"
    acronym: Literal["IG"] = "IG"
    id: Literal["19"] = "19"


class _Ic(_BrainStructureModel):
    """Model IC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Inferior colliculus"] = "Inferior colliculus"
    acronym: Literal["IC"] = "IC"
    id: Literal["4"] = "4"


class _Icc(_BrainStructureModel):
    """Model ICc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Inferior colliculus, central nucleus"] = "Inferior colliculus, central nucleus"
    acronym: Literal["ICc"] = "ICc"
    id: Literal["811"] = "811"


class _Icd(_BrainStructureModel):
    """Model ICd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Inferior colliculus, dorsal nucleus"] = "Inferior colliculus, dorsal nucleus"
    acronym: Literal["ICd"] = "ICd"
    id: Literal["820"] = "820"


class _Ice(_BrainStructureModel):
    """Model ICe"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Inferior colliculus, external nucleus"] = "Inferior colliculus, external nucleus"
    acronym: Literal["ICe"] = "ICe"
    id: Literal["828"] = "828"


class _Io(_BrainStructureModel):
    """Model IO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Inferior olivary complex"] = "Inferior olivary complex"
    acronym: Literal["IO"] = "IO"
    id: Literal["83"] = "83"


class _Isn(_BrainStructureModel):
    """Model ISN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Inferior salivatory nucleus"] = "Inferior salivatory nucleus"
    acronym: Literal["ISN"] = "ISN"
    id: Literal["106"] = "106"


class _Icb(_BrainStructureModel):
    """Model ICB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Infracerebellar nucleus"] = "Infracerebellar nucleus"
    acronym: Literal["ICB"] = "ICB"
    id: Literal["372"] = "372"


class _Ila(_BrainStructureModel):
    """Model ILA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Infralimbic area"] = "Infralimbic area"
    acronym: Literal["ILA"] = "ILA"
    id: Literal["44"] = "44"


class _Ila1(_BrainStructureModel):
    """Model ILA1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Infralimbic area, layer 1"] = "Infralimbic area, layer 1"
    acronym: Literal["ILA1"] = "ILA1"
    id: Literal["707"] = "707"


class _Ila2_3(_BrainStructureModel):
    """Model ILA2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Infralimbic area, layer 2/3"] = "Infralimbic area, layer 2/3"
    acronym: Literal["ILA2/3"] = "ILA2/3"
    id: Literal["556"] = "556"


class _Ila5(_BrainStructureModel):
    """Model ILA5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Infralimbic area, layer 5"] = "Infralimbic area, layer 5"
    acronym: Literal["ILA5"] = "ILA5"
    id: Literal["827"] = "827"


class _Ila6A(_BrainStructureModel):
    """Model ILA6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Infralimbic area, layer 6a"] = "Infralimbic area, layer 6a"
    acronym: Literal["ILA6a"] = "ILA6a"
    id: Literal["1054"] = "1054"


class _Ila6B(_BrainStructureModel):
    """Model ILA6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Infralimbic area, layer 6b"] = "Infralimbic area, layer 6b"
    acronym: Literal["ILA6b"] = "ILA6b"
    id: Literal["1081"] = "1081"


class _Iad(_BrainStructureModel):
    """Model IAD"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interanterodorsal nucleus of the thalamus"] = "Interanterodorsal nucleus of the thalamus"
    acronym: Literal["IAD"] = "IAD"
    id: Literal["1113"] = "1113"


class _Iam(_BrainStructureModel):
    """Model IAM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interanteromedial nucleus of the thalamus"] = "Interanteromedial nucleus of the thalamus"
    acronym: Literal["IAM"] = "IAM"
    id: Literal["1120"] = "1120"


class _Ib(_BrainStructureModel):
    """Model IB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interbrain"] = "Interbrain"
    acronym: Literal["IB"] = "IB"
    id: Literal["1129"] = "1129"


class _Ia(_BrainStructureModel):
    """Model IA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Intercalated amygdalar nucleus"] = "Intercalated amygdalar nucleus"
    acronym: Literal["IA"] = "IA"
    id: Literal["1105"] = "1105"


class _If(_BrainStructureModel):
    """Model IF"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interfascicular nucleus raphe"] = "Interfascicular nucleus raphe"
    acronym: Literal["IF"] = "IF"
    id: Literal["12"] = "12"


class _Igl(_BrainStructureModel):
    """Model IGL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Intergeniculate leaflet of the lateral geniculate complex"] = (
        "Intergeniculate leaflet of the lateral geniculate complex"
    )
    acronym: Literal["IGL"] = "IGL"
    id: Literal["27"] = "27"


class _Intg(_BrainStructureModel):
    """Model IntG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Intermediate geniculate nucleus"] = "Intermediate geniculate nucleus"
    acronym: Literal["IntG"] = "IntG"
    id: Literal["563807439"] = "563807439"


class _Irn(_BrainStructureModel):
    """Model IRN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Intermediate reticular nucleus"] = "Intermediate reticular nucleus"
    acronym: Literal["IRN"] = "IRN"
    id: Literal["136"] = "136"


class _Imd(_BrainStructureModel):
    """Model IMD"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Intermediodorsal nucleus of the thalamus"] = "Intermediodorsal nucleus of the thalamus"
    acronym: Literal["IMD"] = "IMD"
    id: Literal["59"] = "59"


class _Ipn(_BrainStructureModel):
    """Model IPN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interpeduncular nucleus"] = "Interpeduncular nucleus"
    acronym: Literal["IPN"] = "IPN"
    id: Literal["100"] = "100"


class _Ipa(_BrainStructureModel):
    """Model IPA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interpeduncular nucleus, apical"] = "Interpeduncular nucleus, apical"
    acronym: Literal["IPA"] = "IPA"
    id: Literal["607344842"] = "607344842"


class _Ipc(_BrainStructureModel):
    """Model IPC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interpeduncular nucleus, caudal"] = "Interpeduncular nucleus, caudal"
    acronym: Literal["IPC"] = "IPC"
    id: Literal["607344838"] = "607344838"


class _Ipdl(_BrainStructureModel):
    """Model IPDL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interpeduncular nucleus, dorsolateral"] = "Interpeduncular nucleus, dorsolateral"
    acronym: Literal["IPDL"] = "IPDL"
    id: Literal["607344858"] = "607344858"


class _Ipdm(_BrainStructureModel):
    """Model IPDM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interpeduncular nucleus, dorsomedial"] = "Interpeduncular nucleus, dorsomedial"
    acronym: Literal["IPDM"] = "IPDM"
    id: Literal["607344854"] = "607344854"


class _Ipi(_BrainStructureModel):
    """Model IPI"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interpeduncular nucleus, intermediate"] = "Interpeduncular nucleus, intermediate"
    acronym: Literal["IPI"] = "IPI"
    id: Literal["607344850"] = "607344850"


class _Ipl(_BrainStructureModel):
    """Model IPL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interpeduncular nucleus, lateral"] = "Interpeduncular nucleus, lateral"
    acronym: Literal["IPL"] = "IPL"
    id: Literal["607344846"] = "607344846"


class _Ipr(_BrainStructureModel):
    """Model IPR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interpeduncular nucleus, rostral"] = "Interpeduncular nucleus, rostral"
    acronym: Literal["IPR"] = "IPR"
    id: Literal["607344834"] = "607344834"


class _Iprl(_BrainStructureModel):
    """Model IPRL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interpeduncular nucleus, rostrolateral"] = "Interpeduncular nucleus, rostrolateral"
    acronym: Literal["IPRL"] = "IPRL"
    id: Literal["607344862"] = "607344862"


class _Ip(_BrainStructureModel):
    """Model IP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interposed nucleus"] = "Interposed nucleus"
    acronym: Literal["IP"] = "IP"
    id: Literal["91"] = "91"


class _Inc(_BrainStructureModel):
    """Model INC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Interstitial nucleus of Cajal"] = "Interstitial nucleus of Cajal"
    acronym: Literal["INC"] = "INC"
    id: Literal["67"] = "67"


class _I5(_BrainStructureModel):
    """Model I5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Intertrigeminal nucleus"] = "Intertrigeminal nucleus"
    acronym: Literal["I5"] = "I5"
    id: Literal["549009227"] = "549009227"


class _Ilm(_BrainStructureModel):
    """Model ILM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Intralaminar nuclei of the dorsal thalamus"] = "Intralaminar nuclei of the dorsal thalamus"
    acronym: Literal["ILM"] = "ILM"
    id: Literal["51"] = "51"


class _Isocortex(_BrainStructureModel):
    """Model Isocortex"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Isocortex"] = "Isocortex"
    acronym: Literal["Isocortex"] = "Isocortex"
    id: Literal["315"] = "315"


class _Kf(_BrainStructureModel):
    """Model KF"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Koelliker-Fuse subnucleus"] = "Koelliker-Fuse subnucleus"
    acronym: Literal["KF"] = "KF"
    id: Literal["123"] = "123"


class _La(_BrainStructureModel):
    """Model LA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral amygdalar nucleus"] = "Lateral amygdalar nucleus"
    acronym: Literal["LA"] = "LA"
    id: Literal["131"] = "131"


class _Ld(_BrainStructureModel):
    """Model LD"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral dorsal nucleus of thalamus"] = "Lateral dorsal nucleus of thalamus"
    acronym: Literal["LD"] = "LD"
    id: Literal["155"] = "155"


class _Lat(_BrainStructureModel):
    """Model LAT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral group of the dorsal thalamus"] = "Lateral group of the dorsal thalamus"
    acronym: Literal["LAT"] = "LAT"
    id: Literal["138"] = "138"


class _Lh(_BrainStructureModel):
    """Model LH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral habenula"] = "Lateral habenula"
    acronym: Literal["LH"] = "LH"
    id: Literal["186"] = "186"


class _Lha(_BrainStructureModel):
    """Model LHA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral hypothalamic area"] = "Lateral hypothalamic area"
    acronym: Literal["LHA"] = "LHA"
    id: Literal["194"] = "194"


class _Lm(_BrainStructureModel):
    """Model LM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral mammillary nucleus"] = "Lateral mammillary nucleus"
    acronym: Literal["LM"] = "LM"
    id: Literal["210"] = "210"


class _Lp(_BrainStructureModel):
    """Model LP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral posterior nucleus of the thalamus"] = "Lateral posterior nucleus of the thalamus"
    acronym: Literal["LP"] = "LP"
    id: Literal["218"] = "218"


class _Lpo(_BrainStructureModel):
    """Model LPO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral preoptic area"] = "Lateral preoptic area"
    acronym: Literal["LPO"] = "LPO"
    id: Literal["226"] = "226"


class _Lrn(_BrainStructureModel):
    """Model LRN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral reticular nucleus"] = "Lateral reticular nucleus"
    acronym: Literal["LRN"] = "LRN"
    id: Literal["235"] = "235"


class _Lrnm(_BrainStructureModel):
    """Model LRNm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral reticular nucleus, magnocellular part"] = "Lateral reticular nucleus, magnocellular part"
    acronym: Literal["LRNm"] = "LRNm"
    id: Literal["955"] = "955"


class _Lrnp(_BrainStructureModel):
    """Model LRNp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral reticular nucleus, parvicellular part"] = "Lateral reticular nucleus, parvicellular part"
    acronym: Literal["LRNp"] = "LRNp"
    id: Literal["963"] = "963"


class _Lsx(_BrainStructureModel):
    """Model LSX"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral septal complex"] = "Lateral septal complex"
    acronym: Literal["LSX"] = "LSX"
    id: Literal["275"] = "275"


class _Ls(_BrainStructureModel):
    """Model LS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral septal nucleus"] = "Lateral septal nucleus"
    acronym: Literal["LS"] = "LS"
    id: Literal["242"] = "242"


class _Lsc(_BrainStructureModel):
    """Model LSc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral septal nucleus, caudal (caudodorsal) part"] = (
        "Lateral septal nucleus, caudal (caudodorsal) part"
    )
    acronym: Literal["LSc"] = "LSc"
    id: Literal["250"] = "250"


class _Lsr(_BrainStructureModel):
    """Model LSr"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral septal nucleus, rostral (rostroventral) part"] = (
        "Lateral septal nucleus, rostral (rostroventral) part"
    )
    acronym: Literal["LSr"] = "LSr"
    id: Literal["258"] = "258"


class _Lsv(_BrainStructureModel):
    """Model LSv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral septal nucleus, ventral part"] = "Lateral septal nucleus, ventral part"
    acronym: Literal["LSv"] = "LSv"
    id: Literal["266"] = "266"


class _Lt(_BrainStructureModel):
    """Model LT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral terminal nucleus of the accessory optic tract"] = (
        "Lateral terminal nucleus of the accessory optic tract"
    )
    acronym: Literal["LT"] = "LT"
    id: Literal["66"] = "66"


class _Lav(_BrainStructureModel):
    """Model LAV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral vestibular nucleus"] = "Lateral vestibular nucleus"
    acronym: Literal["LAV"] = "LAV"
    id: Literal["209"] = "209"


class _Visl(_BrainStructureModel):
    """Model VISl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral visual area"] = "Lateral visual area"
    acronym: Literal["VISl"] = "VISl"
    id: Literal["409"] = "409"


class _Visl1(_BrainStructureModel):
    """Model VISl1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral visual area, layer 1"] = "Lateral visual area, layer 1"
    acronym: Literal["VISl1"] = "VISl1"
    id: Literal["421"] = "421"


class _Visl2_3(_BrainStructureModel):
    """Model VISl2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral visual area, layer 2/3"] = "Lateral visual area, layer 2/3"
    acronym: Literal["VISl2/3"] = "VISl2/3"
    id: Literal["973"] = "973"


class _Visl4(_BrainStructureModel):
    """Model VISl4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral visual area, layer 4"] = "Lateral visual area, layer 4"
    acronym: Literal["VISl4"] = "VISl4"
    id: Literal["573"] = "573"


class _Visl5(_BrainStructureModel):
    """Model VISl5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral visual area, layer 5"] = "Lateral visual area, layer 5"
    acronym: Literal["VISl5"] = "VISl5"
    id: Literal["613"] = "613"


class _Visl6A(_BrainStructureModel):
    """Model VISl6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral visual area, layer 6a"] = "Lateral visual area, layer 6a"
    acronym: Literal["VISl6a"] = "VISl6a"
    id: Literal["74"] = "74"


class _Visl6B(_BrainStructureModel):
    """Model VISl6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lateral visual area, layer 6b"] = "Lateral visual area, layer 6b"
    acronym: Literal["VISl6b"] = "VISl6b"
    id: Literal["121"] = "121"


class _Ldt(_BrainStructureModel):
    """Model LDT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Laterodorsal tegmental nucleus"] = "Laterodorsal tegmental nucleus"
    acronym: Literal["LDT"] = "LDT"
    id: Literal["162"] = "162"


class _Visli(_BrainStructureModel):
    """Model VISli"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Laterointermediate area"] = "Laterointermediate area"
    acronym: Literal["VISli"] = "VISli"
    id: Literal["312782574"] = "312782574"


class _Visli1(_BrainStructureModel):
    """Model VISli1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Laterointermediate area, layer 1"] = "Laterointermediate area, layer 1"
    acronym: Literal["VISli1"] = "VISli1"
    id: Literal["312782578"] = "312782578"


class _Visli2_3(_BrainStructureModel):
    """Model VISli2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Laterointermediate area, layer 2/3"] = "Laterointermediate area, layer 2/3"
    acronym: Literal["VISli2/3"] = "VISli2/3"
    id: Literal["312782582"] = "312782582"


class _Visli4(_BrainStructureModel):
    """Model VISli4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Laterointermediate area, layer 4"] = "Laterointermediate area, layer 4"
    acronym: Literal["VISli4"] = "VISli4"
    id: Literal["312782586"] = "312782586"


class _Visli5(_BrainStructureModel):
    """Model VISli5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Laterointermediate area, layer 5"] = "Laterointermediate area, layer 5"
    acronym: Literal["VISli5"] = "VISli5"
    id: Literal["312782590"] = "312782590"


class _Visli6A(_BrainStructureModel):
    """Model VISli6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Laterointermediate area, layer 6a"] = "Laterointermediate area, layer 6a"
    acronym: Literal["VISli6a"] = "VISli6a"
    id: Literal["312782594"] = "312782594"


class _Visli6B(_BrainStructureModel):
    """Model VISli6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Laterointermediate area, layer 6b"] = "Laterointermediate area, layer 6b"
    acronym: Literal["VISli6b"] = "VISli6b"
    id: Literal["312782598"] = "312782598"


class _Lin(_BrainStructureModel):
    """Model LIN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Linear nucleus of the medulla"] = "Linear nucleus of the medulla"
    acronym: Literal["LIN"] = "LIN"
    id: Literal["203"] = "203"


class _Ling(_BrainStructureModel):
    """Model LING"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lingula (I)"] = "Lingula (I)"
    acronym: Literal["LING"] = "LING"
    id: Literal["912"] = "912"


class _Cent2(_BrainStructureModel):
    """Model CENT2"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lobule II"] = "Lobule II"
    acronym: Literal["CENT2"] = "CENT2"
    id: Literal["976"] = "976"


class _Cent3(_BrainStructureModel):
    """Model CENT3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lobule III"] = "Lobule III"
    acronym: Literal["CENT3"] = "CENT3"
    id: Literal["984"] = "984"


class _Cul4_5(_BrainStructureModel):
    """Model CUL4, 5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Lobules IV-V"] = "Lobules IV-V"
    acronym: Literal["CUL4, 5"] = "CUL4, 5"
    id: Literal["1091"] = "1091"


class _Lc(_BrainStructureModel):
    """Model LC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Locus ceruleus"] = "Locus ceruleus"
    acronym: Literal["LC"] = "LC"
    id: Literal["147"] = "147"


class _Ma(_BrainStructureModel):
    """Model MA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Magnocellular nucleus"] = "Magnocellular nucleus"
    acronym: Literal["MA"] = "MA"
    id: Literal["298"] = "298"


class _Marn(_BrainStructureModel):
    """Model MARN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Magnocellular reticular nucleus"] = "Magnocellular reticular nucleus"
    acronym: Literal["MARN"] = "MARN"
    id: Literal["307"] = "307"


class _Mob(_BrainStructureModel):
    """Model MOB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Main olfactory bulb"] = "Main olfactory bulb"
    acronym: Literal["MOB"] = "MOB"
    id: Literal["507"] = "507"


class _Mbo(_BrainStructureModel):
    """Model MBO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Mammillary body"] = "Mammillary body"
    acronym: Literal["MBO"] = "MBO"
    id: Literal["331"] = "331"


class _Ma3(_BrainStructureModel):
    """Model MA3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial accesory oculomotor nucleus"] = "Medial accesory oculomotor nucleus"
    acronym: Literal["MA3"] = "MA3"
    id: Literal["549009211"] = "549009211"


class _Mea(_BrainStructureModel):
    """Model MEA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial amygdalar nucleus"] = "Medial amygdalar nucleus"
    acronym: Literal["MEA"] = "MEA"
    id: Literal["403"] = "403"


class _Mg(_BrainStructureModel):
    """Model MG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial geniculate complex"] = "Medial geniculate complex"
    acronym: Literal["MG"] = "MG"
    id: Literal["475"] = "475"


class _Mgd(_BrainStructureModel):
    """Model MGd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial geniculate complex, dorsal part"] = "Medial geniculate complex, dorsal part"
    acronym: Literal["MGd"] = "MGd"
    id: Literal["1072"] = "1072"


class _Mgm(_BrainStructureModel):
    """Model MGm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial geniculate complex, medial part"] = "Medial geniculate complex, medial part"
    acronym: Literal["MGm"] = "MGm"
    id: Literal["1088"] = "1088"


class _Mgv(_BrainStructureModel):
    """Model MGv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial geniculate complex, ventral part"] = "Medial geniculate complex, ventral part"
    acronym: Literal["MGv"] = "MGv"
    id: Literal["1079"] = "1079"


class _Med(_BrainStructureModel):
    """Model MED"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial group of the dorsal thalamus"] = "Medial group of the dorsal thalamus"
    acronym: Literal["MED"] = "MED"
    id: Literal["444"] = "444"


class _Mh(_BrainStructureModel):
    """Model MH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial habenula"] = "Medial habenula"
    acronym: Literal["MH"] = "MH"
    id: Literal["483"] = "483"


class _Mm(_BrainStructureModel):
    """Model MM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial mammillary nucleus"] = "Medial mammillary nucleus"
    acronym: Literal["MM"] = "MM"
    id: Literal["491"] = "491"


class _Mmd(_BrainStructureModel):
    """Model MMd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial mammillary nucleus, dorsal part"] = "Medial mammillary nucleus, dorsal part"
    acronym: Literal["MMd"] = "MMd"
    id: Literal["606826659"] = "606826659"


class _Mml(_BrainStructureModel):
    """Model MMl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial mammillary nucleus, lateral part"] = "Medial mammillary nucleus, lateral part"
    acronym: Literal["MMl"] = "MMl"
    id: Literal["606826647"] = "606826647"


class _Mmm(_BrainStructureModel):
    """Model MMm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial mammillary nucleus, medial part"] = "Medial mammillary nucleus, medial part"
    acronym: Literal["MMm"] = "MMm"
    id: Literal["606826651"] = "606826651"


class _Mmme(_BrainStructureModel):
    """Model MMme"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial mammillary nucleus, median part"] = "Medial mammillary nucleus, median part"
    acronym: Literal["MMme"] = "MMme"
    id: Literal["732"] = "732"


class _Mmp(_BrainStructureModel):
    """Model MMp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial mammillary nucleus, posterior part"] = "Medial mammillary nucleus, posterior part"
    acronym: Literal["MMp"] = "MMp"
    id: Literal["606826655"] = "606826655"


class _Mpo(_BrainStructureModel):
    """Model MPO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial preoptic area"] = "Medial preoptic area"
    acronym: Literal["MPO"] = "MPO"
    id: Literal["523"] = "523"


class _Mpn(_BrainStructureModel):
    """Model MPN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial preoptic nucleus"] = "Medial preoptic nucleus"
    acronym: Literal["MPN"] = "MPN"
    id: Literal["515"] = "515"


class _Mpt(_BrainStructureModel):
    """Model MPT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial pretectal area"] = "Medial pretectal area"
    acronym: Literal["MPT"] = "MPT"
    id: Literal["531"] = "531"


class _Msc(_BrainStructureModel):
    """Model MSC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial septal complex"] = "Medial septal complex"
    acronym: Literal["MSC"] = "MSC"
    id: Literal["904"] = "904"


class _Ms(_BrainStructureModel):
    """Model MS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial septal nucleus"] = "Medial septal nucleus"
    acronym: Literal["MS"] = "MS"
    id: Literal["564"] = "564"


class _Mt(_BrainStructureModel):
    """Model MT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial terminal nucleus of the accessory optic tract"] = (
        "Medial terminal nucleus of the accessory optic tract"
    )
    acronym: Literal["MT"] = "MT"
    id: Literal["58"] = "58"


class _Mv(_BrainStructureModel):
    """Model MV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medial vestibular nucleus"] = "Medial vestibular nucleus"
    acronym: Literal["MV"] = "MV"
    id: Literal["202"] = "202"


class _Me(_BrainStructureModel):
    """Model ME"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Median eminence"] = "Median eminence"
    acronym: Literal["ME"] = "ME"
    id: Literal["10671"] = "10671"


class _Mepo(_BrainStructureModel):
    """Model MEPO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Median preoptic nucleus"] = "Median preoptic nucleus"
    acronym: Literal["MEPO"] = "MEPO"
    id: Literal["452"] = "452"


class _Md(_BrainStructureModel):
    """Model MD"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Mediodorsal nucleus of thalamus"] = "Mediodorsal nucleus of thalamus"
    acronym: Literal["MD"] = "MD"
    id: Literal["362"] = "362"


class _My(_BrainStructureModel):
    """Model MY"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medulla"] = "Medulla"
    acronym: Literal["MY"] = "MY"
    id: Literal["354"] = "354"


class _My_Sat(_BrainStructureModel):
    """Model MY-sat"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medulla, behavioral state related"] = "Medulla, behavioral state related"
    acronym: Literal["MY-sat"] = "MY-sat"
    id: Literal["379"] = "379"


class _My_Mot(_BrainStructureModel):
    """Model MY-mot"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medulla, motor related"] = "Medulla, motor related"
    acronym: Literal["MY-mot"] = "MY-mot"
    id: Literal["370"] = "370"


class _My_Sen(_BrainStructureModel):
    """Model MY-sen"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medulla, sensory related"] = "Medulla, sensory related"
    acronym: Literal["MY-sen"] = "MY-sen"
    id: Literal["386"] = "386"


class _Mdrn(_BrainStructureModel):
    """Model MDRN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medullary reticular nucleus"] = "Medullary reticular nucleus"
    acronym: Literal["MDRN"] = "MDRN"
    id: Literal["395"] = "395"


class _Mdrnd(_BrainStructureModel):
    """Model MDRNd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medullary reticular nucleus, dorsal part"] = "Medullary reticular nucleus, dorsal part"
    acronym: Literal["MDRNd"] = "MDRNd"
    id: Literal["1098"] = "1098"


class _Mdrnv(_BrainStructureModel):
    """Model MDRNv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Medullary reticular nucleus, ventral part"] = "Medullary reticular nucleus, ventral part"
    acronym: Literal["MDRNv"] = "MDRNv"
    id: Literal["1107"] = "1107"


class _Mb(_BrainStructureModel):
    """Model MB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Midbrain"] = "Midbrain"
    acronym: Literal["MB"] = "MB"
    id: Literal["313"] = "313"


class _Ramb(_BrainStructureModel):
    """Model RAmb"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Midbrain raphe nuclei"] = "Midbrain raphe nuclei"
    acronym: Literal["RAmb"] = "RAmb"
    id: Literal["165"] = "165"


class _Mrn(_BrainStructureModel):
    """Model MRN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Midbrain reticular nucleus"] = "Midbrain reticular nucleus"
    acronym: Literal["MRN"] = "MRN"
    id: Literal["128"] = "128"


class _Rr(_BrainStructureModel):
    """Model RR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Midbrain reticular nucleus, retrorubral area"] = "Midbrain reticular nucleus, retrorubral area"
    acronym: Literal["RR"] = "RR"
    id: Literal["246"] = "246"


class _Mev(_BrainStructureModel):
    """Model MEV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Midbrain trigeminal nucleus"] = "Midbrain trigeminal nucleus"
    acronym: Literal["MEV"] = "MEV"
    id: Literal["460"] = "460"


class _Mbsta(_BrainStructureModel):
    """Model MBsta"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Midbrain, behavioral state related"] = "Midbrain, behavioral state related"
    acronym: Literal["MBsta"] = "MBsta"
    id: Literal["348"] = "348"


class _Mbmot(_BrainStructureModel):
    """Model MBmot"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Midbrain, motor related"] = "Midbrain, motor related"
    acronym: Literal["MBmot"] = "MBmot"
    id: Literal["323"] = "323"


class _Mbsen(_BrainStructureModel):
    """Model MBsen"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Midbrain, sensory related"] = "Midbrain, sensory related"
    acronym: Literal["MBsen"] = "MBsen"
    id: Literal["339"] = "339"


class _Mtn(_BrainStructureModel):
    """Model MTN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Midline group of the dorsal thalamus"] = "Midline group of the dorsal thalamus"
    acronym: Literal["MTN"] = "MTN"
    id: Literal["571"] = "571"


class _V(_BrainStructureModel):
    """Model V"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Motor nucleus of trigeminal"] = "Motor nucleus of trigeminal"
    acronym: Literal["V"] = "V"
    id: Literal["621"] = "621"


class _Nod(_BrainStructureModel):
    """Model NOD"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nodulus (X)"] = "Nodulus (X)"
    acronym: Literal["NOD"] = "NOD"
    id: Literal["968"] = "968"


class _Acb(_BrainStructureModel):
    """Model ACB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus accumbens"] = "Nucleus accumbens"
    acronym: Literal["ACB"] = "ACB"
    id: Literal["56"] = "56"


class _Amb(_BrainStructureModel):
    """Model AMB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus ambiguus"] = "Nucleus ambiguus"
    acronym: Literal["AMB"] = "AMB"
    id: Literal["135"] = "135"


class _Ambd(_BrainStructureModel):
    """Model AMBd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus ambiguus, dorsal division"] = "Nucleus ambiguus, dorsal division"
    acronym: Literal["AMBd"] = "AMBd"
    id: Literal["939"] = "939"


class _Ambv(_BrainStructureModel):
    """Model AMBv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus ambiguus, ventral division"] = "Nucleus ambiguus, ventral division"
    acronym: Literal["AMBv"] = "AMBv"
    id: Literal["143"] = "143"


class _Ni(_BrainStructureModel):
    """Model NI"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus incertus"] = "Nucleus incertus"
    acronym: Literal["NI"] = "NI"
    id: Literal["604"] = "604"


class _Nd(_BrainStructureModel):
    """Model ND"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of Darkschewitsch"] = "Nucleus of Darkschewitsch"
    acronym: Literal["ND"] = "ND"
    id: Literal["587"] = "587"


class _Nr(_BrainStructureModel):
    """Model NR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of Roller"] = "Nucleus of Roller"
    acronym: Literal["NR"] = "NR"
    id: Literal["177"] = "177"


class _Re(_BrainStructureModel):
    """Model RE"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of reuniens"] = "Nucleus of reuniens"
    acronym: Literal["RE"] = "RE"
    id: Literal["181"] = "181"


class _Nb(_BrainStructureModel):
    """Model NB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of the brachium of the inferior colliculus"] = (
        "Nucleus of the brachium of the inferior colliculus"
    )
    acronym: Literal["NB"] = "NB"
    id: Literal["580"] = "580"


class _Nll(_BrainStructureModel):
    """Model NLL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of the lateral lemniscus"] = "Nucleus of the lateral lemniscus"
    acronym: Literal["NLL"] = "NLL"
    id: Literal["612"] = "612"


class _Nlot(_BrainStructureModel):
    """Model NLOT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of the lateral olfactory tract"] = "Nucleus of the lateral olfactory tract"
    acronym: Literal["NLOT"] = "NLOT"
    id: Literal["619"] = "619"


class _Nlot3(_BrainStructureModel):
    """Model NLOT3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of the lateral olfactory tract, layer 3"] = "Nucleus of the lateral olfactory tract, layer 3"
    acronym: Literal["NLOT3"] = "NLOT3"
    id: Literal["1139"] = "1139"


class _Nlot1(_BrainStructureModel):
    """Model NLOT1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of the lateral olfactory tract, molecular layer"] = (
        "Nucleus of the lateral olfactory tract, molecular layer"
    )
    acronym: Literal["NLOT1"] = "NLOT1"
    id: Literal["260"] = "260"


class _Nlot2(_BrainStructureModel):
    """Model NLOT2"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of the lateral olfactory tract, pyramidal layer"] = (
        "Nucleus of the lateral olfactory tract, pyramidal layer"
    )
    acronym: Literal["NLOT2"] = "NLOT2"
    id: Literal["268"] = "268"


class _Not(_BrainStructureModel):
    """Model NOT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of the optic tract"] = "Nucleus of the optic tract"
    acronym: Literal["NOT"] = "NOT"
    id: Literal["628"] = "628"


class _Npc(_BrainStructureModel):
    """Model NPC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of the posterior commissure"] = "Nucleus of the posterior commissure"
    acronym: Literal["NPC"] = "NPC"
    id: Literal["634"] = "634"


class _Nts(_BrainStructureModel):
    """Model NTS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of the solitary tract"] = "Nucleus of the solitary tract"
    acronym: Literal["NTS"] = "NTS"
    id: Literal["651"] = "651"


class _Ntb(_BrainStructureModel):
    """Model NTB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus of the trapezoid body"] = "Nucleus of the trapezoid body"
    acronym: Literal["NTB"] = "NTB"
    id: Literal["642"] = "642"


class _Prp(_BrainStructureModel):
    """Model PRP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus prepositus"] = "Nucleus prepositus"
    acronym: Literal["PRP"] = "PRP"
    id: Literal["169"] = "169"


class _Rm(_BrainStructureModel):
    """Model RM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus raphe magnus"] = "Nucleus raphe magnus"
    acronym: Literal["RM"] = "RM"
    id: Literal["206"] = "206"


class _Ro(_BrainStructureModel):
    """Model RO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus raphe obscurus"] = "Nucleus raphe obscurus"
    acronym: Literal["RO"] = "RO"
    id: Literal["222"] = "222"


class _Rpa(_BrainStructureModel):
    """Model RPA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus raphe pallidus"] = "Nucleus raphe pallidus"
    acronym: Literal["RPA"] = "RPA"
    id: Literal["230"] = "230"


class _Rpo(_BrainStructureModel):
    """Model RPO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus raphe pontis"] = "Nucleus raphe pontis"
    acronym: Literal["RPO"] = "RPO"
    id: Literal["238"] = "238"


class _Sag(_BrainStructureModel):
    """Model SAG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus sagulum"] = "Nucleus sagulum"
    acronym: Literal["SAG"] = "SAG"
    id: Literal["271"] = "271"


class _X(_BrainStructureModel):
    """Model x"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus x"] = "Nucleus x"
    acronym: Literal["x"] = "x"
    id: Literal["765"] = "765"


class _Y(_BrainStructureModel):
    """Model y"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Nucleus y"] = "Nucleus y"
    acronym: Literal["y"] = "y"
    id: Literal["781"] = "781"


class _Iii(_BrainStructureModel):
    """Model III"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Oculomotor nucleus"] = "Oculomotor nucleus"
    acronym: Literal["III"] = "III"
    id: Literal["35"] = "35"


class _Olf(_BrainStructureModel):
    """Model OLF"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Olfactory areas"] = "Olfactory areas"
    acronym: Literal["OLF"] = "OLF"
    id: Literal["698"] = "698"


class _Ot(_BrainStructureModel):
    """Model OT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Olfactory tubercle"] = "Olfactory tubercle"
    acronym: Literal["OT"] = "OT"
    id: Literal["754"] = "754"


class _Op(_BrainStructureModel):
    """Model OP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Olivary pretectal nucleus"] = "Olivary pretectal nucleus"
    acronym: Literal["OP"] = "OP"
    id: Literal["706"] = "706"


class _Orb(_BrainStructureModel):
    """Model ORB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area"] = "Orbital area"
    acronym: Literal["ORB"] = "ORB"
    id: Literal["714"] = "714"


class _Orbl(_BrainStructureModel):
    """Model ORBl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, lateral part"] = "Orbital area, lateral part"
    acronym: Literal["ORBl"] = "ORBl"
    id: Literal["723"] = "723"


class _Orbl1(_BrainStructureModel):
    """Model ORBl1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, lateral part, layer 1"] = "Orbital area, lateral part, layer 1"
    acronym: Literal["ORBl1"] = "ORBl1"
    id: Literal["448"] = "448"


class _Orbl2_3(_BrainStructureModel):
    """Model ORBl2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, lateral part, layer 2/3"] = "Orbital area, lateral part, layer 2/3"
    acronym: Literal["ORBl2/3"] = "ORBl2/3"
    id: Literal["412"] = "412"


class _Orbl5(_BrainStructureModel):
    """Model ORBl5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, lateral part, layer 5"] = "Orbital area, lateral part, layer 5"
    acronym: Literal["ORBl5"] = "ORBl5"
    id: Literal["630"] = "630"


class _Orbl6A(_BrainStructureModel):
    """Model ORBl6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, lateral part, layer 6a"] = "Orbital area, lateral part, layer 6a"
    acronym: Literal["ORBl6a"] = "ORBl6a"
    id: Literal["440"] = "440"


class _Orbl6B(_BrainStructureModel):
    """Model ORBl6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, lateral part, layer 6b"] = "Orbital area, lateral part, layer 6b"
    acronym: Literal["ORBl6b"] = "ORBl6b"
    id: Literal["488"] = "488"


class _Orbm(_BrainStructureModel):
    """Model ORBm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, medial part"] = "Orbital area, medial part"
    acronym: Literal["ORBm"] = "ORBm"
    id: Literal["731"] = "731"


class _Orbm1(_BrainStructureModel):
    """Model ORBm1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, medial part, layer 1"] = "Orbital area, medial part, layer 1"
    acronym: Literal["ORBm1"] = "ORBm1"
    id: Literal["484"] = "484"


class _Orbm2_3(_BrainStructureModel):
    """Model ORBm2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, medial part, layer 2/3"] = "Orbital area, medial part, layer 2/3"
    acronym: Literal["ORBm2/3"] = "ORBm2/3"
    id: Literal["582"] = "582"


class _Orbm5(_BrainStructureModel):
    """Model ORBm5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, medial part, layer 5"] = "Orbital area, medial part, layer 5"
    acronym: Literal["ORBm5"] = "ORBm5"
    id: Literal["620"] = "620"


class _Orbm6A(_BrainStructureModel):
    """Model ORBm6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, medial part, layer 6a"] = "Orbital area, medial part, layer 6a"
    acronym: Literal["ORBm6a"] = "ORBm6a"
    id: Literal["910"] = "910"


class _Orbm6B(_BrainStructureModel):
    """Model ORBm6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, medial part, layer 6b"] = "Orbital area, medial part, layer 6b"
    acronym: Literal["ORBm6b"] = "ORBm6b"
    id: Literal["527696977"] = "527696977"


class _Orbvl(_BrainStructureModel):
    """Model ORBvl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, ventrolateral part"] = "Orbital area, ventrolateral part"
    acronym: Literal["ORBvl"] = "ORBvl"
    id: Literal["746"] = "746"


class _Orbvl1(_BrainStructureModel):
    """Model ORBvl1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, ventrolateral part, layer 1"] = "Orbital area, ventrolateral part, layer 1"
    acronym: Literal["ORBvl1"] = "ORBvl1"
    id: Literal["969"] = "969"


class _Orbvl2_3(_BrainStructureModel):
    """Model ORBvl2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, ventrolateral part, layer 2/3"] = "Orbital area, ventrolateral part, layer 2/3"
    acronym: Literal["ORBvl2/3"] = "ORBvl2/3"
    id: Literal["288"] = "288"


class _Orbvl5(_BrainStructureModel):
    """Model ORBvl5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, ventrolateral part, layer 5"] = "Orbital area, ventrolateral part, layer 5"
    acronym: Literal["ORBvl5"] = "ORBvl5"
    id: Literal["1125"] = "1125"


class _Orbvl6A(_BrainStructureModel):
    """Model ORBvl6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, ventrolateral part, layer 6a"] = "Orbital area, ventrolateral part, layer 6a"
    acronym: Literal["ORBvl6a"] = "ORBvl6a"
    id: Literal["608"] = "608"


class _Orbvl6B(_BrainStructureModel):
    """Model ORBvl6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Orbital area, ventrolateral part, layer 6b"] = "Orbital area, ventrolateral part, layer 6b"
    acronym: Literal["ORBvl6b"] = "ORBvl6b"
    id: Literal["680"] = "680"


class _Pal(_BrainStructureModel):
    """Model PAL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pallidum"] = "Pallidum"
    acronym: Literal["PAL"] = "PAL"
    id: Literal["803"] = "803"


class _Palc(_BrainStructureModel):
    """Model PALc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pallidum, caudal region"] = "Pallidum, caudal region"
    acronym: Literal["PALc"] = "PALc"
    id: Literal["809"] = "809"


class _Pald(_BrainStructureModel):
    """Model PALd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pallidum, dorsal region"] = "Pallidum, dorsal region"
    acronym: Literal["PALd"] = "PALd"
    id: Literal["818"] = "818"


class _Palm(_BrainStructureModel):
    """Model PALm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pallidum, medial region"] = "Pallidum, medial region"
    acronym: Literal["PALm"] = "PALm"
    id: Literal["826"] = "826"


class _Palv(_BrainStructureModel):
    """Model PALv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pallidum, ventral region"] = "Pallidum, ventral region"
    acronym: Literal["PALv"] = "PALv"
    id: Literal["835"] = "835"


class _Pbg(_BrainStructureModel):
    """Model PBG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parabigeminal nucleus"] = "Parabigeminal nucleus"
    acronym: Literal["PBG"] = "PBG"
    id: Literal["874"] = "874"


class _Pb(_BrainStructureModel):
    """Model PB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parabrachial nucleus"] = "Parabrachial nucleus"
    acronym: Literal["PB"] = "PB"
    id: Literal["867"] = "867"


class _Pcn(_BrainStructureModel):
    """Model PCN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paracentral nucleus"] = "Paracentral nucleus"
    acronym: Literal["PCN"] = "PCN"
    id: Literal["907"] = "907"


class _Pf(_BrainStructureModel):
    """Model PF"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parafascicular nucleus"] = "Parafascicular nucleus"
    acronym: Literal["PF"] = "PF"
    id: Literal["930"] = "930"


class _Pfl(_BrainStructureModel):
    """Model PFL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paraflocculus"] = "Paraflocculus"
    acronym: Literal["PFL"] = "PFL"
    id: Literal["1041"] = "1041"


class _Pgrn(_BrainStructureModel):
    """Model PGRN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paragigantocellular reticular nucleus"] = "Paragigantocellular reticular nucleus"
    acronym: Literal["PGRN"] = "PGRN"
    id: Literal["938"] = "938"


class _Pgrnd(_BrainStructureModel):
    """Model PGRNd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paragigantocellular reticular nucleus, dorsal part"] = (
        "Paragigantocellular reticular nucleus, dorsal part"
    )
    acronym: Literal["PGRNd"] = "PGRNd"
    id: Literal["970"] = "970"


class _Pgrnl(_BrainStructureModel):
    """Model PGRNl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paragigantocellular reticular nucleus, lateral part"] = (
        "Paragigantocellular reticular nucleus, lateral part"
    )
    acronym: Literal["PGRNl"] = "PGRNl"
    id: Literal["978"] = "978"


class _Prm(_BrainStructureModel):
    """Model PRM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paramedian lobule"] = "Paramedian lobule"
    acronym: Literal["PRM"] = "PRM"
    id: Literal["1025"] = "1025"


class _Pn(_BrainStructureModel):
    """Model PN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paranigral nucleus"] = "Paranigral nucleus"
    acronym: Literal["PN"] = "PN"
    id: Literal["607344830"] = "607344830"


class _Ppy(_BrainStructureModel):
    """Model PPY"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parapyramidal nucleus"] = "Parapyramidal nucleus"
    acronym: Literal["PPY"] = "PPY"
    id: Literal["1069"] = "1069"


class _Pas(_BrainStructureModel):
    """Model PAS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parasolitary nucleus"] = "Parasolitary nucleus"
    acronym: Literal["PAS"] = "PAS"
    id: Literal["859"] = "859"


class _Ps(_BrainStructureModel):
    """Model PS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parastrial nucleus"] = "Parastrial nucleus"
    acronym: Literal["PS"] = "PS"
    id: Literal["1109"] = "1109"


class _Par(_BrainStructureModel):
    """Model PAR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parasubiculum"] = "Parasubiculum"
    acronym: Literal["PAR"] = "PAR"
    id: Literal["843"] = "843"


class _Pstn(_BrainStructureModel):
    """Model PSTN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parasubthalamic nucleus"] = "Parasubthalamic nucleus"
    acronym: Literal["PSTN"] = "PSTN"
    id: Literal["364"] = "364"


class _Pt(_BrainStructureModel):
    """Model PT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parataenial nucleus"] = "Parataenial nucleus"
    acronym: Literal["PT"] = "PT"
    id: Literal["15"] = "15"


class _Pa5(_BrainStructureModel):
    """Model Pa5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paratrigeminal nucleus"] = "Paratrigeminal nucleus"
    acronym: Literal["Pa5"] = "Pa5"
    id: Literal["589508451"] = "589508451"


class _Pa4(_BrainStructureModel):
    """Model Pa4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paratrochlear nucleus"] = "Paratrochlear nucleus"
    acronym: Literal["Pa4"] = "Pa4"
    id: Literal["606826663"] = "606826663"


class _Pvh(_BrainStructureModel):
    """Model PVH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paraventricular hypothalamic nucleus"] = "Paraventricular hypothalamic nucleus"
    acronym: Literal["PVH"] = "PVH"
    id: Literal["38"] = "38"


class _Pvhd(_BrainStructureModel):
    """Model PVHd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paraventricular hypothalamic nucleus, descending division"] = (
        "Paraventricular hypothalamic nucleus, descending division"
    )
    acronym: Literal["PVHd"] = "PVHd"
    id: Literal["63"] = "63"


class _Pvt(_BrainStructureModel):
    """Model PVT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Paraventricular nucleus of the thalamus"] = "Paraventricular nucleus of the thalamus"
    acronym: Literal["PVT"] = "PVT"
    id: Literal["149"] = "149"


class _Pc5(_BrainStructureModel):
    """Model PC5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parvicellular motor 5 nucleus"] = "Parvicellular motor 5 nucleus"
    acronym: Literal["PC5"] = "PC5"
    id: Literal["549009223"] = "549009223"


class _Parn(_BrainStructureModel):
    """Model PARN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Parvicellular reticular nucleus"] = "Parvicellular reticular nucleus"
    acronym: Literal["PARN"] = "PARN"
    id: Literal["852"] = "852"


class _Ppn(_BrainStructureModel):
    """Model PPN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pedunculopontine nucleus"] = "Pedunculopontine nucleus"
    acronym: Literal["PPN"] = "PPN"
    id: Literal["1052"] = "1052"


class _Pag(_BrainStructureModel):
    """Model PAG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Periaqueductal gray"] = "Periaqueductal gray"
    acronym: Literal["PAG"] = "PAG"
    id: Literal["795"] = "795"


class _Pef(_BrainStructureModel):
    """Model PeF"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Perifornical nucleus"] = "Perifornical nucleus"
    acronym: Literal["PeF"] = "PeF"
    id: Literal["576073704"] = "576073704"


class _Phy(_BrainStructureModel):
    """Model PHY"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Perihypoglossal nuclei"] = "Perihypoglossal nuclei"
    acronym: Literal["PHY"] = "PHY"
    id: Literal["154"] = "154"


class _Pp(_BrainStructureModel):
    """Model PP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Peripeduncular nucleus"] = "Peripeduncular nucleus"
    acronym: Literal["PP"] = "PP"
    id: Literal["1044"] = "1044"


class _Pr(_BrainStructureModel):
    """Model PR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Perireunensis nucleus"] = "Perireunensis nucleus"
    acronym: Literal["PR"] = "PR"
    id: Literal["1077"] = "1077"


class _Peri(_BrainStructureModel):
    """Model PERI"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Perirhinal area"] = "Perirhinal area"
    acronym: Literal["PERI"] = "PERI"
    id: Literal["922"] = "922"


class _Peri1(_BrainStructureModel):
    """Model PERI1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Perirhinal area, layer 1"] = "Perirhinal area, layer 1"
    acronym: Literal["PERI1"] = "PERI1"
    id: Literal["540"] = "540"


class _Peri2_3(_BrainStructureModel):
    """Model PERI2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Perirhinal area, layer 2/3"] = "Perirhinal area, layer 2/3"
    acronym: Literal["PERI2/3"] = "PERI2/3"
    id: Literal["888"] = "888"


class _Peri5(_BrainStructureModel):
    """Model PERI5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Perirhinal area, layer 5"] = "Perirhinal area, layer 5"
    acronym: Literal["PERI5"] = "PERI5"
    id: Literal["692"] = "692"


class _Peri6A(_BrainStructureModel):
    """Model PERI6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Perirhinal area, layer 6a"] = "Perirhinal area, layer 6a"
    acronym: Literal["PERI6a"] = "PERI6a"
    id: Literal["335"] = "335"


class _Peri6B(_BrainStructureModel):
    """Model PERI6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Perirhinal area, layer 6b"] = "Perirhinal area, layer 6b"
    acronym: Literal["PERI6b"] = "PERI6b"
    id: Literal["368"] = "368"


class _P5(_BrainStructureModel):
    """Model P5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Peritrigeminal zone"] = "Peritrigeminal zone"
    acronym: Literal["P5"] = "P5"
    id: Literal["549009215"] = "549009215"


class _Pva(_BrainStructureModel):
    """Model PVa"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Periventricular hypothalamic nucleus, anterior part"] = (
        "Periventricular hypothalamic nucleus, anterior part"
    )
    acronym: Literal["PVa"] = "PVa"
    id: Literal["30"] = "30"


class _Pvi(_BrainStructureModel):
    """Model PVi"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Periventricular hypothalamic nucleus, intermediate part"] = (
        "Periventricular hypothalamic nucleus, intermediate part"
    )
    acronym: Literal["PVi"] = "PVi"
    id: Literal["118"] = "118"


class _Pvp(_BrainStructureModel):
    """Model PVp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Periventricular hypothalamic nucleus, posterior part"] = (
        "Periventricular hypothalamic nucleus, posterior part"
    )
    acronym: Literal["PVp"] = "PVp"
    id: Literal["126"] = "126"


class _Pvpo(_BrainStructureModel):
    """Model PVpo"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Periventricular hypothalamic nucleus, preoptic part"] = (
        "Periventricular hypothalamic nucleus, preoptic part"
    )
    acronym: Literal["PVpo"] = "PVpo"
    id: Literal["133"] = "133"


class _Pvr(_BrainStructureModel):
    """Model PVR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Periventricular region"] = "Periventricular region"
    acronym: Literal["PVR"] = "PVR"
    id: Literal["141"] = "141"


class _Pvz(_BrainStructureModel):
    """Model PVZ"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Periventricular zone"] = "Periventricular zone"
    acronym: Literal["PVZ"] = "PVZ"
    id: Literal["157"] = "157"


class _Pir(_BrainStructureModel):
    """Model PIR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Piriform area"] = "Piriform area"
    acronym: Literal["PIR"] = "PIR"
    id: Literal["961"] = "961"


class _Paa(_BrainStructureModel):
    """Model PAA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Piriform-amygdalar area"] = "Piriform-amygdalar area"
    acronym: Literal["PAA"] = "PAA"
    id: Literal["788"] = "788"


class _P(_BrainStructureModel):
    """Model P"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pons"] = "Pons"
    acronym: Literal["P"] = "P"
    id: Literal["771"] = "771"


class _P_Sat(_BrainStructureModel):
    """Model P-sat"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pons, behavioral state related"] = "Pons, behavioral state related"
    acronym: Literal["P-sat"] = "P-sat"
    id: Literal["1117"] = "1117"


class _P_Mot(_BrainStructureModel):
    """Model P-mot"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pons, motor related"] = "Pons, motor related"
    acronym: Literal["P-mot"] = "P-mot"
    id: Literal["987"] = "987"


class _P_Sen(_BrainStructureModel):
    """Model P-sen"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pons, sensory related"] = "Pons, sensory related"
    acronym: Literal["P-sen"] = "P-sen"
    id: Literal["1132"] = "1132"


class _Pcg(_BrainStructureModel):
    """Model PCG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pontine central gray"] = "Pontine central gray"
    acronym: Literal["PCG"] = "PCG"
    id: Literal["898"] = "898"


class _Pg(_BrainStructureModel):
    """Model PG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pontine gray"] = "Pontine gray"
    acronym: Literal["PG"] = "PG"
    id: Literal["931"] = "931"


class _Prnr(_BrainStructureModel):
    """Model PRNr"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pontine reticular nucleus"] = "Pontine reticular nucleus"
    acronym: Literal["PRNr"] = "PRNr"
    id: Literal["146"] = "146"


class _Prnc(_BrainStructureModel):
    """Model PRNc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pontine reticular nucleus, caudal part"] = "Pontine reticular nucleus, caudal part"
    acronym: Literal["PRNc"] = "PRNc"
    id: Literal["1093"] = "1093"


class _Pa(_BrainStructureModel):
    """Model PA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior amygdalar nucleus"] = "Posterior amygdalar nucleus"
    acronym: Literal["PA"] = "PA"
    id: Literal["780"] = "780"


class _Audpo(_BrainStructureModel):
    """Model AUDpo"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior auditory area"] = "Posterior auditory area"
    acronym: Literal["AUDpo"] = "AUDpo"
    id: Literal["1027"] = "1027"


class _Audpo1(_BrainStructureModel):
    """Model AUDpo1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior auditory area, layer 1"] = "Posterior auditory area, layer 1"
    acronym: Literal["AUDpo1"] = "AUDpo1"
    id: Literal["696"] = "696"


class _Audpo2_3(_BrainStructureModel):
    """Model AUDpo2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior auditory area, layer 2/3"] = "Posterior auditory area, layer 2/3"
    acronym: Literal["AUDpo2/3"] = "AUDpo2/3"
    id: Literal["643"] = "643"


class _Audpo4(_BrainStructureModel):
    """Model AUDpo4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior auditory area, layer 4"] = "Posterior auditory area, layer 4"
    acronym: Literal["AUDpo4"] = "AUDpo4"
    id: Literal["759"] = "759"


class _Audpo5(_BrainStructureModel):
    """Model AUDpo5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior auditory area, layer 5"] = "Posterior auditory area, layer 5"
    acronym: Literal["AUDpo5"] = "AUDpo5"
    id: Literal["791"] = "791"


class _Audpo6A(_BrainStructureModel):
    """Model AUDpo6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior auditory area, layer 6a"] = "Posterior auditory area, layer 6a"
    acronym: Literal["AUDpo6a"] = "AUDpo6a"
    id: Literal["249"] = "249"


class _Audpo6B(_BrainStructureModel):
    """Model AUDpo6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior auditory area, layer 6b"] = "Posterior auditory area, layer 6b"
    acronym: Literal["AUDpo6b"] = "AUDpo6b"
    id: Literal["456"] = "456"


class _Po(_BrainStructureModel):
    """Model PO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior complex of the thalamus"] = "Posterior complex of the thalamus"
    acronym: Literal["PO"] = "PO"
    id: Literal["1020"] = "1020"


class _Ph(_BrainStructureModel):
    """Model PH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior hypothalamic nucleus"] = "Posterior hypothalamic nucleus"
    acronym: Literal["PH"] = "PH"
    id: Literal["946"] = "946"


class _Pil(_BrainStructureModel):
    """Model PIL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior intralaminar thalamic nucleus"] = "Posterior intralaminar thalamic nucleus"
    acronym: Literal["PIL"] = "PIL"
    id: Literal["560581563"] = "560581563"


class _Pol(_BrainStructureModel):
    """Model POL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior limiting nucleus of the thalamus"] = "Posterior limiting nucleus of the thalamus"
    acronym: Literal["POL"] = "POL"
    id: Literal["1029"] = "1029"


class _Ptlp(_BrainStructureModel):
    """Model PTLp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior parietal association areas"] = "Posterior parietal association areas"
    acronym: Literal["PTLp"] = "PTLp"
    id: Literal["22"] = "22"


class _Ppt(_BrainStructureModel):
    """Model PPT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior pretectal nucleus"] = "Posterior pretectal nucleus"
    acronym: Literal["PPT"] = "PPT"
    id: Literal["1061"] = "1061"


class _Pot(_BrainStructureModel):
    """Model PoT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterior triangular thalamic nucleus"] = "Posterior triangular thalamic nucleus"
    acronym: Literal["PoT"] = "PoT"
    id: Literal["563807435"] = "563807435"


class _Pd(_BrainStructureModel):
    """Model PD"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterodorsal preoptic nucleus"] = "Posterodorsal preoptic nucleus"
    acronym: Literal["PD"] = "PD"
    id: Literal["914"] = "914"


class _Pdtg(_BrainStructureModel):
    """Model PDTg"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterodorsal tegmental nucleus"] = "Posterodorsal tegmental nucleus"
    acronym: Literal["PDTg"] = "PDTg"
    id: Literal["599626927"] = "599626927"


class _Vispl(_BrainStructureModel):
    """Model VISpl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterolateral visual area"] = "Posterolateral visual area"
    acronym: Literal["VISpl"] = "VISpl"
    id: Literal["425"] = "425"


class _Vispl1(_BrainStructureModel):
    """Model VISpl1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterolateral visual area, layer 1"] = "Posterolateral visual area, layer 1"
    acronym: Literal["VISpl1"] = "VISpl1"
    id: Literal["750"] = "750"


class _Vispl2_3(_BrainStructureModel):
    """Model VISpl2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterolateral visual area, layer 2/3"] = "Posterolateral visual area, layer 2/3"
    acronym: Literal["VISpl2/3"] = "VISpl2/3"
    id: Literal["269"] = "269"


class _Vispl4(_BrainStructureModel):
    """Model VISpl4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterolateral visual area, layer 4"] = "Posterolateral visual area, layer 4"
    acronym: Literal["VISpl4"] = "VISpl4"
    id: Literal["869"] = "869"


class _Vispl5(_BrainStructureModel):
    """Model VISpl5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterolateral visual area, layer 5"] = "Posterolateral visual area, layer 5"
    acronym: Literal["VISpl5"] = "VISpl5"
    id: Literal["902"] = "902"


class _Vispl6A(_BrainStructureModel):
    """Model VISpl6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterolateral visual area, layer 6a"] = "Posterolateral visual area, layer 6a"
    acronym: Literal["VISpl6a"] = "VISpl6a"
    id: Literal["377"] = "377"


class _Vispl6B(_BrainStructureModel):
    """Model VISpl6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Posterolateral visual area, layer 6b"] = "Posterolateral visual area, layer 6b"
    acronym: Literal["VISpl6b"] = "VISpl6b"
    id: Literal["393"] = "393"


class _Tr(_BrainStructureModel):
    """Model TR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Postpiriform transition area"] = "Postpiriform transition area"
    acronym: Literal["TR"] = "TR"
    id: Literal["566"] = "566"


class _Vispor(_BrainStructureModel):
    """Model VISpor"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Postrhinal area"] = "Postrhinal area"
    acronym: Literal["VISpor"] = "VISpor"
    id: Literal["312782628"] = "312782628"


class _Vispor1(_BrainStructureModel):
    """Model VISpor1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Postrhinal area, layer 1"] = "Postrhinal area, layer 1"
    acronym: Literal["VISpor1"] = "VISpor1"
    id: Literal["312782632"] = "312782632"


class _Vispor2_3(_BrainStructureModel):
    """Model VISpor2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Postrhinal area, layer 2/3"] = "Postrhinal area, layer 2/3"
    acronym: Literal["VISpor2/3"] = "VISpor2/3"
    id: Literal["312782636"] = "312782636"


class _Vispor4(_BrainStructureModel):
    """Model VISpor4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Postrhinal area, layer 4"] = "Postrhinal area, layer 4"
    acronym: Literal["VISpor4"] = "VISpor4"
    id: Literal["312782640"] = "312782640"


class _Vispor5(_BrainStructureModel):
    """Model VISpor5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Postrhinal area, layer 5"] = "Postrhinal area, layer 5"
    acronym: Literal["VISpor5"] = "VISpor5"
    id: Literal["312782644"] = "312782644"


class _Vispor6A(_BrainStructureModel):
    """Model VISpor6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Postrhinal area, layer 6a"] = "Postrhinal area, layer 6a"
    acronym: Literal["VISpor6a"] = "VISpor6a"
    id: Literal["312782648"] = "312782648"


class _Vispor6B(_BrainStructureModel):
    """Model VISpor6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Postrhinal area, layer 6b"] = "Postrhinal area, layer 6b"
    acronym: Literal["VISpor6b"] = "VISpor6b"
    id: Literal["312782652"] = "312782652"


class _Post(_BrainStructureModel):
    """Model POST"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Postsubiculum"] = "Postsubiculum"
    acronym: Literal["POST"] = "POST"
    id: Literal["1037"] = "1037"


class _Prc(_BrainStructureModel):
    """Model PRC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Precommissural nucleus"] = "Precommissural nucleus"
    acronym: Literal["PRC"] = "PRC"
    id: Literal["50"] = "50"


class _Pl(_BrainStructureModel):
    """Model PL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Prelimbic area"] = "Prelimbic area"
    acronym: Literal["PL"] = "PL"
    id: Literal["972"] = "972"


class _Pl1(_BrainStructureModel):
    """Model PL1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Prelimbic area, layer 1"] = "Prelimbic area, layer 1"
    acronym: Literal["PL1"] = "PL1"
    id: Literal["171"] = "171"


class _Pl2_3(_BrainStructureModel):
    """Model PL2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Prelimbic area, layer 2/3"] = "Prelimbic area, layer 2/3"
    acronym: Literal["PL2/3"] = "PL2/3"
    id: Literal["304"] = "304"


class _Pl5(_BrainStructureModel):
    """Model PL5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Prelimbic area, layer 5"] = "Prelimbic area, layer 5"
    acronym: Literal["PL5"] = "PL5"
    id: Literal["363"] = "363"


class _Pl6A(_BrainStructureModel):
    """Model PL6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Prelimbic area, layer 6a"] = "Prelimbic area, layer 6a"
    acronym: Literal["PL6a"] = "PL6a"
    id: Literal["84"] = "84"


class _Pl6B(_BrainStructureModel):
    """Model PL6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Prelimbic area, layer 6b"] = "Prelimbic area, layer 6b"
    acronym: Literal["PL6b"] = "PL6b"
    id: Literal["132"] = "132"


class _Pst(_BrainStructureModel):
    """Model PST"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Preparasubthalamic nucleus"] = "Preparasubthalamic nucleus"
    acronym: Literal["PST"] = "PST"
    id: Literal["356"] = "356"


class _Pre(_BrainStructureModel):
    """Model PRE"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Presubiculum"] = "Presubiculum"
    acronym: Literal["PRE"] = "PRE"
    id: Literal["1084"] = "1084"


class _Prt(_BrainStructureModel):
    """Model PRT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pretectal region"] = "Pretectal region"
    acronym: Literal["PRT"] = "PRT"
    id: Literal["1100"] = "1100"


class _Audp(_BrainStructureModel):
    """Model AUDp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary auditory area"] = "Primary auditory area"
    acronym: Literal["AUDp"] = "AUDp"
    id: Literal["1002"] = "1002"


class _Audp1(_BrainStructureModel):
    """Model AUDp1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary auditory area, layer 1"] = "Primary auditory area, layer 1"
    acronym: Literal["AUDp1"] = "AUDp1"
    id: Literal["735"] = "735"


class _Audp2_3(_BrainStructureModel):
    """Model AUDp2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary auditory area, layer 2/3"] = "Primary auditory area, layer 2/3"
    acronym: Literal["AUDp2/3"] = "AUDp2/3"
    id: Literal["251"] = "251"


class _Audp4(_BrainStructureModel):
    """Model AUDp4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary auditory area, layer 4"] = "Primary auditory area, layer 4"
    acronym: Literal["AUDp4"] = "AUDp4"
    id: Literal["816"] = "816"


class _Audp5(_BrainStructureModel):
    """Model AUDp5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary auditory area, layer 5"] = "Primary auditory area, layer 5"
    acronym: Literal["AUDp5"] = "AUDp5"
    id: Literal["847"] = "847"


class _Audp6A(_BrainStructureModel):
    """Model AUDp6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary auditory area, layer 6a"] = "Primary auditory area, layer 6a"
    acronym: Literal["AUDp6a"] = "AUDp6a"
    id: Literal["954"] = "954"


class _Audp6B(_BrainStructureModel):
    """Model AUDp6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary auditory area, layer 6b"] = "Primary auditory area, layer 6b"
    acronym: Literal["AUDp6b"] = "AUDp6b"
    id: Literal["1005"] = "1005"


class _Mop(_BrainStructureModel):
    """Model MOp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary motor area"] = "Primary motor area"
    acronym: Literal["MOp"] = "MOp"
    id: Literal["985"] = "985"


class _Mop1(_BrainStructureModel):
    """Model MOp1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary motor area, Layer 1"] = "Primary motor area, Layer 1"
    acronym: Literal["MOp1"] = "MOp1"
    id: Literal["320"] = "320"


class _Mop2_3(_BrainStructureModel):
    """Model MOp2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary motor area, Layer 2/3"] = "Primary motor area, Layer 2/3"
    acronym: Literal["MOp2/3"] = "MOp2/3"
    id: Literal["943"] = "943"


class _Mop5(_BrainStructureModel):
    """Model MOp5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary motor area, Layer 5"] = "Primary motor area, Layer 5"
    acronym: Literal["MOp5"] = "MOp5"
    id: Literal["648"] = "648"


class _Mop6A(_BrainStructureModel):
    """Model MOp6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary motor area, Layer 6a"] = "Primary motor area, Layer 6a"
    acronym: Literal["MOp6a"] = "MOp6a"
    id: Literal["844"] = "844"


class _Mop6B(_BrainStructureModel):
    """Model MOp6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary motor area, Layer 6b"] = "Primary motor area, Layer 6b"
    acronym: Literal["MOp6b"] = "MOp6b"
    id: Literal["882"] = "882"


class _Ssp(_BrainStructureModel):
    """Model SSp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area"] = "Primary somatosensory area"
    acronym: Literal["SSp"] = "SSp"
    id: Literal["322"] = "322"


class _Ssp_Bfd(_BrainStructureModel):
    """Model SSp-bfd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, barrel field"] = "Primary somatosensory area, barrel field"
    acronym: Literal["SSp-bfd"] = "SSp-bfd"
    id: Literal["329"] = "329"


class _Ssp_Bfd1(_BrainStructureModel):
    """Model SSp-bfd1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, barrel field, layer 1"] = (
        "Primary somatosensory area, barrel field, layer 1"
    )
    acronym: Literal["SSp-bfd1"] = "SSp-bfd1"
    id: Literal["981"] = "981"


class _Ssp_Bfd2_3(_BrainStructureModel):
    """Model SSp-bfd2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, barrel field, layer 2/3"] = (
        "Primary somatosensory area, barrel field, layer 2/3"
    )
    acronym: Literal["SSp-bfd2/3"] = "SSp-bfd2/3"
    id: Literal["201"] = "201"


class _Ssp_Bfd4(_BrainStructureModel):
    """Model SSp-bfd4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, barrel field, layer 4"] = (
        "Primary somatosensory area, barrel field, layer 4"
    )
    acronym: Literal["SSp-bfd4"] = "SSp-bfd4"
    id: Literal["1047"] = "1047"


class _Ssp_Bfd5(_BrainStructureModel):
    """Model SSp-bfd5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, barrel field, layer 5"] = (
        "Primary somatosensory area, barrel field, layer 5"
    )
    acronym: Literal["SSp-bfd5"] = "SSp-bfd5"
    id: Literal["1070"] = "1070"


class _Ssp_Bfd6A(_BrainStructureModel):
    """Model SSp-bfd6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, barrel field, layer 6a"] = (
        "Primary somatosensory area, barrel field, layer 6a"
    )
    acronym: Literal["SSp-bfd6a"] = "SSp-bfd6a"
    id: Literal["1038"] = "1038"


class _Ssp_Bfd6B(_BrainStructureModel):
    """Model SSp-bfd6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, barrel field, layer 6b"] = (
        "Primary somatosensory area, barrel field, layer 6b"
    )
    acronym: Literal["SSp-bfd6b"] = "SSp-bfd6b"
    id: Literal["1062"] = "1062"


class _Ssp_Ll(_BrainStructureModel):
    """Model SSp-ll"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, lower limb"] = "Primary somatosensory area, lower limb"
    acronym: Literal["SSp-ll"] = "SSp-ll"
    id: Literal["337"] = "337"


class _Ssp_Ll1(_BrainStructureModel):
    """Model SSp-ll1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, lower limb, layer 1"] = "Primary somatosensory area, lower limb, layer 1"
    acronym: Literal["SSp-ll1"] = "SSp-ll1"
    id: Literal["1030"] = "1030"


class _Ssp_Ll2_3(_BrainStructureModel):
    """Model SSp-ll2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, lower limb, layer 2/3"] = (
        "Primary somatosensory area, lower limb, layer 2/3"
    )
    acronym: Literal["SSp-ll2/3"] = "SSp-ll2/3"
    id: Literal["113"] = "113"


class _Ssp_Ll4(_BrainStructureModel):
    """Model SSp-ll4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, lower limb, layer 4"] = "Primary somatosensory area, lower limb, layer 4"
    acronym: Literal["SSp-ll4"] = "SSp-ll4"
    id: Literal["1094"] = "1094"


class _Ssp_Ll5(_BrainStructureModel):
    """Model SSp-ll5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, lower limb, layer 5"] = "Primary somatosensory area, lower limb, layer 5"
    acronym: Literal["SSp-ll5"] = "SSp-ll5"
    id: Literal["1128"] = "1128"


class _Ssp_Ll6A(_BrainStructureModel):
    """Model SSp-ll6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, lower limb, layer 6a"] = (
        "Primary somatosensory area, lower limb, layer 6a"
    )
    acronym: Literal["SSp-ll6a"] = "SSp-ll6a"
    id: Literal["478"] = "478"


class _Ssp_Ll6B(_BrainStructureModel):
    """Model SSp-ll6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, lower limb, layer 6b"] = (
        "Primary somatosensory area, lower limb, layer 6b"
    )
    acronym: Literal["SSp-ll6b"] = "SSp-ll6b"
    id: Literal["510"] = "510"


class _Ssp_M(_BrainStructureModel):
    """Model SSp-m"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, mouth"] = "Primary somatosensory area, mouth"
    acronym: Literal["SSp-m"] = "SSp-m"
    id: Literal["345"] = "345"


class _Ssp_M1(_BrainStructureModel):
    """Model SSp-m1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, mouth, layer 1"] = "Primary somatosensory area, mouth, layer 1"
    acronym: Literal["SSp-m1"] = "SSp-m1"
    id: Literal["878"] = "878"


class _Ssp_M2_3(_BrainStructureModel):
    """Model SSp-m2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, mouth, layer 2/3"] = "Primary somatosensory area, mouth, layer 2/3"
    acronym: Literal["SSp-m2/3"] = "SSp-m2/3"
    id: Literal["657"] = "657"


class _Ssp_M4(_BrainStructureModel):
    """Model SSp-m4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, mouth, layer 4"] = "Primary somatosensory area, mouth, layer 4"
    acronym: Literal["SSp-m4"] = "SSp-m4"
    id: Literal["950"] = "950"


class _Ssp_M5(_BrainStructureModel):
    """Model SSp-m5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, mouth, layer 5"] = "Primary somatosensory area, mouth, layer 5"
    acronym: Literal["SSp-m5"] = "SSp-m5"
    id: Literal["974"] = "974"


class _Ssp_M6A(_BrainStructureModel):
    """Model SSp-m6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, mouth, layer 6a"] = "Primary somatosensory area, mouth, layer 6a"
    acronym: Literal["SSp-m6a"] = "SSp-m6a"
    id: Literal["1102"] = "1102"


class _Ssp_M6B(_BrainStructureModel):
    """Model SSp-m6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, mouth, layer 6b"] = "Primary somatosensory area, mouth, layer 6b"
    acronym: Literal["SSp-m6b"] = "SSp-m6b"
    id: Literal["2"] = "2"


class _Ssp_N(_BrainStructureModel):
    """Model SSp-n"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, nose"] = "Primary somatosensory area, nose"
    acronym: Literal["SSp-n"] = "SSp-n"
    id: Literal["353"] = "353"


class _Ssp_N1(_BrainStructureModel):
    """Model SSp-n1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, nose, layer 1"] = "Primary somatosensory area, nose, layer 1"
    acronym: Literal["SSp-n1"] = "SSp-n1"
    id: Literal["558"] = "558"


class _Ssp_N2_3(_BrainStructureModel):
    """Model SSp-n2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, nose, layer 2/3"] = "Primary somatosensory area, nose, layer 2/3"
    acronym: Literal["SSp-n2/3"] = "SSp-n2/3"
    id: Literal["838"] = "838"


class _Ssp_N4(_BrainStructureModel):
    """Model SSp-n4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, nose, layer 4"] = "Primary somatosensory area, nose, layer 4"
    acronym: Literal["SSp-n4"] = "SSp-n4"
    id: Literal["654"] = "654"


class _Ssp_N5(_BrainStructureModel):
    """Model SSp-n5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, nose, layer 5"] = "Primary somatosensory area, nose, layer 5"
    acronym: Literal["SSp-n5"] = "SSp-n5"
    id: Literal["702"] = "702"


class _Ssp_N6A(_BrainStructureModel):
    """Model SSp-n6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, nose, layer 6a"] = "Primary somatosensory area, nose, layer 6a"
    acronym: Literal["SSp-n6a"] = "SSp-n6a"
    id: Literal["889"] = "889"


class _Ssp_N6B(_BrainStructureModel):
    """Model SSp-n6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, nose, layer 6b"] = "Primary somatosensory area, nose, layer 6b"
    acronym: Literal["SSp-n6b"] = "SSp-n6b"
    id: Literal["929"] = "929"


class _Ssp_Tr(_BrainStructureModel):
    """Model SSp-tr"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, trunk"] = "Primary somatosensory area, trunk"
    acronym: Literal["SSp-tr"] = "SSp-tr"
    id: Literal["361"] = "361"


class _Ssp_Tr1(_BrainStructureModel):
    """Model SSp-tr1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, trunk, layer 1"] = "Primary somatosensory area, trunk, layer 1"
    acronym: Literal["SSp-tr1"] = "SSp-tr1"
    id: Literal["1006"] = "1006"


class _Ssp_Tr2_3(_BrainStructureModel):
    """Model SSp-tr2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, trunk, layer 2/3"] = "Primary somatosensory area, trunk, layer 2/3"
    acronym: Literal["SSp-tr2/3"] = "SSp-tr2/3"
    id: Literal["670"] = "670"


class _Ssp_Tr4(_BrainStructureModel):
    """Model SSp-tr4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, trunk, layer 4"] = "Primary somatosensory area, trunk, layer 4"
    acronym: Literal["SSp-tr4"] = "SSp-tr4"
    id: Literal["1086"] = "1086"


class _Ssp_Tr5(_BrainStructureModel):
    """Model SSp-tr5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, trunk, layer 5"] = "Primary somatosensory area, trunk, layer 5"
    acronym: Literal["SSp-tr5"] = "SSp-tr5"
    id: Literal["1111"] = "1111"


class _Ssp_Tr6A(_BrainStructureModel):
    """Model SSp-tr6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, trunk, layer 6a"] = "Primary somatosensory area, trunk, layer 6a"
    acronym: Literal["SSp-tr6a"] = "SSp-tr6a"
    id: Literal["9"] = "9"


class _Ssp_Tr6B(_BrainStructureModel):
    """Model SSp-tr6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, trunk, layer 6b"] = "Primary somatosensory area, trunk, layer 6b"
    acronym: Literal["SSp-tr6b"] = "SSp-tr6b"
    id: Literal["461"] = "461"


class _Ssp_Un(_BrainStructureModel):
    """Model SSp-un"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, unassigned"] = "Primary somatosensory area, unassigned"
    acronym: Literal["SSp-un"] = "SSp-un"
    id: Literal["182305689"] = "182305689"


class _Ssp_Un1(_BrainStructureModel):
    """Model SSp-un1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, unassigned, layer 1"] = "Primary somatosensory area, unassigned, layer 1"
    acronym: Literal["SSp-un1"] = "SSp-un1"
    id: Literal["182305693"] = "182305693"


class _Ssp_Un2_3(_BrainStructureModel):
    """Model SSp-un2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, unassigned, layer 2/3"] = (
        "Primary somatosensory area, unassigned, layer 2/3"
    )
    acronym: Literal["SSp-un2/3"] = "SSp-un2/3"
    id: Literal["182305697"] = "182305697"


class _Ssp_Un4(_BrainStructureModel):
    """Model SSp-un4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, unassigned, layer 4"] = "Primary somatosensory area, unassigned, layer 4"
    acronym: Literal["SSp-un4"] = "SSp-un4"
    id: Literal["182305701"] = "182305701"


class _Ssp_Un5(_BrainStructureModel):
    """Model SSp-un5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, unassigned, layer 5"] = "Primary somatosensory area, unassigned, layer 5"
    acronym: Literal["SSp-un5"] = "SSp-un5"
    id: Literal["182305705"] = "182305705"


class _Ssp_Un6A(_BrainStructureModel):
    """Model SSp-un6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, unassigned, layer 6a"] = (
        "Primary somatosensory area, unassigned, layer 6a"
    )
    acronym: Literal["SSp-un6a"] = "SSp-un6a"
    id: Literal["182305709"] = "182305709"


class _Ssp_Un6B(_BrainStructureModel):
    """Model SSp-un6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, unassigned, layer 6b"] = (
        "Primary somatosensory area, unassigned, layer 6b"
    )
    acronym: Literal["SSp-un6b"] = "SSp-un6b"
    id: Literal["182305713"] = "182305713"


class _Ssp_Ul(_BrainStructureModel):
    """Model SSp-ul"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, upper limb"] = "Primary somatosensory area, upper limb"
    acronym: Literal["SSp-ul"] = "SSp-ul"
    id: Literal["369"] = "369"


class _Ssp_Ul1(_BrainStructureModel):
    """Model SSp-ul1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, upper limb, layer 1"] = "Primary somatosensory area, upper limb, layer 1"
    acronym: Literal["SSp-ul1"] = "SSp-ul1"
    id: Literal["450"] = "450"


class _Ssp_Ul2_3(_BrainStructureModel):
    """Model SSp-ul2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, upper limb, layer 2/3"] = (
        "Primary somatosensory area, upper limb, layer 2/3"
    )
    acronym: Literal["SSp-ul2/3"] = "SSp-ul2/3"
    id: Literal["854"] = "854"


class _Ssp_Ul4(_BrainStructureModel):
    """Model SSp-ul4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, upper limb, layer 4"] = "Primary somatosensory area, upper limb, layer 4"
    acronym: Literal["SSp-ul4"] = "SSp-ul4"
    id: Literal["577"] = "577"


class _Ssp_Ul5(_BrainStructureModel):
    """Model SSp-ul5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, upper limb, layer 5"] = "Primary somatosensory area, upper limb, layer 5"
    acronym: Literal["SSp-ul5"] = "SSp-ul5"
    id: Literal["625"] = "625"


class _Ssp_Ul6A(_BrainStructureModel):
    """Model SSp-ul6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, upper limb, layer 6a"] = (
        "Primary somatosensory area, upper limb, layer 6a"
    )
    acronym: Literal["SSp-ul6a"] = "SSp-ul6a"
    id: Literal["945"] = "945"


class _Ssp_Ul6B(_BrainStructureModel):
    """Model SSp-ul6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary somatosensory area, upper limb, layer 6b"] = (
        "Primary somatosensory area, upper limb, layer 6b"
    )
    acronym: Literal["SSp-ul6b"] = "SSp-ul6b"
    id: Literal["1026"] = "1026"


class _Visp(_BrainStructureModel):
    """Model VISp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary visual area"] = "Primary visual area"
    acronym: Literal["VISp"] = "VISp"
    id: Literal["385"] = "385"


class _Visp1(_BrainStructureModel):
    """Model VISp1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary visual area, layer 1"] = "Primary visual area, layer 1"
    acronym: Literal["VISp1"] = "VISp1"
    id: Literal["593"] = "593"


class _Visp2_3(_BrainStructureModel):
    """Model VISp2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary visual area, layer 2/3"] = "Primary visual area, layer 2/3"
    acronym: Literal["VISp2/3"] = "VISp2/3"
    id: Literal["821"] = "821"


class _Visp4(_BrainStructureModel):
    """Model VISp4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary visual area, layer 4"] = "Primary visual area, layer 4"
    acronym: Literal["VISp4"] = "VISp4"
    id: Literal["721"] = "721"


class _Visp5(_BrainStructureModel):
    """Model VISp5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary visual area, layer 5"] = "Primary visual area, layer 5"
    acronym: Literal["VISp5"] = "VISp5"
    id: Literal["778"] = "778"


class _Visp6A(_BrainStructureModel):
    """Model VISp6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary visual area, layer 6a"] = "Primary visual area, layer 6a"
    acronym: Literal["VISp6a"] = "VISp6a"
    id: Literal["33"] = "33"


class _Visp6B(_BrainStructureModel):
    """Model VISp6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Primary visual area, layer 6b"] = "Primary visual area, layer 6b"
    acronym: Literal["VISp6b"] = "VISp6b"
    id: Literal["305"] = "305"


class _Psv(_BrainStructureModel):
    """Model PSV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Principal sensory nucleus of the trigeminal"] = "Principal sensory nucleus of the trigeminal"
    acronym: Literal["PSV"] = "PSV"
    id: Literal["7"] = "7"


class _Pros(_BrainStructureModel):
    """Model ProS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Prosubiculum"] = "Prosubiculum"
    acronym: Literal["ProS"] = "ProS"
    id: Literal["484682470"] = "484682470"


class _Pyr(_BrainStructureModel):
    """Model PYR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Pyramus (VIII)"] = "Pyramus (VIII)"
    acronym: Literal["PYR"] = "PYR"
    id: Literal["951"] = "951"


class _Rn(_BrainStructureModel):
    """Model RN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Red nucleus"] = "Red nucleus"
    acronym: Literal["RN"] = "RN"
    id: Literal["214"] = "214"


class _Rt(_BrainStructureModel):
    """Model RT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Reticular nucleus of the thalamus"] = "Reticular nucleus of the thalamus"
    acronym: Literal["RT"] = "RT"
    id: Literal["262"] = "262"


class _Rch(_BrainStructureModel):
    """Model RCH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrochiasmatic area"] = "Retrochiasmatic area"
    acronym: Literal["RCH"] = "RCH"
    id: Literal["173"] = "173"


class _Rhp(_BrainStructureModel):
    """Model RHP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrohippocampal region"] = "Retrohippocampal region"
    acronym: Literal["RHP"] = "RHP"
    id: Literal["822"] = "822"


class _Rpf(_BrainStructureModel):
    """Model RPF"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retroparafascicular nucleus"] = "Retroparafascicular nucleus"
    acronym: Literal["RPF"] = "RPF"
    id: Literal["549009203"] = "549009203"


class _Rsp(_BrainStructureModel):
    """Model RSP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area"] = "Retrosplenial area"
    acronym: Literal["RSP"] = "RSP"
    id: Literal["254"] = "254"


class _Rspd(_BrainStructureModel):
    """Model RSPd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, dorsal part"] = "Retrosplenial area, dorsal part"
    acronym: Literal["RSPd"] = "RSPd"
    id: Literal["879"] = "879"


class _Rspd1(_BrainStructureModel):
    """Model RSPd1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, dorsal part, layer 1"] = "Retrosplenial area, dorsal part, layer 1"
    acronym: Literal["RSPd1"] = "RSPd1"
    id: Literal["442"] = "442"


class _Rspd2_3(_BrainStructureModel):
    """Model RSPd2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, dorsal part, layer 2/3"] = "Retrosplenial area, dorsal part, layer 2/3"
    acronym: Literal["RSPd2/3"] = "RSPd2/3"
    id: Literal["434"] = "434"


class _Rspd4(_BrainStructureModel):
    """Model RSPd4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, dorsal part, layer 4"] = "Retrosplenial area, dorsal part, layer 4"
    acronym: Literal["RSPd4"] = "RSPd4"
    id: Literal["545"] = "545"


class _Rspd5(_BrainStructureModel):
    """Model RSPd5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, dorsal part, layer 5"] = "Retrosplenial area, dorsal part, layer 5"
    acronym: Literal["RSPd5"] = "RSPd5"
    id: Literal["610"] = "610"


class _Rspd6A(_BrainStructureModel):
    """Model RSPd6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, dorsal part, layer 6a"] = "Retrosplenial area, dorsal part, layer 6a"
    acronym: Literal["RSPd6a"] = "RSPd6a"
    id: Literal["274"] = "274"


class _Rspd6B(_BrainStructureModel):
    """Model RSPd6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, dorsal part, layer 6b"] = "Retrosplenial area, dorsal part, layer 6b"
    acronym: Literal["RSPd6b"] = "RSPd6b"
    id: Literal["330"] = "330"


class _Rspagl(_BrainStructureModel):
    """Model RSPagl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, lateral agranular part"] = "Retrosplenial area, lateral agranular part"
    acronym: Literal["RSPagl"] = "RSPagl"
    id: Literal["894"] = "894"


class _Rspagl1(_BrainStructureModel):
    """Model RSPagl1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, lateral agranular part, layer 1"] = (
        "Retrosplenial area, lateral agranular part, layer 1"
    )
    acronym: Literal["RSPagl1"] = "RSPagl1"
    id: Literal["671"] = "671"


class _Rspagl2_3(_BrainStructureModel):
    """Model RSPagl2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, lateral agranular part, layer 2/3"] = (
        "Retrosplenial area, lateral agranular part, layer 2/3"
    )
    acronym: Literal["RSPagl2/3"] = "RSPagl2/3"
    id: Literal["965"] = "965"


class _Rspagl5(_BrainStructureModel):
    """Model RSPagl5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, lateral agranular part, layer 5"] = (
        "Retrosplenial area, lateral agranular part, layer 5"
    )
    acronym: Literal["RSPagl5"] = "RSPagl5"
    id: Literal["774"] = "774"


class _Rspagl6A(_BrainStructureModel):
    """Model RSPagl6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, lateral agranular part, layer 6a"] = (
        "Retrosplenial area, lateral agranular part, layer 6a"
    )
    acronym: Literal["RSPagl6a"] = "RSPagl6a"
    id: Literal["906"] = "906"


class _Rspagl6B(_BrainStructureModel):
    """Model RSPagl6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, lateral agranular part, layer 6b"] = (
        "Retrosplenial area, lateral agranular part, layer 6b"
    )
    acronym: Literal["RSPagl6b"] = "RSPagl6b"
    id: Literal["279"] = "279"


class _Rspv(_BrainStructureModel):
    """Model RSPv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, ventral part"] = "Retrosplenial area, ventral part"
    acronym: Literal["RSPv"] = "RSPv"
    id: Literal["886"] = "886"


class _Rspv1(_BrainStructureModel):
    """Model RSPv1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, ventral part, layer 1"] = "Retrosplenial area, ventral part, layer 1"
    acronym: Literal["RSPv1"] = "RSPv1"
    id: Literal["542"] = "542"


class _Rspv2_3(_BrainStructureModel):
    """Model RSPv2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, ventral part, layer 2/3"] = "Retrosplenial area, ventral part, layer 2/3"
    acronym: Literal["RSPv2/3"] = "RSPv2/3"
    id: Literal["430"] = "430"


class _Rspv5(_BrainStructureModel):
    """Model RSPv5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, ventral part, layer 5"] = "Retrosplenial area, ventral part, layer 5"
    acronym: Literal["RSPv5"] = "RSPv5"
    id: Literal["687"] = "687"


class _Rspv6A(_BrainStructureModel):
    """Model RSPv6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, ventral part, layer 6a"] = "Retrosplenial area, ventral part, layer 6a"
    acronym: Literal["RSPv6a"] = "RSPv6a"
    id: Literal["590"] = "590"


class _Rspv6B(_BrainStructureModel):
    """Model RSPv6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Retrosplenial area, ventral part, layer 6b"] = "Retrosplenial area, ventral part, layer 6b"
    acronym: Literal["RSPv6b"] = "RSPv6b"
    id: Literal["622"] = "622"


class _Rh(_BrainStructureModel):
    """Model RH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Rhomboid nucleus"] = "Rhomboid nucleus"
    acronym: Literal["RH"] = "RH"
    id: Literal["189"] = "189"


class _Rl(_BrainStructureModel):
    """Model RL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Rostral linear nucleus raphe"] = "Rostral linear nucleus raphe"
    acronym: Literal["RL"] = "RL"
    id: Literal["197"] = "197"


class _Visrl1(_BrainStructureModel):
    """Model VISrl1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Rostrolateral area, layer 1"] = "Rostrolateral area, layer 1"
    acronym: Literal["VISrl1"] = "VISrl1"
    id: Literal["312782604"] = "312782604"


class _Visrl2_3(_BrainStructureModel):
    """Model VISrl2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Rostrolateral area, layer 2/3"] = "Rostrolateral area, layer 2/3"
    acronym: Literal["VISrl2/3"] = "VISrl2/3"
    id: Literal["312782608"] = "312782608"


class _Visrl4(_BrainStructureModel):
    """Model VISrl4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Rostrolateral area, layer 4"] = "Rostrolateral area, layer 4"
    acronym: Literal["VISrl4"] = "VISrl4"
    id: Literal["312782612"] = "312782612"


class _Visrl5(_BrainStructureModel):
    """Model VISrl5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Rostrolateral area, layer 5"] = "Rostrolateral area, layer 5"
    acronym: Literal["VISrl5"] = "VISrl5"
    id: Literal["312782616"] = "312782616"


class _Visrl6A(_BrainStructureModel):
    """Model VISrl6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Rostrolateral area, layer 6a"] = "Rostrolateral area, layer 6a"
    acronym: Literal["VISrl6a"] = "VISrl6a"
    id: Literal["312782620"] = "312782620"


class _Visrl6B(_BrainStructureModel):
    """Model VISrl6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Rostrolateral area, layer 6b"] = "Rostrolateral area, layer 6b"
    acronym: Literal["VISrl6b"] = "VISrl6b"
    id: Literal["312782624"] = "312782624"


class _Visrl(_BrainStructureModel):
    """Model VISrl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Rostrolateral visual area"] = "Rostrolateral visual area"
    acronym: Literal["VISrl"] = "VISrl"
    id: Literal["417"] = "417"


class _Mos(_BrainStructureModel):
    """Model MOs"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Secondary motor area"] = "Secondary motor area"
    acronym: Literal["MOs"] = "MOs"
    id: Literal["993"] = "993"


class _Mos1(_BrainStructureModel):
    """Model MOs1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Secondary motor area, layer 1"] = "Secondary motor area, layer 1"
    acronym: Literal["MOs1"] = "MOs1"
    id: Literal["656"] = "656"


class _Mos2_3(_BrainStructureModel):
    """Model MOs2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Secondary motor area, layer 2/3"] = "Secondary motor area, layer 2/3"
    acronym: Literal["MOs2/3"] = "MOs2/3"
    id: Literal["962"] = "962"


class _Mos5(_BrainStructureModel):
    """Model MOs5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Secondary motor area, layer 5"] = "Secondary motor area, layer 5"
    acronym: Literal["MOs5"] = "MOs5"
    id: Literal["767"] = "767"


class _Mos6A(_BrainStructureModel):
    """Model MOs6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Secondary motor area, layer 6a"] = "Secondary motor area, layer 6a"
    acronym: Literal["MOs6a"] = "MOs6a"
    id: Literal["1021"] = "1021"


class _Mos6B(_BrainStructureModel):
    """Model MOs6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Secondary motor area, layer 6b"] = "Secondary motor area, layer 6b"
    acronym: Literal["MOs6b"] = "MOs6b"
    id: Literal["1085"] = "1085"


class _Sf(_BrainStructureModel):
    """Model SF"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Septofimbrial nucleus"] = "Septofimbrial nucleus"
    acronym: Literal["SF"] = "SF"
    id: Literal["310"] = "310"


class _Sh(_BrainStructureModel):
    """Model SH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Septohippocampal nucleus"] = "Septohippocampal nucleus"
    acronym: Literal["SH"] = "SH"
    id: Literal["333"] = "333"


class _Sim(_BrainStructureModel):
    """Model SIM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Simple lobule"] = "Simple lobule"
    acronym: Literal["SIM"] = "SIM"
    id: Literal["1007"] = "1007"


class _Mo(_BrainStructureModel):
    """Model MO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Somatomotor areas"] = "Somatomotor areas"
    acronym: Literal["MO"] = "MO"
    id: Literal["500"] = "500"


class _Ss(_BrainStructureModel):
    """Model SS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Somatosensory areas"] = "Somatosensory areas"
    acronym: Literal["SS"] = "SS"
    id: Literal["453"] = "453"


class _Spvc(_BrainStructureModel):
    """Model SPVC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Spinal nucleus of the trigeminal, caudal part"] = "Spinal nucleus of the trigeminal, caudal part"
    acronym: Literal["SPVC"] = "SPVC"
    id: Literal["429"] = "429"


class _Spvi(_BrainStructureModel):
    """Model SPVI"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Spinal nucleus of the trigeminal, interpolar part"] = (
        "Spinal nucleus of the trigeminal, interpolar part"
    )
    acronym: Literal["SPVI"] = "SPVI"
    id: Literal["437"] = "437"


class _Spvo(_BrainStructureModel):
    """Model SPVO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Spinal nucleus of the trigeminal, oral part"] = "Spinal nucleus of the trigeminal, oral part"
    acronym: Literal["SPVO"] = "SPVO"
    id: Literal["445"] = "445"


class _Spiv(_BrainStructureModel):
    """Model SPIV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Spinal vestibular nucleus"] = "Spinal vestibular nucleus"
    acronym: Literal["SPIV"] = "SPIV"
    id: Literal["225"] = "225"


class _Str(_BrainStructureModel):
    """Model STR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Striatum"] = "Striatum"
    acronym: Literal["STR"] = "STR"
    id: Literal["477"] = "477"


class _Strd(_BrainStructureModel):
    """Model STRd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Striatum dorsal region"] = "Striatum dorsal region"
    acronym: Literal["STRd"] = "STRd"
    id: Literal["485"] = "485"


class _Strv(_BrainStructureModel):
    """Model STRv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Striatum ventral region"] = "Striatum ventral region"
    acronym: Literal["STRv"] = "STRv"
    id: Literal["493"] = "493"


class _Samy(_BrainStructureModel):
    """Model sAMY"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Striatum-like amygdalar nuclei"] = "Striatum-like amygdalar nuclei"
    acronym: Literal["sAMY"] = "sAMY"
    id: Literal["278"] = "278"


class _Slc(_BrainStructureModel):
    """Model SLC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subceruleus nucleus"] = "Subceruleus nucleus"
    acronym: Literal["SLC"] = "SLC"
    id: Literal["350"] = "350"


class _Sco(_BrainStructureModel):
    """Model SCO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subcommissural organ"] = "Subcommissural organ"
    acronym: Literal["SCO"] = "SCO"
    id: Literal["599626923"] = "599626923"


class _Sfo(_BrainStructureModel):
    """Model SFO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subfornical organ"] = "Subfornical organ"
    acronym: Literal["SFO"] = "SFO"
    id: Literal["338"] = "338"


class _Subg(_BrainStructureModel):
    """Model SubG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subgeniculate nucleus"] = "Subgeniculate nucleus"
    acronym: Literal["SubG"] = "SubG"
    id: Literal["321"] = "321"


class _Sub(_BrainStructureModel):
    """Model SUB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subiculum"] = "Subiculum"
    acronym: Literal["SUB"] = "SUB"
    id: Literal["502"] = "502"


class _Sld(_BrainStructureModel):
    """Model SLD"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Sublaterodorsal nucleus"] = "Sublaterodorsal nucleus"
    acronym: Literal["SLD"] = "SLD"
    id: Literal["358"] = "358"


class _Smt(_BrainStructureModel):
    """Model SMT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Submedial nucleus of the thalamus"] = "Submedial nucleus of the thalamus"
    acronym: Literal["SMT"] = "SMT"
    id: Literal["366"] = "366"


class _Spa(_BrainStructureModel):
    """Model SPA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subparafascicular area"] = "Subparafascicular area"
    acronym: Literal["SPA"] = "SPA"
    id: Literal["609"] = "609"


class _Spf(_BrainStructureModel):
    """Model SPF"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subparafascicular nucleus"] = "Subparafascicular nucleus"
    acronym: Literal["SPF"] = "SPF"
    id: Literal["406"] = "406"


class _Spfm(_BrainStructureModel):
    """Model SPFm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subparafascicular nucleus, magnocellular part"] = "Subparafascicular nucleus, magnocellular part"
    acronym: Literal["SPFm"] = "SPFm"
    id: Literal["414"] = "414"


class _Spfp(_BrainStructureModel):
    """Model SPFp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subparafascicular nucleus, parvicellular part"] = "Subparafascicular nucleus, parvicellular part"
    acronym: Literal["SPFp"] = "SPFp"
    id: Literal["422"] = "422"


class _Sbpv(_BrainStructureModel):
    """Model SBPV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subparaventricular zone"] = "Subparaventricular zone"
    acronym: Literal["SBPV"] = "SBPV"
    id: Literal["347"] = "347"


class _Si(_BrainStructureModel):
    """Model SI"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Substantia innominata"] = "Substantia innominata"
    acronym: Literal["SI"] = "SI"
    id: Literal["342"] = "342"


class _Snc(_BrainStructureModel):
    """Model SNc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Substantia nigra, compact part"] = "Substantia nigra, compact part"
    acronym: Literal["SNc"] = "SNc"
    id: Literal["374"] = "374"


class _Snr(_BrainStructureModel):
    """Model SNr"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Substantia nigra, reticular part"] = "Substantia nigra, reticular part"
    acronym: Literal["SNr"] = "SNr"
    id: Literal["381"] = "381"


class _Stn(_BrainStructureModel):
    """Model STN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Subthalamic nucleus"] = "Subthalamic nucleus"
    acronym: Literal["STN"] = "STN"
    id: Literal["470"] = "470"


class _Cs(_BrainStructureModel):
    """Model CS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior central nucleus raphe"] = "Superior central nucleus raphe"
    acronym: Literal["CS"] = "CS"
    id: Literal["679"] = "679"


class _Scm(_BrainStructureModel):
    """Model SCm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior colliculus, motor related"] = "Superior colliculus, motor related"
    acronym: Literal["SCm"] = "SCm"
    id: Literal["294"] = "294"


class _Scdg(_BrainStructureModel):
    """Model SCdg"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior colliculus, motor related, deep gray layer"] = (
        "Superior colliculus, motor related, deep gray layer"
    )
    acronym: Literal["SCdg"] = "SCdg"
    id: Literal["26"] = "26"


class _Scdw(_BrainStructureModel):
    """Model SCdw"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior colliculus, motor related, deep white layer"] = (
        "Superior colliculus, motor related, deep white layer"
    )
    acronym: Literal["SCdw"] = "SCdw"
    id: Literal["42"] = "42"


class _Scig(_BrainStructureModel):
    """Model SCig"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior colliculus, motor related, intermediate gray layer"] = (
        "Superior colliculus, motor related, intermediate gray layer"
    )
    acronym: Literal["SCig"] = "SCig"
    id: Literal["10"] = "10"


class _Sciw(_BrainStructureModel):
    """Model SCiw"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior colliculus, motor related, intermediate white layer"] = (
        "Superior colliculus, motor related, intermediate white layer"
    )
    acronym: Literal["SCiw"] = "SCiw"
    id: Literal["17"] = "17"


class _Scop(_BrainStructureModel):
    """Model SCop"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior colliculus, optic layer"] = "Superior colliculus, optic layer"
    acronym: Literal["SCop"] = "SCop"
    id: Literal["851"] = "851"


class _Scs(_BrainStructureModel):
    """Model SCs"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior colliculus, sensory related"] = "Superior colliculus, sensory related"
    acronym: Literal["SCs"] = "SCs"
    id: Literal["302"] = "302"


class _Scsg(_BrainStructureModel):
    """Model SCsg"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior colliculus, superficial gray layer"] = "Superior colliculus, superficial gray layer"
    acronym: Literal["SCsg"] = "SCsg"
    id: Literal["842"] = "842"


class _Sczo(_BrainStructureModel):
    """Model SCzo"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior colliculus, zonal layer"] = "Superior colliculus, zonal layer"
    acronym: Literal["SCzo"] = "SCzo"
    id: Literal["834"] = "834"


class _Soc(_BrainStructureModel):
    """Model SOC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior olivary complex"] = "Superior olivary complex"
    acronym: Literal["SOC"] = "SOC"
    id: Literal["398"] = "398"


class _Socl(_BrainStructureModel):
    """Model SOCl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior olivary complex, lateral part"] = "Superior olivary complex, lateral part"
    acronym: Literal["SOCl"] = "SOCl"
    id: Literal["114"] = "114"


class _Socm(_BrainStructureModel):
    """Model SOCm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior olivary complex, medial part"] = "Superior olivary complex, medial part"
    acronym: Literal["SOCm"] = "SOCm"
    id: Literal["105"] = "105"


class _Por(_BrainStructureModel):
    """Model POR"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior olivary complex, periolivary region"] = "Superior olivary complex, periolivary region"
    acronym: Literal["POR"] = "POR"
    id: Literal["122"] = "122"


class _Suv(_BrainStructureModel):
    """Model SUV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Superior vestibular nucleus"] = "Superior vestibular nucleus"
    acronym: Literal["SUV"] = "SUV"
    id: Literal["217"] = "217"


class _Sss(_BrainStructureModel):
    """Model SSs"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supplemental somatosensory area"] = "Supplemental somatosensory area"
    acronym: Literal["SSs"] = "SSs"
    id: Literal["378"] = "378"


class _Sss1(_BrainStructureModel):
    """Model SSs1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supplemental somatosensory area, layer 1"] = "Supplemental somatosensory area, layer 1"
    acronym: Literal["SSs1"] = "SSs1"
    id: Literal["873"] = "873"


class _Sss2_3(_BrainStructureModel):
    """Model SSs2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supplemental somatosensory area, layer 2/3"] = "Supplemental somatosensory area, layer 2/3"
    acronym: Literal["SSs2/3"] = "SSs2/3"
    id: Literal["806"] = "806"


class _Sss4(_BrainStructureModel):
    """Model SSs4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supplemental somatosensory area, layer 4"] = "Supplemental somatosensory area, layer 4"
    acronym: Literal["SSs4"] = "SSs4"
    id: Literal["1035"] = "1035"


class _Sss5(_BrainStructureModel):
    """Model SSs5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supplemental somatosensory area, layer 5"] = "Supplemental somatosensory area, layer 5"
    acronym: Literal["SSs5"] = "SSs5"
    id: Literal["1090"] = "1090"


class _Sss6A(_BrainStructureModel):
    """Model SSs6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supplemental somatosensory area, layer 6a"] = "Supplemental somatosensory area, layer 6a"
    acronym: Literal["SSs6a"] = "SSs6a"
    id: Literal["862"] = "862"


class _Sss6B(_BrainStructureModel):
    """Model SSs6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supplemental somatosensory area, layer 6b"] = "Supplemental somatosensory area, layer 6b"
    acronym: Literal["SSs6b"] = "SSs6b"
    id: Literal["893"] = "893"


class _Sch(_BrainStructureModel):
    """Model SCH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Suprachiasmatic nucleus"] = "Suprachiasmatic nucleus"
    acronym: Literal["SCH"] = "SCH"
    id: Literal["286"] = "286"


class _Sgn(_BrainStructureModel):
    """Model SGN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Suprageniculate nucleus"] = "Suprageniculate nucleus"
    acronym: Literal["SGN"] = "SGN"
    id: Literal["325"] = "325"


class _Sg(_BrainStructureModel):
    """Model SG"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supragenual nucleus"] = "Supragenual nucleus"
    acronym: Literal["SG"] = "SG"
    id: Literal["318"] = "318"


class _Sum(_BrainStructureModel):
    """Model SUM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supramammillary nucleus"] = "Supramammillary nucleus"
    acronym: Literal["SUM"] = "SUM"
    id: Literal["525"] = "525"


class _Su3(_BrainStructureModel):
    """Model Su3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supraoculomotor periaqueductal gray"] = "Supraoculomotor periaqueductal gray"
    acronym: Literal["Su3"] = "Su3"
    id: Literal["614454277"] = "614454277"


class _So(_BrainStructureModel):
    """Model SO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supraoptic nucleus"] = "Supraoptic nucleus"
    acronym: Literal["SO"] = "SO"
    id: Literal["390"] = "390"


class _Sut(_BrainStructureModel):
    """Model SUT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Supratrigeminal nucleus"] = "Supratrigeminal nucleus"
    acronym: Literal["SUT"] = "SUT"
    id: Literal["534"] = "534"


class _Tt(_BrainStructureModel):
    """Model TT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Taenia tecta"] = "Taenia tecta"
    acronym: Literal["TT"] = "TT"
    id: Literal["589"] = "589"


class _Ttd(_BrainStructureModel):
    """Model TTd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Taenia tecta, dorsal part"] = "Taenia tecta, dorsal part"
    acronym: Literal["TTd"] = "TTd"
    id: Literal["597"] = "597"


class _Ttv(_BrainStructureModel):
    """Model TTv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Taenia tecta, ventral part"] = "Taenia tecta, ventral part"
    acronym: Literal["TTv"] = "TTv"
    id: Literal["605"] = "605"


class _Trn(_BrainStructureModel):
    """Model TRN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Tegmental reticular nucleus"] = "Tegmental reticular nucleus"
    acronym: Literal["TRN"] = "TRN"
    id: Literal["574"] = "574"


class _Tea(_BrainStructureModel):
    """Model TEa"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Temporal association areas"] = "Temporal association areas"
    acronym: Literal["TEa"] = "TEa"
    id: Literal["541"] = "541"


class _Tea1(_BrainStructureModel):
    """Model TEa1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Temporal association areas, layer 1"] = "Temporal association areas, layer 1"
    acronym: Literal["TEa1"] = "TEa1"
    id: Literal["97"] = "97"


class _Tea2_3(_BrainStructureModel):
    """Model TEa2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Temporal association areas, layer 2/3"] = "Temporal association areas, layer 2/3"
    acronym: Literal["TEa2/3"] = "TEa2/3"
    id: Literal["1127"] = "1127"


class _Tea4(_BrainStructureModel):
    """Model TEa4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Temporal association areas, layer 4"] = "Temporal association areas, layer 4"
    acronym: Literal["TEa4"] = "TEa4"
    id: Literal["234"] = "234"


class _Tea5(_BrainStructureModel):
    """Model TEa5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Temporal association areas, layer 5"] = "Temporal association areas, layer 5"
    acronym: Literal["TEa5"] = "TEa5"
    id: Literal["289"] = "289"


class _Tea6A(_BrainStructureModel):
    """Model TEa6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Temporal association areas, layer 6a"] = "Temporal association areas, layer 6a"
    acronym: Literal["TEa6a"] = "TEa6a"
    id: Literal["729"] = "729"


class _Tea6B(_BrainStructureModel):
    """Model TEa6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Temporal association areas, layer 6b"] = "Temporal association areas, layer 6b"
    acronym: Literal["TEa6b"] = "TEa6b"
    id: Literal["786"] = "786"


class _Th(_BrainStructureModel):
    """Model TH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Thalamus"] = "Thalamus"
    acronym: Literal["TH"] = "TH"
    id: Literal["549"] = "549"


class _Dorpm(_BrainStructureModel):
    """Model DORpm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Thalamus, polymodal association cortex related"] = "Thalamus, polymodal association cortex related"
    acronym: Literal["DORpm"] = "DORpm"
    id: Literal["856"] = "856"


class _Dorsm(_BrainStructureModel):
    """Model DORsm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Thalamus, sensory-motor cortex related"] = "Thalamus, sensory-motor cortex related"
    acronym: Literal["DORsm"] = "DORsm"
    id: Literal["864"] = "864"


class _Trs(_BrainStructureModel):
    """Model TRS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Triangular nucleus of septum"] = "Triangular nucleus of septum"
    acronym: Literal["TRS"] = "TRS"
    id: Literal["581"] = "581"


class _Iv(_BrainStructureModel):
    """Model IV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Trochlear nucleus"] = "Trochlear nucleus"
    acronym: Literal["IV"] = "IV"
    id: Literal["115"] = "115"


class _Tu(_BrainStructureModel):
    """Model TU"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Tuberal nucleus"] = "Tuberal nucleus"
    acronym: Literal["TU"] = "TU"
    id: Literal["614"] = "614"


class _Tm(_BrainStructureModel):
    """Model TM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Tuberomammillary nucleus"] = "Tuberomammillary nucleus"
    acronym: Literal["TM"] = "TM"
    id: Literal["557"] = "557"


class _Tmd(_BrainStructureModel):
    """Model TMd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Tuberomammillary nucleus, dorsal part"] = "Tuberomammillary nucleus, dorsal part"
    acronym: Literal["TMd"] = "TMd"
    id: Literal["1126"] = "1126"


class _Tmv(_BrainStructureModel):
    """Model TMv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Tuberomammillary nucleus, ventral part"] = "Tuberomammillary nucleus, ventral part"
    acronym: Literal["TMv"] = "TMv"
    id: Literal["1"] = "1"


class _Uvu(_BrainStructureModel):
    """Model UVU"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Uvula (IX)"] = "Uvula (IX)"
    acronym: Literal["UVU"] = "UVU"
    id: Literal["957"] = "957"


class _Ov(_BrainStructureModel):
    """Model OV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Vascular organ of the lamina terminalis"] = "Vascular organ of the lamina terminalis"
    acronym: Literal["OV"] = "OV"
    id: Literal["763"] = "763"


class _Val(_BrainStructureModel):
    """Model VAL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral anterior-lateral complex of the thalamus"] = (
        "Ventral anterior-lateral complex of the thalamus"
    )
    acronym: Literal["VAL"] = "VAL"
    id: Literal["629"] = "629"


class _Audv(_BrainStructureModel):
    """Model AUDv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral auditory area"] = "Ventral auditory area"
    acronym: Literal["AUDv"] = "AUDv"
    id: Literal["1018"] = "1018"


class _Audv1(_BrainStructureModel):
    """Model AUDv1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral auditory area, layer 1"] = "Ventral auditory area, layer 1"
    acronym: Literal["AUDv1"] = "AUDv1"
    id: Literal["959"] = "959"


class _Audv2_3(_BrainStructureModel):
    """Model AUDv2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral auditory area, layer 2/3"] = "Ventral auditory area, layer 2/3"
    acronym: Literal["AUDv2/3"] = "AUDv2/3"
    id: Literal["755"] = "755"


class _Audv4(_BrainStructureModel):
    """Model AUDv4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral auditory area, layer 4"] = "Ventral auditory area, layer 4"
    acronym: Literal["AUDv4"] = "AUDv4"
    id: Literal["990"] = "990"


class _Audv5(_BrainStructureModel):
    """Model AUDv5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral auditory area, layer 5"] = "Ventral auditory area, layer 5"
    acronym: Literal["AUDv5"] = "AUDv5"
    id: Literal["1023"] = "1023"


class _Audv6A(_BrainStructureModel):
    """Model AUDv6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral auditory area, layer 6a"] = "Ventral auditory area, layer 6a"
    acronym: Literal["AUDv6a"] = "AUDv6a"
    id: Literal["520"] = "520"


class _Audv6B(_BrainStructureModel):
    """Model AUDv6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral auditory area, layer 6b"] = "Ventral auditory area, layer 6b"
    acronym: Literal["AUDv6b"] = "AUDv6b"
    id: Literal["598"] = "598"


class _Vco(_BrainStructureModel):
    """Model VCO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral cochlear nucleus"] = "Ventral cochlear nucleus"
    acronym: Literal["VCO"] = "VCO"
    id: Literal["101"] = "101"


class _Vent(_BrainStructureModel):
    """Model VENT"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral group of the dorsal thalamus"] = "Ventral group of the dorsal thalamus"
    acronym: Literal["VENT"] = "VENT"
    id: Literal["637"] = "637"


class _Vm(_BrainStructureModel):
    """Model VM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral medial nucleus of the thalamus"] = "Ventral medial nucleus of the thalamus"
    acronym: Literal["VM"] = "VM"
    id: Literal["685"] = "685"


class _Lgv(_BrainStructureModel):
    """Model LGv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral part of the lateral geniculate complex"] = "Ventral part of the lateral geniculate complex"
    acronym: Literal["LGv"] = "LGv"
    id: Literal["178"] = "178"


class _Vp(_BrainStructureModel):
    """Model VP"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral posterior complex of the thalamus"] = "Ventral posterior complex of the thalamus"
    acronym: Literal["VP"] = "VP"
    id: Literal["709"] = "709"


class _Vpl(_BrainStructureModel):
    """Model VPL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral posterolateral nucleus of the thalamus"] = "Ventral posterolateral nucleus of the thalamus"
    acronym: Literal["VPL"] = "VPL"
    id: Literal["718"] = "718"


class _Vplpc(_BrainStructureModel):
    """Model VPLpc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral posterolateral nucleus of the thalamus, parvicellular part"] = (
        "Ventral posterolateral nucleus of the thalamus, parvicellular part"
    )
    acronym: Literal["VPLpc"] = "VPLpc"
    id: Literal["725"] = "725"


class _Vpm(_BrainStructureModel):
    """Model VPM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral posteromedial nucleus of the thalamus"] = "Ventral posteromedial nucleus of the thalamus"
    acronym: Literal["VPM"] = "VPM"
    id: Literal["733"] = "733"


class _Vpmpc(_BrainStructureModel):
    """Model VPMpc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral posteromedial nucleus of the thalamus, parvicellular part"] = (
        "Ventral posteromedial nucleus of the thalamus, parvicellular part"
    )
    acronym: Literal["VPMpc"] = "VPMpc"
    id: Literal["741"] = "741"


class _Pmv(_BrainStructureModel):
    """Model PMv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral premammillary nucleus"] = "Ventral premammillary nucleus"
    acronym: Literal["PMv"] = "PMv"
    id: Literal["1004"] = "1004"


class _Vta(_BrainStructureModel):
    """Model VTA"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral tegmental area"] = "Ventral tegmental area"
    acronym: Literal["VTA"] = "VTA"
    id: Literal["749"] = "749"


class _Vtn(_BrainStructureModel):
    """Model VTN"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventral tegmental nucleus"] = "Ventral tegmental nucleus"
    acronym: Literal["VTN"] = "VTN"
    id: Literal["757"] = "757"


class _Vlpo(_BrainStructureModel):
    """Model VLPO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventrolateral preoptic nucleus"] = "Ventrolateral preoptic nucleus"
    acronym: Literal["VLPO"] = "VLPO"
    id: Literal["689"] = "689"


class _Vmh(_BrainStructureModel):
    """Model VMH"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventromedial hypothalamic nucleus"] = "Ventromedial hypothalamic nucleus"
    acronym: Literal["VMH"] = "VMH"
    id: Literal["693"] = "693"


class _Vmpo(_BrainStructureModel):
    """Model VMPO"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Ventromedial preoptic nucleus"] = "Ventromedial preoptic nucleus"
    acronym: Literal["VMPO"] = "VMPO"
    id: Literal["576073699"] = "576073699"


class _Verm(_BrainStructureModel):
    """Model VERM"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Vermal regions"] = "Vermal regions"
    acronym: Literal["VERM"] = "VERM"
    id: Literal["645"] = "645"


class _Vnc(_BrainStructureModel):
    """Model VNC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Vestibular nuclei"] = "Vestibular nuclei"
    acronym: Literal["VNC"] = "VNC"
    id: Literal["701"] = "701"


class _Vecb(_BrainStructureModel):
    """Model VeCB"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Vestibulocerebellar nucleus"] = "Vestibulocerebellar nucleus"
    acronym: Literal["VeCB"] = "VeCB"
    id: Literal["589508455"] = "589508455"


class _Visc(_BrainStructureModel):
    """Model VISC"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Visceral area"] = "Visceral area"
    acronym: Literal["VISC"] = "VISC"
    id: Literal["677"] = "677"


class _Visc1(_BrainStructureModel):
    """Model VISC1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Visceral area, layer 1"] = "Visceral area, layer 1"
    acronym: Literal["VISC1"] = "VISC1"
    id: Literal["897"] = "897"


class _Visc2_3(_BrainStructureModel):
    """Model VISC2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Visceral area, layer 2/3"] = "Visceral area, layer 2/3"
    acronym: Literal["VISC2/3"] = "VISC2/3"
    id: Literal["1106"] = "1106"


class _Visc4(_BrainStructureModel):
    """Model VISC4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Visceral area, layer 4"] = "Visceral area, layer 4"
    acronym: Literal["VISC4"] = "VISC4"
    id: Literal["1010"] = "1010"


class _Visc5(_BrainStructureModel):
    """Model VISC5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Visceral area, layer 5"] = "Visceral area, layer 5"
    acronym: Literal["VISC5"] = "VISC5"
    id: Literal["1058"] = "1058"


class _Visc6A(_BrainStructureModel):
    """Model VISC6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Visceral area, layer 6a"] = "Visceral area, layer 6a"
    acronym: Literal["VISC6a"] = "VISC6a"
    id: Literal["857"] = "857"


class _Visc6B(_BrainStructureModel):
    """Model VISC6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Visceral area, layer 6b"] = "Visceral area, layer 6b"
    acronym: Literal["VISC6b"] = "VISC6b"
    id: Literal["849"] = "849"


class _Vis(_BrainStructureModel):
    """Model VIS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Visual areas"] = "Visual areas"
    acronym: Literal["VIS"] = "VIS"
    id: Literal["669"] = "669"


class _Xi(_BrainStructureModel):
    """Model Xi"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Xiphoid thalamic nucleus"] = "Xiphoid thalamic nucleus"
    acronym: Literal["Xi"] = "Xi"
    id: Literal["560581559"] = "560581559"


class _Zi(_BrainStructureModel):
    """Model ZI"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["Zona incerta"] = "Zona incerta"
    acronym: Literal["ZI"] = "ZI"
    id: Literal["797"] = "797"


class _Alv(_BrainStructureModel):
    """Model alv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["alveus"] = "alveus"
    acronym: Literal["alv"] = "alv"
    id: Literal["466"] = "466"


class _Amc(_BrainStructureModel):
    """Model amc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["amygdalar capsule"] = "amygdalar capsule"
    acronym: Literal["amc"] = "amc"
    id: Literal["884"] = "884"


class _Aco(_BrainStructureModel):
    """Model aco"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["anterior commissure, olfactory limb"] = "anterior commissure, olfactory limb"
    acronym: Literal["aco"] = "aco"
    id: Literal["900"] = "900"


class _Act(_BrainStructureModel):
    """Model act"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["anterior commissure, temporal limb"] = "anterior commissure, temporal limb"
    acronym: Literal["act"] = "act"
    id: Literal["908"] = "908"


class _Arb(_BrainStructureModel):
    """Model arb"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["arbor vitae"] = "arbor vitae"
    acronym: Literal["arb"] = "arb"
    id: Literal["728"] = "728"


class _Ar(_BrainStructureModel):
    """Model ar"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["auditory radiation"] = "auditory radiation"
    acronym: Literal["ar"] = "ar"
    id: Literal["484682524"] = "484682524"


class _Bic(_BrainStructureModel):
    """Model bic"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["brachium of the inferior colliculus"] = "brachium of the inferior colliculus"
    acronym: Literal["bic"] = "bic"
    id: Literal["482"] = "482"


class _Bsc(_BrainStructureModel):
    """Model bsc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["brachium of the superior colliculus"] = "brachium of the superior colliculus"
    acronym: Literal["bsc"] = "bsc"
    id: Literal["916"] = "916"


class _C(_BrainStructureModel):
    """Model c"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["central canal, spinal cord/medulla"] = "central canal, spinal cord/medulla"
    acronym: Literal["c"] = "c"
    id: Literal["164"] = "164"


class _Cpd(_BrainStructureModel):
    """Model cpd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cerebal peduncle"] = "cerebal peduncle"
    acronym: Literal["cpd"] = "cpd"
    id: Literal["924"] = "924"


class _Cbc(_BrainStructureModel):
    """Model cbc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cerebellar commissure"] = "cerebellar commissure"
    acronym: Literal["cbc"] = "cbc"
    id: Literal["744"] = "744"


class _Cbp(_BrainStructureModel):
    """Model cbp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cerebellar peduncles"] = "cerebellar peduncles"
    acronym: Literal["cbp"] = "cbp"
    id: Literal["752"] = "752"


class _Cbf(_BrainStructureModel):
    """Model cbf"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cerebellum related fiber tracts"] = "cerebellum related fiber tracts"
    acronym: Literal["cbf"] = "cbf"
    id: Literal["960"] = "960"


class _Aq(_BrainStructureModel):
    """Model AQ"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cerebral aqueduct"] = "cerebral aqueduct"
    acronym: Literal["AQ"] = "AQ"
    id: Literal["140"] = "140"


class _Epsc(_BrainStructureModel):
    """Model epsc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cerebral nuclei related"] = "cerebral nuclei related"
    acronym: Literal["epsc"] = "epsc"
    id: Literal["760"] = "760"


class _Mfbc(_BrainStructureModel):
    """Model mfbc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cerebrum related"] = "cerebrum related"
    acronym: Literal["mfbc"] = "mfbc"
    id: Literal["768"] = "768"


class _Cett(_BrainStructureModel):
    """Model cett"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cervicothalamic tract"] = "cervicothalamic tract"
    acronym: Literal["cett"] = "cett"
    id: Literal["932"] = "932"


class _Chpl(_BrainStructureModel):
    """Model chpl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["choroid plexus"] = "choroid plexus"
    acronym: Literal["chpl"] = "chpl"
    id: Literal["108"] = "108"


class _Cing(_BrainStructureModel):
    """Model cing"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cingulum bundle"] = "cingulum bundle"
    acronym: Literal["cing"] = "cing"
    id: Literal["940"] = "940"


class _Cviiin(_BrainStructureModel):
    """Model cVIIIn"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cochlear nerve"] = "cochlear nerve"
    acronym: Literal["cVIIIn"] = "cVIIIn"
    id: Literal["948"] = "948"


class _Fx(_BrainStructureModel):
    """Model fx"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["columns of the fornix"] = "columns of the fornix"
    acronym: Literal["fx"] = "fx"
    id: Literal["436"] = "436"


class _Stc(_BrainStructureModel):
    """Model stc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["commissural branch of stria terminalis"] = "commissural branch of stria terminalis"
    acronym: Literal["stc"] = "stc"
    id: Literal["484682528"] = "484682528"


class _Cc(_BrainStructureModel):
    """Model cc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["corpus callosum"] = "corpus callosum"
    acronym: Literal["cc"] = "cc"
    id: Literal["776"] = "776"


class _Fa(_BrainStructureModel):
    """Model fa"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["corpus callosum, anterior forceps"] = "corpus callosum, anterior forceps"
    acronym: Literal["fa"] = "fa"
    id: Literal["956"] = "956"


class _Ccb(_BrainStructureModel):
    """Model ccb"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["corpus callosum, body"] = "corpus callosum, body"
    acronym: Literal["ccb"] = "ccb"
    id: Literal["484682516"] = "484682516"


class _Ee(_BrainStructureModel):
    """Model ee"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["corpus callosum, extreme capsule"] = "corpus callosum, extreme capsule"
    acronym: Literal["ee"] = "ee"
    id: Literal["964"] = "964"


class _Fp(_BrainStructureModel):
    """Model fp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["corpus callosum, posterior forceps"] = "corpus callosum, posterior forceps"
    acronym: Literal["fp"] = "fp"
    id: Literal["971"] = "971"


class _Ccs(_BrainStructureModel):
    """Model ccs"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["corpus callosum, splenium"] = "corpus callosum, splenium"
    acronym: Literal["ccs"] = "ccs"
    id: Literal["986"] = "986"


class _Cst(_BrainStructureModel):
    """Model cst"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["corticospinal tract"] = "corticospinal tract"
    acronym: Literal["cst"] = "cst"
    id: Literal["784"] = "784"


class _Cne(_BrainStructureModel):
    """Model cne"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cranial nerves"] = "cranial nerves"
    acronym: Literal["cne"] = "cne"
    id: Literal["967"] = "967"


class _Tspc(_BrainStructureModel):
    """Model tspc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["crossed tectospinal pathway"] = "crossed tectospinal pathway"
    acronym: Literal["tspc"] = "tspc"
    id: Literal["1043"] = "1043"


class _Cuf(_BrainStructureModel):
    """Model cuf"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["cuneate fascicle"] = "cuneate fascicle"
    acronym: Literal["cuf"] = "cuf"
    id: Literal["380"] = "380"


class _Tspd(_BrainStructureModel):
    """Model tspd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["direct tectospinal pathway"] = "direct tectospinal pathway"
    acronym: Literal["tspd"] = "tspd"
    id: Literal["1051"] = "1051"


class _Dtd(_BrainStructureModel):
    """Model dtd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["doral tegmental decussation"] = "doral tegmental decussation"
    acronym: Literal["dtd"] = "dtd"
    id: Literal["1060"] = "1060"


class _Das(_BrainStructureModel):
    """Model das"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["dorsal acoustic stria"] = "dorsal acoustic stria"
    acronym: Literal["das"] = "das"
    id: Literal["506"] = "506"


class _Dc(_BrainStructureModel):
    """Model dc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["dorsal column"] = "dorsal column"
    acronym: Literal["dc"] = "dc"
    id: Literal["514"] = "514"


class _Df(_BrainStructureModel):
    """Model df"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["dorsal fornix"] = "dorsal fornix"
    acronym: Literal["df"] = "df"
    id: Literal["530"] = "530"


class _Dhc(_BrainStructureModel):
    """Model dhc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["dorsal hippocampal commissure"] = "dorsal hippocampal commissure"
    acronym: Literal["dhc"] = "dhc"
    id: Literal["443"] = "443"


class _Lotd(_BrainStructureModel):
    """Model lotd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["dorsal limb"] = "dorsal limb"
    acronym: Literal["lotd"] = "lotd"
    id: Literal["538"] = "538"


class _Drt(_BrainStructureModel):
    """Model drt"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["dorsal roots"] = "dorsal roots"
    acronym: Literal["drt"] = "drt"
    id: Literal["792"] = "792"


class _Sctd(_BrainStructureModel):
    """Model sctd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["dorsal spinocerebellar tract"] = "dorsal spinocerebellar tract"
    acronym: Literal["sctd"] = "sctd"
    id: Literal["553"] = "553"


class _Mfbse(_BrainStructureModel):
    """Model mfbse"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["epithalamus related"] = "epithalamus related"
    acronym: Literal["mfbse"] = "mfbse"
    id: Literal["1083"] = "1083"


class _Ec(_BrainStructureModel):
    """Model ec"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["external capsule"] = "external capsule"
    acronym: Literal["ec"] = "ec"
    id: Literal["579"] = "579"


class _Em(_BrainStructureModel):
    """Model em"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["external medullary lamina of the thalamus"] = "external medullary lamina of the thalamus"
    acronym: Literal["em"] = "em"
    id: Literal["1092"] = "1092"


class _Eps(_BrainStructureModel):
    """Model eps"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["extrapyramidal fiber systems"] = "extrapyramidal fiber systems"
    acronym: Literal["eps"] = "eps"
    id: Literal["1000"] = "1000"


class _Viin(_BrainStructureModel):
    """Model VIIn"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["facial nerve"] = "facial nerve"
    acronym: Literal["VIIn"] = "VIIn"
    id: Literal["798"] = "798"


class _Fr(_BrainStructureModel):
    """Model fr"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["fasciculus retroflexus"] = "fasciculus retroflexus"
    acronym: Literal["fr"] = "fr"
    id: Literal["595"] = "595"


class _Fiber_Tracts(_BrainStructureModel):
    """Model fiber tracts"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["fiber tracts"] = "fiber tracts"
    acronym: Literal["fiber tracts"] = "fiber tracts"
    id: Literal["1009"] = "1009"


class _Fi(_BrainStructureModel):
    """Model fi"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["fimbria"] = "fimbria"
    acronym: Literal["fi"] = "fi"
    id: Literal["603"] = "603"


class _Fxs(_BrainStructureModel):
    """Model fxs"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["fornix system"] = "fornix system"
    acronym: Literal["fxs"] = "fxs"
    id: Literal["1099"] = "1099"


class _V4(_BrainStructureModel):
    """Model V4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["fourth ventricle"] = "fourth ventricle"
    acronym: Literal["V4"] = "V4"
    id: Literal["145"] = "145"


class _Ccg(_BrainStructureModel):
    """Model ccg"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["genu of corpus callosum"] = "genu of corpus callosum"
    acronym: Literal["ccg"] = "ccg"
    id: Literal["1108"] = "1108"


class _Gviin(_BrainStructureModel):
    """Model gVIIn"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["genu of the facial nerve"] = "genu of the facial nerve"
    acronym: Literal["gVIIn"] = "gVIIn"
    id: Literal["1116"] = "1116"


class _Hbc(_BrainStructureModel):
    """Model hbc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["habenular commissure"] = "habenular commissure"
    acronym: Literal["hbc"] = "hbc"
    id: Literal["611"] = "611"


class _Hc(_BrainStructureModel):
    """Model hc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["hippocampal commissures"] = "hippocampal commissures"
    acronym: Literal["hc"] = "hc"
    id: Literal["618"] = "618"


class _Mfsbshy(_BrainStructureModel):
    """Model mfsbshy"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["hypothalamus related"] = "hypothalamus related"
    acronym: Literal["mfsbshy"] = "mfsbshy"
    id: Literal["824"] = "824"


class _Icp(_BrainStructureModel):
    """Model icp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["inferior cerebellar peduncle"] = "inferior cerebellar peduncle"
    acronym: Literal["icp"] = "icp"
    id: Literal["1123"] = "1123"


class _Cic(_BrainStructureModel):
    """Model cic"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["inferior colliculus commissure"] = "inferior colliculus commissure"
    acronym: Literal["cic"] = "cic"
    id: Literal["633"] = "633"


class _Int(_BrainStructureModel):
    """Model int"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["internal capsule"] = "internal capsule"
    acronym: Literal["int"] = "int"
    id: Literal["6"] = "6"


class _Lfbs(_BrainStructureModel):
    """Model lfbs"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["lateral forebrain bundle system"] = "lateral forebrain bundle system"
    acronym: Literal["lfbs"] = "lfbs"
    id: Literal["983"] = "983"


class _Ll(_BrainStructureModel):
    """Model ll"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["lateral lemniscus"] = "lateral lemniscus"
    acronym: Literal["ll"] = "ll"
    id: Literal["658"] = "658"


class _Lot(_BrainStructureModel):
    """Model lot"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["lateral olfactory tract, body"] = "lateral olfactory tract, body"
    acronym: Literal["lot"] = "lot"
    id: Literal["665"] = "665"


class _Lotg(_BrainStructureModel):
    """Model lotg"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["lateral olfactory tract, general"] = "lateral olfactory tract, general"
    acronym: Literal["lotg"] = "lotg"
    id: Literal["21"] = "21"


class _V4R(_BrainStructureModel):
    """Model V4r"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["lateral recess"] = "lateral recess"
    acronym: Literal["V4r"] = "V4r"
    id: Literal["153"] = "153"


class _Vl(_BrainStructureModel):
    """Model VL"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["lateral ventricle"] = "lateral ventricle"
    acronym: Literal["VL"] = "VL"
    id: Literal["81"] = "81"


class _Mp(_BrainStructureModel):
    """Model mp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["mammillary peduncle"] = "mammillary peduncle"
    acronym: Literal["mp"] = "mp"
    id: Literal["673"] = "673"


class _Mfbsma(_BrainStructureModel):
    """Model mfbsma"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["mammillary related"] = "mammillary related"
    acronym: Literal["mfbsma"] = "mfbsma"
    id: Literal["46"] = "46"


class _Mtg(_BrainStructureModel):
    """Model mtg"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["mammillotegmental tract"] = "mammillotegmental tract"
    acronym: Literal["mtg"] = "mtg"
    id: Literal["681"] = "681"


class _Mtt(_BrainStructureModel):
    """Model mtt"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["mammillothalamic tract"] = "mammillothalamic tract"
    acronym: Literal["mtt"] = "mtt"
    id: Literal["690"] = "690"


class _Mct(_BrainStructureModel):
    """Model mct"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["medial corticohypothalamic tract"] = "medial corticohypothalamic tract"
    acronym: Literal["mct"] = "mct"
    id: Literal["428"] = "428"


class _Mfb(_BrainStructureModel):
    """Model mfb"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["medial forebrain bundle"] = "medial forebrain bundle"
    acronym: Literal["mfb"] = "mfb"
    id: Literal["54"] = "54"


class _Mfbs(_BrainStructureModel):
    """Model mfbs"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["medial forebrain bundle system"] = "medial forebrain bundle system"
    acronym: Literal["mfbs"] = "mfbs"
    id: Literal["991"] = "991"


class _Ml(_BrainStructureModel):
    """Model ml"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["medial lemniscus"] = "medial lemniscus"
    acronym: Literal["ml"] = "ml"
    id: Literal["697"] = "697"


class _Mlf(_BrainStructureModel):
    """Model mlf"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["medial longitudinal fascicle"] = "medial longitudinal fascicle"
    acronym: Literal["mlf"] = "mlf"
    id: Literal["62"] = "62"


class _Mcp(_BrainStructureModel):
    """Model mcp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["middle cerebellar peduncle"] = "middle cerebellar peduncle"
    acronym: Literal["mcp"] = "mcp"
    id: Literal["78"] = "78"


class _Mov(_BrainStructureModel):
    """Model moV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["motor root of the trigeminal nerve"] = "motor root of the trigeminal nerve"
    acronym: Literal["moV"] = "moV"
    id: Literal["93"] = "93"


class _Nst(_BrainStructureModel):
    """Model nst"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["nigrostriatal tract"] = "nigrostriatal tract"
    acronym: Literal["nst"] = "nst"
    id: Literal["102"] = "102"


class _Iiin(_BrainStructureModel):
    """Model IIIn"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["oculomotor nerve"] = "oculomotor nerve"
    acronym: Literal["IIIn"] = "IIIn"
    id: Literal["832"] = "832"


class _In(_BrainStructureModel):
    """Model In"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["olfactory nerve"] = "olfactory nerve"
    acronym: Literal["In"] = "In"
    id: Literal["840"] = "840"


class _Onl(_BrainStructureModel):
    """Model onl"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["olfactory nerve layer of main olfactory bulb"] = "olfactory nerve layer of main olfactory bulb"
    acronym: Literal["onl"] = "onl"
    id: Literal["1016"] = "1016"


class _Och(_BrainStructureModel):
    """Model och"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["optic chiasm"] = "optic chiasm"
    acronym: Literal["och"] = "och"
    id: Literal["117"] = "117"


class _Iin(_BrainStructureModel):
    """Model IIn"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["optic nerve"] = "optic nerve"
    acronym: Literal["IIn"] = "IIn"
    id: Literal["848"] = "848"


class _Or(_BrainStructureModel):
    """Model or"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["optic radiation"] = "optic radiation"
    acronym: Literal["or"] = "or"
    id: Literal["484682520"] = "484682520"


class _Opt(_BrainStructureModel):
    """Model opt"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["optic tract"] = "optic tract"
    acronym: Literal["opt"] = "opt"
    id: Literal["125"] = "125"


class _Fxpo(_BrainStructureModel):
    """Model fxpo"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["postcommissural fornix"] = "postcommissural fornix"
    acronym: Literal["fxpo"] = "fxpo"
    id: Literal["737"] = "737"


class _Pc(_BrainStructureModel):
    """Model pc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["posterior commissure"] = "posterior commissure"
    acronym: Literal["pc"] = "pc"
    id: Literal["158"] = "158"


class _Vispm(_BrainStructureModel):
    """Model VISpm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["posteromedial visual area"] = "posteromedial visual area"
    acronym: Literal["VISpm"] = "VISpm"
    id: Literal["533"] = "533"


class _Vispm1(_BrainStructureModel):
    """Model VISpm1"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["posteromedial visual area, layer 1"] = "posteromedial visual area, layer 1"
    acronym: Literal["VISpm1"] = "VISpm1"
    id: Literal["805"] = "805"


class _Vispm2_3(_BrainStructureModel):
    """Model VISpm2/3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["posteromedial visual area, layer 2/3"] = "posteromedial visual area, layer 2/3"
    acronym: Literal["VISpm2/3"] = "VISpm2/3"
    id: Literal["41"] = "41"


class _Vispm4(_BrainStructureModel):
    """Model VISpm4"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["posteromedial visual area, layer 4"] = "posteromedial visual area, layer 4"
    acronym: Literal["VISpm4"] = "VISpm4"
    id: Literal["501"] = "501"


class _Vispm5(_BrainStructureModel):
    """Model VISpm5"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["posteromedial visual area, layer 5"] = "posteromedial visual area, layer 5"
    acronym: Literal["VISpm5"] = "VISpm5"
    id: Literal["565"] = "565"


class _Vispm6A(_BrainStructureModel):
    """Model VISpm6a"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["posteromedial visual area, layer 6a"] = "posteromedial visual area, layer 6a"
    acronym: Literal["VISpm6a"] = "VISpm6a"
    id: Literal["257"] = "257"


class _Vispm6B(_BrainStructureModel):
    """Model VISpm6b"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["posteromedial visual area, layer 6b"] = "posteromedial visual area, layer 6b"
    acronym: Literal["VISpm6b"] = "VISpm6b"
    id: Literal["469"] = "469"


class _Pm(_BrainStructureModel):
    """Model pm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["principal mammillary tract"] = "principal mammillary tract"
    acronym: Literal["pm"] = "pm"
    id: Literal["753"] = "753"


class _Py(_BrainStructureModel):
    """Model py"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["pyramid"] = "pyramid"
    acronym: Literal["py"] = "py"
    id: Literal["190"] = "190"


class _Pyd(_BrainStructureModel):
    """Model pyd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["pyramidal decussation"] = "pyramidal decussation"
    acronym: Literal["pyd"] = "pyd"
    id: Literal["198"] = "198"


class _Root(_BrainStructureModel):
    """Model root"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["root"] = "root"
    acronym: Literal["root"] = "root"
    id: Literal["997"] = "997"


class _Rust(_BrainStructureModel):
    """Model rust"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["rubrospinal tract"] = "rubrospinal tract"
    acronym: Literal["rust"] = "rust"
    id: Literal["863"] = "863"


class _Sv(_BrainStructureModel):
    """Model sV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["sensory root of the trigeminal nerve"] = "sensory root of the trigeminal nerve"
    acronym: Literal["sV"] = "sV"
    id: Literal["229"] = "229"


class _Ts(_BrainStructureModel):
    """Model ts"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["solitary tract"] = "solitary tract"
    acronym: Literal["ts"] = "ts"
    id: Literal["237"] = "237"


class _Sptv(_BrainStructureModel):
    """Model sptV"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["spinal tract of the trigeminal nerve"] = "spinal tract of the trigeminal nerve"
    acronym: Literal["sptV"] = "sptV"
    id: Literal["794"] = "794"


class _Sm(_BrainStructureModel):
    """Model sm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["stria medullaris"] = "stria medullaris"
    acronym: Literal["sm"] = "sm"
    id: Literal["802"] = "802"


class _St(_BrainStructureModel):
    """Model st"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["stria terminalis"] = "stria terminalis"
    acronym: Literal["st"] = "st"
    id: Literal["301"] = "301"


class _Sez(_BrainStructureModel):
    """Model SEZ"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["subependymal zone"] = "subependymal zone"
    acronym: Literal["SEZ"] = "SEZ"
    id: Literal["98"] = "98"


class _Scp(_BrainStructureModel):
    """Model scp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["superior cerebelar peduncles"] = "superior cerebelar peduncles"
    acronym: Literal["scp"] = "scp"
    id: Literal["326"] = "326"


class _Dscp(_BrainStructureModel):
    """Model dscp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["superior cerebellar peduncle decussation"] = "superior cerebellar peduncle decussation"
    acronym: Literal["dscp"] = "dscp"
    id: Literal["812"] = "812"


class _Csc(_BrainStructureModel):
    """Model csc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["superior colliculus commissure"] = "superior colliculus commissure"
    acronym: Literal["csc"] = "csc"
    id: Literal["336"] = "336"


class _Scwm(_BrainStructureModel):
    """Model scwm"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["supra-callosal cerebral white matter"] = "supra-callosal cerebral white matter"
    acronym: Literal["scwm"] = "scwm"
    id: Literal["484682512"] = "484682512"


class _Sup(_BrainStructureModel):
    """Model sup"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["supraoptic commissures"] = "supraoptic commissures"
    acronym: Literal["sup"] = "sup"
    id: Literal["349"] = "349"


class _Tsp(_BrainStructureModel):
    """Model tsp"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["tectospinal pathway"] = "tectospinal pathway"
    acronym: Literal["tsp"] = "tsp"
    id: Literal["877"] = "877"


class _Lfbst(_BrainStructureModel):
    """Model lfbst"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["thalamus related"] = "thalamus related"
    acronym: Literal["lfbst"] = "lfbst"
    id: Literal["896"] = "896"


class _V3(_BrainStructureModel):
    """Model V3"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["third ventricle"] = "third ventricle"
    acronym: Literal["V3"] = "V3"
    id: Literal["129"] = "129"


class _Tb(_BrainStructureModel):
    """Model tb"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["trapezoid body"] = "trapezoid body"
    acronym: Literal["tb"] = "tb"
    id: Literal["841"] = "841"


class _Vn(_BrainStructureModel):
    """Model Vn"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["trigeminal nerve"] = "trigeminal nerve"
    acronym: Literal["Vn"] = "Vn"
    id: Literal["901"] = "901"


class _Ivn(_BrainStructureModel):
    """Model IVn"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["trochlear nerve"] = "trochlear nerve"
    acronym: Literal["IVn"] = "IVn"
    id: Literal["911"] = "911"


class _Uf(_BrainStructureModel):
    """Model uf"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["uncinate fascicle"] = "uncinate fascicle"
    acronym: Literal["uf"] = "uf"
    id: Literal["850"] = "850"


class _Xn(_BrainStructureModel):
    """Model Xn"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["vagus nerve"] = "vagus nerve"
    acronym: Literal["Xn"] = "Xn"
    id: Literal["917"] = "917"


class _Vhc(_BrainStructureModel):
    """Model vhc"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["ventral hippocampal commissure"] = "ventral hippocampal commissure"
    acronym: Literal["vhc"] = "vhc"
    id: Literal["449"] = "449"


class _Sctv(_BrainStructureModel):
    """Model sctv"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["ventral spinocerebellar tract"] = "ventral spinocerebellar tract"
    acronym: Literal["sctv"] = "sctv"
    id: Literal["866"] = "866"


class _Vtd(_BrainStructureModel):
    """Model vtd"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["ventral tegmental decussation"] = "ventral tegmental decussation"
    acronym: Literal["vtd"] = "vtd"
    id: Literal["397"] = "397"


class _Vs(_BrainStructureModel):
    """Model VS"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["ventricular systems"] = "ventricular systems"
    acronym: Literal["VS"] = "VS"
    id: Literal["73"] = "73"


class _Vviiin(_BrainStructureModel):
    """Model vVIIIn"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["vestibular nerve"] = "vestibular nerve"
    acronym: Literal["vVIIIn"] = "vVIIIn"
    id: Literal["413"] = "413"


class _Viiin(_BrainStructureModel):
    """Model VIIIn"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["vestibulocochlear nerve"] = "vestibulocochlear nerve"
    acronym: Literal["VIIIn"] = "VIIIn"
    id: Literal["933"] = "933"


class _Von(_BrainStructureModel):
    """Model von"""

    atlas: Literal["CCFv3"] = "CCFv3"
    name: Literal["vomeronasal nerve"] = "vomeronasal nerve"
    acronym: Literal["von"] = "von"
    id: Literal["949"] = "949"


class CCFStructure:
    """CCFStructure"""

    VI = _Vi()
    ACVII = _Acvii()
    AOB = _Aob()
    AOBGL = _Aobgl()
    AOBGR = _Aobgr()
    AOBMI = _Aobmi()
    ASO = _Aso()
    ACS5 = _Acs5()
    AI = _Ai()
    AID = _Aid()
    AID1 = _Aid1()
    AID2_3 = _Aid2_3()
    AID5 = _Aid5()
    AID6A = _Aid6A()
    AID6B = _Aid6B()
    AIP = _Aip()
    AIP1 = _Aip1()
    AIP2_3 = _Aip2_3()
    AIP5 = _Aip5()
    AIP6A = _Aip6A()
    AIP6B = _Aip6B()
    AIV = _Aiv()
    AIV1 = _Aiv1()
    AIV2_3 = _Aiv2_3()
    AIV5 = _Aiv5()
    AIV6A = _Aiv6A()
    AIV6B = _Aiv6B()
    CA = _Ca()
    AN = _An()
    AAA = _Aaa()
    VISA = _Visa()
    VISA1 = _Visa1()
    VISA2_3 = _Visa2_3()
    VISA4 = _Visa4()
    VISA5 = _Visa5()
    VISA6A = _Visa6A()
    VISA6B = _Visa6B()
    ACA = _Aca()
    ACAD = _Acad()
    ACAD1 = _Acad1()
    ACAD2_3 = _Acad2_3()
    ACAD5 = _Acad5()
    ACAD6A = _Acad6A()
    ACAD6B = _Acad6B()
    ACAV = _Acav()
    ACAV6A = _Acav6A()
    ACAV6B = _Acav6B()
    ACAV1 = _Acav1()
    ACAV2_3 = _Acav2_3()
    ACAV5 = _Acav5()
    ATN = _Atn()
    AHN = _Ahn()
    AON = _Aon()
    APN = _Apn()
    AT = _At()
    AD = _Ad()
    ADP = _Adp()
    VISAL = _Visal()
    VISAL1 = _Visal1()
    VISAL2_3 = _Visal2_3()
    VISAL4 = _Visal4()
    VISAL5 = _Visal5()
    VISAL6A = _Visal6A()
    VISAL6B = _Visal6B()
    AM = _Am()
    AMD = _Amd()
    AMV = _Amv()
    VISAM = _Visam()
    VISAM1 = _Visam1()
    VISAM2_3 = _Visam2_3()
    VISAM4 = _Visam4()
    VISAM5 = _Visam5()
    VISAM6A = _Visam6A()
    VISAM6B = _Visam6B()
    AV = _Av()
    AVPV = _Avpv()
    AVP = _Avp()
    ARH = _Arh()
    AP = _Ap()
    APR = _Apr()
    AUD = _Aud()
    B = _B()
    GREY = _Grey()
    BLA = _Bla()
    BLAA = _Blaa()
    BLAP = _Blap()
    BLAV = _Blav()
    BMA = _Bma()
    BMAA = _Bmaa()
    BMAP = _Bmap()
    BST = _Bst()
    BA = _Ba()
    BAC = _Bac()
    BS = _Bs()
    CP = _Cp()
    CEA = _Cea()
    CEAC = _Ceac()
    CEAL = _Ceal()
    CEAM = _Ceam()
    CL = _Cl()
    CLI = _Cli()
    CENT = _Cent()
    CM = _Cm()
    CBX = _Cbx()
    CBN = _Cbn()
    CB = _Cb()
    CTX = _Ctx()
    CNU = _Cnu()
    CH = _Ch()
    CLA = _Cla()
    CN = _Cn()
    COPY = _Copy()
    COA = _Coa()
    COAA = _Coaa()
    COAP = _Coap()
    COAPL = _Coapl()
    COAPM = _Coapm()
    CTXPL = _Ctxpl()
    CTXSP = _Ctxsp()
    ANCR1 = _Ancr1()
    ANCR2 = _Ancr2()
    CUL = _Cul()
    CU = _Cu()
    CUN = _Cun()
    DEC = _Dec()
    DG = _Dg()
    DG_SG = _Dg_Sg()
    DG_MO = _Dg_Mo()
    DG_PO = _Dg_Po()
    DN = _Dn()
    NDB = _Ndb()
    AUDD = _Audd()
    AUDD1 = _Audd1()
    AUDD2_3 = _Audd2_3()
    AUDD4 = _Audd4()
    AUDD5 = _Audd5()
    AUDD6A = _Audd6A()
    AUDD6B = _Audd6B()
    DCO = _Dco()
    DCN = _Dcn()
    DMX = _Dmx()
    DR = _Dr()
    LGD = _Lgd()
    LGD_CO = _Lgd_Co()
    LGD_IP = _Lgd_Ip()
    LGD_SH = _Lgd_Sh()
    DP = _Dp()
    PMD = _Pmd()
    DTN = _Dtn()
    DT = _Dt()
    DMH = _Dmh()
    ECT = _Ect()
    ECT1 = _Ect1()
    ECT2_3 = _Ect2_3()
    ECT5 = _Ect5()
    ECT6A = _Ect6A()
    ECT6B = _Ect6B()
    EW = _Ew()
    EP = _Ep()
    EPD = _Epd()
    EPV = _Epv()
    ENT = _Ent()
    ENTL = _Entl()
    ENTL1 = _Entl1()
    ENTL2 = _Entl2()
    ENTL3 = _Entl3()
    ENTL5 = _Entl5()
    ENTL6A = _Entl6A()
    ENTM = _Entm()
    ENTM1 = _Entm1()
    ENTM2 = _Entm2()
    ENTM3 = _Entm3()
    ENTM5 = _Entm5()
    ENTM6 = _Entm6()
    EPI = _Epi()
    ETH = _Eth()
    ECU = _Ecu()
    VII = _Vii()
    FC = _Fc()
    FN = _Fn()
    CA1 = _Ca1()
    CA2 = _Ca2()
    CA3 = _Ca3()
    FF = _Ff()
    FL = _Fl()
    FOTU = _Fotu()
    FRP = _Frp()
    FRP1 = _Frp1()
    FRP2_3 = _Frp2_3()
    FRP5 = _Frp5()
    FRP6A = _Frp6A()
    FRP6B = _Frp6B()
    FS = _Fs()
    GEND = _Gend()
    GENV = _Genv()
    GRN = _Grn()
    GPE = _Gpe()
    GPI = _Gpi()
    GR = _Gr()
    GU = _Gu()
    GU1 = _Gu1()
    GU2_3 = _Gu2_3()
    GU4 = _Gu4()
    GU5 = _Gu5()
    GU6A = _Gu6A()
    GU6B = _Gu6B()
    HEM = _Hem()
    HB = _Hb()
    HPF = _Hpf()
    HIP = _Hip()
    HATA = _Hata()
    XII = _Xii()
    LZ = _Lz()
    MEZ = _Mez()
    HY = _Hy()
    IG = _Ig()
    IC = _Ic()
    ICC = _Icc()
    ICD = _Icd()
    ICE = _Ice()
    IO = _Io()
    ISN = _Isn()
    ICB = _Icb()
    ILA = _Ila()
    ILA1 = _Ila1()
    ILA2_3 = _Ila2_3()
    ILA5 = _Ila5()
    ILA6A = _Ila6A()
    ILA6B = _Ila6B()
    IAD = _Iad()
    IAM = _Iam()
    IB = _Ib()
    IA = _Ia()
    IF = _If()
    IGL = _Igl()
    INTG = _Intg()
    IRN = _Irn()
    IMD = _Imd()
    IPN = _Ipn()
    IPA = _Ipa()
    IPC = _Ipc()
    IPDL = _Ipdl()
    IPDM = _Ipdm()
    IPI = _Ipi()
    IPL = _Ipl()
    IPR = _Ipr()
    IPRL = _Iprl()
    IP = _Ip()
    INC = _Inc()
    I5 = _I5()
    ILM = _Ilm()
    ISOCORTEX = _Isocortex()
    KF = _Kf()
    LA = _La()
    LD = _Ld()
    LAT = _Lat()
    LH = _Lh()
    LHA = _Lha()
    LM = _Lm()
    LP = _Lp()
    LPO = _Lpo()
    LRN = _Lrn()
    LRNM = _Lrnm()
    LRNP = _Lrnp()
    LSX = _Lsx()
    LS = _Ls()
    LSC = _Lsc()
    LSR = _Lsr()
    LSV = _Lsv()
    LT = _Lt()
    LAV = _Lav()
    VISL = _Visl()
    VISL1 = _Visl1()
    VISL2_3 = _Visl2_3()
    VISL4 = _Visl4()
    VISL5 = _Visl5()
    VISL6A = _Visl6A()
    VISL6B = _Visl6B()
    LDT = _Ldt()
    VISLI = _Visli()
    VISLI1 = _Visli1()
    VISLI2_3 = _Visli2_3()
    VISLI4 = _Visli4()
    VISLI5 = _Visli5()
    VISLI6A = _Visli6A()
    VISLI6B = _Visli6B()
    LIN = _Lin()
    LING = _Ling()
    CENT2 = _Cent2()
    CENT3 = _Cent3()
    CUL4__5 = _Cul4_5()
    LC = _Lc()
    MA = _Ma()
    MARN = _Marn()
    MOB = _Mob()
    MBO = _Mbo()
    MA3 = _Ma3()
    MEA = _Mea()
    MG = _Mg()
    MGD = _Mgd()
    MGM = _Mgm()
    MGV = _Mgv()
    MED = _Med()
    MH = _Mh()
    MM = _Mm()
    MMD = _Mmd()
    MML = _Mml()
    MMM = _Mmm()
    MMME = _Mmme()
    MMP = _Mmp()
    MPO = _Mpo()
    MPN = _Mpn()
    MPT = _Mpt()
    MSC = _Msc()
    MS = _Ms()
    MT = _Mt()
    MV = _Mv()
    ME = _Me()
    MEPO = _Mepo()
    MD = _Md()
    MY = _My()
    MY_SAT = _My_Sat()
    MY_MOT = _My_Mot()
    MY_SEN = _My_Sen()
    MDRN = _Mdrn()
    MDRND = _Mdrnd()
    MDRNV = _Mdrnv()
    MB = _Mb()
    RAMB = _Ramb()
    MRN = _Mrn()
    RR = _Rr()
    MEV = _Mev()
    MBSTA = _Mbsta()
    MBMOT = _Mbmot()
    MBSEN = _Mbsen()
    MTN = _Mtn()
    V = _V()
    NOD = _Nod()
    ACB = _Acb()
    AMB = _Amb()
    AMBD = _Ambd()
    AMBV = _Ambv()
    NI = _Ni()
    ND = _Nd()
    NR = _Nr()
    RE = _Re()
    NB = _Nb()
    NLL = _Nll()
    NLOT = _Nlot()
    NLOT3 = _Nlot3()
    NLOT1 = _Nlot1()
    NLOT2 = _Nlot2()
    NOT = _Not()
    NPC = _Npc()
    NTS = _Nts()
    NTB = _Ntb()
    PRP = _Prp()
    RM = _Rm()
    RO = _Ro()
    RPA = _Rpa()
    RPO = _Rpo()
    SAG = _Sag()
    X = _X()
    Y = _Y()
    III = _Iii()
    OLF = _Olf()
    OT = _Ot()
    OP = _Op()
    ORB = _Orb()
    ORBL = _Orbl()
    ORBL1 = _Orbl1()
    ORBL2_3 = _Orbl2_3()
    ORBL5 = _Orbl5()
    ORBL6A = _Orbl6A()
    ORBL6B = _Orbl6B()
    ORBM = _Orbm()
    ORBM1 = _Orbm1()
    ORBM2_3 = _Orbm2_3()
    ORBM5 = _Orbm5()
    ORBM6A = _Orbm6A()
    ORBM6B = _Orbm6B()
    ORBVL = _Orbvl()
    ORBVL1 = _Orbvl1()
    ORBVL2_3 = _Orbvl2_3()
    ORBVL5 = _Orbvl5()
    ORBVL6A = _Orbvl6A()
    ORBVL6B = _Orbvl6B()
    PAL = _Pal()
    PALC = _Palc()
    PALD = _Pald()
    PALM = _Palm()
    PALV = _Palv()
    PBG = _Pbg()
    PB = _Pb()
    PCN = _Pcn()
    PF = _Pf()
    PFL = _Pfl()
    PGRN = _Pgrn()
    PGRND = _Pgrnd()
    PGRNL = _Pgrnl()
    PRM = _Prm()
    PN = _Pn()
    PPY = _Ppy()
    PAS = _Pas()
    PS = _Ps()
    PAR = _Par()
    PSTN = _Pstn()
    PT = _Pt()
    PA5 = _Pa5()
    PA4 = _Pa4()
    PVH = _Pvh()
    PVHD = _Pvhd()
    PVT = _Pvt()
    PC5 = _Pc5()
    PARN = _Parn()
    PPN = _Ppn()
    PAG = _Pag()
    PEF = _Pef()
    PHY = _Phy()
    PP = _Pp()
    PR = _Pr()
    PERI = _Peri()
    PERI1 = _Peri1()
    PERI2_3 = _Peri2_3()
    PERI5 = _Peri5()
    PERI6A = _Peri6A()
    PERI6B = _Peri6B()
    P5 = _P5()
    PVA = _Pva()
    PVI = _Pvi()
    PVP = _Pvp()
    PVPO = _Pvpo()
    PVR = _Pvr()
    PVZ = _Pvz()
    PIR = _Pir()
    PAA = _Paa()
    P = _P()
    P_SAT = _P_Sat()
    P_MOT = _P_Mot()
    P_SEN = _P_Sen()
    PCG = _Pcg()
    PG = _Pg()
    PRNR = _Prnr()
    PRNC = _Prnc()
    PA = _Pa()
    AUDPO = _Audpo()
    AUDPO1 = _Audpo1()
    AUDPO2_3 = _Audpo2_3()
    AUDPO4 = _Audpo4()
    AUDPO5 = _Audpo5()
    AUDPO6A = _Audpo6A()
    AUDPO6B = _Audpo6B()
    PO = _Po()
    PH = _Ph()
    PIL = _Pil()
    POL = _Pol()
    PTLP = _Ptlp()
    PPT = _Ppt()
    POT = _Pot()
    PD = _Pd()
    PDTG = _Pdtg()
    VISPL = _Vispl()
    VISPL1 = _Vispl1()
    VISPL2_3 = _Vispl2_3()
    VISPL4 = _Vispl4()
    VISPL5 = _Vispl5()
    VISPL6A = _Vispl6A()
    VISPL6B = _Vispl6B()
    TR = _Tr()
    VISPOR = _Vispor()
    VISPOR1 = _Vispor1()
    VISPOR2_3 = _Vispor2_3()
    VISPOR4 = _Vispor4()
    VISPOR5 = _Vispor5()
    VISPOR6A = _Vispor6A()
    VISPOR6B = _Vispor6B()
    POST = _Post()
    PRC = _Prc()
    PL = _Pl()
    PL1 = _Pl1()
    PL2_3 = _Pl2_3()
    PL5 = _Pl5()
    PL6A = _Pl6A()
    PL6B = _Pl6B()
    PST = _Pst()
    PRE = _Pre()
    PRT = _Prt()
    AUDP = _Audp()
    AUDP1 = _Audp1()
    AUDP2_3 = _Audp2_3()
    AUDP4 = _Audp4()
    AUDP5 = _Audp5()
    AUDP6A = _Audp6A()
    AUDP6B = _Audp6B()
    MOP = _Mop()
    MOP1 = _Mop1()
    MOP2_3 = _Mop2_3()
    MOP5 = _Mop5()
    MOP6A = _Mop6A()
    MOP6B = _Mop6B()
    SSP = _Ssp()
    SSP_BFD = _Ssp_Bfd()
    SSP_BFD1 = _Ssp_Bfd1()
    SSP_BFD2_3 = _Ssp_Bfd2_3()
    SSP_BFD4 = _Ssp_Bfd4()
    SSP_BFD5 = _Ssp_Bfd5()
    SSP_BFD6A = _Ssp_Bfd6A()
    SSP_BFD6B = _Ssp_Bfd6B()
    SSP_LL = _Ssp_Ll()
    SSP_LL1 = _Ssp_Ll1()
    SSP_LL2_3 = _Ssp_Ll2_3()
    SSP_LL4 = _Ssp_Ll4()
    SSP_LL5 = _Ssp_Ll5()
    SSP_LL6A = _Ssp_Ll6A()
    SSP_LL6B = _Ssp_Ll6B()
    SSP_M = _Ssp_M()
    SSP_M1 = _Ssp_M1()
    SSP_M2_3 = _Ssp_M2_3()
    SSP_M4 = _Ssp_M4()
    SSP_M5 = _Ssp_M5()
    SSP_M6A = _Ssp_M6A()
    SSP_M6B = _Ssp_M6B()
    SSP_N = _Ssp_N()
    SSP_N1 = _Ssp_N1()
    SSP_N2_3 = _Ssp_N2_3()
    SSP_N4 = _Ssp_N4()
    SSP_N5 = _Ssp_N5()
    SSP_N6A = _Ssp_N6A()
    SSP_N6B = _Ssp_N6B()
    SSP_TR = _Ssp_Tr()
    SSP_TR1 = _Ssp_Tr1()
    SSP_TR2_3 = _Ssp_Tr2_3()
    SSP_TR4 = _Ssp_Tr4()
    SSP_TR5 = _Ssp_Tr5()
    SSP_TR6A = _Ssp_Tr6A()
    SSP_TR6B = _Ssp_Tr6B()
    SSP_UN = _Ssp_Un()
    SSP_UN1 = _Ssp_Un1()
    SSP_UN2_3 = _Ssp_Un2_3()
    SSP_UN4 = _Ssp_Un4()
    SSP_UN5 = _Ssp_Un5()
    SSP_UN6A = _Ssp_Un6A()
    SSP_UN6B = _Ssp_Un6B()
    SSP_UL = _Ssp_Ul()
    SSP_UL1 = _Ssp_Ul1()
    SSP_UL2_3 = _Ssp_Ul2_3()
    SSP_UL4 = _Ssp_Ul4()
    SSP_UL5 = _Ssp_Ul5()
    SSP_UL6A = _Ssp_Ul6A()
    SSP_UL6B = _Ssp_Ul6B()
    VISP = _Visp()
    VISP1 = _Visp1()
    VISP2_3 = _Visp2_3()
    VISP4 = _Visp4()
    VISP5 = _Visp5()
    VISP6A = _Visp6A()
    VISP6B = _Visp6B()
    PSV = _Psv()
    PROS = _Pros()
    PYR = _Pyr()
    RN = _Rn()
    RT = _Rt()
    RCH = _Rch()
    RHP = _Rhp()
    RPF = _Rpf()
    RSP = _Rsp()
    RSPD = _Rspd()
    RSPD1 = _Rspd1()
    RSPD2_3 = _Rspd2_3()
    RSPD4 = _Rspd4()
    RSPD5 = _Rspd5()
    RSPD6A = _Rspd6A()
    RSPD6B = _Rspd6B()
    RSPAGL = _Rspagl()
    RSPAGL1 = _Rspagl1()
    RSPAGL2_3 = _Rspagl2_3()
    RSPAGL5 = _Rspagl5()
    RSPAGL6A = _Rspagl6A()
    RSPAGL6B = _Rspagl6B()
    RSPV = _Rspv()
    RSPV1 = _Rspv1()
    RSPV2_3 = _Rspv2_3()
    RSPV5 = _Rspv5()
    RSPV6A = _Rspv6A()
    RSPV6B = _Rspv6B()
    RH = _Rh()
    RL = _Rl()
    VISRL1 = _Visrl1()
    VISRL2_3 = _Visrl2_3()
    VISRL4 = _Visrl4()
    VISRL5 = _Visrl5()
    VISRL6A = _Visrl6A()
    VISRL6B = _Visrl6B()
    VISRL = _Visrl()
    MOS = _Mos()
    MOS1 = _Mos1()
    MOS2_3 = _Mos2_3()
    MOS5 = _Mos5()
    MOS6A = _Mos6A()
    MOS6B = _Mos6B()
    SF = _Sf()
    SH = _Sh()
    SIM = _Sim()
    MO = _Mo()
    SS = _Ss()
    SPVC = _Spvc()
    SPVI = _Spvi()
    SPVO = _Spvo()
    SPIV = _Spiv()
    STR = _Str()
    STRD = _Strd()
    STRV = _Strv()
    SAMY = _Samy()
    SLC = _Slc()
    SCO = _Sco()
    SFO = _Sfo()
    SUBG = _Subg()
    SUB = _Sub()
    SLD = _Sld()
    SMT = _Smt()
    SPA = _Spa()
    SPF = _Spf()
    SPFM = _Spfm()
    SPFP = _Spfp()
    SBPV = _Sbpv()
    SI = _Si()
    SNC = _Snc()
    SNR = _Snr()
    STN = _Stn()
    CS = _Cs()
    SCM = _Scm()
    SCDG = _Scdg()
    SCDW = _Scdw()
    SCIG = _Scig()
    SCIW = _Sciw()
    SCOP = _Scop()
    SCS = _Scs()
    SCSG = _Scsg()
    SCZO = _Sczo()
    SOC = _Soc()
    SOCL = _Socl()
    SOCM = _Socm()
    POR = _Por()
    SUV = _Suv()
    SSS = _Sss()
    SSS1 = _Sss1()
    SSS2_3 = _Sss2_3()
    SSS4 = _Sss4()
    SSS5 = _Sss5()
    SSS6A = _Sss6A()
    SSS6B = _Sss6B()
    SCH = _Sch()
    SGN = _Sgn()
    SG = _Sg()
    SUM = _Sum()
    SU3 = _Su3()
    SO = _So()
    SUT = _Sut()
    TT = _Tt()
    TTD = _Ttd()
    TTV = _Ttv()
    TRN = _Trn()
    TEA = _Tea()
    TEA1 = _Tea1()
    TEA2_3 = _Tea2_3()
    TEA4 = _Tea4()
    TEA5 = _Tea5()
    TEA6A = _Tea6A()
    TEA6B = _Tea6B()
    TH = _Th()
    DORPM = _Dorpm()
    DORSM = _Dorsm()
    TRS = _Trs()
    IV = _Iv()
    TU = _Tu()
    TM = _Tm()
    TMD = _Tmd()
    TMV = _Tmv()
    UVU = _Uvu()
    OV = _Ov()
    VAL = _Val()
    AUDV = _Audv()
    AUDV1 = _Audv1()
    AUDV2_3 = _Audv2_3()
    AUDV4 = _Audv4()
    AUDV5 = _Audv5()
    AUDV6A = _Audv6A()
    AUDV6B = _Audv6B()
    VCO = _Vco()
    VENT = _Vent()
    VM = _Vm()
    LGV = _Lgv()
    VP = _Vp()
    VPL = _Vpl()
    VPLPC = _Vplpc()
    VPM = _Vpm()
    VPMPC = _Vpmpc()
    PMV = _Pmv()
    VTA = _Vta()
    VTN = _Vtn()
    VLPO = _Vlpo()
    VMH = _Vmh()
    VMPO = _Vmpo()
    VERM = _Verm()
    VNC = _Vnc()
    VECB = _Vecb()
    VISC = _Visc()
    VISC1 = _Visc1()
    VISC2_3 = _Visc2_3()
    VISC4 = _Visc4()
    VISC5 = _Visc5()
    VISC6A = _Visc6A()
    VISC6B = _Visc6B()
    VIS = _Vis()
    XI = _Xi()
    ZI = _Zi()
    ALV = _Alv()
    AMC = _Amc()
    ACO = _Aco()
    ACT = _Act()
    ARB = _Arb()
    AR = _Ar()
    BIC = _Bic()
    BSC = _Bsc()
    C = _C()
    CPD = _Cpd()
    CBC = _Cbc()
    CBP = _Cbp()
    CBF = _Cbf()
    AQ = _Aq()
    EPSC = _Epsc()
    MFBC = _Mfbc()
    CETT = _Cett()
    CHPL = _Chpl()
    CING = _Cing()
    CVIIIN = _Cviiin()
    FX = _Fx()
    STC = _Stc()
    CC = _Cc()
    FA = _Fa()
    CCB = _Ccb()
    EE = _Ee()
    FP = _Fp()
    CCS = _Ccs()
    CST = _Cst()
    CNE = _Cne()
    TSPC = _Tspc()
    CUF = _Cuf()
    TSPD = _Tspd()
    DTD = _Dtd()
    DAS = _Das()
    DC = _Dc()
    DF = _Df()
    DHC = _Dhc()
    LOTD = _Lotd()
    DRT = _Drt()
    SCTD = _Sctd()
    MFBSE = _Mfbse()
    EC = _Ec()
    EM = _Em()
    EPS = _Eps()
    VIIN = _Viin()
    FR = _Fr()
    FIBER_TRACTS = _Fiber_Tracts()
    FI = _Fi()
    FXS = _Fxs()
    V4 = _V4()
    CCG = _Ccg()
    GVIIN = _Gviin()
    HBC = _Hbc()
    HC = _Hc()
    MFSBSHY = _Mfsbshy()
    ICP = _Icp()
    CIC = _Cic()
    INT = _Int()
    LFBS = _Lfbs()
    LL = _Ll()
    LOT = _Lot()
    LOTG = _Lotg()
    V4R = _V4R()
    VL = _Vl()
    MP = _Mp()
    MFBSMA = _Mfbsma()
    MTG = _Mtg()
    MTT = _Mtt()
    MCT = _Mct()
    MFB = _Mfb()
    MFBS = _Mfbs()
    ML = _Ml()
    MLF = _Mlf()
    MCP = _Mcp()
    MOV = _Mov()
    NST = _Nst()
    IIIN = _Iiin()
    IN = _In()
    ONL = _Onl()
    OCH = _Och()
    IIN = _Iin()
    OR = _Or()
    OPT = _Opt()
    FXPO = _Fxpo()
    PC = _Pc()
    VISPM = _Vispm()
    VISPM1 = _Vispm1()
    VISPM2_3 = _Vispm2_3()
    VISPM4 = _Vispm4()
    VISPM5 = _Vispm5()
    VISPM6A = _Vispm6A()
    VISPM6B = _Vispm6B()
    PM = _Pm()
    PY = _Py()
    PYD = _Pyd()
    ROOT = _Root()
    RUST = _Rust()
    SV = _Sv()
    TS = _Ts()
    SPTV = _Sptv()
    SM = _Sm()
    ST = _St()
    SEZ = _Sez()
    SCP = _Scp()
    DSCP = _Dscp()
    CSC = _Csc()
    SCWM = _Scwm()
    SUP = _Sup()
    TSP = _Tsp()
    LFBST = _Lfbst()
    V3 = _V3()
    TB = _Tb()
    VN = _Vn()
    IVN = _Ivn()
    UF = _Uf()
    XN = _Xn()
    VHC = _Vhc()
    SCTV = _Sctv()
    VTD = _Vtd()
    VS = _Vs()
    VVIIIN = _Vviiin()
    VIIIN = _Viiin()
    VON = _Von()

    ALL = tuple(_BrainStructureModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(_BrainStructureModel.__subclasses__())], Field(discriminator="name")]

    id_map = {m().id: m() for m in ALL}

    @classmethod
    def from_id(cls, id: int):
        """Get structure from id"""
        return cls.id_map.get(id, None)
