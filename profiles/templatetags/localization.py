from django import template

register = template.Library()

ELEMENTS = {
    "Wood": "\u6728",
    "Fire": "\u706b",
    "Earth": "\u571f",
    "Metal": "\u91d1",
    "Water": "\u6c34",
}

POLARITY = {"Yang": "\u9633", "Yin": "\u9634"}

PILLARS = {
    "Year": "\u5e74\u67f1",
    "Month": "\u6708\u67f1",
    "Day": "\u65e5\u67f1",
    "Hour": "\u65f6\u67f1",
}

ZODIAC = {
    "Rat": "\u9f20",
    "Ox": "\u725b",
    "Tiger": "\u864e",
    "Rabbit": "\u5154",
    "Dragon": "\u9f99",
    "Snake": "\u86c7",
    "Horse": "\u9a6c",
    "Goat": "\u7f8a",
    "Monkey": "\u7334",
    "Rooster": "\u9e21",
    "Dog": "\u72d7",
    "Pig": "\u732a",
}

TEN_GODS = {
    "Friend": "\u6bd4\u80a9",
    "Rob Wealth": "\u52ab\u8d22",
    "Eating God": "\u98df\u795e",
    "Hurting Officer": "\u4f24\u5b98",
    "Indirect Wealth": "\u504f\u8d22",
    "Direct Wealth": "\u6b63\u8d22",
    "Seven Killings": "\u4e03\u6740",
    "Direct Officer": "\u6b63\u5b98",
    "Indirect Resource": "\u504f\u5370",
    "Direct Resource": "\u6b63\u5370",
}

