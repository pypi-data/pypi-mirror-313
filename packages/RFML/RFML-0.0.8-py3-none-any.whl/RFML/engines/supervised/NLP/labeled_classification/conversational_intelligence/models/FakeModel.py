from RFML.core.Results import PredictResult, ResultType


class FakeModel:
    @staticmethod
    def predict(input_text):

        if input_text == "hi" or input_text == "hello":
            return PredictResult(
                label="greet",
                probability=1.0,
                message="hi there !",
                input_text=input_text
            )
        elif input_text == "time" or input_text == "now":  # "book a room joba from 10am to 11pm":
            return PredictResult(
                label="time",
                probability=1.0,
                message="10:15am",
                input_text=input_text
            )
        elif input_text == "book":  # "book a room joba from 10am to 11pm":
            return PredictResult(
                label="book",
                probability=1.0,
                message="Please wait.. ",
                route="rf-ce-flight_booking",  # rf-m1-npl-extractor
                input_text=input_text
            )
        else:
            return PredictResult(
                label="default",
                probability=1.0,
                message="I do not understand",
                result_type=ResultType.do_not_understand,
                input_text=input_text
            )

            # book = RFML(cognitive=CommandExtractor(model="rf-nexus-classifier"))
            # msg = book.predict("book a room JOBA from 10am to 11am").message
