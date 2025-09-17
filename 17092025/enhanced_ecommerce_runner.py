#!/usr/bin/env python3
"""
Enhanced E-commerce Platform Runner - Advanced Simulation for Postmortem Analysis
This file generates comprehensive, realistic errors and issues for postmortem analysis
with structured data for RAG knowledge base population
"""

import sys
import time
import random
import logging
import json
import os
import uuid
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import requests
import psutil

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)
os.makedirs("incident_data", exist_ok=True)

# Create timestamp for filenames
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Log filenames with timestamp
app_log_file = f"logs/application_{timestamp}.log"
error_log_file = f"logs/error_{timestamp}.log"
access_log_file = f"logs/access_{timestamp}.log"
incident_file = f"incident_data/incident_{timestamp}.json"

# Custom filter to separate error logs from application logs
class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR

class AppFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR

# Configure separate loggers
def setup_logging():
    # Main application logger (INFO and WARNING only)
    app_logger = logging.getLogger("EcommerceRunner")
    app_logger.setLevel(logging.INFO)
    
    # Application log handler (INFO and WARNING)
    app_handler = logging.FileHandler(app_log_file)
    app_handler.setLevel(logging.INFO)
    app_handler.addFilter(AppFilter())
    app_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    app_handler.setFormatter(app_formatter)
    
    # Error log handler (ERROR and CRITICAL only)
    error_handler = logging.FileHandler(error_log_file)
    error_handler.setLevel(logging.ERROR)
    error_handler.addFilter(ErrorFilter())
    error_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    error_handler.setFormatter(error_formatter)
    
    # Console handler (all levels)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    app_logger.addHandler(app_handler)
    app_logger.addHandler(error_handler)
    app_logger.addHandler(console_handler)
    
    return app_logger

# Setup logging
logger = setup_logging()

