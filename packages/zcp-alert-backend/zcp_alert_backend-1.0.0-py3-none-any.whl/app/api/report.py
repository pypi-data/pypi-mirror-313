import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from app.auth.oauth2_keycloak import TokenData, get_current_user
from app.exception.common_exception import AlertBackendException, AlertError
from app.model.alert_model import AlertStatus
from app.service.report_service import ReportService

# import matplotlib.pyplot as plt

log = logging.getLogger("appLogger")

router = APIRouter()

__service = ReportService()


@router.get(
    "/report/alerts/by/status",
    summary="Get number of alerts by status",
    response_class=JSONResponse,
    response_model=list[dict],
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def get_number_of_alert_by_status(
    exclude_closed: Optional[bool] = Query(
        False, title="exclude closed", description="Exclude closed alerts"
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> list[dict]:
    excludes_status = []
    if exclude_closed:
        excludes_status.append(AlertStatus.CLOSED)
    result = __service.get_number_of_alerts_by_status(excludes_status=excludes_status)

    # df = pd.DataFrame(result)
    # plot_pie_chart(df)

    return result


@router.get(
    "/report/alerts/by/priority",
    summary="Get number of alerts by priority",
    response_class=JSONResponse,
    response_model=list[dict],
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_number_of_alert_by_priority(
    exclude_closed: Optional[bool] = Query(
        False, title="exclude closed", description="Exclude closed alerts"
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> list[dict]:
    excludes_status = []
    if exclude_closed:
        excludes_status.append(AlertStatus.CLOSED)
    return __service.get_number_of_alerts_by_label(
        key_label="priority", excludes_status=excludes_status
    )


@router.get(
    "/report/alerts/by/alertname",
    summary="Get number of alerts by alertname",
    response_class=JSONResponse,
    response_model=list[dict],
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_number_of_alert_by_alertname(
    exclude_closed: Optional[bool] = Query(
        False, title="exclude closed", description="Exclude closed alerts"
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> list[dict]:
    excludes_status = []
    if exclude_closed:
        excludes_status.append(AlertStatus.CLOSED)
    return __service.get_number_of_alerts_by_label(
        key_label="alertname", excludes_status=excludes_status, limit=5
    )


@router.get(
    "/report/alerts/by/cluster",
    summary="Get number of alerts by cluster",
    response_class=JSONResponse,
    response_model=list[dict],
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_number_of_alert_by_cluster(
    exclude_closed: Optional[bool] = Query(
        False, title="exclude closed", description="Exclude closed alerts"
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> list[dict]:
    excludes_status = []
    if exclude_closed:
        excludes_status.append(AlertStatus.CLOSED)
    return __service.get_number_of_alerts_by_label(
        key_label="cluster", excludes_status=excludes_status, limit=5
    )


@router.get(
    "/report/alerts/by/label",
    summary="Get number of alerts by label with limit",
    response_class=JSONResponse,
    response_model=list[dict],
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_number_of_alert_by_label(
    label: str = Query(
        ..., max_length=100, min_length=3, title="label", description="Label to filter"
    ),
    exclude_closed: Optional[bool] = Query(
        False, title="exclude closed", description="Exclude closed alerts"
    ),
    limit: Optional[int] = Query(
        10, title="limit", description="Limit the number of results"
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> list[dict]:
    excludes_status = []
    if exclude_closed:
        excludes_status.append(AlertStatus.CLOSED)
    return __service.get_number_of_alerts_by_label(
        key_label=label, excludes_status=excludes_status, limit=limit
    )


@router.get(
    "/report/alerts/trend/by/priority",
    summary="Get alert count trend by priority",
    response_class=JSONResponse,
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_alert_trend_data_by_priority(
    start_date: str = Query(
        ...,
        title="start_date",
        description="Start date to filter (ISO 8601 format(e.g. 2024-11-01T00:00:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    end_date: str = Query(
        ...,
        title="end_date",
        description="End date to filter (ISO 8601 format(e.g. 2024-11-31T23:59:59.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> dict:
    start_date = datetime.fromisoformat(start_date)  # .astimezone(DEFAULT_TIME_ZONE)
    end_date = datetime.fromisoformat(end_date)  # .astimezone(DEFAULT_TIME_ZONE)

    if start_date > end_date:
        raise AlertBackendException(
            AlertError.BAD_REQUEST,
            details=f"start_date({start_date}) should be less than end_date({end_date})",
        )

    data = __service.get_number_of_alerts_by_priority_trend_data(
        start_date=start_date, end_date=end_date
    )

    df = pd.DataFrame(data)
    df = df.fillna(0)

    log.info(f"dataframe is \n{df}")

    # _plot_line_chart(df)

    return data


@router.get(
    "/report/alerts/mttar/counts",
    summary="Get alert count regarding MTTA and MTTR (created, closed)",
    response_class=JSONResponse,
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_number_of_alert_mttar(
    start_date: str = Query(
        ...,
        title="start_date",
        description="Start date to filter (ISO 8601 format(e.g. 2024-11-01T00:00:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    end_date: str = Query(
        ...,
        title="end_date",
        description="End date to filter (ISO 8601 format(e.g. 2024-11-31T23:59:59.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> dict:
    start_date = datetime.fromisoformat(start_date)  # .astimezone(DEFAULT_TIME_ZONE)
    end_date = datetime.fromisoformat(end_date)  # .astimezone(DEFAULT_TIME_ZONE)

    if start_date > end_date:
        raise AlertBackendException(
            AlertError.BAD_REQUEST,
            details=f"start_date({start_date}) should be less than end_date({end_date})",
        )

    created_count = __service.get_number_of_alerts_for_mttar(
        date_field="CREATED", start_date=start_date, end_date=end_date
    )

    # acknowledged_count = __service.get_alerts_count_with_date_field(
    #     date_field='ACKNOWLEDGED',
    #     start_date=start_date,
    #     end_date=end_date
    # )

    closed_count = __service.get_number_of_alerts_for_mttar(
        date_field="CLOSED", start_date=start_date, end_date=end_date
    )

    return {
        "created_count": created_count,
        # 'acknowledged_count': acknowledged_count,
        "closed_count": closed_count,
    }


@router.get(
    "/report/alerts/mttar",
    summary="Get alert MTTA and MTTR. Returns the mean time to acknowledge and resolve alerts in minutes",
    response_class=JSONResponse,
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_alert_mttar(
    start_date: str = Query(
        ...,
        title="start_date",
        description="Start date to filter (ISO 8601 format(e.g. 2024-11-01T00:00:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    end_date: str = Query(
        ...,
        title="end_date",
        description="End date to filter (ISO 8601 format(e.g. 2024-11-31T23:59:59.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> dict:
    start_date = datetime.fromisoformat(start_date)  # .astimezone(DEFAULT_TIME_ZONE)
    end_date = datetime.fromisoformat(end_date)  # .astimezone(DEFAULT_TIME_ZONE)

    if start_date > end_date:
        raise AlertBackendException(
            AlertError.BAD_REQUEST,
            details=f"start_date({start_date}) should be less than end_date({end_date})",
        )

    mtta = __service.get_alerts_mttar(
        type="MTTA", start_date=start_date, end_date=end_date
    )

    mttr = __service.get_alerts_mttar(
        type="MTTR", start_date=start_date, end_date=end_date
    )

    return {"mtta": mtta, "mttr": mttr}


@router.get(
    "/report/alerts/mtta/trend",
    summary="Get alert MTTA trend data",
    response_class=JSONResponse,
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_alert_mtta_trend_data(
    start_date: str = Query(
        ...,
        title="start_date",
        description="Start date to filter (ISO 8601 format(e.g. 2024-11-01T00:00:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    end_date: str = Query(
        ...,
        title="end_date",
        description="End date to filter (ISO 8601 format(e.g. 2024-11-31T23:59:59.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> dict:
    start_date = datetime.fromisoformat(start_date)  # .astimezone(DEFAULT_TIME_ZONE)
    end_date = datetime.fromisoformat(end_date)  # .astimezone(DEFAULT_TIME_ZONE)

    if start_date > end_date:
        raise AlertBackendException(
            AlertError.BAD_REQUEST,
            details=f"start_date({start_date}) should be less than end_date({end_date})",
        )

    data = __service.get_alerts_mtta_trend_data(
        start_date=start_date, end_date=end_date
    )

    df = pd.DataFrame(data, index=["count", "min", "max", "avg"])
    df = df.T
    # _plot_trend_chart(df)

    return df.to_dict()


@router.get(
    "/report/alerts/mttr/trend",
    summary="Get alert MTTR trend data",
    response_class=JSONResponse,
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_alert_mttr_trend_data(
    start_date: str = Query(
        ...,
        title="start_date",
        description="Start date to filter (ISO 8601 format(e.g. 2024-11-01T00:00:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    end_date: str = Query(
        ...,
        title="end_date",
        description="End date to filter (ISO 8601 format(e.g. 2024-11-31T23:59:59.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> dict:
    start_date = datetime.fromisoformat(start_date)  # .astimezone(DEFAULT_TIME_ZONE)
    end_date = datetime.fromisoformat(end_date)  # .astimezone(DEFAULT_TIME_ZONE)

    if start_date > end_date:
        raise AlertBackendException(
            AlertError.BAD_REQUEST,
            details=f"start_date({start_date}) should be less than end_date({end_date})",
        )

    data = __service.get_alerts_mttr_trend_data(
        start_date=start_date, end_date=end_date
    )

    df = pd.DataFrame(data, index=["count", "min", "max", "avg"])
    df = df.T
    # _plot_trend_chart(df)

    return df.to_dict()


"""
def _plot_trend_chart(df: pd.DataFrame):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 첫 번째 Y축에 알림 개수 바 차트 추가
    ax1.bar(df.index, df['count'], color='gray', alpha=0.7, label='Alerts')
    ax1.set_xlabel('Date alert created')
    ax1.set_ylabel('Alerts', color='black')

    # 두 번째 Y축에 평균, 최소, 최대 해결 시간 라인 그래프 추가
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['avg'], color='orange', marker='o', label='Average time')
    ax2.plot(df.index, df['min'], color='red', marker='o', label='Min time')
    ax2.plot(df.index, df['max'], color='gold', marker='o', label='Max time')
    ax2.set_ylabel('Time (minutes)', color='black')

    # 제목과 범례 추가
    fig.suptitle('Daily mean time to resolve/close')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.show()

def _plot_pie_chart(df: pd.DataFrame):
    # 데이터 준비
    labels = df['status']
    sizes = df['count']

    # 파이 차트 그리기
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # 차트 제목 설정
    plt.title('Alert Status Distribution')

    # 차트 보여주기
    plt.show()

def _plot_line_chart(df: pd.DataFrame):
    df = df.reindex(sorted(df.columns), axis=1)

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))

    # 각 우선순위(Priority) 별로 스택형 막대그래프 그리기
    df.T.plot(kind='bar', stacked=True, ax=ax)

    # 그래프 타이틀 및 축 라벨 설정
    ax.set_title("Number of alerts per day by priority", fontsize=16)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Number of alerts", fontsize=12)

    # 범례 설정 (Priority 별 색상)
    ax.legend(title="Priority", bbox_to_anchor=(1.05, 1), loc='upper left')

    # 날짜 레이블을 가로로 돌려서 표시
    plt.xticks(rotation=45)

    # 그래프 보여주기
    plt.tight_layout()
    plt.show()
"""
