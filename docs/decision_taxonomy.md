# Taxonomia de Decision del Producto

## Regla central

El proyecto evalua el universo completo de 217 barras. El Top 20 mensual se conserva como una zona ejecutiva de seguimiento, no como el universo metodologico.

Esto separa dos preguntas distintas:

1. **Universo completo:** donde se ubica cada barra frente a todas las demas.
2. **Top 20 mensual:** que barras entran cada mes en la zona de atencion ejecutiva.

## Taxonomia para dashboard

| Concepto publico | Campo recomendado | Que significa | Como leerlo |
|---|---|---|---|
| Universo completo | `analysis_scope_es` | Todas las 217 barras comparables se evaluan en la capa producto | Evita sesgo de seleccionar solo casos visibles |
| Estres nodal | `avg_icpi` / `estres_nodal` | Senal relativa de precio marginal por barra | Mayor valor = senal de precio mas intensa dentro del universo |
| Prioridad operativa | `avg_oanri` / `prioridad_operativa` | Estres nodal leido con contexto mensual del sistema | Mayor valor = mayor prioridad de revision bajo contexto operativo |
| Score de revision | `decision_priority_score` / `score_revision` | Traduccion ejecutiva para ordenar la cola de trabajo | Mayor valor = revisar antes |
| Nivel de revision | `due_diligence_priority_es` / `prioridad` | Categoria de accion sugerida | No clasifica barras como buenas o malas |
| Estabilidad de senal | `signal_stability_label_es` / `estabilidad_senal` | Que tan consistente es la barra bajo supuestos alternativos | No es cobertura de datos ni prueba causal |
| Zona mensual | `monthly_attention_label_es` / `zona_mensual` | Frecuencia con que la barra entra al Top 20 mensual | Sirve para distinguir persistencia, frecuencia y episodios |
| Meses Top 20 | `monthly_top20_months` / `meses_top20_mensual` | Numero de meses en la zona ejecutiva mensual | Capa operativa de monitoreo |
| Soporte de evidencia | `evidence_grade` / `soporte_evidencia` | Contexto revisado de activo, barra, subestacion, central, corredor o industria | Ayuda a explicar por que revisar; no prueba causalidad fisica |

## Niveles de revision

| Nivel publico | Interno | Accion |
|---|---|---|
| Revision prioritaria | Priority A | Abrir revision estructurada |
| Revision recomendada | Priority B | Revisar despues de prioritarias o si sector/contrato/ubicacion aumenta exposicion |
| Seguimiento activo | Watchlist | Monitorear recurrencia mensual |
| Referencia comparativa | Monitor | Mantener como contexto del universo |
| Informacion por completar | Low information | Completar evidencia antes de interpretar fuerte |

## Estabilidad de senal

| Etiqueta publica | Interno | Lectura correcta |
|---|---|---|
| Estabilidad alta | High robustness | La barra se mantiene relevante bajo supuestos alternativos |
| Estabilidad moderada | Moderate robustness | La senal es util pero mas sensible a supuestos |
| Estabilidad baja | Low robustness | La barra es menos estable como candidata prioritaria; no significa dato invalido |

## Zona mensual

| Etiqueta | Regla | Uso |
|---|---:|---|
| Zona mensual recurrente | 18 o mas meses en Top 20 | Caso persistente para seguimiento estructurado |
| Zona mensual frecuente | 8 a 17 meses en Top 20 | Caso frecuente; revisar recurrencia y exposicion |
| Zona mensual episodica | 2 a 7 meses en Top 20 | Caso temporal; revisar meses especificos |
| Entrada puntual a zona mensual | 1 mes en Top 20 | Revisar episodio antes de generalizar |
| Fuera de zona mensual | 0 meses en Top 20 | Referencia comparativa dentro del universo completo |

## Frase recomendada para dashboard

> Todas las barras se evaluan dentro del universo completo. El Top 20 mensual no define el universo: funciona como zona ejecutiva para detectar persistencia, frecuencia o episodios de seguimiento.

## Limite de claim

Esta taxonomia ordena revision experta. No prueba congestion fisica, no predice precios, no calcula facturas reales y no reemplaza analisis contractual, tecnico u operativo.
