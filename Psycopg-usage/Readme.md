# FastAPI + PostgreSQL + pgAdmin (Kubernetes Deployment)

This project is a **CRUD API built with FastAPI** connected to a **PostgreSQL** database deployed on Kubernetes using Helm.  
It also includes a **pgAdmin4** interface for database administration.

## 🚀 Features
- FastAPI CRUD endpoints (`/posts`)
- PostgreSQL connection with `psycopg`
- PostgreSQL deployed on Kubernetes with Helm
- pgAdmin4 for database administration
- Interactive Swagger UI for API testing

## 📂 Project Structure
```
.
├── main.py                # FastAPI application
├── pgadmin.yaml           # Kubernetes Pod manifest for pgAdmin4
├── helm-create.txt        # Helm command to deploy PostgreSQL
└── README.md
```

## ⚙️ Requirements
- Python **3.9+**
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- PostgreSQL (Bitnami Helm chart)
- A Kubernetes cluster with `kubectl` configured
- Helm 3 installed

## 🐍 Install & Run FastAPI Locally
1. **Create a virtual environment & install dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn psycopg[binary]
```

2. **Run the API:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. **Access Swagger UI:**  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

## 🗄️ Deploy PostgreSQL with Helm
1. **Add the Bitnami Helm repo:**
```bash
helm repo add postgres https://charts.bitnami.com/bitnami
helm repo update
```

2. **Install PostgreSQL:**
```bash
helm upgrade --install postgres postgres/postgresql -n postgres   --create-namespace   --set auth.username=admin   --set auth.password=admin   --set auth.database=Fastapi   --set primary.persistence.enabled=false
```

> ⚠️ The database created is `Fastapi` (adjust if needed).  
> For persistence, enable PVC with:  
> `--set primary.persistence.enabled=true`

3. **Verify PostgreSQL is running on Kubernetes:**
```bash
kubectl -n postgres get all
```
Example output:
```
pod/postgres-0   1/1   Running   2 (18m ago)   17h
service/postgres            ClusterIP      10.106.28.225   <none>         5432/TCP
service/postgres-lb         LoadBalancer   10.104.52.111   192.168.52.1   5432:32168/TCP
statefulset.apps/postgres   1/1   47h
```

## 📊 Deploy pgAdmin4
1. **Create namespace:**
```bash
kubectl create namespace pgadmin
```

2. **Apply pgAdmin manifest:**
```bash
kubectl apply -f pgadmin.yaml
```

3. **Check if the Pod is running:**
```bash
kubectl -n pgadmin get all
```
Example output:
```
pod/pgadmin   1/1   Running   2 (5h19m ago)   23h
service/pgadmin   LoadBalancer   10.99.142.191   192.168.52.2   80:31369/TCP
```

4. **Access pgAdmin via port-forward:**
```bash
kubectl port-forward -n pgadmin pod/pgadmin 8080:80
```

👉 Open [http://localhost:8080](http://localhost:8080)  
- **Email:** `info@mirecloud.com`  
- **Password:** `admin`

Or directly access it via LoadBalancer IP:  
👉 [http://192.168.52.2](http://192.168.52.2)

## 🔗 FastAPI Endpoints
### Create a post
```http
POST /posts
Content-Type: application/json

{
  "title": "My first post",
  "content": "Post content",
  "published": true
}
```

### Get all posts
```http
GET /posts
```

### Get a post by ID
```http
GET /posts/{id}
```

### Update a post
```http
PUT /posts/{id}
```

### Delete a post
```http
DELETE /posts/{id}
```

## 📌 Database Setup
The API requires a `Posts` table in your PostgreSQL database:
```sql
CREATE TABLE "Posts" (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    published BOOLEAN DEFAULT TRUE
);
```

Default connection settings used in `main.py`:
```
host=192.168.52.1
port=5432
user=admin
password=admin
dbname=Fastapi
```

## ✅ Roadmap
- Migrate to **SQLAlchemy ORM**
- Add unit tests
- Docker/Helm deployment for FastAPI
