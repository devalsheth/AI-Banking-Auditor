import random

AREAS = [
    'KYC refresh monitoring', 'AML alert handling', 'Treasury liquidity reporting',
    'Loan underwriting quality', 'NPA classification review', 'Branch cash operations',
    'Core banking access review', 'SWIFT payment controls', 'Regulatory reporting',
    'ATM dispute handling', 'Fraud case management', 'Trade finance documentation'
]
OWNERS = ['Compliance', 'Treasury', 'Retail Ops', 'IT Controls', 'Credit Risk', 'Branch Ops']
BRANCH_TYPES = ['Retail', 'Corporate', 'Treasury', 'Digital', 'Rural']
PRODUCTS = ['Deposits', 'Loans', 'Cards', 'Trade Finance', 'Payments', 'Wealth']
NOTES = [
    'Exception trend increasing over last two quarters.',
    'Control evidence incomplete for sampled transactions.',
    'Regulatory scrutiny has increased for this process.',
    'Repeat findings indicate weak remediation governance.',
    'Large-value transactions increase materiality and audit attention.'
]

def generate_synthetic_audits(count: int = 20):
    items = []
    for _ in range(count):
        items.append({
            'area': random.choice(AREAS),
            'owner': random.choice(OWNERS),
            'impact': random.randint(2, 5),
            'likelihood': random.randint(2, 5),
            'openFindings': random.randint(0, 10),
            'repeatIssues': random.randint(0, 5),
            'controlMaturity': random.randint(1, 5),
            'overdueDays': random.randint(0, 60),
            'regulatoryChange': random.randint(0, 5),
            'materiality': random.randint(2, 5),
            'branchType': random.choice(BRANCH_TYPES),
            'productLine': random.choice(PRODUCTS),
            'note': random.choice(NOTES)
        })
    return items
