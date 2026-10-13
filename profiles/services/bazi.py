from lunar_python import Solar


ZODIAC_EN = {
    "鼠": "Rat", "牛": "Ox", "虎": "Tiger", "兔": "Rabbit",
    "龙": "Dragon", "蛇": "Snake", "马": "Horse", "羊": "Goat",
    "猴": "Monkey", "鸡": "Rooster", "狗": "Dog", "猪": "Pig",
}

ELEMENT_EN = {
    "木": "Wood",
    "火": "Fire",
    "土": "Earth",
    "金": "Metal",
    "水": "Water",
}

STEM_ELEMENT = {
    "甲": "Wood", "乙": "Wood",
    "丙": "Fire", "丁": "Fire",
    "戊": "Earth", "己": "Earth",
    "庚": "Metal", "辛": "Metal",
    "壬": "Water", "癸": "Water",
}

BAZI_DAY_PILLAR_SECT = 2


def _pillar(name, value, element_value, stem):
    elements = list(element_value or "")
    return {
        "name": name,
        "chinese": value,
        "stem": stem,
        "stem_element": STEM_ELEMENT.get(stem),
        "associated_elements": [
            ELEMENT_EN.get(element, element) for element in elements
        ],
    }


def calculate_birth_reading(profile):
    """
    Calculate a preliminary Chinese zodiac and BaZi reading.

    Birth time is interpreted as the local civil time entered by the user.
    No birthplace geocoding or historical time-zone conversion is performed.

    The Day Pillar convention is explicitly set to Sect 2. The Hour Pillar
    follows the behavior provided by lunar_python.
    """
    if not profile or not profile.birth_date:
        raise ValueError("A birth date is required to calculate a reading.")

    birth_date = profile.birth_date
    birth_time = profile.birth_time
    time_is_known = birth_time is not None

    # Noon is only a calculation placeholder when the birth time is unknown.
    # The Hour Pillar is never displayed in that case.
    hour = birth_time.hour if time_is_known else 12
    minute = birth_time.minute if time_is_known else 0
    second = birth_time.second if time_is_known else 0

    solar = Solar.fromYmdHms(
        birth_date.year,
        birth_date.month,
        birth_date.day,
        hour,
        minute,
        second,
    )
    lunar = solar.getLunar()
    eight_char = lunar.getEightChar()

    # Make the chosen Day Pillar convention explicit rather than relying
    # on the library's default.
    eight_char.setSect(BAZI_DAY_PILLAR_SECT)

    year_value = eight_char.getYear()
    month_value = eight_char.getMonth()
    day_value = eight_char.getDay()

    pillars = [
        _pillar(
            "Year", year_value, eight_char.getYearWuXing(),
            eight_char.getYearGan()
        ),
        _pillar(
            "Month", month_value, eight_char.getMonthWuXing(),
            eight_char.getMonthGan()
        ),
        _pillar(
            "Day", day_value, eight_char.getDayWuXing(),
            eight_char.getDayGan()
        ),
    ]

    if time_is_known:
        pillars.append(
            _pillar(
                "Hour", eight_char.getTime(),
                eight_char.getTimeWuXing(),
                eight_char.getTimeGan(),
            )
        )

    zodiac_chinese = lunar.getYearShengXiao()
    warnings = []

    if not time_is_known:
        warnings.append(
            "Birth time was not provided. The Hour Pillar is unavailable. "
            "Pillars near a solar-term boundary may need further verification."
        )

    if not (profile.birth_place or "").strip():
        warnings.append(
            "Birthplace was not provided. Time-zone and location-dependent "
            "verification has not been performed."
        )
    else:
        warnings.append(
            "Birth time is interpreted as local civil time. The birthplace's "
            "historical time zone has not yet been automatically verified."
        )

    return {
        "birth_date": birth_date.isoformat(),
        "lunar_date": str(lunar),
        "zodiac": {
            "chinese": zodiac_chinese,
            "english": ZODIAC_EN.get(zodiac_chinese, zodiac_chinese),
        },
        "pillars": pillars,
        "day_master": {
            "stem": eight_char.getDayGan(),
            "element": STEM_ELEMENT.get(eight_char.getDayGan()),
        },
        "birth_time_known": time_is_known,
        "birth_place": (profile.birth_place or "").strip() or None,
        "is_full_four_pillars": time_is_known,
        "warnings": warnings,
        "calculation_note": (
            "Preliminary traditional-calendar calculation using the Sect 2 "
            "Day Pillar convention. Five Element associations shown here are "
            "not a complete Five Element balance analysis."
        ),
    }
