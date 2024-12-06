from datetime import datetime, timedelta
import re


class DateTime:
    def regex_extract(self, user_input):
        # Define regex patterns for different date formats
        date_patterns = [
            r"\b\d{2}/\d{2}/\d{4}\b",  # DD/MM/YYYY
            r"\b\d{2}-\d{2}-\d{4}\b",  # MM-DD-YYYY
            r"\b\d{4}\.\d{2}\.\d{2}\b",  # YYYY.MM.DD
            r"\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b"
            # Month DD, YYYY
        ]

        # Combine all patterns into one
        combined_pattern = "|".join(date_patterns)

        # Find all matches
        matches = re.search(combined_pattern, user_input)

        if not matches:
            extended_date_patterns = [
                r"\b\d{2} \w+ \d{4}\b",  # DD Month YYYY
                r"\b\d{4}-\d{2}-\d{2}\b",  # YYYY-MM-DD
                r"\b\d{2}/\d{2}/\d{2}\b",  # MM/DD/YY
                *date_patterns  # Include the previous patterns
            ]

            combined_pattern = "|".join(extended_date_patterns)

            # Find all matches
            matches = re.search(combined_pattern, user_input)
            if not matches:
                return self.adverbs_to_date(user_input)
            else:
                return matches.group(0)
        else:
            return matches.group(0)

    def adverbs_to_date(self, adverb):
        date_map = {
            "today": datetime.now(),
            "tomorrow": datetime.now() + timedelta(days=1),
            "day after tomorrow": datetime.now() + timedelta(days=2)
        }
        matches = re.findall(r"\b(today|tomorrow|day after tomorrow)\b", adverb, flags=re.IGNORECASE)
        try:
            if not matches: return ""
            return date_map[matches[0]]
        except KeyError:
            return ""

    def is_valid(self, date):
        pass
