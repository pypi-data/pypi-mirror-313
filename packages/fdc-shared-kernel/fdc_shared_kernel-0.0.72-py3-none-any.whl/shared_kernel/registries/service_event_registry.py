from shared_kernel.config import Config

config = Config()


class ServiceEventRegistry:
    # Sync events to master service to create/update status tracker
    CREATE_TASK = (
        config.get("MASTER_SERVICE_BASE_ENDPOINT")
        + "/event/subscribe-sync-event/CREATE_TASK/"
    )

    UPDATE_TASK = (
        config.get("MASTER_SERVICE_BASE_ENDPOINT")
        + "/event/subscribe-sync-event/UPDATE_TASK/"
    )

    MARK_TASK_AS_FAILURE = (
        config.get("MASTER_SERVICE_BASE_ENDPOINT")
        + "/event/subscribe-sync-event/MARK_TASK_AS_FAILURE/"
    )

    GET_TASK = (
        config.get("MASTER_SERVICE_BASE_ENDPOINT")
        + "/event/subscribe-sync-event/GET_TASK/"
    )

    GET_IN_PROGRESS_TASK = (
        config.get("MASTER_SERVICE_BASE_ENDPOINT")
        + "/event/subscribe-sync-event/GET_IN_PROGRESS_TASK/"
    )

    SET_EVENT_META_AND_MESSAGE_RECEIPT_HANDLE = (
        config.get("MASTER_SERVICE_BASE_ENDPOINT")
        + "/event/subscribe-sync-event/SET_EVENT_META_AND_MESSAGE_RECEIPT_HANDLE/"
    )

    SET_TRACKING_ID = (
        config.get("MASTER_SERVICE_BASE_ENDPOINT")
        + "/event/subscribe-sync-event/SET_TRACKING_ID/"
    )
