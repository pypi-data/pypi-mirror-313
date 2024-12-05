## Installation
To install the Trinity package, run the following command:
```
pip install trinityml
```

## Setup the Environment Variable
```
export TRINITY_SECRET_KEY="your_secret_key"
export TRINITY_PUBLIC_KEY="your_public_key"
export TRINITY_HOST="http://your_trinity_host"
```

## Record the Experiment
To use the record function, ensure that you have properly set up your environment and then call the function as shown below:

```
# Import the Trinity package
import trinityml

# Call the record() function
trinityml.record(
    experiment_name=experiment_name,
    questions=questions,
    contexts=contexts,
    generated_prompts=generated_prompts,
    answers=answers,
    ground_truths=ground_truths,
    model_temperature=model_temperature,
    top_k=top_k,
    model_name=model_name,
    prompt_template=prompt_template
)
