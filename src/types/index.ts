export interface AuditResult {
    id: string;
    rule_id: string;
    status: 'PASS' | 'FAIL' | 'WARN';
    message: string;
    coordinates: {
        page: number;
        x: number;
        y: number;
        w: number;
        h: number;
    };
}

export interface ServiceRecordMeta {
    file_name: string;
    total_pages: number;
    upload_timestamp: number;
}

export interface AuditResponse {
    record_meta: ServiceRecordMeta;
    audit_results: AuditResult[];
}
