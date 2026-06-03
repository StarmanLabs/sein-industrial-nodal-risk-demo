# Brief de Defensibilidad Metodologica

## Proposito

Este documento resume por que los indicadores del proyecto son defendibles para un sistema de soporte a decisiones y screening industrial. No intenta convertirlos en un modelo causal, un pronostico de precios, una simulacion electrica ni una herramienta de facturacion.

El objetivo correcto es mas acotado y mas defendible:

> ordenar barras del SEIN segun senales relativas de estres marginal nodal, prioridad operativa mensual, estabilidad de la senal y contexto revisado para armar una cola de due diligence industrial.

## Realidad de los datos

- Fuente base: precios marginales COES por barra.
- Unidad analitica mensual: barra-mes.
- Universo auditado: 217 barras y 36 meses, 2023-2025.
- Filas auditadas: 6,779 barra-mes.
- Share de baja informacion: 1.8%.
- Cobertura de indices principales: 0 faltantes en ICPI, OANRI, precio medio, p95 y score de calidad.

Esto permite construir indicadores de comparacion, ranking, monitoreo y priorizacion. No permite inferir por si solo causalidad fisica, congestion real, restricciones de red, precios futuros ni facturas industriales reales.

## Critica 1: "ICPI podria ser arbitrario o duplicar informacion"

### Riesgo real

ICPI combina dimensiones que nacen de precios marginales: nivel de precio, volatilidad, estres, colas y ventanas criticas. Es normal que algunos componentes esten correlacionados porque observan el mismo fenomeno desde angulos distintos. La pregunta seria seria:

> la cola de barras candidatas depende demasiado de una formula puntual o de pesos arbitrarios?

### Prueba aplicada

Se recalculo una version alternativa del indice bajo varios escenarios:

- bloques con pesos iguales;
- familia de precio + criticidad;
- sin componente de volatilidad;
- sin componente de costo/precio.

No se cambio la formula oficial del proyecto. Se uso sensibilidad metodologica para revisar estabilidad.

### Evidencia

| Escenario | Spearman vs ICPI base | Overlap top-20 promedio | Overlap top-20 minimo | Lectura |
|---|---:|---:|---:|---|
| Bloques iguales | 0.999 | 0.964 | 0.850 | Muy estable |
| Familia de precio + criticidad | 0.998 | 0.936 | 0.800 | Muy estable |
| Sin volatilidad | 0.989 | 0.879 | 0.500 | Cambia mas la cola extrema |
| Sin costo/precio | 0.974 | 0.819 | 0.300 | Cambia mas la cola extrema |

### Conclusion defendible

ICPI no queda defendido porque "suena sofisticado", sino porque la cola principal se mantiene bajo especificaciones balanceadas. Cuando se quitan componentes centrales de precio, la cola cambia mas; eso indica que esos componentes aportan informacion material, no que sean decoracion.

La defensa correcta es:

> ICPI es un indice relativo de estres nodal basado en varias dimensiones del precio marginal. Su cola principal es estable bajo alternativas razonables de ponderacion, aunque sus componentes deben interpretarse como dimensiones relacionadas de un mismo fenomeno de precio, no como variables causalmente independientes.

## Critica 2: "OANRI podria confundirse con causalidad fisica local"

### Riesgo real

OANRI usa un contexto mensual del regimen operativo del sistema. Ese regimen es comun a todas las barras dentro de un mes. Por lo tanto, no puede probar que una barra especifica causo una condicion fisica del sistema.

### Prueba aplicada

Se separo OANRI en:

- exposicion nodal;
- contexto mensual del sistema.

Luego se verifico si el regimen sistemico variaba dentro del mes y como se relacionaba con la cola nodal.

### Evidencia

| Prueba | Resultado | Lectura |
|---|---:|---|
| Valores unicos del regimen sistemico dentro de cada mes | 1 | Es contexto mensual comun, no diagnostico local |
| Overlap top-20 OANRI vs exposicion nodal | 1.000 | Preserva la cola nodal mensual |
| Spearman OANRI vs exposicion nodal | 0.681 | Tiene componente nodal relevante |
| Spearman OANRI vs regimen sistemico | 0.657 | Tambien incorpora contexto sistemico |

### Conclusion defendible

OANRI es defendible si se comunica como prioridad operativa, no como causalidad. Su valor es ordenar la senal nodal bajo contexto mensual del sistema.

La defensa correcta es:

> OANRI no identifica congestion fisica localizada. Ajusta la lectura de la senal nodal segun el contexto mensual del sistema y sirve para priorizar revision, no para diagnosticar restricciones fisicas.

## Critica 3: "Robustez baja suena a indice debil"

### Riesgo real

El termino "robustez baja" puede malinterpretarse como "dato malo" o "metodologia fallida". En este proyecto significa otra cosa:

> la barra aparece con menor estabilidad como candidata prioritaria cuando se prueban escenarios alternativos de ranking.

Eso no invalida el dato COES ni invalida el indice. Indica que la barra no debe venderse como caso prioritario estable sin mas contexto.

### Correccion conceptual

El dashboard y la narrativa publica deben separar:

1. Cobertura de datos: si la barra tiene informacion suficiente.
2. Estabilidad de senal: si la barra sigue siendo relevante bajo escenarios alternativos.
3. Prioridad de revision: si conviene revisarla primero para due diligence.

### Conclusion defendible

El termino publico recomendado es "estabilidad de senal", no "robustez". Una barra con estabilidad baja puede seguir siendo util como referencia, monitoreo o caso contextual; simplemente no debe presentarse como candidata fuerte sin mayor soporte.

## Que queda metodologicamente defendible

El proyecto queda defendible como:

- sistema descriptivo de screening;
- ranking relativo de barras;
- cola de revision experta;
- herramienta de monitoreo mensual;
- capa de priorizacion para due diligence industrial;
- soporte para decidir donde investigar contrato, demanda, ubicacion, confiabilidad y contexto tecnico.

## Que no debe afirmarse

No se debe decir que el proyecto:

- prueba congestion fisica;
- predice precios;
- calcula facturas reales;
- reemplaza estudios electricos;
- determina restricciones fisicas definitivas;
- recomienda inversiones por si solo;
- produce diagnosticos causales.

## Frase defendible para entrevista o README

Construí un sistema auditado de soporte a decisiones que transforma precios marginales COES por barra en un panel de 217 barras y 36 meses. A partir de ese panel, construye senales relativas de estres nodal, prioridad operativa mensual, estabilidad de senal y contexto revisado para ordenar una cola de due diligence industrial. La metodologia fue auditada con sensibilidad de pesos, estabilidad de rankings, cobertura de datos y descomposicion del ajuste operativo, manteniendo limites claros: no prueba congestion fisica, no predice precios y no reemplaza revision contractual, tecnica u operativa.

## Veredicto

Los indices son defendibles para el claim correcto: screening, monitoreo y priorizacion. No son defendibles para claims fisicos, causales, predictivos o de facturacion.

La solucion no es inflar la metodologia. La solucion es mostrar que:

1. la cobertura de datos es amplia;
2. los indicadores tienen escala y variacion util;
3. las colas principales sobreviven pruebas razonables;
4. los puntos debiles estan delimitados;
5. la interpretacion publica esta correctamente acotada.
