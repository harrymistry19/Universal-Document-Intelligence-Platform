from app.core.source_detector import detect_source
from app.extractors.html_static import extract as extract_static
from app.extractors.pdf_extractor import extract as extract_pdf
from app.extractors.image_ocr import extract as extract_image
from app.processors.formatter import format_data
from app.storage.database import save
from app.storage.metadata import log_run
from app.logger import logger


def run(input_value):
    logger.info(f"Pipeline started for input: {input_value}")

    source = detect_source(input_value)

    if source == "url":
        logger.info("Detected source: URL")
        data = extract_static(input_value)

    elif source == "pdf":
        logger.info("Detected source: PDF")
        data = extract_pdf(input_value)

    elif source == "image":
        logger.info("Detected source: IMAGE")
        data = extract_image(input_value)

    else:
        logger.error("Unsupported source type")
        raise ValueError("Unsupported source")

    df = format_data(data, source)

    save(df)
    log_run(source, input_value)

    logger.info("Pipeline completed successfully")

    return df
