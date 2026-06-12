export interface AuditItem {
  area: string;
  owner: string;
  branchType: string;
  productLine: string;
  score: number;
  level: string;
  drivers: string[];
  recommendation: string;
  note: string;
}

export interface GuardrailsInfo {
  allowed: boolean;
  in_scope: boolean;
  human_review_required: boolean;
  negative_test: {
    passed: boolean;
    issues: string[];
  };
  pii_redaction: {
    redacted: string;
    findings: { type: string; value: string }[];
  };
  safe_question: string;
}

export interface ChatResponse {
  answer: string;
  context: { source?: string; text?: string; distance?: number }[];
  type: 'normal' | 'fallback' | 'blocked';
  in_scope: boolean;
  guardrails?: GuardrailsInfo | null;
}