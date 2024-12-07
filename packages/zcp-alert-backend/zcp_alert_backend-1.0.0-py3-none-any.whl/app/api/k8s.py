import logging

import kubernetes.client.models.v1_pod as V1Pod
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.exception.common_exception import AlertBackendException, AlertError
from app.k8s.kubernetes_proxy import KubernetesProxy

log = logging.getLogger("appLogger")

kubernetes_proxy = KubernetesProxy()

router = APIRouter()


@router.get("/kubernetes/{namespace}/pods", response_class=JSONResponse)
async def get_pods(namespace: str):
    pods = []
    for pod in kubernetes_proxy.get_pods(namespace):
        pods.append(__remove_managed_fields(pod))

    return pods


@router.get("/kubernetes/pods", response_class=JSONResponse)
async def get_all_pods():
    return get_pods(None)


@router.get("/kubernetes/pods/count", response_class=JSONResponse)
async def get_pods_count():
    count = kubernetes_proxy.get_pods_count(None)
    return {"count": count}


@router.get("/kubernetes/{namespace}/pods/count", response_class=JSONResponse)
async def get_pods_count_of_namespace(namespace: str):
    count = kubernetes_proxy.get_pods_count(namespace)
    return {"count": count}


@router.get("/kubernetes/{namespace}/pods/{pod_name}", response_class=JSONResponse)
async def get_pod(namespace: str, pod_name: str):
    return __remove_managed_fields(kubernetes_proxy.get_pod(namespace, pod_name))


def __remove_managed_fields(pod: V1Pod) -> dict:
    """
    Remove managed_fields from the pod object
    """
    pod_dict = pod.to_dict()
    try:
        del pod_dict["metadata"]["managed_fields"]
    except KeyError:
        raise AlertBackendException(
            AlertError.INTERNAL_SERVER_ERROR,
            details="managed_fields not found in the pod object",
        )
    return pod_dict