class EcommercePlatform:
    def __init__(self):
        self.services = {
            'user-service': {'port': 8001, 'status': 'running', 'cpu_usage': 0, 'version': 'v1.2.3'},
            'product-service': {'port': 8002, 'status': 'running', 'cpu_usage': 0, 'version': 'v2.1.0'},
            'order-service': {'port': 8003, 'status': 'running', 'cpu_usage': 0, 'version': 'v1.5.7'},
            'payment-service': {'port': 8004, 'status': 'running', 'cpu_usage': 0, 'version': 'v3.0.1'},
            'inventory-service': {'port': 8005, 'status': 'running', 'cpu_usage': 0, 'version': 'v1.8.2'},
            'notification-service': {'port': 8006, 'status': 'running', 'cpu_usage': 0, 'version': 'v1.0.9'}
        }
        self.database_connection_pool = 20
        self.redis_connections = 100
        self.current_incident = None
        
        # Enhanced incident scenarios with categories for RAG knowledge base
        self.incident_scenarios = {
            'database_issues': [
                'database_connection_leak',
                'database_deadlock',
                'database_slow_queries',
                'database_replication_lag',
                'database_connection_timeout'
            ],
            'api_failures': [
                'third_party_api_failure',
                'api_rate_limiting',
                'service_mesh_failure',
                'circuit_breaker_open',
                'load_balancer_failure'
            ],
            'performance_bottlenecks': [
                'memory_leak',
                'high_cpu_usage',
                'cache_thrashing',
                'thread_pool_exhaustion',
                'garbage_collection_pressure'
            ],
            'infrastructure_issues': [
                'disk_space_issue',
                'network_timeout',
                'dns_resolution_failure',
                'kubernetes_pod_eviction',
                'auto_scaling_failure'
            ],
            'security_incidents': [
                'authentication_failure',
                'sql_injection_attempt',
                'ddos_attack',
                'certificate_expiration',
                'unauthorized_access_attempt'
            ],
            'deployment_issues': [
                'configuration_error',
                'deployment_rollback_failure',
                'health_check_failure',
                'version_compatibility_issue',
                'environment_variable_missing'
            ]
        }
        
    def generate_incident_fingerprint(self, incident_type, service_name, error_details):
        """Generate unique fingerprint for incident tracking"""
        fingerprint_data = {
            'incident_type': incident_type,
            'service': service_name,
            'error_hash': hash(str(error_details)),
            'timestamp': datetime.now().isoformat()
        }
        return str(uuid.uuid4())[:8]
    
    def save_incident_metadata(self, incident_type, service_name, severity, details):
        """Save structured incident data for RAG knowledge base"""
        incident_id = str(uuid.uuid4())
        incident_data = {
            'incident_id': incident_id,
            'timestamp': datetime.now().isoformat(),
            'incident_type': incident_type,
            'service': service_name,
            'severity': severity,
            'fingerprint': self.generate_incident_fingerprint(incident_type, service_name, details),
            'details': details,
            'metrics': self.get_current_metrics(),
            'affected_services': self.get_affected_services(),
            'resolution_status': 'open'
        }
        
        # Save to file for RAG knowledge base
        with open(incident_file, 'a') as f:
            f.write(json.dumps(incident_data) + '\n')
        
        self.current_incident = incident_data
        return incident_id
        
    def simulate_incident(self):
        """Randomly trigger different types of incidents with enhanced scenarios"""
        category = random.choice(list(self.incident_scenarios.keys()))
        scenario = random.choice(self.incident_scenarios[category])
        
        logger.info(f"🚨 INCIDENT TRIGGERED: {scenario} (Category: {category})")
        
        # Database Issues
        if scenario == 'database_connection_leak':
            self._database_connection_leak()
        elif scenario == 'database_deadlock':
            self._database_deadlock()
        elif scenario == 'database_slow_queries':
            self._database_slow_queries()
        elif scenario == 'database_replication_lag':
            self._database_replication_lag()
        elif scenario == 'database_connection_timeout':
            self._database_connection_timeout()
            
        # API Failures
        elif scenario == 'third_party_api_failure':
            self._third_party_api_failure()
        elif scenario == 'api_rate_limiting':
            self._api_rate_limiting()
        elif scenario == 'service_mesh_failure':
            self._service_mesh_failure()
        elif scenario == 'circuit_breaker_open':
            self._circuit_breaker_open()
        elif scenario == 'load_balancer_failure':
            self._load_balancer_failure()
            
        # Performance Issues
        elif scenario == 'memory_leak':
            self._memory_leak()
        elif scenario == 'high_cpu_usage':
            self._high_cpu_usage()
        elif scenario == 'cache_thrashing':
            self._cache_thrashing()
        elif scenario == 'thread_pool_exhaustion':
            self._thread_pool_exhaustion()
        elif scenario == 'garbage_collection_pressure':
            self._garbage_collection_pressure()
            
        # Infrastructure Issues
        elif scenario == 'disk_space_issue':
            self._disk_space_issue()
        elif scenario == 'network_timeout':
            self._network_timeout()
        elif scenario == 'dns_resolution_failure':
            self._dns_resolution_failure()
        elif scenario == 'kubernetes_pod_eviction':
            self._kubernetes_pod_eviction()
        elif scenario == 'auto_scaling_failure':
            self._auto_scaling_failure()
            
        # Security Issues
        elif scenario == 'authentication_failure':
            self._authentication_failure()
        elif scenario == 'sql_injection_attempt':
            self._sql_injection_attempt()
        elif scenario == 'ddos_attack':
            self._ddos_attack()
        elif scenario == 'certificate_expiration':
            self._certificate_expiration()
        elif scenario == 'unauthorized_access_attempt':
            self._unauthorized_access_attempt()
            
        # Deployment Issues
        elif scenario == 'configuration_error':
            self._configuration_error()
        elif scenario == 'deployment_rollback_failure':
            self._deployment_rollback_failure()
        elif scenario == 'health_check_failure':
            self._health_check_failure()
        elif scenario == 'version_compatibility_issue':
            self._version_compatibility_issue()
        elif scenario == 'environment_variable_missing':
            self._environment_variable_missing()
    
    # Enhanced Database Issues
    def _database_connection_leak(self):
        service = 'order-service'
        incident_id = self.save_incident_metadata('database_connection_leak', service, 'critical', 
                                                 {'connection_pool_size': 50, 'max_connections': 20, 'affected_queries': ['SELECT * FROM orders', 'UPDATE inventory']})
        logger.error(f"INCIDENT_ID:{incident_id} - DATABASE CONNECTION POOL EXHAUSTED")
        logger.error("Connection pool size exceeded: 50/20 connections active")
        logger.error("service=order-service error=connection_timeout duration=30s")
        logger.error("Multiple queries stuck in WAITING state")
        logger.error("Stack trace: ConnectionPool.getConnection() timeout after 30000ms")
        logger.critical("Database performance degraded - query timeout increased to 45s")
        self.services[service]['status'] = 'degraded'
        
    def _database_deadlock(self):
        service = 'inventory-service'
        incident_id = self.save_incident_metadata('database_deadlock', service, 'high',
                                                 {'deadlocked_tables': ['inventory', 'orders'], 'transaction_ids': ['tx_001', 'tx_002']})
        logger.error(f"INCIDENT_ID:{incident_id} - DATABASE DEADLOCK DETECTED")
        logger.error("Deadlock detected between transactions tx_001 and tx_002")
        logger.error("Table inventory locked by UPDATE statement")
        logger.error("Table orders locked by SELECT FOR UPDATE")
        logger.error("InnoDB: Transaction rolled back due to deadlock")
        logger.critical("Automatic deadlock detection triggered - transaction aborted")
        
    def _database_slow_queries(self):
        service = 'product-service'
        incident_id = self.save_incident_metadata('database_slow_queries', service, 'medium',
                                                 {'slow_query_threshold': '2s', 'affected_tables': ['products', 'categories']})
        logger.error(f"INCIDENT_ID:{incident_id} - SLOW QUERY PERFORMANCE ALERT")
        logger.error("Query execution time: 15.3s (threshold: 2s)")
        logger.error("SELECT * FROM products WHERE category_id IN (SELECT id FROM categories WHERE name LIKE '%electronics%')")
        logger.error("Missing index on products.category_id detected")
        logger.warning("Database CPU utilization: 87%")
        
    def _database_replication_lag(self):
        incident_id = self.save_incident_metadata('database_replication_lag', 'database', 'medium',
                                                 {'replication_delay': '45s', 'master_server': 'db-master-01', 'slave_server': 'db-slave-02'})
        logger.error(f"INCIDENT_ID:{incident_id} - DATABASE REPLICATION LAG")
        logger.error("Replication delay: 45s between master and slave")
        logger.error("Slave server db-slave-02 falling behind master")
        logger.warning("Read queries may return stale data")
        logger.error("Binlog position mismatch detected")
        
    def _database_connection_timeout(self):
        service = 'payment-service'
        incident_id = self.save_incident_metadata('database_connection_timeout', service, 'high',
                                                 {'timeout_duration': '30s', 'connection_attempts': 5})
        logger.error(f"INCIDENT_ID:{incident_id} - DATABASE CONNECTION TIMEOUT")
        logger.error("Connection attempt #5 failed after 30s timeout")
        logger.error("Database server not responding to connection requests")
        logger.error("Connection string: jdbc:mysql://db-cluster:3306/payments")
        logger.critical("Payment processing halted - database unreachable")
        self.services[service]['status'] = 'degraded'

    # Enhanced API Failures
    def _api_rate_limiting(self):
        incident_id = self.save_incident_metadata('api_rate_limiting', 'payment-service', 'medium',
                                                 {'rate_limit': '100/min', 'current_rate': '156/min', 'api_provider': 'stripe'})
        logger.error(f"INCIDENT_ID:{incident_id} - API RATE LIMIT EXCEEDED")
        logger.error("Stripe API rate limit exceeded: 156 requests/min (limit: 100/min)")
        logger.error("HTTP 429: Too Many Requests received")
        logger.warning("Implementing exponential backoff with jitter")
        logger.error("Payment processing delayed by average 2.3 seconds")

    def _service_mesh_failure(self):
        incident_id = self.save_incident_metadata('service_mesh_failure', 'istio-proxy', 'critical',
                                                 {'mesh_version': 'v1.15.0', 'affected_routes': ['/api/orders', '/api/payments']})
        logger.error(f"INCIDENT_ID:{incident_id} - SERVICE MESH ROUTING FAILURE")
        logger.error("Istio proxy sidecar not responding")
        logger.error("Service discovery failed for payment-service.default.svc.cluster.local")
        logger.error("HTTP 503: Service Unavailable from envoy proxy")
        logger.critical("Inter-service communication broken")

    def _circuit_breaker_open(self):
        service = 'order-service'
        incident_id = self.save_incident_metadata('circuit_breaker_open', service, 'high',
                                                 {'failure_threshold': 5, 'failure_count': 8, 'circuit_state': 'open'})
        logger.error(f"INCIDENT_ID:{incident_id} - CIRCUIT BREAKER OPENED")
        logger.error("Circuit breaker opened for inventory-service calls")
        logger.error("Failure threshold exceeded: 8/5 failures in 60s window")
        logger.error("Fallback mechanism: Using cached inventory data")
        logger.warning("Order processing using potentially stale inventory")

    def _load_balancer_failure(self):
        incident_id = self.save_incident_metadata('load_balancer_failure', 'nginx-lb', 'critical',
                                                 {'upstream_servers': 3, 'healthy_servers': 0})
        logger.error(f"INCIDENT_ID:{incident_id} - LOAD BALANCER HEALTH CHECK FAILURE")
        logger.error("All upstream servers marked as down")
        logger.error("nginx: no live upstreams while connecting to upstream")
        logger.error("Health check failed for user-service:8001, user-service:8002, user-service:8003")
        logger.critical("Service completely unavailable - no healthy backends")

    # Enhanced Performance Issues
    def _cache_thrashing(self):
        service = 'product-service'
        incident_id = self.save_incident_metadata('cache_thrashing', service, 'medium',
                                                 {'cache_hit_rate': '12%', 'normal_hit_rate': '85%', 'cache_size': '2GB'})
        logger.error(f"INCIDENT_ID:{incident_id} - CACHE THRASHING DETECTED")
        logger.error("Redis cache hit rate dropped to 12% (normal: 85%)")
        logger.error("Frequent cache evictions due to memory pressure")
        logger.error("Cache key pattern causing hotspot: product:search:*")
        logger.warning("Database query load increased by 340%")

    def _thread_pool_exhaustion(self):
        service = 'user-service'
        incident_id = self.save_incident_metadata('thread_pool_exhaustion', service, 'high',
                                                 {'max_threads': 200, 'active_threads': 200, 'queued_requests': 1500})
        logger.error(f"INCIDENT_ID:{incident_id} - THREAD POOL EXHAUSTION")
        logger.error("All 200 threads in use - no threads available")
        logger.error("Request queue size: 1500 (max: 1000)")
        logger.error("java.util.concurrent.RejectedExecutionException")
        logger.critical("Service rejecting new requests - immediate scaling required")

    def _garbage_collection_pressure(self):
        service = 'product-service'
        incident_id = self.save_incident_metadata('garbage_collection_pressure', service, 'high',
                                                 {'gc_time_percentage': '45%', 'heap_usage': '95%'})
        logger.error(f"INCIDENT_ID:{incident_id} - EXCESSIVE GARBAGE COLLECTION")
        logger.error("GC consuming 45% of CPU time (threshold: 10%)")
        logger.error("Old generation heap usage: 95%")
        logger.error("Full GC triggered 15 times in last minute")
        logger.critical("Application pauses causing timeout failures")

    # Enhanced Infrastructure Issues
    def _dns_resolution_failure(self):
        incident_id = self.save_incident_metadata('dns_resolution_failure', 'dns', 'high',
                                                 {'failed_domains': ['payment-gateway.com', 'inventory-api.internal']})
        logger.error(f"INCIDENT_ID:{incident_id} - DNS RESOLUTION FAILURE")
        logger.error("Cannot resolve payment-gateway.com: NXDOMAIN")
        logger.error("DNS server 8.8.8.8 not responding")
        logger.error("Local DNS cache expired for critical services")
        logger.critical("External service integrations failing")

    def _kubernetes_pod_eviction(self):
        service = 'order-service'
        incident_id = self.save_incident_metadata('kubernetes_pod_eviction', service, 'critical',
                                                 {'eviction_reason': 'NodePressure', 'node_name': 'worker-node-03'})
        logger.error(f"INCIDENT_ID:{incident_id} - KUBERNETES POD EVICTED")
        logger.error("Pod order-service-7d6f8b9-xyz evicted from node worker-node-03")
        logger.error("Eviction reason: NodePressure (memory)")
        logger.error("Available memory on node: 0.1GB (threshold: 1GB)")
        logger.critical("Service capacity reduced by 33%")

    def _auto_scaling_failure(self):
        service = 'user-service'
        incident_id = self.save_incident_metadata('auto_scaling_failure', service, 'high',
                                                 {'target_replicas': 10, 'current_replicas': 3, 'cpu_utilization': '92%'})
        logger.error(f"INCIDENT_ID:{incident_id} - AUTO-SCALING FAILURE")
        logger.error("HPA unable to scale beyond 3 replicas (target: 10)")
        logger.error("Resource quota exceeded: requests.cpu")
        logger.error("Node pool at maximum capacity")
        logger.critical("Cannot handle current load - service degradation inevitable")

    # Enhanced Security Issues
    def _sql_injection_attempt(self):
        incident_id = self.save_incident_metadata('sql_injection_attempt', 'user-service', 'critical',
                                                 {'attack_pattern': "' OR '1'='1", 'source_ip': '203.0.113.42'})
        logger.error(f"INCIDENT_ID:{incident_id} - SQL INJECTION ATTEMPT DETECTED")
        logger.error("Suspicious query pattern detected: ' OR '1'='1 --")
        logger.error("Source IP: 203.0.113.42 (flagged as malicious)")
        logger.error("Attempted SQL injection on login endpoint")
        logger.critical("WAF blocked request - security team alerted")

    def _ddos_attack(self):
        incident_id = self.save_incident_metadata('ddos_attack', 'load-balancer', 'critical',
                                                 {'request_rate': '10000/s', 'normal_rate': '500/s', 'attack_vectors': ['HTTP flood', 'SYN flood']})
        logger.error(f"INCIDENT_ID:{incident_id} - DDOS ATTACK IN PROGRESS")
        logger.error("Abnormal traffic detected: 10,000 requests/second")
        logger.error("Attack vectors: HTTP flood + SYN flood")
        logger.error("Multiple source IPs from botnet")
        logger.critical("Rate limiting activated - legitimate traffic affected")

    def _certificate_expiration(self):
        incident_id = self.save_incident_metadata('certificate_expiration', 'payment-service', 'critical',
                                                 {'certificate_domain': 'api.payments.com', 'expiry_date': '2024-01-15'})
        logger.error(f"INCIDENT_ID:{incident_id} - SSL CERTIFICATE EXPIRED")
        logger.error("Certificate for api.payments.com expired on 2024-01-15")
        logger.error("SSL handshake failures causing payment API errors")
        logger.error("Browser warnings blocking customer payments")
        logger.critical("Revenue impact - immediate certificate renewal required")

    def _unauthorized_access_attempt(self):
        incident_id = self.save_incident_metadata('unauthorized_access_attempt', 'admin-panel', 'high',
                                                 {'failed_attempts': 25, 'source_ip': '198.51.100.123', 'target_accounts': ['admin', 'root']})
        logger.error(f"INCIDENT_ID:{incident_id} - UNAUTHORIZED ACCESS ATTEMPT")
        logger.error("25 failed login attempts on admin panel")
        logger.error("Source IP: 198.51.100.123 targeting admin/root accounts")
        logger.error("Brute force attack pattern detected")
        logger.warning("Account lockout mechanism triggered")

    # Enhanced Deployment Issues  
    def _deployment_rollback_failure(self):
        service = 'product-service'
        incident_id = self.save_incident_metadata('deployment_rollback_failure', service, 'critical',
                                                 {'current_version': 'v2.1.1', 'target_version': 'v2.1.0', 'rollback_reason': 'configuration_error'})
        logger.error(f"INCIDENT_ID:{incident_id} - DEPLOYMENT ROLLBACK FAILED")
        logger.error("Cannot rollback from v2.1.1 to v2.1.0")
        logger.error("Database schema migration cannot be reverted")
        logger.error("kubectl rollout undo deployment/product-service failed")
        logger.critical("Service stuck in broken state - manual intervention required")

    def _health_check_failure(self):
        service = 'inventory-service'
        incident_id = self.save_incident_metadata('health_check_failure', service, 'high',
                                                 {'health_endpoint': '/health', 'status_code': 503, 'dependency_failures': ['database', 'redis']})
        logger.error(f"INCIDENT_ID:{incident_id} - HEALTH CHECK FAILURE")
        logger.error("Health endpoint /health returning 503")
        logger.error("Dependency check failed: database connection error")
        logger.error("Dependency check failed: Redis connection timeout")
        logger.warning("Load balancer removing service from rotation")

    def _version_compatibility_issue(self):
        incident_id = self.save_incident_metadata('version_compatibility_issue', 'order-service', 'high',
                                                 {'service_versions': {'order-service': 'v1.5.7', 'payment-service': 'v3.0.1'}, 'incompatible_api': '/api/v2/process-payment'})
        logger.error(f"INCIDENT_ID:{incident_id} - VERSION COMPATIBILITY ERROR")
        logger.error("API version mismatch between order-service v1.5.7 and payment-service v3.0.1")
        logger.error("Endpoint /api/v2/process-payment not found")
        logger.error("Payment processing failing due to API contract changes")
        logger.critical("Service integration broken - urgent version alignment needed")

    def _environment_variable_missing(self):
        service = 'notification-service'
        incident_id = self.save_incident_metadata('environment_variable_missing', service, 'medium',
                                                 {'missing_variables': ['SMTP_HOST', 'EMAIL_API_KEY'], 'config_source': 'kubernetes_configmap'})
        logger.error(f"INCIDENT_ID:{incident_id} - ENVIRONMENT VARIABLE MISSING")
        logger.error("Required environment variable SMTP_HOST not set")
        logger.error("Required environment variable EMAIL_API_KEY not found")
        logger.error("ConfigMap notification-config missing required keys")
        logger.warning("Email notifications disabled - customers not receiving order updates")

    def get_current_metrics(self):
        """Get current system metrics for incident context"""
        return {
            'cpu_usage': random.randint(15, 95),
            'memory_usage': random.randint(30, 88),
            'disk_usage': random.randint(45, 97),
            'network_latency': random.uniform(0.1, 3.2),
            'active_connections': random.randint(50, 500)
        }

    def get_affected_services(self):
        """Get list of affected services based on current status"""
        affected = []
        for service, config in self.services.items():
            if config['status'] != 'running':
                affected.append({
                    'service': service,
                    'status': config['status'],
                    'port': config['port'],
                    'version': config['version']
                })
        return affected

    def generate_access_logs(self):
        """Generate realistic access log entries with error patterns"""
        # Create separate access logger
        access_logger = logging.getLogger('access')
        access_logger.setLevel(logging.INFO)
        
        # Remove any existing handlers to avoid duplicates
        access_logger.handlers.clear()
        
        # Create access log handler
        access_handler = logging.FileHandler(access_log_file)
        access_handler.setFormatter(logging.Formatter('%(message)s'))
        access_logger.addHandler(access_handler)
        access_logger.propagate = False  # Prevent propagation to parent logger
        
        # Enhanced endpoints with more realistic patterns
        endpoints = [
            ('/api/v1/users/profile', 'GET', 8001),
            ('/api/v1/users/register', 'POST', 8001),
            ('/api/v1/users/login', 'POST', 8001),
            ('/api/v2/products/search', 'GET', 8002),
            ('/api/v2/products/categories', 'GET', 8002),
            ('/api/v1/orders/create', 'POST', 8003),
            ('/api/v1/orders/status/{id}', 'GET', 8003),
            ('/api/v3/payments/process', 'POST', 8004),
            ('/api/v1/inventory/check', 'GET', 8005),
            ('/api/v1/notifications/send', 'POST', 8006),
            ('/health', 'GET', random.choice([8001, 8002, 8003, 8004, 8005, 8006])),
            ('/metrics', 'GET', random.choice([8001, 8002, 8003, 8004, 8005, 8006]))
        ]
        
        user_agents = [
            'curl/7.68.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'PostmanRuntime/7.28.4',
            'monitoring/1.0',
            'python-requests/2.28.2',
            'mobile-app/2.1.0',
            'react-frontend/1.5.2'
        ]
        
        for _ in range(random.randint(15, 35)):
            endpoint, method, port = random.choice(endpoints)
            user_agent = random.choice(user_agents)
            
            # More realistic endpoint patterns
            if '{id}' in endpoint:
                endpoint = endpoint.replace('{id}', str(random.randint(1000, 9999)))
            
            # Determine status code based on service health and add incident-specific patterns
            service_name = list(self.services.keys())[port-8001]
            service_status = self.services[service_name]['status']
            
            if service_status == 'running':
                status_code = random.choices([200, 201, 400, 404, 422], weights=[80, 5, 8, 5, 2])[0]
            elif service_status == 'degraded':
                status_code = random.choices([200, 500, 502, 503, 504], weights=[50, 20, 10, 15, 5])[0]
            elif service_status == 'critical':
                status_code = random.choices([500, 502, 503, 504], weights=[35, 20, 30, 15])[0]
            else:  # down
                status_code = random.choices([502, 503, 504], weights=[30, 50, 20])[0]
            
            response_size = random.randint(45, 2048)
            response_time = random.uniform(0.05, 5.0)
            timestamp = datetime.now().strftime('%d/%b/%Y:%H:%M:%S +0000')
            
            # Add response time to access logs for better analysis
            access_entry = f'127.0.0.1 - - [{timestamp}] "{method} {endpoint} HTTP/1.1" {status_code} {response_size} "-" "{user_agent}" {response_time:.3f}s'
            access_logger.info(access_entry)

    def generate_metrics(self):
        """Generate realistic metrics for monitoring with incident correlation"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'incident_id': self.current_incident['incident_id'] if self.current_incident else None,
            'services': {},
            'system': {
                'cpu_usage': random.randint(15, 95),
                'memory_usage': random.randint(30, 88),
                'disk_usage': random.randint(45, 97),
                'network_latency': random.uniform(0.1, 3.2),
                'load_average': random.uniform(0.5, 8.0),
                'active_connections': random.randint(50, 500)
            },
            'database': {
                'connection_pool_usage': random.randint(5, 50),
                'query_response_time': random.uniform(0.1, 2.5),
                'active_transactions': random.randint(0, 25),
                'deadlock_count': random.randint(0, 3)
            },
            'cache': {
                'redis_hit_rate': random.uniform(0.75, 0.98),
                'memory_usage': random.randint(30, 90),
                'evicted_keys': random.randint(0, 100),
                'connection_count': random.randint(10, 100)
            }
        }
        
        for service, config in self.services.items():
            # Adjust metrics based on service status for realistic incident correlation
            base_error_rate = 0.5 if config['status'] == 'running' else 8.0
            base_response_time = 0.2 if config['status'] == 'running' else 2.0
            
            metrics['services'][service] = {
                'status': config['status'],
                'version': config['version'],
                'response_time': random.uniform(base_response_time, base_response_time * 3),
                'error_rate': random.uniform(0, base_error_rate * 2),
                'throughput': random.randint(50, 1200) if config['status'] == 'running' else random.randint(10, 300),
                'cpu_usage': config.get('cpu_usage', random.randint(10, 45)),
                'memory_usage': random.randint(20, 85),
                'active_threads': random.randint(5, 200),
                'gc_time': random.uniform(0.01, 0.15) if service.endswith('-service') else 0
            }
        
        logger.info(f"METRICS: {json.dumps(metrics, indent=2)}")
        return metrics

    def health_check(self):
        """Perform comprehensive health checks on all services"""
        logger.info("=== COMPREHENSIVE HEALTH CHECK STARTED ===")
        
        overall_health = "HEALTHY"
        critical_count = 0
        degraded_count = 0
        
        for service, config in self.services.items():
            status = config['status']
            port = config['port']
            version = config['version']
            
            if status == 'running':
                logger.info(f"✅ {service} (port {port}, {version}): HEALTHY")
            elif status == 'degraded':
                logger.warning(f"⚠️  {service} (port {port}, {version}): DEGRADED - Performance issues detected")
                degraded_count += 1
                overall_health = "DEGRADED"
            elif status == 'critical':
                logger.error(f"🔥 {service} (port {port}, {version}): CRITICAL - Immediate attention required")
                critical_count += 1
                overall_health = "CRITICAL"
            elif status == 'down':
                logger.critical(f"❌ {service} (port {port}, {version}): DOWN - Service unavailable")
                critical_count += 1
                overall_health = "CRITICAL"
        
        logger.info(f"=== HEALTH CHECK SUMMARY ===")
        logger.info(f"Overall Status: {overall_health}")
        logger.info(f"Critical Services: {critical_count}")
        logger.info(f"Degraded Services: {degraded_count}")
        logger.info("=== HEALTH CHECK COMPLETED ===")

    def run_load_test(self):
        """Simulate comprehensive load testing that triggers various issues"""
        logger.info("🔄 Starting comprehensive load test simulation...")
        
        # Simulate different types of load patterns
        load_patterns = [
            {'name': 'normal_load', 'requests': 10, 'workers': 3},
            {'name': 'spike_load', 'requests': 25, 'workers': 8},
            {'name': 'sustained_high_load', 'requests': 50, 'workers': 12}
        ]
        
        pattern = random.choice(load_patterns)
        logger.info(f"Load pattern: {pattern['name']} - {pattern['requests']} requests, {pattern['workers']} workers")
        
        # Simulate concurrent requests
        with ThreadPoolExecutor(max_workers=pattern['workers']) as executor:
            futures = []
            for i in range(pattern['requests']):
                future = executor.submit(self._simulate_request, f"load_test_req_{i}", pattern['name'])
                futures.append(future)
            
            # Wait for completion and potentially trigger errors
            success_count = 0
            error_count = 0
            for future in futures:
                try:
                    future.result(timeout=5)
                    success_count += 1
                except Exception as e:
                    logger.error(f"Load test request failed: {str(e)}")
                    error_count += 1
        
        logger.info(f"Load test completed - Success: {success_count}, Errors: {error_count}")

    def _simulate_request(self, request_id, load_pattern):
        """Simulate individual service requests with realistic patterns"""
        # Random delay to simulate processing
        base_delay = 0.1 if load_pattern == 'normal_load' else 0.5
        time.sleep(random.uniform(base_delay, base_delay * 3))
        
        # Adjust failure rate based on load pattern and service status
        failure_rate = 0.1 if load_pattern == 'normal_load' else 0.3
        
        # Higher failure rate if services are degraded
        degraded_services = [s for s, c in self.services.items() if c['status'] != 'running']
        if degraded_services:
            failure_rate += 0.2
        
        if random.random() < failure_rate:
            service = random.choice(list(self.services.keys()))
            error_types = ['connection_timeout', 'service_unavailable', 'internal_error', 'rate_limit_exceeded']
            error = random.choice(error_types)
            logger.error(f"Request {request_id} failed on {service}: {error}")
            raise Exception(f"Service {service} error: {error}")
        
        logger.info(f"Request {request_id} completed successfully")

    def simulate_recovery_scenario(self):
        """Simulate service recovery for realistic incident lifecycle"""
        logger.info("🔧 Initiating recovery procedures...")
        
        # Reset some services to simulate recovery
        recovering_services = [s for s, c in self.services.items() if c['status'] != 'running']
        
        if recovering_services:
            service_to_recover = random.choice(recovering_services)
            old_status = self.services[service_to_recover]['status']
            
            # Simulate gradual recovery
            if old_status == 'down':
                self.services[service_to_recover]['status'] = 'critical'
                logger.info(f"🔄 {service_to_recover}: DOWN → CRITICAL (partial recovery)")
            elif old_status == 'critical':
                self.services[service_to_recover]['status'] = 'degraded'
                logger.info(f"🔄 {service_to_recover}: CRITICAL → DEGRADED (improvement detected)")
            elif old_status == 'degraded':
                self.services[service_to_recover]['status'] = 'running'
                logger.info(f"✅ {service_to_recover}: DEGRADED → RUNNING (full recovery)")
                
            # Update incident status if we have one
            if self.current_incident and self.current_incident['service'] == service_to_recover:
                if self.services[service_to_recover]['status'] == 'running':
                    self.current_incident['resolution_status'] = 'resolved'
                    logger.info(f"✅ Incident {self.current_incident['incident_id']} resolved")

    def generate_business_impact_data(self):
        """Generate business impact metrics for incidents"""
        if not self.current_incident:
            return
            
        impact_data = {
            'incident_id': self.current_incident['incident_id'],
            'revenue_impact': random.uniform(1000, 50000),
            'affected_customers': random.randint(50, 5000),
            'failed_transactions': random.randint(10, 500),
            'sla_breach': random.choice([True, False]),
            'customer_complaints': random.randint(0, 25),
            'downtime_minutes': random.randint(1, 60)
        }
        
        logger.info(f"BUSINESS_IMPACT: {json.dumps(impact_data, indent=2)}")
        return impact_data

def create_rag_knowledge_structure():
    """Create initial RAG knowledge base structure with sample data"""
    rag_structure = {
        "remediation_patterns": {
            "database_issues": [
                {
                    "pattern": "connection_pool_exhaustion",
                    "symptoms": ["connection timeout", "pool size exceeded", "waiting connections"],
                    "remediation": ["Increase connection pool size", "Optimize query performance", "Implement connection pooling best practices"],
                    "success_rate": 0.85
                },
                {
                    "pattern": "slow_queries", 
                    "symptoms": ["high query execution time", "database CPU spike", "missing indexes"],
                    "remediation": ["Add database indexes", "Query optimization", "Implement query caching"],
                    "success_rate": 0.92
                }
            ],
            "api_failures": [
                {
                    "pattern": "rate_limiting",
                    "symptoms": ["HTTP 429", "rate limit exceeded", "request throttling"],
                    "remediation": ["Implement exponential backoff", "Request rate optimization", "Upgrade API plan"],
                    "success_rate": 0.88
                }
            ],
            "performance_bottlenecks": [
                {
                    "pattern": "memory_leak",
                    "symptoms": ["increasing memory usage", "OutOfMemoryError", "frequent GC"],
                    "remediation": ["Memory profiling", "Fix memory leaks", "Increase heap size", "Restart service"],
                    "success_rate": 0.78
                }
            ]
        },
        "historical_reports": {
            "successful_resolutions": [
                {
                    "incident_type": "database_connection_leak",
                    "resolution_time": "45 minutes",
                    "root_cause": "Connection pool misconfiguration",
                    "solution": "Increased max connections from 20 to 50",
                    "lessons_learned": "Monitor connection pool metrics proactively"
                }
            ]
        }
    }
    
    # Save RAG structure to file
    os.makedirs("rag_knowledge_base", exist_ok=True)
    with open("rag_knowledge_base/knowledge_structure.json", "w") as f:
        json.dump(rag_structure, f, indent=2)
    
    logger.info("📚 RAG knowledge base structure created")

def main():
    """Main execution function that generates comprehensive scenarios for postmortem analysis"""
    print("🚀 Starting Enhanced E-commerce Platform Simulation")
    print("=" * 70)
    
    platform = EcommercePlatform()
    
    try:
        # Create RAG knowledge base structure
        create_rag_knowledge_structure()
        
        # Initial health check
        platform.health_check()
        time.sleep(2)
        
        # Generate baseline metrics
        logger.info("📊 Generating baseline metrics...")
        platform.generate_metrics()
        
        # Generate initial access logs
        logger.info("🌐 Generating access logs...")
        platform.generate_access_logs()
        time.sleep(2)
        
        # Simulate normal operations
        logger.info("✅ Platform running normally...")
        time.sleep(3)
        
        # Multiple load test cycles
        for cycle in range(2):
            logger.info(f"🔄 Load test cycle {cycle + 1}")
            platform.run_load_test()
            time.sleep(2)
        
        # Trigger multiple incidents with recovery scenarios
        logger.info("🎯 Simulating comprehensive incident scenarios...")
        for i in range(random.randint(3, 6)):
            platform.simulate_incident()
            time.sleep(random.uniform(1, 3))
            
            # Generate metrics during incident
            platform.generate_metrics()
            platform.generate_access_logs()
            
            # Generate business impact data
            platform.generate_business_impact_data()
            
            # Sometimes simulate recovery
            if random.random() < 0.4:  # 40% chance of recovery
                time.sleep(2)
                platform.simulate_recovery_scenario()
                platform.generate_metrics()
        
        # Final health check and metrics
        time.sleep(2)
        platform.health_check()
        final_metrics = platform.generate_metrics()
        
        print("\n" + "=" * 70)
        print("🏁 Enhanced simulation completed!")
        print("📝 Generated comprehensive incident data:")
        print("   - Application logs with structured errors")
        print("   - Access logs with realistic traffic patterns") 
        print("   - Error logs with detailed stack traces")
        print("   - Incident metadata in JSON format")
        print("   - Business impact metrics")
        print("   - Recovery scenarios")
        print("📚 RAG knowledge base structure created")
        print("🔍 Ready for MCP-based postmortem analysis")
        print("=" * 70)
        
    except KeyboardInterrupt:
        logger.info("🛑 Platform simulation interrupted by user")
        print("\nSimulation stopped by user")
    except Exception as e:
        logger.critical(f"💥 FATAL ERROR: {str(e)}")
        print(f"\nFatal error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()