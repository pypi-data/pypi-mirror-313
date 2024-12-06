import spacy
from spacy import Language
from spacy.matcher import Matcher


class CancelPrompt:
    nlp: Language

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = Matcher(self.nlp.vocab)

    def is_cancel_text(self, text: str):
        # Define relevant keywords
        cancel_keywords = ["cancel", "terminate", "abort", "stop"]
        request_keywords = ["request", "order", "application", "task"]

        if text.strip().lower() == 'cancel' or text.strip().lower() == 'please cancel': return True

        # Function to check for variations
        def check_variation():
            doc = self.nlp(text.lower())
            # Look for cancel-related and request-related keywords
            has_cancel_keyword = any(token.text in cancel_keywords for token in doc)
            has_request_keyword = any(token.text in request_keywords for token in doc)
            return has_cancel_keyword and has_request_keyword

        return check_variation()

    def is_incomplete_booking(self, sentence):
        # Define patterns for variations of "please book a"
        patterns = [
            [{"LOWER": "please", "OP": "?"}, {"LOWER": "book"}, {"POS": "DET"}],
            [{"LOWER": "could"}, {"LOWER": "you"}, {"LOWER": "kindly"}, {"LOWER": "book"}, {"POS": "DET"}],
            [{"LOWER": "kindly"}, {"LOWER": "book"}, {"POS": "DET"}],
            [{"LOWER": "can"}, {"LOWER": "you"}, {"LOWER": "book"}, {"POS": "DET"}],
            [{"LOWER": "reserve"}, {"POS": "DET"}],
            [{"LOWER": "arrange"}, {"POS": "DET"}],
            [{"LOWER": "secure"}, {"POS": "DET"}],
        ]

        self.matcher.add("BOOK_REQUEST", patterns)

        # Test the matcher on sample text
        doc = self.nlp(sentence)
        matches = self.matcher(doc)

        for match_id, start, end in matches:
            val = "Match found:", doc[start:end].text
            return True

        # booking_keywords = ["book", "reserve"]
        # request_keywords = ["please", "can you", "could you please"]
        #
        # # Function to check if text matches
        # def check_variation(text):
        #     doc = self.nlp(text.lower())
        #     # Look for booking-related and polite keywords
        #     has_booking_keyword = any(token.text in booking_keywords for token in doc)
        #     has_request_keyword = any(token.text in request_keywords for token in doc)
        #     return has_booking_keyword or has_request_keyword
        #
        # return check_variation(sentence)
