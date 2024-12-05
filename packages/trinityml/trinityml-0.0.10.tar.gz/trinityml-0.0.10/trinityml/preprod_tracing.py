from langfuse import Langfuse
    
from datetime import datetime
import os


def connect(secret_key=None, public_key=None, host=None):
    """
    Function Overview:

        This function establishes a connection with the trinity platform using the provided credentials.
        Input Parameters:

        Mandatory Parameters:
            secret_key: A string representing the secret key for the trinity platform.
                Example: secret_key = "your_secret_key"
            public_key: A string representing the public key for the trinity platform.
                Example: public_key = "your_public_key"
            host: A string representing the host URL for the trinity platform.
                Example: host = "https://api.trinity.com"

    Important Notes:

        Required Data:
            The secret_key, public_key, and host parameters are mandatory for the function to run.
        
    Example of calling the function with all the input parameters:
    # Input parameters
        secret_key = "your_secret_key"
        public_key = "your_public_key"
        host = "https://api.trinity.com"

    # Function call
        connect(secret_key=secret_key, public_key=public_key, host=host)
    
    ##  Please contact Giggso support team if you face any issue while running this script on local ##
    """
    try:
        if not secret_key or not public_key or not host:
            print("Secret key, public key, and host are required. Please make sure you have provided all the necessary parameters.")
            return
        os.environ["TRINITY_SECRET_KEY"] = secret_key
        os.environ["TRINITY_PUBLIC_KEY"] = public_key
        os.environ["TRINITY_HOST"] = host
        try:
            langfuse = Langfuse(
                secret_key=os.environ.get("TRINITY_SECRET_KEY"),
                public_key=os.environ.get("TRINITY_PUBLIC_KEY"),
                host=os.environ.get("TRINITY_HOST")
            )
            langfuse.client.trace.list()
            print(f"Connected to Trinity platform with the following credentials: Secret Key: {secret_key}, Public Key: {public_key}, Host: {host}")
            return
        except:
            print("An error occurred while attempting to connect to the Trinity platform. Please ensure that the input credentials are correct.")
            return
        
    except Exception as e:
        print(f"Error occurred: {e}")


