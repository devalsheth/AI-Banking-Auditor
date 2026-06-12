from app.services.vector_store import build_index

BANKING_KNOWLEDGE = [
    {'source': 'RBIA', 'text': 'Risk based internal audit in banks should align audit frequency and coverage to the institution risk profile, materiality, and changing regulatory expectations.'},
    {'source': 'AML', 'text': 'KYC and AML reviews should prioritize overdue refreshes, alert backlogs, weak screening evidence, and unusual transaction monitoring gaps.'},
    {'source': 'Treasury', 'text': 'Treasury audits should review liquidity reporting, investment controls, limit breaches, and valuation governance.'},
    {'source': 'ITGC', 'text': 'Core banking and privileged access audits should validate user provisioning, periodic access recertification, segregation of duties, and incident response evidence.'},
    {'source': 'Credit', 'text': 'Credit audit focus areas include underwriting exceptions, documentation gaps, NPA classification, collateral controls, and sanction deviations.'},
    {'source': 'Branch Ops', 'text': 'Branch operations audits should examine cash management, maker-checker breakdowns, dormant accounts, exception reversals, and customer grievance patterns.'},
    {'source': 'Regulatory', 'text': 'Regulatory reporting audits should assess timeliness, data lineage, reconciliation quality, and evidence for statutory submissions.'}
]

def bootstrap_knowledge_base():
    build_index(BANKING_KNOWLEDGE)
