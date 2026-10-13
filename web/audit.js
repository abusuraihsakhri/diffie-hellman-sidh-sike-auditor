/* Deterministic, client-side demonstration of the legacy Python threshold rules.
   This is not an SIDH/SIKE implementation or cryptographic security assessment. */
(function (root) {
  'use strict';

  function evaluateAudit(input) {
    if (!input || typeof input !== 'object') throw new TypeError('Audit input is required');
    const taskId = String(input.task_id ?? '').trim();
    const target = String(input.target_identifier ?? '').trim();
    const descriptor = String(input.status_descriptor ?? '').trim();
    const primary = input.primary_metric;
    const secondary = input.secondary_metric;
    if (!taskId || !target || !descriptor) throw new Error('All identifier and descriptor fields are required');
    if (typeof primary !== 'number' || !Number.isFinite(primary) ||
        typeof secondary !== 'number' || !Number.isFinite(secondary)) {
      throw new Error('Both metrics must be finite numbers');
    }
    if (typeof input.is_critical_flag !== 'boolean') throw new Error('Critical flag must be boolean');

    const alerts = [];
    if (primary > 25) alerts.push({
      source: 'InvariantQCWorker', level: 'ELEVATED_RISK',
      detail: 'Primary metric is greater than the demonstration threshold of 25.'
    });
    if (input.is_critical_flag || secondary > 12) alerts.push({
      source: 'SafetyEscalationWorker',
      level: input.is_critical_flag ? 'CRITICAL_STAT_PANIC' : 'ELEVATED_RISK',
      detail: input.is_critical_flag
        ? 'The user-supplied critical flag is set.'
        : 'Secondary metric is greater than the demonstration threshold of 12.'
    });
    if (['DISCORDANT', 'ANOMALY', 'MUTANT', 'VIOLATION', 'FAIL', 'REJECT']
      .some(token => descriptor.toUpperCase().includes(token))) {
      alerts.push({
        source: 'ProtocolConformanceWorker', level: 'ELEVATED_RISK',
        detail: 'Descriptor contains a demonstration anomaly keyword.'
      });
    }
    const critical = alerts.some(a => a.level === 'CRITICAL_STAT_PANIC');
    const status = critical ? 'CRITICAL_STAT_PANIC' :
      alerts.length ? 'ELEVATED_RISK' : 'ROUTINE';
    return {
      task_id: taskId,
      target_identifier: target,
      overall_urgency: status,
      total_alerts: alerts.length,
      alerts,
      cryptographic_assurance: 'NOT_ASSESSED',
      security_notice: 'SIDH/SIKE are cryptographically broken. These arbitrary numerical rules do not validate any cryptosystem.',
      methodology: 'Offline demonstration mirroring the three legacy agents/workers threshold checks; no server or signing key is used.'
    };
  }

  if (typeof module !== 'undefined' && module.exports) module.exports = { evaluateAudit };
  if (typeof document === 'undefined') return;

  const form = document.getElementById('audit-form');
  if (!form) return;
  const output = document.getElementById('output');
  const status = document.getElementById('status');
  const count = document.getElementById('task-count');
  let processed = 0;

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const primaryRaw = document.getElementById('primary').value;
    const secondaryRaw = document.getElementById('secondary').value;
    try {
      if (!primaryRaw.trim() || !secondaryRaw.trim()) throw new Error('Enter both metrics');
      const result = evaluateAudit({
        task_id: document.getElementById('task-id').value,
        target_identifier: document.getElementById('target').value,
        primary_metric: Number(primaryRaw),
        secondary_metric: Number(secondaryRaw),
        status_descriptor: document.getElementById('descriptor').value,
        is_critical_flag: document.getElementById('critical').checked
      });
      processed++;
      count.textContent = String(processed);
      status.textContent = result.overall_urgency.replaceAll('_', ' ');
      status.dataset.level = result.overall_urgency;
      output.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
      status.textContent = 'INVALID INPUT';
      status.dataset.level = 'INVALID';
      output.textContent = String(error.message || error);
    }
  });
})(typeof globalThis !== 'undefined' ? globalThis : this);
