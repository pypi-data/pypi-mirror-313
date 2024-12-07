import logging
from threading import Lock, Thread

import urllib3
from kubernetes import client, config, watch

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

log = logging.getLogger("appLogger")


class KubernetesProxy:
    def __init__(self):
        try:
            config.load_kube_config(
                "/Users/kks/cloud/aws/clusters/dev-clusters/zcp-system-admin.conf"
            )
        except Exception as e:
            log.critical(f"An error occurred: {e}")

        self.__pod_cache = {}
        self.__lock = Lock()
        self.__start_watch_thread()

        log.info("Initialized")

    def __add_or_update_pod(self, event_type, pod):
        with self.__lock:
            key = f"{pod.metadata.namespace}:{pod.metadata.name}"
            self.__pod_cache[key] = pod
            log.debug(f"Pod {key} : {event_type}")

    def __delete_pod(self, pod):
        with self.__lock:
            key = f"{pod.metadata.namespace}:{pod.metadata.name}"
            if key in self.__pod_cache:
                del self.__pod_cache[key]
                log.debug(f"Pod {key} : DELETED")

    def list_pods(self):
        """
        Deprecated
        """
        with self.__lock:
            return list(self.__pod_cache.values())

    def get_pods(self, namespace: str | None):
        with self.__lock:
            if namespace is None:
                return list(self.__pod_cache.values())
            else:
                return [
                    pod
                    for pod in self.__pod_cache.values()
                    if pod.metadata.namespace == namespace
                ]

    def __watch_pods(self):
        v1 = client.CoreV1Api()
        w = watch.Watch()

        for event in w.stream(v1.list_pod_for_all_namespaces):
            event_type = event["type"]
            pod = event["object"]

            if event_type == "ADDED" or event_type == "MODIFIED":
                self.__add_or_update_pod(event_type, pod)
            elif event_type == "DELETED":
                self.__delete_pod(pod)

    def __start_watch_thread(self):
        watch_thread = Thread(target=self.__watch_pods, args=())
        watch_thread.daemon = True
        watch_thread.start()

    def get_pod(self, namespace: str, pod_name: str):
        with self.__lock:
            for pod in self.__pod_cache.values():
                if (
                    pod.metadata.namespace == namespace
                    and pod.metadata.name == pod_name
                ):
                    return pod
            return None

    def get_pods_count(self, namespace: str | None):
        with self.__lock:
            if namespace is None:
                return len(self.__pod_cache)
            else:
                return len(
                    [
                        pod
                        for pod in self.__pod_cache.values()
                        if pod.metadata.namespace == namespace
                    ]
                )