def record(experiment_name=None,questions=None, contexts=None, generated_prompts=None, answers=None, ground_truths=None, model_temperature=None, top_k=None, model_name=None, prompt_template=None,model_provider=None,API_key=None,maxToken=None,top_p=None,system_prompt=None,user_prompt=None,llm_endpoint=None,promptName=None,apiVersion=None,deploymentName=None):
    """
    Function Overview:

        This function evaluates a series of questions using various spans, depending on the availability of input data.
        Input Parameters:

        Mandatory Parameters:
            experiment_name: A string representing the name of the experiment.
                Example: experiment_name = "Experiment_1"
            questions: A list of strings containing the questions to be evaluated.
                Example: questions = ["What is the capital of France?", "Who wrote '1984'?"]
            answers: A list of strings containing the corresponding answers.
                Example: answers = ["Paris", "George Orwell"]

        Optional Parameters:
            contexts: A list of strings providing context for each question.
                Example: contexts = ["Capital cities of European countries", "Famous books and their authors"]
            generated_prompts: A list of strings with prompts generated for each question.
                Example: generated_prompts = ["Tell me about European capitals.", "Discuss authors of classic literature."]
            ground_truths: A list of strings with the correct answers or ground truths.
                Example: ground_truths = ["Paris", "George Orwell"]

        Configuration Parameters:
            model_temperature: A string representing the model temperature.
                Example: model_temperature = "0.3"
            top_k: A string indicating the top-K sampling for the model.
                Example: top_k = "5"
            model_name: A string specifying the model name to be used.
                Example: model_name = "GPT-3"
            prompt_template: A string with the template to be used for prompts.
                Example: prompt_template = "Describe the following topic:"

    Important Notes:

        Required Data:
            The experiment_name, questions, and answers parameters are mandatory for the function to run.
        Enhanced Evaluation:
            Including contexts, ground_truths, and generated_prompts can enhance the evaluation metrics, though they are optional.
        
    Example of calling the function with all the input parameters:
     # Input parameters
        experiment_name = "Experiment_1"
        questions = ["What is the capital of France?", "Who wrote '1984'?"]
        contexts = ["Capital cities of European countries", "Famous books and their authors"]
        generated_prompts = ["Tell me about European capitals.", "Discuss authors of classic literature."]
        answers = ["Paris", "George Orwell"]
        ground_truths = ["Paris", "George Orwell"]
        model_temperature = "0.3"
        top_k = "5"
        model_name = "GPT-3"
        prompt_template = "Describe the following topic:"

    # Function call
        record(
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
    
    ##  Please contact Giggso support team if you face any issue while running this script on local ##
    """
    model_temperature = model_temperature if model_temperature is not None else 1
    top_k = top_k if top_k is not None else 1
    top_p = top_p if top_p is not None else 1
    maxToken = maxToken if maxToken is not None else 1000 

    if not experiment_name:
        print("Experiment name is required. Please make sure you have provided all the necessary parameters.")
        return
    

    if not model_name or not prompt_template or not model_provider or not API_key or not promptName or not apiVersion:
        print("Model parameters (model_name, prompt_template, temperature, model_provider,, API_key, ) are required. Please make sure you have provided all the necessary parameters.")
        return
    secret_key = None
    public_key = None
    host = None
    try:
        secret_key = os.environ.get("TRINITY_SECRET_KEY")
        public_key = os.environ.get("TRINITY_PUBLIC_KEY")
        host = os.environ.get("TRINITY_HOST")
    except Exception as e:
        print("An error occurred while connecting to the Trinity platform. Please ensure that the Trinity environment variables (TRINITY_SECRET_KEY, TRINITY_PUBLIC_KEY, TRINITY_HOST) are set, or test the connectivity using the 'connect' function provided by Trinity.")
        return

    if secret_key == None or public_key == None or host == None:
        print("An error occurred while connecting to the Trinity platform. Please ensure that the Trinity environment variables (TRINITY_SECRET_KEY, TRINITY_PUBLIC_KEY, TRINITY_HOST) are set, or test the connectivity using the 'connect' function provided by Trinity.")
        return
    
    if secret_key == "" or public_key == "" or host == "":
        print("Secret key, public key, and host are required. Please make sure you have provided all the necessary parameters.")
        return

    try:
        langfuse = Langfuse(
            secret_key= secret_key,
            public_key=public_key,
            host=host
        )
        langfuse.client.trace.list()
    except Exception as e:
        print("An error occurred while connecting to the Trinity platform. Please ensure that the Trinity environment variables (TRINITY_SECRET_KEY, TRINITY_PUBLIC_KEY, TRINITY_HOST) are set, or test the connectivity using the 'connect' function provided by Trinity.")
        return

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
    trace_name = experiment_name

    try:
        trace = langfuse.trace(name=trace_name, metadata={
            "ExperimentName": trace_name,
            "Timestamp": timestamp,
            "ModelTemperature": model_temperature,
            "TopK": top_k,
            "PromptTemplate": prompt_template,
            "ModelName": model_name,
            "ModelProvider": model_provider,
            "APIKey": API_key,
            "TotalOutputTokenCount": maxToken,
            "TopP": top_p,
            "SystemPrompt": system_prompt,
            "UserPrompt": user_prompt,
            "llm_endpoint": llm_endpoint,
            "PromptName": promptName,
            "apiVersion": apiVersion,
            "deploymentName": deploymentName
        })
        
        if questions != None and answers != None:
            trace.span(name="agent", input={"questions": questions}, output={"answers": answers})
            print(
                "Run recorded successfully with the following details:"
                + "\n Experiment Name: " + experiment_name
                + "\n Timestamp: " + timestamp
                + "\n Record Count: " + str(len(questions))
                + "\n Model Name: " + model_name
                + "\n Model Temperature: " + model_temperature
                + "\n Top K: " + top_k
                + "\n Questions: " + str(len(questions))
                + "\n Answers: " + str(len(answers))    
            )
            
            if contexts != None:
                trace.span(name="retriever", input={"contexts": contexts})
                print(" Contexts: " + str(len(contexts)))
            else:
                print(" Contexts: " + str(contexts))
            
            if generated_prompts != None:
                trace.span(name="generated_prompt", input={"generated_prompts": generated_prompts})
                print( " Generated prompts: " + str(len(generated_prompts)))
            else:
                print( " Generated prompts: " + str(generated_prompts))

            if ground_truths != None:
                trace.span(name="ground_truth", input={"ground_truths": ground_truths})
                print(" Ground truths: " + str(len(ground_truths)))
            else:
                print(" Ground truths: " + str(ground_truths))

            if prompt_template != None:
                print(" Prompt template: " + prompt_template)
            else:
                print(" Prompt template: " + str(prompt_template))
        else:
            print("No records to save. Please ensure that you have provided questions and answers.")
            return
    
    except Exception as e:
        print(f"Error occurred: {e}")

    
