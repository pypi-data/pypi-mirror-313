import dataclasses


@dataclasses.dataclass
class AiscWideFlange(object):
    """This is a dataclass containing the properties of an AISC Wide Flange section. Properties follow the AISC shapes
    database.

    :param A: Cross-sectional area (in^2)
    :type A: float
    :param AISC_name: The name of the AISC section
    :type AISC_name: str
    :param Cw: Warping constant (in^6)
    :type Cw: float
    :param EDI_Std_Nomenclature: The EDI standard nomenclature name
    :type EDI_Std_Nomenclature: str
    :param Ix: Moment of inertia about the x-axis (in^4)
    :type Ix: float
    :param Iy: Moment of inertia about the y-axis (in^4)
    :type Iy: float
    :param J: Torsional constant (in^4)
    :type J: float
    :param PA: Shape perimeter minus one flange surface, as used in Design Guide 19 (in)
    :type PA: float
    :param PB: Shape perimeter, as used in AISC Design Guide 19 (in)
    :type PB: float
    :param PC: Box perimeter minus one flange surface, as used in Design Guide 19 (in)
    :type PC: float
    :param PD: Box perimeter, as used in AISC Design Guide 19 (in)
    :type PD: float
    :param Qf: Statical moment for a point in the flange directly above the vertical edge of the web (in^3)
    :type Qf: float
    :param Qw: Statical moment for a point at mid-depth of the cross section (in^3)
    :type Qw: float
    :param Sw1: Warping statical moment at point 1 on cross section (in^4)
    :type Sw1: float
    :param Sx: Elastic section modulus about the x-axis (in^3)
    :type Sx: float
    :param Sy: Elastic section modulus about the y-axis (in^3)
    :type Sy: float
    :param T: Distance between web toes of fillets at top and bottom of web (in)
    :type T: float
    :param T_F: Whether the section has an additional note in the AISC shapes database (T or F)
    :type T_F: str
    :param Type: The section type
    :type Type: str
    :param W: Nominal weight (lb/ft)
    :type W: float
    :param WGi: The workable gage for the inner fastener holes in the flange (in)
    :type WGi: float
    :param Wno: Normalized warping function, as used in Design Guide 9 (in^2)
    :type Wno: float
    :param Zx: Plastic section modulus about the x-axis (in^3)
    :type Zx: float
    :param Zy: Plastic section modulus about the y-axis (in^3)
    :type Zy: float
    :param bf: Width of flange (in)
    :type bf: float
    :param bfdet: Detailing value of flange width (in)
    :type bfdet: float
    :param bf_2tf: Slenderness ratio for flange, bf/2tf
    :type bf_2tf: float
    :param d: Overall depth of member (in)
    :type d: float
    :param ddet: Detailing value of member depth (in)
    :type ddet: float
    :param h_tw: Slenderness ratio for web, h/tw
    :type h_tw: float
    :param ho: Distance between the flange centroids (in)
    :type ho: float
    :param k1: Distance from web center line to flange toe of fillet used for detailing (in)
    :type k1: float
    :param kdes: Distance from outer face of flange to web toe of fillet used for design (in)
    :type kdes: float
    :param kdet: Distance from outer face of flange to web toe of fillet used for detailing (in)
    :type kdet: float
    :param rts: Effective radius of gyration (in)
    :type rts: float
    :param rx: Radius of gyration about the x-axis (in)
    :type rx: float
    :param ry: Radius of gyration about the y-axis (in)
    :type ry: float
    :param tf: Thickness of flange (in)
    :type tf: float
    :param tfdet: Detailing value of flange thickness (in)
    :type tfdet: float
    :param tw: Thickness of web (in)
    :type tw: float
    :param twdet: Detailing value of web thickness (in)
    :type twdet: float
    :param twdet_2: Half the web thickness for detailing purposes, twdet/2 (in)
    :type twdet_2: float
    """

    A: float
    AISC_name: str
    Cw: float
    EDI_Std_Nomenclature: str
    Ix: float
    Iy: float
    J: float
    PA: float
    PB: float
    PC: float
    PD: float
    Qf: float
    Qw: float
    Sw1: float
    Sx: float
    Sy: float
    T: float
    T_F: str
    Type: str
    W: float
    WGi: float
    Wno: float
    Zx: float
    Zy: float
    bf: float
    bfdet: float
    bf_2tf: float
    d: float
    ddet: float
    h_tw: float
    ho: float
    k1: float
    kdes: float
    kdet: float
    rts: float
    rx: float
    ry: float
    tf: float
    tfdet: float
    tw: float
    twdet: float
    twdet_2: float


