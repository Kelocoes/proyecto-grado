import os
from pathlib import Path

import joblib
import pandas as pd


class IAModel:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent
        self.model = joblib.load(os.path.join(BASE_DIR, "model.joblib"))
        self.pipeline_inputer = joblib.load(
            os.path.join(BASE_DIR, "./pipeline_inputer.joblib")
        )
        self.pipeline_norm = joblib.load(
            os.path.join(BASE_DIR, "./pipeline_norm.joblib")
        )
        self.threshold_1 = 0.639
        self.threshold_2 = 0.75

    def normalization(self, outputs):
        if self.model.activation == "tanh":
            if not hasattr(self.model.hidden_layer_sizes, "__iter__"):
                n_nodes_last_hidden_layer = self.model.model.hidden_layer_sizes
            else:
                n_nodes_last_hidden_layer = list(self.model.hidden_layer_sizes)[-1]

            last_weights = self.model.coefs_[-1].ravel()
            # print("Last weights --> ",last_weights)
            last_bias = self.model.intercepts_[-1][0]
            # print("Last bias --> ", last_bias)
            max_value, min_value = 0, 0

            for i in range(0, n_nodes_last_hidden_layer):
                max_value += abs(last_weights[i]) * 1
                min_value += abs(last_weights[i]) * -1

            max_value += last_bias
            min_value += last_bias
            # print("Max value: ",max_value,"Min value: ", min_value)
            return (outputs - min_value) / (max_value - min_value)
        return "error"

    def predict(self, data):
        data = list(data.values())[3:]

        # Lógica de predicción utilizando el modelo
        columns = [
            "sexo",
            "diabetes",
            "tabaco",
            "antecedentes",
            "edad",
            "peso",
            "talla",
            "sistolica",
            "diastolica",
            "colesterol",
            "hdl",
            "ldl",
            "trigliceridos",
        ]

        df = pd.DataFrame([data], columns=columns)
        data_inputed = self.pipeline_inputer.transform(df)

        df = pd.DataFrame([data_inputed[0]], columns=columns)
        data_normalized = self.pipeline_norm.transform(df)

        prediction = self.model.predict(data_normalized)
        normalized_prediction = self.normalization(prediction)[0]

        severity = "none"
        if normalized_prediction != "error":
            if normalized_prediction < self.threshold_1:
                severity = "Low"
            elif normalized_prediction < self.threshold_2:
                severity = "Medium"
            else:
                severity = "High"

        return {"prediction": normalized_prediction, "severity": severity}
