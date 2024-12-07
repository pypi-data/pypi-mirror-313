from enum import Enum


class KEYS_MESSAGES(str, Enum):
    CORE_QUERY_MADE = "core_query_made"
    CORE_SAVED_INFORMATION = "core_saved_information"
    CORE_UPDATED_INFORMATION = "core_updated_information"
    CORE_DELETION_PERFORMED = "core_deletion_performed"
    CORE_RECORD_NOT_FOUND_TO_DELETE = "core_record_not_found_to_delete"
    CORE_NO_RESULTS_FOUND = "core_no_results_found"
    CORE_RECORD_NOT_FOUND = "core_record_not_found"
    CORE_ERROR_SAVING_RECORD = "core_error_saving_record"
    CORE_UPDATE_FAILED = "core_update_failed"