ALL_AISC_WIDE_FLANGE_NAMES = (
    "W44X335",
    "W44X290",
    "W44X262",
    "W40X655",
    "W44X230",
    "W40X503",
    "W40X593",
    "W40X431",
    "W40X397",
    "W40X372",
    "W40X297",
    "W40X362",
    "W40X277",
    "W40X249",
    "W40X215",
    "W40X199",
    "W40X324",
    "W40X392",
    "W40X331",
    "W40X327",
    "W40X294",
    "W40X278",
    "W40X264",
    "W40X235",
    "W40X211",
    "W40X183",
    "W40X149",
    "W40X167",
    "W36X853",
    "W36X802",
    "W36X723",
    "W36X652",
    "W36X529",
    "W36X487",
    "W36X925",
    "W36X441",
    "W36X395",
    "W36X361",
    "W36X330",
    "W36X302",
    "W36X262",
    "W36X282",
    "W36X231",
    "W36X247",
    "W36X256",
    "W36X232",
    "W36X210",
    "W36X194",
    "W36X182",
    "W36X170",
    "W36X160",
    "W36X150",
    "W36X135",
    "W33X387",
    "W33X354",
    "W33X291",
    "W33X318",
    "W33X241",
    "W33X263",
    "W33X221",
    "W33X201",
    "W33X169",
    "W33X152",
    "W33X141",
    "W33X130",
    "W33X118",
    "W30X357",
    "W30X391",
    "W30X326",
    "W30X292",
    "W30X235",
    "W30X261",
    "W30X191",
    "W30X211",
    "W30X173",
    "W30X148",
    "W30X124",
    "W30X132",
    "W30X116",
    "W30X108",
    "W30X99",
    "W30X90",
    "W27X368",
    "W27X539",
    "W27X336",
    "W27X307",
    "W27X281",
    "W27X258",
    "W27X235",
    "W27X194",
    "W27X217",
    "W27X178",
    "W27X161",
    "W27X129",
    "W27X146",
    "W27X114",
    "W27X102",
    "W27X84",
    "W24X370",
    "W27X94",
    "W24X335",
    "W24X306",
    "W24X279",
    "W24X250",
    "W24X229",
    "W24X192",
    "W24X207",
    "W24X176",
    "W24X162",
    "W24X146",
    "W24X117",
    "W24X131",
    "W24X104",
    "W24X94",
    "W24X103",
    "W24X84",
    "W24X68",
    "W24X76",
    "W24X62",
    "W24X55",
    "W21X275",
    "W21X248",
    "W21X201",
    "W21X223",
    "W21X182",
    "W21X166",
    "W21X147",
    "W21X132",
    "W21X111",
    "W21X93",
    "W21X73",
    "W21X122",
    "W21X83",
    "W21X68",
    "W21X62",
    "W21X101",
    "W21X55",
    "W21X48",
    "W21X50",
    "W21X57",
    "W18X311",
    "W21X44",
    "W18X283",
    "W18X258",
    "W18X234",
    "W18X192",
    "W18X211",
    "W18X175",
    "W18X158",
    "W18X143",
    "W18X130",
    "W18X119",
    "W18X106",
    "W18X86",
    "W18X97",
    "W18X76",
    "W18X71",
    "W18X65",
    "W18X55",
    "W18X60",
    "W18X50",
    "W18X46",
    "W18X40",
    "W18X35",
    "W16X100",
    "W16X89",
    "W16X67",
    "W16X77",
    "W16X57",
    "W16X50",
    "W16X40",
    "W16X45",
    "W16X36",
    "W16X31",
    "W16X26",
    "W14X873",
    "W14X808",
    "W14X730",
    "W14X665",
    "W14X550",
    "W14X605",
    "W14X500",
    "W14X455",
    "W14X426",
    "W14X398",
    "W14X370",
    "W14X311",
    "W14X342",
    "W14X283",
    "W14X257",
    "W14X233",
    "W14X211",
    "W14X193",
    "W14X176",
    "W14X159",
    "W14X145",
    "W14X132",
    "W14X120",
    "W14X99",
    "W14X109",
    "W14X90",
    "W14X82",
    "W14X74",
    "W14X68",
    "W14X61",
    "W14X53",
    "W14X48",
    "W14X43",
    "W14X38",
    "W14X34",
    "W14X30",
    "W14X26",
    "W14X22",
    "W12X336",
    "W12X305",
    "W12X279",
    "W12X252",
    "W12X230",
    "W12X210",
    "W12X190",
    "W12X170",
    "W12X152",
    "W12X136",
    "W12X120",
    "W12X106",
    "W12X87",
    "W12X96",
    "W12X79",
    "W12X72",
    "W12X65",
    "W12X58",
    "W12X53",
    "W12X50",
    "W12X45",
    "W12X35",
    "W12X40",
    "W12X30",
    "W12X26",
    "W12X22",
    "W12X19",
    "W12X14",
    "W12X16",
    "W10X112",
    "W10X100",
    "W10X77",
    "W10X88",
    "W10X68",
    "W10X60",
    "W10X54",
    "W10X45",
    "W10X49",
    "W10X39",
    "W10X30",
    "W10X33",
    "W10X26",
    "W10X22",
    "W10X19",
    "W10X17",
    "W10X15",
    "W10X12",
    "W8X67",
    "W8X48",
    "W8X58",
    "W8X40",
    "W8X35",
    "W8X31",
    "W8X28",
    "W8X24",
    "W8X21",
    "W8X18",
    "W8X15",
    "W8X13",
    "W8X10",
    "W6X25",
    "W6X20",
    "W6X15",
    "W6X12",
    "W6X16",
    "W6X9",
    "W6X8.5",
    "W5X19",
    "W5X16",
    "W4X13",
    "M12.5X12.4",
    "M12X11.8",
    "M12.5X11.6",
    "M12X10.8",
    "M10X9",
    "M12X10",
    "M10X8",
    "M10X7.5",
    "M8X6.5",
    "M8X6.2",
    "M6X4.4",
    "M6X3.7",
    "M5X18.9",
    "M4X4.08",
    "M4X6",
    "M4X3.2",
    "M4X3.45",
    "S24X106",
    "S24X121",
    "S24X90",
    "S24X100",
    "S24X80",
    "M3X2.9",
    "S20X96",
    "S20X86",
    "S20X66",
    "S20X75",
    "S18X70",
    "S18X54.7",
    "S15X50",
    "S15X42.9",
    "S12X50",
    "S12X40.8",
    "S12X31.8",
    "S12X35",
    "S10X35",
    "S10X25.4",
    "S8X23",
    "S8X18.4",
    "S6X17.25",
    "S6X12.5",
    "S5X10",
    "S4X9.5",
    "S4X7.7",
    "S3X7.5",
    "S3X5.7",
    "HP18X204",
    "HP18X181",
    "HP18X157",
    "HP18X135",
    "HP16X162",
    "HP16X183",
    "HP16X121",
    "HP16X141",
    "HP16X101",
    "HP16X88",
    "HP14X117",
    "HP14X102",
    "HP14X73",
    "HP14X89",
    "HP12X89",
    "HP12X84",
    "HP12X74",
    "HP12X53",
    "HP10X57",
    "HP10X42",
    "HP12X63",
    "HP8X36",
)
