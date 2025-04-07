# Usa una imagen base oficial de Python
FROM python:3.11-slim


# Actualiza los repositorios e instala las dependencias nativas necesarias para WeasyPrint
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgirepository1.0-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*


# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del proyecto
COPY . .

# Expone el puerto 8000 para la API
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
