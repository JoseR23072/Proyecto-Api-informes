## 🧾 Proyecto Microservicio ApiREST para la gestión de batidas

Microservicio basado en **FastAPI** para gestionar, generar y enviar informes de voluntarios participantes en batidas de limpieza.

---

## 📑 Índice

1. [Descripción](#descripción)
2. [Tecnologías utilizadas](#tecnologías-utilizadas)
3. [Funcionalidades principales](#funcionalidades-principales)
4. [Prerrequisitos](#prerrequisitos)
5. [Estructura del proyecto](#estructura-del-proyecto)
6. [Instalación](#instalación)
7. [Uso](#uso)
8. [Pruebas](#pruebas)
9. [Contribuciones](#contribuciones)
10. [Licencia](#licencia)
11. [Autor](#autor)

---

## 🔍 Descripción

Este microservicio permite la gestión de batidas de limpieza, incluyendo el registro de voluntarios, la generación de informes en PDF y Excel, y el envío automatizado de recordatorios por correo electrónico con los detalles del evento y adjuntos. Está diseñado para integrarse en una arquitectura de microservicios con registro en Eureka.

---

## 🚀 Tecnologías utilizadas

* **FastAPI**: Framework web de alto rendimiento.
* **uvicorn**: Servidor ASGI para FastAPI.
* **SQLModel**: Modelado de datos con Pydantic y SQLAlchemy.
* **MySQL**: Base de datos relacional.
* **mysql-connector-python**: Conector de MySQL.
* **Pydantic**: Validación de datos.
* **Jinja2**: Plantillas HTML para PDF.
* **WeasyPrint**: Generación de PDFs desde HTML.
* **Pandas**: Manipulación de datos y exportación a Excel.
* **openpyxl**: Lectura y escritura de archivos Excel.
* **Yagmail**: Envío de correos electrónicos.
* **email-validator**: Validación de direcciones de correo.
* **APScheduler**: Programación de tareas.
* **httpx**: Cliente HTTP asíncrono.
* **py-eureka-client**: Cliente Eureka para descubrimiento de servicios.
* **Docker & Docker Compose**: Contenerización y orquestación.
* **Python 3.11+**
* **.venv**: Entorno virtual recomendado.

---

## ✨ Funcionalidades principales

* Gestión CRUD de **batidas** y **voluntarios**.
* Generación automática de informes en **PDF** (WeasyPrint) y **Excel** (Pandas + openpyxl).
* Envío de recordatorios por correo electrónico con PDF adjunto.
* Validación y seguridad básica de datos.
* Registro en servidor **Eureka** para descubrimiento de servicios.

---

## 📝 Prerrequisitos

Antes de comenzar, asegúrate de tener:

1. **Java y Spring Cloud Config** desplegados para Eureka. Consulta el repositorio de microservicios principal:

   * [https://github.com/MiguelCocoHdez/proyecto-microservicios-riverspain.git](https://github.com/MiguelCocoHdez/proyecto-microservicios-riverspain.git)
2. **Docker** y **Docker Compose** instalados.
3. **Git** para clonar este repositorio.

---

## 🗂️ Estructura del proyecto

```text
├── config/           # Configuraciones de base de datos, Eureka, APScheduler
├── models/           # Definición de modelos SQLModel (Batida, Voluntario)
├── repository/       # Clases para acceso a datos
├── schemas/          # Esquemas Pydantic para validación y respuesta
│   ├── batida.py     # DTOs de batida
│   └── voluntario.py # DTOs de voluntario
├── services/         # Lógica de negocio y generación de informes
├── utils/            # Funciones auxiliares (PDF, email, Excel)
├── rest/             # Endpoints REST (FastAPI routers)
└── main.py           # Punto de entrada de la aplicación
```

---

## ⚙️ Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/JoseR23072/Proyecto-Api-informes.git
   cd Proyecto-Api-informes
   ```
2. Crea un archivo `.env` en la raíz con las siguientes variables:

   ```ini
   API_GOOGLE=<tu-api-key-para-mapas>
   EMAIL_USER=<tu-email>
   EMAIL_PASSWORD=<tu-password-de-app>
   ```
3. Levanta los servicios con Docker Compose:

   ```bash
   docker-compose up --build -d
   ```

---

## 🎯 Uso

* Accede a la documentación interactiva de la API en:

  ```
  http://localhost:8000/docs
  ```

* Para detener los servicios en Docker Compose, ejecuta:

  ```bash
  docker-compose down
  ```

---

## 🧪 Pruebas

Ejecuta los tests unitarios y de integración con:

```bash
pytest --cov=.
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas:

1. Abre un **Issue** para discutir tu propuesta.
2. Realiza un **Fork** del proyecto.
3. Crea una rama con tus cambios: `git checkout -b feature/nombre-cambio`.
4. Envía un **Pull Request** describiendo los cambios.

---

## 📄 Licencia

Este proyecto está bajo la **MIT License**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙋 Autor

Desarrollado con ❤️ por **Jose R. Ogosi**
