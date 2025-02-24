import random
import time
from google.generativeai import GenerativeModel

# Seleccionar el modelo base
base_model = [
    m for m in genai.list_models()
    if "createTunedModel" in m.supported_generation_methods and
    "flash" in m.name][0]

# Nombre único para el modelo afinado
name = f'architect-python-es-{random.randint(0, 10000)}'

# Crear el modelo afinado
operation = genai.create_tuned_model(
    source_model=base_model.name,
    training_data=training_data,
    id=name,
    epoch_count=200,
    batch_size=8,
    learning_rate=0.0005,
)

# Monitorear el progreso
for status in operation.wait_bar():
    time.sleep(30)

# Obtener el modelo afinado
model = operation.result()

# Visualizar la curva de pérdida
import pandas as pd
import seaborn as sns
snapshots = pd.DataFrame(model.tuning_task.snapshots)
sns.lineplot(data=snapshots, x='epoch', y='mean_loss')
