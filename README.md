
# Actividad del módulo: Introducción a DevOps

## 1. Integración continua (`integration.yml`)
| Fase | Descripción | Resultado esperado |
|------|-------------|--------------------|
| **Instalación** | `pip install -r requirements.txt` | Dependencias resueltas |
| **Pruebas unitarias** | Ejecuta `pytest unit_tests/` | Todas las pruebas pasan |
| **Cobertura** | Calcula y publica cobertura | ≥ 90 % recomendado |
| **Comentario en el PR** | Resumen automático con ✔/❌ y cobertura | Feedback inmediato |

Si falla una prueba, el _merge_ queda bloqueado.

---

## 2. Entrenamiento y registro (`build.yml`)
1. **Descarga de datos**  
2. **Entrenamiento**: `python src/main.py`  
3. **Serialización**: guarda `models/model.pkl`  
4. **Pruebas sobre el modelo**: `pytest model_tests/`  
5. **Registro en MLflow**: `python scripts/register_model.py`

Resultado: un artefacto versionado, trazable y probado, listo para producción (cuando el _pipeline_ de despliegue se recupere).

---

## 3. Despliegue del modelo (`deploy.yml`) ‑ ***❌❌❌ACTUALMENTE CON ERRORES❌❌❌***
| Paso | Acción | Observación |
|------|--------|-------------|
| **Build Docker** | Empaqueta la API FastAPI en una imagen | Correcto |
| **Push a ACR** | `docker push` al registro | Correcto |
| **Deploy ACI** | Crea un contenedor y expone el endpoint REST | **Falla**: error en las credenciales/quotas |

> 🛠️ **Siguiente paso recomendado**: verificar los secretos `AZURE_CREDENTIALS`, `ACR_*` y los límites de la suscripción.

---

## 4. Requisitos previos
Configura en **GitHub → Settings → Secrets and variables**:

| Tipo | Clave | Uso |
|------|-------|-----|
| Secret | `AZURE_CREDENTIALS` | Login mediante `az login --service-principal` |
| Secret | `ACR_NAME` / `ACR_USERNAME` / `ACR_PASSWORD` | Push de imágenes |
| Secret | `AZURE_RESOURCE_GROUP` | Resource group destino |
| Secret | `AZURE_STORAGE_CONNECTION_STRING` | Persistencia en MLflow |
| Variable | `EXPERIMENT_NAME` | Nombre del experimento MLflow |
| Variable | `MLFLOW_URL` | Tracking server |
| Variable | `MODEL_NAME` | Alias del modelo |

---

## 5. Ejecución local
```bash
# 1. Dependencias
pip install -r requirements.txt

# 2. Entrenamiento
python src/main.py

# 3. Pruebas del modelo
pytest model_tests/test_model.py
