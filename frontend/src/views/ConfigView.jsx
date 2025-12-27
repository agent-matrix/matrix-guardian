import React from 'react';
import {
  PolicyViewer,
  ConfigurationFlags,
  WorkerStatus,
} from '../components/config';
import { MOCK_CONFIG_FLAGS } from '../data/mockData';

/**
 * ConfigView Component
 * View for displaying policy configuration and system settings
 *
 * @param {Object} props
 * @param {string} props.policy - Policy YAML string
 */
const ConfigView = ({ policy }) => (
  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
    <PolicyViewer policy={policy} />

    <div className="flex flex-col gap-6">
      <ConfigurationFlags flags={MOCK_CONFIG_FLAGS} />
      <WorkerStatus />
    </div>
  </div>
);

export default ConfigView;
