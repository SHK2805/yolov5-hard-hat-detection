# YOLOv5 Hard Hat Detection
* This project uses YOLOv5 to detect hard hats in images and videos.

### Technologies
* The project is built using the following technologies:
  * Python
  * Flask
  * YOLOv5

### Steps

#### Install dependencies
* Install the dependencies using the following command
```bash
pip install -r requirements.txt
```

#### Data
* Before running the project you need to get the following from roboflow
  * API key
    * The API key is added to the file roboflow_api_key.yaml as ROBOFLOW_API_KEY
    * **DO NOT ADD THIS FILE TO THE GIT**. Add this to the .gitignore file
    ```yaml
    # roboflow api key
    roboflow_api_key:
        ROBOFLOW_API_KEY: "your_roboflow_api_key"
    ```
  * workspace name
  * project name
  * data version
  * data format

#### Data 
* The data is downloaded from the roboflow source and saved to the artifacts folder
* The data is saved to the folder artifacts\data_ingestion
* The data is transformed and copied to the artifacts\data_transformation folder
* From the below structure the data is saved to the artifacts folder
data_ingestion
│
├── test
│   ├── images
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── labels
│       ├── image1.txt
│       ├── image2.txt
│       └── ...
│
├── train
│   ├── images
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── labels
│       ├── image1.txt
│       ├── image2.txt
│       └── ...
│
├── valid
│   ├── images
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── labels
│       ├── image1.txt
│       ├── image2.txt
│       └── ...
│
└── data.yaml

* Data is transformed to the below structure
data_transformation
│
├── images
│   ├── test
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── train
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── valid
│       ├── image1.jpg
│       ├── image2.jpg
│       └── ...
│
└── labels
    ├── test
    │   ├── image1.txt
    │   ├── image2.txt
    │   └── ...
    ├── train
    │   ├── image1.txt
    │   ├── image2.txt
    │   └── ...
    └── valid
        ├── image1.txt
        ├── image2.txt
        └── ...



#### MLFlow
* Before running the model evaluation pipeline or the model prediction pipeline make sure the **mlflow server is running**
* Make sure the correct **mlflow uri** is set in the config file **config.yaml**
* Add **mlflow** package to the **requirements.txt** file or install it manually using `pip install mlflow`
  * The other packages needed are given in the **requirements.txt** file
* Make sure the mlflow server port does not conflict with any other port on your machine
* Make sure the mlflow server port does not conflict with Flask server port on your machine
* * Run the mlflow server using the following command
* Open the terminal and run the following command
```bash
# mlflow server will be running on localhost: 127.0.0.1 and on port: 8080
mlflow server --host 127.0.0.1 --port 8080
```
* Access the mlflow server at http://127.0.0.1:8080/ 
* Run the MLFlow and Flask in two different terminals

#### Flask
* Before running the Flask API make sure the **Flask server is running**, to run the flask server flollow the below steps
* Make sure the correct **Flask server host ip** and  **Flask server port** is set in the app.py file
```python
# Flask server will be running on localhost:127.0.0.1  and on port: 5000
from flask import Flask
app = Flask(__name__) 
app.run(host="0.0.0.0", port=5000)
```
* Open the terminal and run the following command
```bash
python app.py
```
* Access the flask app at http://127.0.0.1:5000

#### Run
* To run the ML pipeline run the following steps
* Open the flask app at http://127.0.0.1:5000
* Train the model using the train page http://127.0.0.1:5000/train
  * This will trigger the model training and evaluation pipeline from main.py
* Go to the home page to give input values for the model at http://127.0.0.1:5000
* Click on the **predict** button to get the prediction. This will navigate to the result page http://127.0.0.1:5000/result

#### Clean
* To delete the artifacts, logs and mlflow folders run the code in **clean.py**

### Explanation
* The project is a template for a Computer Vision project.
* The implementation is done in the **components** package
* The data ingestion pipeline downloads data from the source and saves it to the artifacts folder
  * Data file extracted to: artifacts\data_ingestion
* The data validation pipeline validates the data
  * Writes the status to artifacts/data_validation/status.txt
* The data transformation pipeline performs the data cleaning and feature engineering. 
  * Performs the train test split and saves the train and test data into csv files
  * The train and test data is saved to 
    * artifacts\data_transformation\
* The model training pipeline gets the train and test data, trains the model using the train data and saves the model in the artifacts folder
  * Data read from: artifacts\data_transformation and artifacts\data_transformation
* The model evaluation pipeline evaluates the model using the test data and saves the metrics in the artifacts folder
  *  Metrics data saved to the JSON file: artifacts\model_evaluation\metrics.json

### YOLO pretrained
* When we initialize a YOLO model, it will by default download the pretrained weights (i.e., yolov5n.pt) to facilitate transfer learning. 
* This is designed to help users achieve better results, as the model can start training from a point where it has already learned certain features.
* But if you're seeking to train a model from scratch without loading any pretrained weights, it's definitely possible. 
* You just need to disable transfer learning while invoking the train function. 
* You can do this by setting the weights parameter to '' (an empty string) in the train method. 
* When the weights parameter is set to '', the YOLO model will then initialize random weights instead of using pretrained weights, hence disabling transfer learning. 
* This applies for classifications tasks as well as other tasks like object detection or segmentation. 
* Do keep in mind though, training a model from scratch could potentially require a lot more training data and considerably more time to converge compared to transfer learning. 
* So make sure your dataset is sufficiently large and diverse.
* We are using the pretrained weights in this project

### ML Pipeline
* The ML pipeline is a sequence of steps that are executed in order to build, train, evaluate, and deploy a machine learning model.
* Below are the steps in the ML pipeline:
1. Data Collection
2. Data Ingestion
3. Data Transformation
4. Model Training
5. Model Evaluation
6. Model Deployment
7. Model Monitoring
8. Model Retraining

### Workflow
* We update the below files in that order to achieve the ML pipeline:
1. config > config.yaml
   1. data_ingestion
   2. data_validation
   3. data_transformation
   4. model_training
2. params.yaml
   1. The hyperparameters for the model
   2. model_training
3. Update the entity
   1. In src > entity > config_entity.py
4. Update the configuration manager 
   1. In src > config > configuration.py
5. Update the components 
   1. In src > components 
      1. data_ingestion.py
      2. data_validation.py
      3. data_transformation.py
      4. model_trainer.py
      5. model_evaluation.py
6. Update the pipeline
    1. In src > pipeline
        1. data_ingestion.py
        2. data_validation.py
        3. data_transformation.py 
        4. model_trainer.py
        5. model_evaluation.py
        6. prediction.py
           1. The prediction pipeline is written only in this file the other above steps are not used in the prediction pipeline
7. Update the main.py
    1. In main.py
8. Predictions
   1. Create the templates folder with the html files
   2. Create the app.py for the Flask API
      1. The app.py file is the main file where we run the Flask API
   3. The index.html file is the main file where we give the input to the model and get the output into the result.html file
   4. There is function /predict  that is index.html that is defined in the app.py file 
   5. The result.html file is the file where we get the output of the model
   6. Follow the below steps to run the app
      1. open the terminal and run the following command
      2. python app.py
      3. The app will run on the localhost http://127.0.0.1/ and port 8080 of the local machine
      4. To access the app go to the http://127.0.0.1:5000
      5. to train the model go to the train page http://127.0.0.1:5000/train
      6. give the values to the form and click on the predict button to get the prediction
