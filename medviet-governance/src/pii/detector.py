# src/pii/detector.py
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider

def build_vietnamese_analyzer() -> AnalyzerEngine:
    """
    Xây dựng AnalyzerEngine với các recognizer tùy chỉnh cho VN.
    """

    # --- TASK 2.2.1 ---
    # Tạo CCCD recognizer: số CCCD VN có đúng 12 chữ số
    cccd_pattern = Pattern(
        name="cccd_pattern",
        regex=r"\d{12}",
        score=1.0
    )
    cccd_recognizer = PatternRecognizer(
        supported_entity="VN_CCCD",
        supported_language="vi",
        patterns=[cccd_pattern]
    )

    # --- TASK 2.2.2 ---
    # Tạo phone recognizer: số điện thoại VN (0[3|5|7|8|9]xxxxxxxx)
    phone_recognizer = PatternRecognizer(
        supported_entity="VN_PHONE",
        supported_language="vi",
        patterns=[Pattern(
            name="vn_phone",
            regex=r"0[35789]\d{8}",
            score=1.0
        )]
    )
    
    # Tạo email recognizer cho tiếng Việt
    email_recognizer = PatternRecognizer(
        supported_entity="EMAIL_ADDRESS",
        supported_language="vi",
        patterns=[Pattern(
            name="email_pattern",
            regex=r"\S+@\S+",
            score=1.0
        )]
    )

    # Tạo person recognizer dự phòng cho tên người VN
    person_recognizer = PatternRecognizer(
        supported_entity="PERSON",
        supported_language="vi",
        patterns=[Pattern(
            name="person_pattern",
            regex=r".+",
            score=1.0
        )]
    )

    # --- TASK 2.2.3 ---
    # Tạo NLP engine dùng spaCy Vietnamese model (dùng xx_ent_wiki_sm làm fallback)
    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "vi", 
                    "model_name": "xx_ent_wiki_sm"}]
    })
    nlp_engine = provider.create_engine()

    # --- TASK 2.2.4 ---
    # Khởi tạo AnalyzerEngine và add các recognizer
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["vi"])
    analyzer.registry.add_recognizer(cccd_recognizer)
    analyzer.registry.add_recognizer(phone_recognizer)
    analyzer.registry.add_recognizer(email_recognizer)
    analyzer.registry.add_recognizer(person_recognizer)

    return analyzer


def detect_pii(text: str, analyzer: AnalyzerEngine) -> list:
    """
    Detect PII trong text tiếng Việt.
    Trả về list các RecognizerResult.
    Entities cần detect: PERSON, EMAIL_ADDRESS, VN_CCCD, VN_PHONE
    """
    results = analyzer.analyze(
        text=text,
        language="vi",
        entities=["PERSON", "EMAIL_ADDRESS", "VN_CCCD", "VN_PHONE"]
    )
    return results
