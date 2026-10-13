const test = require('node:test');
const assert = require('node:assert/strict');
const { evaluateAudit } = require('./audit.js');

const sample = {
  task_id: 'T1', target_identifier: 'KEY-01', primary_metric: 10,
  secondary_metric: 4, status_descriptor: 'NOMINAL', is_critical_flag: false
};

test('nominal threshold result never claims cryptographic assurance', () => {
  const result = evaluateAudit(sample);
  assert.equal(result.overall_urgency, 'ROUTINE');
  assert.equal(result.total_alerts, 0);
  assert.equal(result.cryptographic_assurance, 'NOT_ASSESSED');
  assert.equal(Object.hasOwn(result, 'audit_hash'), false);
});

test('strict thresholds match the backend workers', () => {
  const result = evaluateAudit({ ...sample, primary_metric: 25.1, secondary_metric: 12.1, status_descriptor: 'ANOMALY' });
  assert.equal(result.overall_urgency, 'ELEVATED_RISK');
  assert.equal(result.total_alerts, 3);
  assert.equal(evaluateAudit({ ...sample, primary_metric: 25, secondary_metric: 12 }).total_alerts, 0);
});

test('critical flag overrides elevated results', () => {
  assert.equal(evaluateAudit({ ...sample, is_critical_flag: true }).overall_urgency, 'CRITICAL_STAT_PANIC');
});

test('invalid payloads fail closed', () => {
  for (const change of [{ primary_metric: NaN }, { secondary_metric: Infinity },
    { target_identifier: ' ' }, { status_descriptor: '' }, { is_critical_flag: 'false' }]) {
    assert.throws(() => evaluateAudit({ ...sample, ...change }));
  }
});
