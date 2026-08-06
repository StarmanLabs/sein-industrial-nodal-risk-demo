# Resumen Metodológico Público

La capa pública usa salidas agregadas y sanitizadas derivadas de precios marginales COES por barra.

- Estrés nodal resume presión relativa de precio marginal por barra.
- Prioridad operativa lee esa señal junto con el contexto mensual del sistema.
- Score de revisión convierte la señal en una cola de due diligence.
- El contexto topológico revisado identifica el tipo de evidencia, las fuentes aceptadas y las advertencias específicas de cada barra.

El pipeline completo, los archivos crudos, los datos intermedios y las auditorías internas permanecen privados.