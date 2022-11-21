import tensorflow

load_model=tensorflow.keras.models.load_model
def ensemble_models(model_genres:list,model_input,model_input_cnn):

    #loading all models
    models=[]
    models.append(load_model('./models/model1/'))
    models.append(load_model('./models/model2/'))
    models.append(load_model('./models/model3/'))
    models.append(load_model('./models/model4/'))

    #prediction
    model1=models[0].predict(model_input)
    model2=models[1].predict(model_input)
    model3=models[2].predict(model_input)
    model4=models[3].predict(model_input_cnn)

    avgEnsemble=(model1+model2+model3+model4)/len(models)

    avgLis=[]
    for i in avgEnsemble:
        avgLis.append(i.argmax())
    
    most_confi=max(avgLis,key=avgLis.count)

    return model_genres[most_confi]

