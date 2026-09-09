<div align="center">

<img src="assets/header.svg" alt="Nikita Moskalev — Java Backend Developer" width="100%">

<img src="https://komarev.com/ghpvc/?username=SmesiteJl&style=for-the-badge&color=cba6f7&labelColor=181825&label=PROFILE+VIEWS" alt="Profile views">
<img src="https://img.shields.io/badge/Kazan-RU-181825?style=for-the-badge&logo=googlemaps&logoColor=94e2d5" alt="Kazan, Russia">
<img src="https://img.shields.io/badge/KFU%20%2F%20ITIS-181825?style=for-the-badge&logoColor=cdd6f4" alt="KFU / ITIS">
<img src="https://img.shields.io/badge/on%20GitHub%20since-2022-181825?style=for-the-badge&logo=github&logoColor=cba6f7" alt="On GitHub since 2022">

</div>

## About

Backend developer from Kazan, studying at **KFU / ITIS**. I build services that other people have to
run in production, which mostly means caring about the parts nobody notices while they work.

- **End to end on a feature** — REST contract, domain model, schema migration, integration tests on real containers, and the metrics that show it holds up.
- **Event-driven by default** — separate deployables talking over queues, with dead-letter handling and idempotent consumers instead of hopeful retries.
- **Migrations that roll back** — `ddl-auto: validate` always; every schema change is a reviewed changelog, never a surprise at startup.
- **LLMs behind ordinary backends** — a model gateway, a Telegram front end, and a state machine that keeps a generated conversation on the rails.

## What I build

