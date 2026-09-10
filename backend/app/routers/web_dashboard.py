"""Dashboard de cobertura y resultados de un proyecto: cuanto se ha
ejecutado, con que resultado, y cuantos defectos siguen abiertos. El acceso
al proyecto (dueno o ADMIN) se valida via proyecto_autorizado."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.dependencias import exigir_login, proyecto_autorizado
from app.repositorios import casos_prueba as repo_casos
from app.repositorios import defectos as repo_defectos
from app.repositorios import ejecuciones as repo_ejecuciones
from app.repositorios import suites as repo_suites

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

_RESULTADOS_POSIBLES = ("Passed", "Failed", "Blocked", "Skipped", "Sin ejecutar")


@router.get("/proyectos/{proyecto_id}/dashboard", response_class=HTMLResponse)
def ver(
    request: Request,
    proyecto_id: str,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    suites = repo_suites.listar_por_proyecto(proyecto_id)
    ultimas = repo_ejecuciones.ultimas_por_proyecto(proyecto_id)

    conteo_resultados = {clave: 0 for clave in _RESULTADOS_POSIBLES}
    filas_suites = []
    total_casos = 0
    total_ejecutados = 0

    for suite in suites:
        casos = repo_casos.listar_por_suite(str(suite["_id"]))
        conteo_suite = {clave: 0 for clave in _RESULTADOS_POSIBLES}
        ejecutados_suite = 0

        for caso in casos:
            ultima = ultimas.get(str(caso["_id"]))
            if ultima:
                resultado = ultima["resultado"]
                ejecutados_suite += 1
            else:
                resultado = "Sin ejecutar"
            conteo_suite[resultado] += 1
            conteo_resultados[resultado] += 1

        total_casos += len(casos)
        total_ejecutados += ejecutados_suite
        filas_suites.append(
            {
                "nombre": suite["nombre"],
                "total": len(casos),
                "ejecutados": ejecutados_suite,
                "cobertura": round(ejecutados_suite / len(casos) * 100) if casos else 0,
                "resultados": conteo_suite,
            }
        )

    cobertura_total = round(total_ejecutados / total_casos * 100) if total_casos else 0

    return templates.TemplateResponse(
        "proyectos/dashboard.html",
        {
            "request": request,
            "usuario": usuario,
            "proyecto": proyecto,
            "total_casos": total_casos,
            "total_ejecutados": total_ejecutados,
            "cobertura_total": cobertura_total,
            "conteo_resultados": conteo_resultados,
            "filas_suites": filas_suites,
            "defectos_abiertos": repo_defectos.contar_abiertos_por_severidad(proyecto_id),
        },
    )
