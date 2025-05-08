<!-- Project title -->

Heart Disease Prediction

<!-- create env -->
conda create -p venv python==3.9 -y

<!-- requirements.txt -->
requirements.txt file--->which can be used for install all libraries that can be placed in that file...

<!-- project structure -->
heart_disease_prediction 
  __init_.py
     components(folder)
      __init__.py
      data_ingestion.py
      data_validation.py
      data_transformation.py
      model_trainer.py
    constanr(folder)
     __init__.py
      training_pipeline(folder)
       __init__.py

    entity(folder)
     __init__.py
      artifact_entity.py
      config_entity.py
    exception(folder)
     __init__.py
      exception.py
    logging(folder)
     __init__.py
      logging.py