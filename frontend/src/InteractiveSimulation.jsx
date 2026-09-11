import { useEffect, useState } from 'react';

const steps = [
  'Synthetic vessel telemetry loaded',
  'Sea-ice concentration mapped',
  'TL3 iceberg detected',
  'Five-day trajectory generated',
  'AI route recalculated',
  'Operator approval required',
];

export default function InteractiveSimulation({ Header, Card, MapView }) {
  const [running, setRunning] = useState(false);
  const [step, setStep] = useState(0);
  const [approved, setApproved] = useState(false);
  const complete = step === steps.length;

  useEffect(() => {
    if (!running || complete) return undefined;
    const timer = setInterval(() => {
      setStep(current => {
        const next = Math.min(current + 1, steps.length);
        if (next === steps.length) setRunning(false);
        return next;
      });
    }, 1100);
    return () => clearInterval(timer);
  }, [running, complete]);

  const reset = () => { setStep(0); setRunning(false); setApproved(false); };

  return <>
    <Header eyebrow="Module / simulation lab" title="Simulation sandbox" detail="Run a synthetic scenario from hazard detection to an explainable route recommendation." />
    <section className="shell sim-layout">
      <Card><div className="panel-heading"><div><p className="eyebrow">Scenario runner</p><h2>Multi-hazard convergence</h2></div><span className="demo-tag">Synthetic data</span></div><div className="sim-controls"><label>Wind speed <input type="range" defaultValue="24" /></label><label>Ice density <input type="range" defaultValue="68" /></label><label>Vessel speed <input type="range" defaultValue="42" /></label></div><button className="button primary full" onClick={() => complete ? reset() : setRunning(value => !value)}>{complete ? 'Run again' : running ? 'Pause simulation' : step ? 'Resume simulation' : 'Run simulation'} <span>{running ? 'Ⅱ' : complete ? '↻' : '↗'}</span></button>{running && <p className="simulation-clock">LIVE SIMULATION · STEP {step} / {steps.length}</p>}</Card>
      <Card><p className="eyebrow">Event timeline</p><h2>Data → decision</h2><div className="timeline">{steps.map((event, index) => <div className={index < step ? 'done' : ''} key={event}><i />{event}<small>{index < step ? 'COMPLETE' : 'QUEUED'}</small></div>)}</div></Card>
    </section>
    {complete && <section className="shell simulation-result"><Card><div><p className="eyebrow">{approved ? 'Operator action recorded' : 'Simulation complete'}</p><h2>{approved ? 'AI ROUTE ACTIVE' : 'DYNAMIC AI ROUTE READY'}</h2><p className="muted">{approved ? 'The safer corridor is approved and ready for operator monitoring.' : 'The predicted iceberg intersection triggered a safer corridor for operator review.'}</p></div><div className="simulation-route-stats"><span><b>28</b>New risk score</span><span><b>17.2 d</b>Estimated ETA</span><span><b>1,240 L</b>Estimated fuel</span><span><b>78%</b>Intersection avoided</span></div><div className="button-row"><button className="button primary" onClick={() => setApproved(true)}>{approved ? 'AI route approved ✓' : 'Approve AI route ✓'}</button><button className="button quiet" onClick={reset}>Reset scenario</button></div></Card></section>}
    <section className="shell map-section"><div className="section-heading"><div><p className="eyebrow">Route output</p><h2>{complete ? 'Recommended corridor' : 'Live simulation map'}</h2></div>{complete && <span className="live-pill">● ROUTE READY</span>}</div><MapView /></section>
  </>;
}
