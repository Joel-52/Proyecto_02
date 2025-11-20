# Proyecto_02
Segundo Proyecto de la materia Python Avanzado (UPSO)
https://github.com/Joel-52/Proyecto_02/blob/main/README.md

Alumnos: Iñaki Echeverria, Xavi Joel Juan

## Diagrama de Flujo del Menu

```
INICIO
  |
  v
MENU
  |
  +--> 1. Cargar Imagen -----------+
  |                                 |
  +--> 2. Ajustar Contraste --------+--> Requiere imagen cargada
  |                                 |
  +--> 3. Aplicar Filtro -----------+
  |                                 |
  +--> 4. Mostrar Todos Filtros ----+
  |                                 |
  +--> 5. Modo Pintor --------------+
  |
  +--> 0. Salir
```

## Conclusiones Segunda Parte

**Dataset utilizado:** California Housing (precios de casas)  
**Fuente:** Scikit-learn / GitHub  
**Features:** total_rooms, total_bedrooms, population  
**Target:** median_house_value

**1. Desempeño del modelo:**  
El modelo obtuvo un R² de aproximadamente 0.64 en el conjunto de test, lo que significa que explica el 64% de la variabilidad del precio de las casas. Es un desempeño aceptable para un modelo lineal simple.

**2. Variable más influyente:**  
La variable total_rooms tiene el coeficiente más alto, siendo el predictor que más impacta en el precio final de las viviendas.

**3. Calidad de predictores:**  
Las features seleccionadas son buenos predictores (R² > 0.5). Se podría mejorar agregando variables como ubicación geográfica, antigüedad de la vivienda o características de la zona.

**4. Comparativa Train vs Test:**  
Los valores de R² son muy similares entre entrenamiento (0.64) y test (0.64), con diferencia menor a 0.01. Esto indica que el modelo no tiene overfitting y generaliza correctamente a datos nuevos.
