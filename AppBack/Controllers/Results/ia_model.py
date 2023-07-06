import math
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
            last_bias = self.model.intercepts_[-1][0]
            max_value, min_value = 0, 0

            for i in range(0, n_nodes_last_hidden_layer):
                max_value += abs(last_weights[i]) * 1
                min_value += abs(last_weights[i]) * -1

            max_value += last_bias
            min_value += last_bias
            return (outputs - min_value) / (max_value - min_value)
        return "error"

    def predict(self, data):
        data = list(data.values())[2:]

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
        framingham_result = self.framingham(df)
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

        return {
            "detail": "Estimación realizada con éxito",
            "prediction": normalized_prediction,
            "framingham": framingham_result[0],
            "severity": severity,
        }

    def framingham(self, df):  # NOSONAR
        results = []
        for index, row in df.iterrows():
            be1 = 0.04826 if row["sexo"] == "0" else 0.33766
            be2 = 0 if row["sexo"] == "0" else -0.00268

            if row["colesterol"] < 160:
                bc = -0.65945 if row["sexo"] == "0" else -0.26138
            elif 160 <= row["colesterol"] <= 199:
                bc = 0
            elif 200 <= row["colesterol"] <= 239:
                bc = 0.17692 if row["sexo"] == "0" else 0.20771
            elif 240 <= row["colesterol"] <= 279:
                bc = 0.50539 if row["sexo"] == "0" else 0.24385
            else:
                bc = 0.65713 if row["sexo"] == "0" else 0.53513

            if row["hdl"] < 35:
                bh = 0.49744 if row["sexo"] == "0" else 0.84312
            elif 35 <= row["hdl"] <= 44:
                bh = 0.24310 if row["sexo"] == "0" else 0.37796
            elif 45 <= row["hdl"] <= 49:
                bh = 0 if row["sexo"] == "0" else 0.19785
            elif 50 <= row["hdl"] <= 59:
                bh = -0.05107 if row["sexo"] == "0" else 0
            else:
                bh = -0.48660 if row["sexo"] == "0" else -0.42951

            if row["sistolica"] < 120 and row["diastolica"] < 80:
                bt = -0.00226 if row["sexo"] == "0" else -0.53363
            elif row["sistolica"] < 130 and row["diastolica"] < 85:
                bt = 0
            elif row["sistolica"] < 140 and row["diastolica"] < 90:
                bt = 0.28320 if row["sexo"] == "0" else -0.06773
            elif row["sistolica"] < 160 and row["diastolica"] < 100:
                bt = 0.52168 if row["sexo"] == "0" else 0.26288
            elif row["sistolica"] >= 160 and row["diastolica"] >= 100:
                bt = 0.61859 if row["sexo"] == "0" else 0.46573
            else:
                bt = 0

            if row["diabetes"] == "0":
                bd = 0
            else:
                bd = 0.42839 if row["sexo"] == "0" else 0.59626

            if row["tabaco"] == "0":
                bf = 0
            else:
                bf = 0.52337 if row["sexo"] == "0" else 0.29246

            # print(be1,be2,bc,bh,bt,bd,bf)
            L = -1
            if row["sexo"] == "0":
                L = be1 * row["edad"] + bc + bh + bt + bd + bf
            else:
                L = be1 * row["edad"] + be2 * row["edad"] ** 2 + bc + bh + bt + bd + bf

            # print("L --> ", L)
            B = -1
            if row["sexo"] == "0":
                B = math.exp(L - 3.0975)
            else:
                B = math.exp(L - 9.92545)

            # print("B --> ", B)
            if row["sexo"] == "0":
                results.append(1 - 0.90015**B)
            else:
                results.append(1 - 0.96246**B)
        return results
