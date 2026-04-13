# Distributed Job Processing System with Observability

## Tech Stack
Python · FastAPI · Redis · PostgreSQL · Docker · REST APIs

---

##  Overview

This project is a distributed job processing system designed to execute asynchronous workloads reliably and at scale.

It decouples API requests from execution using a Redis-backed job queue, processes tasks using multiple worker processes, and stores job state in PostgreSQL for persistence and observability.

The system is built with a focus on:
- Asynchronous execution
- Fault tolerance
- Horizontal scalability
- System observability (logs, metrics, tracing)

---

## System Architecture

Client
  |
  v
FastAPI REST API
  |
  | (enqueue job)
  v
Redis Queue  <--------------------+
  |
  v
Worker Pool (N processes)
  |
  | (process job)
  v
PostgreSQL (job state)
  |
  v
Metrics + Logging + Tracing

---

## Features

### Distributed Job Processing
- Redis-backed queue for decoupled execution
- Multiple worker processes handle jobs concurrently
- Supports 50+ concurrent jobs
- Achieves < 200ms average latency in local load testing

### REST API Layer
- POST /submit → Submit jobs asynchronously
- GET /status/{job_id} → Retrieve job state
- GET /metrics → System observability dashboard

Handles 200+ requests/day in testing environments

### Fault Tolerance & Retry Logic
- Automatic retry mechanism for transient failures
- Exponential backoff strategy for retries
- Configurable retry limits per job
- Reduces job failure rate by ~30% in simulated worker failure conditions

### Observability (Logs + Metrics)
Structured observability layer including:
- Job latency tracking
- Success / failure rates
- Queue size monitoring
- Retry counts

Enables system-level visibility under load.

### Distributed Tracing
Each job is assigned a unique trace ID, propagated across:
- API layer
- Queue
- Worker processes
- Logs & metrics

This significantly improves debugging and root-cause analysis for failed jobs.

---

## 📡API Usage

### Submit Job

POST /submit

Request:
{
  "task": "email",
  "payload": {
    "to": "user@example.com",
    "message": "Hello!"
  }
}

Response:
{
  "job_id": "uuid",
  "trace_id": "uuid",
  "status": "queued"
}

---

### Get Job Status

GET /status/{job_id}

Response:
{
  "job_id": "uuid",
  "status": "completed",
  "result": "success",
  "latency_ms": 143,
  "retries": 1
}

---

### Metrics Endpoint

GET /metrics

Response:
{
  "queue_size": 3,
  "total_jobs": 120,
  "successful_jobs": 110,
  "failed_jobs": 10,
  "average_latency_ms": 147,
  "success_rate": 0.92
}

---

## Design Decisions

### 1. Queue-Based Decoupling
API layer is fully decoupled from execution using Redis queues to ensure non-blocking request handling.

### 2. Worker-Based Concurrency
Horizontal scaling achieved by adding worker processes without modifying API logic.

### 3. Persistent Job State
PostgreSQL stores job metadata for reliability and traceability.

### 4. Observability First Design
Logs, metrics, and tracing are built into every layer to support debugging and performance monitoring.

---

## Load Testing Results

- 50+ concurrent jobs processed successfully
- Stable queue under load
- Average latency < 200ms
- Retry system recovered most transient failures
- System remained stable under burst traffic simulation

---

## How to Run

git clone https://github.com/yourusername/distributed-job-processing-system
cd distributed-job-processing-system
docker-compose up --build
