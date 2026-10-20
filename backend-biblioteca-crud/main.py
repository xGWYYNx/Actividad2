from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="API Tienda de Moda - ADSO",
    description="API RESTful con operaciones CRUD para artículos de moda",
    version="2.0.0"
)


# Modelo de artículo de moda
class ArticuloModa(BaseModel):
    id: int
    referencia_sku: str
    talla: str
    precio_publico: float
    en_promocion: bool = True


# Modelo para actualizar un artículo
class ArticuloModaUpdate(BaseModel):
    referencia_sku: str
    talla: str
    precio_publico: float
    en_promocion: bool = True


# Base de datos temporal
db_articulosModa: List[ArticuloModa] = [
    ArticuloModa(
        id=1,
        referencia_sku="CAM-001",
        talla="M",
        precio_publico=59900.0,
        en_promocion=True
    ),
    ArticuloModa(
        id=2,
        referencia_sku="PAN-002",
        talla="L",
        precio_publico=89900.0,
        en_promocion=False
    )
]


# GET: Obtener todos los artículos
@app.get(
    "/api/v1/articulos",
    response_model=List[ArticuloModa],
    status_code=status.HTTP_200_OK
)
def obtener_todos_los_articulos():
    return db_articulosModa


# GET: Obtener un artículo por ID
@app.get(
    "/api/v1/articulos/{articulo_id}",
    response_model=ArticuloModa,
    status_code=status.HTTP_200_OK
)
def obtener_articulo_por_id(articulo_id: int):
    for articulo in db_articulosModa:
        if articulo.id == articulo_id:
            return articulo

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El artículo con ID {articulo_id} no existe"
    )


# POST: Registrar un nuevo artículo
@app.post(
    "/api/v1/articulos",
    response_model=ArticuloModa,
    status_code=status.HTTP_201_CREATED
)
def crear_articulo(articulo: ArticuloModa):
    for existente in db_articulosModa:
        if existente.id == articulo.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un artículo con el ID {articulo.id}"
            )

    db_articulosModa.append(articulo)
    return articulo


# PUT: Actualizar un artículo existente
@app.put(
    "/api/v1/articulos/{articulo_id}",
    response_model=ArticuloModa,
    status_code=status.HTTP_200_OK
)
def actualizar_articulo(
    articulo_id: int,
    datos_actualizados: ArticuloModaUpdate
):
    for index, articulo in enumerate(db_articulosModa):
        if articulo.id == articulo_id:
            articulo_modificado = ArticuloModa(
                id=articulo_id,
                referencia_sku=datos_actualizados.referencia_sku,
                talla=datos_actualizados.talla,
                precio_publico=datos_actualizados.precio_publico,
                en_promocion=datos_actualizados.en_promocion
            )

            db_articulosModa[index] = articulo_modificado
            return articulo_modificado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se puede actualizar: el artículo con ID {articulo_id} no existe"
    )


# DELETE: Eliminar un artículo
@app.delete(
    "/api/v1/articulos/{articulo_id}",
    status_code=status.HTTP_200_OK
)
def eliminar_articulo(articulo_id: int):
    for index, articulo in enumerate(db_articulosModa):
        if articulo.id == articulo_id:
            db_articulosModa.pop(index)
            return {
                "mensaje": f"El artículo con ID {articulo_id} fue eliminado correctamente"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se puede eliminar: el artículo con ID {articulo_id} no existe"
    )