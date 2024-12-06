from golean import GoLean
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize the client
    golean = GoLean()  # API key will be read from GOLEAN_API_KEY environment variable

    context = """
    The Industrial Revolution was a period of major industrialization and innovation during the late 18th and early 19th century. 
    The Industrial Revolution began in Great Britain and quickly spread throughout Europe and North America. 
    This era saw the mechanization of agriculture and textile manufacturing and a revolution in power, including steam ships and railroads, 
    that affected social, cultural and economic conditions.
    """
    
    try:
        print("Example 1")
        result = golean.compress_with_context(context=context)
        print(result)
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")

    template = """Read the passage, then answer the question. Only output the exact answer without any extra word or punctuation. 
Passage: {context}
Question: {question}"""

    question = "when was Industrial Revolution started"

    data = {
        "context": context,
        "question": question
    }

    try:
        print("Example 2")
        result = golean.compress_with_template(template=template, data=data)
        print(result)
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()