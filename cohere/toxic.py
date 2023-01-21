import cohere
from cohere.classify import Example

co = cohere.Client('3E7E98dyvUvoVm59NG3Z9HWyTuUaKdvNOaxx7u8r')

EXAMPLES = [
  Example("you are hot trash", "Toxic"),
  Example("go to hell", "Toxic"),
  Example("get rekt moron", "Toxic"),
  Example("get a brain and use it", "Toxic"),
  Example("say what you mean, you jerk.", "Toxic"),
  Example("Are you really this stupid", "Toxic"),
  Example("I will honestly kill you", "Toxic"),
  Example("yo how are you", "Benign"),
  Example("I'm curious, how did that happen", "Benign"),
  Example("Try that again", "Benign"),
  Example("Hello everyone, excited to be here", "Benign"),
  Example("I think I saw it first", "Benign"),
  Example("That is an interesting point", "Benign"),
  Example("I love this", "Benign"),
  Example("We should try that sometime", "Benign"),
  Example("You should go for it", "Benign")
]


def is_toxic(message: str) -> bool:
    """Return whether the input message is classified as toxic
    """

    response = co.classify(model='large', inputs=[message], examples=EXAMPLES)

    if response[0].prediction == 'Toxic' and response[0].confidence >= 0.80:
        return True
    else:
        return False