| | | |
| :--- | :--- | :--- |
| **leadgen**&nbsp;🔒 | Cold outreach to courier candidates on Telegram. Three services — a Spring Boot orchestrator, an LLM gateway, and a Python/Telethon account pool — find candidates, hold a live dialogue in a manager's voice, score how warm each one is, and hand the ready ones to a human operator. | `Java 21` `Spring Boot` `PostgreSQL` `RabbitMQ` `Python` |
| **fincat**&nbsp;🔒 | Self-hosted finance assistant for Russian banks: imports PDF statements, categorises transactions on its own, tracks loans and savings goals. Invite-only registration, JWT with refresh rotation. | `Java 21` `Spring Boot` `PostgreSQL` `Next.js` |
| **kairos**&nbsp;🔒 | Telegram secretary bot — routes requests to OpenRouter models, transcribes voice, and calls Google Calendar as a tool. | `Python` `OpenRouter` `Docker` |
| [**letters-LF**](https://github.com/SmesiteJl/letters-LF) | Service for a 2026 youth forum: team leads upload a participant table and generate a personal letter for each one through an LLM — versioned, then exported to `.docx` per team. | `Python` `Flask` `SQLite` |
| [**algorithms**](https://github.com/SmesiteJl/moskalev-additional-chapters-on-algorithms-2025) | Every problem from the *Additional Chapters on Algorithms* course, solved and explained. | `Java` |

<sub>🔒 private — happy to walk through the code.</sub>

## Stack

<div align="center">

**Backend**

<img src="https://img.shields.io/badge/Java%2021-181825?style=for-the-badge&logo=openjdk&logoColor=cba6f7" alt="Java 21">
<img src="https://img.shields.io/badge/Spring%20Boot-181825?style=for-the-badge&logo=springboot&logoColor=a6e3a1" alt="Spring Boot">
<img src="https://img.shields.io/badge/Gradle-181825?style=for-the-badge&logo=gradle&logoColor=89dceb" alt="Gradle">
<img src="https://img.shields.io/badge/Hibernate-181825?style=for-the-badge&logo=hibernate&logoColor=f9e2af" alt="Hibernate">
<img src="https://img.shields.io/badge/Thymeleaf-181825?style=for-the-badge&logo=thymeleaf&logoColor=a6e3a1" alt="Thymeleaf">
<img src="https://img.shields.io/badge/OpenAPI-181825?style=for-the-badge&logo=openapiinitiative&logoColor=94e2d5" alt="OpenAPI">

**Data**

<img src="https://img.shields.io/badge/PostgreSQL-181825?style=for-the-badge&logo=postgresql&logoColor=89b4fa" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Liquibase-181825?style=for-the-badge&logo=liquibase&logoColor=74c7ec" alt="Liquibase">
<img src="https://img.shields.io/badge/Redis-181825?style=for-the-badge&logo=redis&logoColor=f38ba8" alt="Redis">
<img src="https://img.shields.io/badge/SQLite-181825?style=for-the-badge&logo=sqlite&logoColor=89dceb" alt="SQLite">
<img src="https://img.shields.io/badge/MinIO-181825?style=for-the-badge&logo=minio&logoColor=eba0ac" alt="MinIO">

**Messaging &amp; infrastructure**

<img src="https://img.shields.io/badge/Kafka-181825?style=for-the-badge&logo=apachekafka&logoColor=cdd6f4" alt="Kafka">
<img src="https://img.shields.io/badge/RabbitMQ-181825?style=for-the-badge&logo=rabbitmq&logoColor=fab387" alt="RabbitMQ">
<img src="https://img.shields.io/badge/Docker-181825?style=for-the-badge&logo=docker&logoColor=89b4fa" alt="Docker">
<img src="https://img.shields.io/badge/Consul-181825?style=for-the-badge&logo=consul&logoColor=f5c2e7" alt="Consul">
<img src="https://img.shields.io/badge/GitHub%20Actions-181825?style=for-the-badge&logo=githubactions&logoColor=b4befe" alt="GitHub Actions">

**Testing &amp; observability**

<img src="https://img.shields.io/badge/JUnit%205-181825?style=for-the-badge&logo=junit5&logoColor=a6e3a1" alt="JUnit 5">
<img src="https://img.shields.io/badge/Testcontainers-181825?style=for-the-badge&logo=docker&logoColor=94e2d5" alt="Testcontainers">
<img src="https://img.shields.io/badge/Prometheus-181825?style=for-the-badge&logo=prometheus&logoColor=fab387" alt="Prometheus">
<img src="https://img.shields.io/badge/Grafana-181825?style=for-the-badge&logo=grafana&logoColor=f9e2af" alt="Grafana">

**Python, front end &amp; LLM**

<img src="https://img.shields.io/badge/Python-181825?style=for-the-badge&logo=python&logoColor=f9e2af" alt="Python">
<img src="https://img.shields.io/badge/Flask-181825?style=for-the-badge&logo=flask&logoColor=cdd6f4" alt="Flask">
<img src="https://img.shields.io/badge/TypeScript-181825?style=for-the-badge&logo=typescript&logoColor=89b4fa" alt="TypeScript">
<img src="https://img.shields.io/badge/Next.js-181825?style=for-the-badge&logo=nextdotjs&logoColor=cdd6f4" alt="Next.js">
<img src="https://img.shields.io/badge/Spring%20AI-181825?style=for-the-badge&logo=spring&logoColor=a6e3a1" alt="Spring AI">
<img src="https://img.shields.io/badge/OpenRouter-181825?style=for-the-badge&logo=openrouter&logoColor=cba6f7" alt="OpenRouter">

</div>

## Activity

<div align="center">

<img src="assets/metrics-stats.svg" alt="Code volume and language breakdown, private repositories included" width="100%">

<sub>Counted with a token of my own, so the private repositories are in there — public-only tooling sees about a third of this.</sub>

<br>

<img src="https://raw.githubusercontent.com/SmesiteJl/SmesiteJl/output/snake.svg" alt="Snake eating my contribution graph" width="100%">

<br><br>

<img src="assets/skyline.gif" alt="3D contribution skyline, 2022-2026" width="100%">

<sub>Every week of contributions since 2022, built from GitHub's <a href="https://github.com/github/gh-skyline"><code>gh-skyline</code></a> and rendered by <a href="scripts/render_skyline.py"><code>render_skyline.py</code></a> · <a href="assets/skyline-full.stl">open the STL</a> for the interactive 3D view</sub>

</div>

## Get in touch

<div align="center">

<a href="https://t.me/Smesitejl"><img src="https://img.shields.io/badge/Telegram-%40Smesitejl-313244?style=for-the-badge&logo=telegram&logoColor=89b4fa&labelColor=181825" alt="Telegram @Smesitejl"></a> <a href="mailto:nik_mos2@mail.ru"><img src="https://img.shields.io/badge/Email-nik__mos2%40mail.ru-313244?style=for-the-badge&logo=maildotru&logoColor=cba6f7&labelColor=181825" alt="Email nik_mos2@mail.ru"></a> <a href="https://github.com/SmesiteJl"><img src="https://img.shields.io/badge/GitHub-SmesiteJl-313244?style=for-the-badge&logo=github&logoColor=cdd6f4&labelColor=181825" alt="GitHub SmesiteJl"></a>

<br>

<sub>The snake and the skyline regenerate themselves from <a href=".github/workflows"><code>.github/workflows</code></a>.</sub>

</div>
