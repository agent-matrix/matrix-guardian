import React from 'react';
import { Radio } from 'lucide-react';
import Card from '../components/common/Card';
import { ProbesTable } from '../components/probes';

/**
 * ProbesView Component
 * View for displaying health probes and monitors
 *
 * @param {Object} props
 * @param {Array} props.probes - Array of probe objects
 */
const ProbesView = ({ probes }) => (
  <Card title="Probes & Health Monitors" icon={Radio} className="h-full">
    <ProbesTable probes={probes} />
  </Card>
);

export default ProbesView;
