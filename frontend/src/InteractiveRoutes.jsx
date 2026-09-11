import { useState } from 'react';

const routeOptions = [
  ['DIRECT', 'HIGH', '14 days', '1,110 L', 'Not advised'],
  ['MODERATE DEVIATION', 'MEDIUM', '16.5 days', '1,280 L', 'Acceptable'],
  ['SAFETY-FIRST', 'LOW', '19 days', '1,420 L', 'Recommended'],
  ['DYNAMIC AI', 'ADAPTIVE', 'Variable', 'Optimized', 'AI optimized'],
];

function RouteCard({ option, index }) {
  const [name, risk, eta, fuel, note] = option;
  return <article className={`route-option ${index === 2 ? 'recommended' : ''}`}>
    <span>0{index + 1}</span><h3>{name}</h3><b className={`risk-${risk.toLowerCase()}`}>{risk} RISK</b>
    <div><small>ETA <strong>{eta}</strong></small><small>FUEL <strong>{fuel}</strong></small></div><p>{note}</p>
  </article>;
}

export default function InteractiveRoutes({ Header, Card }) {
  const [tolerance, setTolerance] = useState('MEDIUM');
  const [status, setStatus] = useState('pending');
  const [reviewing, setReviewing] = useState(false);
  const statusCopy = {
    pending: ['TL3 ICEBERG ALERT', 'Intersection probability: 78% · Time to intersection: 9 hours', 'New AI route reduces risk from 76 to 28 with a 1.2 day ETA increase.'],
    review: ['REROUTE REVIEW MODE', 'Compare the route options before approving the change.', 'Safety-first route lowers projected risk to 28 with a 1.2 day ETA increase.'],
    approved: ['REROUTE APPROVED', 'New AI route is active for operator monitoring.', 'Risk reduced from 76 to 28. Continue monitoring the corridor.'],
    rejected: ['ALERT DISMISSED', 'The reroute was rejected by the operator.', 'The original route remains selected. Review operational data before continuing.'],
  }[status];
  return <>
    <Header eyebrow="Module 03 / AI routing" title="Route intelligence" detail="Compare four route strategies and inspect why the dynamic AI route is preferred." />
    <section className="shell route-layout">
      <Card><p className="eyebrow">Operator preference</p><h2>Risk tolerance</h2><div className="segmented">{['LOW', 'MEDIUM', 'HIGH'].map(value => <button type="button" className={tolerance === value ? 'active' : ''} onClick={() => setTolerance(value)} key={value}>{value}</button>)}</div><div className="route-explanation"><span>WHY THIS ROUTE?</span><p>✓ Lower ice concentration<br />✓ Avoids TL3 iceberg zone<br />✓ Safer for vessel draught<br />✓ Acceptable fuel increase</p></div></Card>
      <div className="route-options">{routeOptions.map((option, index) => <RouteCard key={option[0]} option={option} index={index} />)}</div>
    </section>
    <section className="shell reroute"><Card><div className={`alert ${status === 'approved' ? 'resolved' : status === 'rejected' ? 'dismissed' : 'red'}`}><strong>{statusCopy[0]}</strong><span>{statusCopy[1]}</span><small>{statusCopy[2]}</small></div><div className="button-row"><button type="button" className="button primary" onClick={() => { setStatus('approved'); setReviewing(false); }}>{status === 'approved' ? 'Reroute approved ✓' : 'Approve reroute'}</button><button type="button" className="button quiet" onClick={() => { setStatus('review'); setReviewing(true); }}>Review reroute</button><button type="button" className="button quiet" onClick={() => { setStatus('rejected'); setReviewing(false); }}>Reject</button></div>{reviewing && <span className="review-note">Review mode active · route comparison is ready for operator decision.</span>}</Card></section>
  </>;
}
