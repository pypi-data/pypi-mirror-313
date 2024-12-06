# iaparc_inference


[![PyPI version](https://badge.fury.io/py/iaparc-inference.svg)](https://badge.fury.io/py/iaparc-inference)
![PyPI - License](https://img.shields.io/pypi/l/iaparc-inference)


The IA Parc inference plugin allows developers to easily integrate their inference pipeline into IA Parc's production module.   


## Installation

```bash
pip install iaparc-inference
```

## Usage

* If your inference pipeline support batching:
  
    ```python
    from iaparc_inference import IAPListener

    # Define a callback to query your inference pipeline
    # To load your model only once it is recommended to use a class:
    class MyModel:
        def __init__(self, model_path: str):
            ## Load your model in pytorch, tensorflow or any other backend
        
        def batch_query(batch: list, parameters: Optional) -> list:
            ''' execute your pipeline on a batch input
                Note:   "parameters" is an optional argument.
                        It can be used to handle URL's query parameters
                        It's a list of key(string)/value(string) dictionaries
            '''

    if __name__ == '__main__':
        # Initiate your model class
        my_model = MyModel("path/to/my/model")

        # Initiate IAParc listener
        listener = IAPListener(my_model.batch_query)
        # Start the listener
        listener.run()

    ```
* If your inference pipeline **do not** support batching:
  
    ```python
    from iaparc_inference import IAPListener

    # Define a callback to query your inference pipeline
    # To load your model only once it is recommended to use a class:
    class MyModel:
        def __init__(self, model_path: str):
            ## Load your model in pytorch, tensorflow or any other backend
        
        def single_query(one_input, parameters: Optional):
            ''' execute your pipeline on a single input
                Note:   "parameters" is an optional argument.
                        It can be used to handle URL's query parameters
                        It's a key(string)/value(string) dictionary
            '''

    if __name__ == '__main__':
        # Initiate your model class
        my_model = MyModel("path/to/my/model")

        # Initiate IAParc listener
        listener = IAPListener(my_model.single_query, batch=1)  # Note that batch size is forced to 1 here
        # Start the listener
        listener.run()

## Features
* Dynamic batching
* Autoscalling 
* Support both synchronous and asynchronous queries
* Data agnostic


## License
This project is licensed under the Apache License Version 2.0  - see the Apache [LICENSE](https://www.apache.org/licenses/LICENSE-2.0) file for details.