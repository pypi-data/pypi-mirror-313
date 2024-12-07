# Proyecto FastAPI - Platform

Este proyecto es una aplicación desarrollada en FastAPI que incluye validación de datos con Pydantic.

## Requisitos previos

- **Python 3.11**
- **pip**

## Configuración del entorno de desarrollo

Para comenzar, es necesario crear y activar un entorno virtual para gestionar las dependencias del proyecto.

### 1. Crear el entorno de desarrollo

```bash
python3.11 -m venv env
```

### 2. Activar el entorno de desarrollo

```bash
source env/bin/activate
```

### 3. Instalar las librerías

```bash
pip install -r pipfiles.txt
```

## Ejecutar el proyecto

### 1. Ejecutar en modo local (PC)

```bash
ENV=pc uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

### 2. Ejecutar en modo producción

```bash
ENV=production uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```


## Comandos Docker y Docker Compose

### Eliminar todos los contenedores existentes

```bash
docker rm $(docker ps -aq)
```

### Docker Compose - Ambiente local

- **Crear y construir contenedor**:

```bash
sudo docker-compose -f docker-compose.local.yml up --build
```

- **Iniciar el contenedor sin construir**:

```bash
sudo docker-compose -f docker-compose.local.yml up
```

### Docker Compose - Ambiente QA

- **Crear y construir contenedor en QA**:

```bash
sudo docker-compose -f docker-compose.qa.yml up --build
```

---









