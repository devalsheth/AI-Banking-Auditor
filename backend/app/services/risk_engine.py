def score_records(records: list[dict]):
    scored = []
    for row in records:
        impact = int(row.get('impact', 3))
        likelihood = int(row.get('likelihood', 3))
        open_findings = int(row.get('openFindings', 0))
        repeat_issues = int(row.get('repeatIssues', 0))
        control_maturity = int(row.get('controlMaturity', 3))
        overdue_days = int(row.get('overdueDays', 0))
        reg_change = int(row.get('regulatoryChange', 0))
        materiality = int(row.get('materiality', 3))
        score = round(
            open_findings * 4.2 +
            repeat_issues * 6 +
            (6 - control_maturity) * 8 +
            min(overdue_days, 60) * 0.55 +
            reg_change * 6 +
            materiality * 5 +
            impact * 4 + likelihood * 3
        )
        score = min(score, 100)
        level = 'critical' if score >= 80 else 'high' if score >= 65 else 'medium' if score >= 45 else 'low'
        drivers = []
        if open_findings >= 6: drivers.append('High volume of unresolved findings')
        if repeat_issues >= 3: drivers.append('Repeated issues across audit cycles')
        if control_maturity <= 2: drivers.append('Weak control maturity in critical process')
        if overdue_days >= 30: drivers.append('Remediation actions significantly overdue')
        if reg_change >= 4: drivers.append('Recent regulatory changes require added scrutiny')
        if materiality >= 4: drivers.append('High materiality process with significant financial impact')
        if not drivers: drivers.append('Routine audit monitoring recommended')
        recommendation = (
            'Immediate focused audit with senior reviewer and expanded sampling.' if score >= 80 else
            'Schedule in next audit cycle with increased testing.' if score >= 65 else
            'Monitor monthly and validate remediation progress.' if score >= 45 else
            'Handle through routine control testing.'
        )
        scored.append({
            **row,
            'score': score,
            'level': level,
            'drivers': drivers,
            'recommendation': recommendation
        })
    return sorted(scored, key=lambda x: x['score'], reverse=True)
