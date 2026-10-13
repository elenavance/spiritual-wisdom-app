
from datetime import date

from lunar_python import Solar


ZODIAC_EN = {
    "鼠": "Rat", "牛": "Ox", "虎": "Tiger", "兔": "Rabbit",
    "龙": "Dragon", "蛇": "Snake", "马": "Horse", "羊": "Goat",
    "猴": "Monkey", "鸡": "Rooster", "狗": "Dog", "猪": "Pig",
}

ELEMENT_EN = {
    "木": "Wood", "火": "Fire", "土": "Earth",
    "金": "Metal", "水": "Water",
}

STEM_ELEMENT = {
    "甲": "Wood", "乙": "Wood", "丙": "Fire", "丁": "Fire",
    "戊": "Earth", "己": "Earth", "庚": "Metal", "辛": "Metal",
    "壬": "Water", "癸": "Water",
}

STEM_POLARITY = {
    "甲": "Yang", "乙": "Yin", "丙": "Yang", "丁": "Yin",
    "戊": "Yang", "己": "Yin", "庚": "Yang", "辛": "Yin",
    "壬": "Yang", "癸": "Yin",
}

TEN_GODS_EN = {
    "比肩": "Friend",
    "劫财": "Rob Wealth",
    "食神": "Eating God",
    "伤官": "Hurting Officer",
    "偏财": "Indirect Wealth",
    "正财": "Direct Wealth",
    "七杀": "Seven Killings",
    "正官": "Direct Officer",
    "偏印": "Indirect Resource",
    "正印": "Direct Resource",
}

GENERATES = {
    "Wood": "Fire", "Fire": "Earth", "Earth": "Metal",
    "Metal": "Water", "Water": "Wood",
}

CONTROLS = {
    "Wood": "Earth", "Earth": "Water", "Water": "Fire",
    "Fire": "Metal", "Metal": "Wood",
}

BAZI_DAY_PILLAR_SECT = 2


def ten_god_for_stem(day_master_stem, other_stem):
    day_element = STEM_ELEMENT.get(day_master_stem)
    other_element = STEM_ELEMENT.get(other_stem)

    if not day_element or not other_element:
        return None

    same_polarity = (
        STEM_POLARITY[day_master_stem] == STEM_POLARITY[other_stem]
    )

    if day_element == other_element:
        return "比肩" if same_polarity else "劫财"
    if GENERATES[day_element] == other_element:
        return "食神" if same_polarity else "伤官"
    if CONTROLS[day_element] == other_element:
        return "偏财" if same_polarity else "正财"
    if CONTROLS[other_element] == day_element:
        return "七杀" if same_polarity else "正官"
    if GENERATES[other_element] == day_element:
        return "偏印" if same_polarity else "正印"
    return None


def _pillar(name, value, element_value, stem, branch, hidden_stems, day_master):
    elements = list(element_value or "")
    hidden_stems = list(hidden_stems or [])
    ten_god = ten_god_for_stem(day_master, stem)

    return {
        "name": name,
        "chinese": value,
        "stem": stem,
        "stem_element": STEM_ELEMENT.get(stem),
        "stem_polarity": STEM_POLARITY.get(stem),
        "ten_god": ten_god,
        "ten_god_english": TEN_GODS_EN.get(ten_god),
        "branch": branch,
        "hidden_stems": [
            {
                "stem": hidden,
                "element": STEM_ELEMENT.get(hidden),
                "ten_god": ten_god_for_stem(day_master, hidden),
                "ten_god_english": TEN_GODS_EN.get(
                    ten_god_for_stem(day_master, hidden)
                ),
            }
            for hidden in hidden_stems
        ],
        "associated_elements": [
            ELEMENT_EN.get(element, element) for element in elements
        ],
    }


def _get_luck_pillars(eight_char, gender, day_master, birth_date):
    """Calculate traditional DaYun periods using lunar_python."""
    gender_codes = {"male": 1, "female": 0}

    if gender not in gender_codes:
        return {
            "available": False,
            "direction": None,
            "start_age": {"years": 0, "months": 0, "days": 0},
            "start_date": None,
            "pillars": [],
            "message": (
                "Luck Pillar direction needs a male/female selection under "
                "this traditional calculation convention. No direction "
                "was assumed for the supplied gender."
            ),
        }

    try:
        yun = eight_char.getYun(
            gender_codes[gender], BAZI_DAY_PILLAR_SECT
        )
        start_solar = yun.getStartSolar()
        start_age = {
            "years": yun.getStartYear(),
            "months": yun.getStartMonth(),
            "days": yun.getStartDay(),
        }

        pillars = []
        for item in yun.getDaYun(11):
            index = item.getIndex()
            gan_zhi = item.getGanZhi()

            if index <= 0 or not gan_zhi or len(gan_zhi) != 2:
                continue

            stem, branch = gan_zhi[0], gan_zhi[1]
            ten_god = ten_god_for_stem(day_master, stem)

            pillars.append({
                "index": index,
                "gan_zhi": gan_zhi,
                "stem": stem,
                "branch": branch,
                "element": STEM_ELEMENT.get(stem),
                "polarity": STEM_POLARITY.get(stem),
                "ten_god": ten_god,
                "ten_god_english": TEN_GODS_EN.get(ten_god),
                "start_year": item.getStartYear(),
                "end_year": item.getEndYear(),
                "start_age": item.getStartAge(),
                "end_age": item.getEndAge(),
            })

        return {
            "available": bool(pillars),
            "direction": "Forward" if yun.isForward() else "Backward",
            "start_age": start_age,
            "start_date": start_solar.toYmd(),
            "pillars": pillars[:10],
            "message": (
                "Luck Pillars use the installed lunar_python calculation. "
                "When birth time is unknown, noon is used as a placeholder, "
                "so the starting timing is approximate."
            ),
        }

    except (AttributeError, TypeError, ValueError, IndexError):
        return {
            "available": False,
            "direction": None,
            "start_age": {"years": 0, "months": 0, "days": 0},
            "start_date": None,
            "pillars": [],
            "message": "Luck Pillars could not be calculated for this chart.",
        }


