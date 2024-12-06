[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![pipeline status](https://git.uni-luebeck.de/its/anomed/challenge/badges/main/pipeline.svg?ignore_skipped=true)
![coverage](https://git.uni-luebeck.de/its/anomed/challenge/badges/main/coverage.svg?job=run_tests)

# Challenge

A library aiding to create challenges for the AnoMed competition platform.

# Usage Example

```python
import challenge
import challenge_server
import numpy as np
from challenge import InMemoryNumpyArrays


example_challenge = challenge.SupervisedLearningMIAChallenge(
    training_data=InMemoryNumpyArrays(X=np.arange(70), y=np.arange(70)),
    tuning_data=InMemoryNumpyArrays(X=np.arange(30), y=np.arange(30)),
    validation_data=InMemoryNumpyArrays(X=np.arange(20), y=np.arange(20)),
    anonymizer_evaluator=challenge.strict_binary_accuracy,
    MIA_evaluator=challenge.evaluate_MIA,
)
app = challenge_server.supervised_learning_MIA_challenge_server_factory(
    example_challenge
)
```
