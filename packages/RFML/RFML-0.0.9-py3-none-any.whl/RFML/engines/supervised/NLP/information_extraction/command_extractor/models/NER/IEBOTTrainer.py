import random
import spacy
from spacy.training import Example


class IEBOTTrainer:
    @staticmethod
    def Train(data, model, vector_db_path: str):
        TRAIN_DATA = data

        # Step 1: Create a blank 'en' model
        nlp = spacy.blank("en")

        # Step 2: Add the Named Entity Recognition (NER) pipeline
        if "ner" not in nlp.pipe_names:
            ner = nlp.add_pipe("ner", last=True)

        # Step 3: Add labels to the NER component
        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

        # Step 4: Prepare the training data as 'Example' objects
        def create_training_data(nlp, train_data):
            examples = []
            for text, annotations in train_data:
                doc = nlp.make_doc(text)  # Create a Doc object from the raw text
                example = Example.from_dict(doc, annotations)  # Create an Example object
                examples.append(example)
            return examples

        # Create training examples
        training_examples = create_training_data(nlp, TRAIN_DATA)

        # Step 5: Start training the NER model
        optimizer = nlp.begin_training()

        # Disable other components (if any) during training
        with nlp.disable_pipes(*[pipe for pipe in nlp.pipe_names if pipe != "ner"]):
            for iteration in range(40):  # Iterate through the training loop
                random.shuffle(training_examples)
                losses = {}

                # Update the model using the training examples
                for batch in spacy.util.minibatch(training_examples, size=8):
                    nlp.update(batch, sgd=optimizer, losses=losses)

                print(f"Iteration {iteration + 1} - Loss: {losses['ner']}")

        # Step 6: Save the trained model to disk
        output_dir = rf"{vector_db_path}\{model}"
        nlp.to_disk(output_dir)
        print(f"Model saved to {output_dir}")
        return True, f"Model training was successful! (Iteration: {iteration + 1}, Loss: {losses['ner']})"  # Success