def _get_annual_influences(day_master, start_year=None, count=10):
    """Return annual Li Chun year-pillar stems and Ten Gods associations."""
    if start_year is None:
        start_year = date.today().year

    years = []
    for year in range(start_year, start_year + count):
        solar = Solar.fromYmdHms(year, 6, 15, 12, 0, 0)
        gan_zhi = solar.getLunar().getYearInGanZhiByLiChun()
        stem, branch = gan_zhi[0], gan_zhi[1]
        ten_god = ten_god_for_stem(day_master, stem)

        years.append({
            "year": year,
            "gan_zhi": gan_zhi,
            "stem": stem,
            "branch": branch,
            "element": STEM_ELEMENT.get(stem),
            "polarity": STEM_POLARITY.get(stem),
            "ten_god": ten_god,
            "ten_god_english": TEN_GODS_EN.get(ten_god),
        })

    return {
        "years": years,
        "method": (
            "Annual influences use the Li Chun year-pillar convention and "
            "classify the year's Heavenly Stem relative to the Day Master. "
            "They are not a complete natal-chart interaction analysis or "
            "predictions of specific events."
        ),
    }


def calculate_birth_reading(profile):
    if not profile or not profile.birth_date:
        raise ValueError("A birth date is required to calculate a reading.")

    birth_date = profile.birth_date
    birth_time = profile.birth_time
    time_is_known = birth_time is not None

    hour = birth_time.hour if time_is_known else 12
    minute = birth_time.minute if time_is_known else 0
    second = birth_time.second if time_is_known else 0

    solar = Solar.fromYmdHms(
        birth_date.year, birth_date.month, birth_date.day,
        hour, minute, second,
    )
    lunar = solar.getLunar()
    eight_char = lunar.getEightChar()
    eight_char.setSect(BAZI_DAY_PILLAR_SECT)
    day_master = eight_char.getDayGan()

    pillar_data = [
        (
            "Year", eight_char.getYear(), eight_char.getYearWuXing(),
            eight_char.getYearGan(), eight_char.getYearZhi(),
            eight_char.getYearHideGan(),
        ),
        (
            "Month", eight_char.getMonth(), eight_char.getMonthWuXing(),
            eight_char.getMonthGan(), eight_char.getMonthZhi(),
            eight_char.getMonthHideGan(),
        ),
        (
            "Day", eight_char.getDay(), eight_char.getDayWuXing(),
            eight_char.getDayGan(), eight_char.getDayZhi(),
            eight_char.getDayHideGan(),
        ),
    ]

    if time_is_known:
        pillar_data.append((
            "Hour", eight_char.getTime(), eight_char.getTimeWuXing(),
            eight_char.getTimeGan(), eight_char.getTimeZhi(),
            eight_char.getTimeHideGan(),
        ))

    pillars = [
        _pillar(
            name, value, element_value, stem, branch, hidden_stems, day_master
        )
        for name, value, element_value, stem, branch, hidden_stems
        in pillar_data
    ]

    zodiac_chinese = lunar.getYearShengXiao()
    warnings = []

    if not time_is_known:
        warnings.append(
            "Birth time was not provided. The Hour Pillar is unavailable. "
            "Noon is used only as a placeholder for calculations that need "
            "a time; time-dependent results may differ from the true chart."
        )

    if not (profile.birth_place or "").strip():
        warnings.append(
            "Birthplace was not provided. Historical time-zone and "
            "location-dependent verification has not been performed."
        )
    else:
        warnings.append(
            "Birth time is interpreted as local civil time. Historical "
            "time-zone verification has not been automated."
        )

    luck_pillars = _get_luck_pillars(
        eight_char,
        getattr(profile, "gender", None),
        day_master,
        birth_date,
    )

    annual_influences = _get_annual_influences(
        day_master, start_year=date.today().year, count=10
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
            "stem": day_master,
            "element": STEM_ELEMENT.get(day_master),
            "polarity": STEM_POLARITY.get(day_master),
        },
        "birth_time_known": time_is_known,
        "birth_place": (profile.birth_place or "").strip() or None,
        "is_full_four_pillars": time_is_known,
        "luck_pillars": luck_pillars,
        "annual_influences": annual_influences,
        "warnings": warnings,
        "calculation_note": (
            "Traditional BaZi relationships are presented for cultural "
            "learning and reflection. Ten Gods and annual influences are "
            "symbolic frameworks, not scientific personality assessments "
            "or predictions."
        ),
    }
