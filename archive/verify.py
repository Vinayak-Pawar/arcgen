import os
from dotenv import load_dotenv
from llm_engine import LLMEngine
from diagram_gen import execute_diagram_code

# Load environment variables
load_dotenv()

def test_end_to_end():
    print("1. Testing LLM Connection...")
    llm = LLMEngine()
    prompt = """Design the complete end-to-end system architecture for a global video streaming platform similar to Netflix. The platform must support web, mobile (iOS/Android), smart TV, gaming consoles, and set-top boxes, with millions of concurrent users across multiple continents and strict SLAs for availability, latency, and data consistency where appropriate.
Describe the architecture in terms of logical components, data flows, and infrastructure. Include all major subsystems and how they interact:
Clients and Edge Layer
Multiple client types: web browsers, mobile apps, smart TV apps, game console apps, and embedded apps on third-party devices.
A global DNS and traffic management layer that routes users to the nearest region or edge location using anycast and geo-DNS.
A CDN layer (multiple CDNs if needed) for streaming video segments, images, and static assets. Show how clients request manifests (HLS/DASH) and then individual video chunks from edge caches, falling back to origin if needed.
An API Gateway or “edge API” that fronts all backend microservices, providing rate limiting, authentication, request routing, and protocol translation (REST/GraphQL/gRPC).
Authentication and Identity
An Authentication Service handling login via email/password, SSO, OAuth with partners, multi-device sessions, and token issuance (JWT or opaque tokens).
A separate User Account Service that stores account profiles, subscription plan, billing status, allowed devices, and parental controls.
Session management with refresh tokens, device-level session tracking, and revocation (e.g., when password changes or account is locked).
User Profiles and Preferences
User Profile Service: supports multiple profiles under one account, with per-profile language, maturity rating, UI preferences, and watch history.
A Preference Store for likes/dislikes, “My List”, continue-watching rows, and explicit feedback on titles.
These services should expose APIs to Recommendation Service, UI composition services, and Analytics.
Catalog and Metadata
Catalog Service that stores all titles: movies, series, episodes, trailers, artwork, tags, and availability windows (start/end dates per region, per license).
A Metadata Service that holds richer semantic tags: genres, moods, actors, directors, content ratings, production studios, and internal tags used by ML models.
A Rights & Availability Service that determines which title is viewable in which country, on which device types, at what time, and under which subscription plan.
These services must be region-aware and cacheable, with strong consistency for licensing constraints.
Search and Discovery
A Search Service backed by a distributed search engine (e.g., Elasticsearch/OpenSearch/Lucene-based), indexing all titles with multilingual support and typo tolerance.
Autocomplete and suggestion pipeline, including trending queries and personalized keyword suggestions.
Integration with Recommendation Service so results and ranking are personalized per profile.
Explain how indexing is updated when new content is ingested or metadata changes.
Recommendation and Personalization
Recommendation Service that consumes user events (views, clicks, ratings, session context) to generate personalized home-rows (e.g., “Top Picks for You”, “Because you watched X”, “Trending Now”).
Use online feature stores and offline batch processing pipelines. Show both:
Batch layer (daily/weekly training using a data lake and ML pipeline).
Streaming layer (near real-time updates for recency, popularity, and user-session signals).
A Ranking Service that merges multiple candidate lists (collaborative filtering, content-based, popularity, novelty, diversity constraints) and returns ordered rows.
Experimentation hooks: A/B test framework that routes different recommendation strategies to different user cohorts and logs outcomes.
Playback and Streaming Pipeline
Playback Orchestrator Service that, given a user, device type, and title, decides:
The correct bitrate ladder and codec (H.264/HEVC/AV1, etc.).
DRM requirements based on device and region.
Which CDN and origin URL to return.
A Licensing/DRM Service that issues short-lived playback licenses/keys.
A Manifest Service that generates or returns the playback manifest (HLS/DASH playlists), tuned to user’s subscription (e.g., HD vs 4K) and device capabilities.
Client-side adaptive bitrate streaming: clients measure bandwidth and buffer, request segments of different bitrates, and handle failures (retry other CDNs, lower bitrates, etc.).
Real-time playback telemetry: buffered events, errors, quality metrics streamed back to a Telemetry/Analytics Ingestion Service.
Content Ingestion, Encoding, and Storage
Ingestion pipeline for raw studio-delivered media:
A Content Ingest Service that accepts large video files from studios or internal tools.
A workflow engine to orchestrate transcoding jobs, thumbnail generation, and quality control.
Transcoding/Encoding Service that produces multi-bitrate, multi-resolution segments for multiple codecs, and stores them in an origin storage system (e.g., object storage bucket).
DRM packaging step that encrypts segments and prepares keys.
A Media Asset Management Service to track all variants (resolutions, languages, audio tracks, subtitles, captions, dubs).
Integration with CDN origin servers and cache warmup strategies for upcoming popular content.
Offline Downloads (Mobile)
Download Service for mobile apps that issues time-bound, device-bound licenses and provides encrypted segments for offline viewing.
Mechanism to enforce expiration of downloads (license revocation, periodic online checks, or time-based decryption keys).
Sync of offline watch history and last-watched positions back to the server when device reconnects.
Billing, Payments, and Subscriptions
Subscription Service that manages plans, trial periods, upgrades/downgrades, suspensions, and region-specific pricing.
Payment Service integrating with multiple payment gateways (credit cards, UPI, wallets, in-app purchases, third-party carriers).
Invoicing and receipts, fraud detection and limits (multiple failed attempts, unusual location/device changes), and integration with Account Service to lock/unlock viewing based on payment status.
Support for gift codes, promo codes, and partner bundles (e.g., telecom or ISP partnerships).
Notifications and Communications
Notification Service to send emails, push notifications, and in-app messages (e.g., “new season released”, “continue watching”).
Preference management for opting in/out of different notification channels.
Global scheduling and throttling to avoid spamming users and to respect local quiet hours.
Data Platform, Analytics, and Logging
Centralized event ingestion via a distributed log/streaming system (e.g., Kafka/Kinesis/Pub/Sub) for:
Playback events, search queries, clicks, impressions.
Service logs, metrics, and traces.
Data Lake/Data Warehouse where raw and processed data is stored (e.g., S3/GCS + BigQuery/Snowflake/Redshift), accessible by analysts and data scientists.
Batch ETL/ELT jobs that transform streams into analysis-friendly tables.
Real-time analytics for operational dashboards (concurrent streams per region, error spike detection, CDN hit/miss ratio, signup funnel analytics).
ML platform: feature store, model registry, training pipelines, and deployment endpoints for recommendation and fraud models.
Observability, Reliability, and Operations
Centralized Monitoring Service that collects metrics (latency, error rates, resource utilization), traces, and logs from all microservices.
Alerting system with SLO/SLA-based alerts (e.g., 99.9% availability per region, maximum allowed error budget).
Circuit breakers, rate limiters, retries, and backoff mechanisms at service boundaries.
Chaos engineering tools that intentionally break components (e.g., region outage, cache failure, CDN degradation) to test resilience.
Rollout strategies: blue-green deployments, canary releases, feature flags, and quick rollback support.
Strong separation between production, staging, and testing environments.
Security and Compliance
Zero-trust internal network: all inter-service calls authenticated and authorized via service identity.
API-level authorization checks for each resource (e.g., can this profile watch this title in this region?).
Encryption in transit (TLS everywhere) and encryption at rest for sensitive data (user PII, billing data, cryptographic keys).
Secrets management and key management systems (KMS/HSM).
Compliance aspects: GDPR (data deletion/export for users), COPPA/child-safety rules, and regional data residency if required.
Multi-Region, Multi-Cloud, and Disaster Recovery
Deploy services in multiple regions with active-active or active-passive setups.
Data replication strategy:
For strongly consistent data (e.g., billing), use primary/replica or globally consistent databases.
For eventually consistent data (watch history, analytics), use asynchronous replication.
Failover mechanisms: if a region goes down, traffic is re-routed at DNS/load-balancer level, and minimal-critical services are guaranteed in fallback regions.
Backup/restore strategy for key datastores, with regular testing of restore procedures.
Optionally describe limited multi-cloud usage (e.g., using multiple CDNs and possibly some services in another cloud as backup).
Internal Tools and Content Operations
Admin Portal for content operations teams to:
Configure catalog entries, attach metadata, set availability windows, and schedule releases.
Monitor ingestion and transcoding jobs.
Customer Support Tools that allow support staff to view user sessions, devices, recent errors, billing status, and to trigger actions like password reset or account credit.
Access control for internal tools via RBAC, audit logging of staff actions.
Use clear logical groupings and show service boundaries, main data stores (relational databases, NoSQL stores, caches, object storage, search clusters, streams), and communication patterns (synchronous REST/gRPC vs asynchronous events/streams). Highlight where caching is used (API Gateway cache, CDN edge, microservice-level caches) and where strict consistency is required versus where eventual consistency is acceptable.
Model the architecture at a level where each logical component could be a separate microservice or service cluster, and ensure the diagram reflects the flow of:
user sign-up and subscription,
browsing and personalized home page,
search and recommendations,
starting playback, streaming via CDN, and sending telemetry,
background analytics and ML pipelines,
multi-region resilience and failover."""
    
    try:
        code = llm.generate_code(prompt)
        print("   [SUCCESS] Code generated:")
        print("-" * 40)
        print(code)
        print("-" * 40)
        
        if not code:
            print("   [FAILURE] No code generated.")
            return

        print("\n2. Testing Diagram Generation...")
        image_path = execute_diagram_code(code)
        print(f"   [SUCCESS] Image generated at: {image_path}")
        
    except Exception as e:
        print(f"   [FAILURE] Error occurred: {e}")

if __name__ == "__main__":
    test_end_to_end()