TEXT = {
    "Day Master": "\u65e5\u4e3b",
    "Preliminary chart assessment": "\u547d\u76d8\u521d\u6b65\u8bc4\u4f30",
    "Provided": "\u5df2\u63d0\u4f9b",
    "Not provided; Hour Pillar omitted": "\u672a\u63d0\u4f9b\u51fa\u751f\u65f6\u95f4\uff1b\u4e0d\u663e\u793a\u65f6\u67f1",
    "Personality Themes": "\u6027\u683c\u4e3b\u9898",
    "Personality and Natural Tendencies": "\u6027\u683c\u4e0e\u81ea\u7136\u503e\u5411",
    "Career and Working Style": "\u4e8b\u4e1a\u4e0e\u5de5\u4f5c\u65b9\u5f0f",
    "Love and Relationships": "\u7231\u60c5\u4e0e\u4eba\u9645\u5173\u7cfb",
    "Relationships and Communication": "\u5173\u7cfb\u4e0e\u6c9f\u901a",
    "Money and Financial Habits": "\u91d1\u94b1\u4e0e\u8d22\u52a1\u4e60\u60ef",
    "Family and Communication": "\u5bb6\u5ead\u4e0e\u6c9f\u901a",
    "Health and Wellbeing": "\u5065\u5eb7\u4e0e\u8eab\u5fc3\u72b6\u6001",
    "Personal Development": "\u4e2a\u4eba\u53d1\u5c55",
    "Personal Growth": "\u4e2a\u4eba\u6210\u957f",
    "Reflect:": "\u53cd\u601d\uff1a",
    "Birth date": "\u51fa\u751f\u65e5\u671f",
    "Chinese zodiac": "\u4e2d\u56fd\u751f\u8096",
    "Zodiac": "\u751f\u8096",
    "No hidden-stem details.": "\u6682\u65e0\u85cf\u5e72\u8be6\u60c5\u3002",
    "Total:": "\u603b\u8ba1\uff1a",
    "Visible": "\u5929\u5e72\u53ef\u89c1\u4e94\u884c",
    "Branch": "\u5730\u652f",
    "Hidden": "\u85cf\u5e72",
    "Support score": "\u6276\u52a9\u5206\u6570",
    "Pressure score": "\u538b\u529b\u5206\u6570",
    "Support ratio": "\u6276\u52a9\u6bd4\u4f8b",
    "Roots in hidden stems": "\u85cf\u5e72\u4e2d\u7684\u6839\u6c14",
    "Direction": "\u65b9\u5411",
    "Forward": "\u987a\u884c",
    "Backward": "\u9006\u884c",
    "Starting age": "\u8d77\u8fd0\u5e74\u9f84",
    "Start date": "\u8d77\u8fd0\u65e5\u671f",
    "Pillar": "\u67f1",
    "Ten Gods": "\u5341\u795e",
    "Calendar years": "\u516c\u5386\u5e74\u4efd",
    "Nominal ages": "\u865a\u5c81",
    "Year": "\u5e74\u4efd",
    "Year pillar": "\u5e74\u67f1",
    "Stem element": "\u5929\u5e72\u4e94\u884c",
    "Calculation Notes": "\u8ba1\u7b97\u8bf4\u660e",
    "Traditional cultural learning and reflection": "\u4f20\u7edf\u6587\u5316\u5b66\u4e60\u4e0e\u4e2a\u4eba\u53cd\u601d",
    "Intermediate support balance": "\u6276\u52a9\u7a0b\u5ea6\u4e2d\u7b49",
    "Preliminarily strong": "\u521d\u6b65\u5224\u65ad\u4e3a\u504f\u5f3a",
    "Preliminarily weak": "\u521d\u6b65\u5224\u65ad\u4e3a\u504f\u5f31",
    (
        "Preliminary structural heuristic. Visible stems count once, hidden "
        "stems fractionally, and the Month Branch receives extra weight. "
        "This does not fully model solar-term seasonal strength, stem "
        "combinations, transformations, or all classical schools. It must "
        "not be treated as a definitive traditional verdict."
    ): (
        "\u8fd9\u662f\u521d\u6b65\u7684\u547d\u76d8\u7ed3\u6784\u4f30\u7b97\u65b9\u6cd5\u3002"
        "\u663e\u5e72\u6309\u4e00\u6b21\u8ba1\u6570\uff0c\u85cf\u5e72\u6309\u6bd4\u4f8b\u8ba1\u6570\uff0c"
        "\u6708\u652f\u53e6\u7ed9\u4e88\u66f4\u9ad8\u6743\u91cd\u3002\u8be5\u65b9\u6cd5\u672a\u5b8c\u6574\u6a21\u62df\u8282\u6c14\u5b63\u8282\u65fa\u8870\u3001\u5929\u5e72\u7ec4\u5408\u3001"
        "\u4e94\u884c\u8f6c\u5316\u6216\u6240\u6709\u4f20\u7edf\u6d41\u6d3e\u7684\u89c4\u5219\uff0c\u4e0d\u5e94\u89c6\u4e3a\u6700\u7ec8\u7684\u4f20\u7edf\u547d\u7406\u7ed3\u8bba\u3002"
    ),
    "Preliminary candidates derived from the strength heuristic":
        "\u6839\u636e\u65e5\u4e3b\u5f3a\u5f31\u4f30\u7b97\u5f97\u51fa\u7684\u521d\u6b65\u5019\u9009\u4e94\u884c",
    (
        "The preliminary chart heuristic indicates less structural support "
        "for the Day Master. Its own element and its resource element are "
        "listed as candidates for further review."
    ): (
        "\u521d\u6b65\u547d\u76d8\u4f30\u7b97\u663e\u793a\uff0c\u65e5\u4e3b\u5f97\u5230\u7684\u7ed3\u6784\u6027\u6276\u52a9\u66f4\u5c11\u3002"
        "\u65e5\u4e3b\u81ea\u8eab\u4e94\u884c\u53ca\u751f\u52a9\u65e5\u4e3b\u7684\u5370\u661f\u4e94\u884c\u5217\u4e3a\u8fdb\u4e00\u6b65\u7814\u7a76\u7684\u5019\u9009\u3002"
    ),
    (
        "The preliminary chart heuristic indicates substantial structural "
        "support. Output, wealth, and officer elements are listed as "
        "candidates for further review."
    ): (
        "\u521d\u6b65\u547d\u76d8\u4f30\u7b97\u663e\u793a\uff0c\u65e5\u4e3b\u5f97\u5230\u7684\u7ed3\u6784\u6027\u6276\u52a9\u66f4\u591a\u3002"
        "\u98df\u4f24\u3001\u8d22\u661f\u53ca\u5b98\u6740\u76f8\u5173\u4e94\u884c\u5217\u4e3a\u8fdb\u4e00\u6b65\u7814\u7a76\u7684\u5019\u9009\u3002"
    ),
    (
        "The preliminary support balance is intermediate. No single element "
        "can be confidently selected from this heuristic alone."
    ): (
        "\u521d\u6b65\u4f30\u7b97\u663e\u793a\uff0c\u65e5\u4e3b\u6276\u52a9\u7a0b\u5ea6\u5904\u4e8e\u4e2d\u95f4\u72b6\u6001\u3002"
        "\u4ec5\u51ed\u6b64\u65b9\u6cd5\uff0c\u65e0\u6cd5\u6709\u628a\u63e1\u5730\u9009\u5b9a\u67d0\u4e00\u79cd\u4e94\u884c\u3002"
    ),
    (
        "A full traditional useful-element assessment may require solar-term "
        "seasonal strength, chart structure, combinations, climate "
        "considerations, and school-specific rules. Element counts alone "
        "cannot establish a definitive favorable element."
    ): (
        "\u5b8c\u6574\u7684\u4f20\u7edf\u559c\u7528\u795e\u5206\u6790\u53ef\u80fd\u9700\u8981\u8003\u8651\u8282\u6c14\u65fa\u8870\u3001\u547d\u5c40\u7ed3\u6784\u3001\u5e72\u652f\u7ec4\u5408\u3001"
        "\u8c03\u5019\u56e0\u7d20\u53ca\u4e0d\u540c\u6d41\u6d3e\u7684\u89c4\u5219\u3002\u5355\u51ed\u4e94\u884c\u6570\u91cf\uff0c\u4e0d\u80fd\u786e\u5b9a\u6700\u7ec8\u7684\u559c\u7528\u4e94\u884c\u3002"
    ),
    (
        "This preliminary heuristic identifies substantial structural "
        "support for the Day Master. It is not a fixed personality judgment "
        "or a guarantee."
    ): (
        "\u8fd9\u9879\u521d\u6b65\u4f30\u7b97\u663e\u793a\u65e5\u4e3b\u5f97\u5230\u66f4\u591a\u7ed3\u6784\u6027\u6276\u52a9\u3002"
        "\u8fd9\u4e0d\u662f\u5bf9\u4e2a\u4eba\u6027\u683c\u7684\u56fa\u5b9a\u5224\u65ad\uff0c\u4e5f\u4e0d\u6784\u6210\u4efb\u4f55\u4fdd\u8bc1\u3002"
    ),
    (
        "This preliminary heuristic identifies less structural support for "
        "the Day Master. It does not mean personal weakness or predict poor "
        "outcomes."
    ): (
        "\u8fd9\u9879\u521d\u6b65\u4f30\u7b97\u663e\u793a\u65e5\u4e3b\u5f97\u5230\u7684\u7ed3\u6784\u6027\u6276\u52a9\u66f4\u5c11\u3002"
        "\u8fd9\u4e0d\u4ee3\u8868\u4e2a\u4eba\u80fd\u529b\u66f4\u5f31\uff0c\u4e5f\u4e0d\u9884\u793a\u4e0d\u826f\u7ed3\u679c\u3002"
    ),
    (
        "This preliminary heuristic finds an intermediate support balance. "
        "It does not establish that every area of life is balanced."
    ): (
        "\u8fd9\u9879\u521d\u6b65\u4f30\u7b97\u663e\u793a\u65e5\u4e3b\u6276\u52a9\u7a0b\u5ea6\u5904\u4e8e\u4e2d\u95f4\u72b6\u6001\u3002"
        "\u8fd9\u5e76\u4e0d\u610f\u5473\u7740\u4eba\u751f\u7684\u6bcf\u4e2a\u65b9\u9762\u90fd\u5904\u4e8e\u5e73\u8861\u72b6\u6001\u3002"
    ),
    (
        "BaZi is a traditional Chinese interpretive system, not a "
        "scientifically validated method for predicting personality, career "
        "outcomes, relationships, health, wealth, or future events. These "
        "descriptions are for cultural learning and personal reflection, "
        "not professional advice."
    ): (
        "\u516b\u5b57\u662f\u4e2d\u56fd\u4f20\u7edf\u8be0\u91ca\u4f53\u7cfb\uff0c\u5e76\u975e\u7ecf\u8fc7\u79d1\u5b66\u9a8c\u8bc1\u7684\u9884\u6d4b\u65b9\u6cd5\uff0c\u4e0d\u80fd\u53ef\u9760\u5730"
        "\u9884\u6d4b\u6027\u683c\u3001\u4e8b\u4e1a\u3001\u5173\u7cfb\u3001\u5065\u5eb7\u3001\u8d22\u5bcc\u6216\u672a\u6765\u4e8b\u4ef6\u3002\u76f8\u5173\u5185\u5bb9\u4ec5\u4f9b\u4f20\u7edf\u6587\u5316"
        "\u5b66\u4e60\u4e0e\u4e2a\u4eba\u53cd\u601d\uff0c\u4e0d\u6784\u6210\u4e13\u4e1a\u5efa\u8bae\u3002"
    ),
    (
        "Annual influences use the Li Chun year-pillar convention and "
        "classify the year's Heavenly Stem relative to the Day Master. "
        "They are not a complete natal-chart interaction analysis or "
        "predictions of specific events."
    ): (
        "\u6d41\u5e74\u5206\u6790\u91c7\u7528\u7acb\u6625\u6362\u5e74\u67f1\u7684\u89c4\u5219\uff0c\u5e76\u4ee5\u65e5\u4e3b\u4e3a\u53c2\u7167\u5206\u6790\u5f53\u5e74\u5929\u5e72\u7684\u5341\u795e\u5173\u7cfb\u3002"
        "\u8fd9\u4e0d\u662f\u5b8c\u6574\u7684\u539f\u5c40\u4e92\u52a8\u5206\u6790\uff0c\u4e5f\u4e0d\u4ee3\u8868\u5bf9\u5177\u4f53\u4e8b\u4ef6\u7684\u9884\u6d4b\u3002"
    ),
    "Luck Pillars could not be calculated for this chart.":
        "\u65e0\u6cd5\u8ba1\u7b97\u6b64\u547d\u76d8\u7684\u5927\u8fd0\u3002",
    (
        "Luck Pillars use the installed lunar_python calculation. When birth "
        "time is unknown, noon is used as a placeholder, so the starting "
        "timing is approximate."
    ): (
        "\u5927\u8fd0\u4f7f\u7528\u5f53\u524d\u5b89\u88c5\u7684 lunar_python \u8fdb\u884c\u8ba1\u7b97\u3002\u51fa\u751f\u65f6\u95f4\u672a\u77e5\u65f6\uff0c"
        "\u4f1a\u4ee5\u6b63\u5348\u4f5c\u4e3a\u5360\u4f4d\u65f6\u95f4\uff0c\u56e0\u6b64\u8d77\u8fd0\u65f6\u95f4\u4ec5\u4e3a\u8fd1\u4f3c\u503c\u3002"
    ),
    (
        "Luck Pillar direction needs a male/female selection under this "
        "traditional calculation convention. No direction was assumed for "
        "the supplied gender."
    ): (
        "\u6309\u7167\u6b64\u4f20\u7edf\u8ba1\u7b97\u89c4\u5219\uff0c\u5927\u8fd0\u987a\u9006\u9700\u8981\u9009\u62e9\u7537\u6027\u6216\u5973\u6027\u3002"
        "\u5bf9\u4e8e\u5f53\u524d\u63d0\u4f9b\u7684\u6027\u522b\uff0c\u7cfb\u7edf\u672a\u64c5\u81ea\u5047\u5b9a\u5927\u8fd0\u65b9\u5411\u3002"
    ),
    (
        "Birth time was not provided. The Hour Pillar is unavailable. Noon "
        "is used only as a placeholder for calculations that need a time; "
        "time-dependent results may differ from the true chart."
    ): (
        "\u672a\u63d0\u4f9b\u51fa\u751f\u65f6\u95f4\uff0c\u56e0\u6b64\u65e0\u6cd5\u786e\u5b9a\u65f6\u67f1\u3002\u5bf9\u4e8e\u9700\u8981\u65f6\u95f4\u7684\u8ba1\u7b97\uff0c"
        "\u4ec5\u4ee5\u6b63\u5348\u4f5c\u4e3a\u5360\u4f4d\u65f6\u95f4\uff1b\u4e0e\u65f6\u95f4\u76f8\u5173\u7684\u7ed3\u679c\u53ef\u80fd\u4e0d\u540c\u4e8e\u771f\u5b9e\u547d\u76d8\u3002"
    ),
    (
        "Birthplace was not provided. Historical time-zone and "
        "location-dependent verification has not been performed."
    ): (
        "\u672a\u63d0\u4f9b\u51fa\u751f\u5730\u70b9\uff0c\u56e0\u6b64\u5c1a\u672a\u8fdb\u884c\u5386\u53f2\u65f6\u533a\u53ca\u5730\u70b9\u76f8\u5173\u7684\u6838\u9a8c\u3002"
    ),
    (
        "Birth time is interpreted as local civil time. Historical "
        "time-zone verification has not been automated."
    ): (
        "\u51fa\u751f\u65f6\u95f4\u6309\u5f53\u5730\u6c11\u7528\u65f6\u95f4\u89e3\u91ca\u3002\u76ee\u524d\u5c1a\u672a\u81ea\u52a8\u6838\u9a8c\u5386\u53f2\u65f6\u533a\u89c4\u5219\u3002"
    ),
    (
        "Traditional BaZi relationships are presented for cultural learning "
        "and reflection. Ten Gods and annual influences are symbolic "
        "frameworks, not scientific personality assessments or predictions."
    ): (
        "\u4f20\u7edf\u516b\u5b57\u5173\u7cfb\u4ec5\u7528\u4e8e\u6587\u5316\u5b66\u4e60\u4e0e\u4e2a\u4eba\u53cd\u601d\u3002\u5341\u795e\u548c\u6d41\u5e74\u5f71\u54cd\u5c5e\u4e8e\u8c61\u5f81\u6027"
        "\u8be0\u91ca\u6846\u67b6\uff0c\u5e76\u975e\u79d1\u5b66\u7684\u6027\u683c\u8bc4\u4f30\u6216\u9884\u6d4b\u3002"
    ),
    'This overview connects traditional BaZi symbolism to practical questions about everyday life. It is a cultural reflection tool, not a fixed description of your personality or a prediction of future events.': '这份概览将传统八字象征与日常生活中的实际问题联系起来。这是一种用于文化反思的工具，而不是对你个性的固定定义或对未来事件的预测。',
    'Wood symbolizes growth, learning, planning, and a forward-looking approach. Reflect on how you set goals and respond when plans change.': '木象征成长、学习、规划和着眼未来的思维方式。可以反思自己如何设定目标，以及在计划变化时如何应对。',
    'Reflect on your goals, adaptability, and the balance between persistence and flexibility.': '反思自己的目标、适应能力，以及坚持与灵活调整之间的平衡。',
    'Which tasks use your skills well, based on your actual experience and interests?': '根据你的实际经验和兴趣，哪些任务能更好地发挥你的技能？',
    'Wood symbolism is linked with development, education, planning, and helping ideas grow. Consider where you can learn, organize, or build something useful.': '木的象征与发展、教育、规划以及促进想法成长有关。可以思考自己可以在哪些方面学习、组织或建立有益的事物。',
    'Wood symbolism emphasizes shared growth, patience, and room for each person to develop. Healthy relationships also need listening and mutual respect.': '木的象征强调共同成长、耐心以及给予每个人发展的空间。健康的关系也需要倾听与相互尊重。',
    'What need or expectation could you communicate more clearly in an important relationship?': '在一段重要的关系中，你可以更清楚地表达哪一项需求或期待？',
    'Choose one practical goal based on your circumstances, rather than relying on a chart alone.': '根据自己的实际情况选择一个可行的目标，不要只依赖命盘。',
    'Structural occurrence count: each visible stem, branch element, and hidden stem is counted separately. A branch element is a simplified representation of the branch, not a substitute for its hidden stems. These totals and percentages are descriptive only; they do not establish Day Master strength or favorable elements.': '结构出现次数：每个可见天干、地支五行和藏干分别计数。地支五行只是对地支的简化表示，不能代替其藏干。这些总数和百分比仅用于描述，不能用来确定日主强弱或喜用五行。',
    'years': '年',
    'months': '个月',
    'days': '天',
    'Birth time': '出生时间',
}


@register.filter
def localize_bazi(value, language="en"):
    if value is None:
        return ""

    text = str(value)

    if language != "zh":
        return text

    if text in TEXT:
        return TEXT[text]
    if text in ELEMENTS:
        return ELEMENTS[text]
    if text in POLARITY:
        return POLARITY[text]
    if text in PILLARS:
        return PILLARS[text]
    if text in ZODIAC:
        return ZODIAC[text]
    if text in TEN_GODS:
        return TEN_GODS[text]

    return text
